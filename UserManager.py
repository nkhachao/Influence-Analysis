import pickle
import os



def save_user_discovery_session(base_users, discovered_users, scan, following_dict, opinion_dict):
    save_data(base_users, "base_users")
    save_data(discovered_users, "discovered_users")
    save_data(following_dict, "following_dict")
    save_data(opinion_dict, "opinion_dict")
    save_data(scan, "scan")


def load_user_discovery_session():
    base_users = load_data("base_users")
    if base_users is not None:
        return base_users, load_data("discovered_users"), load_data("scan"), load_data("following_dict"), load_data("opinion_dict")


def load_data(name):
    if os.path.isfile("Saved_Data/" + name + ".pickle"):
        return pickle.load(open("Saved_Data/" + name + ".pickle", "rb"))
    return None


def save_data(data, name):
    pickle.dump(data, open("Saved_Data/" + name + ".pickle", "wb"))


