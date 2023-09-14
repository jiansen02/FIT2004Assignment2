"""
Assignment 2 FIT2004 
Name: Chan Jian Sen
Student ID: 31859097
"""
from collections import deque
from typing import Any

# ==================== Q1 Code ====================

class ResidualNetwork:

    def __init__(self,V,length):
        """
               
        Init for the class 
        Written by Jian Sen Chan

        Precondition: length > 0
        Postcondition:  self.vertices != [None]*(length)

        Input:
            V: list of connections
            length: number of data centres in the network
        Return:
            None

        Time complexity: 
            Best: O(C)
            Worst: O(C)
        Space complexity: 
            Input: O(C)
            Aux: O(C)

        We are using this graph to construct the redisual flow network.
        This residual flow network will also be used to initialise vertices and edges.
   
        """

        self.vertices = [None]*(length)

        #This helps to add all of the vertices into the graph
        added_vertex = []

        for i in range(0,len(V),1):

            if V[i][0] not in added_vertex:
                
                #Add the vertex
                self.vertices[V[i][0]] = Vertex(V[i][0])
                added_vertex.append(V[i][0])
               

            if V[i][1] not in added_vertex:

                #Add the vertex
                self.vertices[V[i][1]] = Vertex(V[i][1])
                added_vertex.append(V[i][1])
           


        
        # Once all the vertices have been added, it's time to insert the edges
        # Add the edges into the graph
        for i in range(0,len(V),1):
            if self.vertices[V[i][0]] != None:
                self.vertices[V[i][0]].edges.append(Edge(self.vertices[V[i][0]],self.vertices[V[i][1]],V[i][2]))
        



    def __str__(self):
        """
    
        Written by Jian Sen Chan

        Precondition: self.vertices != [None]*length
        Postcondition: len(return_string) == len(self.vertices)

        Input:
            None
        Return:
            List of the vertex numbers (showing the list of data centres)

        Time complexity: 
            Best: O(D)
            Worst: O(D)
        Space complexity: 
            Input: O(D)
            Aux: O(D)

        This function returns the list of vertices in string format.

        """
        return_string = ""
        for vertex in self.vertices:
            return_string = return_string + "," + str(vertex)
        return return_string
    
    def list_of_connections(self):
        """
    
        Written by Jian Sen Chan

        Precondition: self.vertices != [None]*length
        Postcondition: len(return_list) >= len(self.vertices)

        Input:
            None
        Return:
            A nested list of [edge.u.id,edge.v.id,edge.w] for every forward edge in all the vertices 

        Time complexity: 
            Best: O(DC)
            Worst: O(DC)
        Space complexity: 
            Input: O(DC)
            Aux: O(DC)

        This function returns the list of the connections. It shows the id of the data centre sending data, the 
        id of the data centre receiving data and the amount of data flowing from the former to the latter.

        """        
        
        return_list = []
        for vertex in self.vertices:
            if vertex != None:
                for edge in vertex.edges:
                    return_list.append([edge.u.id,edge.v.id,edge.w])
        return return_list
    
    def list_of_all_connections(self):

        """
    
        Written by Jian Sen Chan

        Precondition: self.vertices != [None]*length
        Postcondition: len(return_list) >= len(self.vertices)

        Input:
            None
        Return:
            A nested list of [edge.u.id,edge.v.id,edge.w] for every forward and backward edge in all the vertices .


        Time complexity: 
            Best: O(DC)
            Worst: O(DC)
        Space complexity: 
            Input: O(DC)
            Aux: O(DC)

        This function returns the list of the connections. It shows the id of the data centre sending data, the 
        id of the data centre receiving data and the amount of data flowing from the former to the latter.

        Not only that, it shows the backward edges as well, which are used to represent the reverse flow in the network.

        """    
        return_list = []
        for vertex in self.vertices:
            for edge in vertex.edges:
                return_list.append([edge.u.id,edge.v.id,edge.w])

        for vertex in self.vertices:
            for edge in vertex.backward_edges:
                return_list.append([edge.u.id,edge.v.id,edge.w])
        return return_list
 
    
    def bfs(self,origin,length):

        """
        Written by Jian Sen Chan

        Precondition: self.vertices[origin] != None
        Postcondition: parents != [None]*length

        Input:
            origin: The number of the data centre which is backing up data in other places
            length: The number of data centres + one super_target 
        Return:
            A list of vertex ids showing the parents of each vertex id in the breadth first search traversal.


        Time complexity: 
            Best: O(D + C)
            Worst: O(D + C)
        Space complexity: 
            Input: O(D + C)
            Aux: O(D + C)
        This function is the first part of ford_fulkerson. 

        Essentially, it is a breadth first search algorithm which is going to traverse the whole graph to find out what
        is the path. This is part and parcel of executing path augmentation in ford fulkerson. 

        With the list of parents, we can then use it for backtracking later on in the backtracker() function.

        This is what I would call the "Part 1" of my ford fulkerson method. "Part 2" will be in the backtracker() function.
        """

        
        return_bfs = []
        parents= [-1]*length   
        discovered = deque()
        #discovered is a dequeue
        
        
        #Identify the source according to what the vertex value is:
        source = self.vertices[origin]
        discovered.append(source)
        while len(discovered) > 0:

            #pop it
            u = discovered.popleft()
            u.visit_node() 
            #this means that u has been visited
            return_bfs.append(u.id)
            for edge in u.edges:
                v = edge.v
                if v.discovered == False:
                    discovered.append(v)
                    #this means that v has been discovered
                    v.added_to_queue()
                    parents[v.id] = (u.id)

        #Now that we have the list of parents, we backtrack in order to update the flow 
        #We do so by calling the backtracker function which will backtrack to update the
        #graph with the right flow



        #Reset the visited to be all equal to False so that this function can be used again
        #for the next time
        for vertex in self.vertices:
            if vertex != None:
                vertex.unvisit_node()

        return parents
    
    def backtracker(self,source,parents):
         
        """
        Written by Jian Sen Chan

        Precondition: parents != [None]*length
        Postcondition: max_flow > 0

        Input:
            source: The origin 
            parents: the list which shows the parent vertices of every vertex in an augmented path from the origin to the super target
        Return:
            A list showing two items: The maximum flow of one of the paths of origin to the super target vertex and the list of the connections
            (both forward and backward) after the operation is done.

        Time complexity: 
            Best: O(X)
            Worst: O(DX)
        Space complexity: 
            Input: O(DX)
            Aux: O(DX)
        This function is the second part of ford_fulkerson. 

        Essentially, it backtracks the graph according to the parents list so that the flow of the residual network is updated.
        This is done in order to achieve the maximum flow of the network.
        
        A path from the origin to the target will be selected and the smallest value amongst all the edges from the origin vertex to 
        the super target vertex will be chosen. This is because this is the only biggest value which can be flowed from the origin
        vertex to the super target vertex.

        We will then return the value of the flow alongside an updated list of connections (both forward and backward) after the operation
        has been done.

        This is the Part 2 of my ford_fulkerson method.

        """


        #Part 2: Now that we have the list of parents, backtrack in order to update the flow 
        
        return_data = []
        start_point = source   
        i = len(parents)-1
        #i is used to represent the current point  we are at as we backtrack.
        #We will start with the super target first. The super target id is equivalent to len(parents)-1
        max_flow = 0
        current_possible_flows = []
        connection_between_flows = []
        while i != start_point:
            if i >= 0:
                for edge in self.vertices[parents[i]].edges:
                    v = edge.v
                    
                    if v.id == i:
                    #We are only looking for the edge between parent and the v.
                    #Execute the following line of code if the vertex reached by the edge is the one which 
                    #we are currently looking at
                        current_possible_flows.append(edge.w)
                        a = self.vertices[v.id]
                        b = self.vertices[parents[v.id]]
                        connection_between_flows.append([a.id,b.id])

                    #We do not need to go through all of the 
                    #edges in self.vertices[parents[i]].edges as we only need the one edge which we are 
                    #which connects the current point i with it's parent
                    

                #The purpose of this is to backtrack along the flow network and 
                #make the current point the parent point which we just looked at
                
                i = int(self.vertices[parents[i]].__str__())
                
        min_flow = min(current_possible_flows)

        max_flow = max_flow + min_flow
        #update the flow from the source to the destination by deducting the minimum flow 
        for flow in range(0,len(current_possible_flows)):
            current_possible_flows[flow] = current_possible_flows[flow] - min_flow

        #update the graph's edges with backward flows, and deduct the forward flows
        for k in range(0,len(connection_between_flows)):
            
            for edge in self.vertices[connection_between_flows[k][1]].edges:
                
                
                v = edge.v
                if v == self.vertices[connection_between_flows[k][0]]:
                    
                    #update the forward edge by subtracting the max flow
                    edge.w = edge.w - min_flow
                    
                    #if the forward is already 0 then just delete it
                    if edge.w == 0:
                        #Deletion of edge performed
                        self.vertices[edge.u.id].edges.remove(edge)
                        
                    #create a new backward edge using the min flow
                    #Attacht the new backward edge to the vertex
                    self.vertices[connection_between_flows[k][0]].backward_edge.append(Edge(self.vertices[connection_between_flows[k][0]],self.vertices[connection_between_flows[k][1]],min_flow))
                    
                    
                    ##By doing these two steps^, there is both a forward an backward edge 
        
        return_data = [max_flow, self.list_of_connections()]
        return return_data
    

    def ford_fulkerson_ended(self,origin,super_target,list_of_connections):


        """
        Written by Jian Sen Chan

        Precondition: self.vertices[origin] != None
        Postcondition: 

        Input:
            origin: The number of the data centre which is backing up data in other places
            super_target: A vertex added which all target vertices point to because there are multiple targets
            list_of_conncections: The current list of edges in the network in list form. A super target is also added in this list as there are multiple targets.
        Return:
            A list showing two items: The maximum flow of one of the paths of origin to the super target vertex and the list of the connections
            (both forward and backward) after the operation is done.

        Time complexity: 
            Best: O(D + C)
            Worst: O(D + C)
        Space complexity: 
            Input: O(D + C)
            Aux: O(D + C)

        
        This function acts as a checker to see if the ford fulkerson method (which is, the combination of bfs() and backtracker())
        needs to be executed again or not.
        
        But in order to understand the logic of this function, one must understand that:
        A shortcut to find which should be the source and which should be the target in (S,T) 
        is to group the vertices which are reachable by the source vertex altogether as the source,
        and the remaining vertices can then be grouped as the target. 

        Now, if the super target vertex is reachable by the source vertex then what it would mean
        is that even the super target vertex cannot be grouped in the target. 
        If this is the case, it means that the residual flow network is still not final yet, 
        and Ford-Fulkerson still needs to be implemented. So we would return a False to 
        say that there is no cut available yet.

        (This shortcut is taught by Dr Ian Lim in lectures. I am unsure if the Monash Australia syllabus has it.)
        """
        
        #Identify the source according to what the vertex value is:

        
        source = self.vertices[origin]
        
        return_bfs = []
        parents= [-1]*len(list_of_connections)
        discovered = deque()
        #discovered is a dequeue
        

        #Identify the source according to what the vertex value is:
       
        discovered.append(source)
        
        while len(discovered) > 0:

            #pop it
            
            u = discovered.popleft()
            if u != None:
                u.visit_node() 
           
            #this means that u has been visited

                return_bfs.append(u.id)
            
            if u != None:
                for edge in u.edges:
                    
                    v = edge.v
                    
                    #If our BFS algorithm is able to find a path from the source to the target then it means
                    #that ford fulkerson still needs to be executed. Hence, it is false that the ford-fulkerson 
                    #has been finished.
                    if v.id == super_target:
                        
                        return False
                    

                    if v.discovered == False:

                        discovered.append(v)
                        #this means that v has been discovered
                        v.added_to_queue()
        
        #This means that the source vertex  is not able to reach the super target vertex
        return True

           

       

