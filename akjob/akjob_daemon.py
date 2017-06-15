"""
python-daemon asks for pylockfile but that package is depreciated. Instead I'm
using pid which is python-daemon compatible.

Do I need to define what to do in response to diferent signals or is the
default that python-daemon uses good enough?

Start the daemon using AppConfig.ready()
"""

# import pid
from daemon import runner, DaemonContext
from time import sleep


class DaemonRunner(runner.DaemonRunner):
    "Overriding non-compatable python 2 code."

    def __init__(self, app):
        """ Set up the parameters of a new runner.

            :param app: The application instance; see below.
            :return: ``None``.

            The `app` argument must have the following attributes:

            * `stdin_path`, `stdout_path`, `stderr_path`: Filesystem paths
              to open and replace the existing `sys.stdin`, `sys.stdout`,
              `sys.stderr`.

            * `pidfile_path`: Absolute filesystem path to a file that will
              be used as the PID file for the daemon. If ``None``, no PID
              file will be used.

            * `pidfile_timeout`: Used as the default acquisition timeout
              value supplied to the runner's PID lock file.

            * `run`: Callable that will be invoked when the daemon is
              started.

            """
        self.parse_args()
        self.app = app
        self.daemon_context = DaemonContext()
        self.daemon_context.stdin = open(app.stdin_path, 'rt')
        self.daemon_context.stdout = open(app.stdout_path, 'w+t')
        self.daemon_context.stderr = open(app.stderr_path, 'w+t')

        self.pidfile = None
        if app.pidfile_path is not None:
            self.pidfile = runner.make_pidlockfile(
                app.pidfile_path, app.pidfile_timeout)
        self.daemon_context.pidfile = self.pidfile


# with daemon.DaemonContext(pidfile=pid.PidFile('/Users/robwirk/dev/akbash/akjob.pid')):
class App():

    def __init__(self):
        self.pidfile_path = '/Users/robwirk/dev/akbash/akjob.pid'
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_timeout = 5

    def run(self):
        while True:
            # do_the_things()
            sleep(10)


app = App()
daemon_runner = DaemonRunner(app)
daemon_runner.do_action()
