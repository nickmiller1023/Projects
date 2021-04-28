
"""
Nick Miller
This Project uses Python to analyze mobile games from the Apple App Store
"""

from csv import DictReader
from fuzzywuzzy import fuzz

data_rdr = DictReader(open('appstore_games.csv', 'r', encoding='UTF8'))
data_rows = [d for d in data_rdr]

print(data_rows[:1])
print('\n')

#Format Data Output for Readability
for this_row in data_rows[0:1]:
    print('********* App ***************')
    for dict_item in this_row.items():
        print('Variable: {}\nValue: {}'.format(dict_item[0], dict_item[1]))
    print('*****************************\n')
    

record_count = 0
null_count = 0
duplicate_count = 0
fuzzy_count = 0
unique_data = []
clean_data = []
unique_ids = []
unfuzzy_data = []

#Remove Duplicate Records
for row in data_rows:
    record_count += 1
    for item in row.items():
        if item[0] == 'ID':
            if item[1] in unique_ids:
                duplicate_count += 1              
            else:
                unique_ids.append(item[1])
                unique_data.append(row)
                
#Remove Records with Null User Ratings       
for row in unique_data:
    for item in row.items():        
        if item[0] == 'User Rating Count':
            if not item[1]:
                null_count += 1
            else:
                clean_data.append(row)
               
#Print fuzzy matched records to see if we should group them
prev_app_name = ''
fuzzy_ratio = 0
for row in clean_data:
    for item in row.items():        
        if item[0] == 'Name':
            fuzzy_ratio = fuzz.token_set_ratio(item[1], prev_app_name)
            if fuzzy_ratio > 50:
                fuzzy_count += 1  
                print('Can these be grouped?', item[1], '---', prev_app_name)
            prev_app_name = item[1]
                
    
                
print('intial record count is', record_count)
print('count of nulls removed is', null_count)
print('count of duplicates removed is', duplicate_count)
print('count of clean records is', len(clean_data))
print('count of fuzzy matched app names is', fuzzy_count)
