import csv

with open('x.csv',"r", newline='') as input:
    with open('24_04_ch_ka_3D_5_5Ghz_1_5m_jest_zero_copy.csv',"w", newline='') as output:
        spamreader = csv.reader(input, delimiter=";", quotechar='|')
        writer = csv.writer(output, delimiter=';', quotechar='|')
        for row in spamreader:
            row[0] = str(round(float(row[0]), 2))
            row[1] = str(round(float(row[1]), 2))
            writer.writerow(row,)



                    
                
