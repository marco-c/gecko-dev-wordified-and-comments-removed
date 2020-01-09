import
re
from
copy
import
deepcopy
from
collections
import
OrderedDict
import
ipdl
.
ast
import
ipdl
.
builtin
from
ipdl
.
cxx
.
ast
import
*
from
ipdl
.
type
import
ActorType
UnionType
TypeVisitor
builtinHeaderIncludes
class
LowerToCxx
:
    
def
lower
(
self
tu
segmentcapacitydict
)
:
        
'
'
'
returns
|
[
header
:
File
]
[
cpp
:
File
]
|
representing
the
lowered
form
of
|
tu
|
'
'
'
        
tu
.
accept
(
_DecorateWithCxxStuff
(
)
)
        
name
=
tu
.
name
        
pheader
pcpp
=
File
(
name
+
'
.
h
'
)
File
(
name
+
'
.
cpp
'
)
        
_GenerateProtocolCode
(
)
.
lower
(
tu
pheader
pcpp
segmentcapacitydict
)
        
headers
=
[
pheader
]
        
cpps
=
[
pcpp
]
        
if
tu
.
protocol
:
            
pname
=
tu
.
protocol
.
name
            
parentheader
parentcpp
=
File
(
pname
+
'
Parent
.
h
'
)
File
(
pname
+
'
Parent
.
cpp
'
)
            
_GenerateProtocolParentCode
(
)
.
lower
(
                
tu
pname
+
'
Parent
'
parentheader
parentcpp
)
            
childheader
childcpp
=
File
(
pname
+
'
Child
.
h
'
)
File
(
pname
+
'
Child
.
cpp
'
)
            
_GenerateProtocolChildCode
(
)
.
lower
(
                
tu
pname
+
'
Child
'
childheader
childcpp
)
            
headers
+
=
[
parentheader
childheader
]
            
cpps
+
=
[
parentcpp
childcpp
]
        
return
headers
cpps
def
hashfunc
(
value
)
:
    
h
=
hash
(
value
)
%
2
*
*
32
    
if
h
<
0
:
        
h
+
=
2
*
*
32
    
return
h
_NULL_ACTOR_ID
=
ExprLiteral
.
ZERO
_FREED_ACTOR_ID
=
ExprLiteral
.
ONE
_DISCLAIMER
=
Whitespace
(
'
'
'
/
/
/
/
Automatically
generated
by
ipdlc
.
/
/
Edit
at
your
own
risk
/
/
'
'
'
)
class
_struct
:
    
pass
def
_namespacedHeaderName
(
name
namespaces
)
:
    
pfx
=
'
/
'
.
join
(
[
ns
.
name
for
ns
in
namespaces
]
)
    
if
pfx
:
        
return
pfx
+
'
/
'
+
name
    
else
:
        
return
name
def
_ipdlhHeaderName
(
tu
)
:
    
assert
tu
.
filetype
=
=
'
header
'
    
return
_namespacedHeaderName
(
tu
.
name
tu
.
namespaces
)
def
_protocolHeaderName
(
p
side
=
'
'
)
:
    
if
side
:
        
side
=
side
.
title
(
)
    
base
=
p
.
name
+
side
    
return
_namespacedHeaderName
(
base
p
.
namespaces
)
def
_includeGuardMacroName
(
headerfile
)
:
    
return
re
.
sub
(
r
'
[
.
/
]
'
'
_
'
headerfile
.
name
)
def
_includeGuardStart
(
headerfile
)
:
    
guard
=
_includeGuardMacroName
(
headerfile
)
    
return
[
CppDirective
(
'
ifndef
'
guard
)
            
CppDirective
(
'
define
'
guard
)
]
def
_includeGuardEnd
(
headerfile
)
:
    
guard
=
_includeGuardMacroName
(
headerfile
)
    
return
[
CppDirective
(
'
endif
'
'
/
/
ifndef
'
+
guard
)
]
def
_messageStartName
(
ptype
)
:
    
return
ptype
.
name
(
)
+
'
MsgStart
'
def
_protocolId
(
ptype
)
:
    
return
ExprVar
(
_messageStartName
(
ptype
)
)
def
_protocolIdType
(
)
:
    
return
Type
.
INT32
def
_actorName
(
pname
side
)
:
    
"
"
"
|
pname
|
is
the
protocol
name
.
|
side
|
is
'
Parent
'
or
'
Child
'
.
"
"
"
    
tag
=
side
    
if
not
tag
[
0
]
.
isupper
(
)
:
        
tag
=
side
.
title
(
)
    
return
pname
+
tag
def
_actorIdType
(
)
:
    
return
Type
.
INT32
def
_actorTypeTagType
(
)
:
    
return
Type
.
INT32
def
_actorId
(
actor
=
None
)
:
    
if
actor
is
not
None
:
        
return
ExprCall
(
ExprSelect
(
actor
'
-
>
'
'
Id
'
)
)
    
return
ExprCall
(
ExprVar
(
'
Id
'
)
)
def
_actorHId
(
actorhandle
)
:
    
return
ExprSelect
(
actorhandle
'
.
'
'
mId
'
)
def
_actorState
(
actor
)
:
    
return
ExprSelect
(
actor
'
-
>
'
'
mLivenessState
'
)
def
_backstagePass
(
)
:
    
return
ExprCall
(
ExprVar
(
'
mozilla
:
:
ipc
:
:
PrivateIPDLInterface
'
)
)
def
_iterType
(
ptr
)
:
    
return
Type
(
'
PickleIterator
'
ptr
=
ptr
)
def
_deleteId
(
)
:
    
return
ExprVar
(
'
Msg___delete____ID
'
)
def
_deleteReplyId
(
)
:
    
return
ExprVar
(
'
Reply___delete____ID
'
)
def
_lookupListener
(
idexpr
)
:
    
return
ExprCall
(
ExprVar
(
'
Lookup
'
)
args
=
[
idexpr
]
)
def
_makeForwardDeclForQClass
(
clsname
quals
cls
=
True
struct
=
False
)
:
    
fd
=
ForwardDecl
(
clsname
cls
=
cls
struct
=
struct
)
    
if
0
=
=
len
(
quals
)
:
        
return
fd
    
outerns
=
Namespace
(
quals
[
0
]
)
    
innerns
=
outerns
    
for
ns
in
quals
[
1
:
]
:
        
tmpns
=
Namespace
(
ns
)
        
innerns
.
addstmt
(
tmpns
)
        
innerns
=
tmpns
    
innerns
.
addstmt
(
fd
)
    
return
outerns
def
_makeForwardDeclForActor
(
ptype
side
)
:
    
return
_makeForwardDeclForQClass
(
_actorName
(
ptype
.
qname
.
baseid
side
)
                                     
ptype
.
qname
.
quals
)
def
_makeForwardDecl
(
type
)
:
    
return
_makeForwardDeclForQClass
(
type
.
name
(
)
type
.
qname
.
quals
)
def
_putInNamespaces
(
cxxthing
namespaces
)
:
    
"
"
"
|
namespaces
|
is
in
order
[
outer
.
.
.
inner
]
"
"
"
    
if
0
=
=
len
(
namespaces
)
:
        
return
cxxthing
    
outerns
=
Namespace
(
namespaces
[
0
]
.
name
)
    
innerns
=
outerns
    
for
ns
in
namespaces
[
1
:
]
:
        
newns
=
Namespace
(
ns
.
name
)
        
innerns
.
addstmt
(
newns
)
        
innerns
=
newns
    
innerns
.
addstmt
(
cxxthing
)
    
return
outerns
def
_sendPrefix
(
msgtype
)
:
    
"
"
"
Prefix
of
the
name
of
the
C
+
+
method
that
sends
|
msgtype
|
.
"
"
"
    
if
msgtype
.
isInterrupt
(
)
:
        
return
'
Call
'
    
return
'
Send
'
def
_recvPrefix
(
msgtype
)
:
    
"
"
"
Prefix
of
the
name
of
the
C
+
+
method
that
handles
|
msgtype
|
.
"
"
"
    
if
msgtype
.
isInterrupt
(
)
:
        
return
'
Answer
'
    
return
'
Recv
'
def
_flatTypeName
(
ipdltype
)
:
    
"
"
"
Return
a
'
flattened
'
IPDL
type
name
that
can
be
used
as
an
identifier
.
E
.
g
.
|
Foo
[
]
|
-
-
>
|
ArrayOfFoo
|
.
"
"
"
    
if
ipdltype
.
isIPDL
(
)
and
ipdltype
.
isArray
(
)
:
        
return
'
ArrayOf
'
+
ipdltype
.
basetype
.
name
(
)
    
return
ipdltype
.
name
(
)
def
_hasVisibleActor
(
ipdltype
)
:
    
"
"
"
Return
true
iff
a
C
+
+
decl
of
|
ipdltype
|
would
have
an
Actor
*
type
.
For
example
:
|
Actor
[
]
|
would
turn
into
|
Array
<
ActorParent
*
>
|
so
this
function
would
return
true
for
|
Actor
[
]
|
.
"
"
"
    
return
(
ipdltype
.
isIPDL
(
)
            
and
(
ipdltype
.
isActor
(
)
                 
or
(
ipdltype
.
isArray
(
)
                     
and
_hasVisibleActor
(
ipdltype
.
basetype
)
)
)
)
def
_abortIfFalse
(
cond
msg
)
:
    
return
StmtExpr
(
ExprCall
(
        
ExprVar
(
'
MOZ_RELEASE_ASSERT
'
)
        
[
cond
ExprLiteral
.
String
(
msg
)
]
)
)
def
_refptr
(
T
)
:
    
return
Type
(
'
RefPtr
'
T
=
T
)
def
_uniqueptr
(
T
)
:
    
return
Type
(
'
UniquePtr
'
T
=
T
)
def
_tuple
(
types
const
=
False
ref
=
False
)
:
    
return
Type
(
'
Tuple
'
T
=
types
const
=
const
ref
=
ref
)
def
_promise
(
resolvetype
rejecttype
tail
resolver
=
False
)
:
    
inner
=
Type
(
'
Private
'
)
if
resolver
else
None
    
return
Type
(
'
MozPromise
'
T
=
[
resolvetype
rejecttype
tail
]
inner
=
inner
)
def
_makePromise
(
returns
side
resolver
=
False
)
:
    
if
len
(
returns
)
>
1
:
        
resolvetype
=
_tuple
(
[
d
.
bareType
(
side
)
for
d
in
returns
]
)
    
else
:
        
resolvetype
=
returns
[
0
]
.
bareType
(
side
)
    
return
_promise
(
resolvetype
                    
_ResponseRejectReason
.
Type
(
)
                    
ExprLiteral
.
TRUE
                    
resolver
=
resolver
)
def
_makeResolver
(
returns
side
)
:
    
if
len
(
returns
)
>
1
:
        
resolvetype
=
_tuple
(
[
d
.
moveType
(
side
)
for
d
in
returns
]
)
    
else
:
        
resolvetype
=
returns
[
0
]
.
moveType
(
side
)
    
return
TypeFunction
(
[
Decl
(
resolvetype
'
'
)
]
)
def
_cxxArrayType
(
basetype
const
=
False
ref
=
False
)
:
    
return
Type
(
'
nsTArray
'
T
=
basetype
const
=
const
ref
=
ref
hasimplicitcopyctor
=
False
)
def
_cxxManagedContainerType
(
basetype
const
=
False
ref
=
False
)
:
    
return
Type
(
'
ManagedContainer
'
T
=
basetype
                
const
=
const
ref
=
ref
hasimplicitcopyctor
=
False
)
def
_callInsertManagedActor
(
managees
actor
)
:
    
return
ExprCall
(
ExprSelect
(
managees
'
.
'
'
PutEntry
'
)
                    
args
=
[
actor
]
)
def
_callRemoveManagedActor
(
managees
actor
)
:
    
return
ExprCall
(
ExprSelect
(
managees
'
.
'
'
RemoveEntry
'
)
                    
args
=
[
actor
]
)
def
_callClearManagedActors
(
managees
)
:
    
return
ExprCall
(
ExprSelect
(
managees
'
.
'
'
Clear
'
)
)
def
_callHasManagedActor
(
managees
actor
)
:
    
return
ExprCall
(
ExprSelect
(
managees
'
.
'
'
Contains
'
)
args
=
[
actor
]
)
def
_otherSide
(
side
)
:
    
if
side
=
=
'
child
'
:
        
return
'
parent
'
    
if
side
=
=
'
parent
'
:
        
return
'
child
'
    
assert
0
def
_ifLogging
(
topLevelProtocol
stmts
)
:
    
iflogging
=
StmtIf
(
ExprCall
(
ExprVar
(
'
mozilla
:
:
ipc
:
:
LoggingEnabledFor
'
)
                                
args
=
[
topLevelProtocol
]
)
)
    
iflogging
.
addifstmts
(
stmts
)
    
return
iflogging
def
_printErrorMessage
(
msg
)
:
    
if
isinstance
(
msg
str
)
:
        
msg
=
ExprLiteral
.
String
(
msg
)
    
return
StmtExpr
(
        
ExprCall
(
ExprVar
(
'
NS_ERROR
'
)
args
=
[
msg
]
)
)
def
_protocolErrorBreakpoint
(
msg
)
:
    
if
isinstance
(
msg
str
)
:
        
msg
=
ExprLiteral
.
String
(
msg
)
    
return
StmtExpr
(
ExprCall
(
ExprVar
(
'
mozilla
:
:
ipc
:
:
ProtocolErrorBreakpoint
'
)
                             
args
=
[
msg
]
)
)
def
_printWarningMessage
(
msg
)
:
    
if
isinstance
(
msg
str
)
:
        
msg
=
ExprLiteral
.
String
(
msg
)
    
return
StmtExpr
(
        
ExprCall
(
ExprVar
(
'
NS_WARNING
'
)
args
=
[
msg
]
)
)
def
_fatalError
(
msg
)
:
    
return
StmtExpr
(
        
ExprCall
(
ExprVar
(
'
FatalError
'
)
args
=
[
ExprLiteral
.
String
(
msg
)
]
)
)
def
_logicError
(
msg
)
:
    
return
StmtExpr
(
        
ExprCall
(
ExprVar
(
'
mozilla
:
:
ipc
:
:
LogicError
'
)
args
=
[
ExprLiteral
.
String
(
msg
)
]
)
)
def
_sentinelReadError
(
classname
)
:
    
return
StmtExpr
(
        
ExprCall
(
ExprVar
(
'
mozilla
:
:
ipc
:
:
SentinelReadError
'
)
                 
args
=
[
ExprLiteral
.
String
(
classname
)
]
)
)
class
_Result
:
    
staticmethod
    
def
Type
(
)
:
        
return
Type
(
'
Result
'
)
    
Processed
=
ExprVar
(
'
MsgProcessed
'
)
    
NotKnown
=
ExprVar
(
'
MsgNotKnown
'
)
    
NotAllowed
=
ExprVar
(
'
MsgNotAllowed
'
)
    
PayloadError
=
ExprVar
(
'
MsgPayloadError
'
)
    
ProcessingError
=
ExprVar
(
'
MsgProcessingError
'
)
    
RouteError
=
ExprVar
(
'
MsgRouteError
'
)
    
ValuError
=
ExprVar
(
'
MsgValueError
'
)
def
errfnSend
(
msg
errcode
=
ExprLiteral
.
FALSE
)
:
    
return
[
        
_fatalError
(
msg
)
        
StmtReturn
(
errcode
)
    
]
def
errfnSendCtor
(
msg
)
:
return
errfnSend
(
msg
errcode
=
ExprLiteral
.
NULL
)
def
errfnSendDtor
(
msg
)
:
    
return
[
        
_printErrorMessage
(
msg
)
        
StmtReturn
.
FALSE
    
]
def
errfnRecv
(
msg
errcode
=
_Result
.
ValuError
)
:
    
return
[
        
_fatalError
(
msg
)
        
StmtReturn
(
errcode
)
    
]
def
errfnSentinel
(
rvalue
=
ExprLiteral
.
FALSE
)
:
    
def
inner
(
msg
)
:
        
return
[
_sentinelReadError
(
msg
)
StmtReturn
(
rvalue
)
]
    
return
inner
def
_destroyMethod
(
)
:
    
return
ExprVar
(
'
ActorDestroy
'
)
def
errfnUnreachable
(
msg
)
:
    
return
[
        
_logicError
(
msg
)
    
]
class
_DestroyReason
:
    
staticmethod
    
def
Type
(
)
:
return
Type
(
'
ActorDestroyReason
'
)
    
Deletion
=
ExprVar
(
'
Deletion
'
)
    
AncestorDeletion
=
ExprVar
(
'
AncestorDeletion
'
)
    
NormalShutdown
=
ExprVar
(
'
NormalShutdown
'
)
    
AbnormalShutdown
=
ExprVar
(
'
AbnormalShutdown
'
)
    
FailedConstructor
=
ExprVar
(
'
FailedConstructor
'
)
class
_ResponseRejectReason
:
    
staticmethod
    
def
Type
(
)
:
        
return
Type
(
'
ResponseRejectReason
'
)
    
SendError
=
ExprVar
(
'
ResponseRejectReason
:
:
SendError
'
)
    
ChannelClosed
=
ExprVar
(
'
ResponseRejectReason
:
:
ChannelClosed
'
)
    
HandlerRejected
=
ExprVar
(
'
ResponseRejectReason
:
:
HandlerRejected
'
)
    
ActorDestroyed
=
ExprVar
(
'
ResponseRejectReason
:
:
ActorDestroyed
'
)
class
_ConvertToCxxType
(
TypeVisitor
)
:
    
def
__init__
(
self
side
fq
)
:
        
self
.
side
=
side
        
self
.
fq
=
fq
    
def
typename
(
self
thing
)
:
        
if
self
.
fq
:
            
return
thing
.
fullname
(
)
        
return
thing
.
name
(
)
    
def
visitImportedCxxType
(
self
t
)
:
        
cxxtype
=
Type
(
self
.
typename
(
t
)
)
        
if
t
.
isRefcounted
(
)
:
            
cxxtype
=
_refptr
(
cxxtype
)
        
return
cxxtype
    
def
visitActorType
(
self
a
)
:
        
return
Type
(
_actorName
(
self
.
typename
(
a
.
protocol
)
self
.
side
)
ptr
=
True
)
    
def
visitStructType
(
self
s
)
:
        
return
Type
(
self
.
typename
(
s
)
)
    
def
visitUnionType
(
self
u
)
:
        
return
Type
(
self
.
typename
(
u
)
)
    
def
visitArrayType
(
self
a
)
:
        
basecxxtype
=
a
.
basetype
.
accept
(
self
)
        
return
_cxxArrayType
(
basecxxtype
)
    
def
visitShmemType
(
self
s
)
:
        
return
Type
(
self
.
typename
(
s
)
)
    
def
visitByteBufType
(
self
s
)
:
        
return
Type
(
self
.
typename
(
s
)
)
    
def
visitFDType
(
self
s
)
:
        
return
Type
(
self
.
typename
(
s
)
)
    
def
visitEndpointType
(
self
s
)
:
        
return
Type
(
self
.
typename
(
s
)
)
    
def
visitUniquePtrType
(
self
s
)
:
        
return
Type
(
self
.
typename
(
s
)
)
    
def
visitProtocolType
(
self
p
)
:
assert
0
    
def
visitMessageType
(
self
m
)
:
assert
0
    
def
visitVoidType
(
self
v
)
:
assert
0
    
def
visitStateType
(
self
st
)
:
assert
0
def
_cxxBareType
(
ipdltype
side
fq
=
False
)
:
    
return
ipdltype
.
accept
(
_ConvertToCxxType
(
side
fq
)
)
def
_cxxRefType
(
ipdltype
side
)
:
    
t
=
_cxxBareType
(
ipdltype
side
)
    
t
.
ref
=
True
    
return
t
def
_cxxConstRefType
(
ipdltype
side
)
:
    
t
=
_cxxBareType
(
ipdltype
side
)
    
if
ipdltype
.
isIPDL
(
)
and
ipdltype
.
isActor
(
)
:
        
return
t
    
if
ipdltype
.
isIPDL
(
)
and
ipdltype
.
isShmem
(
)
:
        
t
.
ref
=
True
        
return
t
    
if
ipdltype
.
isIPDL
(
)
and
ipdltype
.
isByteBuf
(
)
:
        
t
.
ref
=
True
        
return
t
    
if
ipdltype
.
isIPDL
(
)
and
ipdltype
.
isArray
(
)
:
        
inner
=
_cxxConstRefType
(
ipdltype
.
basetype
side
)
        
t
.
const
=
inner
.
const
or
not
inner
.
ref
        
t
.
ref
=
True
        
return
t
    
if
ipdltype
.
isCxx
(
)
and
ipdltype
.
isMoveonly
(
)
:
        
t
.
ref
=
True
        
return
t
    
if
ipdltype
.
isCxx
(
)
and
ipdltype
.
isRefcounted
(
)
:
        
t
=
t
.
T
        
t
.
ptr
=
True
        
return
t
    
if
ipdltype
.
isUniquePtr
(
)
:
        
t
.
ref
=
True
        
return
t
    
t
.
const
=
True
    
t
.
ref
=
True
    
return
t
def
_cxxTypeCanMoveSend
(
ipdltype
)
:
    
return
ipdltype
.
isUniquePtr
(
)
def
_cxxTypeNeedsMove
(
ipdltype
)
:
    
if
ipdltype
.
isUniquePtr
(
)
:
        
return
True
    
if
ipdltype
.
isCxx
(
)
:
        
return
ipdltype
.
isMoveonly
(
)
    
if
ipdltype
.
isIPDL
(
)
:
        
return
(
ipdltype
.
isArray
(
)
or
                
ipdltype
.
isShmem
(
)
or
                
ipdltype
.
isByteBuf
(
)
or
                
ipdltype
.
isEndpoint
(
)
)
    
return
False
def
_cxxTypeCanMove
(
ipdltype
)
:
    
return
not
(
ipdltype
.
isIPDL
(
)
and
ipdltype
.
isActor
(
)
)
def
_cxxMoveRefType
(
ipdltype
side
)
:
    
t
=
_cxxBareType
(
ipdltype
side
)
    
if
_cxxTypeNeedsMove
(
ipdltype
)
:
        
t
.
rvalref
=
True
        
return
t
    
return
_cxxConstRefType
(
ipdltype
side
)
def
_cxxForceMoveRefType
(
ipdltype
side
)
:
    
assert
_cxxTypeCanMove
(
ipdltype
)
    
t
=
_cxxBareType
(
ipdltype
side
)
    
t
.
rvalref
=
True
    
return
t
def
_cxxPtrToType
(
ipdltype
side
)
:
    
t
=
_cxxBareType
(
ipdltype
side
)
    
if
ipdltype
.
isIPDL
(
)
and
ipdltype
.
isActor
(
)
:
        
t
.
ptr
=
False
        
t
.
ptrptr
=
True
        
return
t
    
t
.
ptr
=
True
    
return
t
def
_cxxConstPtrToType
(
ipdltype
side
)
:
    
t
=
_cxxBareType
(
ipdltype
side
)
    
if
ipdltype
.
isIPDL
(
)
and
ipdltype
.
isActor
(
)
:
        
t
.
ptr
=
False
        
t
.
ptrconstptr
=
True
        
return
t
    
t
.
const
=
True
    
t
.
ptr
=
True
    
return
t
def
_allocMethod
(
ptype
side
)
:
    
return
'
Alloc
'
+
ptype
.
name
(
)
+
side
.
title
(
)
def
_deallocMethod
(
ptype
side
)
:
    
return
'
Dealloc
'
+
ptype
.
name
(
)
+
side
.
title
(
)
class
_HybridDecl
:
    
"
"
"
A
hybrid
decl
stores
both
an
IPDL
type
and
all
the
C
+
+
type
info
needed
by
later
passes
along
with
a
basic
name
for
the
decl
.
"
"
"
    
def
__init__
(
self
ipdltype
name
)
:
        
self
.
ipdltype
=
ipdltype
        
self
.
name
=
name
    
def
isCopyable
(
self
)
:
        
return
not
_cxxTypeNeedsMove
(
self
.
ipdltype
)
    
def
var
(
self
)
:
        
return
ExprVar
(
self
.
name
)
    
def
mayMoveExpr
(
self
)
:
        
if
self
.
isCopyable
(
)
:
            
return
self
.
var
(
)
        
return
ExprMove
(
self
.
var
(
)
)
    
def
bareType
(
self
side
fq
=
False
)
:
        
"
"
"
Return
this
decl
'
s
unqualified
C
+
+
type
.
"
"
"
        
return
_cxxBareType
(
self
.
ipdltype
side
fq
=
fq
)
    
def
refType
(
self
side
)
:
        
"
"
"
Return
this
decl
'
s
C
+
+
type
as
a
'
reference
'
type
which
is
not
necessarily
a
C
+
+
reference
.
"
"
"
        
return
_cxxRefType
(
self
.
ipdltype
side
)
    
def
constRefType
(
self
side
)
:
        
"
"
"
Return
this
decl
'
s
C
+
+
type
as
a
const
'
reference
'
type
.
"
"
"
        
return
_cxxConstRefType
(
self
.
ipdltype
side
)
    
def
rvalueRefType
(
self
side
)
:
        
"
"
"
Return
this
decl
'
s
C
+
+
type
as
an
r
-
value
'
reference
'
type
.
"
"
"
        
return
_cxxMoveRefType
(
self
.
ipdltype
side
)
    
def
ptrToType
(
self
side
)
:
        
return
_cxxPtrToType
(
self
.
ipdltype
side
)
    
def
constPtrToType
(
self
side
)
:
        
return
_cxxConstPtrToType
(
self
.
ipdltype
side
)
    
def
inType
(
self
side
)
:
        
"
"
"
Return
this
decl
'
s
C
+
+
Type
with
inparam
semantics
.
"
"
"
        
if
self
.
ipdltype
.
isIPDL
(
)
and
self
.
ipdltype
.
isActor
(
)
:
            
return
self
.
bareType
(
side
)
        
return
self
.
constRefType
(
side
)
    
def
moveType
(
self
side
)
:
        
"
"
"
Return
this
decl
'
s
C
+
+
Type
with
move
semantics
.
"
"
"
        
if
self
.
ipdltype
.
isIPDL
(
)
and
self
.
ipdltype
.
isActor
(
)
:
            
return
self
.
bareType
(
side
)
        
return
self
.
rvalueRefType
(
side
)
    
def
outType
(
self
side
)
:
        
"
"
"
Return
this
decl
'
s
C
+
+
Type
with
outparam
semantics
.
"
"
"
        
t
=
self
.
bareType
(
side
)
        
if
self
.
ipdltype
.
isIPDL
(
)
and
self
.
ipdltype
.
isActor
(
)
:
            
t
.
ptr
=
False
            
t
.
ptrptr
=
True
            
return
t
        
t
.
ptr
=
True
        
return
t
    
def
forceMoveType
(
self
side
)
:
        
"
"
"
Return
this
decl
'
s
C
+
+
Type
with
forced
move
semantics
.
"
"
"
        
assert
_cxxTypeCanMove
(
self
.
ipdltype
)
        
return
_cxxForceMoveRefType
(
self
.
ipdltype
side
)
class
HasFQName
:
    
def
fqClassName
(
self
)
:
        
return
self
.
decl
.
type
.
fullname
(
)
class
_CompoundTypeComponent
(
_HybridDecl
)
:
    
def
__init__
(
self
ipdltype
name
side
ct
)
:
        
_HybridDecl
.
__init__
(
self
ipdltype
name
)
        
self
.
side
=
side
        
self
.
special
=
_hasVisibleActor
(
ipdltype
)
    
def
bareType
(
self
side
=
None
fq
=
False
)
:
        
return
_HybridDecl
.
bareType
(
self
self
.
side
fq
=
fq
)
    
def
refType
(
self
side
=
None
)
:
        
return
_HybridDecl
.
refType
(
self
self
.
side
)
    
def
constRefType
(
self
side
=
None
)
:
        
return
_HybridDecl
.
constRefType
(
self
self
.
side
)
    
def
ptrToType
(
self
side
=
None
)
:
        
return
_HybridDecl
.
ptrToType
(
self
self
.
side
)
    
def
constPtrToType
(
self
side
=
None
)
:
        
return
_HybridDecl
.
constPtrToType
(
self
self
.
side
)
    
def
inType
(
self
side
=
None
)
:
        
return
_HybridDecl
.
inType
(
self
self
.
side
)
    
def
forceMoveType
(
self
side
=
None
)
:
        
return
_HybridDecl
.
forceMoveType
(
self
self
.
side
)
class
StructDecl
(
ipdl
.
ast
.
StructDecl
HasFQName
)
:
    
staticmethod
    
def
upgrade
(
structDecl
)
:
        
assert
isinstance
(
structDecl
ipdl
.
ast
.
StructDecl
)
        
structDecl
.
__class__
=
StructDecl
class
_StructField
(
_CompoundTypeComponent
)
:
    
def
__init__
(
self
ipdltype
name
sd
side
=
None
)
:
        
self
.
basename
=
name
        
fname
=
name
        
