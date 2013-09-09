=======================================================
Pymon: Python module for Xymon(hobbit) external scripts
=======================================================

Pymon it's a module to write xymon(Hobbit) external scripts and send it to a xymon server.
It uses the xymon binary to send the information. But it also works in a native mode if you don't have the xymon client installed.
Its very easy to use, because it read most of the information needed from the xymon environment variables.

Installation
========
```
git clone https://github.com/aenima-x/Pymon.git
cd Pymon
python setup.py install
```

Examples
========
Using clientlaunch to write xymon variables
```
import pymon

def main():
    c = pymon.Client("column_name")
    # Do your logic...
    c.logFile.write("write some log\n")
    c.tmpFile.write("write some temp stuff\n")
    c.msg.color = c.msg.GREEN_COLOR
    c.msg.text = "test message"
    c.send()

if __name__ == "__main__":
    main()
```

Load variables by hand (for run scripts in cron)
```
import pymon
import os
def main():
    os.environ['XYMSRV']='127.0.0.1'
    os.environ['XYMSERVERS']=''
    os.environ['XYMONDPORT']='1984'
    os.environ['XYMONCLIENTLOGS']='/home/xymon/client/logs'
    os.environ['XYMONTMP']='/home/xymon/client/tmp/'
    os.environ['XYMON']='/home/xymon/client/bin/xymon'
    os.environ['MACHINE']='ubuntu'
    os.environ['SERVEROSTYPE']='linux'
    os.environ['XYMONCLIENTHOME']='/home/xymon'
    c = pymon.Client("column_name")
    # Do your logic...
    c.logFile.write("write some log\n")
    c.tmpFile.write("write some temp stuff\n")
    c.msg.text = "test message"
    c.msg.color = c.msg.RED_COLOR
    c.send()

if __name__ == "__main__":
    main()
```

Even if you don't have the client installed, you can use pymon in native mode.
And send the message anyway.
In this mode, you don't need all the variables. Just some of them.

```
import pymon
import os
def main():
    os.environ['XYMSRV']='127.0.0.1'
    os.environ['XYMSERVERS']=''
    os.environ['XYMONDPORT']='1984'
    os.environ['XYMONCLIENTLOGS']='/tmp'
    os.environ['XYMONTMP']='/tmp'
    os.environ['MACHINE']='ubuntu'
    c = pymon.Client("column_name", useXymon=False)
    c.logFile.write("write some log\n")
    c.tmpFile.write("write some temp stuff\n")
    c.msg.text = "python message"
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
