import os
import psycopg2
import re
import time
import subprocess

DBHOSTNAME = os.environ['DBHOSTNAME']
USER = os.environ['USER']
DATABASE = os.environ['DATABASE']
PASSWORD = os.environ['PASSWORD']

conn = psycopg2.connect(host=DBHOSTNAME, database=DATABASE, user=USER, password=PASSWORD)
cur = conn.cursor()

prevs = []
# Jeremy and Noah = 3
# Michael and Nitzan = 6
# Michelle and Hailey = 9
# faustino =

# query = """
#     SELECT * FROM Compilations
#     WHERE group_id=6
#     ORDER BY time
# """
# query = """
#     SELECT group_id, students, COUNT(*) as cnt
#     FROM Compilations, Groups
#     WHERE Compilations.group_id = Groups.id
#     GROUP BY group_id, students
#     ORDER BY cnt DESC
# """
# query = """
#     SELECT students[1], students[2], code, output, error, time
#     FROM Compilations, Groups
#     WHERE Groups.id = """ + str(16) + """
#     AND Groups.id = Compilations.group_id
#     ORDER BY Compilations.id
# """
# cur.execute(query)
# res = cur.fetchall()
# f = open("data_analysis/felix/-1.py", 'w+')
# for x in range(len(res)):
#     f = open("data_analysis/felix/" + str(x) + ".py", 'w+')
#     to_write = res[x][2]
#     f.write(to_write)
#     f.close()
#
# lines_diff = []
# for x in range(1 + len(res)):
#     cmd = """diff -y --suppress-common-lines data_analysis/jeremy/""" + str(x-1) + """.py data_analysis/jeremy/""" + str(x) + """.py"""
#     process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
#     output, error = process.communicate()
#     lines_diff.append(len(re.findall(r'\\n', str(output))))
#
# print(lines_diff)

    # for x in res:
        # print("=========start=========")
        # print(x)
        # print("=========-end-=========")
        # print("\n")

query = """
SELECT * FROM Groups
"""

cur.execute(query)
res = cur.fetchall()
print(res)
