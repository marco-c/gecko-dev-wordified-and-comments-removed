import
datetime
import
glob
import
time
import
re
import
os
import
posixpath
import
tempfile
import
shutil
import
sys
from
automation
import
Automation
from
mozdevice
import
DMError
DeviceManager
from
mozlog
import
get_default_logger
from
mozscreenshot
import
dump_screen
import
mozcrash
fennecLogcatFilters
=
[
"
The
character
encoding
of
the
HTML
document
was
not
declared
"
                        
"
Use
of
Mutation
Events
is
deprecated
.
Use
MutationObserver
instead
.
"
                        
"
Unexpected
value
from
nativeGetEnabledTags
:
0
"
]
class
RemoteAutomation
(
Automation
)
:
    
_devicemanager
=
None
    
def
__init__
(
self
deviceManager
appName
=
'
'
remoteLog
=
None
                 
processArgs
=
None
)
:
        
self
.
_dm
=
deviceManager
        
self
.
_appName
=
appName
        
self
.
_remoteProfile
=
None
        
self
.
_remoteLog
=
remoteLog
        
self
.
_processArgs
=
processArgs
or
{
}
;
        
self
.
lastTestSeen
=
"
remoteautomation
.
py
"
        
Automation
.
__init__
(
self
)
    
def
setDeviceManager
(
self
deviceManager
)
:
        
self
.
_dm
=
deviceManager
    
def
setAppName
(
self
appName
)
:
        
self
.
_appName
=
appName
    
def
setRemoteProfile
(
self
remoteProfile
)
:
        
self
.
_remoteProfile
=
remoteProfile
    
def
setRemoteLog
(
self
logfile
)
:
        
self
.
_remoteLog
=
logfile
    
def
environment
(
self
env
=
None
xrePath
=
None
crashreporter
=
True
debugger
=
False
lsanPath
=
None
ubsanPath
=
None
)
:
        
if
env
is
None
:
            
env
=
{
}
        
if
'
MOZ_HIDE_RESULTS_TABLE
'
in
os
.
environ
:
            
env
[
'
MOZ_HIDE_RESULTS_TABLE
'
]
=
os
.
environ
[
'
MOZ_HIDE_RESULTS_TABLE
'
]
        
if
crashreporter
and
not
debugger
:
            
env
[
'
MOZ_CRASHREPORTER_NO_REPORT
'
]
=
'
1
'
            
env
[
'
MOZ_CRASHREPORTER
'
]
=
'
1
'
            
env
[
'
MOZ_CRASHREPORTER_SHUTDOWN
'
]
=
'
1
'
        
else
:
            
env
[
'
MOZ_CRASHREPORTER_DISABLE
'
]
=
'
1
'
        
env
.
setdefault
(
'
MOZ_DISABLE_NONLOCAL_CONNECTIONS
'
'
1
'
)
        
env
.
setdefault
(
'
MOZ_IN_AUTOMATION
'
'
1
'
)
        
env
.
setdefault
(
'
R_LOG_LEVEL
'
'
6
'
)
        
env
.
setdefault
(
'
R_LOG_DESTINATION
'
'
stderr
'
)
        
env
.
setdefault
(
'
R_LOG_VERBOSE
'
'
1
'
)
        
return
env
    
def
waitForFinish
(
self
proc
utilityPath
timeout
maxTime
startTime
debuggerInfo
symbolsPath
outputHandler
=
None
)
:
        
"
"
"
Wait
for
tests
to
finish
.
            
If
maxTime
seconds
elapse
or
no
output
is
detected
for
timeout
            
seconds
kill
the
process
and
fail
the
test
.
        
"
"
"
        
proc
.
utilityPath
=
utilityPath
        
status
=
proc
.
wait
(
timeout
=
maxTime
noOutputTimeout
=
timeout
)
        
self
.
lastTestSeen
=
proc
.
getLastTestSeen
        
topActivity
=
self
.
_dm
.
getTopActivity
(
)
        
if
topActivity
=
=
proc
.
procName
:
            
print
"
Browser
unexpectedly
found
running
.
Killing
.
.
.
"
            
proc
.
kill
(
True
)
        
if
status
=
=
1
:
            
if
maxTime
:
                
print
"
TEST
-
UNEXPECTED
-
FAIL
|
%
s
|
application
ran
for
longer
than
"
\
                      
"
allowed
maximum
time
of
%
s
seconds
"
%
(
self
.
lastTestSeen
maxTime
)
            
else
:
                
print
"
TEST
-
UNEXPECTED
-
FAIL
|
%
s
|
application
ran
for
longer
than
"
\
                      
