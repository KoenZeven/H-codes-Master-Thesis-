""" This file is meant to store the functions meant for finding a subgraph in a graph, by chosing the right permutation"""

from math import sqrt

def edge_to_bit_location(number_of_nodes:int, node1:int, node2:int) -> int:
    """In binary edge representation, returns the bit belonging to the edge (node1,node2), based on the number of nodes.
    The way the bit location is calculated is based on the following ordering of edges:
    (1,2), (1,3), ..., (1,n), (2,3), (2,4), ..., (2,n), ..., (n-1,n).
    
    Input:
        :int number_of_nodes: the number of nodes
        :int node1, node2: the integer values of the two nodes of the edge (node1,node2)
    
    Output:
        :int: bit location (from the left of the binary string)"""
    return (node1 - 1) * number_of_nodes - node1 * (node1 - 1) // 2 + node2 - node1

def bit_location_to_edge(number_of_nodes:int, bit_location:int) -> tuple[int,int]:
    """Given the bit location in the binary edge representation, returns the edge it belongs to.
    This is done by solving the following equation for x:
        \n(x - 1) * number_of_nodes - x * (x-1) / 2 = bit_location\n
    and rounding down to get the value for node 1. Then the value for node 2 is found by solving
        \n(node1 - 1) * number_of_nodes - node1 * (node1 - 1) / 2 + y - node1 = bit_location\n
    for y.
    
    Input:
        :int number_of_nodes: the number of nodes of the graph.
        :int bit_location: location of the bit (from the left of the binary string)"""
    num = (1+2*number_of_nodes) - sqrt((1+2*number_of_nodes)**2 - 4*2*(number_of_nodes - 1 + bit_location))
    node1 = num // 2
    node2 = bit_location - (node1 - 1) * number_of_nodes + node1 * (node1 - 1) // 2 + node1
    return (node1, node2)
