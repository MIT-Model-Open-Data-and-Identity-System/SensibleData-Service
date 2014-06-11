import who_did_i_see_question as wdisq
import networkx as nx
import community

#http://raman.imm.dtu.dk:8086/magda/sensible-dtu/connectors/connector_answer/v1/my_communities_question/my_communities_answer/?bearer_token=c9af1c97a08500ba33635cf2568ce1&username=331f9e3859ae7f3c457498d423d29d&type=today

NAME = "my_communities_question"

def run():
    pass

def my_communities_answer(request, user, scopes, users_to_return, user_roles, own_data):
    parsed_request = wdisq.parse_request(request)
    if isinstance(parsed_request, dict) or (isinstance(parsed_request, list) and len(parsed_request) != 4):
        return parsed_request
    [username, from_date, end_date, output_type] = parsed_request
    db_connection = wdisq.connect_to_db()
    
    users_list = wdisq.get_users_list(db_connection, username, from_date, end_date)
    return _get_my_communities(users_list, username)

def _get_my_network(users_list, my_username):
    my_network = nx.Graph()
    my_network.add_node(my_username)
    # add nodes to the graph and edge with me
    for user in users_list:
        my_network.add_node(user[0])
        my_network.add_edge(my_username, user[0])
        
    #add edges between users to the graph
    sorted(users_list, key=lambda user: user[1])
    for user in users_list:
        for i in xrange(0, len(users_list)):
            if(user[1] == users_list[i][1] and user[0] != users_list[i][0]):
                my_network.add_edge(user[0], users_list[i][0])
    return my_network.edges()
    
def _get_my_communities(users_list, my_username):
    my_network = nx.Graph()
    
    #add edges between users to the graph
    sorted(users_list, key=lambda user: user[1])
    for user in users_list:
        for i in xrange(0, len(users_list)):
            if(user[1] == users_list[i][1] and user[0] != users_list[i][0]):
                my_network.add_edge(user[0], users_list[i][0])
    return community.best_partition(my_network)