# vi: spell spl=en

"""Classes and function to execute test scenario's
"""
#-----------------------------------------------------------
import time
import signal      # To capture control C
import logging
import subprocess  # To start simulation processes
import sys
import os
import zmq
import re

from queue             import PriorityQueue
from inspect           import getargspec
#-----------------------------------------------------------


class ScenarioPlayerException(Exception):
    """Base class for ScenarioPlayer exceptions"""
    pass

class TimeSpecException(Exception):
    """Exception for bad timespecs"""
    pass

class ScenarioPlayer(object):
    """Stores and executes test scenario's"""
    def __init__(self, test_system):
        #: queue for the test steps
        self.priority_queue = PriorityQueue()
        self._start_time = None

        #: flag to indicate a scenario should be run or stopped
        self.runit = 1

        #: array with information about which function to call
        #: when data arrives at a particular socket.
        self.call_backs = {}
        self.logger = logging.getLogger('ScenarioPlayer')

        #: test system this scenario is part of
        self.test_system = test_system
        self.old = signal.signal(signal.SIGINT, self.control_c_handler)

        #: zmq context
        self.context = zmq.Context(1)

        #: zmq poller to poll all registered sockets
        self.poller  = zmq.Poller()


    # The unused parameters are signal and frame.
    # these are not needed for a controlled stop.
    # pylint: disable=W0613
    def control_c_handler(self, unused1, unused2):
        """Handler for control C

        Stops the scenario and logs the event.

        :param unused1: signal, but is not used.
        :param unused2: frame, but s not used.
        """
        # Log that we were stopped by a control C
        self.logger.info("User requested a scenario stop via CTRL-C ")
        # try a controlled stop
        self.stop()


    def add_step( self, when, priority, step):
        """Add the given step to the list of scenario steps.
        :param when: tells when it is to be executed.

        The steps in scenario are executed approximately at the time 
        specified. If the time interval between two steps is large
        (1 s or more) it will be a close approximation.  If the time 
        interval is small (<0.1) the execution can be slightly delayed. 
        :type when: int, float, string
        :param step: a reference to a function that takes a
        single parameter, a reference to the scenario player.
        :type step: function

        ``when``  

        If ``when`` is a number, it is interpreted
        as being a number of seconds.

        ``when`` can also be a string of the following format:
        "mm:ss.ss"

        For instance:

        * "00:30"    means 30 seconds
        * "01:40"    means 1 minute 40 seconds
        * "00:00.5"  means 0.5 a second

        Note that this method behaves differently according to when it 
        is called:

        * If it is called before the scenario is started, ``when``
          indicates offset from when the scenario is actually started.
        * If it is called after the scenario is started, ``when``
          indicates the number of seconds from when the method is called

        :param priority: A secondary priority, required when there are two
        "when" values in the queue that are the same.
        :type priority: integer
        """
        if not isinstance(when, int):
            if not isinstance(when, float):
                when = parse_timespec(when)

        if not self._start_time is None:
            # Scenario is running. Need to add an offset to the 
            # delta_time to keep the queue properly sorted.
            current_time = time.time()
            offset = current_time - self._start_time
            when = when + offset

        self.priority_queue.put((when, priority, step))


    def execute_step(self, step):
        """
        Execute the given step and log this.
        
        :param step:a reference to a function that takes a
        single parameter, a reference to the scenario player.
        :type step: function 
        """
        argspec = getargspec(step)
        # Execute the step
        # Does the step require a parameter?
        if len(argspec.args) > 0 and argspec.args[0] == 'self' :
            if len(argspec.args) == 2:
                step(self.test_system)
            else :
                step()
        else:
            if len(argspec.args) == 1:
                step(self.test_system)
            else :
                step()
        self.logger.info("executing " + str(step))


    def play(self):
        """
        Play the current scenario.

        Uses select() to wait for passing of time until the next step 
        in the scenario and for events on the registered sockets or 
        other file handles.
        """
        self.runit = 1
        self._start_time = time.time()
        self.logger.info("starting scenario")
        last_commit_time = time.time()
        while (not self.priority_queue.empty()) and (self.runit):
            # Next step in the scenario
            (delta_time, step) = self.priority_queue.get()

            current_time = time.time()
            # When should the step fire?
            expected_time = self._start_time + delta_time
            # print expected_time, current_time
            if (current_time >= expected_time):
                self.execute_step(step)
            else:
                # This results in a dictionary that contains
                # as a key the fileno to normal sockets, or
                # the reference to a zmq socket.
                # The value is the status  (zmq.POLLIN)
                socks = dict(self.poller.poll( 
                    1000*(expected_time - current_time)))
                # Enough time has passed?
                current_time = time.time()
                if (current_time >= expected_time):
                    self.execute_step(step)
                else:
                    # Put the step back in the queue, because handling 
                    # of the filehandle event might add new events that
                    # come before this event.
                    delta_time = expected_time - current_time
                    self.add_step(delta_time, step)
                    # Handle the filehandle events
                    for socket_key in self.call_backs.copy(): 
                            # Need copy here cause we might modify 
                            # the call_backs while in the call back
                            # functions.
                        if socket_key in socks and ( 
                                socks[socket_key] == zmq.POLLIN):
                            callb = self.call_backs[socket_key]
                            function = callb[1]
                            function(callb[0], self)


    def stop(self):
        """Stop the current scenario.

        Once stopped a scenario cannot be resumed.
        """
        self.runit = 0


    def add_socket(self, a_socket, call_back_function):
        """Add the given socket to the list of sockets to be watched.

        :param a_socket: Socket to add
        :type a_socket: socket or zmq socket
        :param call_back_function: function to register in call_backs
        :type call_back_function: function

        If data arrives on the socket, the given call back function is
        called with as parameters the socket and a reference to the 
        scenario player.
        """
        self.logger.info("adding socket " + str(a_socket))
        self.poller.register(a_socket, zmq.POLLIN)
        # This is needed because poller.poll returns
        # a list with filenumbers for normal sockets andl
        # references to zmq sockets.
        try:
            self.call_backs[a_socket.fileno()] = ( 
                    a_socket, call_back_function)
        except AttributeError:
            # This handles zmq sockets.
            self.call_backs[a_socket] = ( 
                    a_socket, call_back_function)

    def remove_socket(self, a_socket):
        """Remove the given socket from the lost of socket to 
        be watched.
        
        :param a_socket: Socket to add
        :type a_socket: socket or zmq socket
        """
        self.logger.info("removing socket " + str(a_socket))
        self.poller.unregister(a_socket)
        try:
            del self.call_backs[a_socket.fileno()]
        except AttributeError:
            del self.call_backs[a_socket]

def parse_timespec(timespec):
    """
    Parse a time string and convert to seconds.

    Parse a time specification of the format::

       HH:MM:SS.ss

    and convert it to the total number of seconds.

    :raises: TimeSpecException in case the parsing fails.
    :returns: a floating point number otherwise.
    """
    match = re.match(r"(\d\d):(\d\d):(\d\d.\d+|\d\d)", timespec)
    if match is None :
        match = re.match(r"(\d\d):(\d\d\.\d+|\d\d)", timespec)
        if match is None :
            raise TimeSpecException("Incorrect time specification "
                    + timespec)
        else:
            seconds = float(match.group(1))*60 + \
                      float(match.group(2))
    else:
        seconds = float(match.group(1)) * 3600.0 + \
                  float(match.group(2))*60 + \
                  float(match.group(3))

    return seconds

