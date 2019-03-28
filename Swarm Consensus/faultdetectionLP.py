#  Copyright (C) Univesity of Michigan, Ann Arbor


import math
import csv
import logging
import time
from threading import Timer


# Import PuLP modeler functions

from pulp import *

import numpy as np

# Import random number generation functions

from random import *

import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger


# Change uris according to your setup
URI0 = 'radio://0/80/2M/E7E7E7E7E7'
URI1 = 'radio://0/80/2M/E7E7E7E7EC'
URI2 = 'radio://0/80/2M/E7E7E7E7EA'
URI3 = 'radio://0/80/2M/E7E7E7E7E9'
URI4 = 'radio://0/80/2M/E7E7E7E7EB'

#drone height parameters, h being the beginning height before consensus
params0 = {'base': 0.15, 'h': 1.2, 'num': 0}
params1 = {'base': 0.15, 'h': 0.6, 'num': 1}
params2 = {'base': 0.15, 'h': 0.8, 'num': 2}
params3 = {'base': 0.15, 'h': 0.5, 'num': 3}
params4 = {'base': 0.15, 'h': 1.0, 'num': 4}


uris = {
    URI0,
    URI1,
    URI2,
    URI3,
    URI4
}

params = {
    URI0: [params0],
    URI1: [params1],
    URI2: [params2],
    URI3: [params3],
    URI4: [params4],
}

#the current heights of the five drones
currentPos = [0,0,0,0,0]
#the calculated heights of the five drones
nextPos = [0,0,0,0,0]
#log of the heights
savelog = [[],[],[],[],[]]

def reset_estimator(scf):
    cf = scf.cf

    cf.param.set_value('kalman.resetEstimation', '1')
    time.sleep(0.1)
    cf.param.set_value('kalman.resetEstimation', '0')
    time.sleep(2)



def poshold(cf, t, z):

    steps = t * 10

    for r in range(steps):
        cf.commander.send_hover_setpoint(0, 0, 0, z)
        time.sleep(0.1)

def consensus(currentPosition,algNum):
    print('hey')
    if len(currentPosition) == 5 and algNum == 1:
        print('hey1')
        nextPos[0] = 0.5*(currentPosition[0] + currentPosition[1])
        nextPos[1] = 0.333 *(currentPosition[0] + currentPosition[1] + currentPosition[2])
        nextPos[2] = 0.5 *(currentPosition[1] + currentPosition[2])
        nextPos[3] = currentPosition[3]
        nextPos[4] = currentPosition[4]

    elif len(currentPosition) == 5 and algNum == 2:
        print('hey2')
        nextPos[0] = currentPosition[0]
        nextPos[1] = currentPosition[1]
        nextPos[2] = 0.5 * (currentPosition[2] + currentPosition[3])
        nextPos[3] = 0.333 *(currentPosition[2] + currentPosition[3] + currentPosition[4])
        nextPos[4] = 0.5 * (currentPosition[4]+currentPosition[3])

    elif len(currentPosition) == 5 and algNum == 3:
        print('hey3')
        nextPos[0] = currentPosition[0]
        nextPos[1] = currentPosition[1] - 0.25
        nextPos[2] = 0.5 * (currentPosition[2] + currentPosition[3]) - 0.2
        nextPos[3] = 0.333 *(currentPosition[2] + currentPosition[3] + currentPosition[4])
        nextPos[4] = 0.5 * (currentPosition[4]+currentPosition[3])

    elif len(currentPosition) == 5 and algNum == 4:
        print('hey4')
        nextPos[0] = currentPosition[0]
        nextPos[1] = currentPosition[1] - 0.25
        nextPos[2] = 0.5 * (currentPosition[2] + currentPosition[3]) - 0.2
        nextPos[3] = 0.333 *(currentPosition[2] + currentPosition[3] + currentPosition[4])
        nextPos[4] = 0.5 * (currentPosition[4]+currentPosition[3])

faultArray = [[],[],[],[],[]]

numSwitches = 0

safeLand = 0

