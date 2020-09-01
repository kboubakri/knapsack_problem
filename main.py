#!/usr/bin/python2.7

from random import randint
import timeit
from pandas import *

MAX_VOLUME = 10
MAX_VALUE = 20

def generate_random_values(size):
    return [ randint(1,MAX_VALUE) for i in range(size)]

def generate_random_volumes(size):
    return [ randint(1,MAX_VOLUME) for i in range(size)]

def greedy_resolution(capacity,values,volumes):
    """
    Implementation of the greedy algorithm used to solve the Knapsack problem.
    It is based on local optimisation and rank the items based on their "efficiency"
    before summing them. It does not always lead to the optimal solution.
    """
    # Compute the ratio between value and volume
    ratio = [values[i]/float(volumes[i]) for i in range(len(values))]

    # Sort the couples (value/volume) according to the ratio
    # Add indexes to keep track of the original form
    index = [i+1 for i in range(len(values))]
    ratio,values, volumes,index = (list(l) for l in zip(*sorted(zip(ratio,values, volumes,index),reverse=True)))

    # Add elements until the volume is too important
    sum_volumes = 0
    sum_values = 0
    subset = []
    id = 0
    while id < len(values) and sum_volumes + volumes[id] <= capacity:
        sum_volumes += volumes[id]
        sum_values += values[id]
        subset.append(index[id])
        id += 1

    return(sum_volumes,sum_values,sorted(subset))

def dynamic_resolution(capacity,values,volumes):
    """
    Implementation of the dynamical programming algorithm used to solve the Knapsack problem.
    First, it build a capacity*nb_of_items matrix containing the maximum value for all the
    (capacity,nb_items) sub couples. Then, it return the value for the desired couple.
    """
    # Initalization of the variables
    nb_items = len(values)
    subset = []
    sum_volumes = 0
    # Used to keep track of the maximum value possible for each sub capacities
    stored_max = [[0 for j in range(capacity+1)] for i in range(nb_items)]
    # Used to keep track of the items in the final subset
    kept_items = [[0 for j in range(capacity+1)] for i in range(nb_items)]

    # Construction of the table containing the maximum value of a shipment
    # According to the number of items and the total capacity
    for item in range(nb_items):
        for sub_cap in range(1,capacity+1):
            # If the volume of the item is bigger than the sub capacity
            if volumes[item] > sub_cap:
                # Same max as the previous item
                stored_max[item][sub_cap] = stored_max[item-1][sub_cap]
            else:
                max_with_new_item = stored_max[item-1][sub_cap-volumes[item]] + values[item]
                max_without_new_item = stored_max[item-1][sub_cap]
                # Max value is higher if the new item is had
                if max_with_new_item > max_without_new_item:
                    stored_max[item][sub_cap] = max_with_new_item
                    kept_items[item][sub_cap]= 1 # Tells that the item belongs to the subset
                # The new item should not be added
                else:
                    stored_max[item][sub_cap] = max_without_new_item
                    kept_items[item][sub_cap]=0 # Tells that the item is not in the subset

    # Reverse the logic used to construct the table
    # In order to get all the elements of the subset
    current_volume = capacity
    # print(DataFrame(kept_items))
    for i in range(nb_items-1,-1,-1):
        if kept_items[i][current_volume]==1:
            subset.append(i+1) # Get the item's index
            sum_volumes += volumes[i] # Add its volume to the total volume
            current_volume = current_volume - volumes[i] # Get to the new item

    # print(DataFrame(stored_max))
    # The maximal value per shipment can be fetched directly from the table
    return sum_volumes,stored_max[nb_items-1][capacity],sorted(subset)

def print_result(sum_vol,sum_val,subset):
    print(str(sum_vol) + " L of goods can fit into the truck, representing a total worth of " + str(sum_val) + " euros.")
    print("The corresponding subset is composed of the elements " + str(subset))

def run(capacity,volumes,values):
    """
    Main function which print the max value and the used volume for the corresponding
    subset using the greedy and the dynamical programming resolution.
     """
    ## Print the dataset
    print("\nDATASET\n")
    print("values : " + str(values) + " \t (in euros)")
    print("volumes : " + str(volumes) + " \t (in L)")

    ## Verifications
    if capacity <= 0 :
        raise ValueError('Capacity should be strictly positive !')
    if len(values)!=len(volumes):
        raise ValueError('Values and volumes array should be of same size !')

    print("\n\n\nRESOLUTIONS\n")
    ## Find a non optimal solution through a greedy algorithm
    sum_vol,sum_val,subset = greedy_resolution(capacity,values,volumes)
    print("Resolution using a greedy algorithm :\n")
    print_result(sum_vol,sum_val,subset)

    ## Find a solution through dynamical programming
    sum_vol,sum_val,subset = dynamic_resolution(capacity,values,volumes)
    print("\n\nResolution using Dynamical Programming : \n")
    print_result(sum_vol,sum_val,subset)
    print("\n")

def test_accuracy(nb_execution,capacity,size):
    """
    Test the accuracy of the greedy resolution comparing to the dynamical programming
    resolution for a certain capacity and size.
    """
    differences = []
    mean_value = 0.0
    for i in range(nb_execution):
        values = generate_random_values(size)
        volumes = generate_random_volumes(size)
        a,val_greedy,b = greedy_resolution(capacity,values,volumes)
        a,val_dynamic,b = dynamic_resolution(capacity,values,volumes)
        differences.append(val_dynamic-val_greedy)
        mean_value += val_greedy
    mean_value /= nb_execution
    nb_of_success = differences.count(0)
    mean_loss = sum(differences)/(nb_execution-differences.count(0))*(100/mean_value)
    print("Out of " + str(nb_execution) + " executions, " + str(nb_of_success) + " greedy resolution have found the optimal subset.")
    print("When it was not the case, the mean loss was equal to " + str(mean_loss) + " %.")

def test_performances(nb_executions,capacity,size):
    """
    Return the total execution time for the greedy_resolution and the dynamic_resolution
    for a given capacity and size.
    """
    print("this test is done using " + str(size) + ' items and a capacity of ' + str(capacity) +" in L.")
    print("Total time for the greedy algorithm :\n")
    result = timeit.timeit('greedy_resolution(capacity,values,volumes)',globals=globals(),number=nb_executions)
    print(str(result) + " in s.")

    print("\n\nTotal time for the Dynamical Programming : \n")
    result = timeit.timeit('dynamic_resolution(capacity,values,volumes)',globals=globals(),number=nb_executions)
    print(str(result) + " in s.")

if __name__ == "__main__":
    ## Define main variables
    capacity = 15
    size = 100

    # Generate a random dataset if needed
    # values = generate_random_values(size)
    # volumes = generate_random_volumes(size)

    ## Generate the given dataset
    values = [7,9,5,12,14,6,12]
    volumes = [3,4,2,6,7,3,5]

    # test_accuracy(1000,capacity,size) # Uncomment the random dataset
    # test_performances(1000,capacity,size) # Uncomment the random dataset
    run(capacity,volumes,values)
