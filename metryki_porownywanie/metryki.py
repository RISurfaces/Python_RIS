import pandas as pd 
import numpy as np
from time import perf_counter

def read_values_from_file(file_path):
    data_file = pd.read_csv(file_path, sep=';', header=None, names=['horizontal','vertical' , 'pattern', 'freq', 'power'])
    
    return data_file

def read_values_from_file_UNOREVERSE(file_path):
    data_file = pd.read_csv(file_path, sep=';', header=None, names=['vertical','horizontal' , 'pattern', 'freq', 'power'])
    
    return data_file
 
def save_metrics_multiple_patterns_to_excel(filename, results):
    # Tworzenie DataFrame z wynikami
    df_metrics = pd.DataFrame(results, columns=['Pattern', 'MSE', 'MAE', 'SSD', 'SSD Znormalizowane', 'CC', 'CC Znormalizowane'])
    
    # Zapis do pliku Excel
    df_metrics.to_excel(filename, index=False, sheet_name='Metrics')
    print(f'Wyniki dla wielu patternów zostały zapisane do pliku {filename}')

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
path_X = '/Users/dawidbrzakala/Python_RIS_nowy/Python_RIS/maximum.csv'
path_Y = '/Users/dawidbrzakala/Python_RIS_nowy/Python_RIS/minimum.csv'
pattern = 18
horizontal_range=(45, 135) #Oganiczenie pobierania danych - dane z azymutu od 45 do 135 stopni
data_set_X, data_set_Y = read_values_from_file(path_X), read_values_from_file(path_Y)
pattern_set_X,pattern_set_Y = data_filter(data_set_X,horizontal_range,pattern), data_filter(data_set_Y,horizontal_range,pattern)
print('\n')

# Lista do przechowywania wyników
results = []

# Iteracja po patternach
for pattern in range(1, 28):  # Od 1 do 27 włącznie
    try:
        # Filtrowanie danych dla bieżącego pattern
        pattern_set_X = data_filter(data_set_X, horizontal_range, pattern)
        pattern_set_Y = data_filter(data_set_Y, horizontal_range, pattern)
        
        # Obliczanie metryk
        mse_value = MSE(pattern_set_X, pattern_set_Y)
        mae_value = MAE(pattern_set_X, pattern_set_Y)
        ssd_value, ssd_normalized = SSD(pattern_set_X, pattern_set_Y)
        cc_value, cc_normalized = CC(pattern_set_X, pattern_set_Y)
        
        # Dodawanie wyników do listy
        results.append([pattern, mse_value, mae_value, ssd_value, ssd_normalized, cc_value, cc_normalized])
    
    except Exception as e:
        print(f'Błąd dla patternu {pattern}: {e}')
        results.append([pattern, None, None, None, None, None, None])  # Dodaj puste wartości w przypadku błędu

# Zapis do pliku Excel
output_filename = 'metryki_idealny.xlsx'
save_metrics_multiple_patterns_to_excel(output_filename, results)

# wartosc = MSE(pattern_set_X,pattern_set_Y)
# print(f'Wynik MSE: {wartosc} \nIm mniejsza wartość MSE, tym obrazy są bardziej podobne.\n')

# wartosc = MAE(pattern_set_X,pattern_set_Y)
# print(f'Wynik MAE: {wartosc}')

# wartosc,wartosc_znormalizowana = SSD(pattern_set_X,pattern_set_Y)
# print(f'Wynik SSD: {wartosc}, Znormalizowane: {wartosc_znormalizowana}')

# wartosc_CC,wartosc_znormalizowana_CC = CC(pattern_set_X,pattern_set_Y)
# print(f'Wynik CC: {wartosc_CC}, Znormalizowane: {wartosc_znormalizowana_CC}')
