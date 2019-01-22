
import pymysql.cursors

import BaseDataTable
import RDBDataTable

import pandas as pd
import json

# The database server is running somewhere in the network.
# I must specify the IP address (HW server) and port number
# (connection that SW server is listening on)
# Also, I do not want to allow anyone to access the database
# and different people have different permissions. So, the
# client must log on.


# Connect to the database over the network. Use the connection
# to send commands to the DB.
cnx = pymysql.connect(host='localhost',
                             user='dbuser',
                             password='dbuser',
                             db='lahman2017',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



dataTables = dict()

dataTables['People'] = RDBDataTable.RDBDataTable('People', ['playerID'])


def retrieve_by_primary_key(table_name, key_value, fields=None):

    tbl = dataTables.get(table_name)
    if tbl is not None:
        result = tbl.find_by_primary_key(key_value, fields)
        result = result.get_rows()
    else:
        result = None

    return result







# Get metadata to help populate search and data entry forms.
def retrieve_metadata(table):
    cursor = cnx.cursor()
    q = "SHOW FIELDS FROM " + table + ";"
    print("Query = ", q)
    cursor.execute(q)
    r = cursor.fetchall()
    return r







