import os
import numpy as np
import random
from matplotlib import pyplot as plt

from plot import create_animation, create_progress_animation

current_iteration_str = '01'

boid_count = 1
limits = np.array([2000, 2000])
centre = limits / 2

def new_flock(count, lower_limits, upper_limits):
    width = upper_limits - lower_limits
    return (lower_limits[:, np.newaxis] + np.random.rand(2, count) * width[:, np.newaxis])
    
position = new_flock(boid_count, np.array([centre[0]-300, centre[1]-300]), np.array([centre[0]+300, centre[1]+300]))
# velocity = new_flock(boid_count, np.array([-5, -5]), np.array([5, 5]))
velocity = new_flock(boid_count, np.array([0, 0]), np.array([0, 0]))
possible_angles = [0,90,180,270]
angle = random.sample(possible_angles, boid_count)

# create_animation(position, angle, current_iteration_str, xylimits=limits, view='top')


current_iteration = int(current_iteration_str)
iteration_list = [x+1 for x in range(current_iteration)]
iteration_str_list = ["{:02d}".format(iteration_number) for iteration_number in iteration_list]

create_progress_animation('results/', iteration_str_list)