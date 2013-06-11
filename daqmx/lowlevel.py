from .clib import (ffi, lib, handle_error)
from .defs import SystemAttributes, Units, SampleMode, ActiveEdge, \
    EventType, SynchronousEventCallbacks, FillMode, Read, TerminalConfig
from bidict import bidict
import weakref
import logging

log = logging.getLogger('daqmx')

__all__ = ['query_devices', 'query_tasks', 'query_version', 'make_task', 'clear_task', 
    'control_task', 'query_task_is_done', 'start_task', 'stop_task', 'reset_device', 
    'read_f64']

'''holds mapping between created task and handle'''
task_map = bidict()

'''holds callbacks registered'''
callback_store = weakref.WeakKeyDictionary()

def query_devices():
    '''get devices that NIDAQmx knows about '''
    # TODO: eventually this should return Device classes

    tstr = SystemAttributes.get('devices')
    
    if tstr is not None:
        return [x for x in tstr.split(',')]
    else:
        return []

def reset_device(name):
    '''aborts all tasks and resets device to initialized state
    
    Immediately aborts all tasks associated with a device and returns the device to an 
    initialized state. Aborting a task stops and releases any resources the task reserved.
    '''
    res = lib.DAQmxResetDevice(name)
    handle_error(res)

def query_tasks():
    '''get tasks that exist in the library but don't show up in the task list'''
    return task_map.keys()

def query_version():
    '''return version of the NIDAQmx library interface in use'''

    return float(SystemAttributes.get('major_version')) + \
            0.1*float(SystemAttributes.get('minor_version'))

def make_task(task_name):
    '''create a task and return a handle to that task'''
    if isinstance(task_name, basestring):
        p = ffi.new('TaskHandle *')
        res = lib.DAQmxCreateTask(task_name, p)
        handle_error(res)
        task_map.update({task_name: p[0]})
        return p[0]
    else:
    	raise TypeError('task_name must be a string')

def clear_task(handle):
    '''remove task from the system, stopping it if necessary
    '''

    if isinstance(handle, (int, long)):
        res = lib.DAQmxClearTask(handle)
        del task_map[:handle]
        handle_error(res)
    elif isinstance(handle, basestring):
        h = task_map[handle]
        res = lib.DAQmxClearTask(h)
        del task_map[handle]
        handle_error(res)
    else:
    	raise TypeError('handle must be integer')

def start_task(handle):
    '''begin measurement or generation
    '''

    if isinstance(handle, (int, long)):
        res = lib.DAQmxStartTask(handle)
        handle_error(res)
    elif isinstance(handle, basestring):
        h = task_map[handle]
        res = lib.DAQmxStartTask(h)
        handle_error(res)
    else:
    	raise TypeError('handle must be integer')

def stop_task(handle):
    '''stops measurement or generation
    '''
    if isinstance(handle, (int, long)):
        res = lib.DAQmxStopTask(handle)
        handle_error(res)
    elif isinstance(handle, basestring):
        h = task_map[handle]
        res = lib.DAQmxStopTask(h)
        handle_error(res)
    else:
    	raise TypeError('handle must be integer')

def query_task_is_done(handle):
    '''checks if task completed measurement
    '''
    if isinstance(handle, (int, long)):
        done_p = ffi.new('bool32 *')
        res = lib.DAQmxIsTaskDone(handle, done_p)
        handle_error(res)
        return bool(done_p[0])
    elif isinstance(handle, basestring):
        h = task_map[handle]
        done_p = ffi.new('bool32 *')
        res = lib.DAQmxIsTaskDone(h, done_p)
        handle_error(res)
        return bool(done_p[0])
    else:
    	raise TypeError('handle must be integer')

def control_task(handle, task_state):
    '''advanced function that causes task to transition states

    Task lifetime is represented by a state machine. This function causes the
    state machine to transition between states. The function accepts TaskState 
    attributes as values. As stated in documentation,
    
    TaskState.Start   Starts execution of the task. 
    TaskState.Stop   Stops execution of the task. 
    TaskState.Verify   Verifies that all task parameters are valid for the hardware. 
    TaskState.Commit   Programs the hardware as much as possible according to the task configuration. 
    TaskState.Reserve   Reserves the hardware resources needed for the task. No other tasks can reserve these same resources. 
    TaskState.Unreserve   Releases all previously reserved resources. 
    TaskState.Abort   Abort is used to stop an operation, such as Read or Write, that is currently active. Abort puts the task into an unstable but recoverable state. To recover the task, call Start to restart the task or call Stop to reset the task without starting it. 
    '''

    if isinstance(handle, (int, long)):
        res = lib.DAQmxTaskControl(handle, task_state)
        handle_error(res)
    elif isinstance(handle, basestring):
        h = task_map[handle]
        res = lib.DAQmxTaskControl(h, task_state)
        handle_error(res)
    else:
    	raise TypeError('handle must be integer')

def load_task(name):
    raise NotImplementedError('loading a task from MAX is not implemented yet')

