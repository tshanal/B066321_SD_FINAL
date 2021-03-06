import math
import random
import ConfigParser

# Work class is the majpr algorithmic class . 
# Its the work that each Ant do for simlution .
# The Ants can be started by passing the similuation object (colony) and starting node.

class Work():
    def __init__(self, ID, start_node, colony):
        self.ID = ID
        self.start_node = start_node
        self.grouping = colony
        self.curr_node = self.start_node
        self.graph = self.grouping.graph
        self.path_vec = []
        self.path_vec.append(self.start_node)
      
        self.ntv = {}
        config = ConfigParser.ConfigParser()
        config.readfp(open('config.ini')) 
        self.path_cost =  config.getint('Work', 'path_cost')   
        self.Beta =  config.getfloat('Work', 'Beta')   
        self.Q0 =  config.getfloat('Work', 'Q0')   
        self.Rho =  config.getfloat('Work', 'Rho')
        for i in range(0, self.graph.num_nodes):
            if i != self.start_node:
                self.ntv[i] = i
        self.path_mat = []
        for i in range(0, self.graph.num_nodes):
            self.path_mat.append([0] * self.graph.num_nodes)

    
    # Run funtion iterate over all the nodes in graph and apply the state trastion rules on the Ants
    # Each Ants find the new node to traverse , the path cost is updates , the path vector is append 
    # Then each Ant updates the pheromones level by calling local_updating_rule over a path.
    
    def run(self):
        graph = self.grouping.graph
        while not self.end():
            new_node = self.state_transition_rule(self.curr_node)
            self.path_cost += graph.delta(self.curr_node, new_node)
            self.path_vec.append(new_node)
            self.path_mat[self.curr_node][new_node] = 1 
            self.local_updating_rule(self.curr_node, new_node)
            self.curr_node = new_node
        self.path_cost += graph.delta(self.path_vec[-1], self.path_vec[0])
        self.grouping.update(self)
        self.__init__(self.ID, self.start_node, self.grouping)

    def end(self):
        return not self.ntv

   # state_transition_rule funtion takes the current position of Ant on the node  and returns the 
   # the new position
   # New postion depend on the Randon probality of taking the path. There are Two Explortions the Ants can have
   
    def state_transition_rule(self, curr_node):
        graph = self.grouping.graph
        q = random.random()
        max_node = -1
        if q < self.Q0:
            print ("Exploitation 1")
            max_val = -1
            val = None
            for node in self.ntv.values():
                if graph.tau(curr_node, node) == 0:
                    raise Exception("tau = 0")
                val = graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)
                if val > max_val:
                    max_val = val
                    max_node = node
        else:
            #Bob was here
            print ("Exploration 2")
            sum = 0
            node = -1
            for node in self.ntv.values():
                if graph.tau(curr_node, node) == 0:
                    raise Exception("tau = 0")
                sum += graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)
            if sum == 0:
                raise Exception("sum = 0")
            avg = sum / len(self.ntv)
            print ("avg = %s" % (avg,))
            for node in self.ntv.values():
                p = graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)
                if p > avg:
                    print ("p = %s" % (p,))
                    max_node = node
            if max_node == -1:
                max_node = node
        if max_node < 0:
            raise Exception("max_node < 0")
        del self.ntv[max_node]
        return max_node
    # This funtion updates pheromones levels
    def local_updating_rule(self, curr_node, next_node):
        #Update the pheromones on the tau matrix to represent transitions of the ants
        graph = self.grouping.graph
        val = (1 - self.Rho) * graph.tau(curr_node, next_node) + (self.Rho * graph.tau0)
        graph.update_tau(curr_node, next_node, val)


import random
import sys