class Vertex:

    def __init__(self,id):
        """
    
        Written by Jian Sen Chan

        Precondition: self.id != None
        Postcondition: self.vertices != None

        Input:
            None
        Return:
            None

        Time complexity: 
            Best: O(1)
            Worst: O(1)
        Space complexity: 
            Input: O(1)
            Aux: O(1)

        This function helps to initialise a vertex to represent every data centre in the network.
        It also stores attributes which will be referenced by other functions later on.

        """     
        
        self.id = id
        self.edges = []
        #self.edges is for the forward edge
        self.backward_edge = []
        #self.backward edge is for the reverse edges
        self.discovered = False
        self.visited = False
        

    def __str__(self):

        """
    
        Written by Jian Sen Chan

        Precondition: self.id != None
        Postcondition: type(return_string) == string

        Input:
            None
        Return:
            Vertex number in string format

        Time complexity: 
            Best: O(1)
            Worst: O(1)
        Space complexity: 
            Input: O(1)
            Aux: O(1)

        This function returns vertices in string format.

        """
        return_string = str(self.id)
        return return_string

    def added_to_queue(self):

        """
    
        Written by Jian Sen Chan

        Precondition: self.id != None
        Postcondition: self.discovered != False

        Input:
            None
        Return:
            None

        Time complexity: 
            Best: O(1)
            Worst: O(1)
        Space complexity: 
            Input: O(1)
            Aux: O(1)

        This function changes the attribute "discovered" of the vertex to "True", which is used 
        to indicate that the breath first search is eyeing on this vertex.

        """
        self.discovered = True

    def visit_node(self):

        """
    
        Written by Jian Sen Chan

        Precondition: self.id != None
        Postcondition: self.visited != False

        Input:
            None
        Return:
            None

        Time complexity: 
            Best: O(1)
            Worst: O(1)
        Space complexity: 
            Input: O(1)
            Aux: O(1)

        This function changes the attribute "visited" of the vertex to "True", which is used 
        to indicate that the breath first search has visited this vertex.

        """

        self.visited = True

    def unvisit_node(self):

        """
    
        Written by Jian Sen Chan

        Precondition: self.id != None
        Postcondition: self.visited != True

        Input:
            None
        Return:
            None

        Time complexity: 
            Best: O(1)
            Worst: O(1)
        Space complexity: 
            Input: O(1)
            Aux: O(1)

        This function changes the attribute "visited" of the vertex to "False".
        This is used to reset all the vertices to be unvisited after a breadth first
        search has been done.

        """
        self.visited = False


