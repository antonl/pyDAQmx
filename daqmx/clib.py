from cffi import FFI


# Typedefs 
header_str = '''
typedef unsigned long uInt32; 
typedef signed long int32;
typedef unsigned long long uInt64;

typedef float float32;
typedef double float64;

typedef uInt32 bool32;

typedef uInt32 TaskHandle;
typedef uInt32 CalHandle;
'''

# System attributes and functions to read them
header_str += '''
#define DAQmx_Sys_GlobalChans           ... // Indicates an array that contains the names of all global channels saved on the system.
#define DAQmx_Sys_Scales                ... // Indicates an array that contains the names of all custom scales saved on the system.
#define DAQmx_Sys_Tasks                 ... // Indicates an array that contains the names of all tasks saved on the system.
#define DAQmx_Sys_DevNames              ... // Indicates the names of all devices installed in the system.
#define DAQmx_Sys_NIDAQMajorVersion     ... // Indicates the major portion of the installed version of NI-DAQ, such as 7 for version 7.0.
#define DAQmx_Sys_NIDAQMinorVersion     ... // Indicates the minor portion of the installed version of NI-DAQ, such as 0 for version 7.0.

int32 DAQmxGetSystemInfoAttribute (int32 attribute, void *value, ...);
'''

# Task related functions and definitions
header_str += '''
#define DAQmx_Task_Name			... // Indicates the name of the task.
#define DAQmx_Task_Channels		... // Indicates the names of all virtual channels in the task.
#define DAQmx_Task_NumChans		... // Indicates the number of virtual channels in the task.
#define DAQmx_Task_Devices		... // Indicates an array containing the names of all devices in the task.
#define DAQmx_Task_NumDevices	... // Indicates the number of devices in the task.
#define DAQmx_Task_Complete		... // Indicates whether the task completed execution.

int32 DAQmxGetTaskAttribute (TaskHandle taskHandle, int32 attribute, void *value, ...);

int32 DAQmxCreateTask (const char taskName[], TaskHandle *taskHandle);
int32 DAQmxClearTask (TaskHandle taskHandle);
int32 DAQmxStartTask (TaskHandle taskHandle);
int32 DAQmxStopTask (TaskHandle taskHandle);
int32 DAQmxIsTaskDone (TaskHandle taskHandle, bool32 *isTaskDone);

#define DAQmx_Val_Task_Start    ... // Start
#define DAQmx_Val_Task_Stop     ... // Stop
#define DAQmx_Val_Task_Verify   ... // Verify
#define DAQmx_Val_Task_Commit   ... // Commit
#define DAQmx_Val_Task_Reserve  ... // Reserve
#define DAQmx_Val_Task_Unreserve ...// Unreserve
#define DAQmx_Val_Task_Abort    ... // Abort

int32 DAQmxTaskControl (TaskHandle taskHandle, int32 action);
'''

# Error handling
header_str += '''
int32 DAQmxGetErrorString (int32 errorCode, char errorString[], uInt32 bufferSize);
int32 DAQmxGetExtendedErrorInfo (char errorString[], uInt32 bufferSize);
'''

