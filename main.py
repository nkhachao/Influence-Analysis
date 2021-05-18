import networkx as nx

from Crawler import *
from Grapher import *
from UserManager import *
from SentimentAnalyzer import *

import pandas as pd
import numpy as np
import time
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 5)
pd.set_option('display.width', None)


# ----- Find followings -----
def get_user_opinion(username):
    tweets = find_user_tweets(keywords, username)
    if tweets.empty:
        return None
    return positivity(tweets['tweet'])


def string_to_int(string):
    if "K" in string:
        value = float(string.replace("K", ""))
        return int(value * 1000)
    if "M" in string:
        value = float(string.replace("M", ""))
        return int(value * 1000000)

    return int(string.replace(",", ""))


# ------------------------------------ LETS GO ------------------------------------
keywords = ['Biden']

unfinished = True

# Data collection
while unfinished:
    try:
        scan_count = 5

        previous_session = load_user_discovery_session()
        if previous_session:
            base_users, discovered_users, previous_scan, following_dict, opinion_dict = previous_session
        else:
            following_dict = dict()
            opinion_dict = dict()
            discovered_users = []
            previous_scan = 0
            # ----- Find base users -----
            base_tweets = find_all_tweets(keywords)
            base_users = base_tweets['username'].unique()[:30]
            # ----- Find base users' opinion -----
            opinions = np.array(list(map(get_user_opinion, base_users)))
            for i in range(len(base_users)):
                opinion_dict[base_users[i]] = opinions[i]

        print(base_users)

        for scan in range(previous_scan, scan_count):
            for user in base_users:
                if user in following_dict:
                    continue

                user_info = user_summary(user)
                if not user_info or string_to_int(user_info[0]) > 300:
                    following_dict[user] = np.array([])
                    continue

                followings = np.array(find_followings(user, 100))
                opinions = np.array(list(map(get_user_opinion, followings)))
                relevant_opinions = opinions != None   # Filter users with no opinion

                followings = followings[relevant_opinions]      # Filter irrelevant users
                opinions = opinions[relevant_opinions]

                for i in range(len(followings)):
                    opinion_dict[followings[i]] = opinions[i]
                following_dict[user] = followings
                discovered_users += followings.tolist()
                save_user_discovery_session(base_users, discovered_users, scan, following_dict, opinion_dict)

            base_users = list(filter(lambda x: x not in following_dict, discovered_users))   # filter user already discovered
            print(len(base_users), "new users discovered")
            discovered_users = []

        # ----- Data collection completed -----
        unfinished = False

    except:
        unfinished = True
        print("problem occurred. sleeping")
        time.sleep(180)
        print("program restarted")


following_dict = load_data("following_dict")
opinion_dict = load_data("opinion_dict")

all_users = list(following_dict.keys()) + [item for sublist in following_dict.values() for item in sublist]
negative_users = filter(lambda x: opinion_dict[x] <= 0.64, all_users)

Graph = create_graph(following_dict)
Negative_graph = Graph.subgraph(negative_users)

show_graph(Graph)
show_graph(Negative_graph)

print("Most influential users talking about", keywords)
ranks = rank(Graph)
for i in range(5):
    user = list(ranks.keys())[i]
    print(user,ranks[user])

print("--------------")
print("Most influential users who are negative about about", keywords)
ranks = rank(Negative_graph)
for i in range(5):
    user = list(ranks.keys())[i]
    print(user, ranks[user])