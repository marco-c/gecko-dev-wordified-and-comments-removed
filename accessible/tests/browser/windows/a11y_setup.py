"
"
"
Python
environment
for
Windows
a11y
browser
tests
.
"
"
"
import
ctypes
import
os
import
threading
from
ctypes
import
POINTER
byref
from
ctypes
.
wintypes
import
BOOL
HWND
LPARAM
POINT
from
dataclasses
import
dataclass
import
comtypes
.
automation
import
comtypes
.
client
import
psutil
from
comtypes
import
GUID
COMError
IServiceProvider
CHILDID_SELF
=
0
COWAIT_DEFAULT
=
0
EVENT_OBJECT_FOCUS
=
0x8005
EVENT_SYSTEM_SCROLLINGSTART
=
0x12
GA_ROOT
=
2
NAVRELATION_EMBEDS
=
0x1009
OBJID_CARET
=
-
8
OBJID_CLIENT
=
-
4
RPC_S_CALLPENDING
=
-
2147417835
WINEVENT_OUTOFCONTEXT
=
0
WM_CLOSE
=
0x0010
def
registerIa2Proxy
(
)
:
    
"
"
"
Register
the
IAccessible2
proxy
.
    
This
is
only
used
on
CI
because
we
don
'
t
want
to
mess
with
the
registry
on
    
local
developer
machines
.
Developers
should
register
the
proxy
themselves
    
using
regsvr32
.
    
This
registers
in
HKEY_CURRENT_USER
rather
than
HKEY_LOCAL_MACHINE
so
that
    
this
can
be
done
without
administrator
privileges
.
regsvr32
registers
in
    
HKEY_LOCAL_MACHINE
so
we
can
'
t
use
that
here
.
    
"
"
"
    
import
winreg
    
dll
=
os
.
path
.
join
(
os
.
getcwd
(
)
"
IA2Marshal
.
dll
"
)
    
if
not
os
.
path
.
isfile
(
dll
)
:
        
raise
RuntimeError
(
f
"
Couldn
'
t
find
IAccessible2
proxy
dll
:
{
dll
}
"
)
    
clsid
=
"
{
F9A6CC32
-
B0EF
-
490B
-
B102
-
179DDEEB08ED
}
"
    
with
winreg
.
CreateKey
(
        
winreg
.
HKEY_CURRENT_USER
rf
"
SOFTWARE
\
Classes
\
CLSID
\
{
clsid
}
\
InProcServer32
"
    
)
as
key
:
        
winreg
.
SetValue
(
key
None
winreg
.
REG_SZ
dll
)
    
for
interface
in
(
        
"
{
2118B599
-
733F
-
43D0
-
A569
-
0B31D125ED9A
}
"
    
)
:
        
with
winreg
.
CreateKey
(
            
winreg
.
HKEY_CURRENT_USER
            
rf
"
SOFTWARE
\
Classes
\
Interface
\
{
interface
}
\
ProxyStubClsid32
"
        
)
as
key
:
            
winreg
.
SetValue
(
key
None
winreg
.
REG_SZ
clsid
)
user32
=
ctypes
.
windll
.
user32
oleacc
=
ctypes
.
oledll
.
oleacc
oleaccMod
=
comtypes
.
client
.
GetModule
(
"
oleacc
.
dll
"
)
IAccessible
=
oleaccMod
.
IAccessible
del
oleaccMod
ia2Tlb
=
os
.
path
.
join
(
    
os
.
getcwd
(
)
    
"
.
.
"
    
"
.
.
"
    
"
.
.
"
    
"
accessible
"
    
"
interfaces
"
    
"
ia2
"
    
"
IA2Typelib
.
tlb
"
)
if
not
os
.
path
.
isfile
(
ia2Tlb
)
:
    
ia2Tlb
=
os
.
path
.
join
(
os
.
getcwd
(
)
"
ia2Typelib
.
tlb
"
)
    