# Device attributes and reset 
header_str += '''
int32 DAQmxResetDevice (const char deviceName[]);

int32 DAQmxGetDevIsSimulated(const char device[], bool32 *data);

int32 DAQmxGetDevProductCategory(const char device[], int32 *data);
#define DAQmx_Val_MSeriesDAQ ... // M Series DAQ
#define DAQmx_Val_ESeriesDAQ ... // E Series DAQ
#define DAQmx_Val_SSeriesDAQ ... // S Series DAQ
#define DAQmx_Val_BSeriesDAQ ... // B Series DAQ
#define DAQmx_Val_SCSeriesDAQ ... // SC Series DAQ
#define DAQmx_Val_USBDAQ ... // USB DAQ
#define DAQmx_Val_AOSeries ... // AO Series
#define DAQmx_Val_DigitalIO ... // Digital I/O
#define DAQmx_Val_TIOSeries ... // TIO Series
#define DAQmx_Val_DynamicSignalAcquisition ... // Dynamic Signal Acquisition
#define DAQmx_Val_Switches ... // Switches
#define DAQmx_Val_CompactDAQChassis ... // CompactDAQ Chassis
#define DAQmx_Val_CSeriesModule ... // C Series Module
#define DAQmx_Val_SCXIModule ... // SCXI Module
#define DAQmx_Val_SCCConnectorBlock ... // SCC Connector Block
#define DAQmx_Val_SCCModule ... // SCC Module
#define DAQmx_Val_NIELVIS ... // NI ELVIS
#define DAQmx_Val_NetworkDAQ ... // Network DAQ
#define DAQmx_Val_Unknown ... // Unknown

int32 DAQmxGetDevProductType(const char device[], char *data, uInt32 bufferSize);
int32 DAQmxGetDevProductNum(const char device[], uInt32 *data);
int32 DAQmxGetDevSerialNum(const char device[], uInt32 *data);

int32 DAQmxGetCarrierSerialNum(const char device[], uInt32 *data);
int32 DAQmxGetDevChassisModuleDevNames(const char device[], char *data, uInt32 bufferSize);
int32 DAQmxGetDevAnlgTrigSupported(const char device[], bool32 *data);
int32 DAQmxGetDevDigTrigSupported(const char device[], bool32 *data);
int32 DAQmxGetDevAIPhysicalChans(const char device[], char *data, uInt32 bufferSize);
int32 DAQmxGetDevAIMaxSingleChanRate(const char device[], float64 *data);
int32 DAQmxGetDevAIMaxMultiChanRate(const char device[], float64 *data);
int32 DAQmxGetDevAIMinRate(const char device[], float64 *data);
int32 DAQmxGetDevAISimultaneousSamplingSupported(const char device[], bool32 *data);

// Uses bits from enum TriggerUsageTypeBits
int32 DAQmxGetDevAITrigUsage(const char device[], int32 *data);
int32 DAQmxGetDevAIVoltageRngs(const char device[], float64 *data, uInt32 arraySizeInSamples);
int32 DAQmxGetDevAIVoltageIntExcitDiscreteVals(const char device[], float64 *data, uInt32 arraySizeInSamples);
int32 DAQmxGetDevAIVoltageIntExcitRangeVals(const char device[], float64 *data, uInt32 arraySizeInSamples);
int32 DAQmxGetDevAICurrentRngs(const char device[], float64 *data, uInt32 arraySizeInSamples);
int32 DAQmxGetDevAICurrentIntExcitDiscreteVals(const char device[], float64 *data, uInt32 arraySizeInSamples);
int32 DAQmxGetDevAIFreqRngs(const char device[], float64 *data, uInt32 arraySizeInSamples);
int32 DAQmxGetDevAIGains(const char device[], float64 *data, uInt32 arraySizeInSamples);
// Uses bits from enum CouplingTypeBits
int32 DAQmxGetDevAICouplings(const char device[], int32 *data);
int32 DAQmxGetDevAILowpassCutoffFreqDiscreteVals(const char device[], float64 *data, uInt32 arraySizeInSamples);
int32 DAQmxGetDevAILowpassCutoffFreqRangeVals(const char device[], float64 *data, uInt32 arraySizeInSamples);
int32 DAQmxGetDevAOPhysicalChans(const char device[], char *data, uInt32 bufferSize);
int32 DAQmxGetDevAOSampClkSupported(const char device[], bool32 *data);
int32 DAQmxGetDevAOMaxRate(const char device[], float64 *data);
int32 DAQmxGetDevAOMinRate(const char device[], float64 *data);
// Uses bits from enum TriggerUsageTypeBits
int32 DAQmxGetDevAOTrigUsage(const char device[], int32 *data);
int32 DAQmxGetDevAOVoltageRngs(const char device[], float64 *data, uInt32 arraySizeInSamples);
int32 DAQmxGetDevAOCurrentRngs(const char device[], float64 *data, uInt32 arraySizeInSamples);
int32 DAQmxGetDevAOGains(const char device[], float64 *data, uInt32 arraySizeInSamples);
int32 DAQmxGetDevDILines(const char device[], char *data, uInt32 bufferSize);
int32 DAQmxGetDevDIPorts(const char device[], char *data, uInt32 bufferSize);
int32 DAQmxGetDevDIMaxRate(const char device[], float64 *data);
// Uses bits from enum TriggerUsageTypeBits
int32 DAQmxGetDevDOLines(const char device[], char *data, uInt32 bufferSize);
int32 DAQmxGetDevDOPorts(const char device[], char *data, uInt32 bufferSize);
int32 DAQmxGetDevDOMaxRate(const char device[], float64 *data);
// Uses bits from enum TriggerUsageTypeBits
int32 DAQmxGetDevDOTrigUsage(const char device[], int32 *data);
int32 DAQmxGetDevCIPhysicalChans(const char device[], char *data, uInt32 bufferSize);
// Uses bits from enum TriggerUsageTypeBits
int32 DAQmxGetDevCITrigUsage(const char device[], int32 *data);
int32 DAQmxGetDevCISampClkSupported(const char device[], bool32 *data);
int32 DAQmxGetDevCIMaxSize(const char device[], uInt32 *data);
int32 DAQmxGetDevCIMaxTimebase(const char device[], float64 *data);
int32 DAQmxGetDevCOPhysicalChans(const char device[], char *data, uInt32 bufferSize);
// Uses bits from enum TriggerUsageTypeBits
int32 DAQmxGetDevCOTrigUsage(const char device[], int32 *data);
int32 DAQmxGetDevCOMaxSize(const char device[], uInt32 *data);
int32 DAQmxGetDevCOMaxTimebase(const char device[], float64 *data);
int32 DAQmxGetDevNumDMAChans(const char device[], uInt32 *data);
// Uses value set BusType
int32 DAQmxGetDevBusType(const char device[], int32 *data);
int32 DAQmxGetDevPCIBusNum(const char device[], uInt32 *data);
int32 DAQmxGetDevPCIDevNum(const char device[], uInt32 *data);
int32 DAQmxGetDevPXIChassisNum(const char device[], uInt32 *data);
int32 DAQmxGetDevPXISlotNum(const char device[], uInt32 *data);
int32 DAQmxGetDevCompactDAQChassisDevName(const char device[], char *data, uInt32 bufferSize);
int32 DAQmxGetDevCompactDAQSlotNum(const char device[], uInt32 *data);
int32 DAQmxGetDevTCPIPHostname(const char device[], char *data, uInt32 bufferSize);
int32 DAQmxGetDevTCPIPEthernetIP(const char device[], char *data, uInt32 bufferSize);
int32 DAQmxGetDevTCPIPWirelessIP(const char device[], char *data, uInt32 bufferSize);
int32 DAQmxGetDevTerminals(const char device[], char *data, uInt32 bufferSize);
'''

