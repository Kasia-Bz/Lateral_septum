# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 10:51:42 2021

@author: katar
"""

from pathlib import Path
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
#%matplotlib inline
#%matplotlib notebook
plt.style.use('seaborn-ticks')

#from data_analysis import loading
from fklab.spikes.Kilosort import KiloSortResult

# import
from fklab.signals.time_alignment import *
from fklab.io.neuralynx.nlx_sync import nlx_retrieve_event, nlx_start_recording_time
from fklab.io.spikeGLX.glx_sync import glx_extra_sync_signal

project_path = None

""" Time alignment function """
pathnlx = Path('/mnt/fk-fileserver/Project_LS/LS_k_8/110220/Neuralynx_data/2021-02-11_12-35-54/DLC/Events.nev')
pathglx = Path('/mnt/fk-fileserver/Project_LS/LS_k_8/110220/110221_g0/110221_g0_imec0/110221_g0_t0.imec0.lf.bin')
def align_time(align_file, pathnlx, pathglx):
    if align_file.exists():
        ta = TimeAlignment.load(align_file)
    else:
    # load Neuralynx data
        nlx_file = pathnlx
        nlx_data = nlx_retrieve_event(nlx_file)

    # load Neuropixels data
        glx_file = pathglx
        glx_data = glx_extra_sync_signal(glx_file)

    # here use another style to create a TimeAlignment instance.
        ta = TimeAlignment({
            'nlx': nlx_data,
            'npx': glx_data
            })

    # trigger time alignment, and exam whether the value make sense or not.
        print(ta.avg_time_offset('npx'))
    
    return(ta)
[613,2300]
def load_pos(epoch, ):

    Y_maze_epoch = epoch
    
    position_time = np.array(loading.position_time)

    nan_array = np.isnan(position_time)
    not_nan_array = ~ nan_array
    position_time = position_time[not_nan_array]

    position_at = loading.position[np.logical_and(position_time> Y_maze_epoch[0],
                                     position_time < Y_maze_epoch[1]), :]
    
    position_at_cm = position_at * 0.5
    
    x=position_at[:,0]
    y=position_at[:,1]

    xy = np.column_stack([position_at])
    
    plt.plot(x,y)
    plt.gca().invert_yaxis()
    return(position_at, xy)


