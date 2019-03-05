import CSVTable
import json
import copy


def test1():

    csvt = CSVTable.CSVTable("Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"])
    csvt.load()
    print("Table = ", csvt)

#test1()

def test2():
    csvt = CSVTable.CSVTable("Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"])
    csvt.load()
    r = csvt.find_by_template({"playerID" : "willite01", "yearID": "1960"})
    print("Result = ", json.dumps(r, indent=2))

#test2()

def test3():
    csvt = CSVTable.CSVTable("Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"])
    csvt.load()
    r = csvt.find_by_template({"teamID": "BOS", "yearID": "1960"}, ['playerID', 'HR', 'H', 'AB'])
    rows = r.rows
    print(json.dumps(rows, indent=2))

#test3()

'''
try:
    csvt = CSVTable.CSVTable("Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"])
    csvt.load();
    t6 = { "playerID": "willite01"}
    result = csvt.find_by_template(t6)
    print("Query result is ")
    print(json.dumps(result, indent=2))
except Exception as e:
    print("Got exception = ", str(e))
'''

def test4():
    csvt = CSVTable.CSVTable("Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"])
    csvt.load()
    r = csvt.find_by_primary_key(['willite01', '1960', 'BOS', '1'], ['playerID', 'yearID','H', 'AB'])
    print("r = ", json.dumps(r, indent=2))

#test4()

#test3()

def test5():
    csvt = CSVTable.CSVTable("Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"])
    csvt.load()

    result = csvt.find_by_primary_key(['dff9', '2004', 'BOS', "1"])
    print("After find 1, result = ", result)

    new_row = { "playerID": "dff9", "yearID": "2004", "teamID": "BOS", "stint": "1", "H": "300"}
    csvt.insert(new_row)

    result = csvt.find_by_primary_key(['dff9', '2004', 'BOS', "1"])
    print("After find 2, result = ", result)

    try:
        new_row = {"playerID": "dff9", "yearID": "2004", "teamID": "BOS", "stint": "1", "H": "300", "AB": "500"}
        csvt.insert(new_row)
    except ValueError as ve:
        print("Got a value error on insert, = ", ve)


def test6():
    csvt = CSVTable.CSVTable("Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"])
    csvt.load()
    print("CSV Table = ", csvt)
    result = csvt.find_by_template({ "playerID": "willite01", "yearID": "1960"}, ['playerID', 'H', 'AB'])
    print("Result = ", result)


def test8():
    csvt = CSVTable.CSVTable("Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"])
    csvt.load()
    print("CSV Table = ", csvt)
    result = csvt.find_by_template({"playerID": "willite01", "yearID": "1960"}, ['playerID', 'H', 'AB'])
    print("Result 1 = ", result)
    result.insert({"playerID": "DFF1", "H": "100", "AB": "100"})
    print("After insert, resylt = ", result)

def test9():
    csvt = CSVTable.CSVTable("Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"])
    csvt.load()
    #print("CSV Table = ", csvt)
    csvt.create_index(['playerID'])
    print("indexes = ", csvt.indexes)
    print("rows = ", csvt.rows)
    #result = csvt.find_by_template({"playerID": "willite01", "yearID": "1960"}, ['playerID', 'H', 'AB'])
    #print("Result 1 = ", result)
    #result.insert({"playerID": "DFF1", "H": "100", "AB": "100"})
    #print("After insert, resylt = ", result)

test9()