# Physical channel properties
header_str += '''
int32 DAQmxGetPhysicalChanAttribute (const char physicalChannel[], int32 attribute, void *value, ...);

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
'''

# Units
header_str += '''
#define DAQmx_Val_Volts ... // Volts
#define DAQmx_Val_FromCustomScale  ... // Units a custom scale specifies. Use customScaleName to specify a custom scale.
#define DAQmx_Val_Amps ... // Amps
'''

# Terminal Config
header_str += '''
#define DAQmx_Val_Cfg_Default ... // Default
#define DAQmx_Val_RSE ... // Referenced single ended
#define DAQmx_Val_NRSE ... // Non-referenced single ended
#define DAQmx_Val_Diff ... // Differential
#define DAQmx_Val_PseudoDiff ... // Psuedo differential
'''

# Trigger Usage Types
header_str += '''
#define DAQmx_Val_Bit_TriggerUsageTypes_Advance ... // Device supports advance triggers
#define DAQmx_Val_Bit_TriggerUsageTypes_Pause ... // Device supports pause triggers
#define DAQmx_Val_Bit_TriggerUsageTypes_Reference ... // Device supports reference triggers
#define DAQmx_Val_Bit_TriggerUsageTypes_Start ... // Device supports start triggers
#define DAQmx_Val_Bit_TriggerUsageTypes_Handshake ... // Device supports handshake triggers
#define DAQmx_Val_Bit_TriggerUsageTypes_ArmStart ... // Device supports arm start triggers
'''

