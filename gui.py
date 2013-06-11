import threading
import daqmx
import daqmx.lowlevel as d 
from collections import deque
import numpy

import logging

log = logging.getLogger('scope')
dlog = logging.getLogger('daqmx')

f = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(f)
log.addHandler(sh)
dlog.addHandler(sh)
log.setLevel(logging.DEBUG)
dlog.setLevel(logging.DEBUG)

class TwoChanScope(threading.Thread):
    def __init__(self):
        self.h = d.make_task('scope')
        log.debug('Making TwoChanScope, handle %d', self.h)

        d.add_input_voltage_channel(self.h, 'Dev1/ai0', 0., 0.5, units=daqmx.Units.Volts, name='I')
        d.add_input_voltage_channel(self.h, 'Dev1/ai1', 0., 0.5, units=daqmx.Units.Volts, name='Q')
        
        d.set_timing_sample_clock(self.h, 2048, n_samples=128, sample_mode=d.SampleMode.Continuous)

        d.set_input_buffer_size(self.h, 256)
        d.register_nsamples_callback(self.h, 256, self._callback)

        self.running = threading.Event()
        self.data = deque()
        threading.Thread.__init__(self)
        
    def _callback(self, h, t, nsamples, data):
        log.debug('in callback')
        data, count = d.read_f64(h, nsamples, timeout=0.)
        data = numpy.frombuffer(data[:count], dtype='<f2')
        self.data.append(data.reshape(2, -1))
        return 0
    
    def run(self):
        try:
            d.start_task(self.h)
            self.running.set()
        except RuntimeError as e:
            log.error(e)

        log.debug('running is %s', str(self.running.is_set()))

        while self.running.is_set():
            try:
                self.data.pop()
                log.info('got data')
            except IndexError:
                pass

    def join(self):
        d.stop_task(self.h)
        self.running.clear()
        d.clear_task(self.h)

worker = TwoChanScope()

try:
    worker.start()
    log.debug('started thread')

    while True:
    	pass
except KeyboardInterrupt:
    worker.join()

