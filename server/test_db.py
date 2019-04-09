import os
import psycopg2
import re

# DBHOSTNAME = 'localhost'
# USER = 'postgres'
# DATABASE = 'testdb'
# PASSWORD = os.environ['ramen']
DBHOSTNAME = os.environ['DBHOSTNAME']
USER = os.environ['USER']
DATABASE = os.environ['DATABASE']
PASSWORD = os.environ['PASSWORD']


code = "print('hello')"
code.replace("'", "\\\'")


conn = psycopg2.connect(host=DBHOSTNAME, database=DATABASE, user=USER, password=PASSWORD)
cur = conn.cursor()
cur.execute("""
    SELECT code FROM Code_Iterations
    WHERE group_id=17
""")
res = cur.fetchall()
for x in res:
    print(x[0])
    input()
# conn.commit()
# cur.execute("""
#     SELECT code
#     FROM Code_Iterations
#     WHERE id=39
# """)
# res = cur.fetchall()
# print(res[0][0])
