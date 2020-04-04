# pylint: disable=C0111,R0903,W1401

""" Execute command in shell and print result

Few command examples:
    'ping -c 1 1.1.1.1 | grep -Po '(?<=time=)\d+(\.\d+)? ms''
    'echo 'BTC=$(curl -s rate.sx/1BTC | grep -Po \'^\d+\')USD''
    'curl -s https://wttr.in/London?format=%l+%t+%h+%w'
    'pip3 freeze | wc -l'
    'any_custom_script.sh | grep arguments'

Parameters:
    * shell.command:  Command to execute
                      Use single parentheses if evaluating anything inside (sh-style)
                      For example shell.command='echo $(date +'%H:%M:%S')'
                      But NOT shell.command='echo $(date +'%H:%M:%S')'
                      Second one will be evaluated only once at startup
    * shell.interval: Update interval in seconds
                      (defaults to 1s == every bumblebee-status update)
    * shell.async:    Run update in async mode. Won't run next thread if
                      previous one didn't finished yet. Useful for long
                      running scripts to avoid bumblebee-status freezes
                      (defaults to False)
"""

import os
import subprocess
import threading

import core.module
import core.widget
import core.input
import util.format
import util.cli

class Module(core.module.Module):
    def __init__(self, config):
        super().__init__(config, core.widget.Widget(self.get_output))

        self.__command = self.parameter('command')
        self.__async = util.format.asbool(self.parameter('async'))

        if self.__async:
            self.__output = 'please wait...'
            self.__current_thread = threading.Thread()

        # LMB and RMB will update output regardless of timer
        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.update)
        core.input.register(self, button=core.input.RIGHT_MOUSE, cmd=self.update)

    def set_output(self, value):
        self.__output = value

    def get_output(self, _):
        return self.__output

    def update(self):
        # if requested then run not async version and just execute command in this thread
        if not self.__async:
            self.__output = util.cli.execute(self.__command, ignore_errors=True)
            return

        # if previous thread didn't end yet then don't do anything
        if self.__current_thread.is_alive():
            return

        # spawn new thread to execute command and pass callback method to get output from it
        self.__current_thread = threading.Thread(
            target=lambda obj, cmd: obj.set_output(util.cli.execute(cmd, ignore_errors=True)),
            args=(self, self.__command)
        )
        self.__current_thread.start()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4