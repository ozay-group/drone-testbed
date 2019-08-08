import time

import matplotlib as mpl 
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import animation
import numpy as np
import matplotlib.pyplot as plt
import curses
import logging
import math
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

import csv
filename = "datas"

URI = 'radio://0/88/2M/E7E7E7E7EB'
# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(filename='test.log',level=logging.DEBUG)

x_list = list()
y_list = list()
z_list = list()


def init():
    line.set_data(x[:2],y[:2])
    return line,
#The following functions are created for easy use of them
def Backward(t,vf):
    print("Backward ")
    for _ in range(t):
        cf.commander.send_hover_setpoint(vf, 0, 0, 0.2)
        time.sleep(0.1)
    real_time()
    return
def Forward(t,vf):
    print("Forward ")
    for y in range(t):
        cf.commander.send_hover_setpoint(vf, 0, 0, 0.2)
        time.sleep(0.1)
    real_time()
    return
def Right(t,vs):
    print("Right ")
    for _ in range(t):
        cf.commander.send_hover_setpoint(0, vs, 0, 0.2)
        time.sleep(0.1)
    real_time()
    return
def Left(t,vs):
    print("Left ")
    for _ in range(t):
        cf.commander.send_hover_setpoint(0, vs, 0, 0.2)
        time.sleep(0.1)
    real_time()
    return
def Hovering(t):
    print("Hovering ")
    for _ in range(t):
        cf.commander.send_hover_setpoint(0, 0, 0, 0.2)
        time.sleep(0.1)
    real_time()
    return
def Takeoff(t):
    print("Takeoff ")
    for y in range(t):
        cf.commander.send_hover_setpoint(0, 0, 0, y/25)
        time.sleep(0.1)
    real_time()
    return
def landing(t):
    print("Landing ")
    for y in range(t):
        cf.commander.send_hover_setpoint(0, 0, 0, (t-y) / 25)
        time.sleep(0.1)
    cf.commander.send_stop_setpoint()
    real_time()
    return

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    while 1:
        key=stdscr.getch()
        #print(key)
        #TAKING OFF
        if key == 10:#curses.KEY_ENTER:#take off move
            print("Takeoff \r")
            for y in range(5):
                if key==curses.KEY_UP:
                    Forward(30,0.2)
                elif key==curses.KEY_DOWN:
                    Backward(30,-0.2)

                elif key==curses.KEY_RIGHT:
                    Right(30,-0.2)

                elif key==curses.KEY_LEFT:
                    Left(30,0.2)  
                elif key==curses.KEY_BACKSPACE:
                    landing(5)

                elif key==27:
                    break
                elif key==curses.KEY_HOME:
                    Hovering(30)
                cf.commander.send_hover_setpoint(0, 0, 0, y / 25)
                time.sleep(0.1)
                logging.debug('take off'.format(0,0,0,y/25))
                real_time()
                 
                #LANDING
        elif key== curses.KEY_BACKSPACE:#landing 
                print("Landing \r")
                for y in range(5):
                    if key==curses.KEY_UP:
                        Forward(30,0.2)
                         
                    elif key==curses.KEY_DOWN:
                        Backward(30,-0.2)                  

                    elif key==curses.KEY_RIGHT:
                        Right(30,-0.2)                     
                    elif key==curses.KEY_LEFT:
                        Left(30,0.2)                   
                    elif key==curses.KEY_ENTER:
                        Takeoff(10)                   
                    elif key==27:
                        break
                    elif key==curses.KEY_HOME:
                        Hovering(30)
                      
                    cf.commander.send_hover_setpoint(0, 0, 0, (5 - y) / 25)
                    time.sleep(0.1)
                cf.commander.send_stop_setpoint()
                real_time()
                #ESCAPING
        elif key == 27:#Escape tab
            break
                #FORWARD_DIRECTION
        elif key==curses.KEY_UP:
                
                print("Forward \r")
                for _ in range(10):
                    if key==curses.KEY_ENTER:

                        Takeoff(10)                     
                    elif key==curses.KEY_DOWN:
                        Backward(30,-0.2)                     
                    elif key==curses.KEY_RIGHT:
                        Right(30,-0.2)
                       
                    elif key==curses.KEY_LEFT:
                        Left(30,0.2)
                      
                    elif key==curses.KEY_BACKSPACE:
                         landing(5)                    
                    elif key==27:
                        break
                    elif key==curses.KEY_HOME:
                        Hovering(30)
                    cf.commander.send_hover_setpoint(0.2, 0, 0, 0.2)
                    time.sleep(0.1)
                    real_time()
                        
                    #BACKWARD_DIRECTION
        elif key==curses.KEY_DOWN:
                print("Backward \r")
                for _ in range(30):
                    if key==curses.KEY_UP:
                        Forward(30,0.2)
                        
                    elif key==curses.KEY_ENTER:
                        Takeoff(10)              
                    elif key==curses.KEY_RIGHT:
                        Right(30,-0.2)              
                    elif key==curses.KEY_LEFT:
                        Left(30,0.2)                 
                    elif key==curses.KEY_BACKSPACE:
                        landing(5)
                       
                    elif key==27:
                        break
                    elif key==curses.KEY_HOME:
                        Hovering(30)   
                    cf.commander.send_hover_setpoint(-0.2, 0, 0, 0.2)
                    time.sleep(0.1)
                    real_time()
                    #RIGHT_DIRECTION      
        elif key==curses.KEY_RIGHT:
                print("Right \r")
                for _ in range(30):
                    if key==curses.KEY_UP:
                        Forward(30,0.2)                    
                    elif key==curses.KEY_DOWN:
                        Backward(30,-0.2)             
                    elif key==curses.KEY_ENTER:
                        Takeoff(10)
                      
                    elif key==curses.KEY_LEFT:
                        Left(30,0.2)
                       
                    elif key==curses.KEY_BACKSPACE:
                        landing(5)
                       
                    elif key==27:
                        break
                    elif key==curses.KEY_HOME:
                        Hovering(30)
                       
                    cf.commander.send_hover_setpoint(0, -0.2, 0, 0.2)
                    time.sleep(0.1)
                    real_time()
                    #LEFT_DIRECTION        
        elif key==curses.KEY_LEFT:
                print("Left \r")
                for _ in range(30):
                    if key==curses.KEY_UP:
                        Forward(30,0.2)                      
                    elif key==curses.KEY_DOWN:
                        Backward(30,-0.2)
                                         
                    elif key==curses.KEY_ENTER:
                        Takeoff(10)
                        
                    elif key==curses.KEY_RIGHT:
                        Right(30,-0.2)
                       
                    elif key==curses.KEY_BACKSPACE:
                        landing(5)
                       
                    elif key==27:
                        break
                    elif key==curses.KEY_HOME:
                        Hovering(30)
                    cf.commander.send_hover_setpoint(0, 0.2, 0, 0.2)
                    time.sleep(0.1)
                    real_time()
                    #HOVERING                   
        elif key==curses.KEY_HOME:#This is Hovering==Fn+Left arrow
                print("Hovering \r")
                for _ in range(30):
                    if key==curses.KEY_UP:
                        Forward(30,0.2)
                       
                    elif key==curses.KEY_DOWN:
                        Backward(30,-0.2)
                        
                    elif key==curses.KEY_ENTER:
                        Takeoff(10)
                       
                    elif key==curses.KEY_LEFT:
                        Left(30,0.2)      
                    elif key==curses.KEY_BACKSPACE:
                        landing(5) 
                    elif key==27:
                        break
                    elif key==curses.KEY_RIGHT:
                        Right(30,-0.2)                      
                    cf.commander.send_hover_setpoint(0, 0, 0, 0.2)
                    time.sleep(0.1) 
                    real_time()
        
                
        stdscr.refresh()

