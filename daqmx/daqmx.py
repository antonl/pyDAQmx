from cffi import FFI
from itertools import dropwhile, ifilter
import weakref

__all__ = ['NIDAQmx', 'Device', 'AnalogInput', 'AnalogOutput', 'Task']

ffi = FFI()
ffi.cdef('''
typedef unsigned long uInt32; 
typedef signed long int32;

typedef uInt32             TaskHandle;
typedef uInt32             CalHandle;

#define DAQmx_Sys_GlobalChans           ... // Indicates an array that contains the names of all global channels saved on the system.
#define DAQmx_Sys_Scales                ... // Indicates an array that contains the names of all custom scales saved on the system.
#define DAQmx_Sys_Tasks                 ... // Indicates an array that contains the names of all tasks saved on the system.
#define DAQmx_Sys_DevNames              ... // Indicates the names of all devices installed in the system.
#define DAQmx_Sys_NIDAQMajorVersion     ... // Indicates the major portion of the installed version of NI-DAQ, such as 7 for version 7.0.
#define DAQmx_Sys_NIDAQMinorVersion     ... // Indicates the minor portion of the installed version of NI-DAQ, such as 0 for version 7.0.

#define DAQmx_Task_Name			... // Indicates the name of the task.
#define DAQmx_Task_Channels		... // Indicates the names of all virtual channels in the task.
#define DAQmx_Task_NumChans 		... // Indicates the number of virtual channels in the task.
#define DAQmx_Task_Devices		... // Indicates an array containing the names of all devices in the task.
#define DAQmx_Task_NumDevices		... // Indicates the number of devices in the task.
#define DAQmx_Task_Complete		... // Indicates whether the task completed execution.

int32 DAQmxGetSystemInfoAttribute (int32 attribute, void *value, ...);

int32 DAQmxCreateTask (const char taskName[], TaskHandle *taskHandle);
int32 DAQmxClearTask (TaskHandle taskHandle);
int32 DAQmxStartTask (TaskHandle taskHandle);
int32 DAQmxStopTask (TaskHandle taskHandle);
int32 DAQmxGetTaskAttribute (TaskHandle taskHandle, int32 attribute, void *value, ...);

int32 DAQmxGetErrorString (int32 errorCode, char errorString[], uInt32 bufferSize);
int32 DAQmxGetExtendedErrorInfo (char errorString[], uInt32 bufferSize);


#define DAQmx_PhysicalChan_AI_TermCfgs	... // Indicates the list of terminal configurations supported by the channel.
#define DAQmx_PhysicalChan_AO_TermCfgs	... // Indicates the list of terminal configurations supported by the channel.
#define DAQmx_PhysicalChan_AO_ManualControlEnable ... // Specifies if you can control the physical channel externally via a manual control located on the device. You cannot simultaneously control a channel manually and with NI-DAQmx.
#define DAQmx_PhysicalChan_AO_ManualControlAmplitude ... // Indicates the current value of the front panel amplitude control for the physical channel in volts.
#define DAQmx_PhysicalChan_AO_ManualControlFreq	... // Indicates the current value of the front panel frequency control for the physical channel in hertz.
#define DAQmx_PhysicalChan_DI_PortWidth	... // Indicates in bits the width of digital input port.
#define DAQmx_PhysicalChan_DI_SampClkSupported ... // Indicates if the sample clock timing type is supported for the digital input physical channel.
#define DAQmx_PhysicalChan_DI_ChangeDetectSupported ... // Indicates if the change detection timing type is supported for the digital input physical channel.
#define DAQmx_PhysicalChan_DO_PortWidth ... // Indicates in bits the width of digital output port.
#define DAQmx_PhysicalChan_DO_SampClkSupported ... // Indicates if the sample clock timing type is supported for the digital output physical channel.
#define DAQmx_PhysicalChan_TEDS_MfgID ... // Indicates the manufacturer ID of the sensor.
#define DAQmx_PhysicalChan_TEDS_ModelNum ... // Indicates the model number of the sensor.
#define DAQmx_PhysicalChan_TEDS_SerialNum ... // Indicates the serial number of the sensor.
#define DAQmx_PhysicalChan_TEDS_VersionNum ... // Indicates the version number of the sensor.
#define DAQmx_PhysicalChan_TEDS_VersionLetter ... // Indicates the version letter of the sensor.
#define DAQmx_PhysicalChan_TEDS_BitStream ... // Indicates the TEDS binary bitstream without checksums.
#define DAQmx_PhysicalChan_TEDS_TemplateIDs ... // Indicates the IDs of the templates in the bitstream in BitStream.


int32 DAQmxGetDeviceAttribute (const char deviceName[], int32 attribute, void *value, ...);

#define DAQmx_Dev_IsSimulated ... // Indicates if the device is a simulated device.
#define DAQmx_Dev_ProductCategory ... // Indicates the product category of the device. This category corresponds to the category displayed in MAX when creating NI-DAQmx simulated devices.
#define DAQmx_Dev_ProductType ... // Indicates the product name of the device.
#define DAQmx_Dev_ProductNum ... // Indicates the unique hardware identification number for the device.
#define DAQmx_Dev_SerialNum ... // Indicates the serial number of the device. This value is zero if the device does not have a serial number.
#define DAQmx_Carrier_SerialNum ... // Indicates the serial number of the device carrier. This value is zero if the carrier does not have a serial number.
#define DAQmx_Dev_Chassis_ModuleDevNames ... // Indicates an array containing the names of the modules in the chassis.
#define DAQmx_Dev_AnlgTrigSupported ... // Indicates if the device supports analog triggering.
#define DAQmx_Dev_DigTrigSupported ... // Indicates if the device supports digital triggering.
#define DAQmx_Dev_AI_PhysicalChans ... // Indicates an array containing the names of the analog input physical channels available on the device.
#define DAQmx_Dev_AI_MaxSingleChanRate ... // Indicates the maximum rate for an analog input task if the task contains only a single channel from this device.
#define DAQmx_Dev_AI_MaxMultiChanRate ... // Indicates the maximum rate for an analog input task if the task contains multiple channels from this device. For multiplexed devices, divide this rate by the number of channels to determine the maximum sampling rate.
#define DAQmx_Dev_AI_MinRate ... // Indicates the minimum rate for an analog input task on this device. NI-DAQmx returns a warning or error if you attempt to sample at a slower rate.
#define DAQmx_Dev_AI_SimultaneousSamplingSupported ... // Indicates if the device supports simultaneous sampling.
#define DAQmx_Dev_AI_TrigUsage ... // Indicates the triggers supported by this device for an analog input task.
#define DAQmx_Dev_AI_VoltageRngs ... // Indicates pairs of input voltage ranges supported by this device. Each pair consists of the low value, followed by the high value.
#define DAQmx_Dev_AI_VoltageIntExcitDiscreteVals ... // Indicates the set of discrete internal voltage excitation values supported by this device. If the device supports ranges of internal excitation values, use Range Values to determine supported excitation values.
#define DAQmx_Dev_AI_VoltageIntExcitRangeVals ... // Indicates pairs of internal voltage excitation ranges supported by this device. Each pair consists of the low value, followed by the high value. If the device supports a set of discrete internal excitation values, use Discrete Values to determine the supported excitation values.
#define DAQmx_Dev_AI_CurrentRngs ... // Indicates the pairs of current input ranges supported by this device. Each pair consists of the low value, followed by the high value.
#define DAQmx_Dev_AI_CurrentIntExcitDiscreteVals ... // Indicates the set of discrete internal current excitation values supported by this device.
#define DAQmx_Dev_AI_FreqRngs ... // Indicates the pairs of frequency input ranges supported by this device. Each pair consists of the low value, followed by the high value.
#define DAQmx_Dev_AI_Gains ... // Indicates the input gain settings supported by this device.
#define DAQmx_Dev_AI_Couplings ... // Indicates the coupling types supported by this device.
#define DAQmx_Dev_AI_LowpassCutoffFreqDiscreteVals ... // Indicates the set of discrete lowpass cutoff frequencies supported by this device. If the device supports ranges of lowpass cutoff frequencies, use Range Values to determine supported frequencies.
#define DAQmx_Dev_AI_LowpassCutoffFreqRangeVals ... // Indicates pairs of lowpass cutoff frequency ranges supported by this device. Each pair consists of the low value, followed by the high value. If the device supports a set of discrete lowpass cutoff frequencies, use Discrete Values to determine the supported  frequencies.
#define DAQmx_Dev_AO_PhysicalChans ... // Indicates an array containing the names of the analog output physical channels available on the device.
#define DAQmx_Dev_AO_SampClkSupported ... // Indicates if the device supports the sample clock timing  type for analog output tasks.
#define DAQmx_Dev_AO_MaxRate ... // Indicates the maximum analog output rate of the device.
#define DAQmx_Dev_AO_MinRate ... // Indicates the minimum analog output rate of the device.
#define DAQmx_Dev_AO_TrigUsage ... // Indicates the triggers supported by this device for analog output tasks.
#define DAQmx_Dev_AO_VoltageRngs ... // Indicates pairs of output voltage ranges supported by this device. Each pair consists of the low value, followed by the high value.
#define DAQmx_Dev_AO_CurrentRngs ... // Indicates pairs of output current ranges supported by this device. Each pair consists of the low value, followed by the high value.
#define DAQmx_Dev_AO_Gains ... // Indicates the output gain settings supported by this device.
#define DAQmx_Dev_DI_Lines ... // Indicates an array containing the names of the digital input lines available on the device.
#define DAQmx_Dev_DI_Ports ... // Indicates an array containing the names of the digital input ports available on the device.
#define DAQmx_Dev_DI_MaxRate ... // Indicates the maximum digital input rate of the device.
#define DAQmx_Dev_DI_TrigUsage ... // Indicates the triggers supported by this device for digital input tasks.
#define DAQmx_Dev_DO_Lines ... // Indicates an array containing the names of the digital output lines available on the device.
#define DAQmx_Dev_DO_Ports ... // Indicates an array containing the names of the digital output ports available on the device.
#define DAQmx_Dev_DO_MaxRate ... // Indicates the maximum digital output rate of the device.
#define DAQmx_Dev_DO_TrigUsage ... // Indicates the triggers supported by this device for digital output tasks.
#define DAQmx_Dev_CI_PhysicalChans ... // Indicates an array containing the names of the counter input physical channels available on the device.
#define DAQmx_Dev_CI_TrigUsage ... // Indicates the triggers supported by this device for counter input tasks.
#define DAQmx_Dev_CI_SampClkSupported ... // Indicates if the device supports the sample clock timing type for counter input tasks.
#define DAQmx_Dev_CI_MaxSize ... // Indicates in bits the size of the counters on the device.
#define DAQmx_Dev_CI_MaxTimebase ... // Indicates in hertz the maximum counter timebase frequency.
#define DAQmx_Dev_CO_PhysicalChans ... // Indicates an array containing the names of the counter output physical channels available on the device.
#define DAQmx_Dev_CO_TrigUsage ... // Indicates the triggers supported by this device for counter output tasks.
#define DAQmx_Dev_CO_MaxSize ... // Indicates in bits the size of the counters on the device.
#define DAQmx_Dev_CO_MaxTimebase ... // Indicates in hertz the maximum counter timebase frequency.
#define DAQmx_Dev_NumDMAChans ... // Indicates the number of DMA channels on the device.
#define DAQmx_Dev_BusType ... // Indicates the bus type of the device.
#define DAQmx_Dev_PCI_BusNum ... // Indicates the PCI bus number of the device.
#define DAQmx_Dev_PCI_DevNum ... // Indicates the PCI slot number of the device.
#define DAQmx_Dev_PXI_ChassisNum ... // Indicates the PXI chassis number of the device, as identified in MAX.
#define DAQmx_Dev_PXI_SlotNum ... // Indicates the PXI slot number of the device.
#define DAQmx_Dev_CompactDAQ_ChassisDevName ... // Indicates the name of the CompactDAQ chassis that contains this module.
#define DAQmx_Dev_CompactDAQ_SlotNum ... // Indicates the slot number in which this module is located in the CompactDAQ chassis.
#define DAQmx_Dev_TCPIP_Hostname ... // Indicates the IPv4 hostname of the device.
#define DAQmx_Dev_TCPIP_EthernetIP ... // Indicates the IPv4 address of the Ethernet interface. This property returns an empty string if the Ethernet interface cannot acquire an address.
#define DAQmx_Dev_TCPIP_WirelessIP ... // Indicates the IPv4 address of the wireless interface.This property returns an empty string if the wireless interface cannot acquire an address.
#define DAQmx_Dev_Terminals ... // Indicates a list of all terminals on the device.


int32 DAQmxGetPhysicalChanAttribute (const char physicalChannel[], int32 attribute, void *value, ...);
int32 DAQmxGetChanAttribute (TaskHandle taskHandle, const char channel[], int32 attribute, void *value, ...);
''');

