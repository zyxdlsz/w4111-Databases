import pymysql.cursors
import json


def connect():
    connection = pymysql.connect(host='localhost',
                                 user='dbuser',
                                 password='dbuser',
                                 db='lahman2016',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def disconnect(c):
    c.close()


def retrieve_by_id(table, attribute, id):
    try:
        print("DEBUG: table = ", table)
        print("DEBUG: attribute = ", attribute)
        print("DEBUG: id = ", id)

        connection = connect()
        result = {"data": "Not Found"}

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM " + table
            sql = sql + " WHERE "
            sql = sql + attribute + "=" + "'" + id + "';"
            print("DEBUG: SQL = ", sql)
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
    except:
        print("Something happened.")
    finally:
        disconnect(connection)

    return result

#print("Ran")
# And a test would be
player = retrieve_by_id("Master", "playerID", "napolmi01")

#print("\n\n Test Result ")
#print("The player with playerID = napolmi01 is")
#print(json.dumps(player, indent=4, sort_keys=True))