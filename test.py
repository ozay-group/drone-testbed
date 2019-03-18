# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2017 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.

import math
import csv
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
URI0 = 'radio://0/80/2M/E7E7E7E7EB'

#paramaters
params0 = {'base': 0.15, 'h': 1.0, 'num': 0}


uris = {
	URI0,
}

params = {
	URI0: [params0],
}

savelog = []

def reset_estimator(scf):
	cf = scf.cf

	cf.param.set_value('kalman.resetEstimation', '1')
	time.sleep(0.1)
	cf.param.set_value('kalman.resetEstimation', '0')
	time.sleep(2)


def poshold(cf, t, z):

	steps = int(t * 10)

	for r in range(steps):
		cf.commander.send_hover_setpoint(0, 0, 0, z)
		time.sleep(0.1)

def _a_alt_kp_callback(self, name, value):
	"""Callback for pid_attitude.pitch_kd"""
	print('Readback: {0}={1}'.format(name, value))

def run_sequence(scf, params):
	cf = scf.cf
	base = params['base']
	h1 = 0.5
	h2 = 0.7

	# Base altitude in meters


	poshold(cf, 3, base)
	poshold(cf, 3,1)
	poshold(cf,3,2)
	poshold(cf,3,1)
	poshold(cf,3,base)

	# k = 0
	#  # The definition of the logconfig can be made before connecting
	# log_config = LogConfig(name='Height', period_in_ms=100)
	# log_config.add_variable('stateEstimate.z', 'float')
	# with SyncLogger(scf, log_config) as logger:
	# 	endTime = time.time() + 30
	# 	j = 0
	# 	time_elapsed = float(0)
	# 	for log_entry in logger:
	# 		timestamp = log_entry[0]
	# 		data = log_entry[1]
	# 		currentPos = data['stateEstimate.z']
	# 		if j == 0:
	# 			begin_T = timestamp
	# 			j = 1
	# 			for x in range(5):
	# 				poshold(cf,1.5,h1)
	# 		else:
	# 			time_elapsed = float((timestamp - begin_T))/1000
	# 			if (time_elapsed%7.5) == 0 and k == 0:
	# 				for x in range(5):
	# 					poshold(cf,1.5,h2)
	# 				k = 1
	# 			elif (time_elapsed%7.5) == 0 and k == 1:
	# 				for x in range(5):
	# 					poshold(cf,1.5,h1)
	# 				k = 0

	# 		savelog.append([time_elapsed,currentPos])

	# 		if time.time() > endTime:
	# 			break

	# poshold(cf, 2, base)
	# str1 = 'testing'
	# str2 = '.csv'
	# with open(str1+str2, 'w') as f:
	# 	writer = csv.writer(f, delimiter=',')
	# 	writer.writerows(savelog) 
	cf.commander.send_stop_setpoint()


if __name__ == '__main__':
	cflib.crtp.init_drivers(enable_debug_driver=False)

	factory = CachedCfFactory(rw_cache='./cache')

	with Swarm(uris, factory=factory) as swarm:
		swarm.parallel(reset_estimator)
	  # swarm.parallel(height_log)
		swarm.parallel(run_sequence, args_dict=params)
