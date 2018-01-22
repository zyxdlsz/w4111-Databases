# We need a module (library) that can communicate with the
# database server.
import pymysql.cursors
import 

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

# Connect
cnx = pymysql.connection(host='localhost',
                             user='dbuser',
                             password='dbuser',
                             db='lahman2016',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# I manually created the tables (not shown).
# Let's see what database thinks a table is like.
def describe_table(t):

    q = "show columns from  " + t + ";"
    #print ("Query = ", q)
    with cnx.cursor() as cursor:
        # Create a new record
        cursor.execute(q)

    df_mysql = pd.read_sql(q,cnx)
    return df_mysql

# Describe the AllStarFullBetter table.
print("\n\n")
print("AllStarFullBetter table is \n", describe_table("AllStarFullBetter"))