import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl 
from mpl_toolkits.mplot3d import axes3d
import matplotlib.gridspec as gridspec
from matplotlib import animation
import pandas as pd
import curses
import logging
import math
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger
import pyqtgraph as pyqtgraph
import csv
#style.use('bmh')
filename = "datas"

URI = 'radio://0/80/2M/E7E7E7E7EB'
# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(filename='test.log',level=logging.DEBUG)

x_list = list()
y_list = list()
z_list = list()

def init():
    line.set_data(x[:2],y[:2])
    return line,
def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    while 1:
        key=stdscr.getch()
        print(key)
        if key == 10:#curses.KEY_ENTER:#take off move
            print("Takeoff")
            for y in range(5):
                cf.commander.send_hover_setpoint(0, 0, 0, y / 25)
                time.sleep(0.2)
                logging.debug('take off'.format(0,0,0,y/25))
            real_time() 

        elif key== curses.KEY_BACKSPACE:#landing 
                print("Landing")
                for y in range(5):
                    cf.commander.send_hover_setpoint(0, 0, 0, (5 - y) / 25)
                    time.sleep(0.2)

                cf.commander.send_stop_setpoint()
                real_time()
        elif key == 27:#Escape tab
            break
        elif key==curses.KEY_UP:
                print("Forward")
                for _ in range(10):
                    cf.commander.send_hover_setpoint(0.2, 0, 0, 0.2)
                    time.sleep(0.1)
                real_time()
        elif key==curses.KEY_DOWN:
                print("Backward")
                for _ in range(10):
                    cf.commander.send_hover_setpoint(-0.2, 0, 0, 0.2)
                    time.sleep(0.2)
                real_time()
                #Right
        elif key==curses.KEY_RIGHT:
                print("Right")
                for _ in range(5):
                    cf.commander.send_hover_setpoint(0, -0.2, 0, 0.2)
                    time.sleep(0.1)
                real_time()
                #LEFT
        elif key==curses.KEY_LEFT:
                print("Left")
                for _ in range(5):
                    cf.commander.send_hover_setpoint(0, 0.2, 0, 0.2)
                    time.sleep(0.1) 
                real_time()              
        elif key==curses.KEY_HOME:#This is Hovering==Fn+Left arrow
                print("Hovering")
                for _ in range(10):
                    cf.commander.send_hover_setpoint(0, 0, 0, 0.4)
                    time.sleep(0.2)
                real_time()

                
        stdscr.refresh()	

def reset_estimator(scf):
    cf = scf.cf
    cf.param.set_value('kalman.resetEstimation', '1')
    time.sleep(0.1)
    cf.param.set_value('kalman.resetEstimation', '0')

def start_position_printing(scf):
    log_conf = LogConfig(name='Position', period_in_ms=500)
    log_conf.add_variable('kalman.stateX', 'float')
    log_conf.add_variable('kalman.stateY', 'float')
    log_conf.add_variable('kalman.stateZ', 'float')

    scf.cf.log.add_config(log_conf)
    log_conf.data_received_cb.add_callback(position_callback)
    log_conf.start()

def position_callback(timestamp, data, logconf):
    x = data['kalman.stateX']
    y = data['kalman.stateY']
    z = data['kalman.stateZ']
  
    x_list.append(x)
    y_list.append(y)
    z_list.append(z)

y = y_list
x = x_list

fig, ax = plt.subplots()
line, = ax.plot([], [], '-')
plt.ion()
plt.show()
ax.margins(0.05)


def animate(i):
    xdata = x[:i]
    ydata = y[:i]
    
    line.set_data(xdata, ydata)
    plt.plot(x,y)
    plt.gca().line[0].set_xdata(x)
    plt.gca().line[0].set_ydata(y)
    plt.gcf().canvas.flush_events()
    plt.gca().relim()
    plt.gca().autoscale_view()
    plt.pause(0.05)
    # plt.draw()
    # ax.relim()
    # ax.autoscale()
    return line,
def real_time():
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=5)
    plt.ion()
    plt.draw()
    #time.sleep(0.05)
    plt.pause(0.00001) 
    return
# pyqtgraph.plot()
if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf
        time.sleep(2)
        logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
       
        reset_estimator(scf)
        start_position_printing(scf)

        curses.wrapper(main)
    
    f = open(filename + '.csv', 'w')

    with f:

        writer = csv.writer(f)
        writer.writerows([x_list,y_list,z_list])






