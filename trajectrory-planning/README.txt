The following python scripts use the idea of 'flowsequenceSync.py' from the crazyflie library. 
---------------------------------------------------------------------------------------------

Python Scripts

---------------------------------------------------------------------------------------------
keyboard.py- controlling the crazyflie using computer keyboard keys.

real_time.py- displaying the real time animation of the crazyflie trajectory in 2D.

Error_minimization.py- minimizing the error between the logged data and expected data using the idea of average deviation and mean method.

swarm.py- read the control sequence files from the MILP(mixed integer linear programming) solver and generate the path for the 2 drones. it logs data for both of the crazyflies and plot thier respective trajectory.

----------------------------------------------------------------------------------------------

CSV files

----------------------------------------------------------------------------------------------
imprt3.csv- a control sequence(velocity and time) generated from MILP solver and loaded to the first crazyflie.

imprt4.csv- a control sequence(velocity and time) generated from MILP solver and loaded to the second crazyflie.
