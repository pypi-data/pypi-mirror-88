"""Classes and methods for binning and classifying data."""

import abc
import xarray as xr
import numpy as np


class BaseClassifier(abc.ABC):
    """Base classifier class.

    Abstract class that exists as a blueprint for classifier classes.
    This class defines the expected methods for each classifier class that is
    implemented.
    """

    def __init__(self, data):
        """Read data.

        This method should handle pre-processing of data for all classifiers.
        Sub-classed classifiers should be able to pre-process and standardize
        data using methods defined here via `super().__init__(data)`

        """
        self.data = data
        self.classified = None  # init classified array as Nonetype

    @property
    def data(self):
        """Return private data array."""
        return self._data

    @data.setter
    def data(self, data):
        """Type-check the input data array and create private variable."""
        # standardize data to a numpy.ndarray or raise an error
        if type(data) is xr.core.dataarray.DataArray:
            self._data = data.data  # convert to ndarray
        elif type(data) is np.ndarray:
            self._data = data
        else:
            raise TypeError('Invalid type for "data", expected a '
                            'numpy.ndarray but got: %s', type(data))

    @property
    def classified(self):
        """Return private classified array."""
        return self._classified

    @classified.setter
    def classified(self, classified):
        """Create private variable."""
        self._classified = classified

    @abc.abstractmethod
    def classify(self):
        """Classify the data.

        All classifier classes should have this method.
        The object of this method is to perform the classification of the
        data into different bins or categories.

        """


class BinaryClassifier(BaseClassifier):
    """Simple binary classifier.

    This class classifies data into a binary scheme. Pretty simple.

    """

    def __init__(self, data, threshold):
        """Initialize the BinaryClassifier.

        Parameters
        ----------
        data : numpy.ndarray
            Input data array.

        thereshold : int, float
            Value below which data will be put into the "0" class.
            Data values at and above this threshold will go into the "1" class.

        """
        super().__init__(data)
        self.threshold = threshold
        self.classify()

    @property
    def threshold(self):
        """Return private threshold variable."""
        return self._threshold

    @threshold.setter
    def threshold(self, threshold):
        """Type-check the threshold value and set it as a private variable."""
        if type(threshold) is int:
            self._threshold = threshold
        elif type(threshold) is float:
            self._threshold = threshold
        else:
            raise TypeError('Invalid type for "threshold", expected an '
                            'int or float but got: %s' + type(threshold))

    def classify(self, threshold=None):
        """Do the binary classification."""
        # initialize the classified array
        self.classified = np.zeros_like(self._data)
        # can overwrite threshold with a new one if supplied
        if threshold is not None:
            self.threshold = threshold
        # need if tree to avoid making all values 0 or 1 depending on threshold
        if self._threshold > 0:
            self._classified[self._data < self._threshold] = 0
            self._classified[self._data >= self._threshold] = 1
        else:
            self._classified[self._data >= self._threshold] = 1
            self._classified[self._data < self._threshold] = 0


class JenksClassifier(BaseClassifier):
    """Classifier that uses the Fisher-Jenks algorithm.

    This class is used to apply the Fisher-Jenks algorithm to compute natural
    breaks given some data. This classification scheme attempts to define a
    set of classes given some data values so that the variance within classes
    is minimal, and the variance between different classes is maximal. To do
    this in `entrogrammer`, the `jenkspy` python package
    (https://github.com/mthh/jenkspy) is used.

    """
    def __init__(self, data, nb_class):
        """Initialize the JenksClassifier.

        Parameters
        ----------
        data : numpy.ndarray
            Input data array.

        nb_class : int, float
            Desired number of classes to split the data into. If input as a
            float, this will be turned into an integer. Must be lower than the
            number of data points, and greater than 2.

        """
        super().__init__(data)
        self.nb_class = nb_class
        self.classify()

    @property
    def nb_class(self):
        """Return private nb_class variable."""
        return self._nb_class

    @nb_class.setter
    def nb_class(self, nb_class):
        """Check the nb_class value and set it as a private variable."""
        # type checking
        if type(nb_class) is int:
            self._nb_class = nb_class
        elif type(nb_class) is float:
            self._nb_class = int(nb_class)
        else:
            raise TypeError('Invalid type for "nb_class", expected an '
                            'int or float but got: %s' + type(nb_class))
        # value checking
        data_len = len(self._data.ravel())
        if nb_class >= data_len:
            raise ValueError('"nb_class" must be lower than the number of '
                             'data points.')
        if nb_class < 2:
            raise ValueError('"nb_class" must be greater than 2.')

    def classify(self, nb_class=None):
        """Do the jenks classification."""
        # try to import jenkspy package
        try:
            from jenkspy import JenksNaturalBreaks
        except Exception:
            raise ImportError('`jenkspy` optional dependency not installed.')
        # set nb_class
        if nb_class is None:
            nb_class = self._nb_class
        # type-check nb_class
        if type(nb_class) is not int:
            raise ValueError('"nb_class" must be an integer')
        # ravel the data array in-case it is multidimensional
        data = np.ravel(self._data)
        # initialize the jenks object
        jnb = JenksNaturalBreaks(nb_class)
        # do classification
        jnb.fit(data)
        # populate self._classified with the classified labels
        self._classified = np.reshape(jnb.labels_, self._data.shape)


class HistogramClassifier(BaseClassifier):
    """Exposes histogram binning classifiation functionality.

    This class is used to classify data into a specified number of bins.
    Uses np.histogram and np.digitize to do this.

    """

    def __init__(self, data, bins=10, range=None):
        """Initialize the HistogramClassifier.

        Parameters
        ----------
        data : numpy.ndarray
            Input data array.

        bins : int, optional
            Defines the number of bins, is 10 by default.

        range : (float, float), optional
            Lower and upper range of bins if specified.

        """
        super().__init__(data)
        self.bins = bins
        self.range = range
        self.classify()

    @property
    def bins(self):
        """Return private bins variable."""
        return self._bins

    @bins.setter
    def bins(self, bins):
        """Set the bins value."""
        if isinstance(bins, int) is True:
            self._bins = bins
        else:
            if isinstance(bins, float) is True:
                self._bins = int(bins)
            else:
                raise TypeError('Type of bins provided was not recognized '
                                'it must be an integer if specified.')

    @property
    def range(self):
        """Return private range variable."""
        return self._range

    @range.setter
    def range(self, range):
        """Set the range value."""
        if (isinstance(range, tuple) is True) or (range is None):
            self._range = range
        else:
            raise TypeError('Type of range provided was not recognized, '
                            'must be a tuple if specified.')

    def classify(self, bins=None, range=None):
        """Do histogram-based classification."""
        # set up bins and range
        if bins is None:
            bins = self._bins
        if range is None:
            range = self._range
        # if range still none, set by data values
        if range is None:
            range = (np.min(self._data), np.max(self._data))
        # use np.histogram and np.digitize to do classification
        _, bin_edges = np.histogram(self._data, bins, range)
        self.classified = np.digitize(self._data, bin_edges)
