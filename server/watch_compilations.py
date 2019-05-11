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

query = """
    SELECT time
    FROM Code_Iterations
    WHERE group_id = 3
    ORDER BY time
"""

cur.execute(query)
res = cur.fetchall()
first_time = res[0][0]

# 3, 6, 7, 9, 16
for i in [6]:
    prev_chars = []
    times = []

    cur.execute("""
        SELECT time
        FROM Code_Iterations
        WHERE group_id = """ + str(i) + """
        ORDER BY time
    """)
    res = cur.fetchall()
    first_time = res[0][0]

    cur.execute("""
        SELECT students[1], students[2], code, output, error, time
        FROM Compilations, Groups
        WHERE Groups.id = """ + str(i) + """
        AND Groups.id = Compilations.group_id
        ORDER BY Compilations.id
    """)
    res = cur.fetchall()
    prev_char = 0
    com_num = 0
    prev_time = first_time
    for x in res:
        print(chr(27) + "[2J")
        print("Students:", x[0], x[1])
        print("Timestamp:", x[5])
        print("Time:", x[5] - first_time)
        print()
        print("Char Diff (since last compilation):", len(x[2]) - prev_char)
        print("Compilation No.", str(com_num) + "/" + str(len(res) - 1), "\tLast compilation",
                (x[5] - prev_time).total_seconds(), "s ago.")
        prev_chars.append(len(x[2]) - prev_char)
        times.append(x[5])
        # prev_times.append(x[5] - prev_time)
        prev_char = len(x[2])
        prev_time = x[5]

        print("=============================start==============================")
        print(x[2])
        print("==============================end===============================")
        print(x[3][0:30])
        print(x[4][2:-1])
        com_num += 1
        input()

    # f = open("data_analysis/" + x[0] + "_" + x[1] + ".csv", 'w+')
    # to_write = ""
    # for x in times:
    #     to_write += str((x - first_time).total_seconds()) + ","
    # f.write(to_write[:-1] + "\n")
    #
    # to_write = ""
    # for x in prev_chars:
    #     to_write += str(x) + ","
    # f.write(to_write[:-1] + "\n")
    # f.close()
