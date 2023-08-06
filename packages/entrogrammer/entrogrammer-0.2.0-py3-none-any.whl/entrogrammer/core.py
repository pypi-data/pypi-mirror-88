"""Core functions to call to calculate the entrogram/entropy values."""

import numpy as np
from . import classifier
from . import tools


def global_entropy(Classifier, base=np.e):
    """Calculate global entropy of some data.

    From an :obj:`entrogrammer.classifier.BaseClassifier`, calculate the
    global entropy of the classified data.

    Parameters
    ----------
    Classifier: :obj:`entrogrammer.classifier.BaseClassifier`
        Any initialized class from `classifier.py` that has had the
        `classify()` method run.

    base: int, float, optional
        Logarithmic base for the entropy calculation. Same as the
        `scipy.stats.entropy()` base parameter meaning it takes a default
        value of `e` (natural logarithm) if not specified.

    Returns
    -------
    HG: float
        The global entropy of the classified data array

    """
    # type check the classifier
    classify_checker(Classifier)

    # type check base
    base_checker(base)

    # calculate the global entropy
    HG = tools.calculate_HG(Classifier.classified, base)

    return HG


def local_entropy(Classifier, scale, base=np.e):
    """Calculate local entropy of some data at a particular scale.

    From an :obj:`entrogrammer.classifier.BaseClassifier`, calculate the
    local entropy of the classified data at a particular scale.

    Parameters
    ----------
    Classifier: :obj:`entrogrammer.classifier.BaseClassifier`
        Any initialized class from `classifier.py` that has had the
        `classify()` method run.

    scale: int, tuple
        Scale or window size over which to compute the local entropy.
        This is provided as a float, or a tuple.
        If the length of the tuple is less than the number of dimensions in
        the data, the last value in the tuple will be applied to the
        dimensions unaccounted for. Conversely, if the length of the tuple is
        greater than the number of dimensions in the data, N, only the first
        N values of the tuple will be used.

    base: int, float, optional
        Logarithmic base for the entropy calculation. Same as the
        `scipy.stats.entropy()` base parameter meaning it takes a default
        value of `e` (natural logarithm) if not specified.

    Returns
    -------
    HL: numpy.ndarray
        The local entropy array of the classified data array for the
        specified scale

    """
    # type check the classifier
    classify_checker(Classifier)

    # type check base
    base_checker(base)

    # type check the scale
    if type(scale) == int:
        win_size = scale
    elif type(scale) == tuple:
        dims = np.shape(Classifier.classified)
        # 1-D case
        if len(dims) == 1:
            if type(scale[0]) == int:
                win_size = scale[0]  # if integer assignment is simple
            else:
                # if not try to assign from tuple
                try:
                    win_size = int(scale[0])
                except Exception:
                    raise TypeError('value in position 0 of scale was not '
                                    ' an `int` / could not be made an `int`.')
        # other dimensions not yet supported
        else:
            raise NotImplementedError('Only 1-D data currently supported.')
    else:
        raise TypeError('scale must be an `int` or `tuple`, '
                        'was: %s', str(type(scale)))

    # calculate local entropy
    HL = tools.calculate_HL(Classifier.classified, win_size, base)

    return HL


def calculate_entrogram(Classifier, min_win=None, max_win=None, base=np.e):
    """Calculate the isotropic entrogram for some classified data.

    Calculates the entrogram (local entropy normalized by global entropy)
    of some classified data. Scales are set using the minimum and maximum
    window parameters.

    Parameters
    ----------
    Classifier: :obj:`entrogrammer.classifier.BaseClassifier`
        Any initialized class from `classifier.py` that has had the
        `classify()` method run.

    min_win: int, optional
        Minimum window size for the local entropy calculation. This is
        isotropic so this is used to set the initial window size in all
        dimensions. If left undefined, a value of 2 will be used as the
        initial window size.

    max_win: int, optional
        Maximum window size for the local entropy calculation. This is
        optional, and if left undefined the minimum dimension of the input
        data will be used as the maximum window size.

    base: int, float, optional
        Logarithmic base for the entropy calculation. Same as the
        `scipy.stats.entropy()` base parameter meaning it takes a default
        value of `e` (natural logarithm) if not specified.

    Returns
    -------
    HR: list
        Entrogram values (relative entropy values)

    win_size: list
        Corresponding window sizes

    """
    # type check the classifier
    classify_checker(Classifier)

    # type check base
    base_checker(base)

    # quick check of window parameters
    if min_win is None:
        min_win = 2
    else:
        try:
            min_win = int(min_win)
        except Exception:
            raise ValueError('min_win parameter was not int or float type.')

    if max_win is None:
        max_win = np.min(Classifier.classified.shape)
    else:
        try:
            max_win = int(max_win)
        except Exception:
            raise ValueError('max_win parameter was not int or float type.')

    # do entrogram calculation
    HR = []
    HG = tools.calculate_HG(Classifier.classified, base)  # global entropy
    for i in range(min_win, max_win+1):
        HL = np.mean(tools.calculate_HL(Classifier.classified, i, base))
        HR.append(HL / HG)

    win_size = list(range(min_win, max_win+1))  # list of window size values

    return HR, win_size


def calculate_entropic_scale(HR, win_size):
    """Calculate the entropic scale given the HR and window size information.

    Finds first index (and corresponding window size) where the relative
    entropy is greater than or equal to 1 (meaning the local entropy has
    matched the global entropy).

    Parameters
    ----------
    HR: list
        Entrogram values (relative entropy values)

    win_size: list
        Corresponding window sizes

    Returns
    -------
    entropic_scale: int
        Window size corresponding to the entropic scale.

    """
    idx = np.where(np.array(HR) >= 1.0)
    entropic_scale = win_size[np.min(idx)]
    return entropic_scale


def base_checker(base):
    """Type-checks the log-base input 'base'."""
    if ((int(base) == 2) or (int(base) == 10) or (base == np.e)) is False:
        raise TypeError('base, if specified, must be valid log base, '
                        'was: %s', str(type(base)))


def classify_checker(Classifier):
    """Type-checks the classifier input."""
    if isinstance(Classifier, classifier.BaseClassifier) is False:
        raise TypeError('Classifier must be a BaseClassifier, '
                        'was: %s', str(type(Classifier)))
    elif Classifier.classified is None:
        raise ValueError('`Classifier.classify()` method must be run first.')
