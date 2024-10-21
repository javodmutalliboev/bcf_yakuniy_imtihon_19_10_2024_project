import mysql.connector


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="javod",
            password="hHh(26Y2%C~w",
            database="bcf_yakuniy_imtihon_19_10_2024_project",
        )
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, a, b, c):
        self.conn.close()


if __name__ == "__main__":
    with Database() as db:
        db.cursor.execute("SELECT * FROM students;")
        for student in db.cursor.fetchall():
            print(student)
