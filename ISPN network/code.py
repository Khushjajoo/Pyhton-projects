from Graph import *

import random
import sys

class ISPNetwork:

    def __init__(self):
        self.network = Graph()
        self.MST = Graph()

    def buildGraph(self, filename): # build graph from file
        with open(filename) as f: # open file
            for line in f: # traverse thorugh file and store each line in a variable called line
                line = line.split(",") # split line by seperator which is a comma in the CSV file
                # creating bidirectional edges for network undirected graph
                self.network.addEdge(line[0], line[1], float(line[2])) # add edge to graph
                self.network.addEdge(line[1], line[0], float(line[2])) # add edge to graph

    def pathExist(self, router1, route2): # check if path exists between router1 and route2
        router1 = self.network.getVertex(router1) # get vertex of router1
        route2 = self.network.getVertex(route2) # get vertex of route2
        queue = [] # queue to hold vertices to be explored
        visit = [] # list to hold visited vertices
        queue.append(router1) # add router1 to queue
        if router1 is None or route2 is None: # if either router1 or route2 is not in the graph
            return False      # return false which means a path does not exist
        if router1 == route2: # if router1 and route2 are the same
            return True       # return true which means a path does exist
        while len(queue) > 0: # while there are still vertices to be explored
            n = queue.pop(0)  # pop first vertex from queue
            visit.append(n)   # add vertex to visited list
            for i in n.getConnections(): # for each neighbor of n
                if i == route2:          # if neighbor is route2
                    return True          # return true which means a path does exist
                else:                    # if neighbor is not route2
                    if i not in visit:   # if neighbor is not in visited list
                        queue.append(i)  # add neighbor to queue which will be explored later
        return False                     # if we do not find a pth from router1 to router2, we return "path not exist"
            
    def prim(self, G, start): # Prim's algorithm from class lecture codes
        pq = PriorityQueue()  # queue to hold verts to be explored
        for v in G: # set all vertices to infinite distance
            v.setDist(sys.maxsize) 
            v.setPredecessor(None) # set all vertices to no predecessor
        start.setDist(0) # set start vertex to 0
        pq.buildHeap([(v.getDist(), v) for v in G])  # build heap of all verts
        while not pq.isEmpty(): 
            currentVert = pq.delMin()  # starting vert
            for nextVert in currentVert.getConnections():  # grabbing all neighbors of current vert
                newCost = currentVert.getWeight(nextVert) # getting weight of edge between current vert and neighbor
                if nextVert in pq and newCost < nextVert.getDist(): 
                    nextVert.setPredecessor(currentVert) # set predecessor of neighbor to current vert
                    nextVert.setDist(newCost) # set distance of neighbor to new cost
                    pq.decreaseKey(nextVert, newCost) # decrease key of neighbor to new cost
    
    def buildMST(self): # build minimum spanning tree
        self.MST = Graph() # create new graph to hold MST
        temp = self.network # create temporary graph to hold network and store it in temp
        v = [*(temp.getVertices())] # get all vertices from temp and store in v 
        self.prim(temp, temp.getVertex(v[0])) # run prim's algorithm on temp
        for ver in temp: # for each vertex in network
            for neighbor in ver.getConnections(): # for each neighbor of vertex
                if neighbor.getPredecessor() == ver: # if neighbor is predecessor of neighbor vertex
                    # create bidirectional edge for MST undirected graph
                    self.MST.addEdge(ver.getId(), neighbor.getId(), ver.getWeight(neighbor)) # add edge to MST
                    self.MST.addEdge(neighbor.getId(), ver.getId(), ver.getWeight(neighbor)) # add edge to MST

    def dijkstra(self, aGraph, start): # Dijkstra's algorithm from class lecture codes
        pq = PriorityQueue() # Priorityqueue to hold vertices to be explored
        start.setDist(0) # set start vertex's distance to 0
        pq.buildHeap([(v.getDist(), v) for v in aGraph]) # build heap of all verts
        while not pq.isEmpty(): # while there are still vertices to be explored
            currentVert = pq.delMin() # starting vert
            for nextVert in currentVert.getConnections(): # for each neighbor of current vert
                newDist = currentVert.getDist() \
                          + currentVert.getWeight(nextVert) # new distance is current vert's distance + weight of edge between current vert and neighbor
                if newDist < nextVert.getDist() and nextVert.getPredecessor() != currentVert and currentVert.getPredecessor() != nextVert: 
                    nextVert.setDist(newDist) # set distance of neighbor to new distance
                    nextVert.setPredecessor(currentVert) # set predecessor of neighbor to current vert
                    pq.decreaseKey(nextVert, newDist) # decrease key of neighbor to new distance
    
    def findPath(self, router1, router2): # find path between router1 and router2 in MST
        # reset MST 
        if self.MST is not None: 
            for i in self.MST:
                if i is not None:
                   i.setPredecessor(None)
                   i.setDist(sys.maxsize)

        path = [] # list to hold path
        output = "" # string to hold output
        v1 = self.MST.getVertex(router1) # get vertex of router1 and store it in v1
        if v1 is None: # if vertex of router1 is None (router1 is not in MST)
            return "path not exist" 
        else: # if vertex of router1 is not None (router1 is in MST)
            self.dijkstra(self.MST, v1) # run dijkstra's algorithm on MST starting at router1

        v2 = self.MST.getVertex(router2) # get vertex of router2 and store it in v2
        while v2 is not None and v2.getPredecessor() is not None and v2.getId() != router1: # while router2 is in MST and router2 has a predecessor
            path.append(v2.getId()) # add router2 to path
            v2 = v2.getPredecessor() # set v2 to its predecessor

        if v2 is not None: # if vertex of router2 is not None (router2 is in MST)
            path.append(v2.getId()) # add router2 to path

        if router1 in path: # if router1 is in path
            path=path[::-1] # reverse path
            for router in path: # for each router in path
                if router == router2: # if router is router2
                    output = output + router # add router to output
                else: # if router is not router2
                    output = output + router + " -> " # add router to output and add arrow             
        else: # if router1 is not in path
            return "path not exist" 
                   
        return output

    def findForwardingPath(self, router1, router2): # find path with minimum cost between router1 and router2 in network
        # reset network
        if self.network is not None:
            for i in self.network:
                if i is not None:                
                    i.setPredecessor(None)
                    i.setDist(sys.maxsize)
                    
        path = []   # list to hold path
        weight = 0  # int to hold weight
        output = "" # string to hold output
        v1 = self.network.getVertex(router1) # get vertex of router1 and store it in v1
        if v1 is None: # if vertex of router1 is None (router1 is not in network)
            return "path not exist" 
        else: # if vertex of router1 is not None (router1 is in network)
            self.dijkstra(self.network, v1)  # run dijkstra's algorithm on network starting at router1
        
        v2 = self.network.getVertex(router2) # get vertex of router2 and store it in v2
        while v2 is not None and v2.getPredecessor() is not None and v2.getId() != router1: # while router2 is in network and router2 has a predecessor
            path.append(v2.getId()) # add router2 to path
            weight += v2.getWeight(v2.getPredecessor()) # add weight of edge between router2 and its predecessor to weight
            v2 = v2.getPredecessor() # set v2 to its predecessor
        if v2 is not None: # if vertex of router2 is not None (router2 is in network)
            path.append(v2.getId()) # add router2 to path
        if router1 in path: # if router1 is in path
            path=path[::-1] # reverse path
            for router in path: # for each router in path
                if router == router2: # if router is router2
                    output = output + router + " (" + str(weight) + ")" # add router to output and add weight
                else: # if router is not router2
                    output = output + router + " -> " # add router to output and add arrow
        else: # if router1 is not in path
            output = "path not exist"

        return output
    
    def dijkstramax(self, aGraph, start): # Dijkstra's algorithm from class lecture codes modified to find max distance
        pq = PriorityQueue() # Priorityqueue to hold vertices to be explored
        start.setDist(0) # set start vertex's distance to 0
        pq.buildHeap([(v.getDist(), v) for v in aGraph]) # build heap of all verts
        while not pq.isEmpty(): # while there are still vertices to be explored
            currentVert = pq.delMin() # starting vert
            for nextVert in currentVert.getConnections(): # for each neighbor of current vert
                newDist = max(currentVert.getDist(), currentVert.getWeight(nextVert)) # new distance is max of current vert's distance and weight of edge between current vert and neighbor
                if newDist < nextVert.getDist() and nextVert.getPredecessor() != currentVert and currentVert.getPredecessor() != nextVert:
                    nextVert.setDist(newDist) # set distance of neighbor to new distance
                    nextVert.setPredecessor(currentVert) # set predecessor of neighbor to current vert
                    pq.decreaseKey(nextVert, newDist) # decrease key of neighbor to new distance
    
    def findPathMaxWeight(self, router1, router2): # find path between router1 and router2 in network with max weight
        # reset network
        if self.network is not None:
            for i in self.network:
                if i is not None:
                    i.setPredecessor(None)
                    i.setDist(sys.maxsize)

        path = [] # list to hold path
        output = "" # string to hold output
        v1 = self.network.getVertex(router1) # get vertex of router1 and store it in v1
        if v1 is None: # if vertex of router1 is None (router1 is not in network)
            return "path not exist" 
        else:   # if vertex of router1 is not None (router1 is in network)
            self.dijkstramax(self.network, v1) # run dijkstra's algorithm on network starting at router1
            
        v2 = self.network.getVertex(router2) # get vertex of router2 and store it in v2
        while  v2 is not None and v2.getPredecessor() is not None and v2.getId() != router1: # while router2 is in network and router2 has a predecessor
            if v2.getPredecessor() is not None: # if vertex of router2 has a predecessor
                path.append(v2.getId()) # add router2 to path
                v2 = v2.getPredecessor() # set v2 to its predecessor
        if v2 is not None: # if vertex of router2 is not None (router2 is in network)
            path.append(v2.getId()) # add router2 to path
        path = path[::-1]  # reverse path
        if router1 in path and router2 in path: # if router1 and router2 are in path
            for i in path: # for each router in path
                if i == router2: # if router is router2
                    output = output + i # add router to output
                else: # if router is not router2
                    output = output + i + " -> " # add router to output and add arrow
        else: # if router1 and router2 are not in path
            return "path not exist"

        return output

    @staticmethod
    def nodeEdgeWeight(edge):
        return sum([neighbor for neighbor in edge.connectedTo.values()]) # return sum of all neighbors of edge

    @staticmethod
    def totalEdgeWeight(graph): 
        return sum([ISPNetwork.nodeEdgeWeight(edge) for edge in graph]) // 2 # return sum of all edges in graph


