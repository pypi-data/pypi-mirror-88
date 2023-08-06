"""Plotting odds and ends, included for users' convenience."""

import numpy as np
import matplotlib.pyplot as plt


def plot_entrogram(win_size, HR, labels=True):
    """Make simple plot of entrogram given window sizes and HR."""
    ax1 = plt.gca()  # make plot on current axis if possible
    # plot line and scatter points
    ax1.plot(win_size, HR)
    ax1.scatter(win_size, HR)
    # label axes and titles if labels==True
    if labels is True:
        ax1.set_title('Entrogram')
        ax1.set_xlabel('Length Scale')
        ax1.set_ylabel(r'$H_R$')


def plot_HL(HL, win_size=None, labels=True):
    """Visual map-like plot of the local entropy values."""
    # reshape if HL is just 1-D or pretending to be 2-D
    if len(np.shape(HL)) < 2:
        HL = np.vstack((HL, HL))
    elif (np.shape(HL)[1] == 1) and (len(np.shape(HL)) == 2):
        HL = np.hstack((HL, HL)).T
    # make figure
    ax1 = plt.gca()  # make plot on current axis if possible
    # make plot
    HL_plot = ax1.imshow(HL, cmap='plasma')
    cbar = plt.colorbar(HL_plot)
    # label axes and titles if labels==True
    if labels is True:
        if win_size is not None:
            ax1.set_title('Local Entropy Map, Window Size: ' + str(win_size))
        else:
            ax1.set_title('Local Entropy Map')
        cbar.set_label('Local Entropy')
