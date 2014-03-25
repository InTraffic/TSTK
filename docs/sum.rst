User Manual
**********************

Scope
=====================

Identification
---------------------
This document is the Software User Manual (SUM) for the Test and Simulation Toolkit (TSTK). This SUM will explain the possibilities of the TSTK and how to use it. 

System overview
---------------------
The TSTK consists of an install script and a driver package.

Document overview
---------------------
Chapter 3 in this document describes the software and it’s environment requirements. It is recommended to read this chapter if you are going to install a system using the TSTK, just to make sure your that system meets the requirements.

If you are going to use the TSTK for the first time, you should also read chapter 4. This chapter describes how to install and use the TSTK. After you have familiarized yourself with the TSTK you should take a look at Chapters 5 and 6 which describe how to use the drivers and simulators installed by the TSTK.

Software Summary
====================

Software-application
---------------------
This Test and Simulation Toolkit, from this moment on called TSKT, is a combination of an install script and a package containing drivers. With this the TSTK it’s possible to install an existing test system, but only if it has been created using the TSTK. It’s also possible to create an environment in which you can develop a new test system. The TSTK also provides the possibility to update the test system or developing environment. 

With the TSTK the need to create specialized drivers for each test system is limited to the translation of messages that are to be sent over a connection to your test system. Besides this, the installation ,distribution and updating of test systems is greatly simplified by just executing one script which will do the work for you.

When you have created a test system with the TSTK you can create a package for distribution and installation on other systems. This will be explained in detail in chapter 5.

Software-inventory
---------------------
The TSTK is created to be used on Linux systems. The software that must be present on the system for the TSTK to function is
 - Python 2.7
 - Python 3.2
 - Python-virtualenv
 - Git

Software-environment
---------------------
The environment, in which the TSTK will run, shall have to be composed of  computer with the following recommended specifications
 - Ubuntu 12.04 or similar OS
 - 2GHz Dual core
 - 2 GB RAM
 - 500 MB of free disk space
 - The system is connected to the internet

Software organization and overview of operation
-------------------------------------------------
The TSTK contains the following two components:
 - An install script. This script creates the environment and installs all the drivers.
 - A package containing all drivers for the test system or the test system itself. The contents of the package depend on whether you are installing an existing test system or if you are installing an environment to develop a new test system.

Contingencies and alternate states and modes of operation.  
---------------------------------------------------------------
The installation script will keep a log during the installation. When something does not execute as it should, the installation is aborted and everything will be reversed. This will al be logged.

Security and privacy
---------------------
The TSTK is distributed under the GPL v3 license, which is added as appendix A.

Assistance and problem reporting
------------------------------------------
For assistance and problem or bug reporting you should go to the GitHub page at https://github.com/InTraffic/TSTK .

Problems and bugs should be reported by creating a new Issue, describing the problem and with the correct label. This can be found at https://github.com/InTraffic/TSTK/issues

For assistance you should check if it hasn’t been mentioned in this document. If it hasn’t, you should go to the wiki on the GitHub page at https://github.com/InTraffic/TSTK/wiki. If that also doesn’t solve the problem, you should create a new issue and attach the “question” label to it.

Access to the software
========================
This chapter assumes that the software from paragraph 3.2 has been installed on the computersystem and that the environment meets the specified requirements.

First time user of the software
-----------------------------------------

Equipment familiarization
############################################
To access the TSTK you will have to download the install script from the GitHub page.
When you have downloaded the script, you can execute the following steps to show the possibilities:

 - Open a new terminal window.
 - Navigate to the folder where the install script has been downloaded, or moved, to.
 - Type this command: ``python2.7 TSTK-install.py --help``
 - Hit the enter key to execute the command
 - You will now be shown the possible options and argument you can pass to the install script.

