#!/usr/bin/env python3


'''Analyze UVIT L1 data.


   Copyright 2020 Prajwel Joseph
  
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
  
       http://www.apache.org/licenses/LICENSE-2.0
  
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License. 

'''


import sys
import numpy as np
from astropy.io import fits


# A dictionary of window sizes and frame rates.
window_rate_dict = {'511': 28.7185,
                    '349': 61.0,
                    '299': 82.0,
                    '249': 115.0,
                    '199': 180.0,
                    '149': 300.0,
                    '99' : 640.0}

# Function to estimate percentage of missing frames from L1.
def whats_missing(data):
    data = np.unique(data)
    data = np.array(data, dtype = np.int32)
    missing_frames = np.diff(data)[np.diff(data) > 1] - 1
    total_missing = np.sum(missing_frames)
    missing_percentage = total_missing * 100.0 / data[-1]
    return missing_percentage

# To detect any sawtooth in data. 
def find_breaks(data):
    if len(data) == 0:
        print('No data')
    data1 = np.roll(data,1)
    data1[0] = 0
    mask = data < data1
    indices = [i for i, m in enumerate(mask) if m ==True]
    return np.array(indices)


def raw_events(L1_FITS):
    hdulist = fits.open(L1_FITS)

    # To get the frame rate.
    window = str(hdulist[0].header['win_x_sz'])
    frame_rate = window_rate_dict[str(window)]

    # Apparently, some 25 seconds of initial data could be BOD check.
    BOD_frame_length = frame_rate * 25

    # This is to fix sawtooths due to arrays being stored in 16-bit.
    times = hdulist[2].data['SecHdrImageFrameTime']
    frames = hdulist[2].data['SecHdrImageFrameCount']
    breaks = find_breaks(frames)
    nonBOD_breaks = breaks[breaks > BOD_frame_length]
    if len(nonBOD_breaks) != 0:
        if np.mean(frames[nonBOD_breaks - 1]) == 65535.0:            
            for index in nonBOD_breaks:
                part1 = frames[:index]
                part2 = frames[index:] + 65536
                frames = np.append(part1,part2)
        else:
            print('\nWe have got a big problem, people!\
                  \nAn unprecedented sawtooth detected in the data\n')

    # To create a universal mask which will be used throughout. 
    pardah = (np.diff(frames) > -1) 
    pardah = np.append(pardah, np.array(pardah[-1])) # to make size equal to that of frames.

    BOD_breaks = breaks[breaks < BOD_frame_length] #To mask BOD data
    if len(BOD_breaks) != 0:
        BOD_mask = np.array([False] * BOD_breaks[-1])
        pardah[: BOD_breaks[-1]] = BOD_mask

    # To print out the percentage of missing data.
    #veil = (np.diff(frames) != 0)
    #veil = np.append(veil, np.array(veil[-1])) # to make size equal to that of frames.
    missing_info = whats_missing(frames[pardah])
    print('\nA small percentage of L1 data frames gets lost. \
           \nThe following percentage tells you exactly how much. \
           \nMissing data = {:.1f} %\n'.format(missing_info))

    pardah = pardah * (frames != 1) # to remove all with framenumber = 1

    # The bloody thing was read as 8-bit integers (2016 columns).
    droid_array = hdulist[2].data['Centroid']

    # Let us enforce the pardah on data.
    times = times[pardah]
    frames = frames[pardah]
    droid_array = droid_array[pardah]

    # Unpacks elements of a 8-bit int array into a binary-valued output array.
    # Now with 16128 columns.
    bit_data = np.unpackbits(droid_array, axis =1)  

    # Reshaping the array with only 3 words (48 bits) in the row.
    no_of_frames = len(frames)
    len_row = no_of_frames * 336
    bit_dat = bit_data.reshape(len_row, 48)

    # Since centroid array is reshaped, frames and times arrays need to be changed too.
    lots_of_ones = np.ones([no_of_frames, 336])

    sheared_frames = lots_of_ones * frames[:, np.newaxis]
    sheared_frames = sheared_frames.reshape(len_row, 1)
    sheared_frames = sheared_frames.astype(int)

    sheared_times = lots_of_ones * times[:, np.newaxis]
    sheared_times = sheared_times.reshape(len_row, 1)
    sheared_times = sheared_times.astype(int)

    # bit data gets converted to useful events data. Hold my beer! 
    Rx = bit_dat[:, 0] * 256
    Lx = np.packbits(bit_dat[:, 1:9])
    Ix = Rx + Lx

    Ry = bit_dat[:, 16] * 256
    Ly = np.packbits(bit_dat[:, 17:25])
    Iy = Ry + Ly

    powers = np.array([32, 16,  8,  4,  2,  1], dtype=np.int8)

    Fx = bit_dat[:, 9:15]
    Fx = Fx.dot(powers)

    Fy = bit_dat[:, 25:31]
    Fy = Fy.dot(powers)

    X_parity = bit_dat[:, 15]
    Y_parity = bit_dat[:, 31]

    # To convert the 6-bit integers to subpixels.
    substep = 0.03125

    Fx[Fx > 31] = Fx[Fx > 31] - 64
    Fx = Fx * substep

    Fy[Fy > 31] = Fy[Fy > 31] - 64
    Fy = Fy * substep

    # Adding the integer and float parts together.
    X_pos = Ix + Fx
    Y_pos = Iy + Fy

    # Keeping some standards.
    X_p = X_pos[X_pos > 0.]
    Y_p = Y_pos[X_pos > 0.]
    sheared_times = sheared_times[X_pos > 0.]
    sheared_frames = sheared_frames[X_pos > 0.]
    X_parity = X_parity[X_pos > 0.]
    Y_parity = Y_parity[X_pos > 0.]

    # Converting it into 4k.
    X_p = X_p * 8
    Y_p = Y_p * 8

    X_parity_check = bit_dat[:, :16]
    X_parity_check = np.sum(X_parity_check, axis = 1)
    failed_X_parity = np.sum(np.mod(X_parity_check, 2))

    Y_parity_check = bit_dat[:, 16:32]
    Y_parity_check = np.sum(Y_parity_check, axis = 1)
    failed_Y_parity = np.sum(np.mod(Y_parity_check, 2))

    print('No. of parity failed events in X = {}, Y = {}'.format(failed_X_parity, failed_Y_parity))

    col1 = fits.Column(name = 'Time', format = 'D', array = sheared_times)
    col2 = fits.Column(name = 'FrameCount', format = 'D', array = sheared_frames)
    col3 = fits.Column(name = 'Fx', format = 'D', array = X_p)
    col4 = fits.Column(name = 'Fy', format = 'D', array = Y_p)
    cols = fits.ColDefs([col1, col2, col3, col4])
    tbhdu = fits.BinTableHDU.from_columns(cols)
    table_name = 'raw_events_' + L1_FITS
    tbhdu.writeto(table_name, overwrite = True)



















      