def add_input_voltage_channel(handle, pchannel, min, max, units=Units.Volts, name=None, \
        term_config=TerminalConfig.Default, custom_scale=None):
    '''adds an analog input channel to a task given by the handle

    '''
    if name is None: name = ffi.NULL
    if units is not Units.FromCustomScale: custom_scale = ffi.NULL 
    
    log.info('adding voltage channel %s', str(pchannel))

    if units == Units.Volts: ustr = 'Units.Volts'

    log.debug('calling with f(%s, %s, %f, %f, %s, %s, %s, %s',
            handle, pchannel, min, max, units, name, str(term_config), str(custom_scale))

    if isinstance(handle, (int, long)):
        res = lib.DAQmxCreateAIVoltageChan(handle, pchannel, name, term_config, min, max, units, custom_scale)
        handle_error(res)
    elif isinstance(handle, basestring):
        h = task_map[handle]
        res = lib.DAQmxCreateAIVoltageChan(h, pchannel, name, term_config, min, max, units, custom_scale)
        handle_error(res)
    else:
    	raise TypeError('handle must be integer or string')

def set_timing_sample_clock(handle, rate, n_samples, sample_mode=SampleMode.Finite, active_edge=ActiveEdge.Rising, \
        source='OnboardClock'):
    if isinstance(handle, (int, long)):
        res = lib.DAQmxCfgSampClkTiming(handle, source, rate, active_edge, sample_mode, n_samples)
        handle_error(res)
    elif isinstance(handle, basestring):
        h = task_map[handle]
        res = lib.DAQmxCfgSampClkTiming(h, source, rate, active_edge, sample_mode, n_samples)
        handle_error(res)
    else:
    	raise TypeError('handle must be integer or string')

def set_timing_implicit(handle, n_samples, sample_mode=SampleMode.Finite):
    if isinstance(handle, (int, long)):
        res = lib.DAQmxCfgImplicitTiming(handle, sample_mode, n_samples)
        handle_error(res)
    elif isinstance(handle, basestring):
        h = task_map[handle]
        res = lib.DAQmxCfgImplicitTiming(h, sample_mode, n_samples)
        handle_error(res)
    else:
    	raise TypeError('handle must be integer or string')

def register_nsamples_callback(handle, nsamples, callback_function, callback_data=None, 
        event_type=EventType.Acquired_Into_Buffer, options=0):

    callback_store[callback_function] = ffi.callback('int32(TaskHandle, int32, uInt32, void*)', callback_function)
    callback = callback_store[callback_function]

    if callback_data is None: callback_data = ffi.NULL

    if isinstance(handle, (int, long)):
        res = lib.DAQmxRegisterEveryNSamplesEvent(handle, event_type, nsamples, options, callback, \
            callback_data)
        handle_error(res)
    elif isinstance(handle, basestring):
        h = task_map[handle]

        res = lib.DAQmxRegisterEveryNSamplesEvent(h, event_type, nsamples, options, callback, \
            callback_data)
        handle_error(res)
    else:
    	raise TypeError('handle must be integer or string')

def unregister_nsamples_callback(handle, event_type):
    if isinstance(handle, (int, long)):
        res = lib.DAQmxRegisterEveryNSamplesEvent(handle, event_type, 0, 0, ffi.NULL, ffi.NULL)
        handle_error(res)
    elif isinstance(handle, basestring):
        h = task_map[handle]

        res = lib.DAQmxRegisterEveryNSamplesEvent(h, event_type, 0, 0, ffi.NULL, ffi.NULL)
        handle_error(res)

def set_input_buffer_size(handle, size):
    if isinstance(handle, (int, long)):
        res = lib.DAQmxCfgInputBuffer(handle, size)
        handle_error(res)
    elif isinstance(handle, basestring):
        h = task_map[handle]
        res = lib.DAQmxCfgInputBuffer(h, size)
        handle_error(res)

def set_output_buffer_size(handle, size):
    if isinstance(handle, (int, long)):
        res = lib.DAQmxCfgOutputBuffer(handle, size)
        handle_error(res)
    elif isinstance(handle, basestring):
        h = task_map[handle]
        res = lib.DAQmxCfgOutputBuffer(h, size)
        handle_error(res)

def read_f64(handle, buf_size, n_samps_per_channel=Read.All, timeout=0., fill_mode=FillMode.GroupByScanNumber):
    data = ffi.new('float64[]', buf_size)
    nsamp = ffi.new('int32 *')

    if isinstance(handle, (int, long)):
        res = lib.DAQmxReadAnalogF64(handle, n_samps_per_channel, timeout, fill_mode, \
                data, buf_size, nsamp, ffi.NULL)
        try:
            handle_error(res)
        except RuntimeWarning as e:
            log.warning(e)
        finally:
            log.debug('count is %d', nsamp[0])
            return (ffi.buffer(data), nsamp[0])

    elif isinstance(handle, basestring):
        h = task_map[handle]

        res = lib.DAQmxReadAnalogF64(h, n_samps_per_channel, timeout, fill_mode, \
                data, buf_size, nsamp, ffi.NULL)
        try:
            handle_error(res)
        except RuntimeWarning as e:
            log.warning(e)
        finally:
            log.debug('count is %d', nsamp[0])
            return (ffi.buffer(data), nsamp[0])

