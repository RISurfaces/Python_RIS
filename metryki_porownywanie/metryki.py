import pandas as pd
import numpy as np
from time import perf_counter

def read_values_from_file(file_path):
    data_file = pd.read_csv(file_path, sep=';', header=None, names=['horizontal','vertical' , 'pattern', 'freq', 'power'])
    
    return data_file
    

def data_filter(data_file_X, horizontal_range,pattern):
    # Filtracja danych dla obu plików
    df_pattern_X = data_file_X[
        (data_file_X['pattern'] == pattern) &
        (data_file_X['horizontal'] >= horizontal_range[0]) &
        (data_file_X['horizontal'] <= horizontal_range[1])
    ]

    # Tworzenie pivot tables
    data = df_pattern_X.pivot_table(index='vertical', columns='horizontal', values='power')
    
    return data

def SSD(data_X, data_Y):   
    diff = data_X-data_Y
    diff = diff.fillna(0)
    diff = diff**2
    result = diff.values.sum()
    sq_X, sq_Y = data_X**2, data_Y**2
    sq_X, sq_Y = sq_X.values.sum(), sq_Y.values.sum()
    denominator = sq_X*sq_Y
    result_normalized = result/np.sqrt(denominator)

    return result, result_normalized

def CC(data_X, data_Y):   
    multiply = data_X*data_Y
    multiply = multiply.fillna(0)
    multiply = multiply**2
    result = multiply.values.sum()
    sq_X, sq_Y = data_X**2, data_Y**2
    sq_X, sq_Y = sq_X.values.sum(), sq_Y.values.sum()
    denominator = sq_X*sq_Y
    result_normalized = result/np.sqrt(denominator)

    return result, result_normalized

#Średni błąd kwadratowy
def MSE(data_X, data_Y):   
    row, cols = data_X.shape
    diff = data_X-data_Y
    diff = diff.fillna(0)
    diff = diff**2
    result = (1/(row*cols))*diff.values.sum()

    return result

#Maksymalny błąd absolutny
def MAE(data_X, data_Y):
    row, cols = data_X.shape
    diff = data_X-data_Y
    diff = diff.fillna(0)
    diff = diff.abs()
    result = (1/(row*cols))*diff.values.sum()

    return result

#MAIN
path_X = '/Users/dawidbrzakala/Python_RIS/wyniki_surowe_dane/charakterystyka_3D/char_pozioma_3D/13_06_ch_ka_3D_5_5Ghz_1m.csv'
path_Y = '/Users/dawidbrzakala/Python_RIS/wyniki_surowe_dane/charakterystyka_3D_nowe_anteny_AINFO/28_10_3D_5_5Ghz_1m_new_ant.csv'
pattern = 18
horizontal_range=(45, 135) #Oganiczenie pobierania danych - dane z azymutu od 45 do 135 stopni
data_set_X, data_set_Y = read_values_from_file(path_X), read_values_from_file(path_Y)
pattern_set_X,pattern_set_Y = data_filter(data_set_X,horizontal_range,pattern), data_filter(data_set_Y,horizontal_range,pattern)
print('\n')

wartosc = MSE(pattern_set_X,pattern_set_Y)
print(f'Wynik MSE: {wartosc} \nIm mniejsza wartość MSE, tym obrazy są bardziej podobne.\n')

wartosc = MAE(pattern_set_X,pattern_set_Y)
print(f'Wynik MAE: {wartosc}')

wartosc,wartosc_znormalizowana = SSD(pattern_set_X,pattern_set_Y)
print(f'Wynik SSD: {wartosc}, Znormalizowane: {wartosc_znormalizowana}')

wartosc_CC,wartosc_znormalizowana_CC = CC(pattern_set_X,pattern_set_Y)
print(f'Wynik CC: {wartosc_CC}, Znormalizowane: {wartosc_znormalizowana_CC}')
