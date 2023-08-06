"""Helper functions for misc. calculations."""

import numpy as np
from scipy.stats import entropy
from numba import njit


def calculate_HG(data, base):
    """Calculate global entropy.

    Internal function to calculate global entropy. Assumes data has been
    type-checked in the function :obj:`entrogrammer.core.global_entropy()`.

    Parameters
    ----------
    data: numpy.ndarray
        An ndarray with the classified data.

    base: int, float
        Logarithmic base for the entropy calculation.

    Returns
    -------
    HG: float
        The global entropy of the data array

    """
    # get probabilities
    n_vals = len(data.flat)  # total number of values
    # get number of each unique (classified) value in the array
    _, unique_counts = np.unique(data, return_counts=True)
    probs = unique_counts / n_vals  # get probabilities
    HG = entropy(probs, base=base)  # get global entropy, this is returned
    return HG


def calculate_HL(data, win_size, base):
    """Calculate local entropy of some data at a particular scale.

    Internal function to calculate averaged local entropy. Assumes data has
    been type-checked in :obj:`entrogrammer.core.local_entropy()`.

    Parameters
    ----------
    data: numpy.ndarray
        An ndarray with the classified data.

    scale: int, tuple
        Scale or window size over which to compute the local entropy.
        This is provided as a float, or a tuple.
        If the length of the tuple is less than the number of dimensions in
        the data, the last value in the tuple will be applied to the
        dimensions unaccounted for. Conversely, if the length of the tuple is
        greater than the number of dimensions in the data, N, only the first
        N values of the tuple will be used.

    base: int, float
        Logarithmic base for the entropy calculation.

    Returns
    -------
    HL: numpy.ndarray
        The local entropy vector of the classified data array for the
        specified scale (same shape as `data` input parameter)

    """
    # init arrays for entropy and counts (because numba is bad for this)
    h = np.zeros_like(data).astype('float')
    cnt = np.zeros_like(data)

    # 1-D solution
    if ((len(np.shape(data)) == 1) and (base == 2)):
        return HL_1D_base2(data, win_size, h, cnt)
    elif ((len(np.shape(data)) == 1) and (base == 10)):
        return HL_1D_base10(data, win_size, h, cnt)
    elif ((len(np.shape(data)) == 1) and (base == np.e)):
        return HL_1D_basee(data, win_size, h, cnt)
    else:
        pass

    # 2-D solution
    if ((len(np.shape(data)) == 2) and (base == 2)):
        raise NotImplementedError('2-D not implemented yet.')
    elif ((len(np.shape(data)) == 2) and (base == 10)):
        raise NotImplementedError('2-D not implemented yet.')
    elif ((len(np.shape(data)) == 2) and (base == np.e)):
        raise NotImplementedError('2-D not implemented yet.')
    else:
        pass

    # 3-D solution
    if ((len(np.shape(data)) == 3) and (base == 2)):
        raise NotImplementedError('3-D not implemented yet.')
    elif ((len(np.shape(data)) == 3) and (base == 10)):
        raise NotImplementedError('3-D not implemented yet.')
    elif ((len(np.shape(data)) == 3) and (base == np.e)):
        raise NotImplementedError('3-D not implemented yet.')
    else:
        raise TypeError('Dimensions beyond 3 are not supported.')


@njit
def HL_1D_base2(data, win_size, h, cnt):
    """Do the 1-D local entropy calculation with base 2."""
    num_slides = len(data) - win_size + 1
    for i in range(num_slides):
        cnt[i:(i+win_size)] += 1  # count the cells visited by this window
        unique_counts = np_unique_impl(data[i:(i+win_size)])
        probs = []
        for k in unique_counts:
            probs.append(k / win_size)
        # do entropy calculation
        for j in range(len(probs)):
            h[i:(i+win_size)] += -1 * probs[j] * np.log2(probs[j])
    h = h / cnt  # make average by dividing by number of visits
    return h


@njit
def HL_1D_base10(data, win_size, h, cnt):
    """Do the 1-D local entropy calculation with base 10."""
    num_slides = len(data) - win_size + 1
    for i in range(num_slides):
        cnt[i:(i+win_size)] += 1  # count the cells visited by this window
        unique_counts = np_unique_impl(data[i:(i+win_size)])
        probs = []
        for k in unique_counts:
            probs.append(k / win_size)
        # do entropy calculation
        for j in range(len(probs)):
            h[i:(i+win_size)] += -1 * probs[j] * np.log10(probs[j])
    h = h / cnt  # make average by dividing by number of visits
    return h


@njit
def HL_1D_basee(data, win_size, h, cnt):
    """Do the 1-D local entropy calculation with base e."""
    num_slides = len(data) - win_size + 1
    for i in range(num_slides):
        cnt[i:(i+win_size)] += 1  # count the cells visited by this window
        unique_counts = np_unique_impl(data[i:(i+win_size)])
        probs = []
        for k in unique_counts:
            probs.append(k / win_size)
        # do entropy calculation
        for j in range(len(probs)):
            h[i:(i+win_size)] += -1 * probs[j] * np.log(probs[j])
    h = h / cnt  # make average by dividing by number of visits
    return h


@njit
def np_unique_impl(a):
    """Get unique counts, from: https://github.com/numba/numba/issues/2884."""
    b = np.sort(a.flatten())
    unique = list(b[:1])
    counts = [1 for _ in unique]
    for x in b[1:]:
        if x != unique[-1]:
            unique.append(x)
            counts.append(1)
        else:
            counts[-1] += 1
    return counts
