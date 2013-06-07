from itertools import dropwhile, ifilter
import time
import weakref

from . import ffi, lib

__all__ = ['NIDAQmx', 'Device', 'Task', 'AnalogInputVoltage', 'SampleClock']

def _get_device_attr(dev_name, attr, value=None):
    if value is None: # need to buffer the variable
        buf_size = lib.DAQmxGetDeviceAttribute(dev_name, attr, ffi.NULL)
        #print 'need buffer of size ', buf_size

        if buf_size == 0:
            return None
        else:
            value = ffi.new('char []', buf_size)
            res = lib.DAQmxGetDeviceAttribute(dev_name, attr, value, ffi.cast('int32', buf_size))
            handle_error(res)
            return value
    else: # Prebuffered
        res = lib.DAQmxGetDeviceAttribute(dev_name, attr, value)
        
    handle_error(res)
    return value

def _get_chan_attr(handle, name, attr, value=None):
    if value is None:
        buf_size = lib.DAQmxGetChanAttribute(handle, attr, ffi.NULL)

        if buf_size == 0:
            return None
        else:
            value = ffi.new('char []', buf_size)
            res = lib.DAQmxGetChanAttribute(handle, attr, value, ffi.cast('int32', buf_size))
            handle_error(res)
            return value
    else:
        res = lib.DAQmxGetChanAttribute(handle, attr, value)
        
    handle_error(res)
    return value

def _get_task_attr(handle, attr, value=None):
    if value is None:
        buf_size = lib.DAQmxGetTaskAttribute(handle, attr, ffi.NULL)
        #print 'need buffer of size ', buf_size

        if buf_size == 0:
            return None
        else:
            value = ffi.new('char []', buf_size)
            res = lib.DAQmxGetTaskAttribute(handle, attr, value, ffi.cast('int32', buf_size))
            handle_error(res)
            return value
    else:
        res = lib.DAQmxGetTaskAttribute(handle, attr, value)
        
    handle_error(res)
    return value

class Device(object):
    def __init__(self, name, *args, **kwargs):
        self._name = name
        self._channels = {}

    name = property(lambda self: self._name)
    ai = property(lambda self: self._get_inputs())
    ao = property(lambda self: self._get_outputs())

    def _get_inputs(self):
        pchan_in = _get_device_attr(self._name, lib.DAQmx_Dev_AI_PhysicalChans)
        
        if pchan_in is not None: 
            names_in = [x.strip() for x in ffi.string(pchan_in).split(',')] 
            for i in names_in:
                pin = self._channels.get(i, None) 
                if pin is None: self._channels.update({i: PhysicalChannelInput(i)})

            return [self._channels.get(i) for i in names_in]
        else: 
            return []

    def _get_outputs(self):
        pchan_out = _get_device_attr(self._name, lib.DAQmx_Dev_AO_PhysicalChans)
        
        if pchan_out is not None: 
            names_out = [x.strip() for x in ffi.string(pchan_out).split(',')] 
            for i in names_out:
                pout = self._channels.get(i, None) 
                if pout is None: self._channels.update({i: PhysicalChannelOutput(i)})

            return [self._channels.get(i) for i in names_out]
        else: 
            return []
    
    def __repr__(self):
        return 'Device(\'{}\', ain=\'{}\', aout=\'{}\')'.format(self.name, self.ai, self.ao) 

class NIDAQmx(object):
    def __new__(cls, *args, **kargs):
        inst = getattr(cls, '_instance', None)
        if inst is not None:
        	return inst
        else:
        	cls._instance = super(NIDAQmx, cls).__new__(cls, *args, **kargs)
        	return cls._instance

    def inputs(self):
        tmp = ifilter(lambda x: len(x)>0, [y.ai for y in _get_devices()])
        ai = []
        for i in tmp: ai += i
        return ai
    
    def outputs(self):
        tmp = ifilter(lambda x: len(x)>0, [y.ao for y in _get_devices()])
        ao = []
        for i in tmp: ai += i
        return ao

    devices = property(lambda self: _get_devices())
    version = property(lambda self: 'NIDAQmx version {}.{}'.format(_maj_version(), _min_version())) 
    tasks = property(lambda self: _sys_tasks())
    global_channels = property(lambda self: _sys_global_chans())

from numpy import frombuffer, float64
from ctypes import pythonapi
from weakref import WeakKeyDictionary

from .units import Auto, GroupByScanNumber

