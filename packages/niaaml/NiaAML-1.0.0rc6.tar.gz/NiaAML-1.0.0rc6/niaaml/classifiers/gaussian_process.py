from niaaml.classifiers.classifier import Classifier
from niaaml.utilities import MinMax
from niaaml.utilities import ParameterDefinition
from sklearn.gaussian_process import GaussianProcessClassifier as GPC
import numpy as np

__all__ = ['GaussianProcess']

class GaussianProcess(Classifier):
    r"""Implementation of gaussian process classifier.
    
    Date:
        2020

    Author:
        Luka Pečnik

    License:
        MIT

    See Also:
        * :class:`niaaml.classifiers.Classifier`
    """
    Name = 'Gaussian Process Classifier'

    def __init__(self, **kwargs):
        r"""Initialize GaussianProcess instance.
        """
        self._params = dict(
            max_iter_predict = ParameterDefinition(MinMax(50, 200), np.uint),
            warm_start = ParameterDefinition([True, False]),
            multi_class = ParameterDefinition(['one_vs_rest', 'one_vs_one'])
        )
        self.__gaussian_process = GPC()

    def set_parameters(self, **kwargs):
        r"""Set the parameters/arguments of the algorithm.
        """
        self.__gaussian_process.set_params(**kwargs)

    def fit(self, x, y, **kwargs):
        r"""Fit GaussianProcess.

        Arguments:
            x (pandas.core.frame.DataFrame): n samples to classify.
            y (pandas.core.series.Series): n classes of the samples in the x array.

        Returns:
            None
        """
        self.__gaussian_process.fit(x, y)

    def predict(self, x, **kwargs):
        r"""Predict class for each sample (row) in x.

        Arguments:
            x (pandas.core.frame.DataFrame): n samples to classify.

        Returns:
            pandas.core.series.Series: n predicted classes.
        """
        return self.__gaussian_process.predict(x)

    def to_string(self):
        r"""User friendly representation of the object.

        Returns:
            str: User friendly representation of the object.
        """
        return Classifier.to_string(self).format(name=self.Name, args=self._parameters_to_string(self.__gaussian_process.get_params()))