Expanding the TSTK
***************************
This part will explain what to do if you want to extend or expand the 
TSTK. An example of extending/expanding is adding a new driver to the 
driver module.

Part one: Github
===================================
If you want to add something to the driver, you should first have some 
knowledge of Github and the workflow. I recommend you to go to
http://guides.github.com/ and read the guide if you aren't familiar with
it.

Part two: The modules
===============================
The TSTK contains three modules:

 - The testsystem module
 - The driver module
 - The simulator module

The driver and simulator modules are the modules where the most 
extending/expanding is expected. 

Adding to the driver module
------------------------------
To add to the driver module you should add the new class to the 
driver.py file in the driver module folder. After that you should also 
add the reference to the ``get_driver`` function in the same file.

Adding to the simulator module
-------------------------------
To add to the simulator module you have to add a daemon and dispatcher 
to their respective files in the simulator module folder. You should 
also create the corresponding connectionfactory and entry in the list 
with known factories in the abstractconnectionfactory.
