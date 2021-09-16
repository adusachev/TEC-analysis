import numpy as np
import pandas as pd


def height_profile(data, months_nums: list, sza_interval=(0, 60), f107_value=150):
    """
    Производит отбор данных по трем критериям:
        1) период солнечной активности (месяц/месяцы)
        2) зенитный угол (от 0 до 60 градусов)
        3) индекс F10.7 > 150
    По отобранным данным усредняет значения давления и температуры
    
    :param data: высотные профили давления и концентраций нейтралов (данные со спутника AURA)
    :param months_nums: номера месяцев для отбора
    :param sza_interval: интервал зенитного угла
    :param f107_value: граничное значение индекса F10.7
    :return: P_mean, T_mean - усренные значения давления и температуры
    """    
    conditions = pd.DataFrame(data['Conditions'])
    
    # отбор данных:
    months = conditions.values[:, 1]
    months_numbers = np.array([], dtype=np.int64)
    for num in months_nums:
        tmp = np.where(months == num)[0]
        months_numbers = np.union1d(tmp, months_numbers)

    sza = conditions.values[:, 7]
    sza_numbers = np.where((sza > sza_interval[0]) & (sza < sza_interval[1]))[0]

    f107 = conditions.values[:, 8]
    f170_numbers = np.where(f107 > f107_value)[0]

    n2 = np.intersect1d(months_numbers, sza_numbers)
    final_numbers = np.intersect1d(f170_numbers, n2)
    
    # усреднение давления и температуры:
    P = data['Pressure'][final_numbers, :]
    T = data['Temperature'][final_numbers, :]

    P_mean = np.mean(P, axis=0)
    T_mean = np.mean(T, axis=0)
    
    return P_mean, T_mean