# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 17:29:22 2021

@author: katar
"""

from fklab.behavior.task_analysis import detect_trajectories

def create_segments(position_time, xy, HR, CP, LR, RR, w_CP):
    outbound_right = detect_trajectories(position_time, xy, include_regions=[HR,CP,RR], exclude_regions=[LR], ordered=True, revisit=False)
    outbound_left = detect_trajectories(position_time, xy, include_regions= [HR, CP,LR], exclude_regions=[RR], ordered=True, revisit=True)
    inbound_right = detect_trajectories(position_time, xy, include_regions= [RR, CP,HR], ordered=True, revisit=True)
    inbound_left = detect_trajectories(position_time, xy, include_regions= [LR, CP,HR], ordered=True, revisit=True)
    choice = detect_trajectories(position_time, xy, include_regions= [HR,CP], ordered=True, revisit=True)
    outbound=outbound_right.union(outbound_left)
    inbound=inbound_right.union(inbound_left)
    out_in = outbound.union(inbound)
    right=detect_trajectories(position_time, xy, include_regions=[CP,RR], exclude_regions=[LR], ordered=True, revisit=False)
    left=detect_trajectories(position_time, xy, include_regions=[CP,LR], exclude_regions=[LR], ordered=True, revisit=False)
    right_in=detect_trajectories(position_time, xy, include_regions=[RR,CP], exclude_regions=[LR], ordered=True, revisit=False)
    left_in=detect_trajectories(position_time, xy, include_regions=[LR,CP], exclude_regions=[RR], ordered=True, revisit=False)
    
    return(outbound, inbound, out_in)