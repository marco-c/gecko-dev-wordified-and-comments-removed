from
__future__
import
absolute_import
import
struct
from
ctypes
import
byref
create_string_buffer
memmove
Union
c_double
\
    
c_longlong
from
ctypes
import
windll
from
ctypes
.
wintypes
import
DWORD
HANDLE
LPSTR
LPCSTR
LPCWSTR
Structure
\
    
pointer
LONG
from
cmanager_base
import
CounterManager
from
utils
import
TalosError
pdh
=
windll
.
pdh
_LONGLONG
=
c_longlong
class
_PDH_COUNTER_PATH_ELEMENTS_A
(
Structure
)
:
    
_fields_
=
[
(
"
szMachineName
"
LPSTR
)
                
(
"
szObjectName
"
LPSTR
)
                
(
"
szInstanceName
"
LPSTR
)
                
(
"
szParentInstance
"
LPSTR
)
                
(
"
dwInstanceIndex
"
DWORD
)
                
(
"
szCounterName
"
LPSTR
)
]
_PDH_MORE_DATA
=
-
2147481646
def
_getExpandedCounterPaths
(
processName
counterName
)
:
    
'
'
'
    
Get
list
of
expanded
counter
paths
given
a
counter
name
.
Returns
a
    
list
of
strings
or
None
if
no
counter
paths
can
be
created
    
'
'
'
    
pcchPathListLength
=
DWORD
(
0
)
    
szWildCardPath
=
LPSTR
(
'
\
\
process
(
%
s
)
\
\
%
s
'
%
(
processName
counterName
)
)
    
if
pdh
.
PdhExpandCounterPathA
(
        
szWildCardPath
        
LPSTR
(
None
)
        
pointer
(
pcchPathListLength
)
    
)
!
=
_PDH_MORE_DATA
:
        
return
[
]
    
pathListLength
=
pcchPathListLength
.
value
    
szExpandedPathList
=
LPCSTR
(
'
\
0
'
*
pathListLength
)
    
if
pdh
.
PdhExpandCounterPathA
(
szWildCardPath
szExpandedPathList
                                 
pointer
(
pcchPathListLength
)
)
!
=
0
:
        
return
[
]
    
buffer
=
create_string_buffer
(
pcchPathListLength
.
value
)
    
memmove
(
buffer
szExpandedPathList
pcchPathListLength
.
value
)
    
paths
=
[
]
    
i
=
0
    
path
=
'
'
    
for
j
in
range
(
0
pcchPathListLength
.
value
)
:
        
c
=
struct
.
unpack_from
(
'
c
'
buffer
offset
=
j
)
[
0
]
        
if
c
=
=
'
\
0
'
:
            
if
j
=
=
i
:
                
break
            
paths
.
append
(
path
)
            
path
=
'
'
            
i
=
j
+
1
        
else
:
            
path
+
=
c
    
return
paths
class
_PDH_Counter_Union
(
Union
)
:
    
_fields_
=
[
(
'
longValue
'
LONG
)
                
(
'
doubleValue
'
c_double
)
                
(
'
largeValue
'
_LONGLONG
)
                
(
'
AnsiStringValue
'
LPCSTR
)
                
(
'
WideStringValue
'
LPCWSTR
)
]
class
_PDH_FMT_COUNTERVALUE
(
Structure
)
:
    
_fields_
=
[
(
'
CStatus
'
DWORD
)
                
(
'
union
'
_PDH_Counter_Union
)
]
_PDH_FMT_LONG
=
0x00000100
class
WinCounterManager
(
CounterManager
)
:
    
def
__init__
(
self
process_name
process
counters
                 
childProcess
=
"
plugin
-
container
"
)
:
        
CounterManager
.
__init__
(
self
)
        
self
.
childProcess
=
childProcess
        
self
.
registeredCounters
=
{
}
        
self
.
registerCounters
(
counters
)
        
pdh
.
PdhEnumObjectsA
(
None
None
0
1
0
True
)
        
for
counter
in
self
.
registeredCounters
:
            
try
:
                
self
.
_addCounter
(
process_name
'
process
'
counter
)
            
except
TalosError
:
                
self
.
_addCounter
(
process_name
'
Memory
'
counter
)
            
self
.
_updateCounterPathsForChildProcesses
(
counter
)
    
def
_addCounter
(
self
processName
counterType
counterName
)
:
        
pCounterPathElements
=
_PDH_COUNTER_PATH_ELEMENTS_A
(
            
LPSTR
(
None
)
            
LPSTR
(
counterType
)
            
LPSTR
(
processName
)
            
LPSTR
(
None
)
            
DWORD
(
-
1
)
            
LPSTR
(
counterName
)
        
)
        
