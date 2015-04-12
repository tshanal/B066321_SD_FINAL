import pickle
import sys
import traceback
from biggroup import BigGroup
from biggroup import GraphBit
import json

def main(argv):
    nodes_count = 10

    if len(argv) >= 3 and argv[0]:
        nodes_count = int(argv[0])
    else:
	print "Expected 3 Inputs : <number of cities> <Name and Distance Picked file> <Output pickled file>" 		
	sys.exit(0)
	
    if nodes_count <= 10:
        ants_count = 20
        iteration_count = 12
        Outer_Repetition = 1
    else:
        ants_count = 28
        iteration_count = 20
        Outer_Repetition = 1
    
    			
    stuff = pickle.load(open(argv[1], "r"))
    citiesArray = stuff[0]
    distanceMatrix = stuff[1]
    #why are we doing this?
    if nodes_count < len(distanceMatrix):
        distanceMatrix = distanceMatrix[0:nodes_count]
        for i in range(0, nodes_count):
            distanceMatrix[i] = distanceMatrix[i][0:nodes_count]



    try:
        graph = GraphBit(nodes_count, distanceMatrix)
        optimalPath = None
        optimalCostArray = sys.maxint
        for i in range(0, Outer_Repetition):
            print "Repetition %s" % i
            graph.reset_tau()
            workers = BigGroup(graph, ants_count, iteration_count)
            print "Colony Started"
            workers.start()
            if workers.optimalCostArray < optimalCostArray:
                print "Colony Path"
                optimalPath = workers.optimalPath
                optimalCostArray = workers.optimalCostArray

        print "\n------------------------------------------------------------"
        print "                     Results                                "
        print "------------------------------------------------------------"
        print "\nBest path = %s" % (optimalPath,)
        city_vec = []
        for node in optimalPath:
            print citiesArray[node] + " ",
            city_vec.append(citiesArray[node])
        print "\nBest path cost = %s\n" % (optimalCostArray,)
        results = [optimalPath, city_vec, optimalCostArray]
        json.dump(results, open(argv[2], 'w+') , skipkeys=True,  ensure_ascii=False)
    except Exception, e:
        print "exception: " + str(e)
        traceback.print_exc()


if __name__ == "__main__":
    main(sys.argv[1:])
