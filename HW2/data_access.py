import dbaccess
import pandas


get_fks_q1 = "SELECT TABLE_NAME, COLUMN_NAME,CONSTRAINT_NAME,REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME "
get_fks_q1 = get_fks_q1 + " FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE "
get_fks_q1 += "WHERE TABLE_SCHEMA = 'lahman2016' AND TABLE_NAME = '"
get_fks_q2 = "' AND REFERENCED_COLUMN_NAME IS NOT NULL;"


def get_foreign_keys(table_name):
    q = get_fks_q1 + table_name + get_fks_q2
    print("Q = ", q)
    # q = "select * from master where nameLast='Williams'"
    r = dbaccess.run_query(q, True)
    print("result =\n", r)


get_foreign_keys("Batting")