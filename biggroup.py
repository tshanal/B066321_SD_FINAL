import math
import random
import sys
import ConfigParser
from work import Work

# BigGroup class initilize the Group of Ants which move in the graph
# The big group is controlled by number of parametrs and it take input 
# (graph, num_ants, num_iterations) 
# Graph can be gentrated by graph class	 

 
class BigGroup:
    def __init__(self, graph, num_ants, num_iterations):
        self.graph = graph
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.initConfigParser()
        self.Alpha=self.config.getfloat('BigGroup', 'Alpha')
        self.reset()
    # initlize the ConfigParser
    def initConfigParser(self):
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open('config.ini'))         
    # Resets the ant poition 
    def reset(self):
        #self.optimalCostArray = sys.maxint
        self.optimalCostArray = sys.maxsize
        self.optimalPath = None
        self.bestPathArray = None
        self.lastpathiter = 0
    # Starts the ants similations	
    def start(self):
        self.ants = self.c_workers()
        self.iter_counter = 0

        while self.iter_counter < self.num_iterations:
            self.iteration()
            # Note that this will help refine the results future iterations.
            self.global_updating_rule()
    # Iterate over the ants and run them.	
    def iteration(self):
        self.avg_path_cost = 0
        self.ant_counter = 0
        self.iter_counter += 1
        for ant in self.ants:
            ant.run()

    def num_ants(self):
        return len(self.ants)

    def num_iterations(self):
        return self.num_iterations

    def iteration_counter(self):
        return self.iter_counter
    # Update the optimal Path and optimalCostArray after each ents 	     	 
    # moved over the nodes in Graph	
    def update(self, ant):
        print ("Update called by %s" % (ant.ID,))
        self.ant_counter += 1
        self.avg_path_cost += ant.path_cost
        if ant.path_cost < self.optimalCostArray:
            self.optimalCostArray = ant.path_cost
            self.bestPathArray = ant.path_mat
            self.optimalPath = ant.path_vec
            self.lastpathiter = self.iter_counter
        if self.ant_counter == len(self.ants):
            self.avg_path_cost /= len(self.ants)
            print ("Best: optimalPath %s \n optimalCostArray %s \n iter_counter %s \n avg_path_cost %s" % (
                self.optimalPath, self.optimalCostArray, self.iter_counter, self.avg_path_cost,))


    def done(self):
        return self.iter_counter == self.num_iterations
    # Initlize the Ants at random location n Graph and Returns the Ants array array	
    def c_workers(self):
        self.reset()
        ants = []
        for i in range(0, self.num_ants):
            ant = Work(i, random.randint(0, self.graph.num_nodes - 1), self)
            ants.append(ant)

        return ants
    # Test Funtion works similar to but initlize the fix position
    def c_workers_test(self,placeSeed):
        self.reset()
        ants = []
        for i in range(0, self.num_ants):
            self.ant = Work(i, placeSeed , self)
            ants.append(self.ant)

        return ants
    # Update the evaporation and Deposition (pheromones)after movement at each iteration	
    def global_updating_rule(self):
        #can someone explain this
        evaporation = 0
        deposition = 0
        for r in range(0, self.graph.num_nodes):
            for s in range(0, self.graph.num_nodes):
                if r != s:
                    delt_tau = self.bestPathArray[r][s] / self.optimalCostArray
                    evaporation = (1 - self.Alpha) * self.graph.tau(r, s)
                    deposition = self.Alpha * delt_tau
                    self.graph.update_tau(r, s, evaporation + deposition)

 # Graph Class is ised to initlize the graph on which the ants will be move
 # This class take the construtor values (num_nodes, cost_matix, tau_mat=None) 
 # This class genrates the delta , tau and etha matrix 
 # (Distance matrix , Phermones level , inverse of Distance matrix )


class GraphBit:
    def __init__(self, num_nodes, delta_mat, tau_mat=None):
        print (len(delta_mat))
        if len(delta_mat) != num_nodes:
            raise Exception("len(delta) != num_nodes")
        self.num_nodes = num_nodes
        self.delta_mat = delta_mat 
        if tau_mat is None:
            self.tau_mat = []
            for i in range(0, num_nodes):
                self.tau_mat.append([0] * num_nodes)

    def delta(self, r, s):
        return self.delta_mat[r][s]
    # Phermones deposited by the ants  	
    def tau(self, r, s):
        return self.tau_mat[r][s]

    def etha(self, r, s):
        return 1.0 / self.delta(r, s)

    def update_tau(self, r, s, val):
        self.tau_mat[r][s] = val

    def reset_tau(self):
        avg = self.average_delta()
        self.tau0 = 1.0 / (self.num_nodes * 0.5 * avg)
        print ("Average = %s" % (avg,))
        print ("Tau0 = %s" % (self.tau0))
        for r in range(0, self.num_nodes):
            for s in range(0, self.num_nodes):
                self.tau_mat[r][s] = self.tau0


    def average_delta(self):
        return self.average(self.delta_mat)


    def average_tau(self):
        return self.average(self.tau_mat)

    def average(self, matrix):
        sum = 0
        for r in range(0, self.num_nodes):
            for s in range(0, self.num_nodes):
                sum += matrix[r][s]

        avg = sum / (self.num_nodes * self.num_nodes)
        return avg

