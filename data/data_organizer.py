import os
import pandas as pd 
import csv
from xlrd import XLRDError

def quarter_sum(column):
    return sum([int(i) for i in column if type(i) == int or i.isdigit()])

years = []

for entry in os.listdir('.'):
    if os.path.isdir(os.path.join('.', entry)):
        years.append(entry)

years.sort()

corrupted_files = []

with open('data_format.csv', 'w') as file:
    fieldnames = ['Quarter_start_date', 'State', 'Occurrence']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for year in years:
        for entry in os.listdir('.'):
            if (entry == year):

                reports = []

                for state_report in os.listdir(entry):
                    reports.append(state_report)

                reports.sort()

                for state in reports:
                    file_path = year + '/' + state

                    try:
                        current_report = pd.read_excel(file_path)
                    except XLRDError:
                        corrupted_files.append(file_path + "\n")
                        continue
                    
                    first_quarter = (quarter_sum(current_report['Unnamed: 8'].dropna().tolist()))
                    second_quarter = (quarter_sum(current_report['Unnamed: 9'].dropna().tolist()))
                    third_quarter = (quarter_sum(current_report['Unnamed: 10'].dropna().tolist()))
                    fourth_quarter = (quarter_sum(current_report['Unnamed: 11'].dropna().tolist()))

                    state = state[:len(state) - 4].capitalize() 

                    writer.writerow({'Quarter_start_date': year + '.01.01', 'State': state, 'Occurrence': first_quarter})
                    writer.writerow({'Quarter_start_date': year + '.04.01', 'State': state, 'Occurrence': second_quarter})
                    writer.writerow({'Quarter_start_date': year + '.07.01', 'State': state, 'Occurrence': third_quarter})
                    writer.writerow({'Quarter_start_date': year + '.10.01', 'State': state, 'Occurrence': fourth_quarter})

corrupted_list = open("corrupted_files_list.txt",'r+')
corrupted_list.writelines(corrupted_files)
corrupted_list.close()