special
=
_hasVisibleActor
(
ipdltype
)
        
if
special
:
            
fname
+
=
side
.
title
(
)
        
_CompoundTypeComponent
.
__init__
(
self
ipdltype
fname
side
sd
)
    
def
getMethod
(
self
thisexpr
=
None
sel
=
'
.
'
)
:
        
meth
=
self
.
var
(
)
        
if
thisexpr
is
not
None
:
            
return
ExprSelect
(
thisexpr
sel
meth
.
name
)
        
return
meth
    
def
refExpr
(
self
thisexpr
=
None
)
:
        
ref
=
self
.
memberVar
(
)
        
if
thisexpr
is
not
None
:
            
ref
=
ExprSelect
(
thisexpr
'
.
'
ref
.
name
)
        
return
ref
    
def
constRefExpr
(
self
thisexpr
=
None
)
:
        
refexpr
=
self
.
refExpr
(
thisexpr
)
        
if
'
Shmem
'
=
=
self
.
ipdltype
.
name
(
)
:
            
refexpr
=
ExprCast
(
refexpr
Type
(
'
Shmem
'
ref
=
True
)
const
=
True
)
        
if
'
ByteBuf
'
=
=
self
.
ipdltype
.
name
(
)
:
            
refexpr
=
ExprCast
(
refexpr
Type
(
'
ByteBuf
'
ref
=
True
)
const
=
True
)
        
if
'
FileDescriptor
'
=
=
self
.
ipdltype
.
name
(
)
:
            
refexpr
=
ExprCast
(
refexpr
Type
(
'
FileDescriptor
'
ref
=
True
)
const
=
True
)
        
return
refexpr
    
def
argVar
(
self
)
:
        
return
ExprVar
(
'
_
'
+
self
.
name
)
    
def
memberVar
(
self
)
:
        
return
ExprVar
(
self
.
name
+
'
_
'
)
class
UnionDecl
(
ipdl
.
ast
.
UnionDecl
HasFQName
)
:
    
def
callType
(
self
var
=
None
)
:
        
func
=
ExprVar
(
'
type
'
)
        
if
var
is
not
None
:
            
func
=
ExprSelect
(
var
'
.
'
func
.
name
)
        
return
ExprCall
(
func
)
    
staticmethod
    
def
upgrade
(
unionDecl
)
:
        
assert
isinstance
(
unionDecl
ipdl
.
ast
.
UnionDecl
)
        
unionDecl
.
__class__
=
UnionDecl
class
_UnionMember
(
_CompoundTypeComponent
)
:
    
"
"
"
Not
in
the
AFL
sense
but
rather
a
member
(
e
.
g
.
|
int
;
|
)
of
an
IPDL
union
type
.
"
"
"
    
def
__init__
(
self
ipdltype
ud
side
=
None
other
=
None
)
:
        
flatname
=
_flatTypeName
(
ipdltype
)
        
special
=
_hasVisibleActor
(
ipdltype
)
        
if
special
:
            
flatname
+
=
side
.
title
(
)
        
_CompoundTypeComponent
.
__init__
(
self
ipdltype
'
V
'
+
flatname
side
ud
)
        
self
.
flattypename
=
flatname
        
if
special
:
            
if
other
is
not
None
:
                
self
.
other
=
other
            
else
:
                
self
.
other
=
_UnionMember
(
ipdltype
ud
_otherSide
(
side
)
self
)
        
self
.
recursive
=
ud
.
decl
.
type
.
mutuallyRecursiveWith
(
ipdltype
)
    
def
enum
(
self
)
:
        
return
'
T
'
+
self
.
flattypename
    
def
enumvar
(
self
)
:
        
return
ExprVar
(
self
.
enum
(
)
)
    
def
internalType
(
self
)
:
        
if
self
.
recursive
:
            
return
self
.
ptrToType
(
)
        
else
:
            
return
self
.
bareType
(
)
    
def
unionType
(
self
)
:
        
"
"
"
Type
used
for
storage
in
generated
C
union
decl
.
"
"
"
        
if
self
.
recursive
:
            
return
self
.
ptrToType
(
)
        
else
:
            
return
Type
(
'
mozilla
:
:
AlignedStorage2
'
T
=
self
.
internalType
(
)
)
    
def
unionValue
(
self
)
:
        
return
ExprSelect
(
ExprVar
(
'
mValue
'
)
'
.
'
self
.
name
)
    
def
typedef
(
self
)
:
        
return
self
.
flattypename
+
'
__tdef
'
    
def
callGetConstPtr
(
self
)
:
        
"
"
"
Return
an
expression
of
type
self
.
constptrToSelfType
(
)
"
"
"
        
return
ExprCall
(
ExprVar
(
self
.
getConstPtrName
(
)
)
)
    
def
callGetPtr
(
self
)
:
        
"
"
"
Return
an
expression
of
type
self
.
ptrToSelfType
(
)
"
"
"
        
return
ExprCall
(
ExprVar
(
self
.
getPtrName
(
)
)
)
    
def
callOperatorEq
(
self
rhs
)
:
        
if
self
.
ipdltype
.
isIPDL
(
)
and
self
.
ipdltype
.
isActor
(
)
:
            
rhs
=
ExprCast
(
rhs
self
.
bareType
(
)
const
=
True
)
        
return
ExprAssn
(
ExprDeref
(
self
.
callGetPtr
(
)
)
rhs
)
    
def
callCtor
(
self
expr
=
None
)
:
        
assert
not
isinstance
(
expr
list
)
        
if
expr
is
None
:
            
args
=
None
        
elif
self
.
ipdltype
.
isIPDL
(
)
and
self
.
ipdltype
.
isActor
(
)
:
            
args
=
[
ExprCast
(
expr
self
.
bareType
(
)
const
=
True
)
]
        
else
:
            
args
=
[
expr
]
        
if
self
.
recursive
:
            
return
ExprAssn
(
self
.
callGetPtr
(
)
                            
ExprNew
(
self
.
bareType
(
self
.
side
)
                                    
args
=
args
)
)
        
else
:
            
return
ExprNew
(
self
.
bareType
(
self
.
side
)
                           
args
=
args
                           
newargs
=
[
ExprVar
(
'
mozilla
:
:
KnownNotNull
'
)
self
.
callGetPtr
(
)
]
)
    
def
callDtor
(
self
)
:
        
if
self
.
recursive
:
            
return
ExprDelete
(
self
.
callGetPtr
(
)
)
        
else
:
            
return
ExprCall
(
                
ExprSelect
(
self
.
callGetPtr
(
)
'
-
>
'
'
~
'
+
self
.
typedef
(
)
)
)
    
def
getTypeName
(
self
)
:
return
'
get_
'
+
self
.
flattypename
    
def
getConstTypeName
(
self
)
:
return
'
get_
'
+
self
.
flattypename
    
def
getOtherTypeName
(
self
)
:
return
'
get_
'
+
self
.
otherflattypename
    
def
getPtrName
(
self
)
:
return
'
ptr_
'
+
self
.
flattypename
    
def
getConstPtrName
(
self
)
:
return
'
constptr_
'
+
self
.
flattypename
    
def
ptrToSelfExpr
(
self
)
:
        
"
"
"
|
*
ptrToSelfExpr
(
)
|
has
type
|
self
.
bareType
(
)
|
"
"
"
        
v
=
self
.
unionValue
(
)
        
if
self
.
recursive
:
            
return
v
        
else
:
            
return
ExprCall
(
ExprSelect
(
v
'
.
'
'
addr
'
)
)
    
def
constptrToSelfExpr
(
self
)
:
        
"
"
"
|
*
constptrToSelfExpr
(
)
|
has
type
|
self
.
constType
(
)
|
"
"
"
        
v
=
self
.
unionValue
(
)
        
if
self
.
recursive
:
            
return
v
        
return
ExprCall
(
ExprSelect
(
v
'
.
'
'
addr
'
)
)
    
def
ptrToInternalType
(
self
)
:
        
t
=
self
.
ptrToType
(
)
        
if
self
.
recursive
:
            
t
.
ref
=
True
        
return
t
    
def
defaultValue
(
self
fq
=
False
)
:
        
if
not
self
.
bareType
(
)
.
hasimplicitcopyctor
:
            
return
None
        
if
self
.
ipdltype
.
isIPDL
(
)
and
self
.
ipdltype
.
isActor
(
)
:
            
return
ExprLiteral
.
NULL
        
return
ExprCall
(
self
.
bareType
(
fq
=
fq
)
)
    
def
getConstValue
(
self
)
:
        
v
=
ExprDeref
(
self
.
callGetConstPtr
(
)
)
        
if
'
ByteBuf
'
=
=
self
.
ipdltype
.
name
(
)
:
            
v
=
ExprCast
(
v
Type
(
'
ByteBuf
'
ref
=
True
)
const
=
True
)
        
if
'
Shmem
'
=
=
self
.
ipdltype
.
name
(
)
:
            
v
=
ExprCast
(
v
Type
(
'
Shmem
'
ref
=
True
)
const
=
True
)
        
if
'
FileDescriptor
'
=
=
self
.
ipdltype
.
name
(
)
:
            
v
=
ExprCast
(
v
Type
(
'
FileDescriptor
'
ref
=
True
)
const
=
True
)
        
return
v
class
MessageDecl
(
ipdl
.
ast
.
MessageDecl
)
:
    
def
baseName
(
self
)
:
        
return
self
.
name
    
def
recvMethod
(
self
)
:
        
name
=
_recvPrefix
(
self
.
decl
.
type
)
+
self
.
baseName
(
)
        
if
self
.
decl
.
type
.
isCtor
(
)
:
            
name
+
=
'
Constructor
'
        
return
name
    
def
sendMethod
(
self
)
:
        
name
=
_sendPrefix
(
self
.
decl
.
type
)
+
self
.
baseName
(
)
        
if
self
.
decl
.
type
.
isCtor
(
)
:
            
name
+
=
'
Constructor
'
        
return
ExprVar
(
name
)
    
def
hasReply
(
self
)
:
        
return
(
self
.
decl
.
type
.
hasReply
(
)
                
or
self
.
decl
.
type
.
isCtor
(
)
                
or
self
.
decl
.
type
.
isDtor
(
)
)
    
def
hasAsyncReturns
(
self
)
:
        
return
(
self
.
decl
.
type
.
isAsync
(
)
and
                
self
.
returns
)
    
def
msgCtorFunc
(
self
)
:
        
return
'
Msg_
%
s
'
%
(
self
.
decl
.
progname
)
    
def
prettyMsgName
(
self
pfx
=
'
'
)
:
        
return
pfx
+
self
.
msgCtorFunc
(
)
    
def
pqMsgCtorFunc
(
self
)
:
        
return
'
%
s
:
:
%
s
'
%
(
self
.
namespace
self
.
msgCtorFunc
(
)
)
    
def
msgId
(
self
)
:
return
self
.
msgCtorFunc
(
)
+
'
__ID
'
    
def
pqMsgId
(
self
)
:
        
return
'
%
s
:
:
%
s
'
%
(
self
.
namespace
self
.
msgId
(
)
)
    
def
replyCtorFunc
(
self
)
:
        
return
'
Reply_
%
s
'
%
(
self
.
decl
.
progname
)
    
def
pqReplyCtorFunc
(
self
)
:
        
return
'
%
s
:
:
%
s
'
%
(
self
.
namespace
self
.
replyCtorFunc
(
)
)
    
def
replyId
(
self
)
:
return
self
.
replyCtorFunc
(
)
+
'
__ID
'
    
def
pqReplyId
(
self
)
:
        
return
'
%
s
:
:
%
s
'
%
(
self
.
namespace
self
.
replyId
(
)
)
    
def
prettyReplyName
(
self
pfx
=
'
'
)
:
        
return
pfx
+
self
.
replyCtorFunc
(
)
    
def
promiseName
(
self
)
:
        
name
=
self
.
baseName
(
)
        
if
self
.
decl
.
type
.
isCtor
(
)
:
            
name
+
=
'
Constructor
'
        
name
+
=
'
Promise
'
        
return
name
    
def
resolverName
(
self
)
:
        
return
self
.
baseName
(
)
+
'
Resolver
'
    
def
actorDecl
(
self
)
:
        
return
self
.
params
[
0
]
    
def
makeCxxParams
(
self
paramsems
=
'
in
'
returnsems
=
'
out
'
                      
side
=
None
implicit
=
True
)
:
        
"
"
"
Return
a
list
of
C
+
+
decls
per
the
spec
'
d
configuration
.
|
params
|
and
|
returns
|
is
the
C
+
+
semantics
of
those
:
'
in
'
'
out
'
or
None
.
"
"
"
        
def
makeDecl
(
d
sems
)
:
            
if
sems
=
=
'
in
'
:
                
return
Decl
(
d
.
inType
(
side
)
d
.
name
)
            
elif
sems
=
=
'
move
'
:
                
return
Decl
(
d
.
moveType
(
side
)
d
.
name
)
            
elif
sems
=
=
'
out
'
:
                
return
Decl
(
d
.
outType
(
side
)
d
.
name
)
            
else
:
                
assert
0
        
def
makeResolverDecl
(
returns
)
:
            
return
Decl
(
Type
(
self
.
resolverName
(
)
rvalref
=
True
)
'
aResolve
'
)
        
def
makeCallbackResolveDecl
(
returns
)
:
            
if
len
(
returns
)
>
1
:
                
resolvetype
=
_tuple
(
[
d
.
bareType
(
side
)
for
d
in
returns
]
)
            
else
:
                
resolvetype
=
returns
[
0
]
.
bareType
(
side
)
            
return
Decl
(
Type
(
"
mozilla
:
:
ipc
:
:
ResolveCallback
"
T
=
resolvetype
rvalref
=
True
)
                        
'
aResolve
'
)
        
def
makeCallbackRejectDecl
(
returns
)
:
            
return
Decl
(
Type
(
"
mozilla
:
:
ipc
:
:
RejectCallback
"
rvalref
=
True
)
'
aReject
'
)
        
cxxparams
=
[
]
        
if
paramsems
is
not
None
:
            
cxxparams
.
extend
(
[
makeDecl
(
d
paramsems
)
for
d
in
self
.
params
]
)
        
if
returnsems
=
=
'
promise
'
and
self
.
returns
:
            
pass
        
elif
returnsems
=
=
'
callback
'
and
self
.
returns
:
            
cxxparams
.
extend
(
[
makeCallbackResolveDecl
(
self
.
returns
)
                              
makeCallbackRejectDecl
(
self
.
returns
)
]
)
        
elif
returnsems
=
=
'
resolver
'
and
self
.
returns
:
            
cxxparams
.
extend
(
[
makeResolverDecl
(
self
.
returns
)
]
)
        
elif
returnsems
is
not
None
:
            
cxxparams
.
extend
(
[
makeDecl
(
r
returnsems
)
for
r
in
self
.
returns
]
)
        
if
not
implicit
and
self
.
decl
.
type
.
hasImplicitActorParam
(
)
:
            
cxxparams
=
cxxparams
[
1
:
]
        
return
cxxparams
    
def
makeCxxArgs
(
self
paramsems
=
'
in
'
retsems
=
'
out
'
retcallsems
=
'
out
'
                    
implicit
=
True
)
:
        
assert
not
retcallsems
or
retsems
        
cxxargs
=
[
]
        
if
paramsems
=
=
'
move
'
:
            
cxxargs
.
extend
(
[
p
.
mayMoveExpr
(
)
for
p
in
self
.
params
]
)
        
elif
paramsems
=
=
'
in
'
:
            
cxxargs
.
extend
(
[
p
.
var
(
)
for
p
in
self
.
params
]
)
        
else
:
            
assert
False
        
for
ret
in
self
.
returns
:
            
if
retsems
=
=
'
in
'
:
                
if
retcallsems
=
=
'
in
'
:
                    
cxxargs
.
append
(
ret
.
var
(
)
)
                
elif
retcallsems
=
=
'
out
'
:
                    
cxxargs
.
append
(
ExprAddrOf
(
ret
.
var
(
)
)
)
                
else
:
                    
assert
0
            
elif
retsems
=
=
'
out
'
:
                
if
retcallsems
=
=
'
in
'
:
                    
cxxargs
.
append
(
ExprDeref
(
ret
.
var
(
)
)
)
                
elif
retcallsems
=
=
'
out
'
:
                    
cxxargs
.
append
(
ret
.
var
(
)
)
                
else
:
                    
assert
0
            
elif
retsems
=
=
'
resolver
'
:
                
pass
        
if
retsems
=
=
'
resolver
'
:
            
cxxargs
.
append
(
ExprMove
(
ExprVar
(
'
resolver
'
)
)
)
        
if
not
implicit
:
            
assert
self
.
decl
.
type
.
hasImplicitActorParam
(
)
            
cxxargs
=
cxxargs
[
1
:
]
        
return
cxxargs
    
staticmethod
    
def
upgrade
(
messageDecl
)
:
        
assert
isinstance
(
messageDecl
ipdl
.
ast
.
MessageDecl
)
        
if
messageDecl
.
decl
.
type
.
hasImplicitActorParam
(
)
:
            
messageDecl
.
params
.
insert
(
                
0
                
_HybridDecl
(
                    
ipdl
.
type
.
ActorType
(
                        
messageDecl
.
decl
.
type
.
constructedType
(
)
)
                    
'
actor
'
)
)
        
messageDecl
.
__class__
=
MessageDecl
def
_usesShmem
(
p
)
:
    
for
md
in
p
.
messageDecls
:
        
for
param
in
md
.
inParams
:
            
if
ipdl
.
type
.
hasshmem
(
param
.
type
)
:
                
return
True
        
for
ret
in
md
.
outParams
:
            
if
ipdl
.
type
.
hasshmem
(
ret
.
type
)
:
                
return
True
    
return
False
def
_subtreeUsesShmem
(
p
)
:
    
if
_usesShmem
(
p
)
:
        
return
True
    
ptype
=
p
.
decl
.
type
    
for
mgd
in
ptype
.
manages
:
        
if
ptype
is
not
mgd
:
            
if
_subtreeUsesShmem
(
mgd
.
_ast
)
:
                
return
True
    
return
False
def
_stateType
(
hasReentrantDelete
)
:
    
if
hasReentrantDelete
:
        
return
Type
(
'
mozilla
:
:
ipc
:
:
ReEntrantDeleteLivenessState
'
)
    
else
:
        
return
Type
(
'
mozilla
:
:
ipc
:
:
LivenessState
'
)
def
_startState
(
hasReentrantDelete
)
:
    
pfx
=
_stateType
(
hasReentrantDelete
)
.
name
+
'
:
:
'
    
return
ExprVar
(
pfx
+
'
Start
'
)
class
Protocol
(
ipdl
.
ast
.
Protocol
)
:
    
def
cxxTypedefs
(
self
)
:
        
return
self
.
decl
.
cxxtypedefs
    
def
managerInterfaceType
(
self
ptr
=
False
)
:
        
return
Type
(
'
mozilla
:
:
ipc
:
:
IProtocol
'
ptr
=
ptr
)
    
def
openedProtocolInterfaceType
(
self
ptr
=
False
)
:
        
return
Type
(
'
mozilla
:
:
ipc
:
:
IToplevelProtocol
'
                    
ptr
=
ptr
)
    
def
_ipdlmgrtype
(
self
)
:
        
assert
1
=
=
len
(
self
.
decl
.
type
.
managers
)
        
for
mgr
in
self
.
decl
.
type
.
managers
:
            
return
mgr
    
def
managerActorType
(
self
side
ptr
=
False
)
:
        
return
Type
(
_actorName
(
self
.
_ipdlmgrtype
(
)
.
name
(
)
side
)
                    
ptr
=
ptr
)
    
def
unregisterMethod
(
self
actorThis
=
None
)
:
        
if
actorThis
is
not
None
:
            
return
ExprSelect
(
actorThis
'
-
>
'
'
Unregister
'
)
        
return
ExprVar
(
'
Unregister
'
)
    
def
removeManageeMethod
(
self
)
:
        
return
ExprVar
(
'
RemoveManagee
'
)
    
def
otherPidMethod
(
self
)
:
        
return
ExprVar
(
'
OtherPid
'
)
    
def
callOtherPid
(
self
actorThis
=
None
)
:
        
fn
=
self
.
otherPidMethod
(
)
        
if
actorThis
is
not
None
:
            
fn
=
ExprSelect
(
actorThis
'
-
>
'
fn
.
name
)
        
return
ExprCall
(
fn
)
    
def
getChannelMethod
(
self
)
:
        
return
ExprVar
(
'
GetIPCChannel
'
)
    
def
callGetChannel
(
self
actorThis
=
None
)
:
        
fn
=
self
.
getChannelMethod
(
)
        
if
actorThis
is
not
None
:
            
fn
=
ExprSelect
(
actorThis
'
-
>
'
fn
.
name
)
        
return
ExprCall
(
fn
)
    
def
processingErrorVar
(
self
)
:
        
assert
self
.
decl
.
type
.
isToplevel
(
)
        
return
ExprVar
(
'
ProcessingError
'
)
    
def
shouldContinueFromTimeoutVar
(
self
)
:
        
assert
self
.
decl
.
type
.
isToplevel
(
)
        
return
ExprVar
(
'
ShouldContinueFromReplyTimeout
'
)
    
def
enteredCxxStackVar
(
self
)
:
        
assert
self
.
decl
.
type
.
isToplevel
(
)
        
return
ExprVar
(
'
EnteredCxxStack
'
)
    
def
exitedCxxStackVar
(
self
)
:
        
assert
self
.
decl
.
type
.
isToplevel
(
)
        
return
ExprVar
(
'
ExitedCxxStack
'
)
    
def
enteredCallVar
(
self
)
:
        
assert
self
.
decl
.
type
.
isToplevel
(
)
        
return
ExprVar
(
'
EnteredCall
'
)
    
def
exitedCallVar
(
self
)
:
        
assert
self
.
decl
.
type
.
isToplevel
(
)
        
return
ExprVar
(
'
ExitedCall
'
)
    
def
routingId
(
self
actorThis
=
None
)
:
        
if
self
.
decl
.
type
.
isToplevel
(
)
:
            
return
ExprVar
(
'
MSG_ROUTING_CONTROL
'
)
        
if
actorThis
is
not
None
:
            
return
ExprCall
(
ExprSelect
(
actorThis
'
-
>
'
'
Id
'
)
)
        
return
ExprCall
(
ExprVar
(
'
Id
'
)
)
    
def
stateVar
(
self
)
:
        
return
ExprVar
(
'
mLivenessState
'
)
    
def
fqStateType
(
self
)
:
        
return
_stateType
(
self
.
decl
.
type
.
hasReentrantDelete
)
    
def
startState
(
self
)
:
        
return
_startState
(
self
.
decl
.
type
.
hasReentrantDelete
)
    
def
deadState
(
self
)
:
        
pfx
=
self
.
fqStateType
(
)
.
name
+
'
:
:
'
        
return
ExprVar
(
pfx
+
'
Dead
'
)
    
def
dyingState
(
self
)
:
        
assert
self
.
decl
.
type
.
hasReentrantDelete
        
pfx
=
self
.
fqStateType
(
)
.
name
+
'
:
:
'
        
return
ExprVar
(
pfx
+
'
Dying
'
)
    
def
managerVar
(
self
thisexpr
=
None
)
:
        
assert
thisexpr
is
not
None
or
not
self
.
decl
.
type
.
isToplevel
(
)
        
mvar
=
ExprCall
(
ExprVar
(
'
Manager
'
)
args
=
[
]
)
        
if
thisexpr
is
not
None
:
            
mvar
=
ExprCall
(
ExprSelect
(
thisexpr
'
-
>
'
'
Manager
'
)
args
=
[
]
)
        
return
mvar
    
def
managedCxxType
(
self
actortype
side
)
:
        
assert
self
.
decl
.
type
.
isManagerOf
(
actortype
)
        
return
Type
(
_actorName
(
actortype
.
name
(
)
side
)
ptr
=
True
)
    
def
managedMethod
(
self
actortype
side
)
:
        
assert
self
.
decl
.
type
.
isManagerOf
(
actortype
)
        
return
ExprVar
(
'
Managed
'
+
_actorName
(
actortype
.
name
(
)
side
)
)
    
def
managedVar
(
self
actortype
side
)
:
        
assert
self
.
decl
.
type
.
isManagerOf
(
actortype
)
        
return
ExprVar
(
'
mManaged
'
+
_actorName
(
actortype
.
name
(
)
side
)
)
    
def
managedVarType
(
self
actortype
side
const
=
False
ref
=
False
)
:
        
assert
self
.
decl
.
type
.
isManagerOf
(
actortype
)
        
return
_cxxManagedContainerType
(
Type
(
_actorName
(
actortype
.
name
(
)
side
)
)
                                        
const
=
const
ref
=
ref
)
    
def
subtreeUsesShmem
(
self
)
:
        
return
_subtreeUsesShmem
(
self
)
    
staticmethod
    
def
upgrade
(
protocol
)
:
        
assert
isinstance
(
protocol
ipdl
.
ast
.
Protocol
)
        
protocol
.
__class__
=
Protocol
class
TranslationUnit
(
ipdl
.
ast
.
TranslationUnit
)
:
    
staticmethod
    
def
upgrade
(
tu
)
:
        
assert
isinstance
(
tu
ipdl
.
ast
.
TranslationUnit
)
        
tu
.
__class__
=
TranslationUnit
class
_DecorateWithCxxStuff
(
ipdl
.
ast
.
Visitor
)
:
    
"
"
"
Phase
1
of
lowering
:
decorate
the
IPDL
AST
with
information
relevant
to
C
+
+
code
generation
.
This
pass
results
in
an
AST
that
is
a
poor
man
'
s
"
IR
"
;
in
reality
a
"
hybrid
"
AST
mainly
consisting
of
IPDL
nodes
with
new
C
+
+
info
along
with
some
new
IPDL
/
C
+
+
nodes
that
are
tuned
for
C
+
+
codegen
.
"
"
"
    
def
__init__
(
self
)
:
        
self
.
visitedTus
=
set
(
)
        
self
.
typedefs
=
[
]
        
self
.
typedefSet
=
set
(
[
Typedef
(
Type
(
'
mozilla
:
:
ipc
:
:
ActorHandle
'
)
                                       
'
ActorHandle
'
)
                               
Typedef
(
Type
(
'
base
:
:
ProcessId
'
)
                                       
'
ProcessId
'
)
                               
Typedef
(
Type
(
'
mozilla
:
:
ipc
:
:
ProtocolId
'
)
                                       
'
ProtocolId
'
)
                               
Typedef
(
Type
(
'
mozilla
:
:
ipc
:
:
Transport
'
)
                                       
'
Transport
'
)
                               
Typedef
(
Type
(
'
mozilla
:
:
ipc
:
:
Endpoint
'
)
                                       
'
Endpoint
'
[
'
FooSide
'
]
)
                               
Typedef
(
Type
(
'
mozilla
:
:
ipc
:
:
TransportDescriptor
'
)
                                       
'
TransportDescriptor
'
)
                               
Typedef
(
Type
(
'
mozilla
:
:
UniquePtr
'
)
                                       
'
UniquePtr
'
[
'
T
'
]
)
                               
Typedef
(
Type
(
'
mozilla
:
:
ipc
:
:
ResponseRejectReason
'
)
                                       
'
ResponseRejectReason
'
)
]
)
        
self
.
protocolName
=
None
    
def
visitTranslationUnit
(
self
tu
)
:
        
if
tu
not
in
self
.
visitedTus
:
            
self
.
visitedTus
.
add
(
tu
)
            
ipdl
.
ast
.
Visitor
.
visitTranslationUnit
(
self
tu
)
            
if
not
isinstance
(
tu
TranslationUnit
)
:
                
TranslationUnit
.
upgrade
(
tu
)
            
self
.
typedefs
[
:
]
=
sorted
(
list
(
self
.
typedefSet
)
)
    
def
visitInclude
(
self
inc
)
:
        
if
inc
.
tu
.
filetype
=
=
'
header
'
:
            
inc
.
tu
.
accept
(
self
)
    
def
visitProtocol
(
self
pro
)
:
        
self
.
protocolName
=
pro
.
name
        
pro
.
decl
.
cxxtypedefs
=
self
.
typedefs
        
Protocol
.
upgrade
(
pro
)
        
return
ipdl
.
ast
.
Visitor
.
visitProtocol
(
self
pro
)
    
def
visitUsingStmt
(
self
using
)
:
        
if
using
.
decl
.
fullname
is
not
None
:
            
self
.
typedefSet
.
add
(
Typedef
(
Type
(
using
.
decl
.
fullname
)
                                        
using
.
decl
.
shortname
)
)
    
def
visitStructDecl
(
self
sd
)
:
        
if
not
isinstance
(
sd
StructDecl
)
:
            
sd
.
decl
.
special
=
False
            
newfields
=
[
]
            
for
f
in
sd
.
fields
:
                
ftype
=
f
.
decl
.
type
                
if
_hasVisibleActor
(
ftype
)
:
                    
sd
.
decl
.
special
=
True
                    
newfields
.
append
(
_StructField
(
ftype
f
.
name
sd
                                                  
side
=
'
parent
'
)
)
                    
