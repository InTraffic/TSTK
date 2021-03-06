"""
From www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
License: Public Domain
"""
import sys, os, time, atexit
from signal import SIGTERM, SIGHUP

class Daemon( object ):
    """A generic daemon class.

    Usage: subclass the Daemon class and override the run() method.
    """

    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null',
            stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile


    def daemonize(self):
        """do the UNIX double fork magic, see Stevens' "Advanced
        Programming in the Unix Environment" for details.
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # Exit first parent.
                sys.exit(0)
        except OSError as err:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (err.errno,
                err.strerror))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent.
                sys.exit(0)
        except OSError as err:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (err.errno,
                err.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        sin = file(self.stdin, 'r')
        sout = file(self.stdout, 'a+')
        serr = file(self.stderr, 'a+', 0)
        os.dup2(sin.fileno(), sys.stdin.fileno())
        os.dup2(sout.fileno(), sys.stdout.fileno())
        os.dup2(serr.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)

    def delpid(self):
        """Remove file with process ID"""
        os.remove(self.pidfile)


    def status(self):
        pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

        try:
            pidf = file(self.pidfile, 'r')
            pid = int(pidf.read().strip())
            pidf.close()
        except IOError:
            pid = None

        message = "Daemon " + sys.argv[0]
        if pid:
            if pid in pids:
                message += " is running\n"
                sys.stderr.write(message)
                sys.exit(0)
            else:
                message += " was started but is NOT running\n"
                sys.stderr.write(message)
                sys.exit(0)
        else:
            message += " is not running\n"
            sys.stderr.write(message)
            sys.exit(0)


    def start(self):
        """Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs.
        try:
            pidf = file(self.pidfile, 'r')
            pid = int(pidf.read().strip())
            pidf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exists. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self, restart=False):
        """Stop the daemon
        """
        # Get the pid from pidfile.
        try:
            pidf = file(self.pidfile, 'r')
            pid = int(pidf.read().strip())
            pidf.close()
        except IOError:
            pid = None


        if not pid:
            if not restart :
                message = "pidfile %s does not exist. Daemon not running?\n"
                sys.stderr.write(message % self.pidfile)
            return # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, SIGHUP)
                time.sleep(1)
                os.kill(pid, SIGTERM)
                time.sleep(1)
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print((str(err)))
                sys.exit(1)


    def restart(self):
        """
        Restart the daemon
        """
        self.stop( restart=True )
        self.start()


    def run(self):
        """
        You should override this method when you subclass Daemon.
        It will be called after the process has been daemonized
        by start() or restart().
        """
        pass


