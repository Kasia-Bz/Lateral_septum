# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 15:46:52 2021

@author: katarzyna
"""

def get_channel_depth(chan,path):
    with HiddenPrints():
        recording = SpikeGLXRecordingExtractor(path)
    channel_ids = np.vstack(recording.get_channel_ids())
    chan_index=np.flatnonzero(channel_ids==chan)
    channel_depth = recording.get_channel_locations()[chan_index,1]

    return channel_depth
