# CMPT 353 - Deducing user reading levels from tweets
## Getting the data
To gather Tweets from specific users, we had three options, scraping data from Twitter directly, leveraging Twitter's API, or searching for third-party collections.
We decided to leverage Twitter's existing developer API to gather tweets, however, this meant we were limited to 3200 tweets per user.

This route also allowed us simplified development as numerous python libraries have been created to interface with the API, abstracting the underlying network requests.
We have chose to use `python-twitter` as it is the most up-to-date library and still being actively maintained.

Script `01_get_data.py` uses the `python-twitter` library to gather the last 3200 tweets for a user from `users.txt`. 
The script then outputs the tweets to a `screen_name.csv` file with the header `created_at, text`.

# Calculating reading level
We used a library called textstat to calculate the reading level of our twitter candidates. We used the following algorithms.

The Flesch Reading Ease formula - returns the difficulty of text given. Max score is 121.22 
Score	Difficulty
90-100	Very Easy
80-89	Easy
70-79	Fairly Easy
60-69	Standard
50-59	Fairly Difficult
30-49	Difficult
0-29	Very Confusing

The Flesch-Kincaid Grade Level - Returns the Flesch-Kincaid Grade of the given text. This is a grade formula in that a score of 9.3 means that a ninth grader would be able to read the document.

Automated Readability index - Returns the ARI (Automated Readability Index) which outputs a number that approximates the grade level needed to comprehend the text.
if the ARI is 6.5, then the grade level to comprehend the text is 6th to 7th grade.

The Coleman-Liau Index - Returns the grade level of the text using the Coleman-Liau Formula. This is a grade formula in that a score of 9.3 means that a ninth grader would be able to read the document.

Dale-Chall Readability Score - Uses a lookup table of the 3000 most commonly used English words. Returns the grade level of the text given.

Score	Understood by
4.9 or lower	average 4th-grade student or lower
5.0–5.9	average 5th or 6th-grade student
6.0–6.9	average 7th or 8th-grade student
7.0–7.9	average 9th or 10th-grade student
8.0–8.9	average 11th or 12th-grade student
9.0–9.9	average 13th to 15th-grade (college) student

Readability Consensus based upon all the above tests - Based upon all the above tests, returns the estimated school grade level required to understand the text.


### Limitations
This script does not do any data cleaning. As a result some artifacts like url the url encoding of special characters and emoji are still persistent in the data. 
Additionally, Twitter's API does not make a distinction between Retweets and Tweets.


| # | script | purpose |
| :---: | :---: | :---: |
| 1 | `01_get_data.py` | Collect user tweets and output them to individual csv files
| 2 | `02_clean_data.py` | Remove artifacts from tweets (emojis, retweets, etc.)
| 3 | `03_combine_data.py` | Consolidate all the collected data into a single pandas data frame