from __future__ import absolute_import

import os

from topaz.module import Module, ModuleDef


class Process(Module):
    moduledef = ModuleDef("Process", filepath=__file__)

    @moduledef.function("euid")
    def method_euid(self, space):
        return space.newint(os.geteuid())

    @moduledef.function("pid")
    def method_pid(self, space):
        return space.newint(os.getpid())

    @moduledef.function("waitpid", pid="int")
    def method_waitpid(self, space, pid=-1):
        pid, status = os.waitpid(pid, 0)
        status = os.WEXITSTATUS(status)
        w_status = space.send(
            space.find_const(self, "Status"),
            space.newsymbol("new"),
            [space.newint(pid), space.newint(status)]
        )
        space.globals.set(space, "$?", w_status)
        return space.newint(pid)

    @moduledef.function("exit", status="int")
    def method_exit(self, space, status=0):
        raise space.error(space.w_SystemExit, "exit", [space.newint(status)])

    @moduledef.function("exit!", status="int")
    def method_exit_bang(self, space, status=0):
        os._exit(status)

    @moduledef.function("fork")
    def method_fork(self, space, block):
        pid = os.fork()
        if pid == 0:
            if block is not None:
                space.invoke_block(block, [])
                space.send(self, space.newsymbol("exit"))
            else:
                return space.w_nil
        else:
            return space.newint(pid)
