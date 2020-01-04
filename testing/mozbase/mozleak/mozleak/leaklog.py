import
os
import
re
import
sys
import
mozinfo
import
mozrunner
.
utils
def
_get_default_logger
(
)
:
    
from
mozlog
import
get_default_logger
    
log
=
get_default_logger
(
component
=
'
mozleak
'
)
    
if
not
log
:
        
import
logging
        
log
=
logging
.
getLogger
(
__name__
)
    
return
log
def
expectedTabProcessLeakCounts
(
)
:
    
leaks
=
{
}
    
def
appendExpectedLeakCounts
(
leaks2
)
:
        
for
obj
count
in
leaks2
.
iteritems
(
)
:
            
leaks
[
obj
]
=
leaks
.
get
(
obj
0
)
+
count
    
appendExpectedLeakCounts
(
{
        
'
AsyncTransactionTrackersHolder
'
:
1
        
'
CondVar
'
:
2
        
'
IPC
:
:
Channel
'
:
1
        
'
MessagePump
'
:
1
        
'
Mutex
'
:
2
        
'
PImageBridgeChild
'
:
1
        
'
RefCountedMonitor
'
:
1
        
'
RefCountedTask
'
:
2
        
'
StoreRef
'
:
1
        
'
WaitableEventKernel
'
:
1
        
'
WeakReference
<
MessageListener
>
'
:
1
        
'
base
:
:
Thread
'
:
1
        
'
ipc
:
:
MessageChannel
'
:
1
        
'
nsTArray_base
'
:
7
        
'
nsThread
'
:
1
    
}
)
    
appendExpectedLeakCounts
(
{
        
'
CompositorChild
'
:
1
        
'
CondVar
'
:
1
        
'
IPC
:
:
Channel
'
:
1
        
'
Mutex
'
:
1
        
'
PCompositorChild
'
:
1
        
'
RefCountedMonitor
'
:
1
        
'
RefCountedTask
'
:
2
        
'
StoreRef
'
:
1
        
'
WeakReference
<
MessageListener
>
'
:
1
        
'
ipc
:
:
MessageChannel
'
:
1
        
'
nsTArray_base
'
:
2
    
}
)
    
if
mozinfo
.
isWin
:
        
appendExpectedLeakCounts
(
{
            
'
AsyncTransactionTrackersHolder
'
:
1
            
'
CompositableChild
'
:
1
            
'
Mutex
'
:
1
            
'
PCompositableChild
'
:
1
            
'
PImageContainerChild
'
:
1
            
'
SyncObject
'
:
1
            
'
WeakReference
<
MessageListener
>
'
:
2
        
}
)
        
appendExpectedLeakCounts
(
{
            
'
AsyncTransactionTracker
'
:
1
            
'
AsyncTransactionTrackersHolder
'
:
4
            
'
AsyncTransactionWaiter
'
:
1
            
'
CompositableChild
'
:
3
            
'
CompositableClient
'
:
3
            
'
CondVar
'
:
5
            
'
DXGID3D9TextureData
'
:
1
            
'
FdObj
'
:
2
            
'
GfxTextureWasteTracker
'
:
1
            
'
IPC
:
:
Message
'
:
1
            
'
ITextureClientRecycleAllocator
'
:
1
            
'
LayerTransactionChild
'
:
5
            
'
Mutex
'
:
7
            
'
PCompositableChild
'
:
3
            
'
PImageContainerChild
'
:
3
            
'
PLayerTransactionChild
'
:
5
            
'
PTextureChild
'
:
5
            
'
RemoveTextureFromCompositableTracker
'
:
1
            
'
SharedMemory
'
:
5
            
'
SyncObject
'
:
5
            
'
TextureChild
'
:
5
            
'
TextureClientHolder
'
:
1
            
'
TextureData
'
:
5
            
'
WeakReference
<
MessageListener
>
'
:
10
            
'
nsTArray_base
'
:
17
        
}
)
    
return
leaks
def
process_single_leak_file
(
leakLogFileName
processType
leakThreshold
                             
ignoreMissingLeaks
log
=
None
                             
stackFixer
=
None
)
:
    
"
"
"
Process
a
single
leak
log
.
    
"
"
"
    
lineRe
=
re
.
compile
(
r
"
^
\
s
*
\
d
+
\
|
"
                        
r
"
(
?
P
<
name
>
[
^
|
]
+
)
\
|
"
                        
r
"
\
s
*
(
?
P
<
size
>
-
?
\
d
+
)
\
s
+
(
?
P
<
bytesLeaked
>
-
?
\
d
+
)
\
s
*
\
|
"
                        
r
"
\
s
*
-
?
\
d
+
\
s
+
(
?
P
<
numLeaked
>
-
?
\
d
+
)
"
)
    
log
=
log
or
_get_default_logger
(
)
    
processString
=
"
%
s
process
:
"
%
processType
    
expectedLeaks
=
expectedTabProcessLeakCounts
(
)
if
processType
=
=
'
tab
'
else
{
}
    
