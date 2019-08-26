#packages
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
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger
import operator
import csv
import threading
from queue import Queue
#name of the file for the data to be written
filename1 = "data_cf1"
filename2="data_cf2"

URI1 = 'radio://0/88/2M/E7E7E7E7EB'
URI2 = 'radio://0/80/2M/E7E7E7E7EC'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(filename='test.log',level=logging.DEBUG)
### the below code is to calculate the expected position sequence values
#initiating approximated positons from kalman filter
x_list_kalman1 = list()
y_list_kalman1 = list()
z_list_kalman1 = list()
x_list_kalman2 = list()
y_list_kalman2 = list()
z_list_kalman2 = list()
z0=0.2
#initiating CF1 expected positions list
x_position1=list()
y_position1=list()
z_position1=list()
sequence1=list()
vx_list1 = list()
vy_list1 = list()
t_list1 = list()

#initiating CF2 expected position list
x_position2=list()
y_position2=list()
z_position2=list()
sequence2=list()
vx_list2 = list()
vy_list2 = list()
t_list2 = list()

#Read the csv file for crazyflie 1
csv_data1= pd.read_csv('imprt3.csv')

for i in range(csv_data1.shape[0]):
    row_values=csv_data1.iloc[i]
    vf1=row_values.values[0]
    vx_list1.append(vf1)
    vs1=row_values.values[1]
    vy_list1.append(vs1)
    t1=row_values.values[2]
    t_list1.append(t1)
#calculating position
x_position=[a*b for a,b in zip(vx_list1,t_list1)]
x_position=map(lambda x: x * 0.1 ,x_position)# since the time scale is a multiple of 0.1, we multiply the result by 0.1
x_position= list(x_position)
x_val=0
for i in range(0,len(x_position)):
    x_val=x_val + x_position[i]
    x_position1.append(x_val)
y_position=[a*b for a,b in zip(vy_list1,t_list1)]
y_position=map(lambda x: x * 0.1 ,y_position)
y_position=list(y_position)
y_val=0
for i in range(0,len(y_position)):
    y_val=y_val + y_position[i]
    y_position1.append(y_val)
z_position1=[z0] * len(x_position1)
sequence1=[(i,j,k,l) for i,j,k,l in zip(x_position1,y_position1,z_position1,t_list1)]


#Read the csv file for crazyflie 2
csv_data2= pd.read_csv('imprt4.csv')

for i in range(csv_data2.shape[0]):
    row_values=csv_data2.iloc[i]
    vf2=row_values.values[0]
    vx_list2.append(vf2)
    vs2=row_values.values[1]
    vy_list2.append(vs2)
    t2=row_values.values[2]
    t_list2.append(t2)

x_positions=[a*b for a,b in zip(vx_list2,t_list2)]
x_positions=map(lambda x: x * 0.1 ,x_positions)
x_positions=list(x_positions)
x_val=0
for i in range(0,len(x_positions)):
    x_val=x_val + x_positions[i]
    x_position2.append(x_val)


y_positions=[a*b for a,b in zip(vy_list2,t_list2)]
y_positions=map(lambda x: x * 0.1 ,y_positions)
y_positions=list(y_positions)
y_val=0
for i in range(0,len(y_positions)):
    y_val=y_val + y_positions[i]
    y_position2.append(y_val)


z_position2=[z0] * len(x_position2)
sequence2=[(i,j,k,l) for i,j,k,l in zip(x_position2,y_position2,z_position2,t_list2)]
### end of the expected position sequence code



uris = {
    URI1,
    URI2
}
seq_args = {
    URI1: [sequence1],
    URI2: [sequence2],}
#estimate the crazyflie position and logg the data
def wait_for_position_estimator(scf):
    print('Waiting for estimator to find position...')
    if scf.cf.link_uri== URI1 | URI2:
        
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
def wait_for_param_download(scf):
    while not scf.cf.param.is_updated:
        time.sleep(1.0)
    print('Parameters downloaded for', scf.cf.link_uri)

def reset_estimator(scf):

    cf = scf.cf
    if scf.cf.link_uri== URI1 | URI2:#for both of the crazyflies , this code will run

        cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
        cf.param.set_value('kalman.resetEstimation', '0')

        wait_for_position_estimator(scf)

def run_sequence(scf,sequence):
    try:
        cf = scf.cf
        cf.param.set_value('flightmode.posSet', '1')
        if scf.cf.link_uri== URI1:#below is for the first crazyflie only
            
            #take off for  drone1
        
            for y in range(5):
                cf.commander.send_hover_setpoint(0, 0, 0, y / 25)
                time.sleep(0.1)
            for _ in range(30):
                cf.commander.send_hover_setpoint(0, 0, 0, 0.2)
                time.sleep(0.1)
            #first drone trajectory
            csv_data1= pd.read_csv('imprt3.csv')
            for i in range(csv_data1.shape[0]):
                row_values=csv_data1.iloc[i]
                vf1=row_values.values[0]
                vf1=0.8*vf1#scale down the velocity
                vs1=row_values.values[1]
                vs1=0.8*vs1#scale down the velocity
                t1=row_values.values[2]
                for _ in range(int(t1)):
                    cf.commander.send_hover_setpoint(vf1,vs1,0,0.2)
                    time.sleep(0.1)

            #landing for drone 1
            for _ in range(30):
                cf.commander.send_hover_setpoint(0, 0, 0, 0.2)
                time.sleep(0.1)
            for y in range(5):
                cf.commander.send_hover_setpoint(0, 0, 0, (5 - y) / 25)
                time.sleep(0.4)
            cf.commander.send_stop_setpoint()
        #drone 2 code
        elif scf.cf.link_uri==URI2:
            #take off
            for y in range(5):
                cf.commander.send_hover_setpoint(0, 0, 0, y / 25)
                time.sleep(0.1)
            for _ in range(10):
                cf.commander.send_hover_setpoint(0, 0, 0, 0.2)
                time.sleep(0.1)
            #trajectory for drone 2    
            csv_data2=pd.read_csv('imprt4.csv')
            for i in range(csv_data2.shape[0]):
                row_values=csv_data2.iloc[i]
                vf2=row_values.values[0]
                vf2=0.8*vf2#scale down the velocity
                vs2=row_values.values[1]
                vs2=0.8*vs2#scale down the velocity
                t2=row_values.values[2]
                for _ in range(int(t2)):
                    cf.commander.send_hover_setpoint(vf2,vs2,0,0.2)
                    time.sleep(0.1)
            #landing for drone 2    
            for y in range(5):
                cf.commander.send_hover_setpoint(0, 0, 0, (5 - y) / 25)
                time.sleep(0.4)
            cf.commander.send_stop_setpoint()

    except Exception as e:
        print(e)
