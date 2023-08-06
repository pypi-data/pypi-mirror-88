
import numpy as np


def reptemp(temp_min=300, temp_max=440, n_replicas=40, mode='geometric'):
    """
    Geometric = the ratio from one temperature to the next is kept constant

    .. math :: T_i = T_1 \frac{T_R}{T_1}^{\frac{i-1}{R-1}}

    .. math :: log T_i - log T_1 = \frac{i-1}{R-1}(log


    Parameters
    ----------
    temp_min : float
    temp_max : float
    n_replicas : int
    mode : str

    Returns
    -------

    """

    if mode != 'geometric':
        raise AttributeError('only supports geometric')

    return temp_min * np.power(temp_max / temp_min, np.arange(n_replicas) / (n_replicas - 1.), dtype=np.float64)


if __name__ == '__main__':
    print(reptemp(300, 440, 40))
