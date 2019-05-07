
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

#  Copyright © 2019 The Regents of the University of Michigan


# This program logs the current height of the drone for 10 seconds
# Drone doesn't fly during this; it was just my work towards learning how 
# to log drone height and be able to use that height as the drone is still
# running.


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
URI0 = 'radio://0/80/2M/E7E7E7E7E8'

params0 = {'base': 0.15, 'h': 1.0, 'num': 0}

uris = {
	URI0,
}

params = {
	URI0: [params0],
}

currentPos = [0]
nextPos = [0]

def reset_estimator(scf):
	cf = scf.cf

	cf.param.set_value('kalman.resetEstimation', '1')
	time.sleep(0.1)
	cf.param.set_value('kalman.resetEstimation', '0')
	time.sleep(2)



def run_sequence(scf, params):
	cf = scf.cf



	# Base altitude in meters
	end = 0.3
	base = params['base']
	h = params['h']
	num = params['num']

	 # The definition of the logconfig can be made before connecting
	log_config = LogConfig(name='Height', period_in_ms=50) #period of height data
	log_config.add_variable('stateEstimate.z', 'float') #stateEstimate.z is the height
	with SyncLogger(scf, log_config) as logger:
		#sets the runtime
		endTime = time.time() + 10
		j = 0
		time_elapsed = float(0)

		for log_entry in logger:
			timestamp = log_entry[0] # log_entry[0] is a time variable
			data = log_entry[1] # log_entry[1] is the data being logged stored in I think a dictionary
			currentPos[num] = data['stateEstimate.z']
			
			#first run through sets the begin time of the drone
			if j == 0:
				begin_T = timestamp
				j = 1
				time.sleep(7)
			
			else:
				time_elapsed = float((timestamp - begin_T))/1000
			
			#prints the current position every second
			if time_elapsed.is_integer():
				print(currentPos[num])
				print(int(time_elapsed) % 3)
			
			#ends program after endTime seconds
			if time.time() > endTime:
				break
	print('end')
	cf.commander.send_stop_setpoint()


if __name__ == '__main__':
	cflib.crtp.init_drivers(enable_debug_driver=False)

	factory = CachedCfFactory(rw_cache='./cache')

	with Swarm(uris, factory=factory) as swarm:
		swarm.parallel(reset_estimator)
		swarm.parallel(run_sequence, args_dict=params)
