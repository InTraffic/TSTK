Software Summary
====================

Software-application
---------------------
This Test and Simulation Toolkit, from this moment on called TSKT, is a 
combination of an install script and a package containing drivers. With 
this the TSTK it’s possible to install an existing test system, but only
if it has been created using the TSTK. It’s also possible to create an 
environment in which you can develop a new test system. The TSTK also 
provides the possibility to update the test system or developing 
environment. 

With the TSTK the need to create specialized drivers for each test 
system is limited to the translation of messages that are to be sent 
over a connection to your test system. Besides this, the installation, 
distribution and updating of test systems is greatly simplified by just 
executing one script which will do the work for you.

When you have created a test system with the TSTK you can create a 
package for distribution and installation on other systems. This will be
explained in detail in chapter 5.

Software-inventory
---------------------
The TSTK is created to be used on Linux systems. The software that must 
be present on the system for the TSTK to function is:

 - Python 2.7
 - Python 3.2
 - Python-virtualenv
 - Git

Software-environment
---------------------
The environment, in which the TSTK will run, shall have to be composed 
of  computer with the following recommended specifications:

 - Ubuntu 12.04 or similar OS
 - 2GHz Dual core
 - 2 GB RAM
 - 500 MB of free disk space
 - The system is connected to the internet

Software organization and overview of operation
-------------------------------------------------
The TSTK contains the following two components:
 - An install script. This script creates the environment and installs 
   all the drivers.
 - A package containing all drivers for the test system or the test 
   system itself. The contents of the package depend on whether you are 
   installing an existing test system or if you are installing an 
   environment to develop a new test system.

Contingencies and alternate states and modes of operation.  
---------------------------------------------------------------
The installation script will keep a log during the installation. When 
something does not execute as it should, the installation is aborted and
everything will be reversed. This will al be logged.

Assistance and problem reporting
------------------------------------------
For assistance and problem or bug reporting you should go to the GitHub 
page at https://github.com/InTraffic/TSTK .

Problems and bugs should be reported by creating a new Issue, describing
 the problem and with the correct label. This can be found at
 https://github.com/InTraffic/TSTK/issues

For assistance you should check if it hasn’t been mentioned in this 
document. If it hasn’t, you should go to the wiki on the GitHub page at 
https://github.com/InTraffic/TSTK/wiki. If that also doesn’t solve the 
problem, you should create a new issue and attach the “question” label 
to it.