The possible options and arguments are displayed below::

    Test and Simulation Toolkit installer script

    Usage:
    installscript.py install (existing TESTSYSTEM| 
                            development TOOLKIT_PACKAGE) 
                           [options...] FOLDER
    installscript.py update FOLDER (PACKAGE...)
    installscript.py -h | --help
    
    Arguments:
     TESTSYSTEM This is the package containing the testsystem that is to be 
                installed
     FOLDER     This is the folder that'll be created for the testsystem to 
                reside in. When updating this is the folder containing the 
                current testsystem.
     TOOLKIT_PACKAGE  
                The package to use when setting up the environment for
                development.
     PACKAGE    The package to update to.
    
    Options:
     -l <package>, --local-packages <package>  
                Use this when you want to  install additional 
                packages from the current folder. The input should
                be a tarball.
     -e <package>, --external-packages <package>  
                Use this when you want to install additional 
                packages from PyPI.
     --no-virtualenv    
                Using this option will result in an OS wide install of the 
                toolkit. It is NOT recommended to use this argument unless 
                you know what you're doing and are willing to risk 
                destabilizing your current package "ecosystem". 
                Use at your own risk!
    

Installation and setup
#######################
The install script has to be downloaded, that’s it. The directory it resides in should allow for executing programs,though.

Initiating a session
-------------------------

Initiating the installation of a development environment
###########################################################

The initiation of the installation of a development environment is as follows::

    Python2.7 TSTK-installscript.py install development [toolkit_package] [folder]

[toolkit_package] should be substituted with the package containing the drivers. Either a path (eg. /foo/bar/baz.tar.gz), a relative path (eg. foo/baz.tar.gz) or a package name (eg. baz.tar.gz or baz) is accepted. When only the package name is provided, without the .tar.gz file extension, the TSTK will get the package from the Python Package Index.

[folder] should be substituted with the folder you want to create for the environment to reside in. Either a path (eg. /foo/bar/baz), a relative path (eg. foo/bar) or a foldername (eg. baz or baz/) is accepted.

The result of the above command will be a folder, with the specified name, containing a virtual environment with the default driver package installed. There will also be a Git repository initiated in this folder, since a development environment is set-up.

Initiating the installation of an existing test system
#############################################################
The initiation of the installation of an existing system is similar to the installation of a development environment, it is as follows::

    Python2.7 TSTK-installscript.py install existing [package] [folder]

[folder] should be substituted with the folder you want to create for the environment to reside in. Either a path (eg. /foo/bar/baz), a relative path (eg. foo/bar) or a foldername (eg. baz or baz/) is accepted.

[package] should be substituted with the tarball of the test system package you want to install. Either a path to a package, a relative path to a package or a just a package is accepted.

The result, of the above command, will be a folder with the specified name. It will contain a virtual environment, and the testsystem installed within. 
 
Initiating the update of a test system or development environment
####################################################################
To initiate the update of an existing system you use the following command::

    Python2.7 TSTK-installscript.py update [folder]

[folder] should be substituted with the folder where the testsystem or development environment resides in. It will update the default set of drivers for you.

Initiating the installation and using the options
###################################################
The install script accepts three options you can use when running the script.These options are:
 
 - local-packages. This option enables you to specify a tarball, specifically a python package, that is installable through PIP. This tarball will then be installed in the virtual environment by the install script. 
 - external-packages. This option enables you to specify a package on PyPI. This package will be downloaded and installed in the virtual environment by the install script.
 - no-virtualenv. This option will cause the installation script to install all pakages in the system-wide environment. WARNING: This can cause unforseen problems and stability/dependency issues. *Use this only when you know what you are doing and at you own risk!* 

An example of the syntax for the use of local-package or external package is:
Python2.7 TSTK-installscript.py install development –l Foo.tar.gz /foo/bar/baz
To install multiple local packages you have to repeat te option, like:
Python2.7 TSTK-installscript.py install development -l foo.tar.gz –l bar.tar.gz baz/

Stopping and suspending work
-----------------------------
To stop the install script during the installation just hit ctrl + C. The installation will be aborted and the changes will be reverted.




