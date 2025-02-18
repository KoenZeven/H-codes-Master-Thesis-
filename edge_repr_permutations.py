""" This file is meant to store the functions meant for finding a subgraph in a graph, by chosing the right permutation"""


def find_edge_bit_location(number_of_nodes:int, node1:int, node2:int) -> int:
    """In binary edge representation, returns the bit belonging to the edge (node1,node2), based on the number of nodes.
    The way the bit location is calculated is based on the following ordering of edges:
    (1,2), (1,3), ..., (1,n), (2,3), (2,4), ..., (2,n), ..., (n-1,n).
    
    Input:
        :int number_of_nodes: the number of nodes
        :int node1, node2: the integer values of the two nodes of the edge (node1,node2)
    
    Output:
        :int: bit location """
    return (node1 - 1) * number_of_nodes - node1 * (node1 - 1) // 2 + node2 - node1