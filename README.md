# Drone-Testbed
Consensus and fault detection in drones
************************************************************************
Folder - Miscellaneous test files

test.py  - File used to test various concepts before implementing in others.

autonomous_sequence.py - Basic use of Loco Positioning System in TWR mode.
************************************************************************
Folder - Swarm Consensus

avg_consensus_cf_parrot.py - Implementation of the average consensus on two CrazyFlie drones and one parrot mini-drone with height logging feature.

avg_consensus_five_log_height.py - Final implementation of the 3 drone simple consensus algorithm. Saves a log of the heights to testing1, testing 2, and testing3.csv

avg_consensus_five_log_height.py - Implementation of the average consensus algorithm for 5 drones with the height loggin feature. Saves a log of the heights to testing1-testing5.csv

switch_consensus_five_log_height.py - Implementation of consensus on a network of 5 CrazyFlie drones with the network topology switching every 2 seconds.
************************************************************************

Folder - Fault-Detection

fd_three: Implemenetation of fault detection on consensus in three drones using Linear Programming. The concept used in Model Invalidation.

fd_five: Implemenetation of fault detection on consensus in five drones using Linear Programming. The concept used in Model Invalidation.
************************************************************************
Folder - how to log data

log_data.py -  A look at how the drone's logging system works + how to read the logged data back to the computer; prints out the height estimate of the drone.

flight_log_data - Applied log_data.py concepts while the drone is flying to print out it's height every second for 10n seconds while the drone is in the air.
************************************************************************

Folder - Backup (Old codes/unsuccesful attempts, provided for pedagogical purpose)

avg_consensus_cf.py - Implementation of the average consensus on two/three CrazyFlie drones with height logging feature.

swarm_sequence_unsucceful.py - An attempt to fly multiple drones with LPS (not successful)

fd_five_old: An LP based fault detection in drones with switching topology. Though we were able to get a few experiments running, most of the times, the drones crashed. One reason may be the fact that PulP requires an old version of Python to run and we were using command "sudo python" instead of "sudo python3".

consensus_saveheight_old.py - Initial implementation of the 3 drone simple consensus algorithm. Saves a log of the heights to testing1, testing 2, and testing3.csv

avg_consensus_three_cf_initial.py - initial attempt to running the 3 drone simple consensus algorithm - without logging the height.