def wait_for_position_estimator(scf):
    print('Waiting for estimator to find position...')

    log_config = LogConfig(name='Kalman Variance', period_in_ms=500)
    log_config.add_variable('kalman.varPX', 'float')
    log_config.add_variable('kalman.varPY', 'float')
    log_config.add_variable('kalman.varPZ', 'float')

    var_y_history = [1000] * 10
    var_x_history = [1000] * 10
    var_z_history = [1000] * 10

    threshold = 0.001

    with SyncLogger(scf, log_config) as logger:
        for log_entry in logger:
            data = log_entry[1]

            var_x_history.append(data['kalman.varPX'])
            var_x_history.pop(0)
            var_y_history.append(data['kalman.varPY'])
            var_y_history.pop(0)
            var_z_history.append(data['kalman.varPZ'])
            var_z_history.pop(0)

            min_x = min(var_x_history)
            max_x = max(var_x_history)
            min_y = min(var_y_history)
            max_y = max(var_y_history)
            min_z = min(var_z_history)
            max_z = max(var_z_history)

            #print("{} {} {}".format(max_x - min_x, max_y - min_y, max_z - min_z))

            if (max_x - min_x) < threshold and (
                    max_y - min_y) < threshold and (
                    max_z - min_z) < threshold:
                break
def reset_estimator(scf):
    cf = scf.cf
    cf.param.set_value('kalman.resetEstimation', '1')
    time.sleep(0.1)
    cf.param.set_value('kalman.resetEstimation', '0')

    wait_for_position_estimator(cf)

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
    # print('pos: ({}, {}, {})'.format(x, y, z))
    x_list.append(x)
    y_list.append(y)
    z_list.append(z)
#real time plot in 2d    
y = y_list
x = x_list

fig, ax = plt.subplots(1,1)
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
  
    return line,
def real_time():#creating function which can plot trajectories in 2D in real time
    anim = animation.FuncAnimation(fig, animate, init_func=init, interval=5)
    plt.ion()
    plt.draw()
   
    plt.pause(0.00001) 
    return

# this is the last line of code for real time plotting in 2d
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
    #3d plot after the flight
    fig=plt.figure()
    ax=fig.gca(projection='3d')

    ax.plot(x_list,y_list,z_list,'b-')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.plot([x_list[0]],[y_list[0]],[z_list[0]],'o',markerfacecolor='none', markeredgecolor='red',markersize=12.5,label='start')
    ax.plot([x_list[-1]],[y_list[-1]],[z_list[-1]],'o',markerfacecolor='red', markeredgecolor='red',markersize=12.5,label='end')
    plt.title('Trajectory of CF')
    
    ax.legend(numpoints=1)
    plt.show(block=True)
    plt.show()
    







