# Twitter Ads Analytics Project

Welcome to the **Twitter Ads Analytics** project! This repository contains my completed assignment for analyzing Twitter ads impressions data using an ETL process to create a relational database and generate analytics queries.

## Project Overview

In this project, I explored and transformed Twitter impressions data into a SQL database, enabling insightful analytics about advertisements shown to a Twitter user. The goal was to help users better understand why Twitter displays certain ads, aligning with the mission of **Scryer**—a personal analytics company dedicated to empowering users to understand their data.
You can request your own data as described here: https://help.twitter.com/en/managing-your-account/how-to-download-your-twitter-archive
## Data Overview

The project focuses on data from a user's personal Twitter archive, specifically the `ad-impressions.js` file. This file contains JSON data with the following key components:

- **ad**: Metadata about the promoted tweets the user viewed.
- **deviceInfo**: Information about the device used (e.g., device ID, operating system).
- **displayLocation**: The location where the ad appeared on Twitter.
- **promotedTweetInfo**: Details about the promoted tweet, including unique ID, text, URLs, and media.
- **advertiserInfo**: Information about the advertiser (e.g., name, screen name).
- **matchedTargetingCriteria**: Criteria used to target the user with the ad.
- **impressionTime**: Timestamp of when the ad was viewed.

## Database Structure

A provided normalized SQL database schema, `twitterads.db`, captures the structure of the data. The schema includes integrity constraints to ensure data consistency.

### Tools and Technologies
- **Python**: Used for the ETL (Extract-Transform-Load) process.
- **SQLite**: Used to store and query the structured data.

## Tasks

### Task 1: ETL Process
I developed a Python script to perform the following:
1. **Extract**: Load JSON data from `ad-impressions.js`.
2. **Transform**: Clean, normalize, and handle irregularities in the data.
3. **Load**: Populate the `twitterads.db` SQLite database.

### Task 2: SQL Queries
I crafted the following analytical queries to extract insights from the database:
1. **Total Ads**: Count the total number of ads shown to the user.
2. **Unique Advertisers**: Count the number of unique advertisers targeting the user.
3. **Top Targeting Types**: Identify the top 10 targeting types and their associated ad counts.
4. **Ads by Time of Day**: Count ads by the hour of the day they were shown.
5. **Advertiser Targeting Details**: For the top 10 advertisers, list their top 10 targeting type-value combinations.

## How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/sumedhuv/Twitter-or-X.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Twitter-or-X
   ```
3. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the ETL script:
   ```bash
   python load_ad_json.py
   ```
5. Open the `twitterads.db` file using your preferred SQLite client to run the analytical queries.

## Results and Insights

This project generated detailed insights about the user's Twitter ads, including:
- Total ad impressions.
- Advertiser diversity.
- Common targeting strategies.
- Ad targeting trends based on time.
- Detailed analysis of top advertisers' targeting methods.

## Contributing

Feel free to fork this repository, open issues, or submit pull requests to enhance the project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Thank you for exploring my project!
