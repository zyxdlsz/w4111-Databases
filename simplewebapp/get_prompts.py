import pymysql
import pandas as pd

# Connect to the database over the network. Use the connection
# to send commands to the DB.
default_cnx = pymysql.connect(host='localhost',
                             user='dbuser',
                             password='dbuser',
                             db='W4111',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def _run_q(q, args=None, fields=None, fetch=True, cnx=None, commit=True):
    """

    :param q: An SQL query string that may have %s slots for argument insertion.
    :param args: A tuple of values to insert in the %s slots.
    :param fetch: If true, return the result.
    :param cnx: A database connection. May be None
    :param commit: Do not worry about this for now. This is more wizard stuff.
    :return: A result set or None.
    """

    # Use the connection in the object if no connection provided.
    if cnx is None:
        cnx = default_cnx

    # Convert the list of columns into the form "col1, col2, ..." for following SELECT.
    if fields:
        q = q.format(",".join(fields))

    cursor = cnx.cursor()  # Just ignore this for now.

    # If debugging is turned on, will print the query sent to the database.
    print("Query = ", cursor.mogrify(q, args))

    cursor.execute(q, args)  # Execute the query.

    # Technically, INSERT, UPDATE and DELETE do not return results.
    # Sometimes the connector libraries return the number of created/deleted rows.
    if fetch:
        r = cursor.fetchall()  # Return all elements of the result.
    else:
        r = None

    if commit:  # Do not worry about this for now.
        cnx.commit()

    return r


def get_product_values():
    q = "describe consumer_complaints_better"
    result = _run_q(q, fetch=True, commit=True)
    for r in result:
        if r['Field']=='Product':
            t = r['Type']
            t = t[5:-1]
            t = t.split("'")
            result = [s for s in t if len(s) > 1]
            return result
    else:
        return None



print(get_product_values())
