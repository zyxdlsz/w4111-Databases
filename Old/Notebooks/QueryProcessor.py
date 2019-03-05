
class QueryProcessor:

    def __init__(self, tables, constraints=None):
        self.tables = tables
        self.constraints = constraints

        for t in self.tables.values():
            t.load()

    def find_by_query(self, q):
        tn = q["table_name"]
        tmp = q["template"]
        ff = q.get("fields", None)

        tbl = self.tables[tn]
        result = tbl.find_by_template(tmp, ff)
        return result

    def insert(self, t_name, row):

        for c in self.constraints:
            if c['source_table'] == t_name:
                self.check_insert_constraint(t_name, row, c)
        else:
            tbl = self.tables[t_name]
            tbl.insert(row)
            tbl.save()

    def delete(self, t_name, tmpl):
        for c in self.constraints:
            if c['target_table'] == t_name:
                self.check_delete_constraint(t_name, tmpl, c)
        else:
            tbl = self.tables[t_name]
            tbl.delete(tmpl)
            tbl.save()

    def check_insert_constraint(self, t_name, row, c):
        target_table = c['target_table']
        target_attribute = c['target_attribute']
        source_value = row[c['source_attribute']]
        target_tbl = self.tables[target_table]
        target_value = row[c['source_attribute']]

        tmpl = { target_attribute: target_value}
        target_row = target_tbl.find_by_template(tmpl)

        if target_row == []:
            raise ValueError("Constraint violation.")

    def check_delete_constraint(self, t_name, tmpl, c):

        # The table from which we will delete the rows.
        tbl = self.tables[t_name]
        # The candidates for deletion.
        candidates = tbl.find_by_template(tmpl)

        # This is the source table for the constraint, i.e. the
        # referencing table.
        source_table = self.tables[c['source_table']]

        # The name of the attribute referenced in the target table.
        t_attribute_name = c['target_attribute']

        # For every row that we might delete.
        for cand in candidates:
            # The test is:
            # We want to see if there is a row in the source table
            # with source_attribute name from the constraint and the
            # value of the target_attribute name.
            test_tmpl = { c['source_attribute']: cand[t_attribute_name]}

            # If there is one, this is an error.
            results = source_table.find_by_template(test_tmpl)
            if len(results) > 0:
                raise ValueError("Constraint violation.")

