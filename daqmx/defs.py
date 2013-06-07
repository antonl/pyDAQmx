from .clib import lib, ffi
from .lowlevel import handle_error

class ChannelUnits:
    Volts = lib.DAQmx_Val_Volts
    FromCustomScale = lib.DAQmx_Val_FromCustomScale 

class TriggerType:
    RisingEdge = lib.DAQmx_Val_Rising
    FallingEdge = lib.DAQmx_Val_Falling

class SampleType:
    FiniteSamples = lib.DAQmx_Val_FiniteSamps
    ContinuousSamples = lib.DAQmx_Val_ContSamps
    HWTimedSinglePoint = lib.DAQmx_Val_HWTimedSinglePoint

Auto = lib.DAQmx_Val_Auto
GroupByChannel = lib.DAQmx_Val_GroupByChannel 
GroupByScanNumber = lib.DAQmx_Val_GroupByScanNumber
WaitInfinitely = lib.DAQmx_Val_WaitInfinitely

class SystemAttributes:
    '''enum class for querying system attributes

    This class allows one to query system attributes. They can be accessed using the 
    `get()` class method or the index operator, e.g.

    >>> from pyDAQmx import SystemAttributes
    >>> SystemAttributes['devices']
    '''

    int_attrs = ['major_version', 'minor_version']
    str_attrs = ['devices', 'tasks', 'global_channels']
    
    attr_map = {
        'major_version':lib.DAQmx_Sys_NIDAQMajorVersion, 
        'minor_version':lib.DAQmx_Sys_NIDAQMinorVersion, 
        'devices':lib.DAQmx_Sys_DevNames,
        'tasks':lib.DAQmx_Sys_Tasks,
        'global_channels':lib.DAQmx_Sys_GlobalChans,
    }

    attributes = attr_map.keys()

    @classmethod
    def get(cls, attr):
        if not isinstance(attr, basestring):
            raise TypeError('attr must be a string')

        if attr in cls.int_attrs:
            # attribute is an integer, TODO: assume unsigned 32 bit?
            attr = attr_map[attr]

            value = ffi.new('uInt32 *', 0)
            res = lib.DAQmxGetSystemInfoAttribute(attr, value)
            handle_error(res)
            return value[0]
        elif attr in cls.str_attrs: 
            # attribute is a string, allocate buffer for it
            attr = attr_map[attr]
            
            buf_size = lib.DAQmxGetSystemInfoAttribute(attr, ffi.NULL)

            if buf_size == 0:
                return None
            else:
                value = ffi.new('char []', buf_size)
                res = lib.DAQmxGetSystemInfoAttribute(attr, value, ffi.cast('int32', buf_size))
                handle_error(res)
                return ffi.string(value)
        else:
            raise AttributeError('no system attribute {}'.format(attr))

    @classmethod
    def __index__(cls, attr):
        return cls.get(attr)

