import sqlite3

"""Testing query for DB"""


def execute_query(sql_file: str) -> list:
    with open(sql_file, "r") as f:
        sql = f.read()

    with sqlite3.connect("university.db") as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


if __name__ == "__main__":
    print(execute_query("query_10.sql"))
