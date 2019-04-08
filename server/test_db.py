import os
import psycopg2
import re

DBHOSTNAME = 'localhost'
USER = 'postgres'
DATABASE = 'testdb'
PASSWORD = os.environ['ramen']

code = "print('hello')"
code.replace("'", "\\\'")


conn = psycopg2.connect(host=DBHOSTNAME, database=DATABASE, user=USER, password=PASSWORD)
cur = conn.cursor()
cur.execute("""
    INSERT INTO Code_Iterations VALUES (
        DEFAULT, 1, '""" + code + """', now()
    )
""")
conn.commit()
# cur.execute("""
#     SELECT code
#     FROM Code_Iterations
#     WHERE id=39
# """)
# res = cur.fetchall()
# print(res[0][0])
