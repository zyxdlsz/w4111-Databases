import Examples.SQLHelper as SQLHelper
import json

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def t1():

    sql = "select * from lahman2019raw.people where nameLast=%s and birthCity=%s"
    args = ('Williams', 'San Diego')

    result = SQLHelper.run_q(sql, args, fetch=True)

    print("Return code = ", result[0])
    print("Data = ")
    if result[1] is not None:
        print(json.dumps(result[1], indent=2))
    else:
        print("None.")

def t2():

    table_name = "lahman2019raw.people"
    fields = ['nameLast', 'nameFirst', 'birthYear', 'birthState', 'birthMonth']
    template = { "nameLast": "Williams", "birthCity": "San Diego"}
    sql, args = SQLHelper.create_select(table_name, template, fields)
    print("SQL = ", sql, ", args = ", args)

    result = SQLHelper.run_q(sql, args)
    if result[1] is not None:
        print(json.dumps(result[1], indent=2))
    else:
        print("None.")

def t3():

    table_name = "classicmodels.offices"
    row = {
        "officeCode": "13",
        "city": "Minas Tirith",
        "state": "Minas Tirith",
        "addressLine1": "23 Level 3",
        "phone": "Palatir",
        "country": "Gondor",
        "postalCode": "12345",
        "territory": "ME"
    }

    sql, args = SQLHelper.create_insert(table_name, row)
    print("SQL = ", sql, ", args = ", args)

    result = SQLHelper.run_q(sql, args, fetch=False, commit=True)
    if result[1] is not None:
        print(json.dumps(result[1], indent=2))
    else:
        print("None.")

def t4():

    table_name = "classicmodels.offices"
    new_cols = {
        "city": "Minas Morgul",
        "state": "Morgul Vale",
        "addressLine1": "1 Shelob Cave",
        "phone": "Ick",
        "country": "Mordor",
        "postalCode": "66666"
    }

    template = { "city": "Minas Tirith", "state": "Minas Tirith"}

    sql, args = SQLHelper.create_update(table_name, new_cols, template)
    print("SQL = ", sql, ", args = ", args)

    result = SQLHelper.run_q(sql, args, fetch=False, commit=True)
    if result[1] is not None:
        print(json.dumps(result[1], indent=2))
    else:
        print("None.")


#t1()
#t2()
#t3()
t4()