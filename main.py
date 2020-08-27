#!/usr/bin/python2.7

from random import randint
from pandas import *

MAX_VOLUME = 10
MAX_VALUE = 20

def generate_random_values(size):
    return [ randint(1,MAX_VALUE) for i in range(size)]

def generate_random_volumes(size):
    return [ randint(1,MAX_VOLUME) for i in range(size)]

def greedy_solution(capacity,values,volumes):
    # Compute the ratio between value and volume
    ratio = [values[i]/float(volumes[i]) for i in range(len(values))]
    index = [i+1 for i in range(len(values))]

    # Sort the couples (value/volume) according to the ratio
    ratio,values, volumes,index = (list(l) for l in zip(*sorted(zip(ratio,values, volumes,index),reverse=True)))

    # Add elements until the volume is too important
    sum_volumes = 0
    sum_values = 0
    subset = []
    id = 0
    while sum_volumes + volumes[id] <= capacity:
        sum_volumes += volumes[id]
        sum_values += values[id]
        subset.append(index[id])
        id += 1

    return(sum_volumes,sum_values,subset)


def dynamic_solution(capacity,values,volumes):
    nb_items = len(values)
    subset = []
    sum_volumes = 0
    stored_max = [[0 for j in range(capacity+1)] for i in range(nb_items)]
    kept_items = [[0 for j in range(capacity+1)] for i in range(nb_items)]

    for item in range(nb_items):
        for sub_cap in range(1,capacity+1):
            if volumes[item] > sub_cap:
                stored_max[item][sub_cap] = stored_max[item-1][sub_cap]
            else:
                max_with_new_item = stored_max[item-1][sub_cap-volumes[item]] + values[item]
                max_without_new_item = stored_max[item-1][sub_cap]
                if max_with_new_item > max_without_new_item:
                    stored_max[item][sub_cap] =max_with_new_item
                    kept_items[item][sub_cap]=1
                    # print("item " + str(item))
                    # print("w " + str(sub_cap))
                else:
                    stored_max[item][sub_cap] =max_without_new_item
                    kept_items[item][sub_cap]=0

    current_volume = capacity
    # print(DataFrame(kept_items))
    for i in range(nb_items-1,-1,-1):
        # print("item = " + str(i))
        # print("w = " + str(current_volume))
        if kept_items[i][current_volume]==1:
            subset.append(i+1)
            sum_volumes += volumes[i]
            current_volume = current_volume - volumes[i]

    # print(DataFrame(stored_max))
    return sum_volumes,stored_max[nb_items-1][capacity],subset

if __name__ == "__main__":
    # Define main variables
    capacity = 15
    size = 5

    # Generate a random dataset
    # values = generate_random_values(size)
    # volumes = generate_random_volumes(size)
    values = [7,9,5,12,14,6,12]
    volumes = [3,4,2,6,7,3,5]
    # values = [6,5,1,15,18]
    # volumes = [1,7,3,7,6]
    print("values : " + str(values))
    print("volumes : " + str(volumes))

    # Verifications
    if capacity <= 0 :
        raise ValueError('Capacity should be strictly positive !')
    if len(values)!=len(volumes):
        raise ValueError('Values and volumes array should be of same size !')

    # Find a solution
    sum_vol,sum_val,subset = greedy_solution(capacity,values,volumes)
    print(str(sum_vol) + " L of goods can fit into the truck, representing a total worth of " + str(sum_val) + " euros.")
    print("The corresponding subset is composed of the elements " + str(subset))
    # Find a solution through dynamical programming
    sum_vol,sum_val,subset = dynamic_solution(capacity,values,volumes)

    # Print the solution
    print(str(sum_vol) + " L of goods can fit into the truck, representing a total worth of " + str(sum_val) + " euros.")
    print("The corresponding subset is composed of the elements " + str(subset))
