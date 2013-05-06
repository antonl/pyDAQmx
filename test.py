from daqmx import NIDAQmx, Task

s = NIDAQmx()
print s.version

print 'Devices:'
for d in s.devices:
    i,o = d._get_phys_channel_props()
    print '> Device {}'.format(d.name)
    print '\tInputs  >> {}'.format(i)
    print '\tOutputs >> {}'.format(o)

print 'Channels: {}'.format(s.channels)

print 'Tasks: {}'.format(s.tasks)
a,b,c = (Task(x) for x in 'abc')
print 'Task names: ', a.name, b.name, c.name
print 'Tasks: {}'.format(s.tasks)
print 'Task channels: ', a.channels, b.channels, c.channels
del a, b, c
print 'Tasks: {}'.format(s.tasks)