registerIa2Proxy
(
)
ia2Mod
=
comtypes
.
client
.
GetModule
(
ia2Tlb
)
del
ia2Tlb
globals
(
)
.
update
(
(
k
getattr
(
ia2Mod
k
)
)
for
k
in
ia2Mod
.
__all__
)
IAccessible2
=
ia2Mod
.
IAccessible2
del
ia2Mod
uiaMod
=
comtypes
.
client
.
GetModule
(
"
UIAutomationCore
.
dll
"
)
globals
(
)
.
update
(
(
k
getattr
(
uiaMod
k
)
)
for
k
in
uiaMod
.
__all__
)
uiaClient
=
comtypes
.
CoCreateInstance
(
    
uiaMod
.
CUIAutomation
.
_reg_clsid_
    
interface
=
uiaMod
.
IUIAutomation
    
clsctx
=
comtypes
.
CLSCTX_INPROC_SERVER
)
uiaCoreMod
=
comtypes
.
client
.
GetModule
(
(
"
{
930299ce
-
9965
-
4dec
-
b0f4
-
a54848d4b667
}
"
)
)
uiaReg
=
comtypes
.
CoCreateInstance
(
    
uiaCoreMod
.
CUIAutomationRegistrar
.
_reg_clsid_
    
interface
=
uiaCoreMod
.
IUIAutomationRegistrar
)
uiaAccessibleActionsPropertyId
=
uiaReg
.
RegisterProperty
(
    
byref
(
        
uiaCoreMod
.
UIAutomationPropertyInfo
(
            
GUID
(
"
{
8C787AC3
-
0405
-
4C94
-
AC09
-
7A56A173F7EF
}
"
)
            
"
AccessibleActions
"
            
uiaCoreMod
.
UIAutomationType_ElementArray
        
)
    
)
)
del
uiaReg
uiaCoreMod
_threadLocal
=
threading
.
local
(
)
def
setup
(
)
:
    
if
getattr
(
_threadLocal
"
isSetup
"
False
)
:
        
return
    
comtypes
.
CoInitialize
(
)
    
_threadLocal
.
isSetup
=
True
def
AccessibleObjectFromWindow
(
hwnd
objectID
=
OBJID_CLIENT
)
:
    
p
=
POINTER
(
IAccessible
)
(
)
    
oleacc
.
AccessibleObjectFromWindow
(
        
hwnd
objectID
byref
(
IAccessible
.
_iid_
)
byref
(
p
)
    
)
    
return
p
def
getWindowClass
(
hwnd
)
:
    
MAX_CHARS
=
257
    
buffer
=
ctypes
.
create_unicode_buffer
(
MAX_CHARS
)
    
user32
.
GetClassNameW
(
hwnd
buffer
MAX_CHARS
)
    
return
buffer
.
value
def
getFirefoxHwnd
(
)
:
    
"
"
"
Search
all
top
level
windows
for
the
Firefox
instance
being
    
tested
.
    
We
search
by
window
class
name
and
window
title
prefix
.
    
"
"
"
    
commonPid
=
psutil
.
Process
(
)
.
parent
(
)
.
ppid
(
)
    
found
=
[
]
    
ctypes
.
WINFUNCTYPE
(
BOOL
HWND
LPARAM
)
    
def
callback
(
hwnd
lParam
)
:
        
if
getWindowClass
(
hwnd
)
!
=
"
MozillaWindowClass
"
:
            
return
True
        
pid
=
ctypes
.
wintypes
.
DWORD
(
)
        
user32
.
GetWindowThreadProcessId
(
hwnd
byref
(
pid
)
)
        
if
psutil
.
Process
(
pid
.
value
)
.
parent
(
)
.
ppid
(
)
!
=
commonPid
:
            
return
True
        
found
.
append
(
hwnd
)
        
return
False
    
user32
.
EnumWindows
(
callback
LPARAM
(
0
)
)
    
if
not
found
:
        
raise
LookupError
(
"
Couldn
'
t
find
Firefox
HWND
"
)
    
return
found
[
0
]
def
toIa2
(
obj
)
:
    
serv
=
obj
.
QueryInterface
(
IServiceProvider
)
    
