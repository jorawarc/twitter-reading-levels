import sys
import os
import pandas as pd
import numpy as np
import re
import emoji

def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(' ', text)


def remove_at(text):
	return re.sub('@[^\s]+', ' ', text)


def remove_symbols(text):
	return re.sub(r'([^\s\w]|_)+', ' ', text)


def remove_whitespace(text):
	text = text.lstrip()
	text = text.rstrip()
	return text


def remove_links(text):
	return re.sub('http\S+|www.\S+', ' ', text)


def main():
	
	files = [i for i in os.listdir("user_tweets") if i.endswith("csv")]
	
	for file in files:
		#read each csv file one at a time and process them
		data = pd.read_csv("user_tweets/"+str(file))
	
		#remove emojis
		data['text'] = data['text'].apply(lambda j: remove_emoji(j))

		#remove links
		data['text'] = data['text'].apply(lambda k: remove_links(k))

		#remove @
		data['text'] = data['text'].apply(lambda l: remove_at(l))

		#remove symbols
		data['text'] = data['text'].apply(lambda n: remove_symbols(n))

		#remove retweets
		data = data[~data.text.str.startswith('RT')]

		#clean white spaces
		data = data[~data['text'].apply(lambda l: l.isspace())]
		data['text'] = data['text'].apply(lambda p: remove_whitespace(p))
		
		#Write to CSV
		data.to_csv("Cleaned_user_tweets/Cleaned_"+str(file), index=False)

if __name__ == '__main__':
    main()