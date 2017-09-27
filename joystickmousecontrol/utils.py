from time import sleep
from datetime import datetime
from pymouse import PyMouse
from threading import Thread
timestamp = datetime.now()
xy = {'X':0,'Y':0  }
m = PyMouse()
ajax = 0

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

def normalize_XY(ajax):
    if (ajax['Y'] < 100 and ajax['X'] < 100):
        return ajax['X'], ajax['Y']
    elif (ajax['X'] >= 100):
        return 100, ajax['Y']
    elif (ajax['Y'] >= 100):
        return ajax['X'], 100
def move_cursor(this_argument):
    if type(this_argument == tuple):
        new_pos = (m.position()[0] + (this_argument[0]/2),m.position()[1] + (this_argument[1]/2))
        m.move(new_pos[0], new_pos[1])
        

def inline_move_cursor(arg):
    thread = Thread(target=move_cursor, args=[arg])
    thread.start()

def print_ajax():
    global ajax
    print ajax['X']
