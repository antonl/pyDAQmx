from . import lib

Volts = lib.DAQmx_Val_Volts
FromCustomScale = lib.DAQmx_Val_FromCustomScale 

#TODO Rename this file to attributes, values, or types maybe?
RisingEdge = lib.DAQmx_Val_Rising
FallingEdge = lib.DAQmx_Val_Falling

FiniteSamples = lib.DAQmx_Val_FiniteSamps
ContinuousSamples = lib.DAQmx_Val_ContSamps
HWTimedSinglePoint = lib.DAQmx_Val_HWTimedSinglePoint


Auto = lib.DAQmx_Val_Auto
GroupByChannel = lib.DAQmx_Val_GroupByChannel 
GroupByScanNumber = lib.DAQmx_Val_GroupByScanNumber
WaitInfinitely = lib.DAQmx_Val_WaitInfinitely
