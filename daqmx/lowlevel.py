from .clib import (ffi, lib)
from .defs import SystemAttributes

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
        raise RuntimeWarning(py_s + ' ({:d}'.format(res))

def query_devices():
    '''get devices that NIDAQmx knows about '''
    # TODO: eventually this should return Device classes

    tstr = SystemAttributes['devices']
    
    if tstr is not None:
        return [x for x in tstr.split(',')]
    else:
        return []

def query_tasks():
    '''get tasks registered in the system '''
    # TODO: eventually this should return Task classes

    tstr = SystemAttributes['tasks']
    
    if tstr is not None:
        return [x for x in tstr.split(',')]
    else:
        return []

def query_version():
    '''return version of the NIDAQmx library interface in use'''

    return float(SystemAttributes['major_version') + 
            0.1*float(SystemAttributes['minor_version')
