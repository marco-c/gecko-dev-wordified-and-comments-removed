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
ADBTimeoutError
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
    
def
__init__
(
self
device
appName
=
'
'
remoteProfile
=
None
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
_device
=
device
        
self
.
_appName
=
appName
        
self
.
_remoteProfile
=
remoteProfile
        
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
_device
.
get_top_activity
(
timeout
=
60
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
(
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
)
            
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
(
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
)
            
else
:
                
print
(
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
)
        
if
status
=
=
2
:
            
print
(
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
"
                  
"
seconds
with
no
output
"
                  
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
_device
.
shell_output
(
'
echo
>
%
s
'
%
traces
root
=
True
)
            
self
.
_device
.
shell_output
(
'
chmod
666
%
s
'
%
traces
root
=
True
)
        
except
Exception
as
e
:
            
print
(
"
Error
deleting
%
s
:
%
s
"
%
(
traces
str
(
e
)
)
)
    
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
_device
.
is_file
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
_device
.
get_file
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
(
"
Contents
of
%
s
:
"
%
traces
)
                        
print
(
t
)
                
self
.
deleteANRs
(
)
            
except
Exception
as
e
:
                
print
(
"
Error
pulling
%
s
:
%
s
"
%
(
traces
str
(
e
)
)
)
        
else
:
            
print
(
"
%
s
not
found
"
%
traces
)
    
def
deleteTombstones
(
self
)
:
        
self
.
_device
.
rm
(
"
/
data
/
tombstones
"
force
=
True
                        
recursive
=
True
root
=
True
)
    
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
_device
.
is_dir
(
remoteDir
)
:
                
self
.
_device
.
chmod
(
remoteDir
recursive
=
True
root
=
True
)
                
self
.
_device
.
pull
(
remoteDir
uploadDir
)
                
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
(
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
)
        
else
:
            
print
(
"
MOZ_UPLOAD_DIR
not
defined
;
tombstone
check
skipped
"
)
    
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
_device
.
get_logcat
(
            
filter_out_regexps
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
_device
.
is_dir
(
remoteCrashDir
)
:
                
print
(
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
)
                
return
True
            
self
.
_device
.
pull
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
Exception
as
e
:
                
print
(
"
WARNING
:
unable
to
remove
directory
%
s
:
%
s
"
%
(
                    
dumpDir
str
(
e
)
)
)
        
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
Exception
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
_device
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
        
def
__init__
(
self
device
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
device
=
device
            
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
messageLogger
=
messageLogger
            
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
            
self
.
stdoutlen
=
0
            
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
cmd
[
0
]
=
=
'
am
'
:
                
cmd
=
'
'
.
join
(
cmd
)
                
self
.
procName
=
app
                
if
not
self
.
device
.
shell_bool
(
cmd
)
:
                    
print
(
"
remote_automation
.
py
failed
to
launch
%
s
"
%
cmd
)
            
else
:
                
args
=
cmd
                
if
args
[
0
]
=
=
app
:
                    
args
=
args
[
1
:
]
                
url
=
args
[
-
1
:
]
[
0
]
                
if
url
.
startswith
(
'
/
'
)
:
                    
url
=
None
                
else
:
                    
args
=
args
[
:
-
1
]
                
if
'
geckoview
'
in
app
:
                    
activity
=
"
TestRunnerActivity
"
                    
self
.
device
.
launch_activity
(
app
activity
e10s
=
True
moz_env
=
env
                                                
extra_args
=
args
url
=
url
)
                
else
:
                    
self
.
device
.
launch_fennec
(
                        
app
moz_env
=
env
extra_args
=
args
url
=
url
)
            
self
.
timeout
=
6600
            
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
            
procs
=
self
.
device
.
get_process_list
(
)
            
pids
=
[
proc
[
0
]
for
proc
in
procs
if
proc
[
1
]
=
=
self
.
procName
[
:
75
]
]
            
if
pids
is
None
or
len
(
pids
)
<
1
:
                
return
0
            
return
pids
[
0
]
        
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
log
any
new
content
and
return
True
if
new
            
content
processed
.
            
"
"
"
            
if
not
self
.
device
.
is_file
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
device
.
get_file
(
                    
self
.
proc
offset
=
self
.
stdoutlen
)
            
except
ADBTimeoutError
:
                
raise
            
except
Exception
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
(
newLogContent
)
                
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
ADBTimeoutError
:
                                    
raise
                                
except
Exception
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
is
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
top
=
=
self
.
procName
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
device
.
get_top_activity
(
timeout
=
60
)
                    
if
top
is
None
:
                        
print
(
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
)
                        
top
=
self
.
device
.
get_top_activity
(
timeout
=
60
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
                
try
:
                    
self
.
device
.
pkill
(
self
.
procName
sig
=
3
attempts
=
1
)
                
except
ADBTimeoutError
:
                    
raise
                
except
:
                    
pass
                
time
.
sleep
(
3
)
                
try
:
                    
self
.
device
.
pkill
(
self
.
procName
sig
=
6
attempts
=
1
)
                
except
ADBTimeoutError
:
                    
raise
                
except
:
                    
pass
                
retries
=
0
                
while
retries
<
3
:
                    
if
self
.
device
.
process_exist
(
self
.
procName
)
:
                        
print
(
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
)
                        
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
                
try
:
                    
self
.
device
.
pkill
(
self
.
procName
sig
=
9
attempts
=
1
)
                
except
ADBTimeoutError
:
                    
raise
                
except
:
                    
print
(
"
%
s
still
alive
after
SIGKILL
!
"
%
self
.
procName
)
                
if
self
.
device
.
process_exist
(
self
.
procName
)
:
                    
self
.
device
.
stop_application
(
self
.
procName
)
            
else
:
                
self
.
device
.
stop_application
(
self
.
procName
)
