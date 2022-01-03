# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 15:46:52 2021

@author: katarzyna
"""
import numpy as np
import pandas as pd 
from fklab.spikes.Kilosort.utilities_kilosort import KiloSortResult

def load_cluster(path=None):


    dtype = np.dtype([
        ('id', np.int),
        ('Amplitude', np.float),
        ('ContamPct', np.float),
        ('KSLabel', np.dtype('U5')),
        ('amp', np.float),
        ('channel', np.int),
        ('depth', np.float),
        ('firing_rate', np.float),
        ('group', np.dtype('U5')),
        ('n_spikes', np.int),
        ('shank', np.int),
    ])

    cluster_data = np.loadtxt(path + "/cluster_info.tsv",
                 dtype=dtype, skiprows=1, delimiter='\t',
                 converters={
                     1:lambda it: float(it) if len(it) else np.nan,
                     2:lambda it: float(it) if len(it) else np.nan,
                     7:lambda fr: fr.replace(b' spk/s', b'')})

    data_good = cluster_data[cluster_data['group'] == 'good']
    
    
    
    ks = KiloSortResult(path + '/params.py') # load kilosort result
    cluster_ids = ks.get_good_cluster_group() 
    channels = ks.get_channel_for_cluster(ks.get_good_cluster_group())
    depth = ks.get_channel_pos(channels)[:, 1]

    
    summary_clusters = pd.DataFrame({'cluster_ids': cluster_ids,
                    'channels': channels,
                    'depth': depth,
                    'n_spikes': data_good["n_spikes"],
                    'firing_rate': data_good['firing_rate']})
    
    return(summary_clusters)
  

def plot_spikes_depth(summary_clusters, color):
    import matplotlib.pyplot as plt
    plt.rcParams["figure.figsize"] = (8,10)
    plt.scatter(summary_clusters['n_spikes'], summary_clusters['depth'], color=color)
    plt.gca().invert_yaxis()
    plt.xlabel('spike count')
    plt.ylabel('depth')

    