class Task(object):
    def __init__(self, name):
        self._phandle = ffi.new('TaskHandle *')
        res = lib.DAQmxCreateTask(name, self._phandle)
        self._channels = {}
        self._data = WeakKeyDictionary()
        self._timing = None

        try:
            handle_error(res)
        except RuntimeError as e:
            self._handle = None
            raise e

    def set_timing(self, timing, *args, **kwargs):
        if issubclass(timing, SampleTiming):
        	print 'Making Timing'
        	self._timing = timing(self._phandle[0], *args, **kwargs)
        else:
        	NotImplementedError('do not understand that timing spec')

    def _get_name(self):
        return ffi.string(_get_task_attr(self._phandle[0], lib.DAQmx_Task_Name))

    def _get_channels(self):
        var = _get_task_attr(self._phandle[0], lib.DAQmx_Task_Channels)

        if var is not None:
            try:
                chan_names = [self._channels[x.strip()] for x in ffi.string(var).split(',')]
            except KeyError:
                raise NotImplementedError('externally added channel. cannot create channel from name')
        else:
            chan_names = []

        return chan_names

    def start(self):
        if self._timing is None:
        	raise RuntimeWarning('task has no explicit timing. values may be inferred.')
        res = lib.DAQmxStartTask(self._phandle[0])
        handle_error(res)

    def stop(self):
        try:
            res = lib.DAQmxStopTask(self._phandle[0])
            handle_error(res)
        except RuntimeWarning as e:
            print e
    
    #XXX Not sure whether I should add the created channel to some inner set 
    # to keep track of it? 
    def add_channel(self, chantype, *args, **kwargs):
        if issubclass(chantype, Channel):
            inst = chantype(self._phandle[0], *args, **kwargs) 
            self._channels.update({inst.name: inst})
            return inst
        elif isinstance(chantype, PhysicalChannel):
            raise RuntimeWarning('you put the physical channel type first')
        elif isinstance(chantype, list):
            raise NotImplementedError('cannot create more than one channel at a time yet')

    def __del__(self):
        if self._phandle:
            res = lib.DAQmxClearTask(self._phandle[0])
            handle_error(res)

    def _is_done(self):
        val = ffi.new('bool32 *')
        res = lib.DAQmxIsTaskDone(self._phandle[0], val)
        handle_error(res)
        return bool(val[0])

    # TODO: handle read types by determining types of channels available and make those types of reads possible  
    # TODO: add a nonblocking read?
    def read_as(self, rtype='AnalogF64', *args, **kwargs):
        if kwargs.get('blocking', False) is True or not kwargs.get('timeout'):
            while not self.is_done:
                time.sleep(0.1)

        print 'Can read now!'

        if rtype != 'AnalogF64': raise NotImplementedError('can only read analog data in floating point')
        self._read_analog_f64(*args, **kwargs)

    def _read_analog_f64(self, buf_size=2048, n_per_channel=Auto, timeout=None, fill_mode=GroupByScanNumber):
        if timeout is None:
        	timeout = 10. # Ten seconds is default

        samples = ffi.new('float64 []', buf_size) 
        count_read = ffi.new('int32 *')
        
        res = lib.DAQmxReadAnalogF64(self._phandle[0], n_per_channel, timeout, fill_mode, samples, buf_size, 
                count_read, ffi.NULL)

        handle_error(res)
        return AnalogF64(samples, count_read[0])

    def channel_by_name(self, name):
        return self._channels.get(name, None)

    name = property(_get_name)
    channels = property(_get_channels)
    timing = property(lambda self: self._timing)
    is_done = property(lambda self: self._is_done())

class Data(object):
    def __init__(self, samples, *args, **kwargs):
        self._cbuf = samples

class AnalogF64(Data):
    def __init__(self, samples, count):
        super(AnalogF64, self).__init__(samples, count)
        self._data = frombuffer(ffi.buffer(self._cbuf), dtype=float64, count=count)

    data = property(lambda self: self._data)

def _get_phys_channel_attr(name, attr, value=None):
    if value is None: # need to buffer the variable
        buf_size = lib.DAQmxGetPhysicalChanAttribute(name, attr, ffi.NULL)
        #print 'need buffer of size ', buf_size

        if buf_size == 0:
            value = ffi.new('char []', 'None')
            return value
        else:
            value = ffi.new('char []', buf_size)
            res = lib.DAQmxGetPhysicalChanAttribute(name, attr, value, ffi.cast('int32', buf_size))
            handle_error(res)
            return value
    else: # Prebuffered
        res = lib.DAQmxGetPhysicalChanAttribute(name, attr, value)
        
    handle_error(res)
    return value

# TODO: rewrite documentation in own words. So far this was taken from the reference
class PhysicalChannel(object):
    '''Represents a physical channel on in NI-DAQmx

    A physical channel is a terminal or pin at which you can measure or generate an analog or digital 
    signal. A single physical channel can include more than one terminal, as in the case of a differential 
    analog input channel or a digital port of eight lines. Every physical channel on a device has a unique 
    name (for instance, SC1Mod4/ai0, Dev2/ao5, and Dev6/ctr3) that follows the NI-DAQmx physical channel naming 
    convention.
    ''' 

    '''
    def _get_TermCfgs(self):
        val = ffi.new('int32 *')
        ai_cfg = _get_phys_channel_attr(self._name, lib.DAQmx_PhysicalChan_AI_TermCfgs, val)
        return ai_cfg[0]
        #return super(AnalogInput, self)._term_cfgs[ai_cfg[0]]
    '''

    #_term_cfgs = {lib.DAQmx_Val_Bit_TermCfg_RSE: 'RSE', lib.DAQmx_Val_Bit_TermCfg_NRSE: 'NRSE', 
        # lib.DAQmx_Val_Bit_TermCfg_Diff: 'Diff', lib.DAQmx_Val_Bit_TermCfg_PseudoDIFF: 'PseudoDiff'}
    
    def __init__(self, name):
        self._name = name
    
    name = property(lambda self: self._name)

