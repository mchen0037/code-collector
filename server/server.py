
from flask import Flask
from flask import request
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
result = None
output = None
error = None
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

# poo = (str(['george', 'watsky']))
# print(type(poo))
conn = psycopg2.connect(host=DBHOSTNAME, database=DATABASE, user=USER, password=PASSWORD)
# cur = conn.cursor()
# cur.execute("""
#     INSERT INTO Groups VALUES (
#         DEFAULT, ARRAY """ + poo + """
#     )
# """)
# conn.commit()
# print(result)

# This is for killing a process that we have spawned
@app.route("/kill")
def kill():
    global result
    global output
    print("Starting kill")
    if result != None:
        print("Killing")
        try:
            os.killpg(os.getpgid(result.pid), SIGTERM)
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
    global result
    global output
    global error


    f = open('userCode/' + str(group) + '.py', 'w+')
    f.write(code)
    f.close()

    f = open('userCode/' + str(group) + 'input.txt', 'w+')
    f.write(userInput)
    f.close()

    result = Popen('python userCode/' + str(group) +
                '.py < userCode/' + str(group) + 'input.txt', stdout=PIPE,
                stdin=PIPE, stderr=PIPE, shell=True, preexec_fn=os.setsid)
    output, error = result.communicate()

    postgres_out = output.decode('utf-8')
    postgres_error = error.decode('utf-8')

    postgres_code = str(code).replace("'", "''") # to escape ' in postgres, use ''
    postgres_out = str(postgres_out).replace("'", "''")
    postgres_error = str(postgres_error).replace("'", "''")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Compilations VALUES(
            DEFAULT, """ + str(group) + """,' """
             + str(postgres_code) + """', '""" + str(postgres_out)
             + """', '""" + str(postgres_error)+ """', now(), """
             + """'""" + str(ticket) + """'
        )
    """)
    conn.commit()

# The endpoint for uploading the code and running it
@app.route("/run", methods=['POST'])
def runcode():
    # Reset all the global variables every time the user submits code
    global output
    global error
    global result
    # global noImports
    output = None
    error = None
    result = None
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
    # global output
    # global error
    # global result
    ticket = request.args.get('ticket')

    temp = None
    errFlag = False
    # Make sure the process has started
    # Wait for it if it has not
    while result == None:
        time.sleep(0.1)
    # We will wait 5 seconds, checking at 0.1 second intervals
    for i in range(1200):
        # The process has terminated, there should be output and/or an error
        if result.poll() != None:
            cur = conn.cursor()
            cur.execute("""
                SELECT output, error FROM Compilations
                WHERE ticket='""" + ticket + """'
            """)
            output, error = cur.fetchone()
            output = bytes(output, 'utf-8')
            error = bytes(error, 'utf-8')
            print(output)
            return output + error
            # return output + error
        time.sleep(0.1)

    # We have waited 5 seconds now, check if the process is still alive
    proc = result.poll()

    # If proc is None, it means it is still alive
    # If the process has completed, proc will have some integer value, like 0
    if proc == None:
        kill()
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
    result = cur.fetchone()
    print(result[0])

    # return the id of the group
    return str(result[0])

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
