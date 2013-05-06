from daqmx import NIDAQmx, Task, AnalogInputVoltage, Volts
from itertools import chain, ifilter

s = NIDAQmx()
print s.version

print 'Devices:'
for d in s.devices:
    print '> Device {}'.format(d.name)
    print '\tInputs  >> {}'.format(d.ai)
    print '\tOutputs >> {}'.format(d.ao)

print 'Channels: {}'.format(s.channels)

print 'Tasks: {}'.format(s.tasks)
a,b,c = (Task(x) for x in 'abc')
print 'Task names: ', a.name, b.name, c.name
print 'Tasks: {}'.format(s.tasks)
print 'Task channels: ', a.channels, b.channels, c.channels
del b, c

print 'Making voltage channel'
# Get all physical input channels
tmp = ifilter(lambda x: len(x)>0, [y.ai for y in s.devices])

ai = []
for i in tmp: ai += i
#print ai 

# use the first one
print a.add_channel(AnalogInputVoltage, ai[0], 0, 10, Volts, name='my_test')
print 'Task {}\'s channels: {}'.format(a.name, a.channels)

