#! /usr/bin/env python
"""Test and Simulation Toolkit installer script

Usage:
 TSTK-installscript.py install (existing TESTSYSTEM| 
                           development TOOLKIT_PACKAGE) 
                          [options...] FOLDER
 TSTK-installscript.py update FOLDER (PACKAGE...)
 TSTK-installscript.py -h | --help

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
"""

import subprocess
import textwrap
import sys
import logging

import virtualenv
from docopt import docopt

# The setup for the argument parser.
args = docopt(__doc__)

# Assign passed arguments to variables.
foldername = args.get('FOLDER')
local_packages = args.get('--local-packages')
external_packages = args.get('--external-packages')
install = args.get('install')
update = args.get('update')
toolkit_package = args.get('TOOLKIT_PACKAGE')
update_packages = args.get('PACKAGE')
existing = args.get('existing')
test_system = args.get('TESTSYSTEM')
development = args.get('development')
no_virtualenv = args.get('--no-virtualenv')

# A list containing the commands executed by this script.
cleanup_command_list = []

# Set-up logging
logger= logging.getLogger('installscript.{0}'.format(foldername))
logger.setLevel(logging.DEBUG)
logfile = 'installscript_{0}.log'.format(foldername)
filehandler = logging.FileHandler(logfile)
filehandler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -'
                              '%(message)s')
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)


# Add a log entry on the debug level to log the given arguments.
logger.debug("The given arguments for this installation:{0}".format(
             ', '.join('{0}'.format(item) for item in args.items())))

try:
    if install:
        # Creating the new folder for the testing environment
        mkdir_command = ["mkdir", "{0}-project/".format(foldername)]
        mkdir_command.append("{0}-project/{0}/".format(foldername))
        mkdir_command.append("{0}-project/{0}/docs".format(foldername))
        mkdir_command.append("{0}-project/{0}/{0}".format(foldername))
        mkdir_command.append("{0}-project/{0}/{0}/test".format(foldername))
        logger.debug("Executing mkdir command: {0}".format(mkdir_command))

        # Checking if the subprocess call is executed without an error. If 
        # it does it returns 1, otherwise it returns 0.If an error occurs 
        # we'll stop the installation, and let the exception be handled in 
        # the catch statement below.This is the same at each point during 
        # the installation procedure and it'll clean up the mess we've made.
    
        if subprocess.call(mkdir_command):
            error_message = ("Error: The folder: '{0}' already exists"
                             .format(foldername))
            logger.critical(error_message)
            sys.exit(error_message)
        else:
            logger.info("({0}) executed successfully.".format(mkdir_command))
            cleanup_command_list.insert(0, ["rm", "-rf", foldername])
            logger.debug('Adding command (["rm", "-rf", {0}]) to cleanup list'
                         .format(foldername))
        # use touch to create empty files in the directories
        touch_command = ["touch",]
        touch_command.append("{0}-project/{0}/README.txt".format(foldername))
        touch_command.append("{0}-project/{0}/setup.py".format(foldername))
        touch_command.append("{0}-project/{0}/{0}/__init__.py".format(foldername))
        touch_command.append("{0}-project/{0}/{0}/test/__init__.py"
                             .format(foldername))
        logger.debug("Executing touch command: {0}".format(touch_command))

        if subprocess.call(touch_command):
            error_message = ("Error while executing touch command")
            logger.critical(error_message)
            sys.exit(error_message)
        else:
            # It is nog required to add a cleanup command for this, it 
            # will be cleaned up by the same command as the one from the
            # mkdir command.
            logger.info("({0}) executed successfully.".format(touch_command))
        
        # Copy the tarballs containing the Packages that are to be installed
        # to the folder that contains the testing environment.
        copy_command = ["cp"]
        if (development) and ('.tar.gz' in toolkit_package):
            copy_command.append(toolkit_package)
        elif (development) and ('tar.gz' not in toolkit_package):
            external_packages.append(toolkit_package)
            
    
        # Add the package for the test system to the local packages list.
        if existing:
            local_packages.append(test_system)

        for arg in local_packages:
        	copy_command.append(arg)

        copy_command.append("{0}-project/".format(foldername))
        logger.debug("Executing copy command: {0}".format(copy_command))
        if subprocess.call(copy_command):
            error_message = "Error: copy command '{0}' failed".format(copy_command)
            logger.critical(error_message)
            sys.exit(error_message)
        else: 
            logger.info("({0}) executed successfully.".format(copy_command))

    
        if not no_virtualenv:
            logger.info("creating virtualenv bootstrap script")
            # Generate a custom bootstrap script with the function provided 
            # by virtualenv. This bootstrap script is used to create the 
            # virtualenv. Added in this script is the 'after_install' 
            # function, which'll be called by the script when it is finished
            # installing the virtualenv itself. We use this 'after_install' 
            # function to automatically install the packages specified in 
            # the arguments at the commandline.
            output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import os, subprocess
