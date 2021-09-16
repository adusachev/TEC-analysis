import numpy as np
import pandas as pd



def satellite_calculations(n_s: int, other_params: list):
    """
    Вычисляет delta TEC для конкретного спутника
    """

    t_start, t_end, t_an_start, t_an_end, m, TECU_normal = other_params

    p = np.where(m.values[:, 1] == n_s)[0]
    time = m.values[p, 0]

    tecu_normal = TECU_normal[p]

    # детрендирование
    indexes = np.where(((time <= t_an_start) & (time >= t_start)) | ((time <= t_end) & (time >= t_an_end)))[0]
    y2 = tecu_normal[indexes]
    t2 = time[indexes]

    from scipy.interpolate import interp1d
    f = interp1d(t2, y2)
    ti = np.arange(t_start, t_end)
    interpolation_values = f(ti)

    # delta tec
    indxs = np.where((time <= t_end) & (time >= t_start))[0]
    y4 = tecu_normal[indxs]

    n = len(ti)
    difference = np.zeros(n)

    for i in range(n):
        difference[i] = y4[i] - interpolation_values[i]

    return ti, difference

    
    











































































