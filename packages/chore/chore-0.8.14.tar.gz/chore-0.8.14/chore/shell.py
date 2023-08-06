#
# Copyright (C) 2017-2018 Maha Farhat
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Martin Owens
"""
This is the most basic way of running jobs, in the local shell.
"""

import os
import signal
import shutil
import psutil

from subprocess import Popen

from .base import JobManagerBase, JobSubmissionError
DIR = os.path.dirname(__file__)

def which(filename):
    """Which replacement for python2 and python3"""
    for path in (DIR, os.path.join(DIR, '..', 'bin')):
        if os.path.exists(os.path.join(path, filename)):
            return os.path.join(path, filename)

    if hasattr(shutil, 'which'):
        return shutil.which(filename)

    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.exists(os.path.join(path, filename)):
            return os.path.join(path, filename)
    raise IOError("Can't find program: {}".format(filename))

class ShellJobManager(JobManagerBase):
    """
    The job is submitted to the raw system and is controlled via it's pid.
    This pid must be stored in the pipeline-shell directory in tmp.
    """
    watch = which("chore.watch")
    DEP = watch + ' %(fn)s && '
    RET = '; echo $? > "%(fn)s"'

    def job_submit(self, job_id, cmd, depend=None, **kw):
        """
        Open the command locally using bash shell.
        """
        if depend:
            (_, pid) = self.job_read(depend, 'pid')
            (_, ret) = self.job_read(depend, 'ret')
            if pid:
                if ret not in (0, None, '0'):
                    # Refuse to submit job if the dependant job failed
                    return False
                elif ret is None:
                    # If we depend on another process, then watch for it's
                    # return by watching for the appearence of the ret file
                    # then checking it's content
                    cmd = (self.DEP % {'fn': self.job_fn(depend, 'ret')}) + cmd
            else:
                raise JobSubmissionError("Couldn't get pid for dependant job.")

        # Collect the standard error into an err file
        err = open(self.job_fn(job_id, 'err'), 'w')
        err.write('S')
        err.seek(0)
        # Dump the standard out into oblivion
        out = open('/dev/null', 'w')
        # Collect the return code into the ret file
        cmd += self.RET % {'fn': self.job_fn(job_id, 'ret')}

        # Run the large shell command
        proc = Popen(cmd, shell=True, stdout=out, stderr=err, close_fds=True)

        # Pid the pid (process id) into the pid file
        self.job_write(job_id, 'pid', proc.pid)
        return True

    def all_children(self):
        """Yields all running children remaining"""
        from collections import defaultdict
        pids = defaultdict(list)
        for pid in os.listdir('/proc'):
            if pid.isdigit() and self.is_running(pid):
                pid_fn = "/proc/%s/status" % str(pid)
                data = dict(line.split(':\t', 1) for line in open(pid_fn).readlines())
                pids[int(data['PPid'])].append(int(pid))
        parents = [os.getpid()]
        while parents:
            for child in pids.get(parents.pop(0), []):
                if self.state_and_clear(child, False):
                    parents.append(child)
                    yield child

    def clean_up(self):
        """Create a list of all processes and kills them all"""
        pids = list(self.all_children())
        for pid in pids:
            try:
                os.kill(int(pid), signal.SIGKILL)
                os.waitpid(int(pid), 0)
            except OSError:
                pass
        super(ShellJobManager, self).clean_up()
        return pids

    def stop(self, job_id):
        """Send a SIGTERM to the job and clean up"""
        #print("STOP: {}".format(job_id))
        (_, pid) = self.job_read(job_id, 'pid')
        if pid is None:
            return

        if self.is_running(pid):
            if not self.clean_up():
                # invoked when an external process wants to kill a separate
                # PipelineRun
                try:
                    # finds children and kills them too
                    parent = psutil.Process(int(pid))
                    children = parent.children(recursive=True)
                    for child in children:
                        child.send_signal(signal.SIGKILL)
                    os.kill(int(pid), signal.SIGKILL)
                    os.waitpid(int(pid), 0)
                except psutil.NoSuchProcess:
                    pass
                except OSError:
                    pass

    @staticmethod
    def is_running(pid):
        """Returns true if the process is still running"""
        return os.path.exists("/proc/%d/status" % int(pid))

    def job_status(self, job_id):
        """Returns a dictionary containing status information,
        can only be called once as it will clean up status files!"""
        ret = self._program_status(job_id)
        if ret.get('pid', None) is not None:
            ret['status'] = self.state_and_clear(ret['pid'], ret['status'])
        return ret

    @staticmethod
    def state_and_clear(pid, default=None):
        """Gets the status of the process and waits for zombies to clear"""
        pid_fn = "/proc/%d/status" % int(pid)
        if os.path.exists(pid_fn):
            with open(pid_fn, 'r') as fhl:
                data = dict(line.strip().split(':\t', 1) for line in fhl)
            if data['State'][0] == 'Z':
                # Clear up zombie processes waiting for us to pid them.
                try:
                    os.waitpid(int(pid), 0)
                except OSError:
                    pass
                return default
            return {
                'D': 'sleeping', # Machine is too busy
                'S': 'sleeping', # Busy doing nothing
                'R': 'running', # Active
                'T': 'pending', # Stopped because we asked it to be
                'X': 'finished', # Pining for the fyords
            }[data['State'][0]]
        return default
