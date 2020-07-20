import sys
import os
import pandas as pd
import numpy as np
import re
import emoji

def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(u'', text)

def remove_at(text):
	return re.sub('@[^\s]+','',text)

def remove_symbols(text):
	return re.sub(r'([^\s\w]|_)+', '', text)

	
files = [i for i in os.listdir("user_tweets") if i.endswith("csv")]

for file in files:
	#read each csv file one at a time and process them
	data = pd.read_csv("user_tweets/"+str(file))

	#remove emojis
	data['text'] = data['text'].apply(lambda k: remove_emoji(k))

	#remove links
	data['text'] = data['text'].str.strip()
	data['text'] = data['text'].str.replace('http\S+|www.\S+', '', case=False)

	#remove @
	data['text'] = data['text'].apply(lambda x: remove_at(x))

	#remove symbols
	data['text'] = data['text'].apply(lambda n: remove_symbols(n))

	#remove retweets
	data = data[~data.text.str.startswith('RT')]

	#drop empty rows
	data.dropna(axis=0, how='all')
	#data['text'] = data['text'].replace('', np.nan, inplace=True)
	#reset index
	data.reset_index()
	#Write to CSV
	data.to_csv("Cleaned_user_tweets/Cleaned_"+str(file), index=False)
