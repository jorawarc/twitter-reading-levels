# CMPT 353 - Deducing user reading levels from tweets
## Getting the data
To gather Tweets from specific users, we had three options, scraping data from Twitter directly, leveraging Twitter's API, or searching for third-party collections.
We decided to leverage Twitter's existing developer API to gather tweets, however, this meant we were limited to 3200 tweets per user.

This route also allowed us simplified development as numerous python libraries have been created to interface with the API, abstracting the underlying network requests.
We have chose to use `python-twitter` as it is the most up-to-date library and still being actively maintained.

Script `01_get_data.py` uses the `python-twitter` library to gather the last 3200 tweets for a user from `users.txt`. 
The script then outputs the tweets to a `screen_name.csv` file with the header `created_at, text`.

###Limitations
This script does not do any data cleaning. As a result some artifacts like url the url encoding of special characters and emoji are still persistent in the data. 
Additionally, Twitter's API does not make a distinction between Retweets and Tweets.


| # | script | purpose |
| :---: | :---: | :---: |
| 1 | `01_get_data.py` | Collect user tweets and output them to individual csv files 