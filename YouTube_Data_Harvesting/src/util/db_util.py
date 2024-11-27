import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
from util.yt_exception import YouTubeException
import mysql.connector
from mysql.connector import Error

class MySqlDBUtil:
    def __init__(self,host, user, password, dbName):
        self.db_url = "mysql+mysqlconnector://root:root%40123@localhost/rsk_youtube_db"
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=dbName
        )
    
    def execute_select(self, query, params=None):
        try:
            print(f"Successfully connected to MySQL: {self.connection.is_connected()}")
            # with self.connection.cursor() as cursor:
            #     cursor.execute(query, params)
            #     result = cursor.fetchall()
            #     return result
            df = pd.read_sql(query, self.connection, params=params)
            return df
        except Error as e:
            print(f"Error: {e}")

    def insert_or_update(self, df, table_name):
        try:
            print(f"Successfully connected to MySQL: {self.connection.is_connected()}")
            # Generate placeholders and columns
            columns = df.columns.tolist()
            columns_names = ', '.join(columns)
            update_columns = ', '.join([f"{col}=VALUES({col})" for col in columns])
            placeholders = ', '.join(['%s'] * len(columns))
            bulk_records = [tuple(row) for row in df.to_numpy()]
            
            
            query = f"""INSERT INTO {table_name} ({columns_names}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {update_columns};"""

            # Execute the query
            with self.connection.cursor() as cursor:
                cursor.executemany(query, bulk_records)
                self.connection.commit()

            print(f"Query executed successfully in {table_name} table. Rows affected: {cursor.rowcount}")
        
        except Error as e:
            print(f"Error: {e}")


    def save_to_db(self, df, table_name):
        engine = create_engine(self.db_url)
        try:
            # Save DataFrame to MySQL
            columns = df.columns.tolist()
            columns_names = ', '.join(columns)
            update_columns = ', '.join([f"{col}=VALUES({col})" for col in columns])
            placeholders = ', '.join(['%s'] * len(columns))
            bulk_records = [tuple(row) for row in df.to_numpy()]

            bulk_query = f"""INSERT INTO {table_name} ({columns_names}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {update_columns}"""
            print(bulk_query)
            print(f"""bulk_records: {bulk_records[:]}""")  
            with engine.connect() as conn:
                conn.execute(text(bulk_query), [tuple(row) for row in df.to_numpy()])

            print("DataFrame successfully saved to MySQL!")
        except Exception as e:
            print(e)
            #raise YouTubeException("Issue while store the data in to database",300)