"
allowed
maximum
time
"
%
(
self
.
lastTestSeen
)
        
if
status
=
=
2
:
            
print
"
TEST
-
UNEXPECTED
-
FAIL
|
%
s
|
application
timed
out
after
%
d
seconds
with
no
output
"
\
                
%
(
self
.
lastTestSeen
int
(
timeout
)
)
        
return
status
    
def
deleteANRs
(
self
)
:
        
traces
=
"
/
data
/
anr
/
traces
.
txt
"
        
try
:
            
self
.
_dm
.
shellCheckOutput
(
[
'
echo
'
'
'
'
>
'
traces
]
root
=
True
                                       
timeout
=
DeviceManager
.
short_timeout
)
            
self
.
_dm
.
shellCheckOutput
(
[
'
chmod
'
'
666
'
traces
]
root
=
True
                                       
timeout
=
DeviceManager
.
short_timeout
)
        
except
DMError
:
            
print
"
Error
deleting
%
s
"
%
traces
            
pass
    
def
checkForANRs
(
self
)
:
        
traces
=
"
/
data
/
anr
/
traces
.
txt
"
        
if
self
.
_dm
.
fileExists
(
traces
)
:
            
try
:
                
t
=
self
.
_dm
.
pullFile
(
traces
)
                
if
t
:
                    
stripped
=
t
.
strip
(
)
                    
if
len
(
stripped
)
>
0
:
                        
print
"
Contents
of
%
s
:
"
%
traces
                        
print
t
                
self
.
deleteANRs
(
)
            
except
DMError
:
                
print
"
Error
pulling
%
s
"
%
traces
            
except
IOError
:
                
print
"
Error
pulling
%
s
"
%
traces
        
else
:
            
print
"
%
s
not
found
"
%
traces
    
def
deleteTombstones
(
self
)
:
        
tombstones
=
"
/
data
/
tombstones
/
*
"
        
try
:
            
self
.
_dm
.
shellCheckOutput
(
[
'
rm
'
'
-
r
'
tombstones
]
root
=
True
                                       
timeout
=
DeviceManager
.
short_timeout
)
        
except
DMError
:
            
pass
    
def
checkForTombstones
(
self
)
:
        
remoteDir
=
"
/
data
/
tombstones
"
        
uploadDir
=
os
.
environ
.
get
(
'
MOZ_UPLOAD_DIR
'
None
)
        
if
uploadDir
:
            
if
not
os
.
path
.
exists
(
uploadDir
)
:
                
os
.
mkdir
(
uploadDir
)
            
if
self
.
_dm
.
dirExists
(
remoteDir
)
:
                
try
:
                    
self
.
_dm
.
shellCheckOutput
(
[
'
chmod
'
'
777
'
remoteDir
]
root
=
True
                                               
timeout
=
DeviceManager
.
short_timeout
)
                    
self
.
_dm
.
shellCheckOutput
(
[
'
chmod
'
'
666
'
os
.
path
.
join
(
remoteDir
'
*
'
)
]
                                               
root
=
True
timeout
=
DeviceManager
.
short_timeout
)
                    
self
.
_dm
.
getDirectory
(
remoteDir
uploadDir
False
)
                
except
DMError
:
                    
pass
                
self
.
deleteTombstones
(
)
                
for
f
in
glob
.
glob
(
os
.
path
.
join
(
uploadDir
"
tombstone_
?
?
"
)
)
:
                    
for
i
in
xrange
(
1
sys
.
maxint
)
:
                        
newname
=
"
%
s
.
%
d
.
txt
"
%
(
f
i
)
                        
if
not
os
.
path
.
exists
(
newname
)
:
                            
os
.
rename
(
f
newname
)
                            
break
            
else
:
                
print
"
%
s
does
not
exist
;
tombstone
check
skipped
"
%
remoteDir
        
else
:
            
print
"
MOZ_UPLOAD_DIR
not
defined
;
tombstone
check
skipped
"
    
def
checkForCrashes
(
self
directory
symbolsPath
)
:
        
self
.
checkForANRs
(
)
        
self
.
checkForTombstones
(
)
        
logcat
=
self
.
_dm
.
getLogcat
(
filterOutRegexps
=
fennecLogcatFilters
)
        
javaException
=
mozcrash
.
check_for_java_exception
(
logcat
test_name
=
self
.
lastTestSeen
)
        
if
javaException
:
            
return
True
        
if
not
self
.
CRASHREPORTER
:
            
return
False
        
try
:
            
dumpDir
=
tempfile
.
mkdtemp
(
)
            