crashedOnPurpose
=
False
    
totalBytesLeaked
=
None
    
logAsWarning
=
False
    
leakAnalysis
=
[
]
    
leakedObjectAnalysis
=
[
]
    
leakedObjectNames
=
[
]
    
recordLeakedObjects
=
False
    
with
open
(
leakLogFileName
"
r
"
)
as
leaks
:
        
for
line
in
leaks
:
            
if
line
.
find
(
"
purposefully
crash
"
)
>
-
1
:
                
crashedOnPurpose
=
True
            
matches
=
lineRe
.
match
(
line
)
            
if
not
matches
:
                
strippedLine
=
line
.
rstrip
(
)
                
log
.
info
(
stackFixer
(
strippedLine
)
if
stackFixer
else
strippedLine
)
                
continue
            
name
=
matches
.
group
(
"
name
"
)
.
rstrip
(
)
            
size
=
int
(
matches
.
group
(
"
size
"
)
)
            
bytesLeaked
=
int
(
matches
.
group
(
"
bytesLeaked
"
)
)
            
numLeaked
=
int
(
matches
.
group
(
"
numLeaked
"
)
)
            
if
numLeaked
!
=
0
or
name
=
=
"
TOTAL
"
:
                
log
.
info
(
line
.
rstrip
(
)
)
            
if
name
=
=
"
TOTAL
"
:
                
if
totalBytesLeaked
!
=
None
:
                    
leakAnalysis
.
append
(
"
WARNING
|
leakcheck
|
%
s
multiple
BloatView
byte
totals
found
"
                                        
%
processString
)
                
else
:
                    
totalBytesLeaked
=
0
                
if
bytesLeaked
>
totalBytesLeaked
:
                    
totalBytesLeaked
=
bytesLeaked
                    
leakedObjectNames
=
[
]
                    
leakedObjectAnalysis
=
[
]
                    
recordLeakedObjects
=
True
                
else
:
                    
recordLeakedObjects
=
False
            
if
size
<
0
or
bytesLeaked
<
0
or
numLeaked
<
0
:
                
leakAnalysis
.
append
(
"
TEST
-
UNEXPECTED
-
FAIL
|
leakcheck
|
%
s
negative
leaks
caught
!
"
                                    
%
processString
)
                
logAsWarning
=
True
                
continue
            
if
name
!
=
"
TOTAL
"
and
numLeaked
!
=
0
and
recordLeakedObjects
:
                
currExpectedLeak
=
expectedLeaks
.
get
(
name
0
)
                
if
not
expectedLeaks
or
numLeaked
<
=
currExpectedLeak
:
                    
if
not
expectedLeaks
:
                        
leakedObjectNames
.
append
(
name
)
                    
leakedObjectAnalysis
.
append
(
"
TEST
-
INFO
|
leakcheck
|
%
s
leaked
%
d
%
s
"
                                                
%
(
processString
numLeaked
name
)
)
                
else
:
                    
leakedObjectNames
.
append
(
name
)
                    
leakedObjectAnalysis
.
append
(
"
WARNING
|
leakcheck
|
%
s
leaked
too
many
%
s
(
expected
%
d
got
%
d
)
"
                                                
%
(
processString
name
currExpectedLeak
numLeaked
)
)
    
leakAnalysis
.
extend
(
leakedObjectAnalysis
)
    
if
logAsWarning
:
        
log
.
warning
(
'
\
n
'
.
join
(
leakAnalysis
)
)
    
else
:
        
log
.
info
(
'
\
n
'
.
join
(
leakAnalysis
)
)
    
logAsWarning
=
False
    
if
totalBytesLeaked
is
None
:
        
if
crashedOnPurpose
:
            
log
.
info
(
"
TEST
-
INFO
|
leakcheck
|
%
s
deliberate
crash
and
thus
no
leak
log
"
                     
%
processString
)
        
elif
ignoreMissingLeaks
:
            
log
.
info
(
"
TEST
-
INFO
|
leakcheck
|
%
s
ignoring
missing
output
line
for
total
leaks
"
                     
%
processString
)
        
else
:
            
log
.
info
(
"
TEST
-
UNEXPECTED
-
FAIL
|
leakcheck
|
%
s
missing
output
line
for
total
leaks
!
"
                     
%
processString
)
            
log
.
info
(
"
TEST
-
INFO
|
leakcheck
|
missing
output
line
from
log
file
%
s
"
                     
%
leakLogFileName
)
        
return
    
if
totalBytesLeaked
=
=
0
:
        
log
.
info
(
"
TEST
-
PASS
|
leakcheck
|
%
s
no
leaks
detected
!
"
%
                 
processString
)
        
return
    
if
totalBytesLeaked
>
leakThreshold
or
(
expectedLeaks
and
leakedObjectNames
)
:
        
logAsWarning
=
True
        
prefix
=
"
TEST
-
UNEXPECTED
-
FAIL
"
    
else
:
        
prefix
=
"
WARNING
"
    
maxSummaryObjects
=
5
    
