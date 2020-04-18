#pylint: disable=C0111,R0903

"""Displays the indicator status, for numlock, scrolllock and capslock 

Parameters:
    * indicator.include: Comma-separated list of interface prefixes to include (defaults to 'numlock,capslock')
    * indicator.signalstype: If you want the signali type color to be 'critical' or 'warning' (defaults to 'warning')
"""

import core.module
import core.widget

import util.cli
import util.format

class Module(core.module.Module):
    def __init__(self, config):
        super().__init__(config, [])

        self.__include = tuple(filter(len, util.format.aslist(self.parameter('include', 'NumLock,CapsLock'))))
        self.__signalType = self.parameter('signaltype') if not self.parameter('signaltype') is None else 'warning'

    def update(self):
        status_line = '' 
        for line in util.cli.execute('xset q', ignore_errors=True).replace(' ', '').split('\n'):
            if 'capslock' in line.lower():
                status_line = line  
                break
        for indicator in self.__include:
            widget = self.widget(indicator)
            if not widget:
                widget = core.widget.Widget(name=indicator, module=self)
                self.widgets().append(widget)

            widget.set('status', True if '{}:on'.format(indicator.lower()) in status_line.lower() else False)
            widget.full_text(indicator)

    def state(self, widget):
        states = []
        if widget.get('status', False):
            states.append(self.__signalType)
        else:
            states.append('normal')
        return states

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