remoteCrashDir
=
posixpath
.
join
(
self
.
_remoteProfile
'
minidumps
'
)
            
if
not
self
.
_dm
.
dirExists
(
remoteCrashDir
)
:
                
print
"
Automation
Error
:
No
crash
directory
(
%
s
)
found
on
remote
device
"
%
remoteCrashDir
                
return
True
            
self
.
_dm
.
getDirectory
(
remoteCrashDir
dumpDir
)
            
logger
=
get_default_logger
(
)
            
crashed
=
mozcrash
.
log_crashes
(
logger
dumpDir
symbolsPath
test
=
self
.
lastTestSeen
)
        
finally
:
            
try
:
                
shutil
.
rmtree
(
dumpDir
)
            
except
:
                
print
"
WARNING
:
unable
to
remove
directory
:
%
s
"
%
dumpDir
        
return
crashed
    
def
buildCommandLine
(
self
app
debuggerInfo
profileDir
testURL
extraArgs
)
:
        
if
self
.
_remoteProfile
:
            
profileDir
=
self
.
_remoteProfile
        
if
app
=
=
"
am
"
and
extraArgs
[
0
]
in
(
'
instrument
'
'
start
'
)
:
            
return
app
extraArgs
        
cmd
args
=
Automation
.
buildCommandLine
(
self
app
debuggerInfo
profileDir
testURL
extraArgs
)
        
try
:
            
args
.
remove
(
'
-
foreground
'
)
        
except
:
            
pass
        
return
app
args
    
def
Process
(
self
cmd
stdout
=
None
stderr
=
None
env
=
None
cwd
=
None
)
:
        
return
self
.
RProcess
(
self
.
_dm
cmd
self
.
_remoteLog
env
cwd
self
.
_appName
                             
*
*
self
.
_processArgs
)
    
class
RProcess
(
object
)
:
        
dm
=
None
        
def
__init__
(
self
dm
cmd
stdout
=
None
env
=
None
cwd
=
None
app
=
None
                     
messageLogger
=
None
counts
=
None
)
:
            
self
.
dm
=
dm
            
self
.
stdoutlen
=
0
            
self
.
lastTestSeen
=
"
remoteautomation
.
py
"
            
self
.
proc
=
dm
.
launchProcess
(
cmd
stdout
cwd
env
True
)
            
self
.
messageLogger
=
messageLogger
            
self
.
utilityPath
=
None
            
self
.
counts
=
counts
            
if
self
.
counts
is
not
None
:
                
self
.
counts
[
'
pass
'
]
=
0
                
self
.
counts
[
'
fail
'
]
=
0
                
self
.
counts
[
'
todo
'
]
=
0
            
if
self
.
proc
is
None
:
                
self
.
proc
=
stdout
            
self
.
procName
=
cmd
[
0
]
.
split
(
posixpath
.
sep
)
[
-
1
]
            
if
cmd
[
0
]
=
=
'
am
'
and
cmd
[
1
]
in
(
'
instrument
'
'
start
'
)
:
                
self
.
procName
=
app
            
self
.
timeout
=
5400
            
self
.
logBuffer
=
"
"
        
property
        
def
pid
(
self
)
:
            
pid
=
self
.
dm
.
processExist
(
self
.
procName
)
            
if
pid
is
None
:
                
return
0
            
return
pid
        
def
read_stdout
(
self
)
:
            
"
"
"
            
Fetch
the
full
remote
log
file
using
devicemanager
process
them
and
            
return
whether
there
were
any
new
log
entries
since
the
last
call
.
            
"
"
"
            
if
not
self
.
dm
.
fileExists
(
self
.
proc
)
:
                
return
False
            
try
:
                
newLogContent
=
self
.
dm
.
pullFile
(
self
.
proc
self
.
stdoutlen
)
            
except
DMError
:
                
return
False
            
if
not
newLogContent
:
                
return
False
            
self
.
stdoutlen
+
=
len
(
newLogContent
)
            
if
self
.
messageLogger
is
None
:
                
testStartFilenames
=
re
.
findall
(
r
"
TEST
-
START
\
|
(
[
^
\
s
]
*
)
"
newLogContent
)
                
if
testStartFilenames
:
                    
self
.
lastTestSeen
=
testStartFilenames
[
-
1
]
                
print
newLogContent
                
return
True
            
self
.
logBuffer
+
=
newLogContent
            
lines
=
self
.
logBuffer
.
split
(
'
\
n
'
)
            
lines
=
[
l
for
l
in
lines
if
l
]
            
if
lines
:
                
if
self
.
logBuffer
.
endswith
(
'
\
n
'
)
:
                    
self
.
logBuffer
=
"
"
                
