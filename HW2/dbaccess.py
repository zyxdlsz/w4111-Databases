import pymysql
import pandas as pd


# Simple class to connect to database. Connection information
# parameters would typically come from a config or context file,
# or call to configuration service.
#
# We would also implement connection pooling for efficiency.
#
def get_connection():
    cnx = pymysql.connect(host='localhost',
                          user='dbuser',
                          password='dbuser',
                          db='lahman2016',
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)
    return cnx


# Closes the connection. Would implement the close/release functions for the
# connection pool.
def close_connection(cnx):
    cnx.close()


# Simple helper function for submitting a query and returning result.
# q is the query string.
# If result == True, the caller expects return data, i.e. is a SELECT.
# Otherwise no return data, i.e. UPDATE, INSERT, DELETE.
#
def run_query(q, return_result):
    print("Execution query = \n", q)
    result = None

    try:
        cnx = get_connection()

        with cnx.cursor() as cursor:
            cursor.execute(q)

            if return_result:
                df_mysql = pd.read_sql(q, cnx)
                result = df_mysql
            else:
                # Could return something else, e.g. RC.
                result = True

    # Catch the base of the pymysql exceptions. Could refine can catch subtypes individually.
    except pymysql.MySQLError as be:
        args = be.args
        print("Got exception = ", be)
        result = args

    return result

#####################################################################################################################
#
# This function has parameters
# 1. source_table
# 2. target_table
#
# It returns a set of pairs (s_column, t_column) where s_column is a column in the source table and t_column is
# the referenced foreign key column in the target table.
#
# Query template.
get_fks_q1 = "SELECT TABLE_NAME, COLUMN_NAME,CONSTRAINT_NAME,REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME "
get_fks_q1 = get_fks_q1 + " FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE "
get_fks_q1 += "WHERE TABLE_SCHEMA = 'lahman2016' AND TABLE_NAME = '"
get_fks_q2 = "' AND REFERENCED_TABLE_NAME='"
get_fks_q3 = "' AND REFERENCED_COLUMN_NAME IS NOT NULL;"


def get_foreign_keys(source_table, target_table):
    result = []
    q = get_fks_q1 + source_table + get_fks_q2 + target_table + get_fks_q3;

    print("Q = ", q)
    r = run_query(q, True)

    s_keys = list(r['COLUMN_NAME'])
    t_keys = list(r['REFERENCED_COLUMN_NAME'])
    for i in range(0, len(s_keys)):
        result.append([s_keys[i], t_keys[i]])

    print("Result = \n", result)


#####################################################################################################################
#
# This function returns the primary key columns in order for a table.
#
show_pk_q_1 = "SHOW KEYS FROM "
show_pk_q_2 = " WHERE key_name = 'PRIMARY'"


def get_primary_key(table):
    result = []
    q = show_pk_q_1 + table + show_pk_q_2
    print("Q = ", q)
    r = run_query(q, True)
    result = r.sort_values(by='Seq_in_index', ascending=True)

    cols = list(result['Column_name'])
    result = cols

    print("Result = ", result)
    return result


#####################################################################################################################
#
#
def get_by_template(table, fields, template):

    if fields is None:
        fields = "*"

    q = "SELECT " + fields + " FROM " + table + " WHERE "

    count = len(template)
    for i in range(0, count):
        term = template[i]
        q += term["column"] + "='" + term["value"] + "' "
        if i < count-1:
            q += " AND "

    r = run_query(q, True)
    print("r = ", r)
    return r

w = []
w.append({"column": "playerid", "value": "willite01"})
#w.append({"column": "yearid", "value": "1959"})

get_by_template("batting", "yearID,stint,teamid,H", w)