lib = ffi.verify('''
#include "NIDAQmx.h"
''', include_dirs=['C:\Program Files\National Instruments\NI-DAQ\DAQmx ANSI C Dev\include'], libraries=['NIDAQmx'], 
library_dirs=['C:\Program Files\National Instruments\NI-DAQ\DAQmx ANSI C Dev\lib\msvc'])

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

def devices():
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
    
def make_task(name=''):
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
			names_in = [AnalogInput(x.strip()) for x in ffi.string(pchan_in).split(',')] 
		else: 
			names_in = []

		if pchan_out is not None: 
			names_out = [AnalogOutput(x.strip()) for x in ffi.string(pchan_out).split(',')] 
		else: 
			names_out = []
			
		return (names_in, names_out)
	
	def __repr__(self):
		#i,o = self._get_phys_channel_props(), 'thing'
		i,o = self._get_phys_channel_props()
		return 'Device(\'{}\', ain=\'{}\', aout=\'{}\')'.format(self._name, i, o) 

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
    
	def add_channel(self, type=None):
		pass

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

class PhysicalChannel(object):
	#_term_cfgs = {lib.DAQmx_Val_Bit_TermCfg_RSE: 'RSE', lib.DAQmx_Val_Bit_TermCfg_NRSE: 'NRSE', 
        # lib.DAQmx_Val_Bit_TermCfg_Diff: 'Diff', lib.DAQmx_Val_Bit_TermCfg_PseudoDIFF: 'PseudoDiff'}
	
	def __init__(self, name):
		self._name = name

	name = property(lambda self: self._name)

