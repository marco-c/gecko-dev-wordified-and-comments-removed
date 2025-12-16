import
re
import
gdb
patterns
=
[
    
(
        
"
__memmove
"
        
1
        
"
js
:
:
jit
:
:
X86Encoding
:
:
BaseAssembler
:
:
executableCopy
"
        
"
src
"
        
"
dst
"
    
)
    
(
        
"
__memcpy
"
        
1
        
"
js
:
:
jit
:
:
X86Encoding
:
:
BaseAssembler
:
:
executableCopy
"
        
"
src
"
        
"
dst
"
    
)
    
(
        
"
__memmove
"
        
1
        
"
arena_t
:
:
RallocSmallOrLarge
"
        
"
aPtr
"
        
"
ret
"
    
)
    
(
"
__memcpy
"
1
"
arena_t
:
:
RallocSmallOrLarge
"
"
aPtr
"
"
ret
"
)
    
(
        
"
mozilla
:
:
detail
:
:
VectorImpl
<
.
*
>
:
:
new_
<
.
*
>
"
        
3
        
"
mozilla
:
:
Vector
<
.
*
>
:
:
convertToHeapStorage
"
        
"
beginNoCheck
(
)
"
        
"
newBuf
"
    
)
    
(
        
"
__memmove
"
        
1
        
"
js
:
:
jit
:
:
AssemblerBufferWithConstantPools
"
        
"
&
cur
-
>
instructions
[
0
]
"
        
"
dest
"
    
)
    
(
        
"
__memcpy
"
        
1
        
"
js
:
:
jit
:
:
AssemblerBufferWithConstantPools
"
        
"
&
cur
-
>
instructions
[
0
]
"
        
"
dest
"
    
)
    
(
        
"
__memcpy
"
        
2
        
"
js
:
:
jit
:
:
AssemblerX86Shared
:
:
executableCopy
"
        
"
masm
.
m_formatter
.
m_buffer
.
m_buffer
.
mBegin
"
        
"
buffer
"
    
)
    
(
"
__memcpy
"
1
"
arena_t
:
:
RallocSmallOrLarge
"
"
aPtr
"
"
ret
"
)
    
(
"
js
:
:
jit
:
:
X86Encoding
:
:
SetInt32
"
0
"
js
:
:
jit
:
:
X86Encoding
:
:
SetInt32
"
"
0
"
"
0
"
)
    
(
        
"
js
:
:
jit
:
:
X86Encoding
:
:
SetPointer
"
        
0
        
"
js
:
:
jit
:
:
X86Encoding
:
:
SetPointer
"
        
"
0
"
        
"
0
"
    
)
    
(
        
"
<
unnamed
>
"
        
1
        
"
js
:
:
jit
:
:
AssemblerBufferWithConstantPools
<
.
*
>
:
:
executableCopy
"
        
"
&
cur
-
>
instructions
[
0
]
"
        
"
dest
"
    
)
    
(
"
std
:
:
__copy_move
"
4
"
CopySpan
"
"
source
.
data
(
)
"
"
target
.
data
(
)
"
)
    
(
        
"
__memmove_
(
avx
|
evex
)
_unaligned_erms
"
        
1
        
"
mozilla
:
:
detail
:
:
EndianUtils
:
:
copyAndSwapTo
<
.
*
0
.
*
0
"
        
"
aSrc
"
        
"
(
size_t
)
aDest
"
    
)
]
class
JitSource
(
gdb
.
Command
)
:
    
def
__init__
(
self
)
:
        
super
(
)
.
__init__
(
"
jitsrc
"
gdb
.
COMMAND_RUNNING
)
        
self
.
dont_repeat
(
)
    
def
disable_breakpoints
(
self
)
:
        
self
.
disabled_breakpoints
=
[
b
for
b
in
gdb
.
breakpoints
(
)
if
b
.
enabled
]
        
for
b
in
self
.
disabled_breakpoints
:
            
b
.
enabled
=
False
    
def
enable_breakpoints
(
self
)
:
        
for
b
in
self
.
disabled_breakpoints
:
            
b
.
enabled
=
True
    
def
search_stack
(
self
base_name
hops
name
src
dst
address
)
:
        
current_frame_name
=
gdb
.
newest_frame
(
)
.
name
(
)
or
"
<
unnamed
>
"
        
if
not
re
.
match
(
base_name
current_frame_name
)
:
            
return
None
        
f
=
gdb
.
newest_frame
(
)
        
for
_
in
range
(
hops
)
:
            
f
=
f
.
older
(
)
        
if
not
re
.
match
(
name
f
.
name
(
)
or
"
<
unnamed
>
"
)
:
            
return
None
        
f
.
select
(
)
        
src_val
=
gdb
.
parse_and_eval
(
src
)
        
dst_val
=
gdb
.
parse_and_eval
(
dst
)
        
return
hex
(
src_val
+
int
(
address
16
)
-
dst_val
)
    
def
next_address
(
self
old
)
:
        
for
pattern
in
patterns
:
            
found
=
self
.
search_stack
(
*
pattern
old
)
            
if
found
:
                
return
found
        
return
None
    
def
runback
(
self
address
)
:
        
b
=
gdb
.
Breakpoint
(
            
"
*
"
+
address
type
=
gdb
.
BP_WATCHPOINT
wp_class
=
gdb
.
WP_WRITE
internal
=
True
        
)
        
try
:
            
while
b
.
hit_count
=
=
0
:
                
gdb
.
execute
(
"
rc
"
to_string
=
True
)
        
finally
:
            
b
.
delete
(
)
    
def
invoke
(
self
arg
from_tty
)
:
        
args
=
gdb
.
string_to_argv
(
arg
)
        
address
=
args
[
0
]
        
self
.
disable_breakpoints
(
)
        
while
address
:
            
self
.
runback
(
address
)
            
address
=
self
.
next_address
(
address
)
        
self
.
enable_breakpoints
(
)
JitSource
(
)
