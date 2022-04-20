from logging import exception
import snowflake.connector
import json
import pandas as pd


def connection():
    with open(r'OL3 Data/snowflake_cred.json', "r") as f:
        cred = json.load(f)
        user = cred["user"]
        pw = cred["password"]
        account = cred["account"]
        warehouse = cred["warehouse"]
        database = cred["database"]
        schema = cred["schema"]

    conn = snowflake.connector.connect(
            user=user,
            password=pw,
            account=account,
            warehouse=warehouse,
            database=database,
            schema=schema
    )

    cur = conn.cursor()

    return cur


def data():
    df = pd.read_csv(r'OL3 Data/OL3_tuotanto_koekayton_aikana.csv')
    print(df.head())
    datetimes = [ x for x in df['DateTime'] ]
    tuntikeskiteho = [ x for x in df['Tuntikeskiteho'] ]
    dateteho = zip(datetimes, tuntikeskiteho)
    
    return dateteho

def main():
    dateteho = data()
    cur = connection()

    try:
        create_table = '''
                        CREATE TABLE IF NOT EXISTS DateTeho(
                        Date datetime, Teho decimal
                        )
                        '''
        cur.execute(create_table)

        for pair in dateteho:
            date, teho = pair
            insert = f'''INSERT INTO DateTeho VALUES ('{date}', {teho})'''
        
            print(insert)
            cur.execute(insert)


    except Exception as e:
        print(f"Unexpected {e}, {type(e)}")
        raise



if __name__ == '__main__':
    main()