class Edge:
    """

    Written by Jian Sen Chan

    Precondition: self.u != None
    Postcondition: self.u != None

    Input:
        None
    Return:
        None

    Time complexity: 
        Best: O(1)
        Worst: O(1)
    Space complexity: 
        Input: O(1)
        Aux: O(1)

    This function helps to initialise an edge to represent a connection between two data centres in a network
    It stores both the vertex which is sending data and the vertex which is receiving data and the amount of
    data flow between them.

    """    
    def __init__(self,u,v,w):

        self.u = u
        self.v = v
        self.w = w


#Create a graph with 5 vertices



# ==================== Q1 Code ====================

def maxThroughput(connections, maxIn, maxOut, origin, targets):
    """
    This function is for Q1
    Written by Jian sen

    Precondition: '' not in connections[2][i for i in connections]
    Postcondition: max_flow > 0

    Input:
        connections: The list of edges in the network in list form. A super target is also added in this list as there are multiple targets.
        maxIn: The list specifying the maximum amount of incoming data that data centres can process 
        maxOut: The list specifying the maximum amount of outgoing data that data centres can process per second
        origin: The integer signifying where the data is located
        targets: The list of integers specifying the locations at which data needs to be stored
    Return:
        max_flow: the maximum flow of data from the origin into the targets

    Time complexity: 
        Best: O(DC)
        Worst: O(DC^2)
    Space complexity: 
        Input: O(DC^2)
        Aux: O(DC^2)

    Description:

    
    This function helps to find the maximum amount of data which can be passed from the origin to the targets. 
    
    
    Part 1: Preprocessing the input
    Firstly, it does so by firstly preprocessing the list of connections in such a way that all the connections are in list form.
    Secondly, it adjusts the values of the maximum throughputs in the connections according to the maxIn and maxOut.
    Thirdly, it adds a super target to the connections given that there are multiple targets in the network so that ford fulkerson
    can be done.

    Part 2: Execution of Ford fulkerson
    Firstly, a residual network graph is created according to the list of connections and breadth first search is called upon it
    as part of path augmentation (finding a path)
    Secondly, a backtracker is used to update the flow from the origin to the super target in that particular path
    Thirdly, a checker called "ford_fulkerson_ended" would be used to check if there are any more paths left to augment. If so, 
    then we will repeat the first and second step. If not, then we will return the maximum flow.


    """
    
    ##Part 1: Preprocessing the input
    #Change the connections list to a list of lists and not a list of tuples
    connections_1 = tuple_to_string_converter(connections)
    
    #Ensure that all the maxIn and maxOut numbers do not have any affect on the graph to be shown
    connections_2 = maxIn_maxOut_cleaner(connections_1, maxIn, maxOut,targets,origin)
    print(connections_2)
    #Ensure that in the event that there are multiple targets, a super target is added into the connection
    connections_3 = super_target_adder(connections_2, maxOut,targets)
    length = len(maxIn) + 1


    ###Part 2: Perform Ford Fulkerson 
    #Fold Fulkerson is a combination of the function bfs() and backtracker()
    my_graph =  ResidualNetwork(connections_3,length)

    parents = my_graph.bfs(origin,length)
    #this list called backtracker_data consists of the flow of the network and the updated list of connections
    backtracker_data = my_graph.backtracker(origin,parents)
    #This shows the current flow of the network which we are going to accumulate overtime
    max_flow = backtracker_data[0]
    #This updated list_of_connections is according to the current residual network which is being built
    updated_list_of_connections = backtracker_data[1]

    super_target = connections_3[-1][1]
    #Continue running Ford-Fulkerson until there is no more path left to augment
    stop = False
    while stop != True:
        my_graph_2 = ResidualNetwork(updated_list_of_connections,length)
        
        #This means that there is no more path to augment and we are done.
        if my_graph_2.ford_fulkerson_ended(origin,super_target,updated_list_of_connections) == True:
            
            stop = True
        
        #This means to continue ford-fulkerson because we are not done 
        #Fold Fulkerson is a combination of the function bfs() and backtracker()
        else:
            my_graph = ResidualNetwork(updated_list_of_connections,length) #We use the updated graph to continue the ford_fulkerson
            parents = my_graph.bfs(origin,length)
            backtracker_data = my_graph.backtracker(origin,parents)
            max_flow =  max_flow + backtracker_data[0]
            updated_list_of_connections = backtracker_data[1]
   
    return max_flow
    
    

    
