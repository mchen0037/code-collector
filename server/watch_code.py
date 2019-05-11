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

prevs = []
for i in [16]:
    cur.execute("""
        SELECT students[1], students[2], code, time
        FROM Code_Iterations, Groups
        WHERE Groups.id = """ + str(i) + """
        AND Groups.id = Code_Iterations.group_id
        ORDER BY Code_Iterations.id
    """)
    res = cur.fetchall()
    prev = 0
    first_time = res[0][3]
    for x in res:
        print(chr(27) + "[2J")
        print("Students:", x[0], x[1])
        print("Timestamp:", x[3])
        print("Time:", x[3] - first_time)
        print("Char Diff:", len(x[2]) - prev)
        prevs.append(len(x[2]) - prev)
        prev = len(x[2])
        print("=============================start==============================")
        print(x[2])
        print("==============================end===============================")
        input()
        # time.sleep(0.2)
    # time.sleep(3)
print(prevs)