return
serv
.
QueryService
(
IAccessible2
.
_iid_
IAccessible2
)
def
getDocIa2
(
)
:
    
"
"
"
Get
the
IAccessible2
for
the
document
being
tested
.
"
"
"
    
hwnd
=
getFirefoxHwnd
(
)
    
root
=
AccessibleObjectFromWindow
(
hwnd
)
    
doc
=
root
.
accNavigate
(
NAVRELATION_EMBEDS
0
)
    
try
:
        
child
=
toIa2
(
doc
.
accChild
(
1
)
)
        
if
"
id
:
default
-
iframe
-
id
;
"
in
child
.
attributes
:
            
doc
=
child
.
accChild
(
1
)
    
except
COMError
:
        
pass
    
return
toIa2
(
doc
)
def
findIa2ByDomId
(
root
id
)
:
    
search
=
f
"
id
:
{
id
}
;
"
    
for
i
in
range
(
1
root
.
accChildCount
+
1
)
:
        
child
=
toIa2
(
root
.
accChild
(
i
)
)
        
if
search
in
child
.
attributes
:
            
return
child
        
descendant
=
findIa2ByDomId
(
child
id
)
        
if
descendant
:
            
return
descendant
dataclass
class
WinEvent
:
    
event
:
int
    
hwnd
:
int
    
objectId
:
int
    
childId
:
int
    
def
getIa2
(
self
)
:
        
acc
=
ctypes
.
POINTER
(
IAccessible
)
(
)
        
child
=
comtypes
.
automation
.
VARIANT
(
)
        
ctypes
.
oledll
.
oleacc
.
AccessibleObjectFromEvent
(
            
self
.
hwnd
            
self
.
objectId
            
self
.
childId
            
ctypes
.
byref
(
acc
)
            
ctypes
.
byref
(
child
)
        
)
        
if
child
.
value
!
=
CHILDID_SELF
:
            
return
None
        
return
toIa2
(
acc
)
class
WaitForWinEvent
:
    
"
"
"
Wait
for
a
win
event
usually
for
IAccessible2
.
    
This
should
be
used
as
follows
:
    
1
.
Create
an
instance
to
wait
for
the
desired
event
.
    
2
.
Perform
the
action
that
should
fire
the
event
.
    
3
.
Call
wait
(
)
on
the
instance
you
created
in
1
)
to
wait
for
the
event
.
    
"
"
"
    
def
__init__
(
self
eventId
match
)
:
        
"
"
"
eventId
is
the
event
id
to
wait
for
.
        
match
is
either
None
to
match
any
object
an
str
containing
the
DOM
id
        
of
the
desired
object
or
a
function
taking
a
WinEvent
which
should
        
return
True
if
this
is
the
requested
event
.
        
"
"
"
        
self
.
_matched
=
None
        
self
.
_signal
=
ctypes
.
windll
.
kernel32
.
CreateEventW
(
None
True
False
None
)
        
ctypes
.
WINFUNCTYPE
(
            
None
            
ctypes
.
wintypes
.
HANDLE
            
ctypes
.
wintypes
.
DWORD
            
ctypes
.
wintypes
.
HWND
            
ctypes
.
wintypes
.
LONG
            
ctypes
.
wintypes
.
LONG
            
ctypes
.
wintypes
.
DWORD
            
ctypes
.
wintypes
.
DWORD
        
)
        
def
winEventProc
(
hook
eventId
hwnd
objectId
childId
thread
time
)
:
            
event
=
WinEvent
(
eventId
hwnd
objectId
childId
)
            
if
isinstance
(
match
str
)
:
                
try
:
                    
ia2
=
event
.
getIa2
(
)
                    
if
f
"
id
:
{
match
}
;
"
in
ia2
.
attributes
:
                        
self
.
_matched
=
event
                
except
(
comtypes
.
COMError
TypeError
)
:
                    
pass
            
elif
callable
(
match
)
:
                
try
:
                    
if
match
(
event
)
:
                        
self
.
_matched
=
event
                
except
Exception
as
e
:
                    
self
.
_matched
=
e
            
if
self
.
_matched
:
                
