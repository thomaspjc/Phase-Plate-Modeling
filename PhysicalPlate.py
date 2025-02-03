#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 16:44:28 2024

Setting up the limitations in our simulation of the phase plate 

@author: thomas
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import h5py
from cmocean import cm


def Box(inputPhase, group):
    """
    Performs grouped averaging on a phase mask to reduce its transverse resolution 
    (referred to as 'boxing').

    Parameters
    ----------
    inputPhase : np.array 
        2D array representing the phase mask that will be processed.
    group : int
        The size of the square pixel groups to average over. Both dimensions of the 
        phase mask must be divisible by this number.

    Raises
    ------
    IndexError
        The array should be a multiple of the group
        Generally should be a 2^n before or after shrinking

    Returns
    -------
    boxedPhase : np.array
        The phase mask with reduced resolution, where each group of pixels 
        has been averaged to represent a single phase value.

    """
    initialPhase = inputPhase
    
    # Adapting for a 2^n + 1 array shape
    if not ((initialPhase.shape[0]-1)%2):
        inputPhase = ShrinkOn(inputPhase)

    # Get the shape of the input array
    rows, cols = inputPhase.shape
    
    # --- Ensure the operation of grouping is possible ---
    if rows % group != 0 or cols % group != 0:
        raise IndexError("The input array is not able to be separated using the group Size")
    
    
    # Reshape the array to group the elements
    reshaped = inputPhase.reshape(rows // group, group, cols // group, group)

    # Sum within the groups
    group_sums = reshaped.sum(axis=(1, 3))
    
    # Expand the group sums back to the original shape
    expanded_sums = np.repeat(np.repeat(group_sums, group, axis=0), group, axis=1)
    
    # Divide by the group^2 to perform the average over the group
    boxedPhase = expanded_sums/group**2
    
    # Reshaping to 2^n+1 if necessary
    if not ((initialPhase.shape[0]-1)%2):
        boxedPhase = ShrinkOff(boxedPhase)

    return boxedPhase 



def ShrinkOn (inputPhase):
    """
    Removes the last column and row from the input phase to obtain a 2^n array
    
    Parameters
    ----------
    inputPhase : 2^n+1 array
        intial phase mask with a 2^n+1 size that needs to be reduced for grouping

    Returns
    -------
    2^n array 

    """
    return inputPhase[:-1,:-1]



def ShrinkOff (boxedPhase):
    """
    Extends the last row and column of the 2^n array to retrieve a 2^n+1 array
    The values that are extended outside of the lens are removed by the realLens function
    Parameters
    ----------
    boxedPhase : 2^n array 
        Grouped phase that needs to be extended back to 2^n+1 size


    Returns
    -------
    2^n+1 array

    """
    #Extend the last row of the array
    extended_row = np.vstack([boxedPhase, boxedPhase[-1, :]])

    #Extend the last column of the array
    extended_row = np.hstack([extended_row, extended_row[:, [-1]]])
    
    return extended_row
    

if __name__ == "__main__": 
    
    #--- Initial Test to see how the boxing works --- 
    
    # Extracting the classic Lenna Target for the test
    from Targets import Lenna
    testArray = np.ones([2**11, 2**11])
    testImage = Lenna(testArray, plot = False)
    testImage = np.array(testImage)

    # --- Applying Boxing ---
    result = Box(testImage, 16)
    
    # --- Plotting Outputs ---
    fig, axs = plt.subplots(1, 2, figsize=(12, 10))
    
    # Importing the Stanford Colormap
    from PlottingTools import StanfordColormap
    stanford_colormap = StanfordColormap()
    
    # Plotting initial Image
    testImagePlot = axs[0].imshow(testImage, cmap = stanford_colormap)
    fig.colorbar(testImagePlot, ax = axs[0], orientation = 'horizontal')
    
    # Plotting grouped averaged image
    resultPlot = axs[1].imshow(result, cmap = stanford_colormap)
    fig.colorbar(resultPlot, ax = axs[1], orientation = 'horizontal')


    
    






































