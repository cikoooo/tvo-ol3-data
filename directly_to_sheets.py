import pygsheets
import pandas as pd
from selenium import webdriver
import sys
import datetime as dt


'''
Same idea as TVO-OL3.py, but this works only with Google Sheets, no dummy csv-files.
'''

def google():
    gc = pygsheets.authorize(service_account_file=r'Credentials_Google_OL3.json')

    # Get current data from web
    df = dataframe()
    df["DateTime"] = df["DateTime"].dt.strftime('%Y-%d-%m %H:%M:%S')
    df["DateTime"] = pd.to_datetime(df["DateTime"], format='%Y-%m-%d %H:%M:%S')
    
    print("Beginning transfer...")
    
    sheet = gc.open('OL3 Data')
    sheets_only = sheet[2]

    # Get data from Sheets
    old_df = sheets_only.get_as_df()
    old_df = old_df[["DateTime", "Tuntikeskiteho", "Päivitetty"]]
    old_df = old_df.reset_index(drop=True)
    old_df["DateTime"] = pd.to_datetime(old_df["DateTime"], format='%Y-%m-%d %H:%M:%S')
    
    # Append the current data to Sheets
    new_df = pd.concat([old_df, df])
    new_df = new_df.drop_duplicates(subset="DateTime" ,keep="last")
    new_df['Id'] = range(0, len(new_df))
    new_df = new_df[["Id", "DateTime", "Tuntikeskiteho", "Päivitetty"]]
    
    print("Updated and appended information:")
    print(df)

    sheets_only.set_dataframe(new_df, (0,0))
    return(print("Transfer done"))


def dataframe():
    # Collects current data from the web and stores it into a DataFrame
    # Might contain some unnecessary code as of yet, as this was copied from TVO-OL3.py

    url = 'https://www.tvo.fi/tuotanto/laitosyksikot/ol3/ol3ennusteet.html'
    try:
        driver = webdriver.Firefox(executable_path=r'C:\Users\Nico\anaconda3\geckodriver.exe')
        driver.get(url)
        driver.implicitly_wait(10)
        df = pd.read_html(driver.find_element_by_id("DataTables_Table_8").get_attribute('outerHTML'))[0]
        df["DateTime"] = pd.to_datetime(df["Pvm"] + " " + df["Tunti"])
        df = df.drop(columns="ID")
        driver.quit()
    except:
        print("Error on Selenium end!")
        print("ending....")
        driver.quit()
        sys.exit()



    df = df.drop_duplicates(subset="DateTime", keep="last") # laitettu parametri keep="last"
    #df = df.drop(columns="Unnamed: 0")
    try:
        df = df.drop(columns=["Viikonp�iv�", "Pvm", "Kuukausi", "Tunti"]) # Viikonpäivä muutettu Viikonp�iv� koska se on jotenkin rikki?
    except KeyError:
        df = df.drop(columns=["Viikonpäivä", "Pvm", "Kuukausi", "Tunti"])

    df["Päivitetty"] = f"{dt.datetime.now():%Y/%m/%d %H:%M}"
    df = df[["DateTime", "Tuntikeskiteho", "Päivitetty"]]
    df.index.name = 'Id'

    return(df)


def main():
    print("Collecting data from the web...")
    google()
    print("Program completed.")

if __name__ == "__main__":
    main()
