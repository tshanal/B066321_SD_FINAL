import pickle
import sys
import traceback
from biggroup import BigGroup
from biggroup import GraphBit
import json

class unitTest:
    def __init__(self):
        self.abc=10
    # Unit test cases for Graph class . Graph class is initiated with 3 nodes and distanceMatrix=[(1,2,1),(1,3,1),(1,4,0)] 
    # Some of the Trivial funtions are tested for the correctnessa and Average funtion is tested for correctness.
    # Tau_mat is genrated after resetting the graph.reset_tau()	and checked for the intented output		
    def unitTestGraph(self):
        nodes_count=3
        distanceMatrix=[(1,2,1),(1,3,1),(1,4,0)]
        graph = GraphBit(nodes_count, distanceMatrix) 
        assert graph.delta(1,2) == 1
        assert graph.tau(2,2) == 0
        assert graph.average_delta() < 1.5555555
        graph.reset_tau()
        assert(graph.tau_mat == [[0.66666666666666663, 0.66666666666666663, 0.66666666666666663], [0.66666666666666663, 0.66666666666666663, 0.66666666666666663], [0.66666666666666663, 0.66666666666666663, 0.66666666666666663]])
   	print "\n Graph Test succesfull"
    # Unit test cases for BigGroup Class
    # As there is unpredictablity in the nature of algorithm, algorithim shows random behavior. 
    # To control random behavior the and start are started on fixed node and allowed to mave .
    # If they take same Path then test is succesfull
    # This will test the Biggroup and work as this test make sure the ant optimization algorithm is working consistently  					 
    def unitTestBigGroup(self):
        nodes_count=4
        ants_count=1
        iteration_count=1
        distanceMatrix=[(5,5,5,1),(5,2,5,5),(5,5,3,5),(5,5,5,5)]
        graph = GraphBit(nodes_count, distanceMatrix)
        graph.reset_tau()
        workers = BigGroup(graph, ants_count, iteration_count)
	# Funtion c_workers_test is test funtion identical to c_workers which starts the ants but with at fixed position 
	# Implementation : workers.c_workers_test(SeedPosition)   
	workers.ants=workers.c_workers_test(1)
	#Insures numbers of spawned equal to the number of ants
        assert len(workers.ants)==ants_count        
	workers.iter_counter=0
	# Workers iterate for single iteration and implement the run in Work class. run funtions is algorithmic funtions.
	# This insures that two ants spwand in same poistion takes same path. 
	# Random behavior is also genrated by the work variable Q0 this is problitity which decided the path ant will take 
        # This is set to 0 to test frist path and set to 1 to test the other path.	 
        # For   ant.Q0 = 0 Exportaion 2 is tested      
	#Ant One 
        for ant in workers.ants:
            ant.Q0 = 0	
	workers.iteration()
	optimalPath1 = workers.optimalPath,
        optimalCostArray1 = workers.optimalCostArray
        avg_path_cost1 = workers.avg_path_cost
        # Ant Two
        workers.ants=workers.c_workers_test(1)
        workers.iter_counter=0
	workers.reset()
        for ant in workers.ants:
            ant.Q0 = 0
        workers.iteration()
	optimalPath2 = workers.optimalPath,
        optimalCostArray2 = workers.optimalCostArray
        avg_path_cost2 = workers.avg_path_cost
        assert optimalPath1 == optimalPath2
	assert optimalCostArray1 == optimalCostArray2
	assert avg_path_cost1 == avg_path_cost2
	
	 # For   ant.Q0 = 1 Exportaion 1 is tested 
	workers.reset()        
	for ant in workers.ants:
            ant.Q0 = 1	
	workers.iteration()
	optimalPath1 = workers.optimalPath,
        optimalCostArray1 = workers.optimalCostArray
        avg_path_cost1 = workers.avg_path_cost
        # Ant Two
	workers.reset()
        workers.ants=workers.c_workers_test(1)
        workers.iter_counter=0	
        for ant in workers.ants:
            ant.Q0 = 1
        workers.iteration()
	optimalPath2 = workers.optimalPath,
        optimalCostArray2 = workers.optimalCostArray
        avg_path_cost2 = workers.avg_path_cost
        assert optimalPath1 == optimalPath2
	assert optimalCostArray1 == optimalCostArray2
	assert avg_path_cost1 == avg_path_cost2
        #workers.start()
	print "\n BigGroup Test succesfull"
        workers.global_updating_rule()

def main(argv):
    ut = unitTest()
    ut.unitTestGraph()
    ut.unitTestBigGroup()

if __name__ == "__main__":
    main(sys.argv[1:])
