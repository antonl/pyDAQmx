from .clib import lib, ffi, handle_error

__all__ = ['TaskState', 'SystemAttributes', 'DeviceAttributes', 'TaskAttributes']

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

class TaskState:
    '''task state enum class that contains values for passing to `control_task` function
    '''

    Start = lib.DAQmx_Val_Task_Start 
    Stop = lib.DAQmx_Val_Task_Stop 
    Verify = lib.DAQmx_Val_Task_Verify 
    Commit = lib.DAQmx_Val_Task_Commit 
    Reserve = lib.DAQmx_Val_Task_Reserve 
    Unreserve = lib.DAQmx_Val_Task_Unreserve 
    Abort = lib.DAQmx_Val_Task_Abort 

class SystemAttributes(object):
    '''enum class for querying system attributes

    This class allows one to query system attributes. They can be accessed using the 
    `get()` class method, e.g.
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
            attr = cls.attr_map[attr]

            value = ffi.new('uInt32 *', 0)
            res = lib.DAQmxGetSystemInfoAttribute(attr, value)
            handle_error(res)
            return value[0]
        elif attr in cls.str_attrs: 
            # attribute is a string, allocate buffer for it
            attr = cls.attr_map[attr]
            
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

class DeviceAttributes(object):
    '''enum class for querying device attributes. Requires device name

    This class allows one to query device attributes. They can be accessed using the 
    `get(name, attr)` class method, e.g.
    '''

    int_attrs = []
    str_attrs = []
    bool_attrs = []
    
    attr_map = {
    }

    attributes = attr_map.keys()

    @classmethod
    def get(cls, name, attr):
        if not isinstance(attr, basestring):
            raise TypeError('attr must be a string')

        if not isinstance(name, basestring):
            raise TypeError('name must be a string')

        if attr in cls.int_attrs:
            # attribute is an integer, TODO: assume unsigned 32 bit?
            attr = cls.attr_map[attr]

            value = ffi.new('uInt32 *', 0)
            res = lib.DAQmxGetDeviceAttribute(name, attr, value)
            handle_error(res)
            return value[0]
        elif attr in cls.str_attrs: 
            # attribute is a string, allocate buffer for it
            attr = cls.attr_map[attr]
            
            buf_size = lib.DAQmxGetDeviceAttribute(name, attr, ffi.NULL)

            if buf_size < 0: # error condition
                handle_error(buf_size)
            elif buf_size == 0: # empty string
                return None
            else:
                value = ffi.new('char []', buf_size)
                res = lib.DAQmxGetDeviceAttribute(name, attr, value, ffi.cast('int32', buf_size))
                handle_error(res)
                return ffi.string(value)
        else:
            raise AttributeError('no device attribute {}'.format(attr))

class TaskAttributes(object):
    '''enum class for querying task attributes. Requires task handle

    This class allows one to query task attributes. They can be accessed using the 
    `get(handle, attr)` class method
    '''

    int_attrs = ['channel_count', 'device_count']
    str_attrs = ['name', 'channels', 'devices']
    bool_attrs = ['is_done']
    
    attr_map = {
            'name': lib.DAQmx_Task_Name,
            'channels': lib.DAQmx_Task_Channels,
            'channel_count': lib.DAQmx_Task_NumChans,
            'devices': lib.DAQmx_Task_Devices,
            'device_count': lib.DAQmx_Task_NumDevices,
            'is_done': lib.DAQmx_Task_Complete,
    }

    attributes = attr_map.keys()

    @classmethod
    def get(cls, handle, attr):
        if not isinstance(attr, basestring):
            raise TypeError('attr must be a string')

        #if not isinstance(handle, ):
        #    raise TypeError('name must be a string')

        if attr in cls.int_attrs:
            # attribute is an integer, TODO: assume unsigned 32 bit?
            attr = cls.attr_map[attr]

            value = ffi.new('uInt32 *', 0)
            res = lib.DAQmxGetTaskAttribute(handle, attr, value)
            handle_error(res)
            return value[0]
        elif attr in cls.bool_attrs:
            attr = cls.attr_map[attr]

            value = ffi.new('uInt32 *', 0)
            res = lib.DAQmxGetTaskAttribute(handle, attr, value)
            handle_error(res)
            return bool(value[0])
        elif attr in cls.str_attrs: 
            # attribute is a string, allocate buffer for it
            attr = cls.attr_map[attr]
            
            buf_size = lib.DAQmxGetTaskAttribute(handle, attr, ffi.NULL)

            if buf_size < 0:
                # it seems that NIDAQmx returns a negaitve number if the task doens't 
                # exist anymore
                handle_error(buf_size)
                return None
            elif buf_size == 0:
                # There are no elements in the string list
                return None
            else:
                value = ffi.new('char []', buf_size)
                res = lib.DAQmxGetTaskAttribute(handle, attr, value, ffi.cast('int32', buf_size))
                handle_error(res)
                return ffi.string(value)
        else:
            raise AttributeError('no task attribute {}'.format(attr))
