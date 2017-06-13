from flask import Flask, make_response, request, current_app, render_template, url_for
from flask_cors import CORS, cross_origin
import jsonify
import json
from datetime import datetime
from time import sleep
from threading import Thread
from pymouse import PyMouse
from flask_socketio import SocketIO, send
import pyautogui
import Xlib.threaded

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)
m = PyMouse()
CORS(app)

ajax = 0
timestamp = datetime.now()
xy = {'X':0,'Y':0  }

def set_to_zero_timeout():
    while (True):
        sleep(.5)
        delta = datetime.now() - timestamp
        
        try:
            if (int(delta.seconds) > 1):
                global xy
                xy['X'] = 0
                xy['Y'] = 0
                
            
                
        except:
            print 'Exception'
            
        
t1 = Thread(target=set_to_zero_timeout)
t1.start()

@socketio.on('message')
def handMessage(msg):
    try:
        timestamp = datetime.now()
        global xy
        xy = json.loads(msg)
        normalize_xy = normalize_XY(xy)
        print normalize_xy
        inline_move_cursor(normalize_xy)

        
    except:
        print 'Could not parse SocketIO Message'
    
@socketio.on('click')
def handle_click(mouse_button):
    try:
        print mouse_button
        if (mouse_button == 1):
            
            X = m.position()[0]
            Y = m.position()[1]
            m.click(X,Y,button=1)
            print 'Pressed left click'
    except:
        print 'failure'
        return 'failure'


def normalize_XY(ajax):
    if (ajax['Y'] < 100 and ajax['X'] < 100):
        return ajax['X'], ajax['Y']
    elif (ajax['X'] >= 100):
        return 100, ajax['Y']
    elif (ajax['Y'] >= 100):
        return ajax['X'], 100
def move_cursor(this_argument):
    if type(this_argument == tuple):
        try:
            new_pos = (m.position()[0] + (this_argument[0]/2),m.position()[1] + (this_argument[1]/2))
            m.move(new_pos[0], new_pos[1])
        except:
            print 'Unable to move Cursor'

def inline_move_cursor(arg):
    thread = Thread(target=move_cursor, args=[arg])
    thread.start()

def print_ajax():
    global ajax
    print ajax['X']



@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/test")
def hello2():
    return "Hello World!"



if __name__ == "__main__":
    socketio.run(app, host='192.168.1.6')
