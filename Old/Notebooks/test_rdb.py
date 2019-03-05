import RDBDataTable
import json

def test_ten_greatest():
    csvt = RDBDataTable.RDBDataTable("Bunny", "People", ["playerID"])
    #x = csvt.find_by_template({"playerID": "willite01"}, ['playerID', 'nameLast', 'nameFirst'])
    x = csvt.ten_greatest()
    print(json.dumps(x, indent=2))

def test_delete_1():
    template = { "playerID" : "cat" }
    csvt = RDBDataTable.RDBDataTable("Bunny", "People", ["playerID"],
                                     { "host": "localhost", "user": "dbbuser",
                                       "pw": "dbuser", "db": "lahman2017"})
    result = csvt.delete(template)
    print("No of rows deleted = ", result)

def test4():

    connect_info = {"host": "localhost", "user": "dbuser",
    "pw": "dbuser", "db": "lahman2017"}
    csvt = RDBDataTable.RDBDataTable("Bunny", "People", ["playerID"], connect_info)

    template = { "playerID" : "willite01" }

    result = csvt.find_by_template(template, ['playerID', 'nameLast', 'nameFirst'])
    print("Result = ", result)

#test4()

def test5():

    connect_info = {"host": "localhost", "user": "dbuser",
    "pw": "dbuser", "db": "lahman2017"}
    csvt = RDBDataTable.RDBDataTable("Bunny", "People", ["playerID"], connect_info)

    template = { "playerID" : "willite01" }

    result = csvt.find_by_template(template, ['playerID', 'nameLast', 'nameFirst'])
    print("Result = ", result)


def test6():

    connect_info = {"host": "localhost", "user": "dbuser",
    "pw": "dbuser", "db": "lahman2017"}
    csvt = RDBDataTable.RDBDataTable("Bunny", "Batting", None, connect_info)

    print("Table = ", csvt)

test5()