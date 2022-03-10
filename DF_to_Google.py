import pygsheets
import pandas as pd

gc = pygsheets.authorize(service_account_file=r'Credentials_Google_OL3.json')

df = pd.read_csv(r'OL3_tuotanto_koekayton_aikana.csv')

print("Beginning transfer...")

sheet = gc.open('OL3 Data')
wks = sheet[1]

wks.set_dataframe(df, (0,0))
print("Done")