class PhysicalChannelInput(PhysicalChannel):
    def __repr__(self): 
        return 'PhysicalChannelInput(\'{}\')'.format(self._name)

class PhysicalChannelOutput(PhysicalChannel):
    def __repr__(self): 
        return 'PhysicalChannelOutput(\'{}\')'.format(self._name)

class Channel(object):
    '''Represents a virtual channel in NI-DAQmx
    
    Virtual channels are software entities that encapsulate the physical channel along with other 
    channel specific information -- range, terminal configuration, and custom scaling -- that formats 
    the data. To create virtual channels, use the DAQmx Create Virtual Channel function/VI or the DAQ Assistant
    '''
    def __init__(self, handle, pchannel, *args, **kwargs):
        self._handle = handle

        if isinstance(pchannel, PhysicalChannel):
        	self._pchannel = pchannel 
        elif isinstance(pchannel, basestring):
            raise NotImplementedError('cannot create channel by name yet')
        elif isinstance(pchannel, list):
            raise NotImplementedError('cannot create multiple channels at once yet')
        else:
        	raise RuntimeError('cannot interpret pchannel type {}'.format(type(pchannel)))

        try:
            #TODO: fix this to use get() perhaps?
            name = kwargs['name']

            if name != '':
                self._name = name
            else:
                self._name = self._pchannel.name
        except AttributeError:
            self._name = self._pchannel.name

    name = property(lambda self: self._name)

class AnalogChannel(Channel):
    def __init__(self, handle, pchannel, min_val, max_val, units, *args, **kwargs):
        super(AnalogChannel, self).__init__(handle, pchannel, min_val, max_val, units, *args, **kwargs)
        self._min_val = min_val
        self._max_val = max_val
        self._units = units

    min = property(lambda self: self._min_val)
    max = property(lambda self: self._max_val)

    # TODO: Make units people friendly
    units = property(lambda self: self._units)


class AnalogInput(AnalogChannel):
    def __init__(self, handle, pchannel, min_val, max_val, units, *args, **kwargs):
        super(AnalogChannel, self).__init__(handle, pchannel, min_val, max_val, units, *args, **kwargs)

        if isinstance(self._pchannel, PhysicalChannelInput) is False:
            raise RuntimeError('cannot create analog input from {}'.format(self._pchannel))

from .units import Volts
class AnalogInputVoltage(AnalogInput):
    def __init__(self, handle, pchannel, min_val, max_val, units=Volts, terminal_cfg=lib.DAQmx_Val_Cfg_Default,  
            name=None, custom_scale_name=None):

        super(AnalogInputVoltage, self).__init__(handle, pchannel, min_val, max_val, units, 
                terminal_cfg=terminal_cfg, name=name, custom_scale_name=custom_scale_name)

        if custom_scale_name is not None and units is FromCustomScale:
            sname = custom_scale_name
        else:
            sname = ffi.NULL

        res = lib.DAQmxCreateAIVoltageChan(self._handle, pchannel.name, self._name, terminal_cfg, min_val,
                max_val, units, sname) 

        handle_error(res)

    def __repr__(self):
        return 'AnalogInputVoltage(\'{}\')'.format(self._name)

class AnalogInputVoltageRMS(AnalogInput):
    def __repr__(self):
        return 'AnalogInputVoltageRMS(\'{}\')'.format(self._name)

class AnalogOutput(AnalogChannel):
    def __repr__(self):
        return 'AnalogOutput(\'{}\')'.format(self._name)

class AnalogOutputCurrent(AnalogOutput):
    def __repr__(self):
        return 'AnalogOutputCurrent(\'{}\')'.format(self._name)

class AnalogOutputVoltage(AnalogOutput):
    def __repr__(self):
        return 'AnalogOutputVoltage(\'{}\')'.format(self._name)

class DigitalChannel(Channel):
    pass

class DigitalInput(DigitalChannel):
    pass

# XXX There are properties that can adjust timing type. this will mean I need to create a new class
# Maybe it is better to have one megaclass instead that handles all of these logistics? 
class SampleTiming(object):
    def __init__(self, handle, *args, **kwargs):
        self._handle = handle

from .units import RisingEdge, FiniteSamples

class SampleClock(SampleTiming):
    def __init__(self, handle, rate, edge=RisingEdge, sample_mode=FiniteSamples, n_per_channel=128, source=None):
        super(SampleClock, self).__init__(handle)
        
        self._source = source
        self._rate = rate
        self._edge = edge
        self._sample_mode = sample_mode
        self._n_per_channel = n_per_channel

        # Use onboard clock as source
        if source is None: source = ffi.NULL

        res = lib.DAQmxCfgSampClkTiming(handle, source, rate, edge, sample_mode, n_per_channel)
        handle_error(res)

