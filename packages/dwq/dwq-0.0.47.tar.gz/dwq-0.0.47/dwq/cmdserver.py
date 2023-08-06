# python's subprocess creation speed depends on the main processes memory consumption
# (due to mmap'ing magic). So with a million targets, pyjam's overhead for calling "true"
# goes from 3ms to 20ms. Using this cmdserver class, the speed stays constant at 3.7ms.
# (measured on my thinkpad x220 core i5).
#
# The class also provides an easy API to run commands in a subprocess, gathering it's output,
# and provides a way of killing it.
# Part of this will be obsolete as soon as everyone can use Python 3.5 subprocess.run().
#

from multiprocessing import Process, Queue
from queue import Empty
from subprocess import Popen, PIPE, STDOUT
import signal
from collections import deque
import os


class CmdTimeout(Exception):
    pass


class CmdHandle(object):
    def __init__(s, queue, pid, pool, server):
        s.queue = queue
        s.pid = pid
        s.pool = pool
        s.server = server
        s.timeout = False

    def wait(s, timeout=None):
        try:
            res = s.queue.get(True, timeout=timeout)
        except Empty:
            s.timeout = True
            return s.killpg()

        s.pool.append(s.server)
        return res

    def kill(s, signal=signal.SIGKILL):
        try:
            os.kill(-s.pid, signal)
        except:
            pass
        return s.wait()

    def killpg(s, signal=signal.SIGKILL):
        try:
            os.killpg(os.getpgid(s.pid), signal)
        except:
            pass
        return s.wait()


class CmdServer(object):
    def __init__(s, pool):
        s.inQueue = Queue()
        s.outQueue = Queue()
        s.cmdHostProcess = Process(
            target=CmdServer.cmdloop, args=(s, s.inQueue, s.outQueue, pool), daemon=True
        )
        s.cmdHostProcess.start()

    def cmdloop(s, inQueue, outQueue, pool):
        try:
            while True:
                args, kwargs = inQueue.get()
                kwargs["stderr"] = STDOUT
                kwargs["stdout"] = PIPE
                output = u""
                try:
                    process = Popen(*args, **kwargs)
                    outQueue.put(process.pid)
                    with process:
                        output += process.stdout.read().decode("utf-8", "replace")
                    outQueue.put((output, process.returncode))
                except FileNotFoundError:
                    outQueue.put((output, 127))
        except (KeyboardInterrupt, SystemExit):
            pass

    def runcmd(s, *args, **kwargs):
        s.inQueue.put((args, kwargs))
        pid = s.outQueue.get()
        return s.outQueue, pid

    def killCmdHostProcess(s):
        s.cmdHostProcess.terminate()


class CmdServerPool(object):
    def __init__(s, n):
        s.pool = deque()
        for i in range(0, n):
            s.pool.append(CmdServer(s.pool))

    def destroy(s):
        while s.pool:
            s.pool.pop().killCmdHostProcess()

    def runcmd(s, *args, **kwargs):
        server = s.pool.pop()
        queue, pid = server.runcmd(*args, **kwargs)
        return CmdHandle(queue, pid, s.pool, server)