def faultDetect(arr):
    print('detecting')

    # y0 = np.matrix('0.575; 0.575; 0.575; 0.575; 0.575')

    # y1 = y0

    # y2 = y1

    # y3 = y2

    # y4 = y3

    # y5 = y4
    df = 12

    y0.append(arr[0][df])
    y0.append(arr[1][df])
    y0.append(arr[2][df])
    y0.append(arr[3][df])
    y0.append(arr[4][df])


    y1.append(arr[0][df+1])
    y1.append(arr[1][df+1])
    y1.append(arr[2][df+1])
    y1.append(arr[3][df+1])
    y1.append(arr[4][df+1])


    y2.append(arr[0][df+2])
    y2.append(arr[1][df+2])
    y2.append(arr[2][df+2])
    y2.append(arr[3][df+2])
    y2.append(arr[4][df+2])


    y3.append(arr[0][df+3])
    y3.append(arr[1][df+3])
    y3.append(arr[2][df+3])
    y3.append(arr[3][df+3])
    y3.append(arr[4][df+3])


    y4.append(arr[0][df+4])
    y4.append(arr[1][df+4])
    y4.append(arr[2][df+4])
    y4.append(arr[3][df+4])
    y4.append(arr[4][df+4])


    y5.append(arr[0][df+5])
    y5.append(arr[1][df+5])
    y5.append(arr[2][df+5])
    y5.append(arr[3][df+5])
    y5.append(arr[4][df+5])





    # A new LP problem

    prob = LpProblem("drones", LpMinimize)


    # A vector of n binary variables

    n0 = LpVariable.matrix("n0", list(range(5)), -0.05, 0.05)

    n1 = LpVariable.matrix("n1", list(range(5)), -0.05, 0.05)

    n2 = LpVariable.matrix("n2", list(range(5)), -0.05, 0.05)

    n3 = LpVariable.matrix("n3", list(range(5)), -0.05, 0.05)

    n4 = LpVariable.matrix("n4", list(range(5)), -0.05, 0.05)


    # Use None for +/- Infinity, i.e. z <= 0 -> LpVariable("z", None, 0)


    A1 = np.matrix('0.5 0.5 0 0 0; 0.3333 0.3333 0.3333 0 0; 0 0.5 0.5 0 0; 0 0 0 1 0; 0 0 0 0 1')

    A2 = np.matrix('1 0 0 0 0; 0 1 0 0 0; 0 0.5 0.5 0 0; 0 0 0.3333 0.3333 0.3333; 0 0 0 0.5 0.5')


    # Objective

    prob += 0, "obj"

    # (the name at the end is facultative)


    z1 = y1-np.dot(A1,y0);

    z2 = y2-np.dot(A2,y1);

    z3 = y3-np.dot(A1,y2);

    z4 = y4-np.dot(A2,y3);

    z5 = y5-np.dot(A1,y4);


    # Constraints


    prob += n0[0]==np.asscalar(z1[0])

    prob += n0[1]==np.asscalar(z1[1])

    prob += n0[2]==np.asscalar(z1[2])

    prob += n0[3]==np.asscalar(z1[3])

    prob += n0[4]==np.asscalar(z1[4])


    prob += n1[0]==np.asscalar(z2[0])

    prob += n1[1]==np.asscalar(z2[1])

    prob += n1[2]==np.asscalar(z2[2])

    prob += n1[3]==np.asscalar(z2[3])

    prob += n1[4]==np.asscalar(z2[4])


    prob += n2[0]==np.asscalar(z3[0])

    prob += n2[1]==np.asscalar(z3[1])

    prob += n2[2]==np.asscalar(z3[2])

    prob += n2[3]==np.asscalar(z3[3])

    prob += n2[4]==np.asscalar(z3[4])


    prob += n3[0]==np.asscalar(z4[0])

    prob += n3[1]==np.asscalar(z4[1])

    prob += n3[2]==np.asscalar(z4[2])

    prob += n3[3]==np.asscalar(z4[3])

    prob += n3[4]==np.asscalar(z4[4])


    prob += n4[0]==np.asscalar(z5[0])

    prob += n4[1]==np.asscalar(z5[1])

    prob += n4[2]==np.asscalar(z5[2])

    prob += n4[3]==np.asscalar(z5[3])

    prob += n4[4]==np.asscalar(z5[4])


    # prob += np.dot(A2,y1)+n1==y2, "c2"

    # prob += np.dot(A1,y2)+n2==y3, "c3"

    # prob += np.dot(A2,y3)+n3==y4, "c4"

    # prob += np.dot(A2,y4)+n4==y5, "c4"

    # (the names at the end are facultative)


    # Write the problem as an LP file

    prob.writeLP("drones.lp")


    # Solve the problem using the default solver

    prob.solve()


    # Print the status of the solved LP

    print("Status:", LpStatus[prob.status])


    # Print the value of the variables at the optimum

    for v in prob.variables():

        print(v.name, "=", v.varValue)


    # Print the value of the objective

    print("objective=", value(prob.objective))


    if (LpStatus[prob.status] == 'Infeasible'):
        print('fault detected!')
        safeLand = 1