def tuple_to_string_converter(connections):
    """
    This function is for Q1
    Written by Jian sen

    Precondition: type(connections) == <class 'tuple'>
    Postcondition: type(connections) != <class 'tuple'> 

    Input:
        connections: The list of edges in the network in list form. A super target is also added in this list as there are multiple targets.
    Return:
        connections_list: The exact same thing as connections but in nested list form

    Time complexity: 
        Best: O(C)
        Worst: O(C)
    Space complexity: 
        Input: O(C)
        Aux: O(C)

    This function converts the list of tuples to a nested list for easier processing in the other functions.
    """
    connections_list = []


    for i in range(0,len(connections)):

        connections_list.append([connections[i][0],connections[i][1],connections[i][2]])

    return connections_list



  


def maxIn_maxOut_cleaner(connections, maxIn, maxOut, targets, origin):
    
    """
    This function is for Q1
    Written by Jian Sen Chan

    Precondition: len(connections) > 0
    Postcondition: len(new_connections) <= len(connections)

    Input:
        connections: The list of edges in the network in list form. A super target is also added in this list as there are multiple targets.
        maxIn: The list specifying the maximum amount of incoming data that data centres can process 
        maxOut: The list specifying the maximum amount of outgoing data that data centres can process per second
        targets: The list of integers specifying the locations at which data needs to be stored
        origin: The integer signifying where the data is located
        
    Return:
        new_connections: The updated list of connections 

    Time complexity: 
        Best: O(DC)
        Worst: O(DC)
    Space complexity: 
        Input: O(DC)
        Aux: O(DC)
    
    Compare the maxIn and maxOut and use the values in the maxIn and maxOut to "update" what the
    the limit of how big the capacities in the network should be. 
    We need to perform this because sometimes it could be that the maxIn is bigger than 
    the maxOut for a particular data centre i and vice versa.
    
    Part 1 of the code: Reducing the incoming capacity
    We should then make the capacity going into the data centre i
    to be only as big as the maxOut (unless it is part of the target because the target does not need to flow data out).
    The reason for doing so is because it does not make any sense for the maximum amount of data coming into data 
    centre i to be bigger than the maximum amount of data going out. If we did so, it is creating opportunity for "wasted" data flow. 
    The data centre i will be redundantly storing extra weightage which cannot be flowed out from it.

    Part 2 of the code: Reducing the outgoing capacity
    We should also make the make the maximum amount of data coming out from a data centre as big as how much it can receive (unless it is the origin).
    This is because a data centre will not be able to flow more data out than it can receive.
    """
    #Sort it in ascending 
    amount_to_subtract = []
    for i in range(0,len(connections)-1):
        if connections[i][2] > connections[i+1][2]:
            connections[i], connections[i+1] = connections[i+1], connections[i]

    #Part 1:  Reducing the incoming capacity
    #For every vertex, update the outgoing connections  
    for j in range(0,len(maxOut)):
        total_outgoing_flows = 0
        for k in range(0,len(connections)):
            if connections[k][0] == j:
                total_outgoing_flows += connections[k][2]
        if total_outgoing_flows > maxOut[j]:
            to_subtract = total_outgoing_flows - maxOut[j]
            amount_to_subtract.append(to_subtract)
          
        else:
            amount_to_subtract.append(0)
    
    for j in range(0,len(maxOut)):
        for k in range(0,len(connections)):
            if connections[k][0] == j:
                if (connections[k][2] - amount_to_subtract[j]) > 0:
                    connections[k][2] = connections[k][2] - amount_to_subtract[j]
                    amount_to_subtract[j] = 0
                elif (connections[k][2] - amount_to_subtract[j]) < 0:
                    amount_to_subtract[j] = amount_to_subtract[j] - connections[k][2]
                    connections[k][2] = 0
    
    amount_to_subtract_2 = []
    
    #Part 2:  Reducing the  outgoing capacity
    #For every vertex, update the incoming connections  
    for j in range(0,len(maxIn)):
        total_incoming_flows = 0
        for k in range(0,len(connections)):
            if connections[k][1] == j:
                total_incoming_flows += connections[k][2]
        if total_incoming_flows > maxIn[j]:
            to_subtract = total_incoming_flows - maxIn[j]
            amount_to_subtract_2.append(to_subtract)
        else:
            amount_to_subtract_2.append(0)
    
    for j in range(0,len(maxIn)):
        for k in range(0,len(connections)):
            if connections[k][1] == j:
                if (connections[k][2] - amount_to_subtract_2[j]) > 0:
                    connections[k][2] = connections[k][2] - amount_to_subtract_2[j]
                    amount_to_subtract_2[j] = 0
                elif (connections[k][2] - amount_to_subtract_2[j]) < 0:
                    
                    amount_to_subtract_2[j] = amount_to_subtract_2[j] - connections[k][2]
                    connections[k][2] = 0
    
    new_connections = []

    #Getting the new list of connections and discarding the ones that are not flowing data anymore
    for c in range(0,len(connections)):
        if connections[c][2] != 0:
            new_connections.append(connections[c])  
    
    return new_connections

