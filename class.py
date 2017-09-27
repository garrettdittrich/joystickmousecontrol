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

import multiprocessing


def worker(q):
    m = PyMouse()
    if (q.empty() == False):
        timestamp = datetime.now()
    while(q.empty() == False):
        sleep(10)
        print 'inside worker function'
        timestamp = datetime.now()
        tuple_get = q.get()
        xy = json.loads(tuple_get)
        move_cursor(normalize_XY(xy))
            
        
        
        

class Mouse_mover(object):

    def __init__(self, coords_q, time_since_last_move_q, mouse_event_func):
        self.coords_q = coords_q
        self.time_since_last_move_q = time_since_last_move_q
        self.mouse_event_func = mouse_event_func
        self.func = multiprocessing.Process(target=self.mouse_event_func, args=(self.coords_q,))
    def add_coord(self, ajax):
        coord_q.put(ajax)
        if (self.func.is_alive() == False):
            self.func.start()


    def start_mouse_func(self):
        func = multiprocessing.Process(target=self.mouse_event_func, args=(self.coords_q,))
        func.start()

       


coord_q = multiprocessing.Queue()
time_q = multiprocessing.Queue()