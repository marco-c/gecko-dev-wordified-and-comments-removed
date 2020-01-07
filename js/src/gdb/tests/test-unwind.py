import
platform
def
do_unwinder_test
(
)
:
    
import
gdb
    
gdb
.
execute
(
"
enable
unwinder
.
*
SpiderMonkey
"
)
    
run_fragment
(
'
unwind
.
simple
'
'
Something
'
)
    
first
=
True
    
found_entry
=
False
    
found_exit
=
False
    
found_main
=
False
    
found_inner
=
False
    
found_outer
=
False
    
frames
=
list
(
gdb
.
frames
.
execute_frame_filters
(
gdb
.
newest_frame
(
)
0
-
1
)
)
    
for
frame
in
frames
:
        
print
(
"
examining
"
+
frame
.
function
(
)
)
        
if
first
:
            
assert_eq
(
frame
.
function
(
)
.
startswith
(
"
Something
"
)
True
)
            
first
=
False
        
elif
frame
.
function
(
)
=
=
"
<
<
JitFrame_Exit
>
>
"
:
            
found_exit
=
True
        
elif
frame
.
function
(
)
=
=
"
<
<
JitFrame_CppToJSJit
>
>
"
:
            
found_entry
=
True
        
elif
frame
.
function
(
)
=
=
"
main
"
:
            
found_main
=
True
        
elif
"
unwindFunctionInner
"
in
frame
.
function
(
)
:
            
found_inner
=
True
        
elif
"
unwindFunctionOuter
"
in
frame
.
function
(
)
:
            
found_outer
=
True
    
assert_eq
(
first
False
)
    
assert_eq
(
found_main
True
)
    
assert_eq
(
found_exit
True
)
    
assert_eq
(
found_entry
True
)
    
assert_eq
(
found_inner
True
)
    
assert_eq
(
found_outer
True
)
if
platform
.
machine
(
)
=
=
'
x86_64
'
and
platform
.
system
(
)
=
=
'
Linux
'
:
    
try
:
        
import
gdb
.
unwinder
        
do_unwinder_test
(
)
    
except
Exception
:
        
pass
