import matplotlib.pyplot as plt
import os
import sys
import pandas as pd
from scipy import stats
combine_data = __import__('03_combine_data')  # import file with improper name

# (Optional) ML algorithm to predict reading level

TITLE_MAP = {'dale_chall_readability_score': 'Dale-Chall Readability Score',
             'flesch_kincaid': 'Flesch-Kincaid Readability Score',
             'automated_readability': 'Automated Readability Readability Score',
             'flesch_reading': 'Flesch Reading Readability Score',
             'coleman_liau_index': 'Coleman-Liau Index'}

METRICS = ['dale_chall_readability_score', 'flesch_kincaid', 'automated_readability', 'flesch_reading',
           'coleman_liau_index']


def plot_reading_levels_over_time(users, tweets_dir):
    for metric in METRICS:
        fig, ax = plt.subplots()
        for user in users['screen_name']:
            tweet_data = combine_data.get_tweets(user, users, tweets_dir)
            grouped = tweet_data[['created_at', metric]].groupby(pd.Grouper(key='created_at', freq='6M')).median()
            ax.plot(grouped.index.values, grouped[metric])
        ax.legend(users['screen_name'])
        title = '{} over Time'.format(TITLE_MAP[metric])
        ax.set_title(title)
        ax.set_xlabel('Time')
        ax.set_ylabel('Reading Level Unit')
    plt.show()


def get_group(users, tweets_dir):
    groups = []
    for user in users['screen_name']:
        tweet_data = combine_data.get_tweets(user, users, tweets_dir)
        tweet_data['screen_name'] = user
        groups.append(tweet_data)
    g = pd.concat(groups)
    return g


def plot_all_metrics(groups, legend, title_template):
    for m in METRICS:
        fig, ax = plt.subplots()
        for i in groups:
            grouped = i[['created_at', m]].groupby(pd.Grouper(key='created_at', freq='6M')).median()
            ax.plot(grouped.index.values, grouped[m])
        ax.legend(legend)
        ax.set_title(title_template.format(TITLE_MAP[m]))
        ax.set_xlabel("Time")
        ax.set_ylabel('Reading Level Unit')
    plt.show()


def group_by_gender(users, tweets_dir):
    male_users = users[users['gender'].str.match('male')]
    female_users = users[users['gender'].str.match('female')]

    males = get_group(male_users, tweets_dir)
    females = get_group(female_users, tweets_dir)

    compute_ttest(males, females)

    plot_all_metrics([males, females], ['Male Users', 'Female Users'], 'Men vs Women ({})')


def compute_ttest(x1, x2):
    for m in METRICS:
        grouped_x1 = x1[['created_at', m]].groupby(pd.Grouper(key='created_at', freq='6M')).median()
        grouped_x2 = x2[['created_at', m]].groupby(pd.Grouper(key='created_at', freq='6M')).median()
        result = stats.ttest_ind(grouped_x1[m], grouped_x2[m])
        print("{}: pvalue = {}".format(m, result.pvalue))


def group_by_political(users, tweets_dir):
    political = users[users['is_political']]
    non_political = users[users['is_political'] == False]

    politicians = get_group(political, tweets_dir)
    non_politicians = get_group(non_political, tweets_dir)

    compute_ttest(politicians, non_politicians)

    plot_all_metrics([politicians, non_politicians], ['Politicians', 'Non-Politicians'],
                     'Politicians vs Non-Politicians ({})')


def group_by_year(users, tweets_dir):
    user_tweets = get_group(users, tweets_dir)
    before_2017 = user_tweets[user_tweets['created_at'].dt.year <= 2017]
    after_2017 = user_tweets[user_tweets['created_at'].dt.year > 2017]

    compute_ttest(before_2017, after_2017)


def compare_users(users, tweets_dir, screen_name1, screen_name2):
    u1 = users[users['screen_name'].str.match(screen_name1)]
    u2 = users[users['screen_name'].str.match(screen_name2)]

    u1_tweets = get_group(u1, tweets_dir)
    u2_tweets = get_group(u2, tweets_dir)
    plot_reading_levels_over_time(users[(users['screen_name'].str.match(screen_name1)) | (users['screen_name'].str.match(screen_name2))], tweets_dir)
    compute_ttest(u1_tweets, u2_tweets)


def main(user_file, tweets_dir):
    users = combine_data.collect_data(user_file, *os.listdir(tweets_dir))

    compare_users(users, tweets_dir, "BarackObama", "realDonaldTrump")
    #group_by_year(users, tweets_dir)
    #group_by_political(users, tweets_dir)
    #plot_reading_levels_over_time(users.head(5), tweets_dir)
    #group_by_political(users, tweets_dir)


if __name__ == '__main__':
    # users.csv Cleaned_user_tweets
    main(sys.argv[1], sys.argv[2])
