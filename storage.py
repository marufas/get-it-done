import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Storage:
    def __init__(self):
        self.db = sqlite3.connect('data.db', check_same_thread=False)
        self.db.row_factory = dict_factory
        self.cur = self.db.cursor()

    def _create_bucket_table(self):
        self.cur.execute("""CREATE TABLE buckets (
            id TEXT,
            name TEXT,
            parent TEXT
        )""")
        self.db.commit()

    def _create_task_table(self):
        self.cur.execute("""CREATE TABLE tasks (
            id TEXT,
            name TEXT,
            priority INTEGER,
            bucket_id TEXT,
            project_id TEXT,
            date_added TEXT,
            date_closed TEXT,
            complete BOOL,
            comments TEXT
        )""")
        self.db.commit()


    def add_bucket(self, id, name, parent=""):
        if self.get_bucket(id):
            return
        cmd = "INSERT INTO buckets VALUES (?, ?, ?)"
        self.cur.execute(cmd, [str(id), str(name), str(parent)])
        self.db.commit()

    def get_bucket(self, id):
        cmd = "SELECT * FROM buckets WHERE id=?"
        self.cur.execute(cmd, [str(id)])
        return self.cur.fetchone()

    def update_bucket(self, id, name=None, parent=None):
        with self.db:
            if name is not None:
                cmd = """UPDATE buckets SET name = ? 
                    WHERE id = ? """
                self.cur.execute(cmd, [str(name), str(id)])
            if parent is not None:
                cmd = """UPDATE buckets SET parent = ? 
                    WHERE id = ? """
                self.cur.execute(cmd, [str(parent), str(id)])

    def delete_bucket(self, id):
        with self.db:
            cmd = """DELETE from buckets WHERE id = ? """
            self.cur.execute(cmd, [str(id)])

    def get_all_buckets(self):
        cmd = "SELECT * FROM buckets"
        self.cur.execute(cmd)
        all_buckets = self.cur.fetchall()
        return all_buckets

    def get_tasks(self, bucket_id=None, project_id=None):
        tasks = []
        if bucket_id is not None:
            cmd = "SELECT * FROM tasks WHERE bucket_id=?"
            self.cur.execute(cmd, [str(bucket_id)])
            tasks.extend(self.cur.fetchall())
        if project_id is not None:
            cmd = "SELECT * FROM tasks WHERE project_id=?"
            self.cur.execute(cmd, [str(project_id)])
            tasks.extend(self.cur.fetchall())
        return tasks


if __name__ == "__main__":
    db = Storage()
    # db._create_bucket_table()
    # db.add_bucket("0", "In basket")
    # db.add_bucket("1", "ToDo")
    # db.add_bucket("2", "Waiting for someone")
    # db.add_bucket("3", "Scheduled")
    # db.add_bucket("4", "Reference")
    # db.add_bucket("5", "Someday/Maybe")
    # db.add_bucket("6", "Generic", "1")
    db.add_bucket("10", "Test", "2")
    print(db.get_all_buckets())
    db.update_bucket("10", "testo")
    print(db.get_all_buckets())
    db.delete_bucket("10")
    print(db.get_all_buckets())