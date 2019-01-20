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

def get_batch(last_offset, batch_size):
    cur = default_cnx.cursor()
    q = "select * from consumer_complaints limit " + str(batch_size) + " offset " + str(last_offset)
    cur.execute(q)
    result = cur.fetchall()
    return result

def simple_reduce(column_name, threshold, batch_size):

    value_count = dict()

    done = False
    last_offset = 0;

    while not done:

        batch = get_batch(last_offset, batch_size)

        if batch is None or len(batch) == 0:
            done = True
        else:
            for r in batch:
                value = r[column_name]
                slot = value_count.get(value, None)
                if slot is None:
                    value_count[value] = 1
                else:
                    value_count[value] += 1

        print("Processed from ", last_offset, " to ", last_offset+batch_size)
        last_offset += batch_size

    return value_count

result = simple_reduce('Company', None, 100)

df = pd.DataFrame.from_dict(result)

print(df)