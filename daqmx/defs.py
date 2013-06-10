from .clib import lib, ffi, handle_error

__all__ = ['TaskState', 'SystemAttributes', 'TaskAttributes', 'TerminalConfig', 'SampleMode', \
    'Units', 'AnalogInputCouplings']

class Units:
    Volts = lib.DAQmx_Val_Volts
    Amps = lib.DAQmx_Val_Amps
    FromCustomScale = lib.DAQmx_Val_FromCustomScale 

class AnalogInputCouplings:
    AC = lib.DAQmx_Val_Bit_CouplingTypes_AC
    DC = lib.DAQmx_Val_Bit_CouplingTypes_DC
    Ground = lib.DAQmx_Val_Bit_CouplingTypes_Ground
    LowPass = lib.DAQmx_Val_Bit_CouplingTypes_HFReject
    HiPass = lib.DAQmx_Val_Bit_CouplingTypes_LFReject
    NoiseReject = lib.DAQmx_Val_Bit_CouplingTypes_NoiseReject

class ActiveEdge:
    Rising = lib.DAQmx_Val_Rising
    Falling = lib.DAQmx_Val_Falling

class SampleMode:
    Finite = lib.DAQmx_Val_FiniteSamps
    Continuous = lib.DAQmx_Val_ContSamps
    HWTimedSinglePoint = lib.DAQmx_Val_HWTimedSinglePoint

class TerminalConfig:
    Default = lib.DAQmx_Val_Cfg_Default
    RSE = lib.DAQmx_Val_RSE
    NRSE = lib.DAQmx_Val_NRSE
    Diff = lib.DAQmx_Val_Diff
    PseudoDiff = lib.DAQmx_Val_PseudoDiff

Auto = lib.DAQmx_Val_Auto
WaitInfinitely = lib.DAQmx_Val_WaitInfinitely
SynchronousEventCallbacks = lib.DAQmx_Val_SynchronousEventCallbacks

class EventType:
    Acquired_Into_Buffer = lib.DAQmx_Val_Acquired_Into_Buffer
    Transferred_From_Buffer = lib.DAQmx_Val_Transferred_From_Buffer

