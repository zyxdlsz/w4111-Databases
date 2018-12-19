# We need a module (library) that can communicate with the
# database server.
import mysql.connector

# Pandas makes handling relation, and other result, in
# Python much, much easer.
import pandas as pd

# The database server is running somewhere in the network.
# I must specify the IP address (HW server) and port number
# (connection that SW server is listening on)
# Also, I do not want to allow anyone to access the database
# and different people have different permissions. So, the
# client must log on.
config = {
  'user': 'dbuser',
  'password': 'dbuser',
  'host': '127.0.0.1',
  'database': 'lahman2016',
  'raise_on_warnings': True,
  'charset' : 'utf8'
}


cnx = mysql.connector.connect(**config)
cursor=cnx.cursor()
q = "CREATE SCHEMA hw1";
cursor.execute(q)
cnx.commit()

# Connect
cnx = mysql.connector.connect(**config)
q = "CREATE TABLE hw1.student (studentID varchar(16), name varchar(64), age int(6));"
cursor=cnx.cursor()
cursor.execute(q)
cnx.commit()

q = "INSERT INTO hw1.student VALUES('dff9', 'Donald Ferguson', 29);"
cursor=cnx.cursor()
cursor.execute(q)
cnx.commit()
result=cursor.rowcount
print("INSERT create ", result, " rows")