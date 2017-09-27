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
from utils import set_to_zero_timeout, normalize_XY, move_cursor, inline_move_cursor
import multiprocessing

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)
m = PyMouse()
CORS(app)

ajax = 0
timestamp = datetime.now()

def worker(q):
    m = PyMouse()
    if (q.empty() == False):
        timestamp = datetime.now()
    while(q.empty() == False):
        timestamp = datetime.now()
        tuple_get = q.get()
        xy = json.loads(tuple_get)
        move_cursor(normalize_XY(xy))
    return 'completed worker'          
        
        
        

class Mouse_mover(object):

    def __init__(self, coords_q, time_since_last_move_q, mouse_event_func):
        self.coords_q = coords_q
        self.time_since_last_move_q = time_since_last_move_q
        self.mouse_event_func = mouse_event_func
        self.func = multiprocessing.Process(target=self.mouse_event_func, args=(self.coords_q,))
    def add_coord(self, ajax):
        try:            
            coord_q.put(ajax)
            
            if (self.func.is_alive() == False):
                self.func.run()
        except Exception as e:
            print e


    def start_mouse_func(self):
        func = multiprocessing.Process(target=self.mouse_event_func, args=(self.coords_q,))
        func.start()

       


coord_q = multiprocessing.Queue()
time_q = multiprocessing.Queue()



mouse_object = Mouse_mover(coord_q, time_q, worker)

            
        
t1 = Thread(target=set_to_zero_timeout)
t1.start()

@socketio.on('message')
def handMessage(msg):

        mouse_object.add_coord(msg)
        

        
   
    
@socketio.on('click')
def handle_click(mouse_button):
    try:
        print mouse_button
        if (mouse_button == 1):
            
            X = m.position()[0]
            Y = m.position()[1]
            m.click(X,Y,button=1)
            print 'Pressed left click'
        elif (mouse_button == 2):
            X = m.position()[0]
            Y = m.position()[1]
            m.click(X,Y,button=2)
            print 'Pressed Right click'
    except:
        print 'failure'
        return 'failure'





@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/test")
def hello2():
    return "Hello World!"



if __name__ == "__main__":
    socketio.run(app, host='192.168.1.6')
