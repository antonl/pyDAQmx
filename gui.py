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
        self.graphicsView.setMenuEnabled(True)

        view = self.graphicsView.getViewBox()
        view.setMouseMode(pyqtgraph.ViewBox.PanMode)

        self.qOffsetBox.valueChanged.connect(self.q_offset_changed)
        self.iOffsetBox.valueChanged.connect(self.i_offset_changed)

        self.qGainBox.valueChanged.connect(self.q_gain_changed)
        self.iGainBox.valueChanged.connect(self.i_gain_changed)

        self.xy_plot.toggled.connect(self.xy_plot_mode)
        self.stacked_plot.toggled.connect(self.stacked_plot_mode)
        
        self.startButton.clicked.connect(self.start_clicked)

        self.stacked_plot.click()

        self.i_offset_changed()
        self.q_offset_changed()

        self.iGainBox.setValue(1.0)
        self.qGainBox.setValue(1.0)

        self.scope_timer = QTimer()
        self.scope_timer.setInterval(25)
        self.scope_timer.timeout.connect(self.update_plots)

        self.data_timer = QTimer()
        self.data_timer.setInterval(1)
        self.data_timer.timeout.connect(self.worker.get_data)

        self.is_paused = False

    def start_clicked(self):
        if self.is_paused:
        	log.debug('was paused, starting')
        	self.startButton.setText('Pause')
        	self.is_paused = not self.is_paused
        	self.data_timer.start()
        	self.worker.start()
        else:
        	log.debug('was running, pausing')
        	self.startButton.setText('Run')
        	self.is_paused = not self.is_paused
        	self.worker.stop()
        	self.data_timer.stop()

    def q_offset_changed(self):
        self._q_val = float(self.qOffsetBox.value())/100
        log.info('changed q offset to %f', self._q_val)

    def i_offset_changed(self):
        self._i_val = float(self.iOffsetBox.value())/100
        log.info('changed i offset to %f', self._i_val)

    def q_gain_changed(self):
        self._q_gain = float(self.qGainBox.value())
        log.info('changed q gain to %f', self._q_gain)

    def i_gain_changed(self):
        self._i_gain = float(self.iGainBox.value())
        log.info('changed i gain to %f', self._i_gain)

    def stacked_plot_mode(self, toggle):
        if toggle:
            self.stacked_mode = True
            self.xy_mode = False

            self.i_curve = self.graphicsView.plot(pen='g', clear=True)
            self.q_curve = self.graphicsView.plot(pen='r')
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
            navg = 1 
            if len(self.worker.data) >= navg:
                block1 = self.worker.data.popleft()
                nsamp = block1.shape[0]
                data = numpy.zeros((nsamp*navg, 2))
                data[:nsamp] = block1

                for i in xrange(1, navg):
                    data[i*nsamp:(i+1)*nsamp, :] = self.worker.data.popleft()

                log.debug('data shape %s', str(data.shape))

                if self.xy_mode is True:
                    log.debug('updating xy plot')
                    self.xy_curve.setData(self._i_gain*data[:, 0] + self._i_val, self._q_gain*data[:, 1] + \
                        self._q_val)
                elif self.stacked_mode is True:
                    log.debug('updating stacked plot')
                    self.i_curve.setData(self._i_gain*data[:, 0] + self._i_val)
                    self.q_curve.setData(self._q_gain*data[:, 1] + self._q_val)
        except IndexError:
            pass
        except Exception as e:
            log.exception(e)

    def close(self):
        self.worker.stop()
        self.worker.clear()

    def show(self):
        self.scope_timer.start()
        self.data_timer.start()
        self.worker.start()

        super(QMainWindow, self).show()
        
    def closeEvent(self, event):
        super(QMainWindow, self).closeEvent(event)

class TwoChanScope(object):
    def __init__(self):
        self.h = d.make_task('scope')
        log.debug('Making TwoChanScope, handle %d', self.h)

        d.add_input_voltage_channel(self.h, 'Dev1/ai0', 0, 0.5, units=daqmx.Units.Volts, name='I')
        d.add_input_voltage_channel(self.h, 'Dev1/ai1', 0, 0.5, units=daqmx.Units.Volts, name='Q')
        
        d.set_timing_sample_clock(self.h, 2<<16, 2<<16, sample_mode=d.SampleMode.Continuous)
        #d.set_input_buffer_size(self.h, 2<<15)
        self.data = deque()
        
    def get_data(self):
        nsamples = 2<<15
        log.debug('in callback, nsamples: %d, reading %d samples per channel', nsamples, nsamples>>1)
        data, count = d.read_f64(self.h, nsamples, n_samps_per_channel=nsamples>>1, timeout=0.2)
        log.debug('got count: %d, data %s', count, str(data))
        data = numpy.frombuffer(data, dtype=numpy.float64, count=count<<1)
        self.data.append(data.reshape(count, 2))

    def start(self):
        d.start_task(self.h)

    def stop(self):
        d.stop_task(self.h)

    def clear(self):
        d.clear_task(self.h)

app = QtGui.QApplication(sys.argv)
ex = ScopeUI()
ex.show()
app.exec_()


