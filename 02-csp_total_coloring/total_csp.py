# Install package python-constraint, not constraint !!!
from constraint import *
import networkx as nx
import numpy as np

def total_coloring(graph):
    """
        Find total chromatic index and total coloring.
        graph - instance of networkx.Graph
        returns - total chromatic index x
        Furthermore, assign property "color" for every vertex and edge. The value of the color has to be an integer between 0 and x-1.

        TODO: The implementation of this function finds some total coloring but the number of colors may not be minimal.
        Find the total chromatic index.
    """
    edges = {}
    i = -1
    for u,v in graph.edges():
        edges[(u,v)] = i
        i -= 1
    #constrains only once, enlarge domain through iterations
    domain_range = [0]
    edges_check_list = []
    maxDegree = 0
    
    problem = Problem(MinConflictsSolver())
    #setting problem variables
    for u in graph.nodes():
        problem.addVariable(u, domain_range)
        maxDegree = max(maxDegree, graph.degree[u])
    for key in edges:
        problem.addVariable(edges[key], domain_range)
    #adding problem constraints
    for u,v in graph.edges():
             problem.addConstraint(AllDifferentConstraint(), [u,v,edges[(u,v)]])
             for y,z in graph.edges():
               #add constraint for edges & change for duplicates
               if ((u == y and v != z) or (u != y and v == z) or (u == z and v != y) or (u != z and v == y)):
                   if ((u,v),(y,z)) not in edges_check_list and ((y,z),(u,v)) not in edges_check_list:
                       problem.addConstraint(AllDifferentConstraint(), [edges[(u,v)],edges[(y,z)]])
                       edges_check_list.append(((u,v),(y,z)))


    # lower bound for chromatic number is maxDeg + 1
    low = maxDegree + 1
    #Upper bound cannot exceed #vertices + 1
    high =  len(graph.nodes) + 1
    temp_best = len(graph.nodes)
    tempBestSOlution = {}

    #binary search over variable domains
    while low <= high:
        mid = low + (high - low)//2
        for key in problem._variables:
            problem._variables[key] = Domain(range(mid))
        solution = problem.getSolution()
        if solution != None:
            tempBestSOlution = solution
            temp_best = mid
            high = mid - 1
        else:
            low = mid + 1
     
    #Graf coloring based on variable values in solution
    for u in graph.nodes():
        graph.nodes[u]["color"] = tempBestSOlution[u]
    for u,v in graph.edges():
        graph.edges[u,v]["color"] = tempBestSOlution[edges[(u,v)]]
    return temp_best