pcchbufferSize
=
DWORD
(
0
)
        
if
pdh
.
PdhMakeCounterPathA
(
pointer
(
pCounterPathElements
)
                                   
LPCSTR
(
0
)
pointer
(
pcchbufferSize
)
                                   
DWORD
(
0
)
)
!
=
_PDH_MORE_DATA
:
            
raise
TalosError
(
                
"
Could
not
create
counter
path
for
counter
%
s
for
%
s
"
                
%
(
counterName
processName
)
            
)
        
szFullPathBuffer
=
LPCSTR
(
'
\
0
'
*
pcchbufferSize
.
value
)
        
if
pdh
.
PdhMakeCounterPathA
(
pointer
(
pCounterPathElements
)
                                   
szFullPathBuffer
pointer
(
pcchbufferSize
)
                                   
DWORD
(
0
)
)
!
=
0
:
            
raise
TalosError
(
                
"
Could
not
create
counter
path
for
counter
%
s
for
%
s
"
                
%
(
counterName
processName
)
            
)
        
path
=
szFullPathBuffer
.
value
        
hq
=
HANDLE
(
)
        
if
pdh
.
PdhOpenQuery
(
None
None
byref
(
hq
)
)
!
=
0
:
            
raise
TalosError
(
"
Could
not
open
win32
counter
query
"
)
        
hc
=
HANDLE
(
)
        
if
pdh
.
PdhAddCounterA
(
hq
path
0
byref
(
hc
)
)
!
=
0
:
            
raise
TalosError
(
"
Could
not
add
win32
counter
%
s
"
%
path
)
        
self
.
registeredCounters
[
counterName
]
=
[
hq
[
(
hc
path
)
]
]
    
def
registerCounters
(
self
counters
)
:
        
for
counter
in
counters
:
            
if
counter
.
strip
(
)
=
=
'
Main_RSS
'
:
                
continue
            
if
counter
.
strip
(
)
=
=
'
mainthread_io
'
:
                
continue
            
self
.
registeredCounters
[
counter
]
=
[
]
    
def
_updateCounterPathsForChildProcesses
(
self
counter
)
:
        
hq
=
self
.
registeredCounters
[
counter
]
[
0
]
        
oldCounterListLength
=
len
(
self
.
registeredCounters
[
counter
]
[
1
]
)
        
pdh
.
PdhEnumObjectsA
(
None
None
0
1
0
True
)
        
expandedPaths
=
_getExpandedCounterPaths
(
self
.
childProcess
counter
)
        
if
not
expandedPaths
:
            
return
        
for
expandedPath
in
expandedPaths
:
            
alreadyInCounterList
=
False
            
for
singleCounter
in
self
.
registeredCounters
[
counter
]
[
1
]
:
                
if
expandedPath
=
=
singleCounter
[
1
]
:
                    
alreadyInCounterList
=
True
            
if
not
alreadyInCounterList
:
                
try
:
                    
newhc
=
HANDLE
(
)
                    
if
pdh
.
PdhAddCounterA
(
hq
expandedPath
0
                                          
byref
(
newhc
)
)
!
=
0
:
                        
raise
TalosError
(
                            
"
Could
not
add
expanded
win32
counter
%
s
"
                            
%
expandedPath
                        
)
                    
self
.
registeredCounters
[
counter
]
[
1
]
.
append
(
(
newhc
                                                                
expandedPath
)
)
                
except
Exception
:
                    
continue
        
if
oldCounterListLength
!
=
len
(
self
.
registeredCounters
[
counter
]
[
1
]
)
:
            
pdh
.
PdhCollectQueryData
(
hq
)
    
def
getCounterValue
(
self
counter
)
:
        
if
counter
not
in
self
.
registeredCounters
:
            
return
None
        
if
self
.
registeredCounters
[
counter
]
=
=
[
]
:
            
return
None
        
self
.
_updateCounterPathsForChildProcesses
(
counter
)
        
hq
=
self
.
registeredCounters
[
counter
]
[
0
]
        
pdh
.
PdhCollectQueryData
(
hq
)
        
aggregateValue
=
0
        
for
singleCounter
in
self
.
registeredCounters
[
counter
]
[
1
]
:
            
hc
=
singleCounter
[
0
]
            
dwType
=
DWORD
(
0
)
            
value
=
_PDH_FMT_COUNTERVALUE
(
)
            
if
pdh
.
PdhGetFormattedCounterValue
(
hc
_PDH_FMT_LONG
                                               
byref
(
dwType
)
                                               
byref
(
value
)
)
=
=
0
:
                
aggregateValue
+
=
value
.
union
.
longValue
        
return
aggregateValue