else
:
                    
self
.
logBuffer
=
lines
[
-
1
]
                    
del
lines
[
-
1
]
            
if
not
lines
:
                
return
False
            
for
line
in
lines
:
                
parsed_messages
=
self
.
messageLogger
.
write
(
line
)
                
for
message
in
parsed_messages
:
                    
if
isinstance
(
message
dict
)
and
message
.
get
(
'
action
'
)
=
=
'
test_start
'
:
                        
self
.
lastTestSeen
=
message
[
'
test
'
]
                    
if
isinstance
(
message
dict
)
and
message
.
get
(
'
action
'
)
=
=
'
log
'
:
                        
line
=
message
[
'
message
'
]
.
strip
(
)
                        
if
self
.
counts
:
                            
m
=
re
.
match
(
"
.
*
:
\
s
*
(
\
d
*
)
"
line
)
                            
if
m
:
                                
try
:
                                    
val
=
int
(
m
.
group
(
1
)
)
                                    
if
"
Passed
:
"
in
line
:
                                        
self
.
counts
[
'
pass
'
]
+
=
val
                                    
elif
"
Failed
:
"
in
line
:
                                        
self
.
counts
[
'
fail
'
]
+
=
val
                                    
elif
"
Todo
:
"
in
line
:
                                        
self
.
counts
[
'
todo
'
]
+
=
val
                                
except
:
                                    
pass
            
return
True
        
property
        
def
getLastTestSeen
(
self
)
:
            
return
self
.
lastTestSeen
        
def
wait
(
self
timeout
=
None
noOutputTimeout
=
None
)
:
            
timer
=
0
            
noOutputTimer
=
0
            
interval
=
10
            
if
timeout
=
=
None
:
                
timeout
=
self
.
timeout
            
status
=
0
            
top
=
self
.
procName
            
slowLog
=
False
            
endTime
=
datetime
.
datetime
.
now
(
)
+
datetime
.
timedelta
(
seconds
=
timeout
)
            
while
(
top
=
=
self
.
procName
)
:
                
hasOutput
=
False
                
if
(
not
slowLog
)
or
(
timer
%
60
=
=
0
)
:
                    
startRead
=
datetime
.
datetime
.
now
(
)
                    
hasOutput
=
self
.
read_stdout
(
)
                    
if
(
datetime
.
datetime
.
now
(
)
-
startRead
)
>
datetime
.
timedelta
(
seconds
=
5
)
:
                        
slowLog
=
True
                    
if
hasOutput
:
                        
noOutputTimer
=
0
                    
if
self
.
counts
and
'
pass
'
in
self
.
counts
and
self
.
counts
[
'
pass
'
]
>
0
:
                        
interval
=
0
.
5
                
time
.
sleep
(
interval
)
                
timer
+
=
interval
                
noOutputTimer
+
=
interval
                
if
datetime
.
datetime
.
now
(
)
>
endTime
:
                    
status
=
1
                    
break
                
if
(
noOutputTimeout
and
noOutputTimer
>
noOutputTimeout
)
:
                    
status
=
2
                    
break
                
if
not
hasOutput
:
                    
top
=
self
.
dm
.
getTopActivity
(
)
                    
if
top
=
=
"
"
:
                        
print
"
Failed
to
get
top
activity
retrying
once
.
.
.
"
                        
top
=
self
.
dm
.
getTopActivity
(
)
            
self
.
read_stdout
(
)
            
return
status
        
def
kill
(
self
stagedShutdown
=
False
)
:
            
if
self
.
utilityPath
:
                
dump_screen
(
self
.
utilityPath
get_default_logger
(
)
)
            
if
stagedShutdown
:
                
self
.
dm
.
killProcess
(
self
.
procName
3
)
                
time
.
sleep
(
3
)
                
self
.
dm
.
killProcess
(
self
.
procName
6
)
                
retries
=
0
                
while
retries
<
3
:
                    
pid
=
self
.
dm
.
processExist
(
self
.
procName
)
                    
if
pid
and
pid
>
0
:
                        
print
"
%
s
still
alive
after
SIGABRT
:
waiting
.
.
.
"
%
self
.
procName
                        
time
.
sleep
(
5
)
                    
else
:
                        
return
                    
retries
+
=
1
                
self
.
dm
.
killProcess
(
self
.
procName
9
)
                
pid
=
self
.
dm
.
processExist
(
self
.
procName
)
                
if
pid
and
pid
>
0
:
                    
self
.
dm
.
killProcess
(
self
.
procName
)
            
else
:
                
self
.
dm
.
killProcess
(
self
.
procName
)
