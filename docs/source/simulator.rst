Simulator Module
***********************

Software reference guide
=========================

Capabilities
-------------
The simulator module contains multiple kinds of Simulators. The 
Simulators consist three parts:

 1. A daemon
 2. A dispatcher
 3. A message

The simulator module contains an AbstractFactory which will allow you to
get the desired concrete Daemon and Dispatcher. The specific message has
to be created by the developers that use the TSTK to create a new 
Testlab. The location of the message.py file that contains the specific 
message has to be specified in the ``simulator.conf`` file.

How to use the Simulator module
---------------------------------

Start_simulator function
===========================

.. automodule:: simulator
    :members:

Connection Factory
=======================

.. automodule:: connectionfactory
    :members:

Daemon
=======================

.. automodule:: daemon
    :members:

    
    
Dispatcher
=======================

.. automodule:: dispatcher
        :members:
    

