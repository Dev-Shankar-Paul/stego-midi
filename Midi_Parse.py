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

def special_pad(byte):
    byte[0] = 128
    byte[2] = 128
    
    return byte

def pad(byte, bit_1, bit_2):
    
    if(bit_1 == 0 and bit_2 == 1):
        byte[2] = 128
        
    elif(bit_1 == 1 and bit_2 == 0):
        byte[1] = 128
        byte[2] = 128

    elif(bit_1 == 1 and bit_2 == 1):
        byte[0] = 128
        byte[1] = 128
        byte[2] = 128
    
    return byte

init_mid = mido.MidiFile('Country_Roads.mid')

# Get the binary form of the secret file
with open('Secret_file.txt', 'rb') as secret:
    f = secret.read()
    b = bytes(f)
    
binary_secret = bin(int.from_bytes(b, byteorder = sys.byteorder))
binary_secret = binary_secret[2: ]

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
   
# Special padding to indicate start and stop
new_bytes[0] = special_pad(new_bytes[0])
new_bytes[len(binary_secret) + 2] = special_pad(new_bytes[len(binary_secret) +2])

# Do the padding
c = 0
for i in range(1, len(binary_secret), 2):
    try:
        new_bytes[i] = pad(new_bytes[i], binary_secret[c], binary_secret[c+1])
    except:
        new_bytes[i] = pad(new_bytes[c], binary_secret[i], 0)
    c+=1
    
for i in range(0, len(new_bytes)):
    new_bytes[i] = bytes(new_bytes[i])
    new_bytes[i] = bytes_to_int(new_bytes[i])
    
i = 0    
for msg in mido.merge_tracks(init_mid.tracks):
    msg.time = new_bytes[i]
    i+=1
    
init_mid.save('same.mid')
          

    
    