def super_target_adder(connections,maxOut,targets):

    """
        
    This function is for Q1
    Written by Jian Sen Chan

    Precondition: len(connections) > 0
    Postcondition: len(connections) >= len(connections) + 1

    Input:
        connections: The list of edges in the network in list form. A super target is also added in this list as there are multiple targets.
        maxOut: The list specifying the maximum amount of outgoing data that data centres can process per second
        targets: The list of integers specifying the locations at which data needs to be stored
    
        
    Return:
        connections: The updated list of connections that has a super target

    Time complexity: 
        Best: O(D)
        Worst: O(D)
    Space complexity: 
        Input: O(D)
        Aux: O(D)
    
    
    Since there are multiple targets to be reached, we need to add a "super target" that connects both targets
    to a final target in order that the graph can be processed by Ford Fulkerson later on.

    This is part and parcel of preprocessing the input.

    Since we are going to add a new super target, we need to make sure that the maximum throughput from the
    targets to the super target are befitting the conditions set by maxOut. Hence, we will refer to the maxOut 
    of the targets to know what should be the throughput from the target to the super target.
    
    """

    #The length of maxIn is basically: the number of vertices + 1
    #I will be using this number to represent the super target
    super_target = len(maxOut)
    for target in targets:
        connections.append([target,super_target,maxOut[target]])
    return connections

