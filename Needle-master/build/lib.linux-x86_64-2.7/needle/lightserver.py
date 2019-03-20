import os
from signal import signal, SIGPIPE, SIG_DFL, SIGTERM
from flask import Flask, render_template
# from flask_bootstrap import Bootstrap
from flask_wtf import Form
from flask_codemirror.fields import CodeMirrorField
from wtforms.fields import SubmitField
from flask_codemirror import CodeMirror
from flask import request
from subprocess import Popen, PIPE, STDOUT
from threading import Thread
signal(SIGPIPE, SIG_DFL)
result = None
output = None

CODEMIRROR_LANGUAGES = ['python', 'html']
SECRET_KEY = 'secret!'
CODEMIRROR_THEME = '3024-night'
CODEMIRROR_ADDONS = (
    ('display', 'placeholder'),
)

app = Flask(__name__)
app.config.from_object(__name__)
codemirror = CodeMirror(app)
# Bootstrap(app)



#RENDER HTML HOME PAGE| WILL NOW USE REACT
@app.route('/')
def test():
    return render_template('v2.html')


#KILL PROGRAM 
@app.route("/kill")
def kill():
    global result
    print "Starting kill"
    if result != None:
        print "Killing"
        os.killpg(os.getpgid(result.pid), SIGTERM)
        result = None
        return "Killed it..."
    else:
        return "Nothing to kill"



def spawn(code, userInput):
    global result
    global output

    f = open('userCode/code.py', 'w')
    f.write(code)
    f.close()
 
    f = open('userCode/input.txt', 'w')
    f.write(userInput)
    f.close()

    #HERE
    result = Popen("python userCode/code.py < userCode/input.txt", stdout=PIPE,
                   stdin=PIPE, stderr=PIPE, shell=True, preexec_fn=os.setsid)
    output = result.communicate()[0]


@app.route("/run", methods=['POST'])
def runcode():
    code = request.form['code']
    userInput = request.form['input']
    #HERE
    t = Thread(target=spawn, args=(code, userInput,))
    t.start()
    return "Running..."


@app.route("/output")
def getOutput():
    global output
    if output != None:
        #HERE
        temp = (output + '.')[:-1]
        output = None
        return temp
    else:
        return "No output..."


if __name__ == '__main__':
    app.run(debug=True)
