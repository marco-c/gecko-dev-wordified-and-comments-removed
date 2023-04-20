import
sys
from
ipdl
.
ast
import
Visitor
ASYNC
class
SyncMessageChecker
(
Visitor
)
:
    
syncMsgList
=
[
]
    
seenProtocols
=
[
]
    
seenSyncMessages
=
[
]
    
def
__init__
(
self
syncMsgList
)
:
        
SyncMessageChecker
.
syncMsgList
=
syncMsgList
        
self
.
errors
=
[
]
    
def
prettyMsgName
(
self
msg
)
:
        
return
"
%
s
:
:
%
s
"
%
(
self
.
currentProtocol
msg
)
    
def
errorUnknownSyncMessage
(
self
loc
msg
)
:
        
self
.
errors
.
append
(
"
%
s
:
error
:
Unknown
sync
IPC
message
%
s
"
%
(
str
(
loc
)
msg
)
)
    
def
errorAsyncMessageCanRemove
(
self
loc
msg
)
:
        
self
.
errors
.
append
(
            
"
%
s
:
error
:
IPC
message
%
s
is
async
can
be
delisted
"
%
(
str
(
loc
)
msg
)
        
)
    
def
visitProtocol
(
self
p
)
:
        
self
.
errors
=
[
]
        
self
.
currentProtocol
=
p
.
name
        
SyncMessageChecker
.
seenProtocols
.
append
(
p
.
name
)
        
Visitor
.
visitProtocol
(
self
p
)
    
def
visitMessageDecl
(
self
md
)
:
        
pn
=
self
.
prettyMsgName
(
md
.
name
)
        
if
md
.
sendSemantics
is
not
ASYNC
:
            
if
pn
not
in
SyncMessageChecker
.
syncMsgList
:
                
self
.
errorUnknownSyncMessage
(
md
.
loc
pn
)
            
SyncMessageChecker
.
seenSyncMessages
.
append
(
pn
)
        
elif
pn
in
SyncMessageChecker
.
syncMsgList
:
            
self
.
errorAsyncMessageCanRemove
(
md
.
loc
pn
)
    
staticmethod
    
def
getFixedSyncMessages
(
)
:
        
return
set
(
SyncMessageChecker
.
syncMsgList
)
-
set
(
            
SyncMessageChecker
.
seenSyncMessages
        
)
def
checkSyncMessage
(
tu
syncMsgList
errout
=
sys
.
stderr
)
:
    
checker
=
SyncMessageChecker
(
syncMsgList
)
    
tu
.
accept
(
checker
)
    
if
len
(
checker
.
errors
)
:
        
for
error
in
checker
.
errors
:
            
print
(
error
file
=
errout
)
        
return
False
    
return
True
def
checkFixedSyncMessages
(
config
errout
=
sys
.
stderr
)
:
    
fixed
=
SyncMessageChecker
.
getFixedSyncMessages
(
)
    
error_free
=
True
    
for
item
in
fixed
:
        
protocol
=
item
.
split
(
"
:
:
"
)
[
0
]
        
if
(
            
protocol
in
SyncMessageChecker
.
seenProtocols
            
and
"
platform
"
not
in
config
.
options
(
item
)
        
)
:
            
print
(
                
"
Error
:
Sync
IPC
message
%
s
not
found
it
appears
to
be
fixed
.
\
n
"
                
"
Please
remove
it
from
sync
-
messages
.
ini
.
"
%
item
                
file
=
errout
            
)
            
error_free
=
False
    
return
error_free
