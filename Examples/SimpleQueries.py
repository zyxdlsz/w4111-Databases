import pymysql.cursors
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
default_cnx = pymysql.connect(host='localhost',
                             user='dbuser',
                             password='dbuser',
                             db='lahman2017',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def run_q(q, args=None, fields= None, fetch=True, cnx=None):
    """

    :param q: An SQL query string that may have %s slots for argument insertion.
    :param args: A tuple of values to insert in the %s slots.
    :param fetch: If true, return the result.
    :param cnx: A database connection. May be None
    :return: A result set or None.
    """

    if cnx is None:
        cnx = default_cnx

    if fields:
        q = q.format(",".join(fields))

    cursor=cnx.cursor()             # Just ignore this for now.
    print ("Query = ", q)

    cursor.execute(q, args)               # Execute the query.
    r = cursor.fetchall()           # Return all elements of the result.

    return r


"""
q = "select {} from people where playerID=%s"

result = run_q(q, args=('willite01'), fields=['nameLast', 'nameFirst'])
print(result)
"""