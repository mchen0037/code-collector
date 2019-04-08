
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

# This is to spawn a process
def spawn(code, userInput):
    global result
    global output
    global error

    f = open('code.py', 'w')
    f.write(code)
    f.close()

    f = open('input.txt', 'w')
    f.write(userInput)
    f.close()

    result = Popen("python code.py < input.txt", stdout=PIPE,
                stdin=PIPE, stderr=PIPE, shell=True, preexec_fn=os.setsid)
    output, error = result.communicate()

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
        userInput = STORE["input"]

        # if (code.find("import") != -1):
        #     noImports = 1
        # Start up the process in a new thread
        # else:
            # code = "from light import *\n" + code
        t = Thread(target=spawn, args=(code, userInput))
        t.start()

        return "RUNNING"


@app.route("/output")
def getOutput():
    global output
    global error
    global result
    # global noImports
    # if (noImports == 1):
    #     return "NO IMPORTS"
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
            return output + error
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

    return "Success!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
