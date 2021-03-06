# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 17:04:25 2021

@author: katarzyna
"""
from pathlib import Path
import numpy as np
import pandas as pd

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