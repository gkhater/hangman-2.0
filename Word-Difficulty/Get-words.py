'''
    You should run this file from Hangman_2 for the relative path to be correct
'''

import json 
import csv 

with open('Data.json', 'r') as file: 
    data = json.load(file)

csv_data = []
model = 'Stat model'

for index, game_id in enumerate(data[model]): 
    if index >= 10**3: 
        break

    csv_data.append([game_id, data[model][game_id]['Target word']])


# Specify the CSV file name
csv_file = './Word-Difficulty/Labelled_difficulty.csv'

with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    # Writing the header (optional but recommended)
    writer.writerow(['Game ID', 'Word', 'Difficulty'])

    # Writing the data
    writer.writerows(csv_data)