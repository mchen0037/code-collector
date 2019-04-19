import os
import psycopg2
import re
import time

DBHOSTNAME = os.environ['DBHOSTNAME']
USER = os.environ['USER']
DATABASE = os.environ['DATABASE']
PASSWORD = os.environ['PASSWORD']

conn = psycopg2.connect(host=DBHOSTNAME, database=DATABASE, user=USER, password=PASSWORD)
cur = conn.cursor()

for i in range(3, 4):
    cur.execute("""
        SELECT students[1], students[2], code, time
        FROM Code_Iterations, Groups
        WHERE Code_Iterations.group_id=""" + str(i) + """
        AND Groups.id = Code_Iterations.group_id
        ORDER BY Code_Iterations.id
    """)
    res = cur.fetchall()
    for x in res:
        print(chr(27) + "[2J")
        print("Students:", x[0][0:3], x[1][0:3])
        print("Time:", x[3])
        print("=============================start==============================")
        print(x[2])
        print("==============================end===============================")
        time.sleep(0.1)
    time.sleep(3)