ctypes
.
windll
.
kernel32
.
SetEvent
(
self
.
_signal
)
        
self
.
_hook
=
user32
.
SetWinEventHook
(
            
eventId
eventId
None
winEventProc
0
0
WINEVENT_OUTOFCONTEXT
        
)
        
self
.
_proc
=
winEventProc
    
def
wait
(
self
)
:
        
"
"
"
Wait
for
and
return
the
desired
WinEvent
.
"
"
"
        
handles
=
(
ctypes
.
c_void_p
*
1
)
(
self
.
_signal
)
        
index
=
ctypes
.
wintypes
.
DWORD
(
)
        
TIMEOUT
=
10000
        
try
:
            
ctypes
.
oledll
.
ole32
.
CoWaitForMultipleHandles
(
                
COWAIT_DEFAULT
TIMEOUT
1
handles
ctypes
.
byref
(
index
)
            
)
        
except
OSError
as
e
:
            
if
e
.
winerror
=
=
RPC_S_CALLPENDING
:
                
raise
TimeoutError
(
"
Timeout
before
desired
event
received
"
)
            
raise
        
finally
:
            
user32
.
UnhookWinEvent
(
self
.
_hook
)
            
ctypes
.
windll
.
kernel32
.
CloseHandle
(
self
.
_signal
)
            
self
.
_proc
=
None
        
if
isinstance
(
self
.
_matched
Exception
)
:
            
raise
self
.
_matched
from
self
.
_matched
        
return
self
.
_matched
def
getDocUia
(
)
:
    
"
"
"
Get
the
IUIAutomationElement
for
the
document
being
tested
.
"
"
"
    
hwnd
=
getFirefoxHwnd
(
)
    
root
=
uiaClient
.
ElementFromHandle
(
hwnd
)
    
doc
=
findUiaByDomId
(
root
"
body
"
)
    
if
not
doc
:
        
info
(
"
getUiaDoc
:
Falling
back
to
IA2
"
)
        
ia2
=
getDocIa2
(
)
        
return
uiaClient
.
ElementFromIAccessible
(
ia2
CHILDID_SELF
)
    
child
=
uiaClient
.
RawViewWalker
.
GetFirstChildElement
(
doc
)
    
if
child
and
child
.
CurrentAutomationId
=
=
"
default
-
iframe
-
id
"
:
        
doc
=
uiaClient
.
RawViewWalker
.
GetFirstChildElement
(
child
)
    
return
doc
def
findUiaByDomId
(
root
id
)
:
    
cond
=
uiaClient
.
CreatePropertyCondition
(
uiaMod
.
UIA_AutomationIdPropertyId
id
)
    
request
=
uiaClient
.
CreateCacheRequest
(
)
    
request
.
TreeFilter
=
uiaClient
.
RawViewCondition
    
el
=
root
.
FindFirstBuildCache
(
uiaMod
.
TreeScope_Descendants
cond
request
)
    
if
not
el
:
        
return
None
    
return
el
.
QueryInterface
(
uiaMod
.
IUIAutomationElement9
)
class
WaitForUiaEvent
(
comtypes
.
COMObject
)
:
    
"
"
"
Wait
for
a
UIA
event
.
    
This
should
be
used
as
follows
:
    
1
.
Create
an
instance
to
wait
for
the
desired
event
.
    
2
.
Perform
the
action
that
should
fire
the
event
.
    
3
.
Call
wait
(
)
on
the
instance
you
created
in
1
)
to
wait
for
the
event
.
    
"
"
"
    
_com_interfaces_
=
[
        
uiaMod
.
IUIAutomationFocusChangedEventHandler
        
uiaMod
.
IUIAutomationPropertyChangedEventHandler
        
uiaMod
.
IUIAutomationEventHandler
    
]
    
def
__init__
(
self
*
eventId
=
None
property
=
None
match
=
None
)
:
        
"
"
"
eventId
is
the
event
id
to
wait
for
.
Alternatively
you
can
pass
        
property
to
wait
for
a
particular
property
to
change
.
        
