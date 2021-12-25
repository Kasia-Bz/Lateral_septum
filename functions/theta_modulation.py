# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 15:53:39 2021

@author: katarzyna
"""
import numpy as np
from scipy.integrate import simps

import pandas as pd
import scipy
import scipy.signal
import fklab.signals.filter
import fklab.signals.multitaper as mt
import fklab.signals.smooth as smooth

def shuffle_spike_train (spike_t, bandwidth=0.0625):
    shuffled_spikes = spike_t + np.random.normal(scale=bandwidth, size=spike_t.shape)
    shuffled_spikes = np.sort(shuffled_spikes)
    
    return (shuffled_spikes)

def theta_modulation (spike_t, segments, bin_size=0.001, window_size =2, bandwidth =1, theta_band=[6,10], freq_band=[1,50], **kwargs):
    #determine start and end times
    start, end = spike_t[0] - 0.5 * bin_size, spike_t[-1] + 0.5 * bin_size
    #bin spike times
    bins = fklab.segments.check_segments(np.arange(start, end, bin_size))
    spikes_binned = fklab.events.basic_algorithms.fastbin(spike_t, bins)

    #compute spectrum
    psd, f, _, _ = mt.mtspectrum(
        spikes_binned.ravel(),
        fs=1.0 / bin_size,
        window_size=window_size,
        bandwidth=bandwidth,
        start_time=spike_t[0],
        fpass=freq_band,
        epochs=segments,
    )

    #compute power in frequency bands
    # Find intersecting values in frequency vector
    idx_theta = np.logical_and(f >= theta_band[0], f <= theta_band[1])
    idx_total = np.logical_and(f >= freq_band[0], f <= freq_band[1])
    
    #find the frequency resolution
    freq_res = f[1] - f[0] 
    
    #compute theta relative power 
        # Compute the absolute power for theta band
    theta_power = simps(psd[idx_theta], dx=freq_res)
        # Compute the absolute power in specified power bands
    total_power = simps(psd[idx_total], dx=freq_res)
        # Compute relative power 
    theta_rel_power = theta_power / total_power
    
    return(psd, f, theta_power, total_power, theta_rel_power)