newfields
.
append
(
_StructField
(
ftype
f
.
name
sd
                                                  
side
=
'
child
'
)
)
                
else
:
                    
newfields
.
append
(
_StructField
(
ftype
f
.
name
sd
)
)
            
sd
.
fields
=
newfields
            
StructDecl
.
upgrade
(
sd
)
        
if
sd
.
decl
.
fullname
is
not
None
:
            
self
.
typedefSet
.
add
(
Typedef
(
Type
(
sd
.
fqClassName
(
)
)
sd
.
name
)
)
    
def
visitUnionDecl
(
self
ud
)
:
        
ud
.
decl
.
special
=
False
        
newcomponents
=
[
]
        
for
ctype
in
ud
.
decl
.
type
.
components
:
            
if
_hasVisibleActor
(
ctype
)
:
                
ud
.
decl
.
special
=
True
                
newcomponents
.
append
(
_UnionMember
(
ctype
ud
side
=
'
parent
'
)
)
                
newcomponents
.
append
(
_UnionMember
(
ctype
ud
side
=
'
child
'
)
)
            
else
:
                
newcomponents
.
append
(
_UnionMember
(
ctype
ud
)
)
        
ud
.
components
=
newcomponents
        
UnionDecl
.
upgrade
(
ud
)
        
if
ud
.
decl
.
fullname
is
not
None
:
            
self
.
typedefSet
.
add
(
Typedef
(
Type
(
ud
.
fqClassName
(
)
)
ud
.
name
)
)
    
def
visitDecl
(
self
decl
)
:
        
return
_HybridDecl
(
decl
.
type
decl
.
progname
)
    
def
visitMessageDecl
(
self
md
)
:
        
md
.
namespace
=
self
.
protocolName
        
md
.
params
=
[
param
.
accept
(
self
)
for
param
in
md
.
inParams
]
        
md
.
returns
=
[
ret
.
accept
(
self
)
for
ret
in
md
.
outParams
]
        
MessageDecl
.
upgrade
(
md
)
def
msgenums
(
protocol
pretty
=
False
)
:
    
msgenum
=
TypeEnum
(
'
MessageType
'
)
    
msgstart
=
_messageStartName
(
protocol
.
decl
.
type
)
+
'
<
<
16
'
    
msgenum
.
addId
(
protocol
.
name
+
'
Start
'
msgstart
)
    
for
md
in
protocol
.
messageDecls
:
        
msgenum
.
addId
(
md
.
prettyMsgName
(
)
if
pretty
else
md
.
msgId
(
)
)
        
if
md
.
hasReply
(
)
:
            
msgenum
.
addId
(
md
.
prettyReplyName
(
)
if
pretty
else
md
.
replyId
(
)
)
    
msgenum
.
addId
(
protocol
.
name
+
'
End
'
)
    
return
msgenum
class
_GenerateProtocolCode
(
ipdl
.
ast
.
Visitor
)
:
    
'
'
'
Creates
code
common
to
both
the
parent
and
child
actors
.
'
'
'
    
def
__init__
(
self
)
:
        
self
.
protocol
=
None
        
self
.
hdrfile
=
None
        
self
.
cppfile
=
None
        
self
.
cppIncludeHeaders
=
[
]
        
self
.
structUnionDefns
=
[
]
        
self
.
funcDefns
=
[
]
    
def
lower
(
self
tu
cxxHeaderFile
cxxFile
segmentcapacitydict
)
:
        
self
.
protocol
=
tu
.
protocol
        
self
.
hdrfile
=
cxxHeaderFile
        
self
.
cppfile
=
cxxFile
        
self
.
segmentcapacitydict
=
segmentcapacitydict
        
tu
.
accept
(
self
)
    
def
visitTranslationUnit
(
self
tu
)
:
        
hf
=
self
.
hdrfile
        
hf
.
addthing
(
_DISCLAIMER
)
        
hf
.
addthings
(
_includeGuardStart
(
hf
)
)
        
hf
.
addthing
(
Whitespace
.
NL
)
        
for
inc
in
builtinHeaderIncludes
:
            
self
.
visitBuiltinCxxInclude
(
inc
)
        
typesToIncludes
=
{
}
        
for
using
in
tu
.
using
:
            
typestr
=
str
(
using
.
type
.
spec
)
            
if
typestr
not
in
typesToIncludes
:
                
typesToIncludes
[
typestr
]
=
using
.
header
            
else
:
                
assert
typesToIncludes
[
typestr
]
=
=
using
.
header
        
aggregateTypeIncludes
=
set
(
)
        
for
su
in
tu
.
structsAndUnions
:
            
typedeps
=
_ComputeTypeDeps
(
su
.
decl
.
type
True
)
            
if
isinstance
(
su
ipdl
.
ast
.
StructDecl
)
:
                
for
f
in
su
.
fields
:
                    
f
.
ipdltype
.
accept
(
typedeps
)
            
elif
isinstance
(
su
ipdl
.
ast
.
UnionDecl
)
:
                
for
c
in
su
.
components
:
                    
c
.
ipdltype
.
accept
(
typedeps
)
            
for
typename
in
[
t
.
fromtype
.
name
for
t
in
typedeps
.
usingTypedefs
]
:
                
if
typename
in
typesToIncludes
:
                    
aggregateTypeIncludes
.
add
(
typesToIncludes
[
typename
]
)
        
if
len
(
aggregateTypeIncludes
)
!
=
0
:
            
hf
.
addthing
(
Whitespace
.
NL
)
            
hf
.
addthings
(
[
Whitespace
(
"
/
/
Headers
for
typedefs
"
)
Whitespace
.
NL
]
)
            
for
headername
in
sorted
(
iter
(
aggregateTypeIncludes
)
)
:
                
hf
.
addthing
(
CppDirective
(
'
include
'
'
"
'
+
headername
+
'
"
'
)
)
        
for
cxxInc
in
tu
.
cxxIncludes
:
            
cxxInc
.
accept
(
self
)
        
for
inc
in
tu
.
includes
:
            
inc
.
accept
(
self
)
        
self
.
generateStructsAndUnions
(
tu
)
        
for
using
in
tu
.
builtinUsing
:
            
using
.
accept
(
self
)
        
for
using
in
tu
.
using
:
            
using
.
accept
(
self
)
        
if
tu
.
protocol
:
            
tu
.
protocol
.
accept
(
self
)
        
if
tu
.
filetype
=
=
'
header
'
:
            
self
.
cppIncludeHeaders
.
append
(
_ipdlhHeaderName
(
tu
)
+
'
.
h
'
)
        
hf
.
addthing
(
Whitespace
.
NL
)
        
hf
.
addthings
(
_includeGuardEnd
(
hf
)
)
        
cf
=
self
.
cppfile
        
cf
.
addthings
(
(
            
[
_DISCLAIMER
Whitespace
.
NL
]
            
+
[
CppDirective
(
'
include
'
'
"
'
+
h
+
'
"
'
)
                
for
h
in
self
.
cppIncludeHeaders
]
            
+
[
Whitespace
.
NL
]
        
)
)
        
if
self
.
protocol
:
            
ns
=
Namespace
(
self
.
protocol
.
name
)
            
cf
.
addthing
(
_putInNamespaces
(
ns
self
.
protocol
.
namespaces
)
)
            
ns
.
addstmts
(
(
[
Whitespace
.
NL
]
                         
+
self
.
funcDefns
                         
+
[
Whitespace
.
NL
]
)
)
        
cf
.
addthings
(
self
.
structUnionDefns
)
    
def
visitBuiltinCxxInclude
(
self
inc
)
:
        
self
.
hdrfile
.
addthing
(
CppDirective
(
'
include
'
'
"
'
+
inc
.
file
+
'
"
'
)
)
    
def
visitCxxInclude
(
self
inc
)
:
        
self
.
cppIncludeHeaders
.
append
(
inc
.
file
)
    
def
visitInclude
(
self
inc
)
:
        
if
inc
.
tu
.
filetype
=
=
'
header
'
:
            
self
.
hdrfile
.
addthing
(
CppDirective
(
                
'
include
'
'
"
'
+
_ipdlhHeaderName
(
inc
.
tu
)
+
'
.
h
"
'
)
)
        
else
:
            
self
.
cppIncludeHeaders
+
=
[
                
_protocolHeaderName
(
inc
.
tu
.
protocol
'
parent
'
)
+
'
.
h
'
                
_protocolHeaderName
(
inc
.
tu
.
protocol
'
child
'
)
+
'
.
h
'
            
]
    
def
generateStructsAndUnions
(
self
tu
)
:
        
'
'
'
Generate
the
definitions
for
all
structs
and
unions
.
This
will
        
re
-
order
the
declarations
if
needed
in
the
C
+
+
code
such
that
        
dependencies
have
already
been
defined
.
'
'
'
        
decls
=
OrderedDict
(
)
        
for
su
in
tu
.
structsAndUnions
:
            
if
isinstance
(
su
StructDecl
)
:
                
which
=
'
struct
'
                
forwarddecls
fulldecltypes
cls
=
_generateCxxStruct
(
su
)
                
traitsdecl
traitsdefns
=
_ParamTraits
.
structPickling
(
su
.
decl
.
type
)
            
else
:
                
assert
isinstance
(
su
UnionDecl
)
                
which
=
'
union
'
                
forwarddecls
fulldecltypes
cls
=
_generateCxxUnion
(
su
)
                
traitsdecl
traitsdefns
=
_ParamTraits
.
unionPickling
(
su
.
decl
.
type
)
            
clsdecl
methoddefns
=
_splitClassDeclDefn
(
cls
)
            
decls
[
su
.
decl
.
type
]
=
(
                
fulldecltypes
                
[
Whitespace
.
NL
]
                
+
forwarddecls
                
+
[
Whitespace
(
"
"
"
/
/
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
/
/
Declaration
of
the
IPDL
type
|
%
s
%
s
|
/
/
"
"
"
%
(
which
su
.
name
)
)
                    
_putInNamespaces
(
clsdecl
su
.
namespaces
)
                
]
                
+
[
Whitespace
.
NL
                    
traitsdecl
]
)
            
self
.
structUnionDefns
.
extend
(
[
                
Whitespace
(
"
"
"
/
/
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
/
/
Method
definitions
for
the
IPDL
type
|
%
s
%
s
|
/
/
"
"
"
%
(
which
su
.
name
)
)
                
_putInNamespaces
(
methoddefns
su
.
namespaces
)
                
Whitespace
.
NL
                
traitsdefns
            
]
)
        
def
gen_struct
(
deps
defn
)
:
            
for
dep
in
deps
:
                
if
dep
in
decls
:
                    
d
t
=
decls
[
dep
]
                    
del
decls
[
dep
]
                    
gen_struct
(
d
t
)
            
self
.
hdrfile
.
addthings
(
defn
)
        
while
len
(
decls
)
>
0
:
            
_
(
d
t
)
=
decls
.
popitem
(
False
)
            
