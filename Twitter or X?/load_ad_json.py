import json
import sqlite3
import argparse
from pathlib import Path
# Needs to be at least Python version 3.6

# DO NOT IMPORT ANY OTHER MODULES!

# Please make sure you don't add any "print" statements in your final version.
# Only existing prints should write to the terminal!
# If you "print" to help with development or debugging, make sure to remove them
# before you submit!


# YOU DO NOT NEED TO MODIFY THIS FUNCTION
# If you break this function, you likely break the whole script, so
# it's best not to touch it.
def load_json_from_js(p):
    """Takes a path to Twitter ad impression data and returns parsed JSON.
    
    Note that the Twitter files are *not* valid JSON but a Javascript file
    with a blog of JSON assigned to a Javascript variable, so some 
    preprocessing is needed.""" 
  
    # Note that this is a horrid hack. It's *fragile* i.e., if Twitter changes it's
    # variable name (currently "window.YTD.ad_engagements.part0 =") this will break.
    # It also requires loading the entire string into memory before parsing. If we're
    # running this on user machines on their own data this is probably fine, but if 
    # we're running it on a server the fact that we have the entire string AND the entire
    # parsed JSON structure in memory will add up.
    
    # If we use the standard json module, then there's no advantage to *not* doing this
    # if we want to json.load the file...it brings the string into memory anyway.
    #     https://pythonspeed.com/articles/json-memory-streaming/
    # We'd need to handle buffering ourselves or explore existing streaming solutions 
    # like:
    #     https://pypi.org/project/json-stream/
    # But then we'll have to play some tricks to avoid the junk at the beginning.
    #
    # Also, the weird, pointless, top level objects might break streaming. So we might
    # need to do a LOT of preprocessing.
    
    # ... further investigation of json-stream suggests it can handle the junk ok!
    #     https://github.com/daggaz/json-stream 
    return json.loads(p.read_text()[33:])


# Don't touch this function!
def populate_db(adsjson, db):
    """Takes a blob of Twitter ad impression data and pushes it into our database.
    
    Note that this is responsible for avoiding redundant entries. Furthermore,
    it should be robust to errors and always get as much data in as it can.
    """ 
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        json2db(adsjson, cur)
    except:
        #We'd prefer no exceptions reached this level.
        print("There was a problem with the loader. This shouldn't happen")
    conn.commit()
    conn.close()

def populate_deviceInfo(adsjson,cur):
    result={}

    for item in adsjson:
        impressions = item["ad"]["adsUserData"]["adImpressions"]["impressions"]

        for each in impressions:

            os_type = each["deviceInfo"]["osType"]
            if("deviceId" in each["deviceInfo"]): 
                device_id = each["deviceInfo"]["deviceId"] 
            else:
                device_id = os_type 
                
                
            if("deviceType" in each["deviceInfo"]):
                device_type = each["deviceInfo"]["deviceType"]
            else:
                device_type = os_type
                
            result[device_id]=[device_type,os_type]

    for key in result:
            cur.execute("INSERT INTO deviceInfo(deviceId, deviceType,osType) VALUES (?, ?, ?)",
                    (key, result[key][0],result[key][1]))


def populate_promotedTweetInfo(adsjson,cur):
    result={}
    for item in adsjson:
        impressions = item["ad"]["adsUserData"]["adImpressions"]["impressions"]
        for every in impressions:
            if "promotedTweetInfo" in every:
                tweetId= every["promotedTweetInfo"]["tweetId"]
                tweetText= every["promotedTweetInfo"]["tweetText"]
                urls= every["promotedTweetInfo"]["urls"]
                mediaUrls= every["promotedTweetInfo"]["mediaUrls"]

                result[tweetId]=[tweetText,urls,mediaUrls]

    for key in result:
                cur.execute("INSERT INTO promotedTweetInfo(tweetId,tweetText, urls,mediaUrls) VALUES (?, ?, ?, ?)",
                                (key,result[key][0],str(result[key][1]),str(result[key][2])))
            
def populate_advertiserInfo(adsjson,cur):
    result={}

    for item in adsjson:
        impressions = item["ad"]["adsUserData"]["adImpressions"]["impressions"]

        for each in impressions:
            advertiserInfo= each["advertiserInfo"]
            if("advertiserName" in advertiserInfo): 

                advertiserName = advertiserInfo["advertiserName"]
            else:
                continue 
        
            if("screenName" in advertiserInfo): 
                screenName = advertiserInfo["screenName"]
            else:
                screenName= ""

            if(advertiserName in result):
                if(screenName not in result[advertiserName]):
                    result[advertiserName]= result[advertiserName] +", "+ screenName
            else:
                result[advertiserName]= screenName


    for key in result:
                cur.execute("INSERT INTO advertiserInfo(advertiserName, screenName) VALUES (?, ?)",
                        (key, result[key]))
                
