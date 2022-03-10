# Install package python-sat !!!
from pysat.solvers import Solver

def total_coloring(graph):
    """
        Find total chromatic index and total coloring.
        graph - instance of networkx.Graph
        returns - total chromatic index x
        Furthermore, assign property "color" for every vertex and edge. The value of the color has to be an integer between 0 and x-1.

        TODO: The implementation of this function finds some total coloring but the number of colors may be minimal.
        Find the total chromatic index.
    """

    #finds max degree of graph, CN cannot be smaller
    maxDegree = 0
    for u in graph.nodes():
        maxDegree = max(maxDegree, graph.degree[u])

    model = None
    CN = maxDegree

    #Every variable has list of possible colors. Index of first positive literal in that list is nummber of color assinged to the edge/node
    while model == None:
        g = Solver()
        #counts used variables, assigns next edge/vertex next ones avalible
        globalCounter = 1
        CN  += 1
        #every node/edge has list of its variables -> colors
        variableDict = {}
        edgesStarterPoint = 0
        for u in graph.nodes():
            #Edges has -1 signature, in case some nodes are tuples, protecting SAT from conflicts
            variableDict[u] = range(globalCounter, globalCounter +CN)
            globalCounter+= CN

        edgesStarterPoint = globalCounter - 1
        for u,v in graph.edges():
            variableDict[(u,v,-1)] = range(globalCounter, globalCounter + CN)
            globalCounter+= CN

   
        for u,v in graph.edges():
            for l in range(CN):
                #Constraints for same color vertices
                g.add_clause([-variableDict[u][l], -variableDict[v][l]])
                 #Constraints for same color vertic and neighbor edges
                g.add_clause([-variableDict[(u,v,-1)][l], -variableDict[v][l]])
                g.add_clause([-variableDict[(u,v,-1)][l], -variableDict[u][l]])


        #This can be done faster by looping only neighbors
        for u,v in graph.edges():
             for y,z in graph.edges():
               #add constraint for edges & change for duplicates
               if ((u == y and v != z) or (u != y and v == z) or (u == z and v != y) or (u != z and v == y)):
                   for l in range(CN):
                       #neighbor edges must have different colors
                       g.add_clause([-variableDict[(u,v,-1)][l], -variableDict[(y,z,-1)][l]])
        
                
        #every edge and vertice must have color
        for key in variableDict:
                g.add_clause(variableDict[key])
        g.solve()
        model = g.get_model()

    #COloring of vertices
    vertexCount = 0
    for u in graph.nodes():
        for c in range(CN):
            if model[(vertexCount*CN + c)] >= 0:
                graph.nodes[u]["color"] = c
                vertexCount += 1
                break
            edgesCount = 0

    #Coloring of edges
    for u,v in graph.edges():
        for c in range(CN):
            if model[(edgesCount*CN + c + edgesStarterPoint)] >= 0:
                graph.edges[u,v]["color"] = c
                break
        edgesCount += 1
    return CN
