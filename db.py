import sqlite3 as sl
def get_con():
    con = sl.connect('off-flix.db')
    return con

# with con:
#     con.execute("""
#         CREATE TABLE seasons (
#             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#             title TEXT,
#             path TEXT,
#             description TEXT
#         );
#     """)

# with con:
#     con.execute("""CREATE TABLE episodes (
#             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#             path TEXT,
#             watched TINYINT,
#             thumbnail TEXT
#         );
#     """)
# sql = 'INSERT INTO episodes (path, watched, thumbnail) values(?, ?, ?)'
# data = [
#     ('D:\\Seasons\\FRIENDS', 1, "Sitcom")
# ]

# with con:
#     con.executemany(sql, data)



def create_tables():
    con = get_con()

    data = con.execute("PRAGMA table_info([seasons])")
    data = data.fetchall()
    if data == []:
        with con:
            con.execute("""
                CREATE TABLE seasons (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    path TEXT UNIQUE,
                    current_part INTEGER,
                    poster TEXT
                );
            """)

    data = con.execute("PRAGMA table_info([episodes])")
    data = data.fetchall()
    if data == []:
        with con:
            con.execute("""
                CREATE TABLE episodes (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    path TEXT,
                    title TEXT,
                    watched TINYINT,
                    thumbnail TEXT,
                    duration TEXT,
                    season INTEGER,
                    part INTEGER,
                    FOREIGN KEY (season) REFERENCES seasons(id),
                    FOREIGN KEY (part) REFERENCES parts(id)
                );
            """)
    
    data = con.execute("PRAGMA table_info([parts])")
    data = data.fetchall()
    if data == []:
        with con:
            con.execute("""
                CREATE TABLE parts (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    path TEXT,
                    title TEXT,
                    season INTEGER,
                    FOREIGN KEY (season) REFERENCES seasons(id)
                );
            """)
if __name__ == "__main__":     

    con = get_con()
    with con:
        create_tables()
        data = con.execute("PRAGMA table_info([parts])")
        data = data.fetchall()
        print(data == [])
        for row in data:
            print(row)

    # create_tables()