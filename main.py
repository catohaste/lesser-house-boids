import os
import numpy as np
import random
from matplotlib import pyplot as plt

from plot import create_animation

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
angles = random.sample(possible_angles, boid_count)

print(position.shape, len(angles))

create_animation(position, angles, xylimits=limits, view='top')

