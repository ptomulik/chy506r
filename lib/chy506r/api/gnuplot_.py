# -*- coding: utf8 -*-

import subprocess
import tempfile
import os

__all__ = ('Gnuplot', )


_gnuplot_script = """
# Plot Title
set title "Temperatures"

# X axis settings
set xdata time
set timefmt "%H:%M:%S"
set format x "%H:%M:%S"
set xtics rotate by 45 right

# Y axis
set yrange[0:300]

# Grid
set grid

# draw chart from a file
set datafile separator ';'
plot file using "TIME":"T1" with lines title "T1", \
     file using "TIME":"T2" with lines title "T2"
pause 1
reread

"""

class Gnuplot(object):
    def __init__(self, file, gnuplot='gnuplot'):
        self._popen = None
        self._file = file
        self._gnuplot = gnuplot
        self._prepare_script()

    def _prepare_script(self):
        (fd, self._script) = tempfile.mkstemp()
        self._scriptfd = os.fdopen(fd, 'wt')
        self._scriptfd.write(_gnuplot_script)
        self._scriptfd.flush()

    def cmd(self):
        return [self._gnuplot, '-e', "file=%s" % repr(self._file), self._script]

    def start(self):
        self._popen =  subprocess.Popen(self.cmd())

    def poll(self):
        return self._popen.poll()

    def terminate(self):
        self._popen.terminate()


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
