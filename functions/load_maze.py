# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 16:54:26 2021

@author: katarzyna
"""

from pathlib import Path
import ruamel_yaml
import h5py
import numpy as np

from fklab.geometry.shapes import graph, polyline, rectangle, polygon

environment_yaml = None

def load_environment_yaml(path):
    global environment_yaml
    if path is None:
        path = str(Path(path).with_name('environment.yaml'))

    with open(path) as f:
        environment_yaml = ruamel_yaml.YAML().load(f)
        
        
def maze():
    Y_maze_data = environment_yaml['ymaze']['shapes']['ymaze']['shape']
    Y_maze_data['polylines'] = [polyline(**p) if not isinstance(p, polyline) else p for p in Y_maze_data['polylines']]
    ymaze = graph(**Y_maze_data)
    
    RR = environment_yaml['ymaze']['shapes']['RR']['shape']
    RR = rectangle(**RR)
    RR = RR.aspolygon()

    LR = environment_yaml['ymaze']['shapes']['LR']['shape']
    LR = rectangle(**LR)
    LR = LR.aspolygon()

    HR = environment_yaml['ymaze']['shapes']['HR']['shape']
    HR = rectangle(**HR)
    HR = HR.aspolygon()

    CP = environment_yaml['ymaze']['shapes']['CP']['shape']
    CP = rectangle(**CP)
    CP = CP.aspolygon()

    w_CP = environment_yaml['ymaze']['shapes']['with_CP']['shape']
    w_CP = rectangle(**w_CP)
    w_CP = w_CP.aspolygon()
    
    return(RR, LR, HR, CP, w_CP)

def plot_maze(RR, LR, HR, CP, w_CP):
    Y_maze_data = environment_yaml['ymaze']['shapes']['ymaze']['shape']
    Y_maze_data['polylines'] = [polyline(**p) if not isinstance(p, polyline) else p for p in Y_maze_data['polylines']]
    ymaze = graph(**Y_maze_data)
    ymaze.plot_path()
    CP.plot_path()
    RR.plot_path()
    LR.plot_path()
    HR.plot_path()
    w_CP.plot_path()