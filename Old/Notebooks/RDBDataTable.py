import pymysql
import copy         # Copy data structures.
import pymysql.cursors
import json
from operator import itemgetter


max_rows_to_print = 10;

cursorClass = pymysql.cursors.DictCursor;
charset = 'utf8mb4';
max_rows_to_show = 5


class RDBDataTable:

    def __init__(self, t_name, t_file, key_columns, connect_info):
        self.table_name = t_name
        self.table_file = t_file
        self.key_columns = key_columns
        self.modified = False
        self.columns = None
        self.rows = None
        self.derived = False

        if connect_info is not None:
            self.cnx = pymysql.connect(host=connect_info['host'],
                                  user=connect_info['user'],
                                  password=connect_info['pw'],
                                  db=connect_info['db'],
                                  charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor)
        else:
            self.derived = True

    def run_q(self, q, fetch=False):
        """

        :param q: The query string to run.
        :param fetch: True if this query produces a result and the function should perform and return fetchall()
        :return:
        """
        cursor = self.cnx.cursor()
        cursor.execute(q)
        if fetch:
            result = cursor.fetchall()
            return result

    # Get the names of the columns
    def get_column_names(self):
        q = "show columns from " + self.table_file
        result = self.run_q(q, True)
        result = [r['Field'] for r in result]
        return list(result)

    def get_no_of_rows(self):
        q = "select count(*) as count from " + self.table_file
        result = self.run_q(q, True)
        result = result[0]['count']
        return result

    def get_key_columns(self):
        q = "show keys from " + self.table_file
        result = self.run_q(q, True)
        keys = [(r['Column_name'], r['Seq_in_index']) for r in result]
        keys = sorted(keys, key=itemgetter(1))
        keys = [k[0] for k in keys]
        return keys

    def __str__(self):
        result = "Table name: {}, File name: {}, No of rows: {}, Key columns: {}"
        row_count = None
        columns = None
        key_names = None

        # Some of the values are not defined for a derived table. We will implement support for
        # derived tables later.
        if self.table_file:
            row_count = self.get_no_of_rows()
            columns = self.get_column_names()
            key_names = self.get_key_columns()
        else:
            row_count = "DERIVED"
            columns = "DERIVED"
            key_names = "DERIVED"

        if self.table_name is None:
            self.table_name = "DERIVED"

        result = result.format(self.table_name, self.table_file, row_count, key_names) + "\n"
        result += "Column names: " + str(columns)

        q_result = []
        if row_count != "DERIVED":
            if row_count <= max_rows_to_print:
                q_result = self.find_by_template(None, fields=None, limit=None, offset=None)
            else:
                q_result = self.find_by_template(None, fields=None, limit=5)

        result += "\n First few rows: \n"
        for r in self.rows:
            result += str(r) + "\n"

        return result

    def template_to_where_clause(self, t):
        s = ""

        if t is None:
            return s

        for (k, v) in t.items():
            if s != "":
                s += " AND "
            s += k + "='" + v + "'"

        if s != "":
            s = "WHERE " + s;

        return s


    def find_by_template(self, t, fields=None, limit=None, offset=None):
        w = self.template_to_where_clause(t)
        cursor = self.cnx.cursor()
        if fields is None:
            fields = ['*']
        q = "SELECT " + ",".join(fields) + " FROM " + self.table_file + " " + w
        if limit is not None:
            q += " limit " + str(limit)
        if offset is not None:
            q += " offset " + offset

        print("Query = ", q)
        cursor.execute(q);
        r = cursor.fetchall()
        result = self.table_from_rows("SELECT", None, None, r)
        # print("Query result = ", r)
        return result

    def ten_greatest(self):
        q = "SELECT \
                Batting.playerID, \
                (SELECT People.nameFirst FROM People WHERE People.playerID=Batting.playerID) AS first_name, \
                (SELECT People.nameLast FROM People WHERE People.playerID=Batting.playerID) AS last_name, \
                sum(Batting.h)/sum(batting.ab) AS career_average, \
                sum(Batting.h) AS career_hits, \
                sum(Batting.ab) AS career_at_bats,\
                min(Batting.yearID) AS first_year, \
                max(Batting.yearID) AS last_year \
                FROM \
                Batting \
                GROUP BY \
                playerId \
                HAVING \
                career_at_bats > 200 AND last_year >= 1960 \
                ORDER BY \
                career_average DESC \
                LIMIT 10;"

        cursor = self.cnx.cursor()
        cursor.execute(q)
        result = cursor.fetchall()
        return result

    def delete(self, template):

        where_clause = self.template_to_where_clause(template)
        q1 = "delete from " + self.t_file + " " + where_clause + ";"
        q2 = "select row_count() as no_of_rows_deleted;"
        cursor = self.cnx.cursor()
        cursor.execute(q1)
        cursor.execute(q2)
        result = cursor.fetchone()
        self.cnx.commit()
        return result

    def insert(self, row):
        keys = row.keys()
        q = "INSERT into " + "foo" + " "
        s1 = ["%s"] * len(keys)
        s1 = ",".join(s1)

        q += "(" + s1 + ") "

        v = ["%s"] * len(keys)
        v = ",".join(v)

        q += "values(" + v + ")"

        params = tuple(keys) + tuple(row.values())

        print(params)

        print(q)

    # Create a new table from a list of rows.
    @staticmethod
    def table_from_rows(t_name, t_file, key_columns, rows):
        result = RDBDataTable(t_name, t_file, key_columns, None)  # Create tge table.
        if rows is None:  # Add a copy of rows if it exists.
            return result
        result.rows = copy.copy(rows)
        result.columns = list(result.rows[0].keys())
        return result


def test1():
    rt = RDBDataTable("Test", "People", ['playerID'],
                      connect_info = {"host": "localhost", "user": "dbuser",
                        "pw": "dbuser", "db": "lahman2017"})
    result = rt.find_by_template({"nameLast" : "Williams"})
    print("Result = ", result)

test1()







