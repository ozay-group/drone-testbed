# Drone-Testbed
Consensus and fault detection in drones


swarmSequenceCircle.py - initial attempt to running the 3 drone simple consensus algorithm - without logging the height.

basiclog.py - A look at how the drone's logging system works + how to read the logged data back to the computer; prints out the height estimate of the drone.

LogTimingTestSuccess.py - Applied basiclog.py concepts while the drone is flying to print out it's height every second for 10n seconds while the drone is in the air.

swarmConsensuAlg2.py - Implemented the height saving into a 3 drone simple consensus algorithm - first iteration of this program.

swarmConsensusAlgWithHeightSave_old.py - Initial implementation of the 3 drone simple consensus algorithm. Saves a log of the heights to testing1, testing 2, and testing3.csv

swarmConsensusAlgWithHeightSave.py - Final implementation of the 3 drone simple consensus algorithm. Saves a log of the heights to testing1, testing 2, and testing3.csv

swarmConsensusAlgWithHeightSave_fivedrones.py - Final implementation of the 5 drone simple consensus algorithm. Saves a log of the heights to testing1-testing5.csv

swarmConsensusAlgWithHeightSave_fivedrones_twoalgs.py - Implementation of a 5 drone consensus algorithm with the algorithm switching every 2 seconds

test.py  - File used to test various concepts before implementing in others.

swarmConsensusAlg3.py - Runs the consensus algorithm with two crazyflie drones and one parrot minidrone. (before we had 3+ flowdecks to fly 3+ crazyflie drones)

autonomousSequence.py - Basic use of Loco Positioning System in TWR mode.

swarmSequence.py - An attempt to fly multiple drones with LPS (not successful)

faultdetectionLP: An LP based fault detection in drones with switching topology. Though we were able to get a few experiments running, most of the times, the drones crashed. One reason may be the fact that PulP requires an old version of Python to run and we were using command "sudo python" instead of "sudo python3".

FDLP3: Working version of faultdetectionLP for three drones.

FDLP5: Working version of faultdetectionLP for five drones.

