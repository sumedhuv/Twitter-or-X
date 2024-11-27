/* Q5 a query that returns "how exactly the advertisers target the user; 
that is, you want to see the top ten advertisers and, for each of these ten advertisers, 
their top ten combinations of targeting type and targeting value".

The query should return a table with three columns labeled 
"Advertiser" (text), "Criteria Type" (text), and "Criterion" (text).

The query should not modify the database and be a single SQL statement.  */

WITH TopAdvertisers AS (
    SELECT advertiserInfo, COUNT(*) AS ad_count
    FROM impressions
    GROUP BY advertiserInfo
    ORDER BY ad_count DESC
    LIMIT 10
),
TargetingDetails AS (
    SELECT 
        i.advertiserInfo,
        tc.targetingType,
        tc.targetingValue,
        COUNT(*) AS combination_count
    FROM impressions i
    JOIN matchedTargetingCriteria mtc ON i.id = mtc.impression
    JOIN TargetingCriteria tc ON mtc.criteria = tc.id
    GROUP BY i.advertiserInfo, tc.targetingType, tc.targetingValue
),
TopTargetingCombinations AS (
    SELECT 
        td.advertiserInfo,
        td.targetingType,
        td.targetingValue,
        td.combination_count,
        RANK() OVER (PARTITION BY td.advertiserInfo ORDER BY td.combination_count DESC) AS rank
    FROM TargetingDetails td
)
SELECT 
    ta.advertiserInfo,
    ttc.targetingType,
    ttc.targetingValue,
    ttc.combination_count
FROM TopAdvertisers ta
JOIN TopTargetingCombinations ttc ON ta.advertiserInfo = ttc.advertiserInfo
WHERE ttc.rank <= 10
ORDER BY ta.advertiserInfo, ttc.combination_count DESC;
