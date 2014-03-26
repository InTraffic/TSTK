Test System Module reference guide
***********************************

Capabilities
=========================
The Test System module is the core of the Testlab you can create with 
the TSTK. It consists of three parts:

 - The testsystem class.
 - The scenario player.
 - Some simulator interfaces.

The testsystem class is the part where testscripts will interact with 
the Testlab. Testscripts will tell the testsystem what drivers, 
simulatorinterfaces, steps to add and to play or stop playing the steps.
The scenarioplayer  stores all steps for a test and executes them at the 
right time. 

The simulatorinterface(s) are for communicating with the running 
simulator(s), they have to be implemented by the developer(s) who create
a Testlab. A simulatorinterface has to start the correct simulator 
through the simulator module within the TSTK. The simulator sends 
commands to the simulator and can receive replies.

How to use the Test System module
==================================

Creating a simulatorinterface
----------------------------------
To use a simulator interface, a developer for a Testlab must create an 
implementation of a specific simulator interface. If desired it can use
the standard simulatorinterface class as superclass and inherit the 
attributes and methods from it. Be sure to add the new 
simulatorinterface to the list in the ``get_simulator_interface`` 
function in simulatorinterface. 


Using the testsystem
----------------------------------
To use the testsystem, you import it in your testscript with 
``from testsystem import testsystem``. You can then instantiate a new 
object from the TestSystem class to access the different methods as 
described in the "Software Documentation" part of this guide.












