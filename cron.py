import os
import pyodbc 
import pandas as pd
def dbconnect():
    mydb = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=database-3.c1tcw6ocvqyh.us-east-1.rds.amazonaws.com;"
                        "Database=damo;"
                        "uid=Damo;pwd=Damo2021")
    return mydb

mydb = dbconnect()
cursor = mydb.cursor()
aid_sql = "select filename from Downloads where status = 'Downloaded'"
main_df = pd.read_sql_query(aid_sql,mydb)
filenames = (main_df.iloc[0:,0]).tolist()
for file in filenames:
	os.remove("static//files/"+ file + ".xlsx")
