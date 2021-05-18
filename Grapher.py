import networkx as nx
import matplotlib.pyplot as plt
from UserManager import *


def show_graph(graph):
    nx.draw(graph, with_labels = True, node_color = "none", font_size=8, bbox=dict(facecolor='w', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.5'))
    plt.show()


def create_graph(following_dict):
    all_users = list(following_dict.keys()) + [item for sublist in following_dict.values() for item in sublist]

    Graph = nx.DiGraph()
    Graph.add_nodes_from(all_users)
    for user in following_dict.keys():
        Graph.add_edges_from([(user, following) for following in following_dict[user]])
    return Graph


def rank(graph):
    ranks = nx.pagerank(graph)
    sorted_ranks = dict(sorted(ranks.items(), key=lambda item: item[1]))
    return sorted_ranks