# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 10:51:42 2021

@author: katar
"""

from pathlib import Path
import numpy as np
import pandas as pd

import h5py
import numpy as np
import ruamel_yaml
import matplotlib.pyplot as plt


        
def load_pos(path, epoch):
    global position_data_path, head_direction, position, position_time, position_velocity
    position_data_path = path
    position_data = h5py.File(path, 'r')

        # diodes = position_data['diodes'].value
    head_direction = np.array(position_data['head_direction'])
    position = np.array(position_data['position'])
    position_time = np.array(position_data['time'])
    position_velocity = np.array(position_data['velocity'])

    Y_maze_epoch = epoch
    
    position_time = np.array(position_time)

    nan_array = np.isnan(position_time)
    not_nan_array = ~ nan_array
    position_time = position_time[not_nan_array]

    position_at = position[np.logical_and(position_time> Y_maze_epoch[0],
                                     position_time < Y_maze_epoch[1]), :]
    
    position_at_cm = position_at * 0.5
    
    x=position_at[:,0]
    y=position_at[:,1]

    xy = np.column_stack([position_at])
    
    
    return(position_at, xy, x, y)

def plot_position(x,y):
    plt.plot(x,y)
    plt.gca().invert_yaxis()
    