# ==================== Q2 Code ====================



class Node:

    """
    Class for Q2
    This class contains the nodes used in the CatsTrie. Each node is meant to represent the the letter of a word.
    """
    
    def __init__(self, freq=None,uniq_freq=None,level=None,size = 27,previous=None,letter = None, data=None, terminals = None):
        """
        Init for the node class
        Written by Jian Sen chan

        Precondition: size > 0 
        Postcondition: len(self.link) = size

        Input:
            freq: the frequency of a letter in the trie
            uniq_freq: the frequency of a letter in the trie insofar as it is able to construct a unique word. 
        Return:
            None

        Time complexity: 
            Best: O(1)
            Worst: O(1)
        Space complexity: 
            Input: O(1)
            Aux: O(1)
        """
        #Terminal $ is at the index 0
        self.link = [None] *size
        #payload
        self.freq = freq
        self.uniq_freq = uniq_freq
        self.level = level
        self.previous = previous
        self.letter = letter
        self.data = data
        self.terminals = []  #This is meant to point to store the terminals of child node inside it

class CatsTrie:

    """
    Class for Q2
    This class represents the CatsTrie, which is used to encapsulate all of the cat sentences.
    """
    def __init__(self,sentences):
        
        """
        Init for the CatsTrie class
        Written by Jian Sen chan

        Precondition: sentences != None
        Postcondition: sentences != None

        Input:
            sentences: the list of sentences representing the cat sentences 
        Return:
            None

        Time complexity: 
            Best: O(MN)
            Worst: O(MN)
        Space complexity: 
            Input: O(MN)
            Aux: O(MN)
        """
        
        self.root = Node(level=0)
        self.sentences = sentences
        for sentence in sentences:
            self.insert(sentence)
        

    def insert(self, key):
        """
        Init for the node class
        Written by Jian Sen chan

        Precondition: size > 0 
        Postcondition: len(self.link) = size

        Input:
            freq: the frequency of a letter in the trie
            uniq_freq: the frequency of a letter in the trie insofar as it is able to construct a unique word. 
        Return:
            current: the current node

        Time complexity: 
            Best: O(M)
            Worst: O(M)
        Space complexity: 
            Input: O(M)
            Aux: O(M)

        Decsription:

        Part 1: Insertion of all the letters.
        Firstly, the function helps to insert all the letters into the Trie, and keeps note of the basic information such as the frequency of the letter's appearance

        Part 2: Insertion of the terminal node
        Secondly, the function will add the terminal node once a word has been added to demarcate that the word has been completely inserted

        Part 3: Storage of words in parent node
        We then want to ensure that all of the parent nodes are able to have a form of access to the terminal for easier referencing to it later on

        Part 4: Updating unique frequency of every letter.
        We will then traverse back to the bottom most node which was just inserted and slowly update the unique frequency of every letter from the bottom to the top node
        """
        if key == "":
            raise Exception("Please ensure that every sentence in 'sentences' is not blank")
        
        
        #Part 1: Insertion of all the letters
        count_level = 0 #Counts how far the node is from the source node
        #begin from the root
        current = self.root
        #going through letter one by one to add nodes or update the frequency of the nodes
        
        for char in key:

            #find out the index
            index = ord(char) - 97 + 1

            if current.link[index] is not None:
                count_level = count_level + 1
                current.link[index].previous = current
                current = current.link[index]
                #Increase the frequency because letter is the same
                #If we see the same letter recurring again, we need to add 1 to the frequency of the letter's appearing
                current.freq = current.freq + 1

                #We put the value of the frequency as the unique frequency for now (although it is not the case) because we will
                #perform something later which would return us the actual unique frequency
                current.uniq_freq = current.freq

                #We will also store the current letter char in the node
                current.letter = char
            else:
                #create a new node for the letter
                count_level = count_level + 1
                current.link[index] = Node(level=count_level) 
                current.link[index].previous = current
                current = current.link[index]
                current.freq = 1
                #Since this is the first time that the letter is occuring, we will set the frequency to 1 

                #You need to traverse back to update the unique frequency
                
                #We put the value of the frequency as the unique frequency for now (although it is not the case) because we will
                #perform something later which would return us the actual unique frequency
                current.uniq_freq = current.freq
                

                #We will also store the current letter char in the node
                current.letter = char
                
        #Part 2: Insertion of all the terminal node
        #Add the terminal $ if it is not present
        index = 0
        if current.link[index] is not None:
            count_level = count_level + 1
            current.link[index].previous = current
            current = current.link[index]
            current.freq = current.freq + 1
            #We put the value of the frequency as the unique frequency for now (although it is not the case) because we will
            #perform something later which would return us the actual unique frequency
            current.uniq_freq = current.freq
        else:
            count_level = count_level + 1
            #create a new Node for the terminal $
            current.link[index] = Node(level=count_level)
            current.link[index].previous = current
            current = current.link[index]
            current.freq = 1
            #We put the value of the frequency as the unique frequency for now (although it is not the case) because we will
            #perform something later which would return us the actual unique frequency
            current.uniq_freq = current.freq

            #We now want to store the key as the data of the terminal node. This stores the sentences in the Trie 
            current.data = key


        #Part 3: Keeping terminal nodes in all parent nodes
        terminal = current    
        #We then want to ensure that all of the parent nodes are able to have a form of access to the terminal for easier referencing to it later on
        self.stored_terminals(current,terminal)


        #Part 4: Update the unique frequency of all of the letters        
        current = self.root
        i = 0
        index = ord(key[i]) - 97 + 1
        current = self.traverse(current,key,i,index)
        
        if current.freq > 1:
            
        #This means that there is more than one copy of the exact same word
        #We then need to subtract all of the unique frequency values by 1 
        #because previously we made unique frequency equivalent to the frequency values
            
            self.unique_freq_updated(current)    

        return current

    def stored_terminals(self,current,terminal):
        """
        Written by Jian Sen Chan

        Precondition: current != None
        Postcondition: current != None

        Input:
            current: reference to a node
        Return:
            None or a call back to itself with the parent node

        Time complexity: 
            Best: O(1)
            Worst: O(M)
        Space complexity: 
            Input: O(M)
            Aux: O(M)

        The purpose of this function is to ensure that every parent node of the terminal node is able to instantly have access to 
        the terminal node. 

        This is for easier referencing of the terminal node from any parent node and will be extremely useful when it comes to finding
        out the most freqent word used.
        """

        if current == self.root:
            current.terminals.append(terminal)
            return None
        current.terminals.append(terminal)
        return self.stored_terminals(current.previous,terminal)



    def traverse(self,current,key,i,index):
        """
        Written by Jian Sen Chan

        Precondition: current != None
        Postcondition: current != None

        Input:
            current: reference to a node
        Return:
            curent or a call back to itself with the parent node

        Time complexity: 
            Best: O(1)
            Worst: O(M)
        Space complexity: 
            Input: O(M)
            Aux: O(M)

        O(M)

        We will use this traverse back to the bottom most node which was just inserted and 
        slowly update the unique frequency of every letter from the bottom to the top node
        """
        if i < len(key):
            index = ord(key[i]) - 97 + 1
        if current.link[index] is not None:
            current = current.link[index]
            i = i + 1
            return self.traverse(current,key,i,index)
        elif current.link[index] is None:
            return current

    def unique_freq_updated(self,current):
        """
        Written by Jian Sen Chan

        Precondition: current != None
        Postcondition: current != None

        Input:
            current: reference to a node
        Return:
            current or a call back to itself with the parent node

        Time complexity: 
            Best: O(1)
            Worst: O(M)
        Space complexity: 
            Input: O(M)
            Aux: O(M)

        The purpose of this function is to help update the unique frequency of each and every letter at a node.
        
        """
        
        if current == self.root:
            return current
        else:
            current.uniq_freq = current.uniq_freq - 1
            return self.unique_freq_updated(current.previous)
        

    def autoComplete(self,prompt):
        
        """
        Written by Jian Sen Chan

        Precondition: self.root.link != [None]*27
        Postcondition: self.root != None

        Input:
            prompt: input given by a user to see if there is such a word in the CatsTrie
        Return:
            most_frequent_word: the word which is predicted to be the closest to prompt

        Time complexity: 
            Best: O(X+Y)
            Worst: O(X+Y)
        Space complexity: 
            Input: O(X+Y)
            Aux: O(X+Y)

        The purpose of this function is to find the word in the Trie which closely resembles the prompt entered by the user.
        If there is no output like it, a None will be returned.
        
        """
        #Exception statement if the Trie is empty
        if self.root.link == [None]*27:
            raise Exception("The Trie is empty. Please fill it up first.")

        sentence = ""
        current = self.root
        

        
        #The purpose of this block of code is to help weed out any prompts which do not 
        #are not prefixes of any of the words in the sentences
        #Apart from that, it also helps to situate the current at prompt[len(prompt)-1]
        #which is is needed for the next operation
        for i in range(0,len(prompt)):
            index = ord(prompt[i]) - 97 + 1

            if current.link[index] == None:
                sentence = None
                return sentence
            #elif current.link[index] != None:
                #sentence = sentence + prompt[i]
                
            current = current.link[index]

        highest_frequency = 0
        most_frequent_word = None

        for node in current.terminals:
            
            if node.freq > highest_frequency:
                highest_frequency = node.freq
                
                most_frequent_word = node.data
 
            elif node.freq == highest_frequency:
                #Compare which is lexicographically smaller if both have the same frequency
                if node.data < most_frequent_word:
                    most_frequent_word = node.data
        return most_frequent_word
        
        
if __name__ == "__main__":
    
    connections = [(0, 1, 3000), (1, 2, 2000), (1, 3, 1000), (0, 3, 2000), (3, 4, 2000), (3, 2, 1000)]
    maxIn = [5000, 3000, 3000, 3000, 2000]
    maxOut = [5000, 3000, 3000, 2500, 1500]
    origin = 0
    targets = [4, 2]
    print(maxThroughput(connections, maxIn, maxOut, origin, targets))


    sentences = ["abc", "abczacy", "dbcef", "xzz", "gdbc", "abczacy", "xyz","abczacy", "dbcef", "xyz", "xxx", "xzz"]
    mycattrie = CatsTrie(sentences)
    prompt = "abc"
    print(mycattrie.autoComplete(prompt))


##References:
##No references used