""" This file is meant to store the functions meant for finding a subgraph in a graph. Two are given"""

from math import sqrt
from copy import deepcopy

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


def find_clique(edge_repr: str, size_clique) -> bool:    
    """This function computes whether there exists a clique of the input size in the graph, given by its binary representation."""

    #   def Bron_Kerbosch1(R:list,P:list,X:list) -> None:
    #     global largest_clique
    #     if len(P) == 0 and len(X) == 0:
    #         if len(R) > len(largest_clique):
    #             largest_clique = R
    #         return
    #     u = (P+X).pop()
    #     pivot_list = [p for p in P if p not in local_network.neighbors(u)]
    #     for v in pivot_list:
    #         Bron_Kerbosch1(R + [v],
    #                        [p for p in P if p in local_network.neighbors(v)],
    #                        [x for x in X if x in local_network.neighbors(v)])
    #         P.remove(v)
    #         X += [v]  

    # def Bron_Kerbosch2(G:nx.Graph) -> None:
    #     def degen_ordering(G: nx.Graph):
    #         if len(G.nodes) == 0:
    #             return []
    #         min_degree_node = min(G.degree(), key = lambda x:x[1])[0]
    #         othernodes = list(G.nodes)
    #         othernodes.remove(min_degree_node)
    #         return [min_degree_node] + degen_ordering(G.subgraph(othernodes))
        
    #     P = list(G.nodes)
    #     R,X = [],[]
    #     for v in degen_ordering(G):
    #         Bron_Kerbosch1(R + [v],
    #                        [p for p in P if p in G.neighbors(v)],
    #                        [x for x in X if x in G.neighbors(v)])
    #         P.remove(v)
    #         X += [v]
    
    # Bron_Kerbosch2(local_network)

    return

def subgraph_isomorphism(step:int, g:str, number_of_nodes:int, h_graph:str, 
                         h_graph_number_nodes:int, map_dict:dict, 
                         has_been_mapped:list) -> bool:
    # Assuming the graph from H is position on the nodes [1,...,k].
    def check_subgraph(mapping_function:dict, g_graph:str, h_graph:str):
        for vertex1 in range(1, h_graph_number_nodes + 1):
            for vertex2 in range(vertex1 + 1, h_graph_number_nodes + 1):
                if h_graph[edge_to_bit_location(number_of_nodes, vertex1, vertex2) - 1] == '1':
                    n1, n2 = mapping_function[vertex1], mapping_function[vertex2]
                    if n1 > n2:
                        if g_graph[edge_to_bit_location(number_of_nodes, n2, n1) - 1] != '1':
                            return False
                    else:
                        if g_graph[edge_to_bit_location(number_of_nodes, n1, n2) - 1] != '1':
                            return False
    
    if step == h_graph_number_nodes:
        if check_subgraph(map_dict, g, h_graph):
            return True
        pass

    for vertex in range(1, number_of_nodes + 1):
        if vertex in has_been_mapped:
            continue
        map_dict_copy = deepcopy(map_dict)
        has_been_mapped_copy = deepcopy(has_been_mapped)
        map_dict_copy[step+1] = vertex
        has_been_mapped_copy.append(vertex)
        subgraph_isomorphism(step+1, g, number_of_nodes, h_graph, h_graph_number_nodes, \
                             map_dict_copy, has_been_mapped_copy)
    return False

def main():
    return

if __name__ == '__main__':
    main()