# Coupling types
header_str += '''
#define DAQmx_Val_Bit_CouplingTypes_AC ... // Device supports AC coupling
#define DAQmx_Val_Bit_CouplingTypes_DC ... // Device supports DC coupling
#define DAQmx_Val_Bit_CouplingTypes_Ground ... // Device supports ground coupling
#define DAQmx_Val_Bit_CouplingTypes_HFReject ... // Device supports High Frequency Reject coupling
#define DAQmx_Val_Bit_CouplingTypes_LFReject ... // Device supports Low Frequency Reject coupling
#define DAQmx_Val_Bit_CouplingTypes_NoiseReject ... // Device supports Noise Reject coupling
'''

# Sampling Settings
header_str += '''
int32 DAQmxCfgSampClkTiming (TaskHandle taskHandle, const char source[], float64 rate, int32 activeEdge, int32 sampleMode, uInt64 sampsPerChanToAcquire);
int32 DAQmxCfgImplicitTiming (TaskHandle taskHandle, int32 sampleMode, uInt64 sampsPerChanToAcquire);
int32 DAQmxCfgChangeDetectionTiming (TaskHandle taskHandle, const char risingEdgeChan[], const char fallingEdgeChan[], int32 sampleMode, uInt64 sampsPerChan);

#define DAQmx_Val_Rising ... // Rising
#define DAQmx_Val_Falling ... // Falling

#define DAQmx_Val_FiniteSamps ... // Finite Samples
#define DAQmx_Val_ContSamps ... // Continuous Samples
#define DAQmx_Val_HWTimedSinglePoint ... // Hardware Timed Single Point
'''

# Callbacks
header_str += '''
int32 DAQmxRegisterEveryNSamplesEvent(TaskHandle taskHandle, int32 everyNsamplesEventType, uInt32 nSamples, uInt32 options, int32 (*)(TaskHandle, int32, uInt32, void *), void *callbackData);

#define DAQmx_Val_SynchronousEventCallbacks ...
#define DAQmx_Val_Acquired_Into_Buffer ...
#define DAQmx_Val_Transferred_From_Buffer ...
'''

# Buffer configuration
header_str += '''
int32 DAQmxCfgInputBuffer (TaskHandle taskHandle, uInt32 numSampsPerChan);
int32 DAQmxCfgOutputBuffer (TaskHandle taskHandle, uInt32 numSampsPerChan);
'''

# Create channels
header_str += '''
int32 DAQmxCreateAIVoltageChan (TaskHandle taskHandle, const char physicalChannel[], const char nameToAssignToChannel[], int32 terminalConfig, float64 minVal, float64 maxVal, int32 units, const char customScaleName[]);
'''

# Reading data and configuration options
header_str += '''
int32 DAQmxReadAnalogF64 (TaskHandle taskHandle, int32 numSampsPerChan, float64 timeout, bool32 fillMode, float64 readArray[], uInt32 arraySizeInSamps, int32 *sampsPerChanRead, bool32 *reserved);

#define DAQmx_Val_WaitInfinitely ...
#define DAQmx_Val_Auto ...
#define DAQmx_Val_GroupByChannel ... // Group by Channel
#define DAQmx_Val_GroupByScanNumber ... // Group by Scan Number
'''

# Misc
header_str += '''
int32 DAQmxGetChanAttribute (TaskHandle taskHandle, const char channel[], int32 attribute, void *value, ...);
'''

ffi = FFI()
ffi.cdef(header_str);

lib = ffi.verify(' #include "NIDAQmx.h" ', include_dirs=['C:\Program Files\National Instruments\NI-DAQ\DAQmx ANSI C Dev\include'], libraries=['NIDAQmx'], 
library_dirs=['C:\Program Files\National Instruments\NI-DAQ\DAQmx ANSI C Dev\lib\msvc'])

def handle_error(res):
    '''utility function for converting error code into exceptions

    The convention for DAQmx is to return an error code for every operation.
    This function checks the error code and converts that code to an exception 
    with the message string as the body.
    '''

    if res == 0: return
    
    msg = ffi.new('char[2048]')
    
    lib.DAQmxGetErrorString(res, msg, 2048)
    py_s = ffi.string(msg)
    del msg
    
    if res < 0:
        raise RuntimeError(py_s + ' ({:d})'.format(res))
    elif res > 0:
        raise RuntimeWarning(py_s + ' ({:d})'.format(res))
