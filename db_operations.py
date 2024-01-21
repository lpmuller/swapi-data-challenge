from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite:///star_wars.db')

def save_to_db(dataframe, table_name):
    dataframe.to_sql(table_name, engine, if_exists='replace', index=False)

def query_db(sql_query):
    return pd.read_sql_query(sql_query, engine)