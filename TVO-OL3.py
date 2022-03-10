'''
Get data from web about the energy production of OL3 nuclear facility.
It is starting, and some data is being published to the web about its power production during deployment.

The purpose is to transform the data into an excel (or csv) file to be visualised with tableau.
'''

import pandas as pd
from pandas import read_csv
from selenium import webdriver
import sys
import datetime as dt


url = 'https://www.tvo.fi/tuotanto/laitosyksikot/ol3/ol3ennusteet.html'


'''
Connect to web with Firefox and try to find datatable. If not found within 10 seconds, the program will shutdown.
If datatable found, read it into a DataFrame and create DateTime-column and drop ID-col.
'''
try:
    driver = webdriver.Firefox(executable_path=<fileLocation>')
    driver.get(url)
    driver.implicitly_wait(10)
    df = pd.read_html(driver.find_element_by_id("DataTables_Table_8").get_attribute('outerHTML'))[0]
    df["DateTime"] = pd.to_datetime(df["Pvm"] + " " + df["Tunti"])
    df = df.drop(columns="ID")
    print("Appending...", "\n", df.head())
except:
    print("Error on Selenium end!")
    print("ending....")
    driver.quit()


'''
Look if test.csv exists. If not, create it.
Append new data entries into a csv-file.
'''
try:
    _dummy = read_csv(r'test.csv')
    df.drop_duplicates(subset="DateTime")
    df.to_csv(r'test.csv', mode="a", header=None)
    print("Done!")
    print("Transforming file...")
        
except FileNotFoundError:
    df.to_csv(r'test.csv')
    print("File not found, creating...")


'''
Read the updated data and create a new DataFrame of it.
Drop duplicates and unnecessary columns, change column order and save the csv-file.
End program.

HOX! If this does not work, replace test with copy of test, as I deleted the Päivitetty-column!!!
'''
df = read_csv(r'test.csv')

df["DateTime"] = df['Pvm'] + " " + df['Tunti']
df["DateTime"] = pd.to_datetime(df["DateTime"], format='%d.%m.%Y %H:%M')

df = df.drop_duplicates(subset="DateTime", keep="last") # laitettu parametri keep="last"
df = df.drop(columns="Unnamed: 0")
try:
    df = df.drop(columns=["Viikonp�iv�", "Pvm", "Kuukausi", "Tunti"]) # Viikonpäivä muutettu Viikonp�iv� koska se on jotenkin rikki?
except KeyError:
    df = df.drop(columns=["Viikonpäivä", "Pvm", "Kuukausi", "Tunti"])

df["Päivitetty"] = f"{dt.datetime.now():%Y/%m/%d %H:%M}"
df = df[["DateTime", "Tuntikeskiteho", "Päivitetty"]]

df.index.name = 'Id'
print(df.tail())
df.to_csv(r'OL3_tuotanto_koekayton_aikana.csv')

print("Saved csv. Ending selenium....")
driver.quit()

