
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
signal(SIGPIPE, SIG_DFL)
result = None
output = None
error = None 
noImports = None
# ====================================================================


app = Flask(__name__)
CORS(app)

# This is for killing a process that we have spawned
@app.route("/kill")
def kill():
    global result
    global output
    print "Starting kill"
    if result != None:
        print "Killing"
        os.killpg(os.getpgid(result.pid), SIGTERM)
        output = "Process was terminated"
        return "Killed it..."
    else:
        return "Nothing to kill"

# This is to spawn a process
def spawn(code, userInput):
    global result
    global output
    global error

    f = open('userCode/code.py', 'w')
    f.write(code)
    f.close()

    f = open('userCode/input.txt', 'w')
    f.write(userInput)
    f.close()

    result = Popen("python userCode/code.py < userCode/input.txt", stdout=PIPE,
                stdin=PIPE, stderr=PIPE, shell=True, preexec_fn=os.setsid)
    output, error = result.communicate()

# The endpoint for uploading the code and running it
@app.route("/run", methods=['POST'])
def runcode():
    # Reset all the global variables every time the user submits code
    global output
    global error
    global result
    global noImports
    output = None
    error = None
    result = None
    if(request.method == "POST"):

        STORE  = json.loads(request.data)
        STORE = STORE["code"]
        code = STORE["code"]
        userInput = STORE["input"]

        if (code.find("import") != -1):
            noImports = 1
        # Start up the process in a new thread
        else:
            code = "from light import *\n" + code
            t = Thread(target=spawn, args=(code, userInput,))
            t.start()

        return "RUNNING"


@app.route("/output")
def getOutput():
    global output
    global error
    global result
    global noImports
    if (noImports == 1):
        return "NO IMPORTS"
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
    


if __name__ == '__main__':
        app.run(host="0.0.0.0", port=5000)
