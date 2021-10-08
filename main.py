import os
import glob
import pandas as pd
os.chdir("C:/Users/crayx/PycharmProjects/AlertTrace/Csv")

try:
    import os

    os.remove('C:/Users/crayx/PycharmProjects/AlertTrace/Csv/combined_csv.csv')

except:
    pass

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

my_csvs = [pd.read_csv(f) for f in all_filenames]
my_csv = my_csvs[0]
for csv in my_csvs[1:]:
    for column in csv.columns:
        my_csv[column] = csv[column]

my_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