class SampleFormat:
    GroupByChannel = lib.DAQmx_Val_GroupByChannel 
    GroupByScanNumber = lib.DAQmx_Val_GroupByScanNumber

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
    str_attrs = ['devices', 'saved_tasks', 'global_channels']
    
    attr_map = {
        'major_version':lib.DAQmx_Sys_NIDAQMajorVersion, 
        'minor_version':lib.DAQmx_Sys_NIDAQMinorVersion, 
        'devices':lib.DAQmx_Sys_DevNames,
        'saved_tasks':lib.DAQmx_Sys_Tasks,
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

class DeviceAttributes(object):
    _category = { \
        lib.DAQmx_Val_MSeriesDAQ: 'M Series DAQ',
        lib.DAQmx_Val_ESeriesDAQ: 'E Series DAQ',
        lib.DAQmx_Val_SSeriesDAQ: 'S Series DAQ',
        lib.DAQmx_Val_BSeriesDAQ: 'B Series DAQ',
        lib.DAQmx_Val_SCSeriesDAQ: 'SC Series DAQ',
        lib.DAQmx_Val_USBDAQ: 'USB DAQ',
        lib.DAQmx_Val_AOSeries: 'AO Series',
        lib.DAQmx_Val_DigitalIO: 'Digital I/O',
        lib.DAQmx_Val_TIOSeries: 'TIO Series',
        lib.DAQmx_Val_DynamicSignalAcquisition: 'Dynamic Signal Acquisition',
        lib.DAQmx_Val_Switches: 'Switches',
        lib.DAQmx_Val_CompactDAQChassis: 'CompactDAQ Chassis',
        lib.DAQmx_Val_CSeriesModule: 'C Series I/O module',
        lib.DAQmx_Val_SCXIModule: 'SCXI Module',
        lib.DAQmx_Val_SCCConnectorBlock: 'SCC Connector Block',
        lib.DAQmx_Val_NIELVIS: 'NI ELVIS',
        lib.DAQmx_Val_NetworkDAQ: 'Network DAQ',
        lib.DAQmx_Val_Unknown: 'Unknown category',
    }

    def __init__(self, name):
        self.name = name

    @property
    def simulated(self):
        p = ffi.new('bool32 *')
        res = lib.DAQmxGetDevIsSimulated(self.name, p)
        handle_error(res)
        return bool(p[0])

    @property
    def product_category(self): 
        p = ffi.new('int32 *')
        res = lib.DAQmxGetDevProductCategory(self.name, p)
        handle_error(res)
        return cls._category[p[0]]


    @property
    def product_type(self):
        p = ffi.new('char[]', 256) 
        res = lib.DAQmxGetDevProductType(self.name, p, 256)
        handle_error(res)
        return ffi.string(p)
    

    def product_number(self):
        p = ffi.new('uInt32 *')
        res = lib.DAQmxGetDevProductNum(self.name, p)
        handle_error(res)
        return p[0]


    @property
    def serial_number(self):
        p = ffi.new('uInt32 *')
        res = lib.DAQmxGetDevSerialNum(self.name, p)
        handle_error(res)
        return p[0]

    @property
    def analog_triggering_supported(self):
        p = ffi.new('bool32 *')
        res = lib.DAQmxGetDevAnlgTrigSupported(self.name, p)
        handle_error(res)
        return bool(p[0])
    
    @property
    def digital_triggering_supported(self):
        p = ffi.new('bool32 *')
        res = lib.DAQmxGetDevDigTrigSupported(self.name, p)
        handle_error(res)
        return bool(p[0])

    @property
    def ai_channels(self):
        p = ffi.new('char[]', 2048)
        res = lib.DAQmxGetDevAIPhysicalChans(self.name, p, 2048);
        handle_error(res)
        return ffi.string(p)


    @property
    def ai_single_chan_max_rate(self):
        p = ffi.new('float64 *')
        res = lib.DAQmxGetDevAIMaxSingleChanRate(self.name, p)
        handle_error(res)
        return p[0]

    @property
    def ai_multi_chan_max_rate(self):
        p = ffi.new('float64 *')
        res = lib.DAQmxGetDevAIMaxMultiChanRate(self.name, p)
        handle_error(res)
        return p[0]

    @property
    def ai_min_rate(self):
        p = ffi.new('float64 *')
        res = lib.DAQmxGetDevAIMinRate(self.name, p)
        handle_error(res)
        return p[0]

    @property
    def ai_simultaneous_sampling(self):
        p = ffi.new('bool32 *')
        res = lib.DAQmxGetDevAISimultaneousSamplingSupported(self.name, p)
        handle_error(res)
        return bool(p[0])

    @property
    def ai_triggers_supported(self):
        p = ffi.new('int32 *')
        res = lib.DAQmxGetDevAITrigUsage(self.name, p)
        handle_error(res)
        return p[0]

    @property
    def ai_voltage_ranges(self):
        # TODO: Can be done with generator expressions
        p = ffi.new('float64[]', 64)
        res = lib.DAQmxGetDevAIVoltageRngs(self.name, p, 64)
        handle_error(res)

        ranges = []
        for i in xrange(0, 64, 2): # iterate in pairs
            if max(p[i], p[i+1]) > 0.001: # real range, not just zeros
                ranges.append((p[i], p[i+1]))

        return ranges


    @property
    def ai_gains(self):
        # TODO: Can be done with generator expressions
        p = ffi.new('float64[]', 64)
        res = lib.DAQmxGetDevAIVoltageRngs(self.name, p, 64)
        handle_error(res)

        gains = []
        for i in xrange(0, 64, 1):
            if p[i] > 0.001: # real range, not just zeros
                gains.append(p[i])

        return gains

    @property
    def ai_couplings(self):
        p = ffi.new('int32 *')
        res = lib.DAQmxGetDevAICouplings(self.name, p);
        handle_error(res)
        return p[0]

    
    @property
    def terminals(self):
        p = ffi.new('char[]', 2048) 
        res = lib.DAQmxGetDevTerminals(self.name, p, 2048)
        handle_error(res)
        return ffi.string(p)

