import pymysql.cursors
import sys
import json
import pandas as pd


def data_access_service(path, query, fields):
    config = {
        'user': 'root',
        'password': 'sh01dan5',
        'host': 'localhost',
        'database': 'lahman2016',
        'raise_on_warnings': True,
        'charset': 'utf8'
    }

    # try:
    cnx = pymysql.connect(
        host='localhost',
        user='dbuser',
        password='dbuser',
        db='lahman2016',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor)

    cursor = cnx.cursor()

    # except:
    #   raise Exception("Error")
    a = path.split('/')
    n = len(a)

    # this is to correctly format fields and put the fields error if there is one
    f = ""
    if (fields == None):
        f = "*"
    elif (type(fields) == list):
        try:
            cursor.execute("SELCT * FROM " + a[2])
        except:
            cnx.close()
            cursor.close()
            return {"error": "Invalid path"}
        for i in fields:
            try:
                cursor.execute("SELECT " + i + " FROM " + a[2])
            except:
                cnx.close()
                cursor.close()
                return {"error": "Field not found", "field": i}
        f = ", ".join(fields)
    elif (type(fields == str)):
        f = fields.split(",")
        try:
            cursor.execute("SELCT * FROM " + a[2])
        except:
            cxn.close()
            cursor.close()
            return {"error": "Invalid path"}
        for i in fields:
            try:
                cursor.execute("SELECT " + i + " FROM " + a[2])
            except:
                cnx.close()
                cursor.close()
                return {"error": "Field not found", "field": i}
        f = fields
    else:
        cnx.close()
        cursor.close()
        return {"ERROR": "fields not a str or list"}

    qry = ""
    if (n == 2 and "metadata" in a):
        # case with metadata
        # the query returns a JSON object containing the information about the resources columns and keys
        if query is not None:
            cnx.close()
            cursor.close()
            return {"Error": "query should be none in metadata case"}
        if fields is not None:
            cnx.close()
            cursor.close()
            return {"Error": "fields should be none in metadata case"}

        qry = "DESCRIBE " + a[1] + ";"
        try:
            cursor.execute(qry)
        except:
            cursor.close()
            return {"error": "Invalid path"}
        result = json.dumps(cursor.fetchall())


    elif (n == 2):
        # case just /resource:
        # filter is a SQL WHERE clause
        # fields is a list of columns to retrieve.
        # The function returns a JSON object containing the selected resources and the selected properties.
        resource = a[1]
        if query is not None:
            qry = "SELECT " + f + " FROM " + resource + " WHERE " + query + ";"
        else:
            qry = "SELECT " + f + " FROM " + resource + ";"
        try:
            cursor.execute(qry)
        except:
            cnx.close()
            cursor.close()
            return {"error": "Invalid path"}
        result = json.dumps(cursor.fetchall())

    elif (n == 3):
        # case with /resource/primary_key
        # filter is none
        # fields is a list of fields to get from the identified resources.
        # The function returns a JSON object containing the identified resources and the selected properties
        # query is null/none
        resource = a[1]
        pk = a[2]
        pk = pk.split('-')

        if query is not None:
            cnx.close()
            cursor.close()
            return {"error": "Invalid path"}

       # cursor.execute("SHOW KEYS FROM " + resource + "WHERE Key_name = 'PRIMARY';")
        cursor.execute("SHOW KEYS FROM " + resource);
        pks = cursor.fetchall()

        if (len(pks) != len(pk)):
            cnx.close()
            cursor.close()
            return {"error": "Invalid path"}
        peekay = []

        for i, key in enumerate(pk):
            peekay.append(key["Column_name"] + " = " + '"' + pk + '"')
        peekay = " AND ".join(where)

        qry = "SELECT " + f + " FROM " + resource + " WHERE " + peekay + ";"
        try:
            cursor.execute(qry)
        except:
            cnx.close()
            cursor.close()
            return {"error": "Invalid path"}
        result = json.dumps(cursor.fetchall())

    elif (n == 4):
        # case with /resource/primary_key/resource
        # query is none
        # fields is a list of fields to get from the identified resources.
        # The function returns a JSON object containing the identified resources and the selected properties
        # return records from r2 for the pk from resource,

        # The function call dataservice_get(/Master/willite01/Batting,['yearID','ab'],None) maps to the SQL statement
        # SELECT yearID, ab FROM Batting where playerID='willite01'

        resource = a[1]
        pk = a[2]
        pk = pk.split('-')
        r2 = a[3]

        if query is not None:
            cnx.close()
            cursor.close()
            return {"error": "Invalid path"}

        cursor.execute("SHOW KEYS FROM " + resource + "WHERE Key_name = 'PRIMARY';")
        pks = cursor.fetchall()

        if (len(pks) != len(pk)):
            cnx.close()
            cursor.close()
            return {"error": "Invalid path"}
        peekay = []

        for i, key in enumerate(pk):
            peekay.append(key["Column_name"] + " = " + '"' + pk + '"')
        peekay = " AND ".join(peekay)

        qry = "SELECT " + f + " FROM " + r2 + " WHERE " + peekay + ";"
        try:
            cursor.execute(qry)
        except:
            cnx.close()
            cursor.close()
            return {"error": "Invalid path"}

        result = json.dumps(cursor.fetchall())
    else:
        cnx.close()
        cursor.close()
        return {"error": "Invalid path"}
    cnx.close()
    cursor.close()
    if (len(result) == 0):
        return {}
    return result


foo = data_access_service("/master/willite01", None, None)
print(foo)