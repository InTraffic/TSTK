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

from Queue             import PriorityQueue
from inspect           import getargspec
#-----------------------------------------------------------


class ScenarioPlayerException(Exception):
    """Base class for ScenarioPlayer exceptions"""
    pass


class ScenarioPlayer(object):
    """Stores and executes test scenario's.

    Attributes:

    * call_backs -- array with information about which function to call
      when data arrives at a particular socket. (TODO REMOVE)
    * priority_queue -- queue for the test steps,
    * runit -- flag to indicate a scenario should be run or stopped,
    * event_store -- the event store,
    * test_case -- test case this scenario is part of,
    * poller -- zmq poller to poll all registered sockets,
    * context -- zmq context.

    """
    def __init__( self, event_store, test_case, system_name ):
        self.priority_queue = PriorityQueue()
        self._start_time = None
        self.runit = 1
        self.call_backs  = {}
        self.event_store = event_store
        self.logger      = logging.getLogger( 'ScenarioPlayer' )
        self.test_case   = test_case
        self.old = signal.signal( signal.SIGINT, self.control_c_handler )

        self.context = zmq.Context(1)
        self.poller  = zmq.Poller()


    # The unused parameters are signal and frame.
    # these are not needed for a controlled stop.
    # pylint: disable=W0613
    def control_c_handler( self, unused1, unused2 ):
        """Handler for control C

        Stops the scenario and logs the event.
        """
        # Log that we were stopped by a control C
        self.logger.info( "User requested a scenario stop via CTRL-C " )
        # try a controlled stop....
        self.stop()


    def add_step( self, when, step, show, question ):
        """Add the given step to the list of scenario steps.

        The parameter ``step`` is a reference to a function that takes a
        single parameter, a reference to the scenario player.

        ``when`` tells when it is to be executed.
        The steps in scenario are executed approximately at the time specified
        If the time interval between two steps is large
        (1 s or more) it will be a close approximation.  If the time interval
        is small (<0.1) the execution can be slightly delayed. 

        If ``when`` is a number, it is interpreted
        as being a number of seconds.

        ``when`` can also be a string of the following format: "mm:ss.ss"

        For instance:

        * "00:30"    means 30 seconds
        * "01:40"    means 1 minute 40 seconds
        * "00:00.5"  means 0.5 a second

        Note that this method behaves differently according to when it is
        called:

        * If it is called before the scenario is started, ``when``
          indicates offset from when the scenario is actually started.
        * If it is called after the scenario is started, ``when``
          indicates the number of seconds from when the method is called.

        """
        if not isinstance( when, int):
            if not isinstance( when, float ):
                when = parse_timespec( when )

        if not self._start_time is None:
            # Scenario is running. Need to add an offset to the delta_time
            # to keep the queue properly sorted.
            current_time = time.time()
            offset = current_time - self._start_time
            when = when + offset

        self.priority_queue.put( ( when, step, show, question ) )


    def execute_step( self, step, show, question ) :
        """
        Execute the given step and log this.

        The parameter `show` indicates whether this step should be shown in
        the OTIS Viewer.  The question, if any, will be presented to the user
        in OTIS Viewer.
        """
        argspec = getargspec( step )
        # Execute the step
        # Does the step require a parameter?
        if len( argspec.args ) > 0 and argspec.args[ 0 ] == 'self' :
            if len( argspec.args ) == 2 :
                step( self.test_case )
            else :
                step()
        else:
            if len( argspec.args ) == 1 :
                step( self.test_case )
            else :
                step()
        self.logger.info( "executing " + str( step ) )
        # This takes about 0.1 second, so we do it last.
        if show :
            self.event_store.store_test_step( step, question )


    def play( self ):
        """
        Play the current scenario.

        Uses select() to wait for passing of time until the next step in the
        scenario and for events on the registered sockets or other file handles.
        """
        self.runit = 1
        self._start_time = time.time()
        self.logger.info( "starting scenario" )
        last_commit_time = time.time()
        while (not self.priority_queue.empty()) and (self.runit):
            # Next step in the scenario
            ( delta_time, step, show, question ) = self.priority_queue.get()

            current_time = time.time()
            # When should the step fire?
            expected_time = self._start_time + delta_time
            # print expected_time, current_time
            if ( current_time >= expected_time ):
                self.execute_step( step, show, question )
            else:
                # This results in a dictionary that contains
                # as a key the fileno to normal sockets, or
                # the reference to a zmq socket.
                # The value is the status  (zmq.POLLIN)
                socks = dict( self.poller.poll( 
                    1000*(expected_time - current_time ) ) )
                # Enough time has passed?
                current_time = time.time()
                if ( current_time >= expected_time ):
                    self.execute_step( step, show, question )
                else:
                    # Put the step back in the queue, because handling of the
                    # filehandle event might add new events that come before
                    # this event.
                    delta_time = expected_time - current_time
                    self.add_step( delta_time, step, show, question )
                    # Handle the filehandle events
                    for socket_key in self.call_backs.copy() : 
                            # Need copy here cause we might modify the 
                            # call_backs while in the call back functions.
                        if socket_key in socks and ( 
                                socks[ socket_key ] == zmq.POLLIN ) :
                            callb = self.call_backs[ socket_key ]
                            function = callb[1]
                            function( callb[0], self )
            if current_time - last_commit_time > 1 :
                self.event_store.commit()
                last_commit_time = current_time

        self.event_store.commit()

    def wait_for_answers( self ):
        """Wait until all test steps with questions are answered"""
        if self.event_store.are_there_unanswered_questions() :
            self.add_step( 10, self.wait_for_answers, 
                           show=False, question=None )

    def stop( self ):
        """Stop the current scenario.

        Once stopped a scenario cannot be resumed.
        """
        self.runit = 0


    def add_socket( self, a_socket, call_back_function ):
        """Add the given socket to the list of sockets to be watched.

        If data arrives on the socket, the given call back function is
        called with as parameters the socket and a reference to the 
        scenario player.
        """
        self.logger.info( "adding socket " + str( a_socket ) )
        self.poller.register( a_socket, zmq.POLLIN )
        # This is needed because poller.poll returns
        # a list with filenumbers for normal sockets and
        # references to zmq sockets.
        try:
            self.call_backs[ a_socket.fileno() ] = ( 
                    a_socket, call_back_function )
        except AttributeError:
            # This handels zmq sockets.
            self.call_backs[ a_socket ] = ( 
                    a_socket, call_back_function )

    def remove_socket( self, a_socket ):
        """Remove the given socket from the lost of socket to be watched.
        """
        self.logger.info( "removing socket " + str( a_socket ) )
        self.poller.unregister( a_socket )
        try:
            del self.call_backs[ a_socket.fileno() ]
        except AttributeError:
            del self.call_backs[ a_socket ]

