""" Small helper functions for the simulator. """

import numpy as np
import pandas as pd

check_val = lambda x, p: (x in p) & (p[x] is not None)

def select_range(values, range_values, mode):
    if isinstance(values, pd.DataFrame):
        values = values.values
    if isinstance(range_values, pd.DataFrame):
        range_values = range_values.values

    if mode == '(]':
        comp = np.less
    elif mode == '[)':
        comp = np.less_equal

    idx = np.reshape(
        [np.nonzero(comp(list(zip(*range_values))[0], v))[0][-1]
         for v in values.reshape(-1)], values.shape)

    return idx