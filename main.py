import os
import numpy as np
import random
from matplotlib import pyplot as plt

from plot import create_animation, create_progress_animation

current_iteration_str = '02'

boid_count = 1
limits = np.array([2000, 2000, 2000]) # x, y, z limits
centre = limits / 2

def new_flock(count, lower_limits, upper_limits):
    width = upper_limits - lower_limits
    return (lower_limits[:, np.newaxis] + np.random.rand(3, count) * width[:, np.newaxis])
    
# position[xyz, fly_idx]
position = new_flock(boid_count, np.array([centre[0]-300, centre[1]-300, centre[2]]), np.array([centre[0]+300, centre[1]+300, centre[2]]))
velocity = new_flock(boid_count, np.array([-5, -5, -2]), np.array([5, 5, 2]))

create_animation(position, velocity, current_iteration_str, xylimits=limits, view='both')


current_iteration = int(current_iteration_str)
iteration_list = [x+1 for x in range(current_iteration)]
iteration_str_list = ["{:02d}".format(iteration_number) for iteration_number in iteration_list]

# create_progress_animation('results/', iteration_str_list)