def after_install(options, home_dir):

    package_install_cmd = None
    pip_path = ('{{a}}/bin/pip').format(a=home_dir)
    extra_packages = {0}
    if extra_packages is not None:
        package_install_cmd = [pip_path, 'install'] + extra_packages

    packages_to_install = {1}
    if packages_to_install is not None:
        for package in packages_to_install:
            package_install_cmd.append('{{0}}/{{1}}'.format(home_dir,package))
    if package_install_cmd is not None:
        subprocess.call(package_install_cmd)
""").format(external_packages, local_packages))
            f = open((foldername + '-virtualenv-bootstrap.py'), 'w').write(output)
            logger.info("Bootstrapscript created "
                        "({0}-virtualenv-bootstrap.py)".format(foldername))
            logger.debug('Adding command (["rm","{0}-virtualenv-bootstrap.py"'
                         ']) to cleanup list'.format(foldername))
            cleanup_command_list.insert(0, ["rm", "{0}-virtualenv-bootstrap.py"
                                                  .format(foldername)])

            # Creating the virtualenv by executing the bootstrap script we 
            # just generated. This is called using the '-p /usr/bin/python3'
            # to make python3 the default version in the virtualenv. This is
            # to encourage development in python3 because it is the future, 
            # and python2 will slowly die.
            logger.info("Installing virtualenv")
            subprocess.call(["python", (foldername +"-virtualenv-bootstrap.py"), 
                             "-p", "/usr/bin/python3.2", 
                             "{0}-project".format(foldername)])
            subprocess.call(["virtualenv", "-p", "/usr/bin/python2.7",
                             "{0}-project/".format(foldername)])
        elif no_virtualenv:
            logger.info("Not creating a virtualenv to install everything in")
            package_install_cmd = [pip_path, 'install'] + external_packages
            for package in local_pacakages:
                package_install_cmd.append(package)
            subprocess.call(package_install_cmd)
            logger.info("installing packages ({0})".format(package_install_cmd))

	
        # Cleaning up the files used for installing
        logger.info("cleaning up files used during install")
        logger.debug('removing the bootstrapscript for the virtualenv (["rm",'
                     '"{0}-virtualenv-bootstrap.py")'.format(foldername))
        subprocess.call(["rm","{0}-virtualenv-bootstrap.py"
                         .format(foldername)])
        for arg in local_packages:
            arg
            subprocess.call(["rm", (foldername + "/{0}".format(arg))])
            logger.debug('removing the additional local package(s) '
                         '(["rm","{0}/{1}]")'.format(foldername, arg))

        if development:
            # Initialize a Git repository in the folder.
            logger.info("Initializing a new Git repository in "
                        "{0}-project/".format(foldername))
            subprocess.call(["git", "init", "{0}-project/".format(foldername)])
    elif update:
        update_command = ["{0}-project/bin/pip".format(foldername), "--upgrade"]
        for package in update_packages:
            update_command.append(package)
        
        logger.debug("Running the following command to update"
                     " packages:{0}".format(update_command))

        if subprocess.call(update_command):
            logger.critical("Something failed during updating of packages")
            

except (SystemExit, KeyboardInterrupt):
    # If the script is stopped by sys.exit() or ctrl+c we'll take the 
    # opportunity to clean up after ourselves.
    logger.critical("Something went wrong during the installation, aborting")
    logger.info("reversing the changes made during installation")
    for command in cleanup_command_list:
        err = subprocess.call(command)
        if err:
            logger.error("{0} command executed unsuccessfully"
                         .format(' '.join(command)))
        elif not err:
            logger.info("{0} executed successfully".format(command))
        else:
            logger.error("{0} command returned with unknown code: {1}"
                         .format(command, err))