gen_struct
(
d
t
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
cppIncludeHeaders
.
append
(
_protocolHeaderName
(
self
.
protocol
'
'
)
+
'
.
h
'
)
        
self
.
hdrfile
.
addthings
(
[
            
Whitespace
.
NL
            
_makeForwardDeclForActor
(
p
.
decl
.
type
'
Parent
'
)
            
_makeForwardDeclForActor
(
p
.
decl
.
type
'
Child
'
)
        
]
)
        
self
.
hdrfile
.
addthing
(
Whitespace
(
"
"
"
/
/
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
/
/
Code
common
to
%
sChild
and
%
sParent
/
/
"
"
"
%
(
p
.
name
p
.
name
)
)
)
        
ns
=
Namespace
(
self
.
protocol
.
name
)
        
self
.
hdrfile
.
addthing
(
_putInNamespaces
(
ns
p
.
namespaces
)
)
        
ns
.
addstmt
(
Whitespace
.
NL
)
        
edecl
edefn
=
_splitFuncDeclDefn
(
self
.
genEndpointFunc
(
)
)
        
ns
.
addstmts
(
[
edecl
Whitespace
.
NL
]
)
        
self
.
funcDefns
.
append
(
edefn
)
        
msgenum
=
msgenums
(
self
.
protocol
)
        
ns
.
addstmts
(
[
StmtDecl
(
Decl
(
msgenum
'
'
)
)
Whitespace
.
NL
]
)
        
for
md
in
p
.
messageDecls
:
            
decls
=
[
]
            
name
=
'
%
s
:
:
%
s
'
%
(
md
.
namespace
md
.
decl
.
progname
)
            
segmentcapacity
=
self
.
segmentcapacitydict
.
get
(
name
0
)
            
mfDecl
mfDefn
=
_splitFuncDeclDefn
(
                
_generateMessageConstructor
(
md
segmentcapacity
p
                                            
forReply
=
False
)
)
            
decls
.
append
(
mfDecl
)
            
self
.
funcDefns
.
append
(
mfDefn
)
            
if
md
.
hasReply
(
)
:
                
rfDecl
rfDefn
=
_splitFuncDeclDefn
(
                    
_generateMessageConstructor
(
md
0
p
forReply
=
True
)
)
                
decls
.
append
(
rfDecl
)
                
self
.
funcDefns
.
append
(
rfDefn
)
            
decls
.
append
(
Whitespace
.
NL
)
            
ns
.
addstmts
(
decls
)
        
ns
.
addstmts
(
[
Whitespace
.
NL
Whitespace
.
NL
]
)
    
def
genEndpointFunc
(
self
)
:
        
p
=
self
.
protocol
.
decl
.
type
        
tparent
=
_cxxBareType
(
ActorType
(
p
)
'
Parent
'
fq
=
True
)
        
tchild
=
_cxxBareType
(
ActorType
(
p
)
'
Child
'
fq
=
True
)
        
methodvar
=
ExprVar
(
'
CreateEndpoints
'
)
        
rettype
=
Type
.
NSRESULT
        
parentpidvar
=
ExprVar
(
'
aParentDestPid
'
)
        
childpidvar
=
ExprVar
(
'
aChildDestPid
'
)
        
parentvar
=
ExprVar
(
'
aParent
'
)
        
childvar
=
ExprVar
(
'
aChild
'
)
        
openfunc
=
MethodDefn
(
MethodDecl
(
            
methodvar
.
name
            
params
=
[
Decl
(
Type
(
'
base
:
:
ProcessId
'
)
parentpidvar
.
name
)
                    
Decl
(
Type
(
'
base
:
:
ProcessId
'
)
childpidvar
.
name
)
                    
Decl
(
Type
(
'
mozilla
:
:
ipc
:
:
Endpoint
<
'
+
tparent
.
name
+
'
>
'
ptr
=
True
)
                         
parentvar
.
name
)
                    
Decl
(
Type
(
'
mozilla
:
:
ipc
:
:
Endpoint
<
'
+
tchild
.
name
+
'
>
'
ptr
=
True
)
                         
childvar
.
name
)
]
            
ret
=
rettype
)
)
        
openfunc
.
addstmt
(
StmtReturn
(
ExprCall
(
            
ExprVar
(
'
mozilla
:
:
ipc
:
:
CreateEndpoints
'
)
            
args
=
[
_backstagePass
(
)
                  
parentpidvar
childpidvar
                  
parentvar
childvar
                  
]
)
)
)
        
return
openfunc
def
_generateMessageConstructor
(
md
segmentSize
protocol
forReply
=
False
)
:
    
if
forReply
:
        
clsname
=
md
.
replyCtorFunc
(
)
        
msgid
=
md
.
replyId
(
)
        
replyEnum
=
'
REPLY
'
    
else
:
        
clsname
=
md
.
msgCtorFunc
(
)
        
msgid
=
md
.
msgId
(
)
        
replyEnum
=
'
NOT_REPLY
'
    
nested
=
md
.
decl
.
type
.
nested
    
prio
=
md
.
decl
.
type
.
prio
    
compress
=
md
.
decl
.
type
.
compress
    
routingId
=
ExprVar
(
'
routingId
'
)
    
func
=
FunctionDefn
(
FunctionDecl
(
        
clsname
        
params
=
[
Decl
(
Type
(
'
int32_t
'
)
routingId
.
name
)
]
        
ret
=
Type
(
'
IPC
:
:
Message
'
ptr
=
True
)
)
)
    
if
compress
=
=
'
compress
'
:
        
compression
=
'
COMPRESSION_ENABLED
'
    
elif
compress
:
        
assert
compress
=
=
'
compressall
'
        
compression
=
'
COMPRESSION_ALL
'
    
else
:
        
compression
=
'
COMPRESSION_NONE
'
    
if
nested
=
=
ipdl
.
ast
.
NOT_NESTED
:
        
nestedEnum
=
'
NOT_NESTED
'
    
elif
nested
=
=
ipdl
.
ast
.
INSIDE_SYNC_NESTED
:
        
nestedEnum
=
'
NESTED_INSIDE_SYNC
'
    
else
:
        
assert
nested
=
=
ipdl
.
ast
.
INSIDE_CPOW_NESTED
        
nestedEnum
=
'
NESTED_INSIDE_CPOW
'
    
if
prio
=
=
ipdl
.
ast
.
NORMAL_PRIORITY
:
        
prioEnum
=
'
NORMAL_PRIORITY
'
    
elif
prio
=
=
ipdl
.
ast
.
INPUT_PRIORITY
:
        
prioEnum
=
'
INPUT_PRIORITY
'
    
else
:
        
prioEnum
=
'
HIGH_PRIORITY
'
    
if
md
.
decl
.
type
.
isSync
(
)
:
        
syncEnum
=
'
SYNC
'
    
else
:
        
syncEnum
=
'
ASYNC
'
    
if
md
.
decl
.
type
.
isInterrupt
(
)
:
        
interruptEnum
=
'
INTERRUPT
'
    
else
:
        
interruptEnum
=
'
NOT_INTERRUPT
'
    
if
md
.
decl
.
type
.
isCtor
(
)
:
        
ctorEnum
=
'
CONSTRUCTOR
'
    
else
:
        
ctorEnum
=
'
NOT_CONSTRUCTOR
'
    
def
messageEnum
(
valname
)
:
        
return
ExprVar
(
'
IPC
:
:
Message
:
:
'
+
valname
)
    
flags
=
ExprCall
(
ExprVar
(
'
IPC
:
:
Message
:
:
HeaderFlags
'
)
                     
args
=
[
messageEnum
(
nestedEnum
)
                           
messageEnum
(
prioEnum
)
                           
messageEnum
(
compression
)
                           
messageEnum
(
ctorEnum
)
                           
messageEnum
(
syncEnum
)
                           
messageEnum
(
interruptEnum
)
                           
messageEnum
(
replyEnum
)
]
)
    
segmentSize
=
int
(
segmentSize
)
    
if
segmentSize
:
        
func
.
addstmt
(
            
StmtReturn
(
ExprNew
(
Type
(
'
IPC
:
:
Message
'
)
                               
args
=
[
routingId
                                     
ExprVar
(
msgid
)
                                     
ExprLiteral
.
Int
(
int
(
segmentSize
)
)
                                     
flags
                                     
ExprLiteral
.
TRUE
]
)
)
)
    
else
:
        
func
.
addstmt
(
            
StmtReturn
(
ExprCall
(
ExprVar
(
'
IPC
:
:
Message
:
:
IPDLMessage
'
)
                                
args
=
[
routingId
                                      
ExprVar
(
msgid
)
                                      
flags
]
)
)
)
    
return
func
class
_ParamTraits
(
)
:
    
var
=
ExprVar
(
'
aVar
'
)
    
msgvar
=
ExprVar
(
'
aMsg
'
)
    
itervar
=
ExprVar
(
'
aIter
'
)
    
actor
=
ExprVar
(
'
aActor
'
)
    
classmethod
    
def
ifsideis
(
cls
side
then
els
=
None
)
:
        
cxxside
=
ExprVar
(
'
mozilla
:
:
ipc
:
:
ChildSide
'
)
        
if
side
=
=
'
parent
'
:
            
cxxside
=
ExprVar
(
'
mozilla
:
:
ipc
:
:
ParentSide
'
)
        
ifstmt
=
StmtIf
(
ExprBinary
(
cxxside
'
=
=
'
                                   
ExprCall
(
ExprSelect
(
cls
.
actor
'
-
>
'
'
GetSide
'
)
)
)
)
        
ifstmt
.
addifstmt
(
then
)
        
if
els
is
not
None
:
            
ifstmt
.
addelsestmt
(
els
)
        
return
ifstmt
    
classmethod
    
def
fatalError
(
cls
reason
)
:
        
return
StmtExpr
(
ExprCall
(
ExprSelect
(
cls
.
actor
'
-
>
'
'
FatalError
'
)
                                 
args
=
[
ExprLiteral
.
String
(
reason
)
]
)
)
    
classmethod
    
def
write
(
cls
var
msgvar
actor
)
:
        
return
ExprCall
(
ExprVar
(
'
WriteIPDLParam
'
)
args
=
[
msgvar
actor
var
]
)
    
classmethod
    
def
checkedWrite
(
cls
ipdltype
var
msgvar
sentinelKey
actor
)
:
        
assert
sentinelKey
        
block
=
Block
(
)
        
if
ipdltype
and
ipdltype
.
isIPDL
(
)
and
ipdltype
.
isActor
(
)
and
not
ipdltype
.
nullable
:
            
block
.
addstmt
(
_abortIfFalse
(
var
'
NULL
actor
value
passed
to
non
-
nullable
param
'
)
)
        
block
.
addstmts
(
[
            
StmtExpr
(
cls
.
write
(
var
msgvar
actor
)
)
            
Whitespace
(
'
/
/
Sentinel
=
'
+
repr
(
sentinelKey
)
+
'
\
n
'
indent
=
True
)
            
StmtExpr
(
ExprCall
(
ExprSelect
(
msgvar
'
-
>
'
'
WriteSentinel
'
)
                              
args
=
[
ExprLiteral
.
Int
(
hashfunc
(
sentinelKey
)
)
]
)
)
        
]
)
        
return
block
    
classmethod
    
def
checkedRead
(
cls
ipdltype
var
                    
msgvar
itervar
errfn
                    
paramtype
sentinelKey
                    
errfnSentinel
actor
)
:
        
block
=
Block
(
)
        
ifbad
=
StmtIf
(
ExprNot
(
ExprCall
(
ExprVar
(
'
ReadIPDLParam
'
)
                                        
args
=
[
msgvar
itervar
actor
var
]
)
)
)
        
if
not
isinstance
(
paramtype
list
)
:
            
paramtype
=
[
'
Error
deserializing
'
+
paramtype
]
        
ifbad
.
addifstmts
(
errfn
(
*
paramtype
)
)
        
block
.
addstmt
(
ifbad
)
        
if
ipdltype
and
ipdltype
.
isIPDL
(
)
and
ipdltype
.
isActor
(
)
and
not
ipdltype
.
nullable
:
            
ifnull
=
StmtIf
(
ExprNot
(
ExprDeref
(
var
)
)
)
            
ifnull
.
addifstmts
(
errfn
(
*
paramtype
)
)
            
block
.
addstmt
(
ifnull
)
        
assert
sentinelKey
        
block
.
addstmt
(
Whitespace
(
'
/
/
Sentinel
=
'
+
repr
(
sentinelKey
)
+
'
\
n
'
                                 
indent
=
True
)
)
        
read
=
ExprCall
(
ExprSelect
(
msgvar
'
-
>
'
'
ReadSentinel
'
)
                        
args
=
[
itervar
ExprLiteral
.
Int
(
hashfunc
(
sentinelKey
)
)
]
)
        
ifsentinel
=
StmtIf
(
ExprNot
(
read
)
)
        
ifsentinel
.
addifstmts
(
errfnSentinel
(
*
paramtype
)
)
        
block
.
addstmt
(
ifsentinel
)
        
return
block
    
classmethod
    
def
_checkedRead
(
cls
ipdltype
var
sentinelKey
what
)
:
        
def
errfn
(
msg
)
:
            
return
[
cls
.
fatalError
(
msg
)
StmtReturn
.
FALSE
]
        
return
cls
.
checkedRead
(
            
ipdltype
var
cls
.
msgvar
cls
.
itervar
            
errfn
=
errfn
            
paramtype
=
what
            
sentinelKey
=
sentinelKey
            
errfnSentinel
=
errfnSentinel
(
)
            
actor
=
cls
.
actor
)
    
classmethod
    
def
generateDecl
(
cls
fortype
write
read
constin
=
True
)
:
        
pt
=
Class
(
'
IPDLParamTraits
'
                   
specializes
=
Type
(
fortype
.
name
                                    
T
=
fortype
.
T
                                    
inner
=
fortype
.
inner
)
                   
struct
=
True
)
        
pt
.
addstmt
(
Typedef
(
fortype
'
paramType
'
)
)
        
iprotocoltype
=
Type
(
'
mozilla
:
:
ipc
:
:
IProtocol
'
ptr
=
True
)
        
intype
=
Type
(
'
paramType
'
ref
=
True
const
=
constin
)
        
writemthd
=
MethodDefn
(
            
MethodDecl
(
'
Write
'
                       
params
=
[
Decl
(
Type
(
'
IPC
:
:
Message
'
ptr
=
True
)
                                    
cls
.
msgvar
.
name
)
                               
Decl
(
iprotocoltype
                                    
cls
.
actor
.
name
)
                               
Decl
(
intype
                                    
cls
.
var
.
name
)
]
                       
methodspec
=
MethodSpec
.
STATIC
)
)
        
writemthd
.
addstmts
(
write
)
        
pt
.
addstmt
(
writemthd
)
        
outtype
=
Type
(
'
paramType
'
ptr
=
True
)
        
readmthd
=
MethodDefn
(
            
MethodDecl
(
'
Read
'
                       
params
=
[
Decl
(
Type
(
'
IPC
:
:
Message
'
ptr
=
True
const
=
True
)
                                    
cls
.
msgvar
.
name
)
                               
Decl
(
_iterType
(
ptr
=
True
)
                                    
cls
.
itervar
.
name
)
                               
Decl
(
iprotocoltype
                                    
cls
.
actor
.
name
)
                               
Decl
(
outtype
                                    
cls
.
var
.
name
)
]
                       
ret
=
Type
.
BOOL
                       
methodspec
=
MethodSpec
.
STATIC
)
)
        
readmthd
.
addstmts
(
read
)
        
pt
.
addstmt
(
readmthd
)
        
clsdecl
methoddefns
=
_splitClassDeclDefn
(
pt
)
        
namespaces
=
[
Namespace
(
'
mozilla
'
)
Namespace
(
'
ipc
'
)
]
        
clsns
=
_putInNamespaces
(
clsdecl
namespaces
)
        
defns
=
_putInNamespaces
(
methoddefns
namespaces
)
        
return
clsns
defns
    
classmethod
    
def
actorPickling
(
cls
actortype
side
)
:
        
"
"
"
Generates
pickling
for
IPDL
actors
.
This
is
a
|
nullable
|
deserializer
.
        
Write
and
read
callers
will
perform
nullability
validation
.
"
"
"
        
cxxtype
=
_cxxBareType
(
actortype
side
fq
=
True
)
        
idvar
=
ExprVar
(
'
id
'
)
        
write
=
[
            
StmtDecl
(
Decl
(
_actorIdType
(
)
idvar
.
name
)
)
        
]
        
ifnull
=
StmtIf
(
ExprNot
(
cls
.
var
)
)
        
ifnull
.
addifstmt
(
StmtExpr
(
ExprAssn
(
idvar
_NULL_ACTOR_ID
)
)
)
        
ifnull
.
addelsestmt
(
StmtExpr
(
ExprAssn
(
idvar
_actorId
(
cls
.
var
)
)
)
)
        
iffreed
=
StmtIf
(
ExprBinary
(
_FREED_ACTOR_ID
'
=
=
'
idvar
)
)
        
iffreed
.
addifstmt
(
cls
.
fatalError
(
"
actor
has
been
|
delete
|
d
"
)
)
        
ifnull
.
addelsestmt
(
iffreed
)
        
ifnull
.
addelsestmt
(
            
StmtExpr
(
ExprCall
(
ExprVar
(
"
MOZ_ASSERT
"
)
args
=
[
                
ExprBinary
(
                    
ExprCall
(
ExprSelect
(
cls
.
actor
'
-
>
'
'
GetIPCChannel
'
)
)
                    
'
=
=
'
                    
ExprCall
(
ExprSelect
(
cls
.
var
'
-
>
'
'
GetIPCChannel
'
)
)
                
)
                
ExprLiteral
.
String
(
"
Actor
must
be
from
the
same
channel
as
the
"
                                   
"
actor
it
'
s
being
sent
over
"
)
            
]
)
)
        
)
        
write
+
=
[
ifnull
                  
StmtExpr
(
cls
.
write
(
idvar
cls
.
msgvar
cls
.
actor
)
)
]
        
actorvar
=
ExprVar
(
'
actor
'
)
        
read
=
[
            
StmtDecl
(
Decl
(
Type
(
'
mozilla
:
:
Maybe
'
T
=
Type
(
'
mozilla
:
:
ipc
:
:
IProtocol
'
                                                        
ptr
=
True
)
)
actorvar
.
name
)
                     
init
=
ExprCall
(
ExprSelect
(
cls
.
actor
'
-
>
'
'
ReadActor
'
)
                                   
args
=
[
cls
.
msgvar
                                         
cls
.
itervar
                                         
ExprLiteral
.
TRUE
                                         
ExprLiteral
.
String
(
actortype
.
name
(
)
)
                                         
_protocolId
(
actortype
)
]
)
)
        
]
        
ifnothing
=
StmtIf
(
ExprCall
(
ExprSelect
(
actorvar
'
.
'
'
isNothing
'
)
)
)
        
ifnothing
.
addifstmts
(
[
StmtReturn
.
FALSE
]
)
        
read
+
=
[
            
ifnothing
            
Whitespace
.
NL
            
StmtExpr
(
ExprAssn
(
ExprDeref
(
cls
.
var
)
                              
ExprCast
(
ExprCall
(
ExprSelect
(
actorvar
'
.
'
'
value
'
)
)
                                       
cxxtype
static
=
True
)
)
)
            
StmtReturn
.
TRUE
        
]
        
return
cls
.
generateDecl
(
cxxtype
write
read
)
    
classmethod
    
def
structPickling
(
cls
structtype
)
:
        
sd
=
structtype
.
_ast
        
cxxtype
=
Type
(
structtype
.
fullname
(
)
)
        
def
get
(
sel
f
)
:
            
return
ExprCall
(
f
.
getMethod
(
thisexpr
=
cls
.
var
sel
=
sel
)
)
        
write
=
[
]
        
read
=
[
]
        
for
f
in
sd
.
fields
:
            
writefield
=
cls
.
checkedWrite
(
f
.
ipdltype
                                          
get
(
'
.
'
f
)
                                          
cls
.
msgvar
                                          
sentinelKey
=
f
.
basename
                                          
actor
=
cls
.
actor
)
            
readfield
=
cls
.
_checkedRead
(
f
.
ipdltype
                                         
ExprAddrOf
(
get
(
'
-
>
'
f
)
)
f
.
basename
                                         
'
\
'
'
+
f
.
getMethod
(
)
.
name
+
'
\
'
'
+
                                         
'
(
'
+
f
.
ipdltype
.
name
(
)
+
'
)
member
of
'
+
                                         
'
\
'
'
+
structtype
.
name
(
)
+
'
\
'
'
)
            
if
f
.
special
:
                
writefield
=
cls
.
ifsideis
(
f
.
side
writefield
)
                
readfield
=
cls
.
ifsideis
(
f
.
side
readfield
)
            
write
.
append
(
writefield
)
            
read
.
append
(
readfield
)
        
read
.
append
(
StmtReturn
.
TRUE
)
        
return
cls
.
generateDecl
(
cxxtype
write
read
)
    
classmethod
    
def
unionPickling
(
cls
uniontype
)
:
        
cxxtype
=
Type
(
uniontype
.
fullname
(
)
)
        
ud
=
uniontype
.
_ast
        
alias
=
'
union__
'
        
typevar
=
ExprVar
(
'
type
'
)
        
prelude
=
[
            
Typedef
(
cxxtype
alias
)
            
StmtDecl
(
Decl
(
Type
.
INT
typevar
.
name
)
)
        
]
        
writeswitch
=
StmtSwitch
(
typevar
)
        
write
=
prelude
+
[
            
StmtExpr
(
ExprAssn
(
typevar
ud
.
callType
(
cls
.
var
)
)
)
            
cls
.
checkedWrite
(
None
                             
typevar
                             
cls
.
msgvar
                             
sentinelKey
=
uniontype
.
name
(
)
                             
actor
=
cls
.
actor
)
            
Whitespace
.
NL
            
writeswitch
        
]
        
readswitch
=
StmtSwitch
(
typevar
)
        
read
=
prelude
+
[
            
cls
.
_checkedRead
(
None
                             
ExprAddrOf
(
typevar
)
                             
uniontype
.
name
(
)
                             
'
type
of
union
'
+
uniontype
.
name
(
)
)
            
Whitespace
.
NL
            
readswitch
        
]
        
for
c
in
ud
.
components
:
            
ct
=
c
.
ipdltype
            
caselabel
=
CaseLabel
(
alias
+
'
:
:
'
+
c
.
enum
(
)
)
            
origenum
=
c
.
enum
(
)
            
writecase
=
StmtBlock
(
)
            
wstmt
=
cls
.
checkedWrite
(
c
.
ipdltype
                                     
ExprCall
(
ExprSelect
(
cls
.
var
'
.
'
                                                         
c
.
getTypeName
(
)
)
)
                                     
cls
.
msgvar
sentinelKey
=
c
.
enum
(
)
                                     
actor
=
cls
.
actor
)
            
if
c
.
special
:
                
wstmt
=
cls
.
ifsideis
(
c
.
side
wstmt
                                     
els
=
cls
.
fatalError
(
'
wrong
side
!
'
)
)
            
writecase
.
addstmts
(
[
wstmt
StmtReturn
(
)
]
)
            
writeswitch
.
addcase
(
caselabel
writecase
)
            
readcase
=
StmtBlock
(
)
            
if
c
.
special
:
                
readcase
.
addstmt
(
cls
.
ifsideis
(
c
.
side
                                              
StmtBlock
(
[
cls
.
fatalError
(
'
wrong
side
!
'
)
                                                         
StmtReturn
.
FALSE
]
)
)
)
                
c
=
c
.
other
            
tmpvar
=
ExprVar
(
'
tmp
'
)
            
ct
=
c
.
bareType
(
fq
=
True
)
            
readcase
.
addstmts
(
[
                
StmtDecl
(
Decl
(
ct
tmpvar
.
name
)
init
=
c
.
defaultValue
(
fq
=
True
)
)
                
StmtExpr
(
ExprAssn
(
ExprDeref
(
cls
.
var
)
tmpvar
)
)
                
cls
.
_checkedRead
(
c
.
ipdltype
                                 
ExprAddrOf
(
ExprCall
(
ExprSelect
(
cls
.
var
'
-
>
'
                                                                
c
.
getTypeName
(
)
)
)
)
                                 
origenum
                                 
'
variant
'
+
origenum
+
'
of
union
'
+
uniontype
.
name
(
)
)
                
StmtReturn
.
TRUE
            
]
)
            
readswitch
.
addcase
(
caselabel
readcase
)
        
writeswitch
.
addcase
(
DefaultLabel
(
)
                            
StmtBlock
(
[
cls
.
fatalError
(
'
unknown
union
type
'
)
                                       
StmtReturn
(
)
]
)
)
        
readswitch
.
addcase
(
DefaultLabel
(
)
                           
StmtBlock
(
[
cls
.
fatalError
(
'
unknown
union
type
'
)
                                      
StmtReturn
.
FALSE
]
)
)
        
return
cls
.
generateDecl
(
cxxtype
write
read
)
class
_ComputeTypeDeps
(
TypeVisitor
)
:
    
'
'
'
Pass
that
gathers
the
C
+
+
types
that
a
particular
IPDL
type
(
recursively
)
depends
on
.
There
are
three
kinds
of
dependencies
:
(
i
)
types
that
need
forward
declaration
;
(
ii
)
types
that
need
a
|
using
|
stmt
;
(
iii
)
IPDL
structs
or
unions
which
must
be
fully
declared
before
this
struct
.
Some
types
generate
multiple
kinds
.
'
'
'
    
def
__init__
(
self
fortype
unqualifiedTypedefs
=
False
)
:
        
ipdl
.
type
.
TypeVisitor
.
__init__
(
self
)
        
self
.
usingTypedefs
=
[
]
        
self
.
forwardDeclStmts
=
[
]
        
self
.
fullDeclTypes
=
[
]
        
self
.
fortype
=
fortype
        
self
.
unqualifiedTypedefs
=
unqualifiedTypedefs
    
def
maybeTypedef
(
self
fqname
name
)
:
        
if
fqname
!
=
name
or
self
.
unqualifiedTypedefs
:
            
self
.
usingTypedefs
.
append
(
Typedef
(
Type
(
fqname
)
name
)
)
    
def
visitImportedCxxType
(
self
t
)
:
        
if
t
in
self
.
visited
:
            
return
        
self
.
visited
.
add
(
t
)
        
self
.
maybeTypedef
(
t
.
fullname
(
)
t
.
name
(
)
)
    
def
visitActorType
(
self
t
)
:
        
if
t
in
self
.
visited
:
            
return
        
self
.
visited
.
add
(
t
)
        
fqname
name
=
t
.
fullname
(
)
t
.
name
(
)
        
self
.
maybeTypedef
(
_actorName
(
fqname
'
Parent
'
)
                          
_actorName
(
name
'
Parent
'
)
)
        
self
.
maybeTypedef
(
_actorName
(
fqname
'
Child
'
)
                          
_actorName
(
name
'
Child
'
)
)
        
self
.
forwardDeclStmts
.
extend
(
[
            
_makeForwardDeclForActor
(
t
.
protocol
'
parent
'
)
Whitespace
.
NL
            
_makeForwardDeclForActor
(
t
.
protocol
'
child
'
)
Whitespace
.
NL
        
]
)
    
def
visitStructOrUnionType
(
self
su
defaultVisit
)
:
        
if
su
in
self
.
visited
or
su
=
=
self
.
fortype
:
            
return
        
self
.
visited
.
add
(
su
)
        
self
.
maybeTypedef
(
su
.
fullname
(
)
su
.
name
(
)
)
        
if
isinstance
(
self
.
fortype
UnionType
)
and
self
.
fortype
.
mutuallyRecursiveWith
(
su
)
:
            
self
.
forwardDeclStmts
.
append
(
_makeForwardDecl
(
su
)
)
        
else
:
            
self
.
fullDeclTypes
.
append
(
su
)
        
return
defaultVisit
(
self
su
)
    
def
visitStructType
(
self
t
)
:
        
return
self
.
visitStructOrUnionType
(
t
TypeVisitor
.
visitStructType
)
    
def
visitUnionType
(
self
t
)
:
        
return
self
.
visitStructOrUnionType
(
t
TypeVisitor
.
visitUnionType
)
    
def
visitArrayType
(
self
t
)
:
        
return
TypeVisitor
.
visitArrayType
(
self
t
)
    
def
visitShmemType
(
self
s
)
:
        
if
s
in
self
.
visited
:
            
return
        
self
.
visited
.
add
(
s
)
        
self
.
maybeTypedef
(
'
mozilla
:
:
ipc
:
:
Shmem
'
'
Shmem
'
)
    
def
visitByteBufType
(
self
s
)
:
        
if
s
in
self
.
visited
:
            
return
        
self
.
visited
.
add
(
s
)
        
self
.
maybeTypedef
(
'
mozilla
:
:
ipc
:
:
ByteBuf
'
'
ByteBuf
'
)
    
def
visitFDType
(
self
s
)
:
        
if
s
in
self
.
visited
:
            
return
        
self
.
visited
.
add
(
s
)
        
self
.
maybeTypedef
(
'
mozilla
:
:
ipc
:
:
FileDescriptor
'
'
FileDescriptor
'
)
    
def
visitUniquePtrType
(
self
s
)
:
        
if
s
in
self
.
visited
:
            
return
        
self
.
visited
.
add
(
s
)
    
def
visitVoidType
(
self
v
)
:
assert
0
    
def
visitMessageType
(
self
v
)
:
assert
0
    
def
visitProtocolType
(
self
v
)
:
assert
0
    
def
visitStateType
(
self
v
)
:
assert
0
def
_generateCxxStruct
(
sd
)
:
    
'
'
'
'
'
'
    
gettypedeps
=
_ComputeTypeDeps
(
sd
.
decl
.
type
)
    
for
f
in
sd
.
fields
:
        
f
.
ipdltype
.
accept
(
gettypedeps
)
    
usingTypedefs
=
gettypedeps
.
usingTypedefs
    
forwarddeclstmts
=
gettypedeps
.
forwardDeclStmts
    
fulldecltypes
=
gettypedeps
.
fullDeclTypes
    
struct
=
Class
(
sd
.
name
final
=
True
)
    
struct
.
addstmts
(
[
Label
.
PRIVATE
]
                    
+
usingTypedefs
                    
+
[
Whitespace
.
NL
Label
.
PUBLIC
]
)
    
constreftype
=
Type
(
sd
.
name
const
=
True
ref
=
True
)
    
def
fieldsAsParamList
(
)
:
        
return
[
Decl
(
f
.
inType
(
)
f
.
argVar
(
)
.
name
)
for
f
in
sd
.
fields
]
    
if
len
(
sd
.
fields
)
:
        
defctor
=
ConstructorDefn
(
ConstructorDecl
(
sd
.
name
force_inline
=
True
)
)
        
defctor
.
memberinits
=
[
ExprMemberInit
(
f
.
memberVar
(
)
)
for
f
in
sd
.
fields
]
        
struct
.
addstmts
(
[
defctor
Whitespace
.
NL
]
)
    
valctor
=
ConstructorDefn
(
ConstructorDecl
(
sd
.
name
                                              
params
=
fieldsAsParamList
(
)
                                              
force_inline
=
True
)
)
    
valctor
.
memberinits
=
[
ExprMemberInit
(
f
.
memberVar
(
)
                                          
args
=
[
f
.
argVar
(
)
]
)
                           
for
f
in
sd
.
fields
]
    
struct
.
addstmts
(
[
valctor
Whitespace
.
NL
]
)
    
ovar
=
ExprVar
(
'
_o
'
)
    
opeqeq
=
MethodDefn
(
MethodDecl
(
        
'
operator
=
=
'
        
params
=
[
Decl
(
constreftype
ovar
.
name
)
]
        
ret
=
Type
.
BOOL
        
const
=
True
)
)
    
for
f
in
sd
.
fields
:
        
ifneq
=
StmtIf
(
ExprNot
(
            
ExprBinary
(
ExprCall
(
f
.
getMethod
(
)
)
'
=
=
'
                       
ExprCall
(
f
.
getMethod
(
ovar
)
)
)
)
)
        
ifneq
.
addifstmt
(
StmtReturn
.
FALSE
)
        
opeqeq
.
addstmt
(
ifneq
)
    
opeqeq
.
addstmt
(
StmtReturn
.
TRUE
)
    
struct
.
addstmts
(
[
opeqeq
Whitespace
.
NL
]
)
    
opneq
=
MethodDefn
(
MethodDecl
(
        
'
operator
!
=
'
        
params
=
[
Decl
(
constreftype
ovar
.
name
)
]
        
ret
=
Type
.
BOOL
        
const
=
True
)
)
    
opneq
.
addstmt
(
StmtReturn
(
ExprNot
(
ExprCall
(
ExprVar
(
'
operator
=
=
'
)
                                              
args
=
[
ovar
]
)
)
)
)
    
struct
.
addstmts
(
[
opneq
Whitespace
.
NL
]
)
    
for
f
in
sd
.
fields
:
        
get
=
MethodDefn
(
MethodDecl
(
f
.
getMethod
(
)
.
name
                                    
params
=
[
]
                                    
ret
=
f
.
refType
(
)
                                    
force_inline
=
True
)
)
        
get
.
addstmt
(
StmtReturn
(
f
.
refExpr
(
)
)
)
        
getconstdecl
=
deepcopy
(
get
.
decl
)
        
getconstdecl
.
ret
=
f
.
constRefType
(
)
        
getconstdecl
.
const
=
True
        
getconst
=
MethodDefn
(
getconstdecl
)
        
getconst
.
addstmt
(
StmtReturn
(
f
.
constRefExpr
(
)
)
)
        
struct
.
addstmts
(
[
get
getconst
Whitespace
.
NL
]
)
    
struct
.
addstmt
(
Label
.
PRIVATE
)
    
struct
.
addstmts
(
[
StmtDecl
(
Decl
(
f
.
bareType
(
)
f
.
memberVar
(
)
.
name
)
)
                     
for
f
in
sd
.
fields
]
)
    
return
forwarddeclstmts
fulldecltypes
struct
def
_generateCxxUnion
(
ud
)
:
    
cls
=
Class
(
ud
.
name
final
=
True
)
    
inClsType
=
Type
(
ud
.
name
const
=
True
ref
=
True
)
    
refClsType
=
Type
(
ud
.
name
ref
=
True
)
    
rvalueRefClsType
=
Type
(
ud
.
name
rvalref
=
True
)
    
typetype
=
Type
(
'
Type
'
)
    
valuetype
=
Type
(
'
Value
'
)
    
mtypevar
=
ExprVar
(
'
mType
'
)
    
mvaluevar
=
ExprVar
(
'
mValue
'
)
    
maybedtorvar
=
ExprVar
(
'
MaybeDestroy
'
)
    
assertsanityvar
=
ExprVar
(
'
AssertSanity
'
)
    
tnonevar
=
ExprVar
(
'
T__None
'
)
    
tlastvar
=
ExprVar
(
'
T__Last
'
)
    
def
callAssertSanity
(
uvar
=
None
expectTypeVar
=
None
)
:
        
func
=
assertsanityvar
        
args
=
[
]
        
if
uvar
is
not
None
:
            
func
=
ExprSelect
(
uvar
'
.
'
assertsanityvar
.
name
)
        
if
expectTypeVar
is
not
None
:
            
args
.
append
(
expectTypeVar
)
        
return
ExprCall
(
func
args
=
args
)
    
def
callMaybeDestroy
(
newTypeVar
)
:
        
return
ExprCall
(
maybedtorvar
args
=
[
newTypeVar
]
)
    
def
maybeReconstruct
(
memb
newTypeVar
)
:
        
ifdied
=
StmtIf
(
callMaybeDestroy
(
newTypeVar
)
)
        
ifdied
.
addifstmt
(
StmtExpr
(
memb
.
callCtor
(
)
)
)
        
return
ifdied
    
def
voidCast
(
expr
)
:
        
return
ExprCast
(
expr
Type
.
VOID
static
=
True
)
    
gettypedeps
=
_ComputeTypeDeps
(
ud
.
decl
.
type
)
    
for
c
in
ud
.
components
:
        
c
.
ipdltype
.
accept
(
gettypedeps
)
    
usingTypedefs
=
gettypedeps
.
usingTypedefs
    
forwarddeclstmts
=
gettypedeps
.
forwardDeclStmts
    
fulldecltypes
=
gettypedeps
.
fullDeclTypes
    
cls
.
addstmt
(
Label
.
PUBLIC
)
    
typeenum
=
TypeEnum
(
typetype
.
name
)
    
typeenum
.
addId
(
tnonevar
.
name
0
)
    
firstid
=
ud
.
components
[
0
]
.
enum
(
)
    
typeenum
.
addId
(
firstid
1
)
    
for
c
in
ud
.
components
[
1
:
]
:
        
typeenum
.
addId
(
c
.
enum
(
)
)
    
typeenum
.
addId
(
tlastvar
.
name
ud
.
components
[
-
1
]
.
enum
(
)
)
    
cls
.
addstmts
(
[
StmtDecl
(
Decl
(
typeenum
'
'
)
)
                  
Whitespace
.
NL
]
)
    
cls
.
addstmt
(
Label
.
PRIVATE
)
    
cls
.
addstmts
(
        
usingTypedefs
        
+
[
Typedef
(
c
.
internalType
(
)
c
.
typedef
(
)
)
for
c
in
ud
.
components
]
)
    
cls
.
addstmt
(
Whitespace
.
NL
)
    
valueunion
=
TypeUnion
(
valuetype
.
name
)
    
for
c
in
ud
.
components
:
        
valueunion
.
addComponent
(
c
.
unionType
(
)
c
.
name
)
    
cls
.
addstmts
(
[
StmtDecl
(
Decl
(
valueunion
'
'
)
)
                  
Whitespace
.
NL
]
)
    
for
c
in
ud
.
components
:
        
getptr
=
MethodDefn
(
MethodDecl
(
            
c
.
getPtrName
(
)
params
=
[
]
ret
=
c
.
ptrToInternalType
(
)
            
force_inline
=
True
)
)
        
getptr
.
addstmt
(
StmtReturn
(
c
.
ptrToSelfExpr
(
)
)
)
        
getptrconst
=
MethodDefn
(
MethodDecl
(
            
c
.
getConstPtrName
(
)
params
=
[
]
ret
=
c
.
constPtrToType
(
)
            
const
=
True
force_inline
=
True
)
)
        
getptrconst
.
addstmt
(
StmtReturn
(
c
.
constptrToSelfExpr
(
)
)
)
        
cls
.
addstmts
(
[
getptr
getptrconst
]
)
    
cls
.
addstmt
(
Whitespace
.
NL
)
    
newtypevar
=
ExprVar
(
'
aNewType
'
)
    
maybedtor
=
MethodDefn
(
MethodDecl
(
        
maybedtorvar
.
name
        
params
=
[
Decl
(
typetype
newtypevar
.
name
)
]
        
ret
=
Type
.
BOOL
)
)
    
ifnone
=
StmtIf
(
ExprBinary
(
mtypevar
'
=
=
'
tnonevar
)
)
    
ifnone
.
addifstmt
(
StmtReturn
.
TRUE
)
    
ifnochange
=
StmtIf
(
ExprBinary
(
mtypevar
'
=
=
'
newtypevar
)
)
    
ifnochange
.
addifstmt
(
StmtReturn
.
FALSE
)
    
dtorswitch
=
StmtSwitch
(
mtypevar
)
    
for
c
in
ud
.
components
:
        
dtorswitch
.
addcase
(
            
CaseLabel
(
c
.
enum
(
)
)
            
StmtBlock
(
[
StmtExpr
(
c
.
callDtor
(
)
)
                       
StmtBreak
(
)
]
)
)
    
dtorswitch
.
addcase
(
        
DefaultLabel
(
)
        
StmtBlock
(
[
_logicError
(
"
not
reached
"
)
StmtBreak
(
)
]
)
)
    
maybedtor
.
addstmts
(
[
        
ifnone
        
ifnochange
        
dtorswitch
        
StmtReturn
.
TRUE
    
]
)
    
cls
.
addstmts
(
[
maybedtor
Whitespace
.
NL
]
)
    
sanity
=
MethodDefn
(
MethodDecl
(
        
assertsanityvar
.
name
ret
=
Type
.
VOID
const
=
True
force_inline
=
True
)
)
    
sanity
.
addstmts
(
[
        
_abortIfFalse
(
ExprBinary
(
tnonevar
'
<
=
'
mtypevar
)
                      
'
invalid
type
tag
'
)
        
_abortIfFalse
(
ExprBinary
(
mtypevar
'
<
=
'
tlastvar
)
                      
'
invalid
type
tag
'
)
]
)
    
cls
.
addstmt
(
sanity
)
    
atypevar
=
ExprVar
(
'
aType
'
)
    
sanity2
=
MethodDefn
(
        
MethodDecl
(
assertsanityvar
.
name
                   
params
=
[
Decl
(
typetype
atypevar
.
name
)
]
                   
ret
=
Type
.
VOID
                   
const
=
True
force_inline
=
True
)
)
    
sanity2
.
addstmts
(
[
        
StmtExpr
(
ExprCall
(
assertsanityvar
)
)
        
_abortIfFalse
(
ExprBinary
(
mtypevar
'
=
=
'
atypevar
)
                      
'
unexpected
type
tag
'
)
]
)
    
cls
.
addstmts
(
[
sanity2
Whitespace
.
NL
]
)
    
cls
.
addstmts
(
[
        
Label
.
PUBLIC
        
ConstructorDefn
(
            
ConstructorDecl
(
ud
.
name
force_inline
=
True
)
            
memberinits
=
[
ExprMemberInit
(
mtypevar
[
tnonevar
]
)
]
)
        
Whitespace
.
NL
    
]
)
    
othervar
=
ExprVar
(
'
aOther
'
)
    
for
c
in
ud
.
components
:
        
copyctor
=
ConstructorDefn
(
ConstructorDecl
(
            
ud
.
name
params
=
[
Decl
(
c
.
inType
(
)
othervar
.
name
)
]
)
)
        
copyctor
.
addstmts
(
[
            
StmtExpr
(
c
.
callCtor
(
othervar
)
)
            
StmtExpr
(
ExprAssn
(
mtypevar
c
.
enumvar
(
)
)
)
]
)
        
cls
.
addstmts
(
[
copyctor
Whitespace
.
NL
]
)
        
if
not
_cxxTypeCanMove
(
c
.
ipdltype
)
:
            
continue
        
movector
=
ConstructorDefn
(
ConstructorDecl
(
            
ud
.
name
params
=
[
Decl
(
c
.
forceMoveType
(
)
othervar
.
name
)
]
)
)
        
movector
.
addstmts
(
[
            
StmtExpr
(
c
.
callCtor
(
ExprMove
(
othervar
)
)
)
            
StmtExpr
(
ExprAssn
(
mtypevar
c
.
enumvar
(
)
)
)
]
)
        
cls
.
addstmts
(
[
movector
Whitespace
.
NL
]
)
    
copyctor
=
ConstructorDefn
(
ConstructorDecl
(
        
ud
.
name
params
=
[
Decl
(
inClsType
othervar
.
name
)
]
)
)
    
othertype
=
ud
.
callType
(
othervar
)
    
copyswitch
=
StmtSwitch
(
othertype
)
    
for
c
in
ud
.
components
:
        
copyswitch
.
addcase
(
            
CaseLabel
(
c
.
enum
(
)
)
            
StmtBlock
(
[
                
StmtExpr
(
c
.
callCtor
(
                    
ExprCall
(
ExprSelect
(
othervar
                                        
'
.
'
c
.
getConstTypeName
(
)
)
)
)
)
                
StmtBreak
(
)
            
]
)
)
    
copyswitch
.
addcase
(
CaseLabel
(
tnonevar
.
name
)
                       
StmtBlock
(
[
StmtBreak
(
)
]
)
)
    
copyswitch
.
addcase
(
        
DefaultLabel
(
)
        
StmtBlock
(
[
_logicError
(
'
unreached
'
)
StmtReturn
(
)
]
)
)
    
copyctor
.
addstmts
(
[
        
StmtExpr
(
callAssertSanity
(
uvar
=
othervar
)
)
        
copyswitch
        
StmtExpr
(
ExprAssn
(
mtypevar
othertype
)
)
    
]
)
    
cls
.
addstmts
(
[
copyctor
Whitespace
.
NL
]
)
    
movector
=
ConstructorDefn
(
ConstructorDecl
(
        
ud
.
name
params
=
[
Decl
(
rvalueRefClsType
othervar
.
name
)
]
)
)
    
othertypevar
=
ExprVar
(
"
t
"
)
    
moveswitch
=
StmtSwitch
(
othertypevar
)
    
for
c
in
ud
.
components
:
        
case
=
StmtBlock
(
)
        
if
c
.
recursive
:
            
case
.
addstmts
(
[
                
StmtExpr
(
ExprAssn
(
c
.
callGetPtr
(
)
                                  
ExprCall
(
ExprSelect
(
othervar
'
.
'
ExprVar
(
c
.
getPtrName
(
)
)
)
)
)
)
            
]
)
        
else
:
            
case
.
addstmts
(
[
                
StmtExpr
(
c
.
callCtor
(
ExprMove
(
ExprCall
(
ExprSelect
(
othervar
'
.
'
                                                                 
c
.
getTypeName
(
)
)
)
)
)
)
                
StmtExpr
(
                    
voidCast
(
ExprCall
(
ExprSelect
(
othervar
'
.
'
maybedtorvar
)
                                      
args
=
[
tnonevar
]
)
)
)
            
]
)
        
case
.
addstmts
(
[
StmtBreak
(
)
]
)
        
moveswitch
.
addcase
(
CaseLabel
(
c
.
enum
(
)
)
case
)
    
moveswitch
.
addcase
(
CaseLabel
(
tnonevar
.
name
)
                       
StmtBlock
(
[
StmtBreak
(
)
]
)
)
    
moveswitch
.
addcase
(
        
DefaultLabel
(
)
        
StmtBlock
(
[
_logicError
(
'
unreached
'
)
StmtReturn
(
)
]
)
)
    
movector
.
addstmts
(
[
        
StmtExpr
(
callAssertSanity
(
uvar
=
othervar
)
)
        
StmtDecl
(
Decl
(
typetype
othertypevar
.
name
)
init
=
ud
.
callType
(
othervar
)
)
        
moveswitch
        
StmtExpr
(
ExprAssn
(
ExprSelect
(
othervar
'
.
'
mtypevar
)
tnonevar
)
)
        
StmtExpr
(
ExprAssn
(
mtypevar
othertypevar
)
)
    
]
)
    
cls
.
addstmts
(
[
movector
Whitespace
.
NL
]
)
    
dtor
=
DestructorDefn
(
DestructorDecl
(
ud
.
name
)
)
    
dtor
.
addstmt
(
StmtExpr
(
voidCast
(
callMaybeDestroy
(
tnonevar
)
)
)
)
    
cls
.
addstmts
(
[
dtor
Whitespace
.
NL
]
)
    
typemeth
=
MethodDefn
(
MethodDecl
(
'
type
'
ret
=
typetype
                                     
const
=
True
force_inline
=
True
)
)
    
typemeth
.
addstmt
(
StmtReturn
(
mtypevar
)
)
    
cls
.
addstmts
(
[
typemeth
Whitespace
.
NL
]
)
    
rhsvar
=
ExprVar
(
'
aRhs
'
)
    
for
c
in
ud
.
components
:
        
opeq
=
MethodDefn
(
MethodDecl
(
            
'
operator
=
'
            
params
=
[
Decl
(
c
.
inType
(
)
rhsvar
.
name
)
]
            
ret
=
refClsType
)
)
        
opeq
.
addstmts
(
[
            
maybeReconstruct
(
c
c
.
enumvar
(
)
)
            
StmtExpr
(
c
.
callOperatorEq
(
rhsvar
)
)
            
StmtExpr
(
ExprAssn
(
mtypevar
c
.
enumvar
(
)
)
)
            
StmtReturn
(
ExprDeref
(
ExprVar
.
THIS
)
)
        
]
)
        
cls
.
addstmts
(
[
opeq
Whitespace
.
NL
]
)
        
if
not
_cxxTypeCanMove
(
c
.
ipdltype
)
:
            
continue
        
opeq
=
MethodDefn
(
MethodDecl
(
            
'
operator
=
'
            
params
=
[
Decl
(
c
.
forceMoveType
(
)
rhsvar
.
name
)
]
            
ret
=
refClsType
)
)
        
opeq
.
addstmts
(
[
            
maybeReconstruct
(
c
c
.
enumvar
(
)
)
            
StmtExpr
(
c
.
callOperatorEq
(
ExprMove
(
rhsvar
)
)
)
            
StmtExpr
(
ExprAssn
(
mtypevar
c
.
enumvar
(
)
)
)
            
StmtReturn
(
ExprDeref
(
ExprVar
.
THIS
)
)
        
]
)
        
cls
.
addstmts
(
[
opeq
Whitespace
.
NL
]
)
    
opeq
=
MethodDefn
(
MethodDecl
(
        
'
operator
=
'
        
params
=
[
Decl
(
inClsType
rhsvar
.
name
)
]
        
ret
=
refClsType
)
)
    
rhstypevar
=
ExprVar
(
'
t
'
)
    
opeqswitch
=
StmtSwitch
(
rhstypevar
)
    
for
c
in
ud
.
components
:
        
case
=
StmtBlock
(
)
        
case
.
addstmts
(
[
            
maybeReconstruct
(
c
rhstypevar
)
            
StmtExpr
(
c
.
callOperatorEq
(
                
ExprCall
(
ExprSelect
(
rhsvar
'
.
'
c
.
getConstTypeName
(
)
)
)
)
)
            
StmtBreak
(
)
        
]
)
        
opeqswitch
.
addcase
(
CaseLabel
(
c
.
enum
(
)
)
case
)
    
opeqswitch
.
addcase
(
        
CaseLabel
(
tnonevar
.
name
)
        
StmtBlock
(
[
StmtExpr
(
ExprCast
(
callMaybeDestroy
(
rhstypevar
)
Type
.
VOID
                                     
static
=
True
)
)
                   
StmtBreak
(
)
]
)
    
)
    
opeqswitch
.
addcase
(
        
DefaultLabel
(
)
        
StmtBlock
(
[
_logicError
(
'
unreached
'
)
StmtBreak
(
)
]
)
)
    
opeq
.
addstmts
(
[
        
StmtExpr
(
callAssertSanity
(
uvar
=
rhsvar
)
)
        
StmtDecl
(
Decl
(
typetype
rhstypevar
.
name
)
init
=
ud
.
callType
(
rhsvar
)
)
        
opeqswitch
        
StmtExpr
(
ExprAssn
(
mtypevar
rhstypevar
)
)
        
StmtReturn
(
ExprDeref
(
ExprVar
.
THIS
)
)
    
]
)
    
cls
.
addstmts
(
[
opeq
Whitespace
.
NL
]
)
    
opeq
=
MethodDefn
(
MethodDecl
(
        
'
operator
=
'
        
params
=
[
Decl
(
rvalueRefClsType
rhsvar
.
name
)
]
        
ret
=
refClsType
)
)
    
rhstypevar
=
ExprVar
(
'
t
'
)
    
opeqswitch
=
StmtSwitch
(
rhstypevar
)
    
for
c
in
ud
.
components
:
        
case
=
StmtBlock
(
)
        
if
c
.
recursive
:
            
case
.
addstmts
(
[
                
StmtExpr
(
voidCast
(
callMaybeDestroy
(
tnonevar
)
)
)
                
StmtExpr
(
ExprAssn
(
c
.
callGetPtr
(
)
                                  
ExprCall
(
ExprSelect
(
rhsvar
'
.
'
ExprVar
(
c
.
getPtrName
(
)
)
)
)
)
)
            
]
)
        
else
:
            
case
.
addstmts
(
[
                
maybeReconstruct
(
c
rhstypevar
)
                
StmtExpr
(
c
.
callOperatorEq
(
                    
ExprMove
(
ExprCall
(
ExprSelect
(
rhsvar
'
.
'
c
.
getTypeName
(
)
)
)
)
)
)
                
StmtExpr
(
                    
voidCast
(
ExprCall
(
ExprSelect
(
rhsvar
'
.
'
maybedtorvar
)
args
=
[
tnonevar
]
)
)
)
            
]
)
        
case
.
addstmts
(
[
StmtBreak
(
)
]
)
        
opeqswitch
.
addcase
(
CaseLabel
(
c
.
enum
(
)
)
case
)
    
opeqswitch
.
addcase
(
        
CaseLabel
(
tnonevar
.
name
)
        
StmtBlock
(
[
StmtExpr
(
voidCast
(
callMaybeDestroy
(
rhstypevar
)
)
)
                   
StmtBreak
(
)
]
)
    
)
    
opeqswitch
.
addcase
(
        
DefaultLabel
(
)
        
StmtBlock
(
[
_logicError
(
'
unreached
'
)
StmtBreak
(
)
]
)
)
    
opeq
.
addstmts
(
[
        
StmtExpr
(
callAssertSanity
(
uvar
=
rhsvar
)
)
        
StmtDecl
(
Decl
(
typetype
rhstypevar
.
name
)
init
=
ud
.
callType
(
rhsvar
)
)
        
opeqswitch
        
StmtExpr
(
ExprAssn
(
ExprSelect
(
rhsvar
'
.
'
mtypevar
)
tnonevar
)
)
        
StmtExpr
(
ExprAssn
(
mtypevar
rhstypevar
)
)
        
StmtReturn
(
ExprDeref
(
ExprVar
.
THIS
)
)
    
]
)
    
cls
.
addstmts
(
[
opeq
Whitespace
.
NL
]
)
    
for
c
in
ud
.
components
:
        
opeqeq
=
MethodDefn
(
MethodDecl
(
            
'
operator
=
=
'
            
params
=
[
Decl
(
c
.
inType
(
)
rhsvar
.
name
)
]
            
ret
=
Type
.
BOOL
            
const
=
True
)
)
        
opeqeq
.
addstmt
(
StmtReturn
(
ExprBinary
(
            
ExprCall
(
ExprVar
(
c
.
getTypeName
(
)
)
)
'
=
=
'
rhsvar
)
)
)
        
cls
.
addstmts
(
[
opeqeq
Whitespace
.
NL
]
)
    
opeqeq
=
MethodDefn
(
MethodDecl
(
        
'
operator
=
=
'
        
params
=
[
Decl
(
inClsType
rhsvar
.
name
)
]
        
ret
=
Type
.
BOOL
        
const
=
True
)
)
    
iftypesmismatch
=
StmtIf
(
ExprBinary
(
ud
.
callType
(
)
'
!
=
'
                                        
ud
.
callType
(
rhsvar
)
)
)
    
iftypesmismatch
.
addifstmt
(
StmtReturn
.
FALSE
)
    
opeqeq
.
addstmts
(
[
iftypesmismatch
Whitespace
.
NL
]
)
    
opeqeqswitch
=
StmtSwitch
(
ud
.
callType
(
)
)
    
for
c
in
ud
.
components
:
        
case
=
StmtBlock
(
)
        
case
.
addstmt
(
StmtReturn
(
ExprBinary
(
            
ExprCall
(
ExprVar
(
c
.
getTypeName
(
)
)
)
'
=
=
'
            
ExprCall
(
ExprSelect
(
rhsvar
'
.
'
c
.
getTypeName
(
)
)
)
)
)
)
        
opeqeqswitch
.
addcase
(
CaseLabel
(
c
.
enum
(
)
)
case
)
    
opeqeqswitch
.
addcase
(
        
DefaultLabel
(
)
        
StmtBlock
(
[
_logicError
(
'
unreached
'
)
                   
StmtReturn
.
FALSE
]
)
)
    
opeqeq
.
addstmt
(
opeqeqswitch
)
    
cls
.
addstmts
(
[
opeqeq
Whitespace
.
NL
]
)
    
for
c
in
ud
.
components
:
        
getValueVar
=
ExprVar
(
c
.
getTypeName
(
)
)
        
getConstValueVar
=
ExprVar
(
c
.
getConstTypeName
(
)
)
        
getvalue
=
MethodDefn
(
MethodDecl
(
getValueVar
.
name
                                         
ret
=
c
.
refType
(
)
                                         
force_inline
=
True
)
)
        
getvalue
.
addstmts
(
[
            
StmtExpr
(
callAssertSanity
(
expectTypeVar
=
c
.
enumvar
(
)
)
)
            
StmtReturn
(
ExprDeref
(
c
.
callGetPtr
(
)
)
)
        
]
)
        
getconstvalue
=
MethodDefn
(
MethodDecl
(
            
getConstValueVar
.
name
ret
=
c
.
constRefType
(
)
            
const
=
True
force_inline
=
True
)
)
        
getconstvalue
.
addstmts
(
[
            
StmtExpr
(
callAssertSanity
(
expectTypeVar
=
c
.
enumvar
(
)
)
)
            
StmtReturn
(
c
.
getConstValue
(
)
)
        
]
)
        
readvalue
=
MethodDefn
(
MethodDecl
(
            
'
get
'
ret
=
Type
.
VOID
const
=
True
            
params
=
[
Decl
(
c
.
ptrToType
(
)
'
aOutValue
'
)
]
)
)
        
readvalue
.
addstmts
(
[
            
StmtExpr
(
ExprAssn
(
ExprDeref
(
ExprVar
(
'
aOutValue
'
)
)
                              
ExprCall
(
getConstValueVar
)
)
)
        
]
)
        
optype
=
MethodDefn
(
MethodDecl
(
'
'
typeop
=
c
.
refType
(
)
force_inline
=
True
)
)
        
optype
.
addstmt
(
StmtReturn
(
ExprCall
(
getValueVar
)
)
)
        
opconsttype
=
MethodDefn
(
MethodDecl
(
            
'
'
const
=
True
typeop
=
c
.
constRefType
(
)
force_inline
=
True
)
)
        
opconsttype
.
addstmt
(
StmtReturn
(
ExprCall
(
getConstValueVar
)
)
)
        
cls
.
addstmts
(
[
getvalue
getconstvalue
readvalue
                      
optype
opconsttype
                      
Whitespace
.
NL
]
)
    
cls
.
addstmts
(
[
        
Label
.
PRIVATE
        
StmtDecl
(
Decl
(
valuetype
mvaluevar
.
name
)
)
        
StmtDecl
(
Decl
(
typetype
mtypevar
.
name
)
)
    
]
)
    
return
forwarddeclstmts
fulldecltypes
cls
class
_FindFriends
(
ipdl
.
ast
.
Visitor
)
:
    
def
__init__
(
self
)
:
        
self
.
mytype
=
None
        
self
.
vtype
=
None
        
self
.
friends
=
set
(
)
    
def
findFriends
(
self
ptype
)
:
        
self
.
mytype
=
ptype
        
for
toplvl
in
ptype
.
toplevels
(
)
:
            
self
.
walkDownTheProtocolTree
(
toplvl
)
        
return
self
.
friends
    
def
walkDownTheProtocolTree
(
self
ptype
)
:
        
if
ptype
!
=
self
.
mytype
:
            
self
.
visit
(
ptype
)
        
for
mtype
in
ptype
.
manages
:
            
if
mtype
is
not
ptype
:
                
self
.
walkDownTheProtocolTree
(
mtype
)
    
def
visit
(
self
ptype
)
:
        
savedptype
=
self
.
vtype
        
self
.
vtype
=
ptype
        
ptype
.
_ast
.
accept
(
self
)
        
self
.
vtype
=
savedptype
    
def
visitMessageDecl
(
self
md
)
:
        
for
it
in
self
.
iterActorParams
(
md
)
:
            
if
it
.
protocol
=
=
self
.
mytype
:
                
self
.
friends
.
add
(
self
.
vtype
)
    
def
iterActorParams
(
self
md
)
:
        
for
param
in
md
.
inParams
:
            
for
actor
in
ipdl
.
type
.
iteractortypes
(
param
.
type
)
:
                
yield
actor
        
for
ret
in
md
.
outParams
:
            
for
actor
in
ipdl
.
type
.
iteractortypes
(
ret
.
type
)
:
                
yield
actor
class
_GenerateProtocolActorCode
(
ipdl
.
ast
.
Visitor
)
:
    
def
__init__
(
self
myside
)
:
        
self
.
side
=
myside
        
self
.
prettyside
=
myside
.
title
(
)
        
self
.
clsname
=
None
        
self
.
protocol
=
None
        
self
.
hdrfile
=
None
        
self
.
cppfile
=
None
        
self
.
ns
=
None
        
self
.
cls
=
None
        
self
.
includedActorTypedefs
=
[
]
        
self
.
protocolCxxIncludes
=
[
]
        
self
.
actorForwardDecls
=
[
]
        
self
.
usingDecls
=
[
]
        
self
.
externalIncludes
=
set
(
)
        
self
.
nonForwardDeclaredHeaders
=
set
(
)
    
def
lower
(
self
tu
clsname
cxxHeaderFile
cxxFile
)
:
        
self
.
clsname
=
clsname
        
self
.
hdrfile
=
cxxHeaderFile
        
self
.
cppfile
=
cxxFile
        
tu
.
accept
(
self
)
    
def
standardTypedefs
(
self
)
:
        
return
[
            
Typedef
(
Type
(
'
mozilla
:
:
ipc
:
:
IProtocol
'
)
'
IProtocol
'
)
            
Typedef
(
Type
(
'
IPC
:
:
Message
'
)
'
Message
'
)
            
Typedef
(
Type
(
'
base
:
:
ProcessHandle
'
)
'
ProcessHandle
'
)
            
Typedef
(
Type
(
'
mozilla
:
:
ipc
:
:
MessageChannel
'
)
'
MessageChannel
'
)
            
Typedef
(
Type
(
'
mozilla
:
:
ipc
:
:
SharedMemory
'
)
'
SharedMemory
'
)
        
]
    
def
visitTranslationUnit
(
self
tu
)
:
        
self
.
protocol
=
tu
.
protocol
        
hf
=
self
.
hdrfile
        
cf
=
self
.
cppfile
        
hf
.
addthings
(
            
[
_DISCLAIMER
]
            
+
_includeGuardStart
(
hf
)
            
+
[
                
Whitespace
.
NL
                
CppDirective
(
                    
'
include
'
                    
'
"
'
+
_protocolHeaderName
(
tu
.
protocol
)
+
'
.
h
"
'
)
            
]
)
        
for
inc
in
tu
.
includes
:
            
inc
.
accept
(
self
)
        
for
inc
in
tu
.
cxxIncludes
:
            
inc
.
accept
(
self
)
        
for
using
in
tu
.
using
:
            
using
.
accept
(
self
)
        
tu
.
protocol
.
accept
(
self
)
        
clsdecl
clsdefn
=
_splitClassDeclDefn
(
self
.
cls
)
        
for
stmt
in
clsdefn
.
stmts
:
            
if
isinstance
(
stmt
MethodDefn
)
:
                
if
stmt
.
decl
.
ret
and
stmt
.
decl
.
ret
.
name
=
=
'
Result
'
:
                    
stmt
.
decl
.
ret
.
name
=
clsdecl
.
name
+
'
:
:
'
+
stmt
.
decl
.
ret
.
name
        
def
setToIncludes
(
s
)
:
            
return
[
CppDirective
(
'
include
'
'
"
%
s
"
'
%
i
)
                    
for
i
in
sorted
(
iter
(
s
)
)
]
        
def
makeNamespace
(
p
file
)
:
            
if
0
=
=
len
(
p
.
namespaces
)
:
                
return
file
            
ns
=
Namespace
(
p
.
namespaces
[
-
1
]
.
name
)
            
outerns
=
_putInNamespaces
(
ns
p
.
namespaces
[
:
-
1
]
)
            
file
.
addthing
(
outerns
)
            
return
ns
        
if
len
(
self
.
nonForwardDeclaredHeaders
)
!
=
0
:
            
self
.
hdrfile
.
addthings
(
                
[
Whitespace
(
'
/
/
Headers
for
things
that
cannot
be
forward
declared
'
)
                 
Whitespace
.
NL
]
                
+
setToIncludes
(
self
.
nonForwardDeclaredHeaders
)
                
+
[
Whitespace
.
NL
]
            
)
        
self
.
hdrfile
.
addthings
(
self
.
actorForwardDecls
)
        
self
.
hdrfile
.
addthings
(
self
.
usingDecls
)
        
hdrns
=
makeNamespace
(
self
.
protocol
self
.
hdrfile
)
        
hdrns
.
addstmts
(
[
            
Whitespace
.
NL
            
Whitespace
.
NL
            
clsdecl
            
Whitespace
.
NL
            
Whitespace
.
NL
        
]
)
        
actortype
=
ActorType
(
tu
.
protocol
.
decl
.
type
)
        
traitsdecl
traitsdefn
=
_ParamTraits
.
actorPickling
(
actortype
self
.
side
)
        
self
.
hdrfile
.
addthings
(
            
[
traitsdecl
Whitespace
.
NL
]
+
_includeGuardEnd
(
hf
)
        
)
        
cf
.
addthings
(
[
            
_DISCLAIMER
            
Whitespace
.
NL
            
CppDirective
(
                
'
include
'
                
'
"
'
+
_protocolHeaderName
(
self
.
protocol
self
.
side
)
+
'
.
h
"
'
)
]
            
+
setToIncludes
(
self
.
externalIncludes
)
)
        
cppheaders
=
[
CppDirective
(
'
include
'
'
"
%
s
"
'
%
filename
)
                      
for
filename
in
ipdl
.
builtin
.
CppIncludes
]
        
cf
.
addthings
(
(
            
[
Whitespace
.
NL
]
            
+
[
CppDirective
(
                
'
include
'
                
'
"
%
s
.
h
"
'
%
(
inc
)
)
for
inc
in
self
.
protocolCxxIncludes
]
            
+
[
Whitespace
.
NL
]
            
+
cppheaders
            
+
[
Whitespace
.
NL
]
)
)
        
cppns
=
makeNamespace
(
self
.
protocol
cf
)
        
cppns
.
addstmts
(
[
            
Whitespace
.
NL
            
Whitespace
.
NL
            
clsdefn
            
Whitespace
.
NL
            
Whitespace
.
NL
        
]
)
        
cf
.
addthing
(
traitsdefn
)
    
def
visitUsingStmt
(
self
using
)
:
        
if
using
.
header
is
None
:
            
return
        
if
using
.
canBeForwardDeclared
(
)
and
not
using
.
decl
.
type
.
isUniquePtr
(
)
:
            
spec
=
using
.
type
.
spec
            
self
.
usingDecls
.
extend
(
[
                
_makeForwardDeclForQClass
(
spec
.
baseid
spec
.
quals
                                          
cls
=
using
.
isClass
(
)
                                          
struct
=
using
.
isStruct
(
)
)
                
Whitespace
.
NL
            
]
)
            
self
.
externalIncludes
.
add
(
using
.
header
)
        
else
:
            
self
.
nonForwardDeclaredHeaders
.
add
(
using
.
header
)
    
def
visitCxxInclude
(
self
inc
)
:
        
self
.
nonForwardDeclaredHeaders
.
add
(
inc
.
file
)
    
def
visitInclude
(
self
inc
)
:
        
ip
=
inc
.
tu
.
protocol
        
if
not
ip
:
            
return
        
self
.
actorForwardDecls
.
extend
(
[
            
_makeForwardDeclForActor
(
ip
.
decl
.
type
self
.
side
)
            
_makeForwardDeclForActor
(
ip
.
decl
.
type
_otherSide
(
self
.
side
)
)
            
Whitespace
.
NL
        
]
)
        
self
.
protocolCxxIncludes
.
append
(
_protocolHeaderName
(
ip
self
.
side
)
)
        
if
ip
.
decl
.
fullname
is
not
None
:
            
self
.
includedActorTypedefs
.
append
(
Typedef
(
                
Type
(
_actorName
(
ip
.
decl
.
fullname
self
.
side
.
title
(
)
)
)
                
_actorName
(
ip
.
decl
.
shortname
self
.
side
.
title
(
)
)
)
)
            
self
.
includedActorTypedefs
.
append
(
Typedef
(
                
Type
(
_actorName
(
ip
.
decl
.
fullname
_otherSide
(
self
.
side
)
.
title
(
)
)
)
                
_actorName
(
ip
.
decl
.
shortname
_otherSide
(
self
.
side
)
.
title
(
)
)
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
hdrfile
.
addthings
(
[
            
CppDirective
(
'
ifdef
'
'
DEBUG
'
)
            
CppDirective
(
'
include
'
'
"
prenv
.
h
"
'
)
            
CppDirective
(
'
endif
'
'
/
/
DEBUG
'
)
        
]
)
        
self
.
protocol
=
p
        
ptype
=
p
.
decl
.
type
        
toplevel
=
p
.
decl
.
type
.
toplevel
(
)
        
if
ptype
.
isManager
(
)
or
1
:
            
self
.
hdrfile
.
addthing
(
CppDirective
(
'
include
'
'
"
base
/
id_map
.
h
"
'
)
)
        
self
.
hdrfile
.
addthings
(
[
            
CppDirective
(
'
include
'
'
"
mozilla
/
ipc
/
MessageChannel
.
h
"
'
)
            
Whitespace
.
NL
]
)
        
self
.
hdrfile
.
addthings
(
[
            
CppDirective
(
'
include
'
'
"
mozilla
/
ipc
/
ProtocolUtils
.
h
"
'
)
            
Whitespace
.
NL
]
)
        
hasAsyncReturns
=
False
        
for
md
in
p
.
messageDecls
:
            
if
md
.
hasAsyncReturns
(
)
:
                
hasAsyncReturns
=
True
                
break
        
inherits
=
[
]
        
if
ptype
.
isToplevel
(
)
:
            
inherits
.
append
(
Inherit
(
p
.
openedProtocolInterfaceType
(
)
                                    
viz
=
'
public
'
)
)
        
else
:
            
inherits
.
append
(
Inherit
(
p
.
managerInterfaceType
(
)
viz
=
'
public
'
)
)
        
if
hasAsyncReturns
:
            
inherits
.
append
(
Inherit
(
Type
(
'
SupportsWeakPtr
'
T
=
ExprVar
(
self
.
clsname
)
)
                                    
viz
=
'
public
'
)
)
            
self
.
hdrfile
.
addthing
(
CppDirective
(
'
include
'
'
"
mozilla
/
WeakPtr
.
h
"
'
)
)
        
if
ptype
.
isToplevel
(
)
and
self
.
side
=
=
'
parent
'
:
            
self
.
hdrfile
.
addthings
(
[
                
_makeForwardDeclForQClass
(
'
nsIFile
'
[
]
)
                
Whitespace
.
NL
            
]
)
        
self
.
cls
=
Class
(
            
self
.
clsname
            
inherits
=
inherits
            
abstract
=
True
)
        
if
hasAsyncReturns
:
            
self
.
cls
.
addstmts
(
[
                
Label
.
PUBLIC
                
Whitespace
(
'
'
indent
=
True
)
                
ExprCall
(
ExprVar
(
'
MOZ_DECLARE_WEAKREFERENCE_TYPENAME
'
)
                         
[
ExprVar
(
self
.
clsname
)
]
)
                
Whitespace
.
NL
            
]
)
        
self
.
cls
.
addstmt
(
Label
.
PRIVATE
)
        
friends
=
_FindFriends
(
)
.
findFriends
(
ptype
)
        
if
ptype
.
isManaged
(
)
:
            
friends
.
update
(
ptype
.
managers
)
        
friends
.
update
(
ptype
.
manages
)
        
friends
.
discard
(
ptype
)
        
for
friend
in
friends
:
            
self
.
actorForwardDecls
.
extend
(
[
                
_makeForwardDeclForActor
(
friend
self
.
prettyside
)
                
Whitespace
.
NL
            
]
)
            
self
.
cls
.
addstmt
(
FriendClassDecl
(
_actorName
(
friend
.
fullname
(
)
                                                        
self
.
prettyside
)
)
)
        
self
.
cls
.
addstmt
(
Label
.
PROTECTED
)
        
for
typedef
in
p
.
cxxTypedefs
(
)
:
            
self
.
cls
.
addstmt
(
typedef
)
        
for
typedef
in
self
.
includedActorTypedefs
:
            
self
.
cls
.
addstmt
(
typedef
)
        
self
.
cls
.
addstmt
(
Whitespace
.
NL
)
        
if
hasAsyncReturns
:
            
self
.
cls
.
addstmt
(
Label
.
PUBLIC
)
            
for
md
in
p
.
messageDecls
:
                
if
self
.
sendsMessage
(
md
)
and
md
.
hasAsyncReturns
(
)
:
                    
self
.
cls
.
addstmt
(
                        
Typedef
(
_makePromise
(
md
.
returns
self
.
side
)
                                
md
.
promiseName
(
)
)
)
                
if
self
.
receivesMessage
(
md
)
and
md
.
hasAsyncReturns
(
)
:
                    
self
.
cls
.
addstmt
(
                        
Typedef
(
_makeResolver
(
md
.
returns
self
.
side
)
                                
md
.
resolverName
(
)
)
)
            
self
.
cls
.
addstmt
(
Whitespace
.
NL
)
        
self
.
cls
.
addstmt
(
Label
.
PROTECTED
)
        
for
md
in
p
.
messageDecls
:
            
isctor
isdtor
=
md
.
decl
.
type
.
isCtor
(
)
md
.
decl
.
type
.
isDtor
(
)
            
if
self
.
receivesMessage
(
md
)
:
                
implicit
=
(
not
isdtor
)
                
returnsems
=
'
resolver
'
if
md
.
decl
.
type
.
isAsync
(
)
else
'
out
'
                
recvDecl
=
MethodDecl
(
                    
md
.
recvMethod
(
)
                    
params
=
md
.
makeCxxParams
(
paramsems
=
'
move
'
returnsems
=
returnsems
                                            
side
=
self
.
side
implicit
=
implicit
)
                    
ret
=
Type
(
'
mozilla
:
:
ipc
:
:
IPCResult
'
)
                    
methodspec
=
MethodSpec
.
VIRTUAL
)
                
if
isctor
or
isdtor
:
                    
defaultRecv
=
MethodDefn
(
recvDecl
)
                    
defaultRecv
.
addstmt
(
StmtReturn
(
ExprCall
(
ExprVar
(
'
IPC_OK
'
)
)
)
)
                    
self
.
cls
.
addstmt
(
defaultRecv
)
                
else
:
                    
recvDecl
.
methodspec
=
MethodSpec
.
PURE
                    
self
.
cls
.
addstmt
(
StmtDecl
(
recvDecl
)
)
        
for
md
in
p
.
messageDecls
:
            
managed
=
md
.
decl
.
type
.
constructedType
(
)
            
if
not
ptype
.
isManagerOf
(
managed
)
or
md
.
decl
.
type
.
isDtor
(
)
:
                
continue
            
actortype
=
md
.
actorDecl
(
)
.
bareType
(
self
.
side
)
            
self
.
cls
.
addstmt
(
StmtDecl
(
MethodDecl
(
                
_allocMethod
(
managed
self
.
side
)
                
params
=
md
.
makeCxxParams
(
side
=
self
.
side
implicit
=
False
)
                
ret
=
actortype
methodspec
=
MethodSpec
.
PURE
)
)
)
            
self
.
cls
.
addstmt
(
StmtDecl
(
MethodDecl
(
                
_deallocMethod
(
managed
self
.
side
)
                
params
=
[
Decl
(
actortype
'
aActor
'
)
]
                
ret
=
Type
.
BOOL
methodspec
=
MethodSpec
.
PURE
)
)
)
        
if
self
.
side
=
=
'
parent
'
:
            
methodspec
=
MethodSpec
.
PURE
        
else
:
            
methodspec
=
MethodSpec
.
VIRTUAL
        
self
.
cls
.
addstmts
(
[
            
Whitespace
.
NL
            
MethodDefn
(
MethodDecl
(
                
_destroyMethod
(
)
.
name
                
params
=
[
Decl
(
_DestroyReason
.
Type
(
)
'
aWhy
'
)
]
                
ret
=
Type
.
VOID
methodspec
=
methodspec
)
)
            
Whitespace
.
NL
        
]
)
        
if
ptype
.
isToplevel
(
)
:
            
processingerror
=
MethodDefn
(
                
MethodDecl
(
p
.
processingErrorVar
(
)
.
name
                           
params
=
[
Param
(
_Result
.
Type
(
)
'
aCode
'
)
                                   
Param
(
Type
(
'
char
'
const
=
True
ptr
=
True
)
'
aReason
'
)
]
                           
methodspec
=
MethodSpec
.
OVERRIDE
)
)
            
shouldcontinue
=
MethodDefn
(
                
MethodDecl
(
p
.
shouldContinueFromTimeoutVar
(
)
.
name
                           
ret
=
Type
.
BOOL
methodspec
=
MethodSpec
.
OVERRIDE
)
)
            
shouldcontinue
.
addstmt
(
StmtReturn
.
TRUE
)
            
entered
=
MethodDefn
(
                
MethodDecl
(
p
.
enteredCxxStackVar
(
)
.
name
methodspec
=
MethodSpec
.
OVERRIDE
)
)
            
exited
=
MethodDefn
(
                
MethodDecl
(
p
.
exitedCxxStackVar
(
)
.
name
methodspec
=
MethodSpec
.
OVERRIDE
)
)
            
enteredcall
=
MethodDefn
(
                
MethodDecl
(
p
.
enteredCallVar
(
)
.
name
methodspec
=
MethodSpec
.
OVERRIDE
)
)
            
exitedcall
=
MethodDefn
(
                
MethodDecl
(
p
.
exitedCallVar
(
)
.
name
methodspec
=
MethodSpec
.
OVERRIDE
)
)
            
self
.
cls
.
addstmts
(
[
processingerror
                               
shouldcontinue
                               
entered
exited
                               
enteredcall
exitedcall
                               
Whitespace
.
NL
]
)
        
self
.
cls
.
addstmts
(
(
            
[
Label
.
PUBLIC
]
            
+
self
.
standardTypedefs
(
)
            
+
[
Whitespace
.
NL
]
        
)
)
        
self
.
cls
.
addstmt
(
Label
.
PUBLIC
)
        
ctor
=
ConstructorDefn
(
ConstructorDecl
(
self
.
clsname
)
)
        
side
=
ExprVar
(
'
mozilla
:
:
ipc
:
:
'
+
self
.
side
.
title
(
)
+
'
Side
'
)
        
if
ptype
.
isToplevel
(
)
:
            
name
=
ExprLiteral
.
String
(
_actorName
(
p
.
name
self
.
side
)
)
            
ctor
.
memberinits
=
[
                
ExprMemberInit
(
ExprVar
(
'
mozilla
:
:
ipc
:
:
IToplevelProtocol
'
)
                               
[
name
_protocolId
(
ptype
)
side
]
)
                
ExprMemberInit
(
p
.
stateVar
(
)
                               
[
p
.
startState
(
)
]
)
            
]
        
else
:
            
ctor
.
memberinits
=
[
                
ExprMemberInit
(
ExprVar
(
'
mozilla
:
:
ipc
:
:
IProtocol
'
)
[
side
]
)
                
ExprMemberInit
(
p
.
stateVar
(
)
                               
[
p
.
deadState
(
)
]
)
            
]
        
ctor
.
addstmt
(
StmtExpr
(
ExprCall
(
ExprVar
(
'
MOZ_COUNT_CTOR
'
)
                                       
[
ExprVar
(
self
.
clsname
)
]
)
)
)
        
self
.
cls
.
addstmts
(
[
ctor
Whitespace
.
NL
]
)
        
dtor
=
DestructorDefn
(
            
DestructorDecl
(
self
.
clsname
methodspec
=
MethodSpec
.
VIRTUAL
)
)
        
dtor
.
addstmt
(
StmtExpr
(
ExprCall
(
ExprVar
(
'
MOZ_COUNT_DTOR
'
)
                                       
[
ExprVar
(
self
.
clsname
)
]
)
)
)
        
self
.
cls
.
addstmts
(
[
dtor
Whitespace
.
NL
]
)
        
if
not
ptype
.
isToplevel
(
)
:
            
if
1
=
=
len
(
p
.
managers
)
:
                
managertype
=
p
.
managerActorType
(
self
.
side
ptr
=
True
)
                
managermeth
=
MethodDefn
(
MethodDecl
(
                    
'
Manager
'
ret
=
managertype
const
=
True
)
)
                
managerexp
=
ExprCall
(
ExprVar
(
'
IProtocol
:
:
Manager
'
)
args
=
[
]
)
                
managermeth
.
addstmt
(
StmtReturn
(
                    
ExprCast
(
managerexp
managertype
static
=
True
)
)
)
                
self
.
cls
.
addstmts
(
[
managermeth
Whitespace
.
NL
]
)
        
def
actorFromIter
(
itervar
)
:
            
return
ExprCall
(
ExprSelect
(
ExprCall
(
ExprSelect
(
itervar
'
.
'
'
Get
'
)
)
                                       
'
-
>
'
'
GetKey
'
)
)
        
def
forLoopOverHashtable
(
hashtable
itervar
const
=
False
)
:
            
return
StmtFor
(
                
init
=
Param
(
Type
.
AUTO
itervar
.
name
                           
ExprCall
(
ExprSelect
(
hashtable
'
.
'
'
ConstIter
'
if
const
else
'
Iter
'
)
)
)
                
cond
=
ExprNot
(
ExprCall
(
ExprSelect
(
itervar
'
.
'
'
Done
'
)
)
)
                
update
=
ExprCall
(
ExprSelect
(
itervar
'
.
'
'
Next
'
)
)
)
        
for
managed
in
ptype
.
manages
:
            
arrvar
=
ExprVar
(
'
aArr
'
)
            
meth
=
MethodDefn
(
MethodDecl
(
                
p
.
managedMethod
(
managed
self
.
side
)
.
name
                
params
=
[
Decl
(
_cxxArrayType
(
p
.
managedCxxType
(
managed
self
.
side
)
ref
=
True
)
                              
arrvar
.
name
)
]
                
const
=
True
)
)
            
meth
.
addstmt
(
StmtExpr
(
                
ExprCall
(
ExprSelect
(
p
.
managedVar
(
managed
self
.
side
)
                                    
'
.
'
'
ToArray
'
)
                         
args
=
[
arrvar
]
)
)
)
            
refmeth
=
MethodDefn
(
MethodDecl
(
                
p
.
managedMethod
(
managed
self
.
side
)
.
name
                
params
=
[
]
                
ret
=
p
.
managedVarType
(
managed
self
.
side
const
=
True
ref
=
True
)
                
const
=
True
)
)
            
refmeth
.
addstmt
(
StmtReturn
(
p
.
managedVar
(
managed
self
.
side
)
)
)
            
self
.
cls
.
addstmts
(
[
meth
refmeth
Whitespace
.
NL
]
)
        
msgvar
=
ExprVar
(
'
msg__
'
)
        
self
.
msgvar
=
msgvar
        
replyvar
=
ExprVar
(
'
reply__
'
)
        
self
.
replyvar
=
replyvar
        
itervar
=
ExprVar
(
'
iter__
'
)
        
self
.
itervar
=
itervar
        
var
=
ExprVar
(
'
v__
'
)
        
self
.
var
=
var
        
handlevar
=
ExprVar
(
'
handle__
'
)
        
self
.
handlevar
=
handlevar
        
msgtype
=
ExprCall
(
ExprSelect
(
msgvar
'
.
'
'
type
'
)
[
]
)
        
self
.
asyncSwitch
=
StmtSwitch
(
msgtype
)
        
self
.
syncSwitch
=
None
        
self
.
interruptSwitch
=
None
        
if
toplevel
.
isSync
(
)
or
toplevel
.
isInterrupt
(
)
:
            
self
.
syncSwitch
=
StmtSwitch
(
msgtype
)
            
if
toplevel
.
isInterrupt
(
)
:
                
self
.
interruptSwitch
=
StmtSwitch
(
msgtype
)
        
for
md
in
p
.
messageDecls
:
            
self
.
visitMessageDecl
(
md
)
        
default
=
StmtBlock
(
)
        
default
.
addstmt
(
StmtReturn
(
_Result
.
NotKnown
)
)
        
self
.
asyncSwitch
.
addcase
(
DefaultLabel
(
)
default
)
        
if
toplevel
.
isSync
(
)
or
toplevel
.
isInterrupt
(
)
:
            
self
.
syncSwitch
.
addcase
(
DefaultLabel
(
)
default
)
            
if
toplevel
.
isInterrupt
(
)
:
                
self
.
interruptSwitch
.
addcase
(
DefaultLabel
(
)
default
)
        
if
1
or
ptype
.
isManager
(
)
:
            
self
.
cls
.
addstmts
(
self
.
implementManagerIface
(
)
)
        
def
makeHandlerMethod
(
name
switch
hasReply
dispatches
=
False
)
:
            
params
=
[
Decl
(
Type
(
'
Message
'
const
=
True
ref
=
True
)
msgvar
.
name
)
]
            
if
hasReply
:
                
params
.
append
(
Decl
(
Type
(
'
Message
'
ref
=
True
ptr
=
True
)
                                   
replyvar
.
name
)
)
            
method
=
MethodDefn
(
MethodDecl
(
name
methodspec
=
MethodSpec
.
OVERRIDE
                                           
params
=
params
ret
=
_Result
.
Type
(
)
)
)
            
if
not
switch
:
                
crash
=
StmtExpr
(
ExprCall
(
                    
ExprVar
(
'
MOZ_ASSERT_UNREACHABLE
'
)
                    
args
=
[
ExprLiteral
.
String
(
'
message
protocol
not
supported
'
)
]
)
)
                
method
.
addstmts
(
[
crash
StmtReturn
(
_Result
.
NotKnown
)
]
)
                
return
method
            
if
dispatches
:
                
routevar
=
ExprVar
(
'
route__
'
)
                
routedecl
=
StmtDecl
(
                    
Decl
(
_actorIdType
(
)
routevar
.
name
)
                    
init
=
ExprCall
(
ExprSelect
(
msgvar
'
.
'
'
routing_id
'
)
)
)
                
routeif
=
StmtIf
(
ExprBinary
(
                    
ExprVar
(
'
MSG_ROUTING_CONTROL
'
)
'
!
=
'
routevar
)
)
                
routedvar
=
ExprVar
(
'
routed__
'
)
                
routeif
.
ifb
.
addstmt
(
                    
StmtDecl
(
Decl
(
Type
(
'
IProtocol
'
ptr
=
True
)
                                  
routedvar
.
name
)
                             
_lookupListener
(
routevar
)
)
)
                
failif
=
StmtIf
(
ExprPrefixUnop
(
routedvar
'
!
'
)
)
                
failif
.
ifb
.
addstmt
(
StmtReturn
(
_Result
.
RouteError
)
)
                
routeif
.
ifb
.
addstmt
(
failif
)
                
routeif
.
ifb
.
addstmt
(
StmtReturn
(
ExprCall
(
                    
ExprSelect
(
routedvar
'
-
>
'
name
)
                    
args
=
[
ExprVar
(
p
.
name
)
for
p
in
params
]
)
)
)
                
method
.
addstmts
(
[
routedecl
routeif
Whitespace
.
NL
]
)
            
if
ptype
.
hasReentrantDelete
:
                
msgVar
=
ExprVar
(
params
[
0
]
.
name
)
                
ifdying
=
StmtIf
(
ExprBinary
(
                    
ExprBinary
(
ExprVar
(
'
mLivenessState
'
)
'
=
=
'
self
.
protocol
.
dyingState
(
)
)
                    
'
&
&
'
                    
ExprBinary
(
                        
ExprBinary
(
ExprCall
(
ExprSelect
(
msgVar
'
.
'
'
is_reply
'
)
)
                                   
'
!
=
'
ExprLiteral
.
TRUE
)
                        
'
|
|
'
                        
ExprBinary
(
ExprCall
(
ExprSelect
(
msgVar
'
.
'
'
is_interrupt
'
)
)
                                   
'
!
=
'
ExprLiteral
.
TRUE
)
)
)
)
                
ifdying
.
addifstmts
(
[
                    
_fatalError
(
'
incoming
message
racing
with
actor
deletion
'
)
                    
StmtReturn
(
_Result
.
Processed
)
]
)
                
method
.
addstmt
(
ifdying
)
            
if
switch
.
nr_cases
>
1
:
                
method
.
addstmt
(
switch
)
            
else
:
                
method
.
addstmt
(
StmtReturn
(
_Result
.
NotKnown
)
)
            
return
method
        
dispatches
=
(
ptype
.
isToplevel
(
)
and
ptype
.
isManager
(
)
)
        
self
.
cls
.
addstmts
(
[
            
makeHandlerMethod
(
'
OnMessageReceived
'
self
.
asyncSwitch
                              
hasReply
=
False
dispatches
=
dispatches
)
            
Whitespace
.
NL
        
]
)
        
self
.
cls
.
addstmts
(
[
            
makeHandlerMethod
(
'
OnMessageReceived
'
self
.
syncSwitch
                              
hasReply
=
True
dispatches
=
dispatches
)
            
Whitespace
.
NL
        
]
)
        
self
.
cls
.
addstmts
(
[
            
makeHandlerMethod
(
'
OnCallReceived
'
self
.
interruptSwitch
                              
hasReply
=
True
dispatches
=
dispatches
)
            
Whitespace
.
NL
        
]
)
        
destroysubtreevar
=
ExprVar
(
'
DestroySubtree
'
)
        
deallocsubtreevar
=
ExprVar
(
'
DeallocSubtree
'
)
        
deallocshmemvar
=
ExprVar
(
'
DeallocShmems
'
)
        
deallocselfvar
=
ExprVar
(
'
Dealloc
'
+
_actorName
(
ptype
.
name
(
)
self
.
side
)
)
        
gettypetag
=
MethodDefn
(
            
MethodDecl
(
'
GetProtocolTypeId
'
ret
=
_actorTypeTagType
(
)
                       
methodspec
=
MethodSpec
.
OVERRIDE
)
)
        
gettypetag
.
addstmt
(
StmtReturn
(
_protocolId
(
ptype
)
)
)
        
self
.
cls
.
addstmts
(
[
gettypetag
Whitespace
.
NL
]
)
        
if
ptype
.
isToplevel
(
)
:
            
onclose
=
MethodDefn
(
MethodDecl
(
'
OnChannelClose
'
                                            
methodspec
=
MethodSpec
.
OVERRIDE
)
)
            
onclose
.
addstmts
(
[
                
StmtExpr
(
ExprCall
(
destroysubtreevar
                                  
args
=
[
_DestroyReason
.
NormalShutdown
]
)
)
                
StmtExpr
(
ExprCall
(
deallocsubtreevar
)
)
                
StmtExpr
(
ExprCall
(
deallocshmemvar
)
)
                
StmtExpr
(
ExprCall
(
deallocselfvar
)
)
            
]
)
            
self
.
cls
.
addstmts
(
[
onclose
Whitespace
.
NL
]
)
            
onerror
=
MethodDefn
(
MethodDecl
(
'
OnChannelError
'
                                            
methodspec
=
MethodSpec
.
OVERRIDE
)
)
            
onerror
.
addstmts
(
[
                
StmtExpr
(
ExprCall
(
destroysubtreevar
                                  
args
=
[
_DestroyReason
.
AbnormalShutdown
]
)
)
                
StmtExpr
(
ExprCall
(
deallocsubtreevar
)
)
                
StmtExpr
(
ExprCall
(
deallocshmemvar
)
)
                
StmtExpr
(
ExprCall
(
deallocselfvar
)
)
            
]
)
            
self
.
cls
.
addstmts
(
[
onerror
Whitespace
.
NL
]
)
        
if
(
ptype
.
isToplevel
(
)
and
ptype
.
isInterrupt
(
)
)
:
            
processnative
=
MethodDefn
(
                
MethodDecl
(
'
ProcessNativeEventsInInterruptCall
'
ret
=
Type
.
VOID
)
)
            
processnative
.
addstmts
(
[
                
CppDirective
(
'
ifdef
'
'
OS_WIN
'
)
                
StmtExpr
(
ExprCall
(
                    
ExprSelect
(
ExprCall
(
ExprSelect
(
ExprCall
(
ExprVar
(
'
DowncastState
'
)
)
                                                   
'
-
>
'
                                                   
'
GetIPCChannel
'
)
)
                               
'
-
>
'
                               
'
ProcessNativeEventsInInterruptCall
'
)
)
)
                
CppDirective
(
'
else
'
)
                
_fatalError
(
'
This
method
is
Windows
-
only
'
)
                
CppDirective
(
'
endif
'
)
            
]
)
            
self
.
cls
.
addstmts
(
[
processnative
Whitespace
.
NL
]
)
        
self
.
cls
.
addstmt
(
Label
.
PRIVATE
)
        
whyvar
=
ExprVar
(
'
why
'
)
        
subtreewhyvar
=
ExprVar
(
'
subtreewhy
'
)
        
kidsvar
=
ExprVar
(
'
kids
'
)
        
itervar
=
ExprVar
(
'
iter
'
)
        
destroysubtree
=
MethodDefn
(
MethodDecl
(
            
destroysubtreevar
.
name
            
params
=
[
Decl
(
_DestroyReason
.
Type
(
)
whyvar
.
name
)
]
)
)
        
if
ptype
.
isManaged
(
)
:
            
destroysubtree
.
addstmt
(
                
Whitespace
(
'
/
/
Unregister
from
our
manager
.
\
n
'
indent
=
True
)
)
            
destroysubtree
.
addstmts
(
self
.
unregisterActor
(
)
)
            
destroysubtree
.
addstmt
(
Whitespace
.
NL
)
        
if
ptype
.
isManager
(
)
:
            
destroysubtree
.
addstmts
(
[
                
StmtDecl
(
                    
Decl
(
_DestroyReason
.
Type
(
)
subtreewhyvar
.
name
)
                    
init
=
ExprConditional
(
                        
ExprBinary
(
                            
ExprBinary
(
whyvar
'
=
=
'
                                       
_DestroyReason
.
Deletion
)
                            
'
|
|
'
                            
ExprBinary
(
whyvar
'
=
=
'
                                       
_DestroyReason
.
FailedConstructor
)
)
                        
_DestroyReason
.
AncestorDeletion
whyvar
)
)
                
Whitespace
.
NL
            
]
)
        
for
managed
in
ptype
.
manages
:
            
managedVar
=
p
.
managedVar
(
managed
self
.
side
)
            
kidvar
=
ExprVar
(
'
kid
'
)
            
foreachdestroy
=
StmtRangedFor
(
kidvar
kidsvar
)
            
foreachdestroy
.
addstmt
(
                
Whitespace
(
'
/
/
Guarding
against
a
child
removing
a
sibling
from
the
list
during
the
iteration
.
\
n
'
indent
=
True
)
)
            
ifhas
=
StmtIf
(
_callHasManagedActor
(
managedVar
kidvar
)
)
            
ifhas
.
addifstmt
(
StmtExpr
(
ExprCall
(
                
ExprSelect
(
kidvar
'
-
>
'
destroysubtreevar
.
name
)
                
args
=
[
subtreewhyvar
]
)
)
)
            
foreachdestroy
.
addstmt
(
ifhas
)
            
block
=
StmtBlock
(
)
            
block
.
addstmts
(
[
                
Whitespace
(
                    
'
/
/
Recursively
shutting
down
%
s
kids
\
n
'
%
(
managed
.
name
(
)
)
                    
indent
=
True
)
                
StmtDecl
(
                    
Decl
(
_cxxArrayType
(
p
.
managedCxxType
(
managed
self
.
side
)
)
kidsvar
.
name
)
)
                
Whitespace
(
                    
'
/
/
Accumulate
kids
into
a
stable
structure
to
iterate
over
\
n
'
                    
indent
=
True
)
                
StmtExpr
(
ExprCall
(
p
.
managedMethod
(
managed
self
.
side
)
                                  
args
=
[
kidsvar
]
)
)
                
foreachdestroy
            
]
)
            
destroysubtree
.
addstmt
(
block
)
        
if
len
(
ptype
.
manages
)
:
            
destroysubtree
.
addstmt
(
Whitespace
.
NL
)
        
rejectPendingResponsesMethod
=
ExprSelect
(
self
.
protocol
.
callGetChannel
(
)
                                                  
'
-
>
'
                                                  
'
RejectPendingResponsesForActor
'
)
        
destroysubtree
.
addstmts
(
[
Whitespace
(
'
/
/
Reject
owning
pending
responses
.
\
n
'
                                            
indent
=
True
)
                                 
StmtExpr
(
ExprCall
(
rejectPendingResponsesMethod
                                                   
args
=
[
ExprVar
(
'
this
'
)
]
)
)
                                 
Whitespace
.
NL
                                 
]
)
        
destroysubtree
.
addstmts
(
[
Whitespace
(
'
/
/
Finally
destroy
"
us
"
.
\
n
'
                                            
indent
=
True
)
                                 
StmtExpr
(
ExprCall
(
_destroyMethod
(
)
                                                   
args
=
[
whyvar
]
)
)
                                 
]
)
        
self
.
cls
.
addstmts
(
[
destroysubtree
Whitespace
.
NL
]
)
        
deallocsubtree
=
MethodDefn
(
MethodDecl
(
deallocsubtreevar
.
name
)
)
        
for
managed
in
ptype
.
manages
:
            
managedVar
=
p
.
managedVar
(
managed
self
.
side
)
            
foreachrecurse
=
forLoopOverHashtable
(
managedVar
itervar
)
            
foreachrecurse
.
addstmt
(
StmtExpr
(
ExprCall
(
                
ExprSelect
(
actorFromIter
(
itervar
)
'
-
>
'
deallocsubtreevar
.
name
)
)
)
)
            
foreachdealloc
=
forLoopOverHashtable
(
managedVar
itervar
)
            
foreachdealloc
.
addstmts
(
[
                
StmtExpr
(
self
.
thisCall
(
_deallocMethod
(
managed
self
.
side
)
                                       
[
actorFromIter
(
itervar
)
]
)
)
            
]
)
            
block
=
StmtBlock
(
)
            
block
.
addstmts
(
[
                
Whitespace
(
                    
'
/
/
Recursively
deleting
%
s
kids
\
n
'
%
(
managed
.
name
(
)
)
                    
indent
=
True
)
                
foreachrecurse
                
Whitespace
.
NL
                
foreachdealloc
                
StmtExpr
(
_callClearManagedActors
(
managedVar
)
)
            
]
)
            
deallocsubtree
.
addstmt
(
block
)
        
self
.
cls
.
addstmts
(
[
deallocsubtree
Whitespace
.
NL
]
)
        
if
ptype
.
isToplevel
(
)
:
            
deallocself
=
MethodDefn
(
MethodDecl
(
                
deallocselfvar
.
name
methodspec
=
MethodSpec
.
VIRTUAL
)
)
            
self
.
cls
.
addstmts
(
[
deallocself
Whitespace
.
NL
]
)
        
self
.
cls
.
addstmt
(
StmtDecl
(
Decl
(
self
.
protocol
.
fqStateType
(
)
p
.
stateVar
(
)
.
name
)
)
)
        
for
managed
in
ptype
.
manages
:
            
self
.
cls
.
addstmts
(
[
                
StmtDecl
(
Decl
(
                    
p
.
managedVarType
(
managed
self
.
side
)
                    
p
.
managedVar
(
managed
self
.
side
)
.
name
)
)
]
)
    
def
implementManagerIface
(
self
)
:
        
p
=
self
.
protocol
        
protocolbase
=
Type
(
'
IProtocol
'
ptr
=
True
)
        
methods
=
[
]
        
if
p
.
decl
.
type
.
isToplevel
(
)
:
            
if
p
.
subtreeUsesShmem
(
)
:
                
self
.
asyncSwitch
.
addcase
(
                    
CaseLabel
(
'
SHMEM_CREATED_MESSAGE_TYPE
'
)
                    
self
.
genShmemCreatedHandler
(
)
)
                
self
.
asyncSwitch
.
addcase
(
                    
CaseLabel
(
'
SHMEM_DESTROYED_MESSAGE_TYPE
'
)
                    
self
.
genShmemDestroyedHandler
(
)
)
            
else
:
                
abort
=
StmtBlock
(
)
                
abort
.
addstmts
(
[
                    
_fatalError
(
'
this
protocol
tree
does
not
use
shmem
'
)
                    
StmtReturn
(
_Result
.
NotKnown
)
                
]
)
                
self
.
asyncSwitch
.
addcase
(
                    
CaseLabel
(
'
SHMEM_CREATED_MESSAGE_TYPE
'
)
abort
)
                
self
.
asyncSwitch
.
addcase
(
                    
CaseLabel
(
'
SHMEM_DESTROYED_MESSAGE_TYPE
'
)
abort
)
        
inoutCtorTypes
=
[
]
        
for
msg
in
p
.
messageDecls
:
            
msgtype
=
msg
.
decl
.
type
            
if
msgtype
.
isCtor
(
)
and
msgtype
.
isInout
(
)
:
                
inoutCtorTypes
.
append
(
msgtype
.
constructedType
(
)
)
        
pvar
=
ExprVar
(
'
aProtocolId
'
)
        
listenervar
=
ExprVar
(
'
aListener
'
)
        
removemanagee
=
MethodDefn
(
MethodDecl
(
            
p
.
removeManageeMethod
(
)
.
name
            
params
=
[
Decl
(
_protocolIdType
(
)
pvar
.
name
)
                    
Decl
(
protocolbase
listenervar
.
name
)
]
            
methodspec
=
MethodSpec
.
OVERRIDE
)
)
        
if
not
len
(
p
.
managesStmts
)
:
            
removemanagee
.
addstmts
(
[
_fatalError
(
'
unreached
'
)
StmtReturn
(
)
]
)
        
else
:
            
switchontype
=
StmtSwitch
(
pvar
)
            
for
managee
in
p
.
managesStmts
:
                
case
=
StmtBlock
(
)
                
actorvar
=
ExprVar
(
'
actor
'
)
                
manageeipdltype
=
managee
.
decl
.
type
                
manageecxxtype
=
_cxxBareType
(
ipdl
.
type
.
ActorType
(
manageeipdltype
)
                                              
self
.
side
)
                
manageearray
=
p
.
managedVar
(
manageeipdltype
self
.
side
)
                
containervar
=
ExprVar
(
'
container
'
)
                
case
.
addstmts
(
[
                    
StmtDecl
(
Decl
(
manageecxxtype
actorvar
.
name
)
                             
ExprCast
(
listenervar
manageecxxtype
static
=
True
)
)
                    
StmtDecl
(
Decl
(
Type
(
'
auto
'
ref
=
True
)
containervar
.
name
)
                             
manageearray
)
                    
_abortIfFalse
(
                        
_callHasManagedActor
(
containervar
actorvar
)
                        
"
actor
not
managed
by
this
!
"
)
                    
Whitespace
.
NL
                    
StmtExpr
(
_callRemoveManagedActor
(
containervar
actorvar
)
)
                    
StmtExpr
(
self
.
thisCall
(
_deallocMethod
(
manageeipdltype
self
.
side
)
                                           
[
actorvar
]
)
)
                    
StmtReturn
(
)
                
]
)
                
switchontype
.
addcase
(
CaseLabel
(
_protocolId
(
manageeipdltype
)
.
name
)
                                     
case
)
            
default
=
StmtBlock
(
)
            
default
.
addstmts
(
[
_fatalError
(
'
unreached
'
)
StmtReturn
(
)
]
)
            
switchontype
.
addcase
(
DefaultLabel
(
)
default
)
            
removemanagee
.
addstmt
(
switchontype
)
        
return
methods
+
[
removemanagee
Whitespace
.
NL
]
    
def
genShmemCreatedHandler
(
self
)
:
        
p
=
self
.
protocol
        
assert
p
.
decl
.
type
.
isToplevel
(
)
        
case
=
StmtBlock
(
)
        
ifstmt
=
StmtIf
(
ExprNot
(
ExprCall
(
ExprVar
(
'
ShmemCreated
'
)
args
=
[
self
.
msgvar
]
)
)
)
        
case
.
addstmts
(
[
            
ifstmt
            
StmtReturn
(
_Result
.
Processed
)
        
]
)
        
ifstmt
.
addifstmt
(
StmtReturn
(
_Result
.
PayloadError
)
)
        
return
case
    
def
genShmemDestroyedHandler
(
self
)
:
        
p
=
self
.
protocol
        
assert
p
.
decl
.
type
.
isToplevel
(
)
        
case
=
StmtBlock
(
)
        
ifstmt
=
StmtIf
(
ExprNot
(
ExprCall
(
ExprVar
(
'
ShmemDestroyed
'
)
args
=
[
self
.
msgvar
]
)
)
)
        
case
.
addstmts
(
[
            
ifstmt
            
StmtReturn
(
_Result
.
Processed
)
        
]
)
        
ifstmt
.
addifstmt
(
StmtReturn
(
_Result
.
PayloadError
)
)
        
return
case
    
def
thisCall
(
self
function
args
)
:
        
return
ExprCall
(
ExprVar
(
function
)
args
=
args
)
    
def
visitMessageDecl
(
self
md
)
:
        
isctor
=
md
.
decl
.
type
.
isCtor
(
)
        
isdtor
=
md
.
decl
.
type
.
isDtor
(
)
        
decltype
=
md
.
decl
.
type
        
sendmethod
=
None
        
movesendmethod
=
None
        
promisesendmethod
=
None
        
recvlbl
recvcase
=
None
None
        
def
addRecvCase
(
lbl
case
)
:
            
if
decltype
.
isAsync
(
)
:
                
self
.
asyncSwitch
.
addcase
(
lbl
case
)
            
elif
decltype
.
isSync
(
)
:
                
self
.
syncSwitch
.
addcase
(
lbl
case
)
            
elif
decltype
.
isInterrupt
(
)
:
                
self
.
interruptSwitch
.
addcase
(
lbl
case
)
            
else
:
                
assert
0
        
if
self
.
sendsMessage
(
md
)
:
            
isasync
=
decltype
.
isAsync
(
)
            
if
isctor
:
                
self
.
cls
.
addstmts
(
[
self
.
genHelperCtor
(
md
)
Whitespace
.
NL
]
)
            
if
isctor
and
isasync
:
                
sendmethod
(
recvlbl
recvcase
)
=
self
.
genAsyncCtor
(
md
)
            
elif
isctor
:
                
sendmethod
=
self
.
genBlockingCtorMethod
(
md
)
            
elif
isdtor
and
isasync
:
                
sendmethod
(
recvlbl
recvcase
)
=
self
.
genAsyncDtor
(
md
)
            
elif
isdtor
:
                
sendmethod
=
self
.
genBlockingDtorMethod
(
md
)
            
elif
isasync
:
                
sendmethod
movesendmethod
promisesendmethod
(
recvlbl
recvcase
)
=
\
                    
self
.
genAsyncSendMethod
(
md
)
            
else
:
                
sendmethod
movesendmethod
=
self
.
genBlockingSendMethod
(
md
)
        
if
isdtor
and
md
.
decl
.
type
.
constructedType
(
)
.
isToplevel
(
)
:
            
sendmethod
=
None
        
if
sendmethod
is
not
None
:
            
self
.
cls
.
addstmts
(
[
sendmethod
Whitespace
.
NL
]
)
        
if
movesendmethod
is
not
None
:
            
self
.
cls
.
addstmts
(
[
movesendmethod
Whitespace
.
NL
]
)
        
if
promisesendmethod
is
not
None
:
            
self
.
cls
.
addstmts
(
[
promisesendmethod
Whitespace
.
NL
]
)
        
if
recvcase
is
not
None
:
            
addRecvCase
(
recvlbl
recvcase
)
            
recvlbl
recvcase
=
None
None
        
if
self
.
receivesMessage
(
md
)
:
            
if
isctor
:
                
recvlbl
recvcase
=
self
.
genCtorRecvCase
(
md
)
            
elif
isdtor
:
                
recvlbl
recvcase
=
self
.
genDtorRecvCase
(
md
)
            
else
:
                
recvlbl
recvcase
=
self
.
genRecvCase
(
md
)
            
if
isdtor
and
md
.
decl
.
type
.
constructedType
(
)
.
isToplevel
(
)
:
                
return
            
addRecvCase
(
recvlbl
recvcase
)
    
def
genAsyncCtor
(
self
md
)
:
        
actor
=
md
.
actorDecl
(
)
        
method
=
MethodDefn
(
self
.
makeSendMethodDecl
(
md
)
)
        
method
.
addstmts
(
self
.
ctorPrologue
(
md
)
+
[
Whitespace
.
NL
]
)
        
msgvar
stmts
=
self
.
makeMessage
(
md
errfnSendCtor
)
        
sendok
sendstmts
=
self
.
sendAsync
(
md
msgvar
)
        
warnif
=
StmtIf
(
ExprNot
(
sendok
)
)
        
warnif
.
addifstmt
(
_printWarningMessage
(
'
Error
sending
constructor
'
)
)
        
method
.
addstmts
(
            
stmts
            
+
self
.
genVerifyMessage
(
md
.
decl
.
type
.
verify
md
.
params
                                    
errfnSendCtor
ExprVar
(
'
msg__
'
)
)
            
+
sendstmts
            
+
[
warnif
               
StmtReturn
(
actor
.
var
(
)
)
]
)
        
lbl
=
CaseLabel
(
md
.
pqReplyId
(
)
)
        
case
=
StmtBlock
(
)
        
case
.
addstmt
(
StmtReturn
(
_Result
.
Processed
)
)
        
return
method
(
lbl
case
)
    
def
genBlockingCtorMethod
(
self
md
)
:
        
actor
=
md
.
actorDecl
(
)
        
method
=
MethodDefn
(
self
.
makeSendMethodDecl
(
md
)
)
        
method
.
addstmts
(
self
.
ctorPrologue
(
md
)
+
[
Whitespace
.
NL
]
)
        
msgvar
stmts
=
self
.
makeMessage
(
md
errfnSendCtor
)
        
replyvar
=
self
.
replyvar
        
sendok
sendstmts
=
self
.
sendBlocking
(
md
msgvar
replyvar
)
        
method
.
addstmts
(
            
stmts
            
+
[
Whitespace
.
NL
                
StmtDecl
(
Decl
(
Type
(
'
Message
'
)
replyvar
.
name
)
)
]
            
+
self
.
genVerifyMessage
(
md
.
decl
.
type
.
verify
md
.
params
                                    
errfnSendCtor
ExprVar
(
'
msg__
'
)
)
            
+
sendstmts
            
+
self
.
failCtorIf
(
md
ExprNot
(
sendok
)
)
)
        
def
errfnCleanupCtor
(
msg
)
:
            
return
self
.
failCtorIf
(
md
ExprLiteral
.
TRUE
)
        
stmts
=
self
.
deserializeReply
(
            
md
ExprAddrOf
(
replyvar
)
self
.
side
            
errfnCleanupCtor
errfnSentinel
(
ExprLiteral
.
NULL
)
)
        
method
.
addstmts
(
stmts
+
[
StmtReturn
(
actor
.
var
(
)
)
]
)
        
return
method
    
def
ctorPrologue
(
self
md
errfn
=
ExprLiteral
.
NULL
idexpr
=
None
)
:
        
actordecl
=
md
.
actorDecl
(
)
        
actorvar
=
actordecl
.
var
(
)
        
actorproto
=
actordecl
.
ipdltype
.
protocol
        
actortype
=
ipdl
.
type
.
ActorType
(
actorproto
)
        
if
idexpr
is
None
:
            
setManagerArgs
=
[
ExprVar
.
THIS
]
        
else
:
            
setManagerArgs
=
[
ExprVar
.
THIS
idexpr
]
        
setmanager
=
ExprCall
(
ExprSelect
(
actorvar
'
-
>
'
'
SetManagerAndRegister
'
)
                              
args
=
setManagerArgs
)
        
return
[
            
self
.
failIfNullActor
(
actorvar
errfn
msg
=
"
Error
constructing
actor
%
s
"
%
                                 
actortype
.
name
(
)
+
self
.
side
.
capitalize
(
)
)
            
StmtExpr
(
setmanager
)
            
StmtExpr
(
_callInsertManagedActor
(
                
self
.
protocol
.
managedVar
(
md
.
decl
.
type
.
constructedType
(
)
                                         
self
.
side
)
                
actorvar
)
)
            
StmtExpr
(
ExprAssn
(
_actorState
(
actorvar
)
                              
_startState
(
md
.
decl
.
type
.
cdtype
.
hasReentrantDelete
)
)
)
        
]
    
def
failCtorIf
(
self
md
cond
)
:
        
actorvar
=
md
.
actorDecl
(
)
.
var
(
)
        
failif
=
StmtIf
(
cond
)
        
if
self
.
side
=
=
'
child
'
:
            
failif
.
addifstmt
(
_fatalError
(
'
constructor
for
actor
failed
'
)
)
        
else
:
            
failif
.
addifstmts
(
self
.
destroyActor
(
md
actorvar
                                                
why
=
_DestroyReason
.
FailedConstructor
)
)
        
failif
.
addifstmt
(
StmtReturn
(
ExprLiteral
.
NULL
)
)
        
return
[
failif
]
    
def
genHelperCtor
(
self
md
)
:
        
helperdecl
=
self
.
makeSendMethodDecl
(
md
)
        
helperdecl
.
params
=
helperdecl
.
params
[
1
:
]
        
helper
=
MethodDefn
(
helperdecl
)
        
callctor
=
self
.
callAllocActor
(
md
retsems
=
'
out
'
side
=
self
.
side
)
        
helper
.
addstmt
(
StmtReturn
(
ExprCall
(
            
ExprVar
(
helperdecl
.
name
)
args
=
[
callctor
]
+
callctor
.
args
)
)
)
        
return
helper
    
def
genAsyncDtor
(
self
md
)
:
        
actor
=
md
.
actorDecl
(
)
        
actorvar
=
actor
.
var
(
)
        
method
=
MethodDefn
(
self
.
makeDtorMethodDecl
(
md
)
)
        
method
.
addstmts
(
self
.
dtorPrologue
(
actorvar
)
)
        
msgvar
stmts
=
self
.
makeMessage
(
md
errfnSendDtor
actorvar
)
        
sendok
sendstmts
=
self
.
sendAsync
(
md
msgvar
actorvar
)
        
method
.
addstmts
(
            
stmts
            
+
self
.
genVerifyMessage
(
md
.
decl
.
type
.
verify
md
.
params
                                    
errfnSendDtor
ExprVar
(
'
msg__
'
)
)
            
+
sendstmts
            
+
[
Whitespace
.
NL
]
            
+
self
.
dtorEpilogue
(
md
actor
.
var
(
)
)
            
+
[
StmtReturn
(
sendok
)
]
)
        
lbl
=
CaseLabel
(
md
.
pqReplyId
(
)
)
        
case
=
StmtBlock
(
)
        
case
.
addstmt
(
StmtReturn
(
_Result
.
Processed
)
)
        
return
method
(
lbl
case
)
    
def
genBlockingDtorMethod
(
self
md
)
:
        
actor
=
md
.
actorDecl
(
)
        
actorvar
=
actor
.
var
(
)
        
method
=
MethodDefn
(
self
.
makeDtorMethodDecl
(
md
)
)
        
method
.
addstmts
(
self
.
dtorPrologue
(
actorvar
)
)
        
msgvar
stmts
=
self
.
makeMessage
(
md
errfnSendDtor
actorvar
)
        
replyvar
=
self
.
replyvar
        
sendok
sendstmts
=
self
.
sendBlocking
(
md
msgvar
replyvar
actorvar
)
        
method
.
addstmts
(
            
stmts
            
+
self
.
genVerifyMessage
(
md
.
decl
.
type
.
verify
md
.
params
                                    
errfnSendDtor
ExprVar
(
'
msg__
'
)
)
            
+
[
Whitespace
.
NL
                
StmtDecl
(
Decl
(
Type
(
'
Message
'
)
replyvar
.
name
)
)
]
            
+
sendstmts
)
        
destmts
=
self
.
deserializeReply
(
            
md
ExprAddrOf
(
replyvar
)
self
.
side
errfnSend
            
errfnSentinel
(
)
actorvar
)
        
ifsendok
=
StmtIf
(
ExprLiteral
.
FALSE
)
        
ifsendok
.
addifstmts
(
destmts
)
        
ifsendok
.
addifstmts
(
[
Whitespace
.
NL
                             
StmtExpr
(
ExprAssn
(
sendok
ExprLiteral
.
FALSE
'
&
=
'
)
)
]
)
        
method
.
addstmt
(
ifsendok
)
        
if
self
.
protocol
.
decl
.
type
.
hasReentrantDelete
:
            
method
.
addstmts
(
self
.
transition
(
md
actor
.
var
(
)
reply
=
True
errorfn
=
errfnUnreachable
)
)
        
method
.
addstmts
(
            
self
.
dtorEpilogue
(
md
actor
.
var
(
)
)
            
+
[
Whitespace
.
NL
StmtReturn
(
sendok
)
]
)
        
return
method
    
def
destroyActor
(
self
md
actorexpr
why
=
_DestroyReason
.
Deletion
)
:
        
if
md
.
decl
.
type
.
isCtor
(
)
:
            
destroyedType
=
md
.
decl
.
type
.
constructedType
(
)
        
else
:
            
destroyedType
=
self
.
protocol
.
decl
.
type
        
managervar
=
ExprVar
(
'
mgr
'
)
        
return
(
[
StmtDecl
(
Decl
(
Type
(
'
IProtocol
'
ptr
=
True
)
managervar
.
name
)
                          
init
=
self
.
protocol
.
managerVar
(
actorexpr
)
)
                 
StmtExpr
(
self
.
callActorDestroy
(
actorexpr
why
)
)
                 
StmtExpr
(
self
.
callDeallocSubtree
(
md
actorexpr
)
)
                 
StmtExpr
(
self
.
callRemoveActor
(
                     
actorexpr
                     
manager
=
managervar
                     
ipdltype
=
destroyedType
)
)
                 
]
)
    
def
dtorPrologue
(
self
actorexpr
)
:
        
return
[
self
.
failIfNullActor
(
actorexpr
)
Whitespace
.
NL
]
    
def
dtorEpilogue
(
self
md
actorexpr
)
:
        
return
self
.
destroyActor
(
md
actorexpr
)
    
def
genRecvAsyncReplyCase
(
self
md
)
:
        
lbl
=
CaseLabel
(
md
.
pqReplyId
(
)
)
        
case
=
StmtBlock
(
)
        
resolve
reason
prologue
desrej
desstmts
=
self
.
deserializeAsyncReply
(
            
md
self
.
side
errfnRecv
errfnSentinel
(
_Result
.
ValuError
)
)
        
ifnocallback
=
StmtIf
(
ExprNot
(
ExprVar
(
'
callback
'
)
)
)
        
ifnocallback
.
addifstmts
(
errfnRecv
(
"
Error
unknown
callback
"
                                          
_Result
.
ProcessingError
)
)
        
if
len
(
md
.
returns
)
>
1
:
            
resolvetype
=
_tuple
(
[
d
.
bareType
(
self
.
side
)
for
d
in
md
.
returns
]
)
            
resolvearg
=
ExprCall
(
ExprVar
(
'
MakeTuple
'
)
                                  
args
=
[
ExprMove
(
p
.
var
(
)
)
for
p
in
md
.
returns
]
)
        
else
:
            
resolvetype
=
md
.
returns
[
0
]
.
bareType
(
self
.
side
)
            
resolvearg
=
ExprMove
(
md
.
returns
[
0
]
.
var
(
)
)
        
untypedcallback
=
Type
(
"
MessageChannel
:
:
UntypedCallbackHolder
"
)
        
callbackptr
=
Type
(
"
MessageChannel
:
:
CallbackHolder
"
T
=
resolvetype
)
        
callbackptr
.
ptr
=
True
        
callback
=
ExprVar
(
'
callback
'
)
        
getcallback
=
[
Whitespace
.
NL
                       
StmtDecl
(
Decl
(
_uniqueptr
(
untypedcallback
)
'
untypedCallback
'
)
                                
init
=
ExprCall
(
ExprSelect
(
self
.
protocol
.
callGetChannel
(
)
                                                         
'
-
>
'
'
PopCallback
'
)
                                              
args
=
[
self
.
msgvar
]
)
)
                       
StmtDecl
(
Decl
(
callbackptr
callback
.
name
)
                                
init
=
ExprCast
(
ExprCall
(
ExprSelect
(
ExprVar
(
'
untypedCallback
'
)
                                                                  
'
.
'
'
get
'
)
)
                                              
callbackptr
                                              
static
=
True
)
)
                       
ifnocallback
]
        
resolvecallback
=
[
StmtExpr
(
ExprCall
(
ExprSelect
(
callback
'
-
>
'
'
Resolve
'
)
                                             
args
=
[
resolvearg
]
)
)
]
        
rejectcallback
=
[
StmtExpr
(
ExprCall
(
ExprSelect
(
callback
'
-
>
'
'
Reject
'
)
                                            
args
=
[
ExprMove
(
reason
)
]
)
)
]
        
ifresolve
=
StmtIf
(
resolve
)
        
ifresolve
.
addifstmts
(
desstmts
)
        
ifresolve
.
addifstmts
(
resolvecallback
)
        
ifresolve
.
addelsestmts
(
desrej
)
        
ifresolve
.
addelsestmts
(
rejectcallback
)
        
case
.
addstmts
(
prologue
)
        
case
.
addstmts
(
getcallback
)
        
case
.
addstmt
(
ifresolve
)
        
case
.
addstmt
(
StmtReturn
(
_Result
.
Processed
)
)
        
return
(
lbl
case
)
    
staticmethod
    
def
hasMoveableParams
(
md
)
:
        
for
param
in
md
.
decl
.
type
.
params
:
            
if
_cxxTypeCanMoveSend
(
param
)
:
                
return
True
        
return
False
    
def
genAsyncSendMethod
(
self
md
)
:
        
method
=
MethodDefn
(
self
.
makeSendMethodDecl
(
md
)
)
        
msgvar
stmts
=
self
.
makeMessage
(
md
errfnSend
)
        
retvar
sendstmts
=
self
.
sendAsync
(
md
msgvar
)
        
method
.
addstmts
(
stmts
                        
+
[
Whitespace
.
NL
]
                        
+
self
.
genVerifyMessage
(
md
.
decl
.
type
.
verify
md
.
params
                                                
errfnSend
ExprVar
(
'
msg__
'
)
)
                        
+
sendstmts
                        
+
[
StmtReturn
(
retvar
)
]
)
        
if
self
.
hasMoveableParams
(
md
)
:
            
movemethod
=
MethodDefn
(
self
.
makeSendMethodDecl
(
md
paramsems
=
'
move
'
)
)
            
movemethod
.
addstmts
(
stmts
                                
+
[
Whitespace
.
NL
]
                                
+
self
.
genVerifyMessage
(
md
.
decl
.
type
.
verify
md
.
params
                                                        
errfnSend
ExprVar
(
'
msg__
'
)
)
                                
+
sendstmts
                                
+
[
StmtReturn
(
retvar
)
]
)
        
else
:
            
movemethod
=
None
        
if
md
.
returns
:
            
promisemethod
=
MethodDefn
(
self
.
makeSendMethodDecl
(
md
promise
=
True
)
)
            
stmts
=
self
.
sendAsyncWithPromise
(
md
)
            
promisemethod
.
addstmts
(
stmts
)
            
(
lbl
case
)
=
self
.
genRecvAsyncReplyCase
(
md
)
        
else
:
            
(
promisemethod
lbl
case
)
=
(
None
None
None
)
        
return
method
movemethod
promisemethod
(
lbl
case
)
    
def
genBlockingSendMethod
(
self
md
fromActor
=
None
)
:
        
method
=
MethodDefn
(
self
.
makeSendMethodDecl
(
md
)
)
        
msgvar
serstmts
=
self
.
makeMessage
(
md
errfnSend
fromActor
)
        
replyvar
=
self
.
replyvar
        
sendok
sendstmts
=
self
.
sendBlocking
(
md
msgvar
replyvar
)
        
failif
=
StmtIf
(
ExprNot
(
sendok
)
)
        
failif
.
addifstmt
(
StmtReturn
.
FALSE
)
        
desstmts
=
self
.
deserializeReply
(
            
md
ExprAddrOf
(
replyvar
)
self
.
side
errfnSend
errfnSentinel
(
)
)
        
method
.
addstmts
(
            
serstmts
            
+
self
.
genVerifyMessage
(
md
.
decl
.
type
.
verify
md
.
params
errfnSend
                                    
ExprVar
(
'
msg__
'
)
)
            
+
[
Whitespace
.
NL
                
StmtDecl
(
Decl
(
Type
(
'
Message
'
)
replyvar
.
name
)
)
]
            
+
sendstmts
            
+
[
failif
]
            
+
desstmts
            
+
[
Whitespace
.
NL
                
StmtReturn
.
TRUE
]
)
        
if
self
.
hasMoveableParams
(
md
)
:
            
movemethod
=
MethodDefn
(
self
.
makeSendMethodDecl
(
md
paramsems
=
'
move
'
)
)
            
movemethod
.
addstmts
(
                
serstmts
                
+
self
.
genVerifyMessage
(
md
.
decl
.
type
.
verify
md
.
params
errfnSend
                                        
ExprVar
(
'
msg__
'
)
)
                
+
[
Whitespace
.
NL
                    
StmtDecl
(
Decl
(
Type
(
'
Message
'
)
replyvar
.
name
)
)
]
                
+
sendstmts
                
+
[
failif
]
                
+
desstmts
                
+
[
Whitespace
.
NL
                    
StmtReturn
.
TRUE
]
)
        
else
:
            
movemethod
=
None
        
return
method
movemethod
    
def
genCtorRecvCase
(
self
md
)
:
        
lbl
=
CaseLabel
(
md
.
pqMsgId
(
)
)
        
case
=
StmtBlock
(
)
        
actorvar
=
md
.
actorDecl
(
)
.
var
(
)
        
actorhandle
=
self
.
handlevar
        
stmts
=
self
.
deserializeMessage
(
md
self
.
side
errfnRecv
                                        
errfnSent
=
errfnSentinel
(
_Result
.
ValuError
)
)
        
idvar
saveIdStmts
=
self
.
saveActorId
(
md
)
        
case
.
addstmts
(
            
stmts
            
+
self
.
transition
(
md
errorfn
=
errfnRecv
)
            
+
[
StmtDecl
(
Decl
(
r
.
bareType
(
self
.
side
)
r
.
var
(
)
.
name
)
)
                
for
r
in
md
.
returns
]
            
+
[
StmtExpr
(
ExprAssn
(
                
actorvar
                
self
.
callAllocActor
(
md
retsems
=
'
in
'
side
=
self
.
side
)
)
)
]
            
+
self
.
ctorPrologue
(
md
errfn
=
_Result
.
ValuError
                                
idexpr
=
_actorHId
(
actorhandle
)
)
            
+
[
Whitespace
.
NL
]
            
+
saveIdStmts
            
+
self
.
invokeRecvHandler
(
md
)
            
+
self
.
makeReply
(
md
errfnRecv
idvar
)
            
+
self
.
genVerifyMessage
(
md
.
decl
.
type
.
verify
md
.
returns
errfnRecv
                                    
self
.
replyvar
)
            
+
[
Whitespace
.
NL
                
StmtReturn
(
_Result
.
Processed
)
]
)
        
return
lbl
case
    
def
genDtorRecvCase
(
self
md
)
:
        
lbl
=
CaseLabel
(
md
.
pqMsgId
(
)
)
        
case
=
StmtBlock
(
)
        
stmts
=
self
.
deserializeMessage
(
md
self
.
side
errfnRecv
                                        
errfnSent
=
errfnSentinel
(
_Result
.
ValuError
)
)
        
idvar
saveIdStmts
=
self
.
saveActorId
(
md
)
        
case
.
addstmts
(
            
stmts
            
+
self
.
transition
(
md
errorfn
=
errfnRecv
)
            
+
[
StmtDecl
(
Decl
(
r
.
bareType
(
self
.
side
)
r
.
var
(
)
.
name
)
)
                
for
r
in
md
.
returns
]
            
+
self
.
invokeRecvHandler
(
md
implicit
=
False
)
            
+
[
Whitespace
.
NL
]
            
+
saveIdStmts
            
+
self
.
makeReply
(
md
errfnRecv
routingId
=
idvar
)
            
+
[
Whitespace
.
NL
]
            
+
self
.
genVerifyMessage
(
md
.
decl
.
type
.
verify
md
.
returns
errfnRecv
                                    
self
.
replyvar
)
            
+
self
.
dtorEpilogue
(
md
md
.
actorDecl
(
)
.
var
(
)
)
            
+
[
Whitespace
.
NL
                
StmtReturn
(
_Result
.
Processed
)
]
)
        
return
lbl
case
    
def
genRecvCase
(
self
md
)
:
        
lbl
=
CaseLabel
(
md
.
pqMsgId
(
)
)
        
case
=
StmtBlock
(
)
        
stmts
=
self
.
deserializeMessage
(
md
self
.
side
errfn
=
errfnRecv
                                        
errfnSent
=
errfnSentinel
(
_Result
.
ValuError
)
)
        
idvar
saveIdStmts
=
self
.
saveActorId
(
md
)
        
declstmts
=
[
StmtDecl
(
Decl
(
r
.
bareType
(
self
.
side
)
r
.
var
(
)
.
name
)
)
                     
for
r
in
md
.
returns
]
        
if
md
.
decl
.
type
.
isAsync
(
)
and
md
.
returns
:
            
declstmts
=
self
.
makeResolver
(
md
errfnRecv
routingId
=
idvar
)
        
case
.
addstmts
(
            
stmts
            
+
self
.
transition
(
md
errorfn
=
errfnRecv
)
            
+
saveIdStmts
            
+
declstmts
            
+
self
.
invokeRecvHandler
(
md
)
            
+
[
Whitespace
.
NL
]
            
+
self
.
makeReply
(
md
errfnRecv
routingId
=
idvar
)
            
+
self
.
genVerifyMessage
(
md
.
decl
.
type
.
verify
md
.
returns
errfnRecv
                                    
self
.
replyvar
)
            
+
[
StmtReturn
(
_Result
.
Processed
)
]
)
        
return
lbl
case
    
def
failIfNullActor
(
self
actorExpr
retOnNull
=
ExprLiteral
.
FALSE
msg
=
None
)
:
        
failif
=
StmtIf
(
ExprNot
(
actorExpr
)
)
        
if
msg
:
            
failif
.
addifstmt
(
_printWarningMessage
(
msg
)
)
        
failif
.
addifstmt
(
StmtReturn
(
retOnNull
)
)
        
return
failif
    
def
unregisterActor
(
self
)
:
        
return
[
StmtExpr
(
ExprCall
(
self
.
protocol
.
unregisterMethod
(
)
                                  
args
=
[
_actorId
(
)
]
)
)
]
    
def
makeMessage
(
self
md
errfn
fromActor
=
None
)
:
        
msgvar
=
self
.
msgvar
        
routingId
=
self
.
protocol
.
routingId
(
fromActor
)
        
this
=
ExprVar
.
THIS
        
if
md
.
decl
.
type
.
isDtor
(
)
:
            
this
=
md
.
actorDecl
(
)
.
var
(
)
        
stmts
=
(
[
StmtDecl
(
Decl
(
Type
(
'
IPC
:
:
Message
'
ptr
=
True
)
msgvar
.
name
)
                           
init
=
ExprCall
(
ExprVar
(
md
.
pqMsgCtorFunc
(
)
)
                                         
args
=
[
routingId
]
)
)
]
                 
+
[
Whitespace
.
NL
]
                 
+
[
_ParamTraits
.
checkedWrite
(
p
.
ipdltype
p
.
var
(
)
msgvar
                                              
sentinelKey
=
p
.
name
actor
=
this
)
                     
for
p
in
md
.
params
]
                 
+
[
Whitespace
.
NL
]
                 
+
self
.
setMessageFlags
(
md
msgvar
)
)
        
return
msgvar
stmts
    
def
makeResolver
(
self
md
errfn
routingId
)
:
        
if
routingId
is
None
:
            
routingId
=
self
.
protocol
.
routingId
(
)
        
if
not
md
.
decl
.
type
.
isAsync
(
)
or
not
md
.
hasReply
(
)
:
            
return
[
]
        
sendok
=
ExprVar
(
'
sendok__
'
)
        
seqno
=
ExprVar
(
'
seqno__
'
)
        
resolve
=
ExprVar
(
'
resolve__
'
)
        
resolvertype
=
Type
(
md
.
resolverName
(
)
)
        
failifsendok
=
StmtIf
(
ExprNot
(
sendok
)
)
        
failifsendok
.
addifstmt
(
_printWarningMessage
(
'
Error
sending
reply
'
)
)
        
sendmsg
=
(
self
.
setMessageFlags
(
md
self
.
replyvar
seqno
=
seqno
)
                   
+
[
self
.
logMessage
(
md
self
.
replyvar
'
Sending
reply
'
)
                       
StmtDecl
(
Decl
(
Type
.
BOOL
sendok
.
name
)
                                
init
=
ExprCall
(
                                    
ExprSelect
(
self
.
protocol
.
callGetChannel
(
)
                                               
'
-
>
'
'
Send
'
)
                                    
args
=
[
self
.
replyvar
]
)
)
                       
failifsendok
]
)
        
if
len
(
md
.
returns
)
>
1
:
            
resolvedecl
=
Decl
(
_tuple
(
[
p
.
moveType
(
self
.
side
)
for
p
in
md
.
returns
]
                                      
const
=
True
ref
=
True
)
                               
'
aParam
'
)
            
destructexpr
=
ExprCall
(
ExprVar
(
'
Tie
'
)
                                    
args
=
[
p
.
var
(
)
for
p
in
md
.
returns
]
)
        
else
:
            
resolvedecl
=
Decl
(
md
.
returns
[
0
]
.
moveType
(
self
.
side
)
'
aParam
'
)
            
destructexpr
=
md
.
returns
[
0
]
.
var
(
)
        
selfvar
=
ExprVar
(
'
self__
'
)
        
ifactorisdead
=
StmtIf
(
ExprNot
(
selfvar
)
)
        
ifactorisdead
.
addifstmts
(
[
            
_printWarningMessage
(
"
Not
resolving
response
because
actor
is
dead
.
"
)
            
StmtReturn
(
)
]
)
        
ifactorisdestroyed
=
StmtIf
(
ExprBinary
(
self
.
protocol
.
stateVar
(
)
'
=
=
'
                                               
self
.
protocol
.
deadState
(
)
)
)
        
ifactorisdestroyed
.
addifstmts
(
[
            
_printWarningMessage
(
"
Not
resolving
response
because
actor
is
destroyed
.
"
)
            
StmtReturn
(
)
]
)
        
returnifactorisdead
=
[
ifactorisdead
                               
ifactorisdestroyed
]
        
resolverfn
=
ExprLambda
(
[
ExprVar
.
THIS
selfvar
routingId
seqno
]
                                
[
resolvedecl
]
)
        
resolverfn
.
addstmts
(
returnifactorisdead
                            
+
[
StmtDecl
(
Decl
(
Type
.
BOOL
resolve
.
name
)
                                        
init
=
ExprLiteral
.
TRUE
)
]
                            
+
[
StmtDecl
(
Decl
(
p
.
bareType
(
self
.
side
)
p
.
var
(
)
.
name
)
)
                                
for
p
in
md
.
returns
]
                            
+
[
StmtExpr
(
ExprAssn
(
destructexpr
ExprMove
(
ExprVar
(
'
aParam
'
)
)
)
)
                                
StmtDecl
(
Decl
(
Type
(
'
IPC
:
:
Message
'
ptr
=
True
)
self
.
replyvar
.
name
)
                                         
init
=
ExprCall
(
ExprVar
(
md
.
pqReplyCtorFunc
(
)
)
                                                       
args
=
[
routingId
]
)
)
]
                            
+
[
_ParamTraits
.
checkedWrite
(
None
resolve
self
.
replyvar
                                                         
sentinelKey
=
resolve
.
name
actor
=
selfvar
)
]
                            
+
[
_ParamTraits
.
checkedWrite
(
r
.
ipdltype
r
.
var
(
)
self
.
replyvar
                                                         
sentinelKey
=
r
.
name
actor
=
selfvar
)
                                
for
r
in
md
.
returns
]
)
        
resolverfn
.
addstmts
(
sendmsg
)
        
makeresolver
=
[
Whitespace
.
NL
                        
StmtDecl
(
Decl
(
Type
.
INT32
seqno
.
name
)
                                 
init
=
ExprCall
(
ExprSelect
(
self
.
msgvar
'
.
'
'
seqno
'
)
)
)
                        
StmtDecl
(
Decl
(
Type
(
'
WeakPtr
'
T
=
ExprVar
(
self
.
clsname
)
)
                                      
selfvar
.
name
)
                                 
init
=
ExprVar
.
THIS
)
                        
StmtDecl
(
Decl
(
resolvertype
'
resolver
'
)
                                 
init
=
resolverfn
)
]
        
return
makeresolver
    
def
makeReply
(
self
md
errfn
routingId
)
:
        
if
routingId
is
None
:
            
routingId
=
self
.
protocol
.
routingId
(
)
        
if
not
md
.
decl
.
type
.
hasReply
(
)
:
            
return
[
]
        
if
md
.
decl
.
type
.
isAsync
(
)
and
md
.
decl
.
type
.
hasReply
(
)
:
            
return
[
]
        
replyvar
=
self
.
replyvar
        
return
(
            
[
StmtExpr
(
ExprAssn
(
                
replyvar
ExprCall
(
ExprVar
(
md
.
pqReplyCtorFunc
(
)
)
args
=
[
routingId
]
)
)
)
             
Whitespace
.
NL
]
            
+
[
_ParamTraits
.
checkedWrite
(
r
.
ipdltype
r
.
var
(
)
replyvar
                                         
sentinelKey
=
r
.
name
actor
=
ExprVar
.
THIS
)
                
for
r
in
md
.
returns
]
            
+
self
.
setMessageFlags
(
md
replyvar
)
            
+
[
self
.
logMessage
(
md
replyvar
'
Sending
reply
'
)
]
)
    
def
genVerifyMessage
(
self
verify
params
errfn
msgsrcVar
)
:
        
stmts
=
[
]
        
if
not
verify
:
            
return
stmts
        
if
len
(
params
)
=
=
0
:
            
return
stmts
        
msgvar
=
ExprVar
(
'
msgverify__
'
)
        
side
=
self
.
side
        
msgexpr
=
ExprAddrOf
(
msgvar
)
        
itervar
=
ExprVar
(
'
msgverifyIter__
'
)
        
stmts
.
append
(
StmtDecl
(
Decl
(
Type
(
'
IPC
:
:
Message
'
ptr
=
False
)
'
msgverify__
'
)
                              
init
=
ExprMove
(
ExprDeref
(
msgsrcVar
)
)
)
)
        
stmts
.
extend
(
(
            
[
StmtDecl
(
Decl
(
_iterType
(
ptr
=
False
)
itervar
.
name
)
                      
initargs
=
[
msgvar
]
)
]
            
+
[
StmtDecl
(
Decl
(
p
.
bareType
(
side
)
p
.
var
(
)
.
name
+
'
Copy
'
)
)
                
for
p
in
params
]
            
+
[
Whitespace
.
NL
]
            
+
[
_ParamTraits
.
checkedRead
(
p
.
ipdltype
                                        
ExprAddrOf
(
ExprVar
(
p
.
var
(
)
.
name
+
'
Copy
'
)
)
                                        
msgexpr
ExprAddrOf
(
itervar
)
                                        
errfn
p
.
bareType
(
side
)
.
name
                                        
sentinelKey
=
p
.
name
                                        
errfnSentinel
=
errfnSentinel
(
)
                                        
actor
=
ExprVar
.
THIS
)
                
for
p
in
params
]
            
+
[
self
.
endRead
(
msgvar
itervar
)
]
            
+
[
StmtExpr
(
ExprAssn
(
ExprDeref
(
msgsrcVar
)
ExprMove
(
msgvar
)
)
)
]
        
)
)
        
return
stmts
    
def
setMessageFlags
(
self
md
var
seqno
=
None
)
:
        
stmts
=
[
]
        
if
seqno
:
            
stmts
.
append
(
StmtExpr
(
ExprCall
(
                
ExprSelect
(
var
'
-
>
'
'
set_seqno
'
)
                
args
=
[
seqno
]
)
)
)
        
return
stmts
+
[
Whitespace
.
NL
]
    
def
deserializeMessage
(
self
md
side
errfn
errfnSent
)
:
        
msgvar
=
self
.
msgvar
        
itervar
=
self
.
itervar
        
msgexpr
=
ExprAddrOf
(
msgvar
)
        
isctor
=
md
.
decl
.
type
.
isCtor
(
)
        
stmts
=
(
[
            
self
.
logMessage
(
md
msgexpr
'
Received
'
                            
receiving
=
True
)
            
self
.
profilerLabel
(
md
)
            
Whitespace
.
NL
        
]
)
        
if
0
=
=
len
(
md
.
params
)
:
            
return
stmts
        
start
decls
reads
=
0
[
]
[
]
        
if
isctor
:
            
handlevar
=
self
.
handlevar
            
handletype
=
Type
(
'
ActorHandle
'
)
            
decls
=
[
StmtDecl
(
Decl
(
handletype
handlevar
.
name
)
)
]
            
reads
=
[
_ParamTraits
.
checkedRead
(
None
ExprAddrOf
(
handlevar
)
msgexpr
                                              
ExprAddrOf
(
self
.
itervar
)
                                              
errfn
"
'
%
s
'
"
%
handletype
.
name
                                              
sentinelKey
=
'
actor
'
errfnSentinel
=
errfnSent
                                              
actor
=
ExprVar
.
THIS
)
]
            
start
=
1
        
stmts
.
extend
(
(
            
[
StmtDecl
(
Decl
(
_iterType
(
ptr
=
False
)
self
.
itervar
.
name
)
                      
initargs
=
[
msgvar
]
)
]
            
+
decls
+
[
StmtDecl
(
Decl
(
p
.
bareType
(
side
)
p
.
var
(
)
.
name
)
)
                       
for
p
in
md
.
params
]
            
+
[
Whitespace
.
NL
]
            
+
reads
+
[
_ParamTraits
.
checkedRead
(
p
.
ipdltype
ExprAddrOf
(
p
.
var
(
)
)
                                                
msgexpr
ExprAddrOf
(
itervar
)
                                                
errfn
"
'
%
s
'
"
%
p
.
bareType
(
side
)
.
name
                                                
sentinelKey
=
p
.
name
errfnSentinel
=
errfnSent
                                                
actor
=
ExprVar
.
THIS
)
                       
for
p
in
md
.
params
[
start
:
]
]
            
+
[
self
.
endRead
(
msgvar
itervar
)
]
)
)
        
return
stmts
    
def
deserializeAsyncReply
(
self
md
side
errfn
errfnSent
)
:
        
msgvar
=
self
.
msgvar
        
itervar
=
self
.
itervar
        
msgexpr
=
ExprAddrOf
(
msgvar
)
        
isctor
=
md
.
decl
.
type
.
isCtor
(
)
        
resolve
=
ExprVar
(
'
resolve__
'
)
        
reason
=
ExprVar
(
'
reason__
'
)
        
desresolve
=
[
StmtDecl
(
Decl
(
Type
.
BOOL
resolve
.
name
)
)
                      
_ParamTraits
.
checkedRead
(
None
ExprAddrOf
(
resolve
)
msgexpr
                                               
ExprAddrOf
(
itervar
)
                                               
errfn
"
'
%
s
'
"
%
resolve
.
name
                                               
sentinelKey
=
resolve
.
name
errfnSentinel
=
errfnSent
                                               
actor
=
ExprVar
.
THIS
)
]
        
desrej
=
[
StmtDecl
(
Decl
(
_ResponseRejectReason
.
Type
(
)
reason
.
name
)
)
                  
_ParamTraits
.
checkedRead
(
None
ExprAddrOf
(
reason
)
msgexpr
                                           
ExprAddrOf
(
itervar
)
                                           
errfn
"
'
%
s
'
"
%
reason
.
name
                                           
sentinelKey
=
reason
.
name
errfnSentinel
=
errfnSent
                                           
actor
=
ExprVar
.
THIS
)
                  
self
.
endRead
(
msgvar
itervar
)
]
        
prologue
=
(
[
            
self
.
logMessage
(
md
msgexpr
'
Received
'
                            
receiving
=
True
)
            
self
.
profilerLabel
(
md
)
            
Whitespace
.
NL
        
]
)
        
if
not
md
.
returns
:
            
return
prologue
        
prologue
.
extend
(
[
StmtDecl
(
Decl
(
_iterType
(
ptr
=
False
)
itervar
.
name
)
                                  
initargs
=
[
msgvar
]
)
]
                        
+
desresolve
)
        
start
decls
reads
=
0
[
]
[
]
        
if
isctor
:
            
handlevar
=
self
.
handlevar
            
handletype
=
Type
(
'
ActorHandle
'
)
            
decls
=
[
StmtDecl
(
Decl
(
handletype
handlevar
.
name
)
)
]
            
reads
=
[
_ParamTraits
.
checkedRead
(
None
ExprAddrOf
(
handlevar
)
msgexpr
                                              
ExprAddrOf
(
itervar
)
                                              
errfn
"
'
%
s
'
"
%
handletype
.
name
                                              
sentinelKey
=
'
actor
'
errfnSentinel
=
errfnSent
                                              
actor
=
ExprVar
.
THIS
)
]
            
start
=
1
        
stmts
=
(
            
decls
+
[
StmtDecl
(
Decl
(
p
.
bareType
(
side
)
p
.
var
(
)
.
name
)
)
                     
for
p
in
md
.
returns
]
            
+
[
Whitespace
.
NL
]
            
+
reads
+
[
_ParamTraits
.
checkedRead
(
p
.
ipdltype
ExprAddrOf
(
p
.
var
(
)
)
                                                
msgexpr
ExprAddrOf
(
itervar
)
                                                
errfn
"
'
%
s
'
"
%
p
.
bareType
(
side
)
.
name
                                                
sentinelKey
=
p
.
name
errfnSentinel
=
errfnSent
                                                
actor
=
ExprVar
.
THIS
)
                       
for
p
in
md
.
returns
[
start
:
]
]
            
+
[
self
.
endRead
(
msgvar
itervar
)
]
)
        
return
resolve
reason
prologue
desrej
stmts
    
def
deserializeReply
(
self
md
replyexpr
side
errfn
errfnSentinel
actor
=
None
decls
=
False
)
:
        
stmts
=
[
Whitespace
.
NL
                 
self
.
logMessage
(
md
replyexpr
                                 
'
Received
reply
'
actor
receiving
=
True
)
]
        
if
0
=
=
len
(
md
.
returns
)
:
            
return
stmts
        
itervar
=
self
.
itervar
        
declstmts
=
[
]
        
if
decls
:
            
declstmts
=
[
StmtDecl
(
Decl
(
p
.
bareType
(
side
)
p
.
var
(
)
.
name
)
)
                         
for
p
in
md
.
returns
]
        
stmts
.
extend
(
            
[
Whitespace
.
NL
             
StmtDecl
(
Decl
(
_iterType
(
ptr
=
False
)
itervar
.
name
)
                      
initargs
=
[
self
.
replyvar
]
)
]
            
+
declstmts
            
+
[
Whitespace
.
NL
]
            
+
[
_ParamTraits
.
checkedRead
(
r
.
ipdltype
r
.
var
(
)
                                        
ExprAddrOf
(
self
.
replyvar
)
                                        
ExprAddrOf
(
self
.
itervar
)
                                        
errfn
"
'
%
s
'
"
%
r
.
bareType
(
side
)
.
name
                                        
sentinelKey
=
r
.
name
errfnSentinel
=
errfnSentinel
                                        
actor
=
ExprVar
.
THIS
)
                
for
r
in
md
.
returns
]
            
+
[
self
.
endRead
(
self
.
replyvar
itervar
)
]
)
        
return
stmts
    
def
sendAsync
(
self
md
msgexpr
actor
=
None
)
:
        
sendok
=
ExprVar
(
'
sendok__
'
)
        
resolvefn
=
ExprVar
(
'
aResolve
'
)
        
rejectfn
=
ExprVar
(
'
aReject
'
)
        
stmts
=
[
Whitespace
.
NL
                 
self
.
logMessage
(
md
msgexpr
'
Sending
'
actor
)
                 
self
.
profilerLabel
(
md
)
]
+
self
.
transition
(
md
actor
errorfn
=
errfnUnreachable
)
        
stmts
.
append
(
Whitespace
.
NL
)
        
send
=
ExprSelect
(
self
.
protocol
.
callGetChannel
(
actor
)
'
-
>
'
'
Send
'
)
        
if
md
.
returns
:
            
stmts
.
append
(
StmtExpr
(
ExprCall
(
send
args
=
[
msgexpr
                                                       
ExprVar
(
'
this
'
)
                                                       
ExprMove
(
resolvefn
)
                                                       
ExprMove
(
rejectfn
)
]
)
)
)
            
retvar
=
None
        
else
:
            
stmts
.
append
(
StmtDecl
(
Decl
(
Type
.
BOOL
sendok
.
name
)
                                  
init
=
ExprCall
(
send
args
=
[
msgexpr
]
)
)
)
            
retvar
=
sendok
        
return
(
retvar
stmts
)
    
def
sendBlocking
(
self
md
msgexpr
replyexpr
actor
=
None
)
:
        
sendok
=
ExprVar
(
'
sendok__
'
)
        
return
(
            
sendok
            
(
[
Whitespace
.
NL
              
self
.
logMessage
(
md
msgexpr
'
Sending
'
actor
)
              
self
.
profilerLabel
(
md
)
]
             
+
self
.
transition
(
md
actor
errorfn
=
errfnUnreachable
)
             
+
[
Whitespace
.
NL
                
StmtDecl
(
Decl
(
Type
.
BOOL
sendok
.
name
)
)
                
StmtBlock
(
[
                    
StmtExpr
(
ExprCall
(
ExprVar
(
'
AUTO_PROFILER_TRACING
'
)
                                      
[
ExprLiteral
.
String
(
"
IPC
"
)
                                       
ExprLiteral
.
String
(
self
.
protocol
.
name
+
"
:
:
"
+
                                                          
md
.
prettyMsgName
(
)
)
                                       
ExprVar
(
'
OTHER
'
)
]
)
)
                    
StmtExpr
(
ExprAssn
(
sendok
                                      
ExprCall
(
                                          
ExprSelect
(
self
.
protocol
.
callGetChannel
(
actor
)
                                                     
'
-
>
'
                                                     
_sendPrefix
(
md
.
decl
.
type
)
)
                                          
args
=
[
msgexpr
ExprAddrOf
(
replyexpr
)
]
)
)
)
                
]
)
                
]
)
        
)
    
def
sendAsyncWithPromise
(
self
md
)
:
        
retpromise
=
ExprVar
(
'
promise__
'
)
        
promise
=
_makePromise
(
md
.
returns
self
.
side
resolver
=
True
)
        
stmts
=
[
Whitespace
.
NL
                 
StmtDecl
(
Decl
(
_refptr
(
promise
)
retpromise
.
name
)
                          
init
=
ExprNew
(
promise
args
=
[
ExprVar
(
'
__func__
'
)
]
)
)
]
        
if
len
(
md
.
returns
)
>
1
:
            
resolvetype
=
_tuple
(
[
d
.
bareType
(
self
.
side
)
for
d
in
md
.
returns
]
)
        
else
:
            
resolvetype
=
md
.
returns
[
0
]
.
bareType
(
self
.
side
)
        
resolvetype
.
rvalref
=
True
        
resolvefn
=
ExprLambda
(
[
retpromise
]
                               
[
Decl
(
resolvetype
"
aValue
"
)
]
)
        
resolvefn
.
addstmts
(
[
            
StmtExpr
(
ExprCall
(
ExprSelect
(
retpromise
'
-
>
'
'
Resolve
'
)
                              
args
=
[
ExprMove
(
ExprVar
(
'
aValue
'
)
)
                                    
ExprVar
(
'
__func__
'
)
]
)
)
        
]
)
        
rejecttype
=
_ResponseRejectReason
.
Type
(
)
        
rejecttype
.
rvalref
=
True
        
rejectfn
=
ExprLambda
(
[
retpromise
]
                              
[
Decl
(
rejecttype
"
aReason
"
)
]
)
        
rejectfn
.
addstmts
(
[
            
StmtExpr
(
ExprCall
(
ExprSelect
(
retpromise
'
-
>
'
'
Reject
'
)
                              
args
=
[
ExprMove
(
ExprVar
(
'
aReason
'
)
)
                                    
ExprVar
(
'
__func__
'
)
]
)
)
        
]
)
        
args
=
[
p
.
var
(
)
for
p
in
md
.
params
]
+
[
resolvefn
rejectfn
]
        
stmts
+
=
[
Whitespace
.
NL
                  
StmtExpr
(
ExprCall
(
ExprVar
(
md
.
sendMethod
(
)
.
name
)
args
=
args
)
)
                  
StmtReturn
(
retpromise
)
]
        
return
stmts
    
def
callAllocActor
(
self
md
retsems
side
)
:
        
return
self
.
thisCall
(
            
_allocMethod
(
md
.
decl
.
type
.
constructedType
(
)
side
)
            
args
=
md
.
makeCxxArgs
(
retsems
=
retsems
retcallsems
=
'
out
'
                                
implicit
=
False
)
)
    
def
callActorDestroy
(
self
actorexpr
why
=
_DestroyReason
.
Deletion
)
:
        
return
ExprCall
(
ExprSelect
(
actorexpr
'
-
>
'
'
DestroySubtree
'
)
                        
args
=
[
why
]
)
    
def
callRemoveActor
(
self
actorexpr
manager
=
None
ipdltype
=
None
)
:
        
if
ipdltype
is
None
:
            
ipdltype
=
self
.
protocol
.
decl
.
type
        
if
not
ipdltype
.
isManaged
(
)
:
            
return
Whitespace
(
'
/
/
unmanaged
protocol
'
)
        
removefunc
=
self
.
protocol
.
removeManageeMethod
(
)
        
if
manager
is
not
None
:
            
removefunc
=
ExprSelect
(
manager
'
-
>
'
removefunc
.
name
)
        
return
ExprCall
(
removefunc
                        
args
=
[
_protocolId
(
ipdltype
)
                              
actorexpr
]
)
    
def
callDeallocSubtree
(
self
md
actorexpr
)
:
        
return
ExprCall
(
ExprSelect
(
actorexpr
'
-
>
'
'
DeallocSubtree
'
)
)
    
def
invokeRecvHandler
(
self
md
implicit
=
True
)
:
        
retsems
=
'
in
'
        
if
md
.
decl
.
type
.
isAsync
(
)
and
md
.
returns
:
            
retsems
=
'
resolver
'
        
failif
=
StmtIf
(
ExprNot
(
self
.
thisCall
(
            
md
.
recvMethod
(
)
            
md
.
makeCxxArgs
(
                
paramsems
=
'
move
'
                
retsems
=
retsems
                
retcallsems
=
'
out
'
                
implicit
=
implicit
            
)
        
)
)
)
        
failif
.
addifstmts
(
[
            
_protocolErrorBreakpoint
(
'
Handler
returned
error
code
!
'
)
            
Whitespace
(
'
/
/
Error
handled
in
mozilla
:
:
ipc
:
:
IPCResult
\
n
'
indent
=
True
)
            
StmtReturn
(
_Result
.
ProcessingError
)
        
]
)
        
return
[
failif
]
    
def
makeDtorMethodDecl
(
self
md
)
:
        
decl
=
self
.
makeSendMethodDecl
(
md
)
        
decl
.
methodspec
=
MethodSpec
.
STATIC
        
return
decl
    
def
makeSendMethodDecl
(
self
md
promise
=
False
paramsems
=
'
in
'
)
:
        
implicit
=
md
.
decl
.
type
.
hasImplicitActorParam
(
)
        
if
md
.
decl
.
type
.
isAsync
(
)
and
md
.
returns
:
            
if
promise
:
                
returnsems
=
'
promise
'
                
rettype
=
_refptr
(
Type
(
md
.
promiseName
(
)
)
)
            
else
:
                
returnsems
=
'
callback
'
                
rettype
=
Type
.
VOID
        
else
:
            
assert
not
promise
            
returnsems
=
'
out
'
            
rettype
=
Type
.
BOOL
        
decl
=
MethodDecl
(
            
md
.
sendMethod
(
)
.
name
            
params
=
md
.
makeCxxParams
(
paramsems
returnsems
=
returnsems
                                    
side
=
self
.
side
implicit
=
implicit
)
            
warn_unused
=
(
self
.
side
=
=
'
parent
'
and
returnsems
!
=
'
callback
'
)
            
ret
=
rettype
)
        
if
md
.
decl
.
type
.
isCtor
(
)
:
            
decl
.
ret
=
md
.
actorDecl
(
)
.
bareType
(
self
.
side
)
        
return
decl
    
def
logMessage
(
self
md
msgptr
pfx
actor
=
None
receiving
=
False
)
:
        
actorname
=
_actorName
(
self
.
protocol
.
name
self
.
side
)
        
return
_ifLogging
(
ExprLiteral
.
String
(
actorname
)
                          
[
StmtExpr
(
ExprCall
(
                              
ExprVar
(
'
mozilla
:
:
ipc
:
:
LogMessageForProtocol
'
)
                              
args
=
[
ExprLiteral
.
String
(
actorname
)
                                    
self
.
protocol
.
callOtherPid
(
actor
)
                                    
ExprLiteral
.
String
(
pfx
)
                                    
ExprCall
(
ExprSelect
(
msgptr
'
-
>
'
'
type
'
)
)
                                    
ExprVar
(
'
mozilla
:
:
ipc
:
:
MessageDirection
:
:
eReceiving
'
                                            
if
receiving
                                            
else
'
mozilla
:
:
ipc
:
:
MessageDirection
:
:
eSending
'
)
]
)
)
]
)
    
def
profilerLabel
(
self
md
)
:
        
labelStr
=
self
.
protocol
.
name
+
'
:
:
'
+
md
.
prettyMsgName
(
)
        
return
StmtExpr
(
ExprCall
(
ExprVar
(
'
AUTO_PROFILER_LABEL
'
)
                                 
[
ExprLiteral
.
String
(
labelStr
)
                                  
ExprVar
(
'
OTHER
'
)
]
)
)
    
def
saveActorId
(
self
md
)
:
        
idvar
=
ExprVar
(
'
id__
'
)
        
if
md
.
decl
.
type
.
hasReply
(
)
:
            
saveIdStmts
=
[
StmtDecl
(
Decl
(
_actorIdType
(
)
idvar
.
name
)
                                    
self
.
protocol
.
routingId
(
)
)
]
        
else
:
            
saveIdStmts
=
[
]
        
return
idvar
saveIdStmts
    
def
transition
(
self
md
actor
=
None
reply
=
False
errorfn
=
None
)
:
        
msgid
=
md
.
msgId
(
)
if
not
reply
else
md
.
replyId
(
)
        
args
=
[
            
ExprVar
(
'
true
'
if
_deleteId
(
)
.
name
=
=
msgid
else
'
false
'
)
        
]
        
if
self
.
protocol
.
decl
.
type
.
hasReentrantDelete
:
            
function
=
'
ReEntrantDeleteStateTransition
'
            
args
.
append
(
                
ExprVar
(
'
true
'
if
_deleteReplyId
(
)
.
name
=
=
msgid
else
'
false
'
)
            
)
        
else
:
            
function
=
'
StateTransition
'
        
if
actor
is
not
None
:
            
stateexpr
=
_actorState
(
actor
)
        
else
:
            
stateexpr
=
self
.
protocol
.
stateVar
(
)
        
args
.
append
(
ExprAddrOf
(
stateexpr
)
)
        
ifstmt
=
StmtIf
(
ExprNot
(
ExprCall
(
ExprVar
(
function
)
args
=
args
)
)
)
        
ifstmt
.
addifstmts
(
errorfn
(
'
Transition
error
'
)
)
        
return
[
ifstmt
]
    
def
endRead
(
self
msgexpr
iterexpr
)
:
        
msgtype
=
ExprCall
(
ExprSelect
(
msgexpr
'
.
'
'
type
'
)
[
]
)
        
return
StmtExpr
(
ExprCall
(
ExprSelect
(
msgexpr
'
.
'
'
EndRead
'
)
                                 
args
=
[
iterexpr
msgtype
]
)
)
class
_GenerateProtocolParentCode
(
_GenerateProtocolActorCode
)
:
    
def
__init__
(
self
)
:
        
_GenerateProtocolActorCode
.
__init__
(
self
'
parent
'
)
    
def
sendsMessage
(
self
md
)
:
        
return
not
md
.
decl
.
type
.
isIn
(
)
    
def
receivesMessage
(
self
md
)
:
        
return
md
.
decl
.
type
.
isInout
(
)
or
md
.
decl
.
type
.
isIn
(
)
class
_GenerateProtocolChildCode
(
_GenerateProtocolActorCode
)
:
    
def
__init__
(
self
)
:
        
_GenerateProtocolActorCode
.
__init__
(
self
'
child
'
)
    
def
sendsMessage
(
self
md
)
:
        
return
not
md
.
decl
.
type
.
isOut
(
)
    
def
receivesMessage
(
self
md
)
:
        
return
md
.
decl
.
type
.
isInout
(
)
or
md
.
decl
.
type
.
isOut
(
)
def
_splitClassDeclDefn
(
cls
)
:
    
"
"
"
Destructively
split
|
cls
|
methods
into
declarations
and
definitions
(
if
|
not
methodDecl
.
force_inline
|
)
.
Return
classDecl
methodDefns
.
"
"
"
    
defns
=
Block
(
)
    
for
i
stmt
in
enumerate
(
cls
.
stmts
)
:
        
if
isinstance
(
stmt
MethodDefn
)
and
not
stmt
.
decl
.
force_inline
:
            
decl
defn
=
_splitMethodDefn
(
stmt
cls
)
            
cls
.
stmts
[
i
]
=
StmtDecl
(
decl
)
            
defns
.
addstmts
(
[
defn
Whitespace
.
NL
]
)
    
return
cls
defns
def
_splitMethodDefn
(
md
cls
)
:
    
saveddecl
=
deepcopy
(
md
.
decl
)
    
md
.
decl
.
cls
=
cls
    
md
.
decl
.
methodspec
=
MethodSpec
.
NONE
    
md
.
decl
.
warn_unused
=
False
    
md
.
decl
.
only_for_definition
=
True
    
for
param
in
md
.
decl
.
params
:
        
if
isinstance
(
param
Param
)
:
            
param
.
default
=
None
    
return
saveddecl
md
def
_splitFuncDeclDefn
(
fun
)
:
    
assert
not
fun
.
decl
.
force_inline
    
return
StmtDecl
(
fun
.
decl
)
fun
