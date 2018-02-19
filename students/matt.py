import pymysql
import pandas as pd


# Connect
def get_connection():
    cnx = pymysql.connect(host='localhost',
                          user='dbuser',
                          password='dbuser',
                          db='lahman2016',
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)
    return cnx


def run_query(q, result):
    print("Execution query = \n", q)

    cnx = get_connection()

    with cnx.cursor() as cursor:
        cursor.execute(q)
        cnx.commit()
        cnx.close()

    if (result):
        cnx = get_connection()
        df_mysql = pd.read_sql(q, cnx)
        cnx.commit()
        cnx.close()
        return df_mysql
    else:
        return True


get_fks_q1 = "SELECT TABLE_NAME, COLUMN_NAME,CONSTRAINT_NAME,REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME "
get_fks_q1 = get_fks_q1 + " FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE "
get_fks_q1 += "WHERE TABLE_SCHEMA = 'lahman2016' AND TABLE_NAME = '"
get_fks_q2 = "' AND REFERENCED_COLUMN_NAME IS NOT NULL;"


def get_foreign_keys(table_name):
    q = get_fks_q1 + table_name + get_fks_q2
    print("Q = ", q)
    # q = "select * from master where nameLast='Williams'"
    r = run_query(q, True)
    print("result =\n", r)


get_foreign_keys("Batting")