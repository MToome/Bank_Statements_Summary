'''CSV library is needed to use CSV dictionary'''
import csv
# Google sheet has a limit on how many times an api
# can interact with it in a minute, with sleep we can limit it
import time
# gspread makes it possible to use Google Sheets
import gspread
# Used to define a certain error
from gspread.exceptions import SpreadsheetNotFound

# Name the MONTH
MONTH = "onjghjkb"

# Empty list for filter data
pank_data= []

# Opens the file using UTF-8 because I have ö,ä,ü,õ in my bank
with open('Example_Account_statment.csv', encoding='UTF-8', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for line in reader:
        pank_data.append(line)

# Empty list for filter data
needed_info = []

# Sorting what data is needed and needs different clauses because I use
for line in pank_data:
    if 'Receiver/Payer account' in line:
        if float(line['Ammount'].replace(',','.')) > 0:
            continue
        else:
            needed_info.append([line['Receiver/Payer account'],
                                line['Explanation'],
                                float(line['Ammount'].replace(',','.')),])
    else:
        if line['Debit/Credit'] == 'D':
            if line['Explanation'] == 'Turnover':
                continue
            else:
                needed_info.append([
                    line['Receiver/Payer'],
                    line['Explanation'],
                    0 - float(line['Ammount'].replace(',','.'))])
        else:
            if line['Explanation'] == 'Opening balance' or line['Explanation'] == 'Turnover':
                continue
            elif line['Explanation'] == 'final balance':
                continue
            else:
                needed_info.append([
                    line['Receiver/Payer'],
                    line['Explanation'],
                    float(line['Ammount'].replace(',','.'))])

# Declear different spending types
Saving = ['Transfer to savings account', 'Saving']
Insurance = ['Life Insurance', 'Insurance payment']
Subscriptions = ['Netflix', 'Cell', 'Web']


def category(info, add_category):
    '''Function for adding category with single value'''
    for one_line in needed_info:
        # Check if the line has a category
        if len(one_line) == 4:
            continue
        else:
            if info in one_line[1]:
                one_line.append(add_category)


def category_from_list(data, add_category):
    '''Function for adding categories using a list'''
    for singel_line in needed_info:
        if len(singel_line) == 4:
            continue
        else:
            for name in data:
                if name in singel_line[1]:
                    singel_line.append(add_category)
                    #print(line)

category('Pay', 'Income')
category('Rent', 'Rent')
category('Granted a Loan', 'Granted a Loan')

category_from_list(Insurance, 'Insurance')
category_from_list(Saving, 'Saving')
category_from_list(Subscriptions, 'Subscription')

# Adds category for lines without one
for line in needed_info:
    if len(line) < 4:
        if line[2] > 0:
            line.append('Income')
        else:
            line.append('Other')

# Connecting to a Google spreadsheet and opening designated folder
gc = gspread.service_account()
sh = gc.open("Raha Asjad")

# Try to go to the assigned sheet if not it will great one
try:
    worksheet = sh.worksheet(f'{MONTH}')
except SpreadsheetNotFound:
    worksheet = sh.add_worksheet(f'{MONTH}',20, 25, None)


rows = needed_info

# Loops through data and inputs it
for row in rows:
    worksheet.insert_row(row, 10)
    # Waits 3 seconds because of connection restriction
    time.sleep(3)
