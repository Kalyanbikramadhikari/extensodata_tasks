# import mysql.connector
import sqlalchemy
import pandas as pd

# building connection
# mydb = mysql.connector.connect(
# #   host="DESKTOP-K0OTGK8",
#   host="localhost",
#   user="root",
#   password="1234",
#   database = "practical"
# )
engine = sqlalchemy.create_engine(
'mysql+mysqlconnector://root:1234@localhost:3306/practical')

# mycursor = engine.cursor()
query = "SELECT * FROM employee "
# mycursor.execute(query)
# myresult = mycursor.fetchall() 
# print(myresult)

df = pd.read_sql(query,engine)
print(df)

# making data manipupulation with data frame
age = [23,54,32,21,34,32,67,43,33,34]
df['Age']= age

print(df)

df.to_sql(
    "employee",
    engine,
    index=False,
    if_exists='replace'

)

