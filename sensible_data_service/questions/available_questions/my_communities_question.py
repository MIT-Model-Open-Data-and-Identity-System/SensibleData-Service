import who_did_i_see_question as wdisq
import networkx as nx
import community
import json
from bson import json_util

NAME = "my_communities_question"

def run():
    """This question does not populate the database since it uses data calculated by who_did_i_see_question"""
    pass

def my_communities_answer(request, user, scopes, users_to_return, user_roles, own_data):
    """The response for my_communities request. Returns the users communities."""
    [collection, user, from_date, end_date, output_type] = wdisq.prepare_to_answer(request, users_to_return, user_roles, user) 
    result = {}
    for single_user in user:
        users_list = wdisq.get_users_list(collection, single_user, from_date, end_date)
        result[single_user] = _get_my_communities(users_list, single_user)
    return json.dumps(result, default=json_util.default)

def _get_my_network(users_list, my_username):
    """Returns the users network of people which he/she met within a given time."""
    my_network = nx.Graph()
    my_network.add_node(my_username)
    
    # add nodes to the graph and edge with me
    for user in users_list:
        my_network.add_node(user['user_seen'])
        my_network.add_edge(my_username, user['user_seen'])
        
    my_friends_network = _add_friends_edges(users_list)
    my_network = dict(my_network.items() + my_friends_network.items())
    return sorted(my_network.edges(), key = lambda user: my_network.edges()[user])
    
def _get_my_communities(users_list, my_username):
    """Returns the users communities based on people which he/she met within a given time."""
    my_network = _add_friends_edges(users_list)
    return community.best_partition(my_network)
    
def _add_friends_edges(users_list):
    """Returns the networkx graph with users friends as nodes and connections between them when they were met during the same timestamp"""
    my_network = nx.Graph()
    #add edges between users to the graph
    sorted(users_list, key=lambda user: user['time'])
    for user in users_list:
        for i in xrange(0, len(users_list)):
            if(user['time'] == users_list[i]['time'] and user['user_seen'] != users_list[i]['user_seen']):
                my_network.add_edge(user['user_seen'], users_list[i]['user_seen'])
    return my_network