if __name__ == '__main__':

    print("--------- Task1 build graph ---------")
    # Note: You should try all six dataset. This is just a example using 1221.csv
    net = ISPNetwork()
    net.buildGraph('data/1221.csv')

    print("--------- Task2 check if path exists ---------")
    routers = [v.id for v in random.sample(list(net.network.vertList.values()), 5)]
    for i in range(4):
        print('Router1:', routers[i], ', Router2:', routers[i+1], 'path exist?:', net.pathExist(routers[i], routers[i+1]))
    
    print("--------- Task3 build MST ---------")
    net.buildMST()
    print('graph node size', net.MST.numVertices)
    print('graph total edge weights', net.totalEdgeWeight(net.MST))
    
    print("--------- Task4 find shortest path in MST ---------")
    for i in range(4):
        print(routers[i], routers[i+1], 'Path:', net.findPath(routers[i], routers[i+1]))

    print("--------- Task5 find shortest path in original graph ---------")
    for i in range(4):
        print(routers[i], routers[i+1], 'Path:', net.findForwardingPath(routers[i], routers[i+1]))

    print("--------- Task6 find path in LowestMaxWeightFirst algorithm ---------")
    for i in range(4):
        print(routers[i], routers[i+1], 'Path:', net.findPathMaxWeight(routers[i], routers[i+1]))

