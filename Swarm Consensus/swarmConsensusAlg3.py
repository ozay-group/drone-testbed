
#  Copyright (C) University of Michigan, Ann Arbor


import math
import logging
import time
from threading import Timer


import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger


# Change uris according to your setup
URI0 = 'radio://0/80/2M/E7E7E7E7E7'
URI1 = 'radio://0/80/2M/E7E7E7E7E8'
#URI2 = 'radio://0/80/2M/E7E7E7E7E9'
# d: diameter of circle
# z: altituce
params0 = {'base': 0.15, 'h': 0.4, 'num': 0}
params1 = {'base': 0.15, 'h': 1.0, 'num': 1}
#params2 = {'base': 0.30, 'h': 1.4, 'num': 2}

uris = {
    URI0,
    URI1,
#    URI2,
}

params = {
    URI0: [params0],
    URI1: [params1],
#    URI2: [params2],
}

currentPos = [0,0,0]
nextPos = [0,0,0]

def reset_estimator(scf):
    cf = scf.cf

    cf.param.set_value('kalman.resetEstimation', '1')
    time.sleep(0.1)
    cf.param.set_value('kalman.resetEstimation', '0')
    time.sleep(2)

# def height_log(scf):
#     log_config = LogConfig(name='Height', period_in_ms=1000)
#     log_config.add_variable('stateEstimate.z', 'float')

#     with SyncLogger(scf, log_config) as logger:
#         for log_entry in logger:
#             data = log_entry[1]
#             print(data)


def poshold(cf, t, z):

    steps = t * 10

    for r in range(steps):
        cf.commander.send_hover_setpoint(0, 0, 0, z)
        time.sleep(0.1)

def consensus(currentPosition):
    if len(currentPosition) == 2: 
        nextPos[0] = 0.5 *(currentPosition[0] + currentPosition[1])
        nextPos[1] = 0.5 *(currentPosition[0] + currentPosition[1])
        #print(nextPos)

    elif len(currentPosition) == 3:
        nextPos[0] = 0.5   *(currentPosition[0] + currentPosition[1])
        nextPos[1] = 0.333 *(currentPosition[0] + currentPosition[1] + currentPosition[2])
        nextPos[2] = 0.5   *(currentPosition[1] + currentPosition[2])


def run_sequence(scf, params):
    cf = scf.cf
    base = params['base']
    z = params['h']


    # Base altitude in meters
    end = 0.3
    base = params['base']
    h = params['h']
    num = params['num']

    if num == 0:
        f = open('height2.txt','w')
        f.write(-1.1)
        f.close()

    #poshold(cf, 2, base)
    #poshold(cf, 5, h)
    i = 0
     # The definition of the logconfig can be made before connecting
    log_config = LogConfig(name='Height', period_in_ms=50)
    log_config.add_variable('stateEstimate.z', 'float')
    with SyncLogger(scf, log_config) as logger:
        endTime = time.time() + 10
        for log_entry in logger:
            data = log_entry[1]
            currentPos[num] = data['stateEstimate.z']
            if num == 0:
                f = open('height.txt','r')
                parrotHeight = f.read()
                f.close
                if parrotHeight > 1.6:
                    parrotHeight = parrotHeight*0.1
                currentPos[2] = parrotHeight

            while currentPos[0] == 0 or currentPos[1] == 0 or currentPos[2] == 0:
                time.sleep(0.001)
                print('wait')
            #print(currentPos)
            if num == 0:
                consensus(currentPos)
            while nextPos[0] == 0 or nextPos[1] == 0 or nextPos[2] == 0:
                time.sleep(0.001)
                print('wait2')
            if num == 0:
                f = open('height2.txt','w')
                f.write(nextPos[2]*-1.0)
                f.close()
            #poshold(cf,1,nextPos[num])

            if time.time() > endTime:
                break

    if num == 0:
        f = open('height2.txt','w')
        f.write(-0.6)
        f.close()   
    #poshold(cf,2,0.35)
    # # Base altitude in meters
    #print(currentPos)
    #poshold(cf, 2, base)
    cf.commander.send_stop_setpoint()


if __name__ == '__main__':
    cflib.crtp.init_drivers(enable_debug_driver=False)

    factory = CachedCfFactory(rw_cache='./cache')

    with Swarm(uris, factory=factory) as swarm:
        swarm.parallel(reset_estimator)
      # swarm.parallel(height_log)
        swarm.parallel(run_sequence, args_dict=params)