class AnalogInput(PhysicalChannel):
	# TODO: if there exists some additional information upon init (or maybe even new) 
	# create a subclass of AnalogInput that will contain the right additional properties
	# for the type of channel created

	def __repr__(self):
		return 'AnalogInput(\'{}\')'.format(self._name)
	
	'''
	def _get_TermCfgs(self):
		val = ffi.new('int32 *')
		ai_cfg = _get_phys_channel_attr(self._name, lib.DAQmx_PhysicalChan_AI_TermCfgs, val)
		return ai_cfg[0]
		#return super(AnalogInput, self)._term_cfgs[ai_cfg[0]]
	'''

class AnalogInputVoltage(AnalogInput):
	pass

class AnalogInputVoltageRMS(AnalogInput):
	pass

class AnalogOutput(PhysicalChannel):
	def __repr__(self):
		return 'AnalogOutput(\'{}\')'.format(self._name)

class AnalogOutputCurrent(AnalogOutput):
	pass

class AnalogOutputVoltage(AnalogOutput):
	pass

class DigitalInput(PhysicalChannel):
	pass

if __name__ == '__main__':
	print 'Running on NI-DAQmx version {}.{}'.format(_maj_version(), _min_version())
	
	print 'Devices:'
	for d in devices():
		i,o = d._get_phys_channel_props()
		print '> Device {}'.format(d.name)
		print '\tInputs  >> {}'.format(i)
		print '\tOutputs >> {}'.format(o)

	print 'Channels: {}'.format(_sys_global_chans())

	print 'Tasks: {}'.format(_sys_tasks())
	a,b,c = (Task(x) for x in 'abc')
	print 'Task names: ', a.name, b.name, c.name
	print 'Tasks: {}'.format(_sys_tasks())
	print 'Task channels: ', a.channels, b.channels, c.channels
	del a, b, c
	print 'Tasks: {}'.format(_sys_tasks())

