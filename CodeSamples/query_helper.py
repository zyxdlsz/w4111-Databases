# We need a module (library) that can communicate with the
# database server.
import pymysql.cursors
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
  'host': '10.0.1.4',
  'database': 'lahman2016',
  'raise_on_warnings': True,
  'charset' : 'utf8'
}

# Connect
cnx = pymysql.connect(host='localhost',
                             user='dbuser',
                             password='dbuser',
                             db='lahman2016',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def run_query(q):
    try:
        with cnx.cursor() as cursor:
            # Create a new record
            cursor.execute(q)

        df_mysql = pd.read_sql(q,cnx)
        return df_mysql
    except pymysql.InternalError as e:
        code, message = e.args
        print (e)
        if code == 1054:
            raise ValueError("Invalid field requested.")
    except pymysql.ProgrammingError as e:
        code, message = e.args
        print(e)
        if code == 1146:
            raise ValueError("Resource type does not exist.")



def print_result(msg, pf):
    print(msg)
    print(pf)


r = run_query("SELECT nameFirst FROM mMaster where nameLast='Williams' and nameFirst LIKE '%a%'")
print("Query result is =\n", r)