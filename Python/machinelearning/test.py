import pymysql
import pandas as pd
conn = pymysql.connect(host ='localhost',user = 'caofa',passwd = 'caofa',db = 'pythonStocks')
df = pd.read_sql('show tables',con=conn)
print(df)


