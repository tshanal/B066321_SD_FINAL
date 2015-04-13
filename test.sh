#!/bin/bash

echo "This is the script for testing Ant colony optimization"
 
# These are the test cases for the ANt colony optmization Tsp solver.
# This file contain the test cases and test data. 

python unitTest.py 

sleep 10 &
wait %1
