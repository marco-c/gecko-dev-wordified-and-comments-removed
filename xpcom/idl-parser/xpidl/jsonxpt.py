"
"
"
Generate
a
json
XPT
typelib
for
an
IDL
file
"
"
"
import
xpidl
import
json
import
itertools
TypeMap
=
{
    
'
boolean
'
:
'
TD_BOOL
'
    
'
void
'
:
'
TD_VOID
'
    
'
int16_t
'
:
'
TD_INT16
'
    
'
int32_t
'
:
'
TD_INT32
'
    
'
int64_t
'
:
'
TD_INT64
'
    
'
uint8_t
'
:
'
TD_UINT8
'
    
'
uint16_t
'
:
'
TD_UINT16
'
    
'
uint32_t
'
:
'
TD_UINT32
'
    
'
uint64_t
'
:
'
TD_UINT64
'
    
'
octet
'
:
'
TD_UINT8
'
    
'
short
'
:
'
TD_INT16
'
    
'
long
'
:
'
TD_INT32
'
    
'
long
long
'
:
'
TD_INT64
'
    
'
unsigned
short
'
:
'
TD_UINT16
'
    
'
unsigned
long
'
:
'
TD_UINT32
'
    
'
unsigned
long
long
'
:
'
TD_UINT64
'
    
'
float
'
:
'
TD_FLOAT
'
    
'
double
'
:
'
TD_DOUBLE
'
    
'
char
'
:
'
TD_CHAR
'
    
'
string
'
:
'
TD_PSTRING
'
    
'
wchar
'
:
'
TD_WCHAR
'
    
'
wstring
'
:
'
TD_PWSTRING
'
    
'
nsid
'
:
'
TD_PNSIID
'
    
'
domstring
'
:
'
TD_DOMSTRING
'
    
'
astring
'
:
'
TD_ASTRING
'
    
'
utf8string
'
:
'
TD_UTF8STRING
'
    
'
cstring
'
:
'
TD_CSTRING
'
    
'
jsval
'
:
'
TD_JSVAL
'
    
'
promise
'
:
'
TD_PROMISE
'
}
def
flags
(
*
flags
)
:
    
return
[
flag
for
flag
cond
in
flags
if
cond
]
def
get_type
(
type
calltype
iid_is
=
None
size_is
=
None
)
:
    
while
isinstance
(
type
xpidl
.
Typedef
)
:
        
type
=
type
.
realtype
    
if
isinstance
(
type
xpidl
.
Builtin
)
:
        
ret
=
{
'
tag
'
:
TypeMap
[
type
.
name
]
}
        
if
type
.
name
in
[
'
string
'
'
wstring
'
]
and
size_is
is
not
None
:
            
ret
[
'
tag
'
]
+
=
'
_SIZE_IS
'
            
ret
[
'
size_is
'
]
=
size_is
        
return
ret
    
if
isinstance
(
type
xpidl
.
Array
)
:
        
return
{
            
'
tag
'
:
'
TD_ARRAY
'
            
'
size_is
'
:
size_is
            
'
element
'
:
get_type
(
type
.
type
calltype
iid_is
)
        
}
    
if
isinstance
(
type
xpidl
.
Interface
)
or
isinstance
(
type
xpidl
.
Forward
)
:
        
return
{
            
'
tag
'
:
'
TD_INTERFACE_TYPE
'
            
'
name
'
:
type
.
name
        
}
    
if
isinstance
(
type
xpidl
.
WebIDL
)
:
        
return
{
            
'
tag
'
:
'
TD_DOMOBJECT
'
            
'
name
'
:
type
.
name
            
'
native
'
:
type
.
native
            
'
headerFile
'
:
type
.
headerFile
        
}
    
if
isinstance
(
type
xpidl
.
Native
)
:
        
if
type
.
specialtype
:
            
return
{
                
'
tag
'
:
TypeMap
[
type
.
specialtype
]
            
}
        
elif
iid_is
is
not
None
:
            
return
{
                
'
tag
'
:
'
TD_INTERFACE_IS_TYPE
'
                
'
iid_is
'
:
iid_is
            
}
        
else
:
            
return
{
'
tag
'
:
'
TD_VOID
'
}
    
raise
Exception
(
"
Unknown
type
!
"
)
def
mk_param
(
type
in_
=
0
out
=
0
optional
=
0
)
:
    
return
{
        
'
type
'
:
type
        
'
flags
'
:
flags
(
            
(
'
in
'
in_
)
            
(
'
out
'
out
)
            
(
'
optional
'
optional
)
        
)
    
}
def
mk_method
(
name
params
getter
=
0
setter
=
0
notxpcom
=
0
              
hidden
=
0
optargc
=
0
context
=
0
hasretval
=
0
)
:
    
return
{
        
'
name
'
:
name
        
'
params
'
:
params
        
'
flags
'
:
flags
(
            
(
'
getter
'
getter
)
            
(
'
setter
'
setter
)
            
(
'
notxpcom
'
notxpcom
)
            
(
'
hidden
'
hidden
)
            
(
'
optargc
'
optargc
)
            
(
'
jscontext
'
context
)
            
(
'
hasretval
'
hasretval
)
        
)
    
}
def
attr_param_idx
(
p
m
attr
)
:
    