leakedObjectSummary
=
'
'
.
join
(
leakedObjectNames
[
:
maxSummaryObjects
]
)
    
if
len
(
leakedObjectNames
)
>
maxSummaryObjects
:
        
leakedObjectSummary
+
=
'
.
.
.
'
    
if
logAsWarning
:
        
log
.
warning
(
"
%
s
|
leakcheck
|
%
s
%
d
bytes
leaked
(
%
s
)
"
                    
%
(
prefix
processString
totalBytesLeaked
leakedObjectSummary
)
)
    
else
:
        
log
.
info
(
"
%
s
|
leakcheck
|
%
s
%
d
bytes
leaked
(
%
s
)
"
                 
%
(
prefix
processString
totalBytesLeaked
leakedObjectSummary
)
)
def
process_leak_log
(
leak_log_file
leak_thresholds
=
None
                     
ignore_missing_leaks
=
None
log
=
None
                     
stack_fixer
=
None
)
:
    
"
"
"
Process
the
leak
log
including
separate
leak
logs
created
    
by
child
processes
.
    
Use
this
function
if
you
want
an
additional
PASS
/
FAIL
summary
.
    
It
must
be
used
with
the
|
XPCOM_MEM_BLOAT_LOG
|
environment
variable
.
    
The
base
of
leak_log_file
for
a
non
-
default
process
needs
to
end
with
      
_proctype_pid12345
.
log
    
"
proctype
"
is
a
string
denoting
the
type
of
the
process
which
should
    
be
the
result
of
calling
XRE_ChildProcessTypeToString
(
)
.
12345
is
    
a
series
of
digits
that
is
the
pid
for
the
process
.
The
.
log
is
    
optional
.
    
All
other
file
names
are
treated
as
being
for
default
processes
.
    
leak_thresholds
should
be
a
dict
mapping
process
types
to
leak
thresholds
    
in
bytes
.
If
a
process
type
is
not
present
in
the
dict
the
threshold
    
will
be
0
.
    
ignore_missing_leaks
should
be
a
list
of
process
types
.
If
a
process
    
creates
a
leak
log
without
a
TOTAL
then
we
report
an
error
if
it
isn
'
t
    
in
the
list
ignore_missing_leaks
.
    
"
"
"
    
log
=
log
or
_get_default_logger
(
)
    
leakLogFile
=
leak_log_file
    
if
not
os
.
path
.
exists
(
leakLogFile
)
:
        
log
.
info
(
            
"
WARNING
|
leakcheck
|
refcount
logging
is
off
so
leaks
can
'
t
be
detected
!
"
)
        
return
    
leakThresholds
=
leak_thresholds
or
{
}
    
ignoreMissingLeaks
=
ignore_missing_leaks
or
[
]
    
knownProcessTypes
=
[
"
default
"
"
plugin
"
"
tab
"
"
geckomediaplugin
"
]
    
for
processType
in
knownProcessTypes
:
        
log
.
info
(
"
TEST
-
INFO
|
leakcheck
|
%
s
process
:
leak
threshold
set
at
%
d
bytes
"
                 
%
(
processType
leakThresholds
.
get
(
processType
0
)
)
)
    
for
processType
in
leakThresholds
:
        
if
not
processType
in
knownProcessTypes
:
            
log
.
info
(
"
TEST
-
UNEXPECTED
-
FAIL
|
leakcheck
|
Unknown
process
type
%
s
in
leakThresholds
"
                     
%
processType
)
    
(
leakLogFileDir
leakFileBase
)
=
os
.
path
.
split
(
leakLogFile
)
    
if
leakFileBase
[
-
4
:
]
=
=
"
.
log
"
:
        
leakFileBase
=
leakFileBase
[
:
-
4
]
        
fileNameRegExp
=
re
.
compile
(
r
"
_
(
[
a
-
z
]
*
)
_pid
\
d
*
.
log
"
)
    
else
:
        
fileNameRegExp
=
re
.
compile
(
r
"
_
(
[
a
-
z
]
*
)
_pid
\
d
*
"
)
    
for
fileName
in
os
.
listdir
(
leakLogFileDir
)
:
        
if
fileName
.
find
(
leakFileBase
)
!
=
-
1
:
            
thisFile
=
os
.
path
.
join
(
leakLogFileDir
fileName
)
            
m
=
fileNameRegExp
.
search
(
fileName
)
            
if
m
:
                
processType
=
m
.
group
(
1
)
            
else
:
                
processType
=
"
default
"
            
if
not
processType
in
knownProcessTypes
:
                
log
.
info
(
"
TEST
-
UNEXPECTED
-
FAIL
|
leakcheck
|
Leak
log
with
unknown
process
type
%
s
"
                         
%
processType
)
            
leakThreshold
=
leakThresholds
.
get
(
processType
0
)
            
process_single_leak_file
(
thisFile
processType
leakThreshold
                                     
processType
in
ignoreMissingLeaks
                                     
log
=
log
stackFixer
=
stack_fixer
)
