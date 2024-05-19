import sqlite3
conn = sqlite3.connect("images.sqlite")

cursor = conn.cursor()

sql_query = """
CREATE TABLE images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(250) NOT NULL,
    url VARCHAR(250) NOT NULL
)
"""

cursor.execute(sql_query)
conn.commit()
conn.close()
