Simulator Module reference guide
*********************************

Capabilities
=================
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
==================================

Configuring your simulators
-----------------------------
To configure your simulator yo uneed to specify some things for the 
dispatcher part in the ``simulator.conf`` file. The config files are 
parsed by the configparser module from the python libraries. An example 
of this is::

    [dispatcher-tcp-2]
    MessagePath=/home/foo/bar/
    AcceptAddress=127.0.0.1
    ListenPort=9010
    CommandListenPort=9000
    MessageForwardPort=9001

The entries in the config file that the dispatchers look for are:

 - MessagePath
 - CommandListenPort
 - MessageForwardPort

The dispatchers, excluding the serial dispatcher, also look for the 
following entries:

 - AcceptAddress
 - Listenport

Starting a simulator
-----------------------------

Starting a simulator is quite a simple thng to do. You import the 
simulator module with ``import simulator``. Then you just excecute the 
``simulator.start_simulator("simulator_type", simulator_id)`` function 
with the correct simulator type and id as arguments. 

The simulator module will start a new simulator of the specified type 
and with the given id. It will use this type and id to look for the 
config entries as specified in the above "Configuring your simulators" 
piece.


















