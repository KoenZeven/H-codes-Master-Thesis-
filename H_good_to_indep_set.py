import gurobipy as gp
from gurobipy import GRB
import time
import itertools

from edge_repr_permutations import edge_to_bit_location, bit_location_to_edge

def IndependentSet(size:int, M:list):
    """ The ILP to solve the independent set problem, given an adjacency matrix M and number of vertices given by 'size'.
    
    Input
        :int size: number of vertices of the graph
        :list M: adjacency matrix for the graph
    
    Output:
        :list x: optimal solution to the independent set problem, gives 1's where the vertex is in the independent set"""
    starttime = time.time()

    # Create a new model
    m1 = gp.Model("newModel")
    m1.Params.LogToConsole = 0

    # Add variables
    x = [m1.addVar(vtype=GRB.INTEGER, name="x["+ str(s)+"]") for s in range(size)]

    # Set objective function
    m1.setObjective(sum(x[i] for i in range(size)), GRB.MAXIMIZE)

    # Add simple constraints
    for i in range(size):
        for j in range(i):
            if M[i][j] == 1:
                m1.addConstr(x[i] + x[j] <= 1)
        m1.addConstr(x[i] <= 1)

    # Optimize
    m1.optimize()

    
    endtime = time.time()
    return m1.ObjVal, endtime - starttime 

def BuildAdjancencyMatrix(graphs:list[str], H: list[str]) -> tuple[int,list]:
    """Builds the adjacency matrix of the following graph: 
    Vertices are the graphs in the list 'graphs', edges are between two graphs whose symmetric difference is in H
    
    Input
    :list[nx.Graph] graphs: list of graphs to be studied
    :list[nx.Graph] H: family of graphs not to be seen in symmetric difference"""
    size = len(graphs)
    M = [[0 for _ in range(i)] for i in range(size)]

    for i in range(size):
        for j in range(i):
            if symmetric_diff_contains_an_h(graphs[i], graphs[j], H):
                M[i][j] = 1
    return size, M

def symmetric_difference(g1:str, g2:str) -> str:
    """Returns the symmetric difference of two binary edge representations, functions the same as bitwise xor
    
    Input:
        :str g1,g2: binary edge-representations of the two graphs being analysed
        
    Output:
        :str x: symmetric difference of the two graphs"""
    x = str()
    for i, g1i in enumerate(g1):
        if g1i != g2[i]:
            x += '1'
        else:
            x += '0'
    return x

def symmetric_diff_contains_an_h(g1:str, g2:str, H:list) -> bool:
    """Computes whether the symmetric difference of the input graphs has a subgraph which is isomorphic to a graph in the list H. 
    This function is currently unneccesary.
    
    Input: 
        :str g1, g2: binary input graphs to be analysed
        :list H: family of graphs
        
    Output:
        :bool 1/0: 1 if True, 0 if not"""
    
    symm_diff = symmetric_difference(g1, g2)
    for H_graph in H:
        # Current idea: loop over all possible permutations of the edge-representation of H_graph
        # Then consider the symmetric difference of symm_diff and such a permutation of H_graph.
        # If this symmetric difference does not add 1's when compared to symm_diff, then
        # H_graph is a subgraph of symm_diff.

        # Requirement: number of edges of symm_diff (number of 1's in the binary rep.) has to be larger or equal than that pf H_graph
        if symm_diff == H_graph:
            return 1
    return 0

def BuildGraphs(n: int) -> list[str]:
    """Generates all graphs on n vertices and returns their binary string representations."""
    graphs = list()
    num_edges = n * (n - 1) // 2  # Number of edges in the complete graph (excluding loops)
    
    # Iterate over all possible edge combinations
    for edges in itertools.product("01", repeat=num_edges):
        binary_string = "".join(edges)  # Convert tuple to string
        graphs.append(binary_string)

    return graphs

def main():
    n = 5
    graphs_n = BuildGraphs(n)

    k3 = '0' * (n * (n - 1) // 2)
    for j in range(3):
        for i in range(j):
            index = edge_to_bit_location(n,i+1,j+1)
            k3 = k3[:index - 1] + '1' + k3[index:]

    size, M = BuildAdjancencyMatrix(graphs_n, [k3])
    optimal, timing = IndependentSet(size,M)
    print(optimal)
    return

if __name__ == "__main__":
    main()