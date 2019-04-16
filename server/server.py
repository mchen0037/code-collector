
from flask import Flask
from flask import request
from flask import jsonify
import json
# from light.py import Light
from flask_cors import CORS

# === This stuff is needed for handling the execution of user code ===
import os
import time
from signal import signal, SIGPIPE, SIG_DFL, SIGTERM
from subprocess import Popen, PIPE, STDOUT
from threading import Thread
import psycopg2
import random
import re
signal(SIGPIPE, SIG_DFL)
# ====================================================================

app = Flask(__name__)
CORS(app)

DBHOSTNAME = os.environ['DBHOSTNAME']
USER = os.environ['USER']
DATABASE = os.environ['DATABASE']
PASSWORD = os.environ['PASSWORD']

# for local DB
# DBHOSTNAME = 'localhost'
# USER = 'postgres'
# DATABASE = 'rc-cola-local'
# PASSWORD = os.environ['ramen']

conn = psycopg2.connect(host=DBHOSTNAME, database=DATABASE, user=USER, password=PASSWORD)

# This is for killing a process that we have spawned
@app.route("/kill")
def kill():
    # print("Starting kill")
    # if program != None:
    #     print("Killing")
    #     try:
    #         os.killpg(os.getpgid(process.pid), SIGTERM)
    #         return "Process was killed."
    #     except:
    #         return 'Nothing to kill!'
    # else:
    #     return "Nothing to kill!"
    return "Broken.."

# This is to spawn a process
def spawn(code, userInput, group):
    f = open('userCode/' + str(group) + '.py', 'w+')
    f.write(code)
    f.close()

    f = open('userCode/' + str(group) + 'input.txt', 'w+')
    f.write(userInput)
    f.close()

    begin = time.time()

    tmp = Popen('python userCode/' + str(group) +
                '.py < userCode/' + str(group) + 'input.txt', stdout=PIPE,
                stdin=PIPE, stderr=PIPE, shell=True, preexec_fn=os.setsid)

    while (True and tmp.poll() == None):
        if (time.time() - begin > 5):
            tmp.kill()
            return (("", "Program took too long! Possible Infinite Loop?"))
    return tmp.communicate()

# The endpoint for uploading the code and running it
@app.route("/run", methods=['POST'])
def runcode():
    global processes
    if(request.method == "POST"):
        STORE  = json.loads(request.data)
        STORE = STORE["code"]
        code = STORE["code"]
        group = STORE["group"]
        userInput = STORE["input"]

        code = re.sub(r'import os', '', code)
        code = re.sub(r'import subprocess', '', code)
        code = re.sub(r'import shlex', '', code)
        code = re.sub(r'import commands', '', code)
        code = re.sub(r'import sh', '', code)
        print(code)
        cur = conn.cursor()
        output, error = spawn(code, userInput, group)

        ps_code = str(code).replace("'", "''")
        ps_output = str(output).replace("'", "''")
        ps_error = str(error).replace("'", "''")
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Compilations VALUES(
                DEFAULT, """ + str(group) + """,' """
                 + str(ps_code) + """', '""" + str(ps_output)
                 + """', '""" + str(ps_error)+ """', now()
            )
        """)
        conn.commit()

        return output + error

@app.route("/login", methods=['POST'])
def login():
    STORE  = json.loads(request.data)
    student_1 = STORE["st_1"]
    student_2 = STORE["st_2"]
    students = str([student_1, student_2])
    cur = conn.cursor()
    cur.execute("""
        SELECT id
        FROM Groups
        WHERE students[1] = '""" + student_1 + """'
        AND students[2] = '""" + student_2 + """'
    """)
    res = cur.fetchone()
    # if pair doesn't exist, create a new pair
    if not res:
        cur.execute("""
            INSERT INTO Groups VALUES (
                DEFAULT, ARRAY """ + students + """
            )
        """)
        conn.commit()
        cur.execute("""
            SELECT id
            FROM Groups
            WHERE students[1] = '""" + student_1 + """'
            AND students[2] = '""" + student_2 + """'
        """)
        res = cur.fetchone()
        group_id = res[0]
        return jsonify({"code": "", "group_id": group_id})
    else: # give them their code back
        group_id = res[0]
        cur.execute("""
            SELECT code FROM Code_Iterations
            WHERE group_id = """ + str(group_id) + """
            ORDER BY time DESC
            LIMIT 1
        """)
        res = cur.fetchone()
        code = res[0]
        return jsonify({"code": code, "group_id": group_id})
    print('some error..')
    return "some error.."

    return ""

@app.route("/upload", methods=['POST'])
def upload():
    STORE = json.loads(request.data)
    code = STORE['code1']
    code = code.replace("'", "''") # to escape ' in postgres, use ''
    group_id = STORE['group_id']

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Code_Iterations VALUES (
            DEFAULT, """ + str(group_id) + """
            ,'""" + str(code) + """', now()
        )
    """)
    conn.commit()
    return ""

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
