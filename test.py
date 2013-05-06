from daqmx import NIDAQmx, Task, AnalogInputVoltage
from daqmx.units import Volts
from itertools import chain, ifilter

s = NIDAQmx()
print s.version

print 'Devices:'
for d in s.devices:
    print '> Device {}'.format(d.name)
    print '\tInputs  >> {}'.format(d.ai)
    print '\tOutputs >> {}'.format(d.ao)

print 'Global channels: {}'.format(s.global_channels)

print 'Tasks: {}'.format(s.tasks)
a,b,c = (Task(x) for x in 'abc')
print 'Task names: ', a.name, b.name, c.name
print 'Tasks: {}'.format(s.tasks)
print 'Task channels: ', a.channels, b.channels, c.channels
del b, c

print 'Making voltage channel'
# Get all physical input channels
ai = s.inputs()
# use the first one
x = a.add_channel(AnalogInputVoltage, ai[0], 0, 10, Volts, name='my_test')
a.add_channel(AnalogInputVoltage, ai[1], 0, 10, Volts, name='my_test2')

print 'Made {}'.format(x)
print 'Task {}\'s channels: {}'.format(a.name, a.channels)

print a.channel_by_name(x.name)



