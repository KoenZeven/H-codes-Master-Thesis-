import gurobipy as gp
from gurobipy import GRB
import time
from math import sqrt
import itertools

from edge_repr_permutations import edge_to_bit_location, bit_location_to_edge, subgraph_isomorphism
from bigadjacencymatrix import Big_matrix

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
    X = [m1.addVar(vtype=GRB.INTEGER, name="x["+ str(s)+"]") for s in range(size)]

    # Set objective function
    m1.setObjective(sum(X[i] for i in range(size)), GRB.MAXIMIZE)

    # Add simple constraints
    for i in range(size):
        for j in range(i):
            if M[i][j] == 1:
                m1.addConstr(X[i] + X[j] <= 1)
        m1.addConstr(X[i] <= 1)

    # Optimize
    m1.optimize()

    for v in m1.getVars():
        if v.x != 0:
            print(v.varName, v.x)

    
    endtime = time.time()
    return m1.ObjVal, endtime - starttime 

def MaxClique(size:int, M:list):
    starttime = time.time()

    # Create a new model
    m2 = gp.Model("newModel")
    m2.Params.LogToConsole = 0

    # Add variables
    X = [m2.addVar(vtype=GRB.INTEGER, name="x["+ str(s)+"]") for s in range(size)]

    # Set objective function
    m2.setObjective(sum(X[i] for i in range(size)), GRB.MAXIMIZE)

    # Add simple constraints
    for i in range(size):
        for j in range(i):
            if M[i][j] == 0:
                m2.addConstr(X[i] + X[j] <= 1)
        m2.addConstr(X[i] <= 1)
    
    # Configure solution pool settings
    m2.setParam(GRB.Param.PoolSearchMode, 2)
    m2.setParam(GRB.Param.PoolSolutions, 10)

    # Optimize
    m2.optimize()
    
    # Retrieve solutions from the solution pool
    num_solutions = m2.SolCount  # Number of solutions found
    print(f"Number of solutions found: {num_solutions}")

    for i in range(min(num_solutions, 10)):  # Retrieve at most 10 solutions
        m2.setParam(GRB.Param.SolutionNumber, i)
        print(f"\nSolution {i + 1}:")
        for v in m2.getVars():
            if v.Xn > 1e-7:
                print(v.varName, v.Xn)
        print()

    
    endtime = time.time()  
    return m2.ObjVal, endtime - starttime 

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

memo = dict()
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
        if (symm_diff,H_graph) in memo:
            x = memo[(symm_diff,H_graph)]
        else:
            x = subgraph_isomorphism(step = 0, g = symm_diff,  number_of_nodes = int((1 + sqrt(1 + 8 * len(g1)))//2),
                                h_graph = H_graph, h_graph_number_nodes = 3, map_dict = dict(), has_been_mapped = list())
            memo[(symm_diff,H_graph)] = x
        if x:
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

    # size, M = BuildAdjancencyMatrix(graphs_n, [k3])
    size = 2**((n - 1) * n // 2)
    M = Big_matrix()
    # optimalInd, timing1 = IndependentSet(size,M)
    optimalCliq, timing2 = MaxClique(size, M)
    # print(optimalInd)
    print(optimalCliq)
    return

if __name__ == "__main__":
    main()