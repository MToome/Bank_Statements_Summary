# Bank_Statements_Summary
Picks data from CSV files, adds categories, and uploads it to Google Sheets where it is summarized.

To connect code to Google Sheets
Will need to install gspread:  pip3 install gspread
Will need to enable API Access for the project Sheets page:
Go to https://docs.gspread.org/en/latest/oauth2.html#enable-api-access-for-a-project
Pick Credentials from the left bar
Then create credentials
 and choose the Service account 
fill in the account name and it will generate an ID for you
Optional info I left it empty
after pressing done click on the service account that was created
on the top bar, there is KEYS, press that and select ADD KEY, Create new key, choose JSON
JSON file will be downloaded
open it with a text editor and copy the email that comes after "client_email ": 
Go to the Google Sheets page that you made for this click share and paste the email.

In the program import gspread
to tell the program to make a connection to Google Sheets enter:

gc = gspread.service_account()
sh = gc.open("Google Sheets Name")

For more info on gspread: visit: https://docs.gspread.org/en/v5.12.0/