match
is
either
None
to
match
any
object
an
str
containing
the
DOM
id
        
of
the
desired
object
or
a
function
taking
a
IUIAutomationElement
which
        
should
return
True
if
this
is
the
requested
event
.
        
"
"
"
        
self
.
_match
=
match
        
self
.
_matched
=
None
        
self
.
_signal
=
ctypes
.
windll
.
kernel32
.
CreateEventW
(
None
True
False
None
)
        
if
eventId
=
=
uiaMod
.
UIA_AutomationFocusChangedEventId
:
            
uiaClient
.
AddFocusChangedEventHandler
(
None
self
)
        
elif
eventId
:
            
uiaClient
.
AddAutomationEventHandler
(
                
eventId
                
uiaClient
.
GetRootElement
(
)
                
uiaMod
.
TreeScope_Subtree
                
None
                
self
            
)
        
elif
property
:
            
uiaClient
.
AddPropertyChangedEventHandler
(
                
uiaClient
.
GetRootElement
(
)
                
uiaMod
.
TreeScope_Subtree
                
None
                
self
                
[
property
]
            
)
        
else
:
            
raise
ValueError
(
"
No
supported
event
specified
"
)
    
def
_checkMatch
(
self
sender
)
:
        
if
isinstance
(
self
.
_match
str
)
:
            
try
:
                
if
sender
.
CurrentAutomationId
=
=
self
.
_match
:
                    
self
.
_matched
=
sender
            
except
comtypes
.
COMError
:
                
pass
        
elif
callable
(
self
.
_match
)
:
            
try
:
                
if
self
.
_match
(
sender
)
:
                    
self
.
_matched
=
sender
            
except
Exception
as
e
:
                
self
.
_matched
=
e
        
else
:
            
self
.
_matched
=
sender
        
if
self
.
_matched
:
            
ctypes
.
windll
.
kernel32
.
SetEvent
(
self
.
_signal
)
    
def
HandleFocusChangedEvent
(
self
sender
)
:
        
self
.
_checkMatch
(
sender
)
    
def
HandlePropertyChangedEvent
(
self
sender
propertyId
newValue
)
:
        
self
.
_checkMatch
(
sender
)
    
def
HandleAutomationEvent
(
self
sender
eventId
)
:
        
self
.
_checkMatch
(
sender
)
    
def
wait
(
self
)
:
        
"
"
"
Wait
for
and
return
the
IUIAutomationElement
which
sent
the
desired
        
event
.
"
"
"
        
handles
=
(
ctypes
.
c_void_p
*
1
)
(
self
.
_signal
)
        
index
=
ctypes
.
wintypes
.
DWORD
(
)
        
TIMEOUT
=
10000
        
try
:
            
ctypes
.
oledll
.
ole32
.
CoWaitForMultipleHandles
(
                
COWAIT_DEFAULT
TIMEOUT
1
handles
ctypes
.
byref
(
index
)
            
)
        
except
OSError
as
e
:
            
if
e
.
winerror
=
=
RPC_S_CALLPENDING
:
                
raise
TimeoutError
(
"
Timeout
before
desired
event
received
"
)
            
raise
        
finally
:
            
uiaClient
.
RemoveAllEventHandlers
(
)
            
ctypes
.
windll
.
kernel32
.
CloseHandle
(
self
.
_signal
)
        
if
isinstance
(
self
.
_matched
Exception
)
:
            
raise
self
.
_matched
from
self
.
_matched
        
return
self
.
_matched
def
getUiaPattern
(
element
patternName
)
:
    
"
"
"
Get
a
control
pattern
interface
from
an
IUIAutomationElement
.
"
"
"
    
patternId
=
getattr
(
uiaMod
f
"
UIA_
{
patternName
}
PatternId
"
)
    
unknown
=
element
.
GetCurrentPattern
(
patternId
)
    
if
not
unknown
:
        
return
None
    
interface
=
getattr
(
uiaMod
f
"
IUIAutomation
{
patternName
}
Pattern
"
)
    
return
unknown
.
QueryInterface
(
interface
)
