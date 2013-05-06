from itertools import dropwhile, ifilter
import weakref

from . import ffi, lib

__all__ = ['NIDAQmx', 'Device', 'Task']

def handle_error(res):
    if res == 0: return
    
    msg = ffi.new('char[2048]')
    
    lib.DAQmxGetExtendedErrorInfo(msg, 2048)
    py_s = ffi.string(msg)
    
    del msg
    
    if res < 0:
        raise RuntimeError(py_s)
    elif res > 0:
        raise RuntimeWarning(py_s)

def _get_system_attr(attr, value=None):
    if value is None:
        buf_size = lib.DAQmxGetSystemInfoAttribute(attr, ffi.NULL)
        #print 'need buffer of size ', buf_size

        if buf_size == 0:
            return None
        else:
            value = ffi.new('char []', buf_size)
            res = lib.DAQmxGetSystemInfoAttribute(attr, value, ffi.cast('int32', buf_size))
            handle_error(res)
            return value
    else:
        res = lib.DAQmxGetSystemInfoAttribute(attr, value)
        
    handle_error(res)
    return value
    
def _maj_version():
    var = ffi.new('uInt32 *')
    return _get_system_attr(lib.DAQmx_Sys_NIDAQMajorVersion, var)[0]
    
def _min_version():   
    var = ffi.new('uInt32 *')
    return _get_system_attr(lib.DAQmx_Sys_NIDAQMinorVersion, var)[0]

def _sys_devnames():
        return ffi.string(_get_system_attr(lib.DAQmx_Sys_DevNames))

def _get_devices():
    return [Device(x.strip()) for x in _sys_devnames().split(',')]

def _sys_tasks():
    var = _get_system_attr(lib.DAQmx_Sys_Tasks)

    if var is not None:
        return [Task(x.strip()) for x in ffi.string(var).split(',')]
    else:
        return []

def _sys_global_chans():
    var = _get_system_attr(lib.DAQmx_Sys_GlobalChans)

    if var is not None:
        return [PhysicalChannel(x.strip()) for x in ffi.string(var).split(',')]
    else:
        return []
    
def _make_task(name=''):
        return Task(name)

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

    name = property(lambda self: self._name)
    channels = property(lambda self: self._get_phys_channel_props)

    def _get_phys_channel_props(self):
        pchan_in = _get_device_attr(self._name, lib.DAQmx_Dev_AI_PhysicalChans)
        pchan_out = _get_device_attr(self._name, lib.DAQmx_Dev_AO_PhysicalChans)
        
        if pchan_in is not None: 
            names_in = [PhysicalChannelInput(x.strip()) for x in ffi.string(pchan_in).split(',')] 
        else: 
            names_in = []

        if pchan_out is not None: 
            names_out = [PhysicalChannelOutput(x.strip()) for x in ffi.string(pchan_out).split(',')] 
        else: 
            names_out = []
            
        return (names_in, names_out)
    
    def __repr__(self):
        #i,o = self._get_phys_channel_props(), 'thing'
        i,o = self._get_phys_channel_props()
        return 'Device(\'{}\', ain=\'{}\', aout=\'{}\')'.format(self._name, i, o) 

class NIDAQmx(object):
    def __new__(cls, *args, **kargs):
        inst = getattr(cls, '_instance', None)
        if inst is not None:
        	return inst
        else:
        	cls._instance = super(NIDAQmx, cls).__new__(cls, *args, **kargs)
        	return cls._instance

    devices = property(lambda self: _get_devices())
    version = property(lambda self: 'NIDAQmx version {}.{}'.format(_maj_version(), _min_version())) 
    tasks = property(lambda self: _sys_tasks())
    channels = property(lambda self: _sys_global_chans())

class Task(object):
    def __init__(self, name):
        self._phandle = ffi.new('TaskHandle *')
        res = lib.DAQmxCreateTask(name, self._phandle)

        try:
            handle_error(res)
        except RuntimeError as e:
            self._handle = None
            raise e

    def _get_name(self):
        return ffi.string(_get_task_attr(self._phandle[0], lib.DAQmx_Task_Name))

    def _get_channels(self):
        var = _get_task_attr(self._phandle[0], lib.DAQmx_Task_Channels)

        if var is not None:
            # TODO: This isn't quite right. Should return Channel class with specific information
            # about the type of channel it is, not just the physical channels.
            chan_names = [PhysicalChannel(x.strip()) for x in ffi.string(var).split(',')]
        else:
            chan_names = []

        return chan_names

    def stop(self):
        try:
            res = lib.DAQmxStopTask(self._phandle[0])
            handle_error(res)
        except RuntimeWarning as e:
            print e
    
    #XXX Not sure whether I should add the created channel to some inner set 
    # to keep track of it? 
    def add_channel(self, chantype):
        if isinstance(chantype, Channel):
        	return chantype(name='') 

    def __del__(self):
        if self._phandle:
            res = lib.DAQmxClearTask(self._phandle[0])
            handle_error(res)

    name = property(_get_name)
    channels = property(_get_channels)


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
    def __init__(self, inp, name=''):
        if isinstance(inp, PhysicalChannel):
        	self._pchannel = inp
        elif isinstance(inp, basestring):
            raise NotImplementedError('cannot create channel by name yet')

        if name != '':
            self._name = name
        else:
            # is this the right thing to do?
        	self._name = self._pchannel.name

    name = property(lambda self: self._name)

class AnalogInput(Channel):
    def __repr__(self):
        return 'AnalogInput(\'{}\')'.format(self._name)
    

class AnalogInputVoltage(AnalogInput):
    def __repr__(self):
        return 'AnalogInputVoltage(\'{}\')'.format(self._name)

class AnalogInputVoltageRMS(AnalogInput):
    def __repr__(self):
        return 'AnalogInputVoltageRMS(\'{}\')'.format(self._name)

class AnalogOutput(Channel):
    def __repr__(self):
        return 'AnalogOutput(\'{}\')'.format(self._name)

class AnalogOutputCurrent(AnalogOutput):
    def __repr__(self):
        return 'AnalogOutputCurrent(\'{}\')'.format(self._name)

class AnalogOutputVoltage(AnalogOutput):
    def __repr__(self):
        return 'AnalogOutputVoltage(\'{}\')'.format(self._name)

class DigitalInput(Channel):
    pass

