import csv
import glob
import os


import csv
with open('24_10_3D_5_5Ghz_1_5m_new_ant_accurate.csv', mode ='r')as file:
  csvFile = csv.reader(file, delimiter=';')
  with open ('24_10_3D_5_5Ghz_1_5m_new_ant.csv', 'w', encoding='utf-8') as f:
        w = csv.writer(f, delimiter=';')
        for row in csvFile:
            print(row)
            if row[1] in ['-27.0', '-18.0', '-9.0', '0', '9.0', '18.0', '27.0']:
                w.writerow(row)
  