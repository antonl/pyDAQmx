from cffi import FFI

ffi = FFI()
ffi.cdef('''
typedef unsigned long uInt32; 
typedef signed long int32;
typedef float float32;
typedef double float64;

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

int32 DAQmxCreateAIVoltageChan (TaskHandle taskHandle, const char physicalChannel[], const char nameToAssignToChannel[], int32 terminalConfig, float64 minVal, float64 maxVal, int32 units, const char customScaleName[]);

#define DAQmx_Val_Cfg_Default ... // Default

#define DAQmx_Val_Volts ... // Volts
#define DAQmx_Val_FromCustomScale  ... // Units a custom scale specifies. Use customScaleName to specify a custom scale.
''');

lib = ffi.verify('''
#include "NIDAQmx.h"
''', include_dirs=['C:\Program Files\National Instruments\NI-DAQ\DAQmx ANSI C Dev\include'], libraries=['NIDAQmx'], 
library_dirs=['C:\Program Files\National Instruments\NI-DAQ\DAQmx ANSI C Dev\lib\msvc'])

from .daqmx import *

