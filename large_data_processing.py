import os
import sqlalchemy 
import argparse
import pandas as pd
import datetime
import pymysql

MYSQLDB = os.environ['MYSQLDB']
class MyDBConnection:
    SELECT_ALL = "SELECT * FROM {df}"
    DELETE_ALL = "DELETE FROM {df}"
    def __init__(self, db):
        url = f'mysql+pymysql://{MYSQLDB}/'
        self.engine = sqlalchemy.create_engine(url)
        try:
            with self.engine.connect() as con:
                self.engine.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
            print('engine is valid')
        except Exception as e:
            print(f'Engine invalid: {str(e)}')
        self.engine = sqlalchemy.create_engine(f'mysql+pymysql://{MYSQLDB}/{db}')
        
    def load_df(self, df_name, empty=False):
        try:
            df = pd.read_sql(self.SELECT_ALL.format(df=df_name), self.engine)
            empty and self.execute_sql_query(self.DELETE_ALL.format(df=df_name))
        except pymysql.err.ProgrammingError:
            df = pd.DataFrame()
        return df
    
    def execute_sql_query(self, sql_query, as_dict=False):
        with self.engine.connect() as con:
            try:
                resp = con.execute(sql_query)
                if as_dict:
                    resp = [{column: value for column, value in rowproxy.items()} for rowproxy in resp]
            except pymysql.err.ProgrammingError:
                resp = []
            return resp
        
    def write_to_sql(self, df, table_name, index=False, if_exists="replace"):
        if df.empty:
            print("DB write Skipped... no data found in df", table_name)
            return True
        try:
            df.to_sql(con=self.engine, name=table_name, if_exists=if_exists, index=index, chunksize=10000)
        except Exception as e:
            return(e, False)
        return "Successful",True
    
    def read_sql_query(self, query):
        try:
            df = pd.read_sql(query, self.engine)
        except pymysql.err.ProgrammingError:
            df = pd.DataFrame()
        return df

class LargeDataProcessor():
    def __init__(self, db):
        self.sql_conn = MyDBConnection(db)
    def append_data_in_product_table(self, csv_path):
        df = pd.read_csv(csv_path, index_col=False)
        df = df[['name', 'sku', 'description']]
        df['upload_date'] = datetime.datetime.now().date()
        msg, r = self.sql_conn.write_to_sql(df=df, table_name="product_details", if_exists="append")
        if r:
            print("Successful Appened Data in product_details table")
        else:
            print("The Data is not be appened due to error:", msg)
        del df
            
    def update_product_count_table(self):
        try:
            date_df = self.sql_conn.read_sql_query("select * from product_count_update_date")
        except sqlalchemy.exc.ProgrammingError:
            date_df = pd.DataFrame(columns=['update_date'])
        if date_df.empty:
            df = self.sql_conn.load_df("product_details")
            temp = pd.DataFrame()
        else:
            max_date = date_df['update_date'][0]
            df = self.sql_conn.read_sql_query(f"select * from product_details where upload_date>{max_date}")
            temp = self.sql_conn.read_sql_query(f"select * from product_count")
        print
        date_df = pd.DataFrame([df['upload_date'].max()], columns=['update_date'])
        product_with_same_name = df.groupby("name")['sku'].size().reset_index(name='no. of products')
        if not temp.empty:
            product_with_same_name = product_with_same_name.append(temp)
        del temp
        del df
        product_with_same_name = product_with_same_name.groupby("name")['no. of products'].sum().reset_index(name='no. of products')
        msg, r = self.sql_conn.write_to_sql(df=product_with_same_name, table_name="product_count")
        if r:
            print("Successful Updated the product_count table")
            self.sql_conn.write_to_sql(df=date_df, table_name="product_count_update_date")
        else:
            print("The Data is not be appened due to error:", msg)

    def update_product_details_table(self, name, sku, desc):
        if sku=="":
            print("Please enter the 'sku' key you want to update")
            return
        if name!="" and desc!="":
            query = f"UPDATE product_details SET name='{name}', description='{desc}'' where sku='{sku}'"
        elif name!="":
            query = f"UPDATE product_details SET name='{name}' where sku='{sku}'"
        elif desc!="":
            query = f"UPDATE product_details SET description='{desc}' where sku='{sku}'"
        else:
            print("please enter the values you want to update")
            return
        try:
            resp = self.sql_conn.execute_sql_query(query)
            print("Successful Updated the product_details table")
        except Exception as e:
            print(e)



        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Large Data Processor')
    parser.add_argument('--database', type=str, help='Database name', default="")
    parser.add_argument('--csv', type=str, help='CSV Path', default="")
    parser.add_argument('--action', type=str, help='Action', default="")
    parser.add_argument('--name', type=str, help='name to update on the basis of sku key', default="")
    parser.add_argument('--desc', type=str, help='description to update on the basis of sku key', default="")
    parser.add_argument('--sku', type=str, help='sku to update on the basis of sku key', default="")
    x = datetime.datetime.now()
    args = parser.parse_args()
    csv_path = args.csv
    db = args.database
    sku = args.sku
    name = args.name
    desc = args.desc
    if db=="":
        print("Please enter the Database name")
    LDP = LargeDataProcessor(db)
    if args.action == "upload_product_details":
        LDP.append_data_in_product_table(csv_path)
        print("Process Execution Time:",datetime.datetime.now()-x)
    elif args.action == "update_product_count_table":
        LDP.update_product_count_table()
        print("Process Execution Time:",datetime.datetime.now()-x)
    elif args.action == "update_product_details_table":
        LDP.update_product_details_table(name, sku, desc)
        print("Process Execution Time:",datetime.datetime.now()-x)
    else:
        print("Please Enter a valid action")
        print("Process Execution Time:",datetime.datetime.now()-x)


