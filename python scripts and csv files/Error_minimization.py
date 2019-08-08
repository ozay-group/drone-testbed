import time
import pandas as pd
import matplotlib as mpl 
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
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
import operator
import csv
filename = "datas"

URI = 'radio://0/79/2M/E7E7E7E7EA'
# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(filename='test.log',level=logging.DEBUG)

x_list = list()
y_list = list()
z_list = list()

std_dev=list()
std_dev1=list()
y_average_list=list()
y_std_deviation_list=list()
y_mean_list_list=list()
y_std_deviation_list_abs=list()
std_dev_dictionary={}
y_list_desired_val=list()
y_list_desired_list=list()

def Backward(t,vf):
    print("Backward ")
    for _ in range(t):
        cf.commander.send_hover_setpoint(vf, 0, 0, 0.2)
        time.sleep(0.1)
    
    return
def Forward(t,vf):
    print("Forward ")
    
    for y in range(t):
        cf.commander.send_hover_setpoint(vf, 0, 0, 0.2)
        time.sleep(0.1)
    
    return
def Right(t,vs):
    print("Right ")
    for _ in range(t):
        cf.commander.send_hover_setpoint(0, vs, 0, 0.2)
        time.sleep(0.1)
    
    return
def Left(t,vs):
    print("Left ")
    for _ in range(t):
        cf.commander.send_hover_setpoint(0, vs, 0, 0.2)
        time.sleep(0.1)
    
    return
def Hovering(t):
    print("Hovering ")
    for _ in range(t):
        cf.commander.send_hover_setpoint(0, 0, 0, 0.2)
        time.sleep(0.1)
    
    return
def Takeoff(t):
    print("Takeoff ")
    for y in range(t):
        cf.commander.send_hover_setpoint(0, 0, 0, y/25)
        time.sleep(0.1)
    
    return
def landing(t):
    print("Landing ")
    for y in range(t):
        cf.commander.send_hover_setpoint(0, 0, 0, (t-y) / 25)
        time.sleep(0.1)
    cf.commander.send_stop_setpoint()
    
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
                
                #ESCAPING
        elif key == 27:#Escape tab
            break
                #FORWARD_DIRECTION
        elif key==curses.KEY_UP:
                #standard_deviation(y_list_desired)

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
        stdscr.refresh()


def reset_estimator(scf):
    cf = scf.cf
    cf.param.set_value('kalman.resetEstimation', '1')
    time.sleep(0.1)
    cf.param.set_value('kalman.resetEstimation', '0')

    # wait_for_position_estimator(cf)

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

#         #1 deviadtion method to minimise error
#     variance=np.var(y_list)
#     standard_dev=np.std(y_list)

#     #appending each standard deviation of y to the std_y csv file
#     row=[standard_dev]
#     row1=[y_list]
#     with open('std_y.csv', 'a') as csvFile:
#         writer = csv.writer(csvFile)
#         writer.writerow(row)
#         writer.writerow(row1)#to append the corresponding y_list
#     csvFile.close()

# #extracting the smallest standard deviation
#     df=pd.read_csv('std_y.csv') 

#     q=df['standard'].min()
#     r=df[df['standard']==q].index.item() # the row numbmer of minimum deviation
#     p=r+1#row number of the desired y_list
#     # print(q)
#     # print(r)
#     y_desired=df.iat[p,0]

#     print(y_desired)#we can plot this desired y-list value from  a different attempted trajectories

       #2 average method   
    y_average= sum(y_list) / len(y_list)
    y_average_list=[y_average] * len(y_list) #we can plot this average y-list which is the desired one
    
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
     #3 deviation of each y list and extracting the smallest one

    y_mean_list=np.mean(y_list)#mean of the Y-list
    y_mean_list_list=[y_mean_list] * len(y_list)
    y_std_deviation_list=list(map(operator.sub, y_list, y_mean_list_list))
    y_std_deviation_list_abs= [abs(number) for number in y_std_deviation_list]
    #difference_squared=[i ** 2 for i in difference]
    #two lists in a dictionary
  #print(y_list_desired)# from this we can plot this desired y-list value
    #conditions for the square 
    
    for key in y_list: 
        for value in y_std_deviation_list_abs:
            std_dev_dictionary[key] = value 
            y_std_deviation_list_abs.remove(value) 
            break
    #y_list_desired_val=y_list_desired    
    #print(std_dev_dictionary)# dictonary={y-list,std_dev_abs}
    y_list_desired= min(std_dev_dictionary, key = lambda x: std_dev_dictionary.get(x))
    y_list_desired_list=[y_list_desired] * len(y_list)#list
    plt.show()
    
  








