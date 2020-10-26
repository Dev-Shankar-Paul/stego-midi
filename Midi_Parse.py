# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 20:49:25 2020

@author: bambo
"""
import mido
import sys

def bytes_to_int(byte):
    result = 0
    
    for b in byte:
        result = result * 256 + int(b)
        
    return result

init_mid = mido.MidiFile('Country_Roads.mid')

# Iterating over the tracks
delta_times_playback = []
for msg in mido.merge_tracks(init_mid.tracks):
    delta_times_playback.append(msg.time)
    
new_bytes = []

# print all the delta times with their respective 4 byte arrays
for i in delta_times_playback:
    byte = i.to_bytes(4, 'big')
    byte = bytearray(byte)
    new_bytes.append(byte)
   
for i in range(0, len(new_bytes)):
    new_bytes[i] = bytes(new_bytes[i])
    new_bytes[i] = bytes_to_int(new_bytes[i])
    
i = 0    
for msg in mido.merge_tracks(init_mid.tracks):
    msg.time = new_bytes[i]
    i+=1
    
init_mid.save('same.mid')
          

    
    