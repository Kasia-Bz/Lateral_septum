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

def save_summary_table(main_path, rat_ID, task, session, summary_clusters):
    # main_path = '/mnt/fk-fileserver/Project_LS'  - remember to add / before mnt
    import os.path
    import pandas as pd
    save_path = str(main_path) + '/' + str(rat_ID) + '/' + str(task) + '/' + str(session) + '/'
    summary_clusters.to_hdf(save_path + 'summary_clusters.h5', key='summary_clusters', mode='w')
    

def read_summary_table(main_path, rat_ID, task, session):
    import os.path 
    import pandas as pd 
    save_path = str(main_path) + '/' + str(rat_ID) + '/' + str(task) + '/' + str(session) + '/'
    summary_table = pd.read_hdf(save_path + 'summary_clusters.h5', key='summary_clusters')
    
    return(summary_table)
    
def plot_spikes_depth(summary_clusters, color):
    import matplotlib.pyplot as plt
    plt.rcParams["figure.figsize"] = (8,10)
    plt.scatter(summary_clusters['n_spikes'], summary_clusters['depth'], color=color)
    plt.gca().invert_yaxis()
    plt.xlabel('spike count')
    plt.ylabel('depth')


def spikes_LS(rat_ID, summary_clusters):
    if rat_ID == 'LS_k_7':
        lateral_septum = summary_clusters[summary_clusters['depth'] <= 2500] 
        LSD = lateral_septum[(lateral_septum['depth'] <= max(lateral_septum['depth']) )
                             & (lateral_septum['depth'] >= max(lateral_septum['depth'] - 300))]
        LSI = lateral_septum[(lateral_septum['depth'] < min(LSD['depth'])) 
                             & (lateral_septum['depth'] >= min(LSD['depth']) - 1400)] 
        LSV = lateral_septum[(lateral_septum['depth'] < min(LSI['depth'])) 
                             & (lateral_septum['depth'] >= min(LSI['depth']) - 600)] 
        return(lateral_septum, LSD, LSI, LSV)
        
    if rat_ID == 'LS_k_8': 
        lateral_septum = summary_clusters[summary_clusters['depth'] <= 2500] 
        LSD = lateral_septum[(lateral_septum['depth'] <= max(lateral_septum['depth']) )
                             & (lateral_septum['depth'] >= max(lateral_septum['depth'] - 300))]
        LSI = lateral_septum[(lateral_septum['depth'] < min(LSD['depth'])) 
                             & (lateral_septum['depth'] >= min(LSD['depth']) - 1800)] 
        SHy = lateral_septum[(lateral_septum['depth'] < min(LSI['depth']))] 
        
        return(lateral_septum, LSD, LSI, SHy)
    
    if rat_ID == 'LS_k_9': 
        lateral_septum = summary_clusters[summary_clusters['depth'] <= 2300] 
        SHi = lateral_septum[(lateral_septum['depth'] <= max(lateral_septum['depth']) )
                             & (lateral_septum['depth'] >= max(lateral_septum['depth'] - 200))]
        LSI = lateral_septum[(lateral_septum['depth'] < min(SHi['depth'])) 
                             & (lateral_septum['depth'] >= min(SHi['depth']) - 400)] 
        SFi = lateral_septum[(lateral_septum['depth'] < min(LSI['depth'])) 
                             & (lateral_septum['depth'] >= min(LSI['depth']) - 600)]  
        MS = lateral_septum[(lateral_septum['depth'] < min(SFi['depth']))]
        
        return(lateral_septum, SHi, LSI, SFi, MS)
    
    if rat_ID == 'LS_k_13':
        lateral_septum = summary_clusters[summary_clusters['depth'] <= 3000] 
        SHi = lateral_septum[(lateral_septum['depth'] <= max(lateral_septum['depth']) )
                             & (lateral_septum['depth'] >= max(lateral_septum['depth'] - 700))]
          
        MS = lateral_septum[(lateral_septum['depth'] < min(SFi['depth']))]
        
        return(lateral_septum, SHi, MS)    
    
    if rat_ID == 'LS_k_14':
        lateral_septum = summary_clusters[summary_clusters['depth'] <= 3000] 
        LSD = lateral_septum[(lateral_septum['depth'] <= max(lateral_septum['depth']) )
                             & (lateral_septum['depth'] >= max(lateral_septum['depth'] - 300))]
        LSI = lateral_septum[(lateral_septum['depth'] < min(LSD['depth'])) 
                             & (lateral_septum['depth'] >= min(LSD['depth']) - 1200)] 
        Ld = lateral_septum[(lateral_septum['depth'] < min(LSI['depth'])) 
                             & (lateral_septum['depth'] >= min(LSI['depth']) - 300)] 
        SHy = lateral_septum[(lateral_septum['depth'] < min(Ld['depth']))] 
        
        return(lateral_septum, LSD, LSI, Ld, SHy)
    
        
        
        
        
        