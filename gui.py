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
log.setLevel(logging.ERROR)
dlog.setLevel(logging.ERROR)

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

        self.q_offset.valueChanged.connect(self.q_offset_changed)
        self.i_offset.valueChanged.connect(self.i_offset_changed)

        self.xy_plot.toggled.connect(self.xy_plot_mode)
        self.stacked_plot.toggled.connect(self.stacked_plot_mode)
        
        self.stacked_plot.click()
        self.i_offset_changed()
        self.q_offset_changed()

        self.scope_timer = QTimer()
        self.scope_timer.timeout.connect(self.update_plots)

    def q_offset_changed(self):
        self._q_val = float(self.q_offset.value())/100

    def i_offset_changed(self):
        self._i_val = float(self.i_offset.value())/100

    def stacked_plot_mode(self, toggle):
        if toggle:
            self.stacked_mode = True
            self.xy_mode = False

            self.i_curve = self.graphicsView.plot(pen='g', clear=True)
            self.q_curve = self.graphicsView.plot(pen='b')
        else:
        	pass

    def xy_plot_mode(self, toggle):
        if toggle:
            self.stacked_mode = False
            self.xy_mode = True
            self.xy_curve = self.graphicsView.plot(pen='r', clear=True)
        else:
        	pass

    def update_plots(self):
        try:
            data = self.worker.data.pop()
            log.debug('data shape %s', str(data.shape))

            if self.xy_mode is True:
                log.debug('updating xy plot')
                self.xy_curve.setData(data[0, :] + self._i_val, data[1, :] + \
                    self._q_val)
            elif self.stacked_mode is True:
                log.debug('updating stacked plot')
                self.i_curve.setData(data[0, :] + self._i_val)
                self.q_curve.setData(data[1, :] + self._q_val)
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
        
        d.set_timing_sample_clock(self.h, 1024*16*4, 1024*2, sample_mode=d.SampleMode.Continuous)

        d.set_input_buffer_size(self.h, 1024*4)
        d.register_nsamples_callback(self.h, 1024*4, self._callback)

        self.data = deque()
        
    def _callback(self, h, t, nsamples, unused):
        log.debug('in callback, nsamples: %d', nsamples)
        data, count = d.read_f64(h, nsamples*2, n_samps_per_channel=nsamples )
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


