import sys
import os
import pandas as pd
import re

files = [i for i in os.listdir("user_tweets") if i.endswith("csv")]

#for file in files:
data = pd.read_csv("user_tweets/"+str(files[0]),index_col=None, header=0)
#data.astype(str).apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))

#delete retweets
data = data[~data.text.str.startswith('RT')]

#remove links
data['trimmed'] = data['text'].str.replace('http\S+|www.\S+', '', case=False)

#remove emojis
data['trimmed'] = data['trimmed'].str.replace("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)aa
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", '',flags=re.UNICODE)

#remove images
#data['trimmed'] = data.drop(data['trimmed'].astype(str).str.startswith('RT'))


data.to_csv('edit.csv', index=False, header=False)
print(data)
