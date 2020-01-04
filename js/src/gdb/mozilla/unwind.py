import
gdb
from
gdb
.
FrameDecorator
import
FrameDecorator
import
re
import
platform
from
mozilla
.
ExecutableAllocator
import
jsjitExecutableAllocatorCache
jsjitExecutableAllocator
try
:
    
long
except
NameError
:
    
long
=
int
try
:
    
from
itertools
import
imap
except
ImportError
:
    
imap
=
map
_have_unwinder
=
True
try
:
    
from
gdb
.
unwinder
import
Unwinder
except
ImportError
:
    
_have_unwinder
=
False
    
Unwinder
=
object
def
debug
(
something
)
:
    
pass
SizeOfFramePrefix
=
{
    
'
JitFrame_IonJS
'
:
'
ExitFrameLayout
'
    
'
JitFrame_BaselineJS
'
:
'
JitFrameLayout
'
    
'
JitFrame_BaselineStub
'
:
'
BaselineStubFrameLayout
'
    
'
JitFrame_IonStub
'
:
'
JitStubFrameLayout
'
    
'
JitFrame_Entry
'
:
'
JitFrameLayout
'
    
'
JitFrame_Rectifier
'
:
'
RectifierFrameLayout
'
    
'
JitFrame_IonAccessorIC
'
:
'
IonAccessorICFrameLayout
'
    
'
JitFrame_Exit
'
:
'
ExitFrameLayout
'
    
'
JitFrame_Bailout
'
:
'
JitFrameLayout
'
}
class
UnwinderTypeCache
(
object
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
d
=
None
        
self
.
frame_enum_names
=
{
}
        
self
.
frame_class_types
=
{
}
    
def
__getattr__
(
self
name
)
:
        
if
self
.
d
is
None
:
            
self
.
initialize
(
)
        
return
self
.
d
[
name
]
    
def
value
(
self
name
)
:
        
return
long
(
gdb
.
parse_and_eval
(
'
js
:
:
jit
:
:
'
+
name
)
)
    
def
initialize
(
self
)
:
        
self
.
d
=
{
}
        
self
.
d
[
'
FRAMETYPE_MASK
'
]
=
(
1
<
<
self
.
value
(
'
FRAMETYPE_BITS
'
)
)
-
1
        
self
.
d
[
'
FRAMESIZE_SHIFT
'
]
=
self
.
value
(
'
FRAMESIZE_SHIFT
'
)
        
self
.
d
[
'
FRAME_HEADER_SIZE_SHIFT
'
]
=
self
.
value
(
'
FRAME_HEADER_SIZE_SHIFT
'
)
        
self
.
d
[
'
FRAME_HEADER_SIZE_MASK
'
]
=
self
.
value
(
'
FRAME_HEADER_SIZE_MASK
'
)
        
self
.
compute_frame_info
(
)
        
commonFrameLayout
=
gdb
.
lookup_type
(
'
js
:
:
jit
:
:
CommonFrameLayout
'
)
        
self
.
d
[
'
typeCommonFrameLayout
'
]
=
commonFrameLayout
        
self
.
d
[
'
typeCommonFrameLayoutPointer
'
]
=
commonFrameLayout
.
pointer
(
)
        
self
.
d
[
'
per_tls_data
'
]
=
gdb
.
lookup_global_symbol
(
'
js
:
:
TlsPerThreadData
'
)
        
self
.
d
[
'
void_starstar
'
]
=
gdb
.
lookup_type
(
'
void
'
)
.
pointer
(
)
.
pointer
(
)
        
self
.
d
[
'
mod_ExecutableAllocator
'
]
=
jsjitExecutableAllocatorCache
(
)
    
def
compute_frame_info
(
self
)
:
        
t
=
gdb
.
lookup_type
(
'
enum
js
:
:
jit
:
:
FrameType
'
)
        
for
field
in
t
.
fields
(
)
:
            
name
=
field
.
name
[
9
:
]
            
self
.
d
[
name
]
=
long
(
field
.
enumval
)
            
self
.
frame_enum_names
[
long
(
field
.
enumval
)
]
=
name
def
parse_proc_maps
(
)
:
    
mapfile
=
'
/
proc
/
'
+
str
(
gdb
.
selected_inferior
(
)
.
pid
)
+
'
/
maps
'
    
matcher
=
re
.
compile
(
"
^
(
[
a
-
fA
-
F0
-
9
]
+
)
-
(
[
a
-
fA
-
F0
-
9
]
+
)
\
s
+
.
.
x
.
\
s
+
\
S
+
\
s
+
\
S
+
\
s
+
\
S
*
(
.
*
)
"
)
    
mappings
=
[
]
    
with
open
(
mapfile
"
r
"
)
as
inp
:
        
for
line
in
inp
:
            
match
=
matcher
.
match
(
line
)
            
if
not
match
:
                
continue
            
start
=
match
.
group
(
1
)
            
end
=
match
.
group
(
2
)
            
name
=
match
.
group
(
3
)
.
strip
(
)
            
if
name
is
'
'
or
(
name
.
startswith
(
'
[
'
)
and
name
is
not
'
[
vdso
]
'
)
:
                
continue
            
mappings
.
append
(
(
long
(
start
16
)
long
(
end
16
)
)
)
    
return
mappings
class
JitFrameDecorator
(
FrameDecorator
)
:
    
def
__init__
(
self
base
info
)
:
        
super
(
JitFrameDecorator
self
)
.
__init__
(
base
)
        
self
.
info
=
info
    
def
function
(
self
)
:
        
if
"
name
"
in
self
.
info
:
            
return
"
<
<
"
+
self
.
info
[
"
name
"
]
+
"
>
>
"
        
return
FrameDecorator
.
function
(
self
)
class
SpiderMonkeyFrameFilter
(
object
)
:
    
def
__init__
(
self
state_holder
)
:
        
self
.
name
=
"
SpiderMonkey
"
        
self
.
enabled
=
True
        
self
.
priority
=
100
        
self
.
state_holder
=
state_holder
    
def
maybe_wrap_frame
(
self
frame
)
:
        
if
self
.
state_holder
is
None
or
self
.
state_holder
.
unwinder_state
is
None
:
            
return
frame
        
base
=
frame
.
inferior_frame
(
)
        
info
=
self
.
state_holder
.
unwinder_state
.
get_frame
(
base
)
        
if
info
is
None
:
            
return
frame
        
return
JitFrameDecorator
(
frame
info
)
    
def
filter
(
self
frame_iter
)
:
        
return
imap
(
self
.
maybe_wrap_frame
frame_iter
)
class
SpiderMonkeyFrameId
(
object
)
:
    
def
__init__
(
self
sp
pc
)
:
        
self
.
sp
=
sp
        
self
.
pc
=
pc
class
UnwinderState
(
object
)
:
    
def
__init__
(
self
typecache
)
:
        
self
.
next_sp
=
None
        
self
.
next_type
=
None
        
self
.
activation
=
None
        
self
.
thread
=
gdb
.
selected_thread
(
)
        
self
.
frame_map
=
{
}
        
self
.
proc_mappings
=
None
        
try
:
            
self
.
proc_mappings
=
parse_proc_maps
(
)
        
except
IOError
:
            
pass
        
self
.
typecache
=
typecache
    
def
get_frame
(
self
frame
)
:
        
sp
=
long
(
frame
.
read_register
(
self
.
SP_REGISTER
)
)
        
if
sp
in
self
.
frame_map
:
            
return
self
.
frame_map
[
sp
]
        
return
None
    
def
add_frame
(
self
sp
name
)
:
        
self
.
frame_map
[
long
(
sp
)
]
=
{
"
name
"
:
name
}
    
def
text_address_claimed
(
self
pc
)
:
        
for
(
start
end
)
in
self
.
proc_mappings
:
            
if
(
pc
>
=
start
and
pc
<
=
end
)
:
                
return
True
        
return
False
    
def
is_jit_address
(
self
pc
)
:
        
if
self
.
proc_mappings
!
=
None
:
            
return
not
self
.
text_address_claimed
(
pc
)
        
ptd
=
self
.
get_tls_per_thread_data
(
)
        
jitRuntime
=
ptd
[
'
runtime_
'
]
[
'
jitRuntime_
'
]
        
execAllocators
=
[
jitRuntime
[
'
execAlloc_
'
]
jitRuntime
[
'
backedgeExecAlloc_
'
]
]
        
for
execAlloc
in
execAllocators
:
            
for
pool
in
jsjitExecutableAllocator
(
execAlloc
self
.
typecache
)
:
                
pages
=
pool
[
'
m_allocation
'
]
[
'
pages
'
]
                
size
=
pool
[
'
m_allocation
'
]
[
'
size
'
]
                
if
pages
<
=
pc
and
pc
<
pages
+
size
:
                    
return
True
        
return
False
    
def
check
(
self
)
:
        
return
gdb
.
selected_thread
(
)
is
self
.
thread
    
def
get_tls_per_thread_data
(
self
)
:
        
return
self
.
typecache
.
per_tls_data
.
value
(
)
[
'
mValue
'
]
    
def
unpack_descriptor
(
self
common
)
:
        
value
=
long
(
common
[
'
descriptor_
'
]
)
        
local_size
=
value
>
>
self
.
typecache
.
FRAMESIZE_SHIFT
        
header_size
=
(
(
value
>
>
self
.
typecache
.
FRAME_HEADER_SIZE_SHIFT
)
&
                       
self
.
typecache
.
FRAME_HEADER_SIZE_MASK
)
        
header_size
=
header_size
*
self
.
typecache
.
void_starstar
.
sizeof
        
frame_type
=
long
(
value
&
self
.
typecache
.
FRAMETYPE_MASK
)
        
if
frame_type
=
=
self
.
typecache
.
JitFrame_Entry
:
            
header_size
=
self
.
typecache
.
typeCommonFrameLayout
.
sizeof
        
return
(
local_size
header_size
frame_type
)
    
def
create_frame
(
self
pc
sp
frame
frame_type
pending_frame
)
:
        
frame_id
=
SpiderMonkeyFrameId
(
frame
pc
)
        
frame_name
=
self
.
typecache
.
frame_enum_names
[
frame_type
]
        
self
.
add_frame
(
sp
name
=
frame_name
)
        
common
=
frame
.
cast
(
self
.
typecache
.
typeCommonFrameLayoutPointer
)
        
next_pc
=
common
[
'
returnAddress_
'
]
        
(
local_size
header_size
next_type
)
=
self
.
unpack_descriptor
(
common
)
        
next_sp
=
frame
+
header_size
+
local_size
        
self
.
next_sp
=
next_sp
        
self
.
next_type
=
next_type
        
unwind_info
=
pending_frame
.
create_unwind_info
(
frame_id
)
        
unwind_info
.
add_saved_register
(
self
.
PC_REGISTER
next_pc
)
        
unwind_info
.
add_saved_register
(
self
.
SP_REGISTER
next_sp
)
        
return
unwind_info
    
def
unwind_ordinary
(
self
pc
pending_frame
)
:
        
return
self
.
create_frame
(
pc
self
.
next_sp
self
.
next_sp
                                 
self
.
next_type
pending_frame
)
    
def
unwind_exit_frame
(
self
pc
pending_frame
)
:
        
if
self
.
activation
=
=
0
:
            
return
None
        
elif
self
.
activation
is
None
:
            
ptd
=
self
.
get_tls_per_thread_data
(
)
            
self
.
activation
=
ptd
[
'
runtime_
'
]
[
'
jitActivation
'
]
            
jittop
=
ptd
[
'
runtime_
'
]
[
'
jitTop
'
]
        
else
:
            
jittop
=
self
.
activation
[
'
prevJitTop_
'
]
            
self
.
activation
=
self
.
activation
[
'
prevJitActivation_
'
]
        
if
jittop
=
=
0
:
            
return
None
        
exit_sp
=
pending_frame
.
read_register
(
self
.
SP_REGISTER
)
        
frame_type
=
self
.
typecache
.
JitFrame_Exit
        
return
self
.
create_frame
(
pc
exit_sp
jittop
frame_type
pending_frame
)
    
def
unwind_entry_frame
(
self
pc
pending_frame
)
:
        
sp
=
self
.
next_sp
        
self
.
add_frame
(
sp
name
=
'
JitFrame_Entry
'
)
        
frame_id
=
SpiderMonkeyFrameId
(
sp
pc
)
        
unwind_info
=
pending_frame
.
create_unwind_info
(
frame_id
)
        
self
.
unwind_entry_frame_registers
(
sp
unwind_info
)
        
self
.
next_sp
=
None
        
self
.
next_type
=
None
        
return
unwind_info
    
def
unwind
(
self
pending_frame
)
:
        
pc
=
pending_frame
.
read_register
(
self
.
PC_REGISTER
)
        
if
not
self
.
is_jit_address
(
long
(
pc
)
)
:
            
return
None
        
if
self
.
next_sp
is
not
None
:
            
if
self
.
next_type
=
=
self
.
typecache
.
JitFrame_Entry
:
                
return
self
.
unwind_entry_frame
(
pc
pending_frame
)
            
return
self
.
unwind_ordinary
(
pc
pending_frame
)
        
return
self
.
unwind_exit_frame
(
pc
pending_frame
)
class
x64UnwinderState
(
UnwinderState
)
:
    
SP_REGISTER
=
'
rsp
'
    
PC_REGISTER
=
'
rip
'
    
SENTINEL_REGISTER
=
'
rip
'
    
PUSHED_REGS
=
[
"
r15
"
"
r14
"
"
r13
"
"
r12
"
"
rbx
"
"
rbp
"
"
rip
"
]
    
def
unwind_entry_frame_registers
(
self
sp
unwind_info
)
:
        
sp
=
sp
.
cast
(
self
.
typecache
.
void_starstar
)
        
sp
=
sp
+
1
        
for
reg
in
self
.
PUSHED_REGS
:
            
data
=
sp
.
dereference
(
)
            
sp
=
sp
+
1
            
unwind_info
.
add_saved_register
(
reg
data
)
            
if
reg
is
"
rbp
"
:
                
unwind_info
.
add_saved_register
(
self
.
SP_REGISTER
sp
)
class
SpiderMonkeyUnwinder
(
Unwinder
)
:
    
UNWINDERS
=
[
x64UnwinderState
]
    
def
__init__
(
self
typecache
)
:
        
super
(
SpiderMonkeyUnwinder
self
)
.
__init__
(
"
SpiderMonkey
"
)
        
self
.
typecache
=
typecache
        
self
.
unwinder_state
=
None
        
self
.
enabled
=
False
        
gdb
.
write
(
"
SpiderMonkey
unwinder
is
disabled
by
default
to
enable
it
type
:
\
n
"
+
                  
"
\
tenable
unwinder
.
*
SpiderMonkey
\
n
"
)
        
gdb
.
events
.
cont
.
connect
(
self
.
invalidate_unwinder_state
)
        
assert
self
.
test_sentinels
(
)
    
def
test_sentinels
(
self
)
:
        
regs
=
{
}
        
for
unwinder
in
self
.
UNWINDERS
:
            
if
unwinder
.
SENTINEL_REGISTER
in
regs
:
                
return
False
            
regs
[
unwinder
.
SENTINEL_REGISTER
]
=
1
        
return
True
    
def
make_unwinder
(
self
pending_frame
)
:
        
for
unwinder
in
self
.
UNWINDERS
:
            
try
:
                
pending_frame
.
read_register
(
unwinder
.
SENTINEL_REGISTER
)
            
except
:
                
continue
            
return
unwinder
(
self
.
typecache
)
        
return
None
    
def
__call__
(
self
pending_frame
)
:
        
if
self
.
unwinder_state
is
None
or
not
self
.
unwinder_state
.
check
(
)
:
            
self
.
unwinder_state
=
self
.
make_unwinder
(
pending_frame
)
        
if
not
self
.
unwinder_state
:
            
return
None
        
return
self
.
unwinder_state
.
unwind
(
pending_frame
)
    
def
invalidate_unwinder_state
(
self
*
args
*
*
kwargs
)
:
        
self
.
unwinder_state
=
None
def
register_unwinder
(
objfile
)
:
    
unwinder
=
None
    
if
_have_unwinder
and
platform
.
system
(
)
=
=
"
Linux
"
:
        
unwinder
=
SpiderMonkeyUnwinder
(
UnwinderTypeCache
(
)
)
        
gdb
.
unwinder
.
register_unwinder
(
objfile
unwinder
replace
=
True
)
    
filt
=
SpiderMonkeyFrameFilter
(
unwinder
)
    
if
objfile
is
None
:
        
objfile
=
gdb
    
objfile
.
frame_filters
[
filt
.
name
]
=
filt