#log data for crazyflie 1
def start_position_printing(scf):
    if scf.cf.link_uri==URI1:
        log_conf = LogConfig(name='Position', period_in_ms=500)
        log_conf.add_variable('kalman.stateX', 'float')
        log_conf.add_variable('kalman.stateY', 'float')
        log_conf.add_variable('kalman.stateZ', 'float')
        scf.cf.log.add_config(log_conf)
        log_conf.data_received_cb.add_callback(position_callback1)
        log_conf.start()
    elif scf.cf.link_uri==URI2:
        log_conf = LogConfig(name='Position', period_in_ms=500)
        log_conf.add_variable('kalman.stateX', 'float')
        log_conf.add_variable('kalman.stateY', 'float')
        log_conf.add_variable('kalman.stateZ', 'float')
        scf.cf.log.add_config(log_conf)
        log_conf.data_received_cb.add_callback(position_callback2)
        log_conf.start()

def position_callback1(timestamp, data, logconf):
    x = data['kalman.stateX']
    y = data['kalman.stateY']
    z = data['kalman.stateZ']
    x_list_kalman1.append(x)
    y_list_kalman1.append(y)
    z_list_kalman1.append(z)        
def position_callback2(timestamp, data, logconf):
    x = data['kalman.stateX']
    y = data['kalman.stateY']
    z = data['kalman.stateZ']
    x_list_kalman2.append(x)
    y_list_kalman2.append(y)
    z_list_kalman2.append(z)



if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    factory = CachedCfFactory(rw_cache='./cache')
    with Swarm(uris, factory=factory) as swarm:
        # If the copters are started in their correct positions this is
        # probably not needed. The Kalman filter will have time to converge
        # any way since it takes a while to start them all up and connect. We
        # keep the code here to illustrate how to do it.
        #swarm.parallel(reset_estimator) # if there is a need to start all cf at the same position
        swarm.parallel(start_position_printing)
        print('Waiting for parameters to be downloaded...')
        swarm.parallel(wait_for_param_download)

        swarm.parallel(run_sequence,args_dict=seq_args)
    #writing logged data to csv files    
    f = open(filename1 + '.csv', 'w')
    with f:

        writer = csv.writer(f)
        writer.writerows([x_list_kalman1,y_list_kalman1,z_list_kalman1])
    f=open(filename2 + '.csv','w')
    with f:
        writer=csv.writer(f)
        writer.writerows([x_list_kalman2,y_list_kalman2,z_list_kalman2])

#3d plot of the trajectories
    fig=plt.figure()
    ax=fig.gca(projection='3d')
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    ax.plot(x_list_kalman1,y_list_kalman1,z_list_kalman1,'b-',label='CF1')
    #ax.plot(x_position1,y_position1,z_position1,'b-')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.title('Trajectory of CF1')
    ax.plot([x_list_kalman1[0]],[y_list_kalman1[0]],[z_list_kalman1[0]],'o',markerfacecolor='none', markeredgecolor='red',markersize=6.5,label='start')
    ax.plot([x_list_kalman1[-1]],[y_list_kalman1[-1]],[z_list_kalman1[-1]],'o',markerfacecolor='red', markeredgecolor='red',markersize=6.5,label='end')
    #ax.plot([x_position1[0]],[y_position1[0]],[z_position1[0]],'o',markerfacecolor='none', markeredgecolor='red',markersize=6.5,label='start')
    #ax.plot([x_position1[-1]],[y_position1[-1]],[z_position1[-1]],'o',markerfacecolor='red', markeredgecolor='red',markersize=6.5,label='end')

    ax = fig.add_subplot(1, 2, 2, projection='3d')
    ax.plot(x_list_kalman2,y_list_kalman2,z_list_kalman2,'k',label='CF2')
    #ax.plot(x_position2,y_position2,z_position2,'k')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.plot([x_list_kalman2[0]],[y_list_kalman2[0]],[z_list_kalman2[0]],'o',markerfacecolor='none', markeredgecolor='red',markersize=6.5,label='start')
    ax.plot([x_list_kalman2[-1]],[y_list_kalman2[-1]],[z_list_kalman2[-1]],'o',markerfacecolor='red', markeredgecolor='red',markersize=6.5,label='end')
    #ax.plot([x_position2[0]],[y_position2[0]],[z_position2[0]],'o',markerfacecolor='none', markeredgecolor='red',markersize=6.5,label='start')
    #ax.plot([x_position2[-1]],[y_position2[-1]],[z_position2[-1]],'o',markerfacecolor='red', markeredgecolor='red',markersize=6.5,label='end')

    plt.title('Trajectory of CF2')
    ax.legend(numpoints=1)
    plt.show()
    





    
    
  








