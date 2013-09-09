=======================================================
Pymon: Python module for Xymon(hobbit) external scripts
=======================================================

TODO

Examples
========
Using clientlaunch to write xymon variables
```
import pymon

def main():
    c = pymon.Client()
    # Do you logic...
    c.msg.column = "test"
    c.msg.text = "test message"
    c.msg.color = c.msg.RED_COLOR
    c.send()

if __name__ == "__main__":
    main()
```

Load variables by hand (for run scripts in cron)
```
import pymon
import os
def main():
import os
    os.environ['XYMSRV']='192.168.1.1'
    os.environ['XYMSERVERS']=''
    os.environ['XYMONDPORT']='1984'
    os.environ['XYMONCLIENTLOGS']='/var/log/xymon'
    os.environ['XYMONTMP']='/home/xymon/client/tmp/'
    os.environ['XYMON']='/home/xymon/client/bin/xymon'
    os.environ['MACHINE']='kenny'
    os.environ['SERVEROSTYPE']='Darwin'
    os.environ['XYMONCLIENTHOME']='/home/xymon'
    c = pymon.Client()
    # Do you logic...
    c.msg.column = "test"
    c.msg.text = "test message"
    c.msg.color = c.msg.RED_COLOR
    c.send()

if __name__ == "__main__":
    main()
```

You can change the test duration
```
c.msg.duration = "+30m"
```

You can change the hostname
```
c.msg.machine = "some_other_host"
```
