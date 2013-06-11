import daqmx
import daqmx.lowlevel as d 
from collections import deque
import numpy
import sys
import logging

log = logging.getLogger('scope')
dlog = logging.getLogger('daqmx')

f = logging.Formatter('%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(f)
log.addHandler(sh)
dlog.addHandler(sh)
log.setLevel(logging.DEBUG)
dlog.setLevel(logging.DEBUG)

from PyQt4 import QtGui
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QMainWindow
import pyqtgraph

from ui import Ui_MainWindow

class ScopeUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # Set up everything
        QMainWindow.__init__(self)

        self.setupUi(self)

        self.worker = TwoChanScope()

        self.graphicsView.showGrid(x=True, y=True)
        self.graphicsView.setMenuEnabled(False)

        view = self.graphicsView.getViewBox()
        view.setMouseMode(pyqtgraph.ViewBox.PanMode)

        self.stacked_plot_mode()

        self.scope_timer = QTimer()
        self.scope_timer.timeout.connect(self.update_plots)

    def stacked_plot_mode(self):
        self.stacked_mode = True
        self.xy_mode = False

        self.i_curve = self.graphicsView.plot(pen='g', clear=True)
        self.q_curve = self.graphicsView.plot(pen='b')

    def xy_plot_mode(self):
        self.stacked_mode = False
        self.xy_mode = True

        self.xy_curve = self.graphicsView.plot(pen='r', clear=True)

    def update_plots(self):
        try:
            data = self.worker.data.pop()
            log.debug('data shape %s', str(data.shape))

            if self.xy_mode is True:
                log.debug('updating xy plot')
                self.xy_curve.setData(data[0, :], data[1, :])
            elif self.stacked_mode is True:
                log.debug('updating stacked plot')
                self.i_curve.setData(data[0, :] + 0.2)
                self.q_curve.setData(data[1, :] - 0.2)
        except IndexError:
            pass

    def close(self):
        self.worker.stop()

    def show(self):
        self.worker.start()
        self.scope_timer.start(25)

        super(QMainWindow, self).show()
        
    def closeEvent(self, event):
        super(QMainWindow, self).closeEvent(event)

class TwoChanScope(object):
    def __init__(self):
        self.h = d.make_task('scope')
        log.debug('Making TwoChanScope, handle %d', self.h)

        d.add_input_voltage_channel(self.h, 'Dev1/ai0', 0., 0.5, units=daqmx.Units.Volts, name='I')
        d.add_input_voltage_channel(self.h, 'Dev1/ai1', 0., 0.5, units=daqmx.Units.Volts, name='Q')
        
        d.set_timing_sample_clock(self.h, 1024, n_samples=128, sample_mode=d.SampleMode.Continuous)

        d.set_input_buffer_size(self.h, 256)
        d.register_nsamples_callback(self.h, 256, self._callback)

        self.data = deque()
        
    def _callback(self, h, t, nsamples, unused):
        log.debug('in callback, nsamples: %d', nsamples)
        data, count = d.read_f64(h, 2048, n_samps_per_channel=nsamples )
        log.debug('got count: %d, data %s', count, str(data))
        data = numpy.frombuffer(data, dtype=numpy.float64, count=count)
        self.data.append(data.reshape(2, nsamples/2))
        return 0

    def start(self):
        d.start_task(self.h)

    def stop(self):
        d.stop_task(self.h)
        d.clear_task(self.h)

app = QtGui.QApplication(sys.argv)
ex = ScopeUI()
ex.show()
app.exec_()