def run_sequence(scf, params):
    cf = scf.cf
    base = params['base']
    z = params['h']


    #sets variables for liftoff, beginning, and end heights
    end = 0.3
    base = params['base']
    h = params['h']
    num = params['num']

    # lifts drones off and sends to beginning heights
    poshold(cf, 2, base)
    poshold(cf, 5,h)

     # The definition of the logconfig can be made before connecting
    log_config = LogConfig(name='Height', period_in_ms=50)
    log_config.add_variable('stateEstimate.z', 'float')
    with SyncLogger(scf, log_config) as logger:
        #sets the runtime
        endTime = time.time() + 46 #second run    
        j = 0
        time_elapsed = float(0)

        #initiliazes the algorithm to the first
        algNum = 1

        for log_entry in logger:
            timestamp = log_entry[0]
            data = log_entry[1]
            currentPos[num] = data['stateEstimate.z']
            
            #first runthrough sets begin time of drone, and holds it in
            #current position for another second
            if j == 0:
                begin_T = timestamp
                j = 1
                poshold(cf,1,h)
                print(0)

            #concurrent runthroughs run the consensus algorithm every
            #three seconds and sends the desired position every second
            else:
                time_elapsed = float((timestamp - begin_T))/1000

                #every three seconds runs consensus alg
                if time_elapsed.is_integer() and (int(time_elapsed) % 2) == 0:
                    #ensures all three drones have sent their positions before continuuing
                    while currentPos[0] == 0 or currentPos[1] == 0 or currentPos[2] == 0 or currentPos[3] == 0 or currentPos[4] == 0:
                        time.sleep(0.001)


                    faultArray[num].append(currentPos[num])
                    #runs consensus algorithm only on one of the 3 parallel programs running
                    if num == 0:
                        print('running consensus')
                        consensus(currentPos,algNum)
                        print(algNum)
                        if algNum == 1 or algNum == 2:
                            if algNum == 1:
                                algNum = 2
                            else:
                                algNum = 1
                        if algNum == 3 or algNum == 4:
                            print(len(faultArray[0]))
                            faultDetect(faultArray)
                            print('hello')
                            if algNum == 3:
                                algNum = 4
                            else:
                                algNum = 3                            
                        print(algNum)
                    #(nextPos)

                    #waits till the algorithm runs to continue
                    while (nextPos[0] == 0 or nextPos[1] == 0 or nextPos[2] == 0 or nextPos[3] == 0 or nextPos[4] == 0):
                        time.sleep(0.001)

                    #sends the update positions to the drones
                    #poshold(cf,1,currentPos[num])
                    print(nextPos[num])
                    print(safeLand)
                    if safeLand == 0:
                        poshold(cf,1,nextPos[num])
                    #print(nextPos)

                #sends position for drones every second
                elif time_elapsed.is_integer():
                    if time_elapsed < 2:
                        poshold(cf,1,h)
                    else:
                        poshold(cf,1,nextPos[num])
            #if time_elapsed.is_integer():
                #print(time_elapsed)
                #print(currentPos)

            #appends the time and height data to a log
            savelog[num].append([time_elapsed,currentPos[num]])

            #switches to faulty algorithm after 60 seconds
            if time_elapsed >= 30:
                algNum = 3

            #ends program after endTime seconds
            if time.time() > endTime or safeLand == 1:
                break

    if safeLand == 1:
        print('Fault Detected')
    #poshold(cf,2, end)
    # # Base altitude in meters
    #print(currentPos)

    #sends drones to base height
    poshold(cf, 2, base)

    #saves the data for future use
    str1 = 'testing'
    str2 = '.csv'
    with open(str1+str(num)+str2, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(savelog[num]) 
    cf.commander.send_stop_setpoint()


if __name__ == '__main__':
    cflib.crtp.init_drivers(enable_debug_driver=False)

    factory = CachedCfFactory(rw_cache='./cache')

    with Swarm(uris, factory=factory) as swarm:
        swarm.parallel(reset_estimator)
      # swarm.parallel(height_log)
        swarm.parallel(run_sequence, args_dict=params)
