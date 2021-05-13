import twint
from Scweet.user import *


def find_all_tweets(keywords, limit=20):
    for keyword in keywords:
        c = twint.Config()
        c.Search = keyword
        c.Limit = limit
        c.Pandas = True
        c.Hide_output = True

        twint.run.Search(c)

    result = twint.storage.panda.Tweets_df[['id', 'username', 'name', 'tweet', 'retweet']]
    twint.storage.panda.clean()
    return result


def find_user_tweets(keywords, username, limit=20):
    for keyword in keywords:
        c = twint.Config()
        c.Search = keyword
        c.Username = username
        c.Limit = limit
        c.Pandas = True
        c.Hide_output = True

        twint.run.Search(c)

    tweets_df = twint.storage.panda.Tweets_df

    if tweets_df.empty:
        return tweets_df

    twint.storage.panda.clean()
    return tweets_df[['id', 'username', 'name', 'tweet', 'retweet']]


def all_user_tweets(username, limit=20):
    c = twint.Config()
    c.Search = "from:@" + username
    c.Limit = limit
    c.Pandas = True
    c.Hide_output = True

    twint.run.Search(c)

    tweets_df = twint.storage.panda.Tweets_df

    if tweets_df.empty:
        return tweets_df

    twint.storage.panda.clean()
    return tweets_df[['id', 'username', 'name', 'tweet', 'retweet']]


def user_summary(username):
    retry = 0
    info = get_user_information([username], headless=True)
    while not info and retry < 3:
        info = get_user_information([username], headless=True)
        retry += 1
    if not info:
        return None
    return info[username]


def find_followings(user, limit=500):
    followings = get_users_following(users=[user], verbose=0, headless = True, wait=1.2)[user]
    return list(map(lambda x: x.replace('@', ''), followings))[:limit]