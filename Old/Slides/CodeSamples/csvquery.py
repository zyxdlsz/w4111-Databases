import csv as csv
import json


# This function takes two dictionary inputs
# 1. Row is a row from the CSV file.
# 2. Template is contains a set of (field name, value) pairs.
# The function returns true if for every (field name, value) pair
# the corresponding (field name, value) pair matches on value.
#
def matches_template(row, template):
    match = True;
    for field, value in template.items():
        rowvalue = row[field]
        if (rowvalue != value):
            return False;
    return match


# The function has the following parameters
# 1. The "name" of a collection of data
# 2. A template that is a dictionary of (name, value) pairs.
# The function returns a list containing all rows from the file
# that match the template.
def query_collection(c, t):
    r = []
    f = '../DataAndSchema/' + c + '.csv'
    with open(f, 'r') as csvfile:
        player_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in player_reader:
            if (matches_template(row, t)):
                r.append(row)
    return r


# { "collection": "Master", "nameLast" : "Williams", "throws" : "R", "bats" : "L"}
# { "collection" : "Batting", "playerID" : "addybo01"}

t = input("Please enter your query template: ")
t = json.loads(t)
print("Template = ", t)
print("\n\nThe players matching template t = ", t, " are:\n")
collection = t["collection"]
del t["collection"]
result = query_collection(collection, t)
#{ "collection" : "Master", "nameLast" : "Williams", "throws" : "R"}result = json.loads(result)
print("Result = ", json.dumps(result, indent=2))
print("\n\n")