def populate_TargetingCriteria(adsjson,cur):
    result={}
    i=1
    for item in adsjson:
        impressions = item["ad"]["adsUserData"]["adImpressions"]["impressions"]
        for every in impressions:
            matchedTargetingCriteria= every["matchedTargetingCriteria"]
            for each in matchedTargetingCriteria:
    
                if("targetingType" in each): 
                    targetingType = each["targetingType"]
                else:
                    targetingType = each.get("")
                    
                if("targetingValue" in each): 
                    targetingValue = each["targetingValue"]
                else:
                    targetingValue=each.get("")
                    
                result[targetingValue,targetingType]=targetingType
                    
    for key in result:
                
                cur.execute("INSERT INTO TargetingCriteria(id,targetingValue, targetingType) VALUES (?, ?, ?)",
                                    (i, key[0], result[key]))  
                i=i+1
                
def populate_matchedTargetingCriteria(adsjson,cur):
    result = {}
    i = 1

    unique_targeting_values = []


    for item in adsjson:
        impressions = item["ad"]["adsUserData"]["adImpressions"]["impressions"]
        
        for every in impressions:
                
            targeting_values = {each["targetingValue"] for each in every["matchedTargetingCriteria"] if "targetingValue" in each}
            unique_targeting_values.extend(targeting_values)

    cur.execute("SELECT targetingValue, id FROM TargetingCriteria WHERE targetingValue IN ({})".format(','.join('?' for _ in tuple(set(unique_targeting_values)))), tuple(set(unique_targeting_values)))
    rows = cur.fetchall()

    value_to_id = {row[0]: row[1] for row in rows}


    for item in adsjson:
        impressions = item["ad"]["adsUserData"]["adImpressions"]["impressions"]
        
        for every in impressions:
            impressionID = i
            criteriaset = []

            for each in every["matchedTargetingCriteria"]:
                    
                if "targetingValue" in each:
                    criteriaset.append(value_to_id.get(each["targetingValue"]))
                else:
                    criteriaset.append(value_to_id.get(""))

            result[impressionID] = criteriaset
            i += 1

    for key in result:
                for each in result[key]:
                    cur.execute("INSERT INTO matchedTargetingCriteria(impression,criteria) values (?, ?)",(key, each))

def populate_impressions(adsjson,cur):
    result={}
    count=0
    for item in adsjson:
        impressions = item["ad"]["adsUserData"]["adImpressions"]["impressions"]
        for every in impressions:
            count+=1
            if "deviceId" in every["deviceInfo"]:
                    
                deviceInfo= every["deviceInfo"]["deviceId"]
            else:
                    deviceInfo=every["deviceInfo"]["osType"]

            displayLocation= every["displayLocation"]
            impressionTime= every["impressionTime"]
            if "promotedTweetInfo" in every:
                    tweetInfo = every["promotedTweetInfo"]["tweetId"]  
            else: 
                tweetInfo= ""
            
            if "advertiserName" in every["advertiserInfo"]:
                    
                advertiserInfo= every["advertiserInfo"]["advertiserName"]
            else:
                    advertiserInfo=""

            result[count]=[deviceInfo,displayLocation,tweetInfo,advertiserInfo,impressionTime]


    for key in result:
                cur.execute("INSERT INTO impressions(id,deviceInfo, displayLocation,promotedTweetInfo,impressionTime,advertiserInfo) VALUES (?, ?, ?, ?, ?, ?)",
                                    (key, result[key][0],result[key][1],result[key][2],result[key][4],result[key][3]))
     
def json2db(adsjson, cur):
    """Processes the JSON and INSERTs it into the db via the cursor, cur"""

    # cur.execute("DELETE FROM TargetingCriteria;")
    # cur.execute("DELETE FROM advertiserInfo;")
    # cur.execute("DELETE FROM deviceInfo;")
    # cur.execute("DELETE FROM impressions;")
    # cur.execute("DELETE FROM matchedTargetingCriteria;")
    # cur.execute("DELETE FROM promotedTweetInfo;")

    populate_deviceInfo(adsjson,cur)
    populate_promotedTweetInfo(adsjson,cur)
    populate_advertiserInfo(adsjson,cur)
    populate_TargetingCriteria(adsjson,cur)
    populate_matchedTargetingCriteria(adsjson,cur)
    populate_impressions(adsjson,cur)


    # THIS IS WHAT YOU SHOULD MODIFY!
    # Feel free to add helper functions...you don't *need* to make a giant
    # hard to test function...indeed, that will come up in code review!
    pass


# DO NOT MODIFY ANYTHING BELOW!
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Load JSON from Twitter's ad-impressions.js into our database.")
    parser.add_argument('--source',  
                        type=Path,
                        default=Path('./ad-impressions.js'),
                        help='path to source  file')    
    parser.add_argument('--output', 
                        type=Path,
                        default=Path('./twitterads.db'),
                        help='path to output DB')    
    args = parser.parse_args()
    
    print('Loading JSON.')
    ads_json = load_json_from_js(args.source)
    print('Populating database.')    
    populate_db(ads_json, args.output)
    print('Done')