if
hasattr
(
p
attr
)
and
getattr
(
p
attr
)
:
        
for
i
param
in
enumerate
(
m
.
params
)
:
            
if
param
.
name
=
=
getattr
(
p
attr
)
:
                
return
i
        
return
None
def
build_interface
(
iface
)
:
    
if
iface
.
namemap
is
None
:
        
raise
Exception
(
"
Interface
was
not
resolved
.
"
)
    
consts
=
[
]
    
methods
=
[
]
    
def
build_const
(
c
)
:
        
consts
.
append
(
{
            
'
name
'
:
c
.
name
            
'
type
'
:
get_type
(
c
.
basetype
'
'
)
            
'
value
'
:
c
.
getValue
(
)
        
}
)
    
def
build_method
(
m
)
:
        
params
=
[
]
        
for
p
in
m
.
params
:
            
params
.
append
(
mk_param
(
                
get_type
(
                    
p
.
realtype
p
.
paramtype
                    
iid_is
=
attr_param_idx
(
p
m
'
iid_is
'
)
                    
size_is
=
attr_param_idx
(
p
m
'
size_is
'
)
)
                
in_
=
p
.
paramtype
.
count
(
"
in
"
)
                
out
=
p
.
paramtype
.
count
(
"
out
"
)
                
optional
=
p
.
optional
            
)
)
        
hasretval
=
len
(
m
.
params
)
>
0
and
m
.
params
[
-
1
]
.
retval
        
if
not
m
.
notxpcom
and
m
.
realtype
.
name
!
=
'
void
'
:
            
hasretval
=
True
            
params
.
append
(
mk_param
(
get_type
(
m
.
realtype
'
out
'
)
out
=
1
)
)
        
methods
.
append
(
mk_method
(
            
m
.
name
params
notxpcom
=
m
.
notxpcom
hidden
=
m
.
noscript
            
optargc
=
m
.
optional_argc
context
=
m
.
implicit_jscontext
            
hasretval
=
hasretval
)
)
    
def
build_attr
(
a
)
:
        
param
=
mk_param
(
get_type
(
a
.
realtype
'
out
'
)
out
=
1
)
        
methods
.
append
(
mk_method
(
a
.
name
[
param
]
getter
=
1
hidden
=
a
.
noscript
                                 
context
=
a
.
implicit_jscontext
hasretval
=
1
)
)
        
if
not
a
.
readonly
:
            
param
=
mk_param
(
get_type
(
a
.
realtype
'
in
'
)
in_
=
1
)
            
methods
.
append
(
mk_method
(
a
.
name
[
param
]
setter
=
1
hidden
=
a
.
noscript
                                     
context
=
a
.
implicit_jscontext
)
)
    
for
member
in
iface
.
members
:
        
if
isinstance
(
member
xpidl
.
ConstMember
)
:
            
build_const
(
member
)
        
elif
isinstance
(
member
xpidl
.
Attribute
)
:
            
build_attr
(
member
)
        
elif
isinstance
(
member
xpidl
.
Method
)
:
            
build_method
(
member
)
        
elif
isinstance
(
member
xpidl
.
CDATA
)
:
            
pass
        
else
:
            
raise
Exception
(
"
Unexpected
interface
member
:
%
s
"
%
member
)
    
assert
iface
.
attributes
.
shim
is
not
None
or
iface
.
attributes
.
shimfile
is
None
    
return
{
        
'
name
'
:
iface
.
name
        
'
uuid
'
:
iface
.
attributes
.
uuid
        
'
methods
'
:
methods
        
'
consts
'
:
consts
        
'
parent
'
:
iface
.
base
        
'
shim
'
:
iface
.
attributes
.
shim
        
'
shimfile
'
:
iface
.
attributes
.
shimfile
        
'
flags
'
:
flags
(
            
(
'
scriptable
'
iface
.
attributes
.
scriptable
)
            
(
'
function
'
iface
.
attributes
.
function
)
            
(
'
builtinclass
'
iface
.
attributes
.
builtinclass
or
iface
.
implicit_builtinclass
)
            
(
'
main_process_only
'
iface
.
attributes
.
main_process_scriptable_only
)
        
)
    
}
def
build_typelib
(
idl
)
:
    
def
exported
(
p
)
:
        
if
p
.
kind
!
=
'
interface
'
:
            
return
False
        
return
p
.
attributes
.
scriptable
or
p
.
attributes
.
shim
    
return
[
build_interface
(
p
)
for
p
in
idl
.
productions
if
exported
(
p
)
]
def
link
(
typelibs
)
:
    
linked
=
list
(
itertools
.
chain
.
from_iterable
(
typelibs
)
)
    
assert
len
(
set
(
iface
[
'
name
'
]
for
iface
in
linked
)
)
=
=
len
(
linked
)
\
        
"
Multiple
typelibs
containing
the
same
interface
were
linked
together
"
    
return
linked
def
write
(
typelib
fd
)
:
    
json
.
dump
(
typelib
fd
indent
=
2
)
