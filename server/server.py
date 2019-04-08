
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
import string
import random
signal(SIGPIPE, SIG_DFL)
processes = {}
output = {}
error = {}
# ====================================================================

app = Flask(__name__)
CORS(app)

DBHOSTNAME = os.environ['DBHOSTNAME']
USER = os.environ['USER']
DATABASE = os.environ['DATABASE']
PASSWORD = os.environ['PASSWORD']

# for local DB
DBHOSTNAME = 'localhost'
USER = 'postgres'
DATABASE = 'testdb'
PASSWORD = os.environ['ramen']

conn = psycopg2.connect(host=DBHOSTNAME, database=DATABASE, user=USER, password=PASSWORD)

# This is for killing a process that we have spawned
@app.route("/kill")
def kill():
    global processes
    global output
    global error
    ticket = request.args.get('ticket')

    program = processes[ticket]

    print("Starting kill")
    if program != None:
        print("Killing")
        try:
            os.killpg(os.getpgid(process.pid), SIGTERM)
            return "Process was killed."
        except:
            return 'Nothing to kill!'
    else:
        return "Nothing to kill!"

# generate a random receipt like ticket for the output to query for this
# in the database, rather than relying on global variables.
def ticketGen(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# This is to spawn a process
def spawn(code, userInput, group, ticket):
    global processes
    global output
    global error
    f = open('userCode/' + str(group) + '.py', 'w+')
    f.write(code)
    f.close()

    f = open('userCode/' + str(group) + 'input.txt', 'w+')
    f.write(userInput)
    f.close()


    tmp = Popen('python userCode/' + str(group) +
                '.py < userCode/' + str(group) + 'input.txt', stdout=PIPE,
                stdin=PIPE, stderr=PIPE, shell=True, preexec_fn=os.setsid)

    processes[ticket] = tmp
    output[ticket], error[ticket] = tmp.communicate()


# The endpoint for uploading the code and running it
@app.route("/run", methods=['POST'])
def runcode():
    if(request.method == "POST"):
        STORE  = json.loads(request.data)
        STORE = STORE["code"]
        code = STORE["code"]
        group = STORE["group"]
        userInput = STORE["input"]

        cur = conn.cursor()
        # probability is low but ensure that no other copilations have the same ticket value
        while (True):
            ticket = ticketGen()
            cur.execute("""
                SELECT ticket FROM Compilations WHERE ticket='""" + ticket + """'
            """)
            res = cur.fetchall()
            if not res: #check for empty list
                break
            print("Ticket already exists! Generating a new one...")
        t = Thread(target=spawn, args=(code, userInput, group, ticket))
        t.start()

        return ticket


@app.route("/output")
def getOutput():
    global processes
    global output
    global error

    ticket = request.args.get('ticket')
    program = processes[ticket]

    # Make sure the process has started
    # Wait for it if it has not
    while program == None:
        time.sleep(0.1)
    # We will wait 5 seconds, checking at 0.1 second intervals
    for i in range(1200):
        # The process has terminated, there should be output and/or an error
        if program.poll() != None:
            if ticket in processes:
                out = output[ticket]
                err = error[ticket]
                del processes[ticket]
                del output[ticket]
                del error[ticket]
            return out + err
        time.sleep(0.1)

    # We have waited 5 seconds now, check if the process is still alive
    proc = program.poll()

    # If proc is None, it means it is still alive
    # If the process has completed, proc will have some integer value, like 0
    if program == None:
        kill(program)
        return "Taking too long..."

    return "This line should never be executed..."

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
    code = " "
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
        return jsonify({"code": code, "group_id": group_id})
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
    # print('hi')
    app.run(host="0.0.0.0", port=5000, debug=True)
