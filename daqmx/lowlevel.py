from .clib import (ffi, lib, handle_error)
from .defs import SystemAttributes
from bidict import bidict
from itertools import ifilter

__all__ = ['query_devices', 'query_tasks', 'query_version', 'make_task', 'clear_task', 
    'control_task', 'query_task_is_done', 'uncommitted_tasks']

'''holds mapping between created task and handle'''
task_map = bidict()

def query_devices():
    '''get devices that NIDAQmx knows about '''
    # TODO: eventually this should return Device classes

    tstr = SystemAttributes.get('devices')
    
    if tstr is not None:
        return [x for x in tstr.split(',')]
    else:
        return []

def query_tasks():
    '''get tasks that are committed in the system 
    
    Querries the tasks attribute within the system. This function returns only
    the verified and committed tasks, not those that have just been created,
    so tasks that have been created but have no channels added to them do not
    show up in this list.
    '''
    # TODO: eventually this should return Task classes

    tstr = SystemAttributes.get('tasks')
    
    if tstr is not None:
        return [x for x in tstr.split(',')]
    else:
        return []

def uncommitted_tasks():
    tmp = []
    for i in ifilter(lambda x: x not in query_tasks(), task_map.keys()):
        tmp.append(i)
    return tmp

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
