import
os
import
sys
from
contextlib
import
contextmanager
JITFLAGS
=
{
    
"
all
"
:
[
        
[
]
        
[
            
"
-
-
ion
-
eager
"
            
"
-
-
ion
-
offthread
-
compile
=
off
"
            
"
-
-
more
-
compartments
"
        
]
        
[
            
"
-
-
ion
-
eager
"
            
"
-
-
ion
-
offthread
-
compile
=
off
"
            
"
-
-
ion
-
check
-
range
-
analysis
"
            
"
-
-
ion
-
extra
-
checks
"
            
"
-
-
no
-
sse3
"
            
"
-
-
no
-
threads
"
        
]
        
[
"
-
-
baseline
-
eager
"
"
-
-
write
-
protect
-
code
=
off
"
]
        
[
"
-
-
no
-
blinterp
"
"
-
-
no
-
baseline
"
"
-
-
no
-
ion
"
"
-
-
more
-
compartments
"
]
        
[
"
-
-
blinterp
-
eager
"
]
    
]
    
"
jstests
"
:
[
        
[
]
        
[
            
"
-
-
ion
-
eager
"
            
"
-
-
ion
-
offthread
-
compile
=
off
"
            
"
-
-
more
-
compartments
"
        
]
        
[
"
-
-
baseline
-
eager
"
"
-
-
write
-
protect
-
code
=
off
"
]
        
[
"
-
-
no
-
blinterp
"
"
-
-
no
-
baseline
"
"
-
-
no
-
ion
"
"
-
-
more
-
compartments
"
]
    
]
    
"
ion
"
:
[
        
[
"
-
-
baseline
-
eager
"
"
-
-
write
-
protect
-
code
=
off
"
]
        
[
"
-
-
ion
-
eager
"
"
-
-
ion
-
offthread
-
compile
=
off
"
"
-
-
more
-
compartments
"
]
    
]
    
"
debug
"
:
[
        
[
]
        
[
            
"
-
-
ion
-
eager
"
            
"
-
-
ion
-
offthread
-
compile
=
off
"
            
"
-
-
more
-
compartments
"
        
]
        
[
"
-
-
baseline
-
eager
"
"
-
-
write
-
protect
-
code
=
off
"
]
    
]
    
"
tsan
"
:
[
        
[
]
        
[
            
"
-
-
ion
-
eager
"
            
"
-
-
ion
-
check
-
range
-
analysis
"
            
"
-
-
ion
-
extra
-
checks
"
            
"
-
-
no
-
sse3
"
        
]
        
[
"
-
-
no
-
blinterp
"
"
-
-
no
-
baseline
"
"
-
-
no
-
ion
"
]
    
]
    
"
baseline
"
:
[
        
[
"
-
-
no
-
ion
"
]
    
]
    
"
interp
"
:
[
        
[
            
"
-
-
no
-
blinterp
"
            
"
-
-
no
-
baseline
"
            
"
-
-
no
-
asmjs
"
            
"
-
-
wasm
-
compiler
=
none
"
            
"
-
-
no
-
native
-
regexp
"
        
]
    
]
    
"
none
"
:
[
[
]
]
}
def
get_jitflags
(
variant
*
*
kwargs
)
:
    
if
variant
not
in
JITFLAGS
:
        
print
(
'
Invalid
jitflag
:
"
{
}
"
'
.
format
(
variant
)
)
        
sys
.
exit
(
1
)
    
if
variant
=
=
"
none
"
and
"
none
"
in
kwargs
:
        
return
kwargs
[
"
none
"
]
    
return
JITFLAGS
[
variant
]
def
valid_jitflags
(
)
:
    
return
JITFLAGS
.
keys
(
)
def
get_environment_overlay
(
js_shell
gc_zeal
)
:
    
"
"
"
    
Build
a
dict
of
additional
environment
variables
that
must
be
set
to
run
    
tests
successfully
.
    
"
"
"
    
env
=
{
        
"
TZ
"
:
"
PST8PDT
"
        
"
LC_ALL
"
:
"
en_US
.
UTF
-
8
"
        
"
XRE_NO_WINDOWS_CRASH_DIALOG
"
:
"
1
"
    
}
    
if
sys
.
platform
.
startswith
(
"
linux
"
)
:
        
env
[
"
LD_LIBRARY_PATH
"
]
=
os
.
path
.
dirname
(
js_shell
)
    
elif
sys
.
platform
.
startswith
(
"
darwin
"
)
:
        
env
[
"
DYLD_LIBRARY_PATH
"
]
=
os
.
path
.
dirname
(
js_shell
)
    
elif
sys
.
platform
.
startswith
(
"
win
"
)
:
        
env
[
"
PATH
"
]
=
os
.
path
.
dirname
(
js_shell
)
    
if
gc_zeal
:
        
env
[
"
JS_GC_ZEAL
"
]
=
gc_zeal
    
return
env
contextmanager
def
change_env
(
env_overlay
)
:
    
prior_env
=
{
}
    
for
key
val
in
env_overlay
.
items
(
)
:
        
prior_env
[
key
]
=
os
.
environ
.
get
(
key
None
)
        
if
"
PATH
"
in
key
and
key
in
os
.
environ
:
            
os
.
environ
[
key
]
=
"
{
}
{
}
{
}
"
.
format
(
val
os
.
pathsep
os
.
environ
[
key
]
)
        
else
:
            
os
.
environ
[
key
]
=
val
    
try
:
        
yield
    
finally
:
        
for
key
val
in
prior_env
.
items
(
)
:
            
if
val
is
not
None
:
                
os
.
environ
[
key
]
=
val
            
else
:
                
del
os
.
environ
[
key
]
def
get_cpu_count
(
)
:
    
"
"
"
    
Guess
at
a
reasonable
parallelism
count
to
set
as
the
default
for
the
    
current
machine
and
run
.
    
"
"
"
    
try
:
        
import
multiprocessing
        
return
multiprocessing
.
cpu_count
(
)
    
except
(
ImportError
NotImplementedError
)
:
        
pass
    
try
:
        
res
=
int
(
os
.
sysconf
(
"
SC_NPROCESSORS_ONLN
"
)
)
        
if
res
>
0
:
            
return
res
    
except
(
AttributeError
ValueError
)
:
        
pass
    
try
:
        
res
=
int
(
os
.
environ
[
"
NUMBER_OF_PROCESSORS
"
]
)
        
if
res
>
0
:
            
return
res
    
except
(
KeyError
ValueError
)
:
        
pass
    
return
1
class
RefTestCase
(
object
)
:
    
"
"
"
A
test
case
consisting
of
a
test
and
an
expected
result
.
"
"
"
    
def
__init__
(
self
root
path
extra_helper_paths
=
None
wpt
=
None
)
:
        
self
.
root
=
root
        
self
.
path
=
path
        
self
.
options
=
[
]
        
self
.
jitflags
=
[
]
        
self
.
ignoredflags
=
[
]
        
self
.
test_reflect_stringify
=
None
        
self
.
is_module
=
False
        
self
.
is_async
=
False
        
self
.
enable
=
True
        
self
.
error
=
None
        
self
.
expect
=
True
        
self
.
random
=
False
        
self
.
slow
=
False
        
self
.
heavy
=
False
        
self
.
is_test262_raw
=
False
        
self
.
selfhosted_xdr_path
=
None
        
self
.
selfhosted_xdr_mode
=
"
off
"
        
self
.
terms
=
None
        
self
.
tag
=
None
        
self
.
comment
=
None
        
self
.
extra_helper_paths
=
extra_helper_paths
or
[
]
        
self
.
wpt
=
wpt
    
def
prefix_command
(
self
)
:
        
"
"
"
Return
the
'
-
f
'
options
needed
to
run
a
test
with
the
given
path
.
"
"
"
        
path
=
self
.
path
        
prefix
=
[
]
        
while
path
!
=
"
"
:
            
assert
path
!
=
"
/
"
            
path
=
os
.
path
.
dirname
(
path
)
            
if
self
.
is_test262_raw
and
path
!
=
"
"
:
                
continue
            
shell_path
=
os
.
path
.
join
(
self
.
root
path
"
shell
.
js
"
)
            
if
os
.
path
.
exists
(
shell_path
)
:
                
prefix
.
append
(
shell_path
)
                
prefix
.
append
(
"
-
f
"
)
        
prefix
.
reverse
(
)
        
for
extra_path
in
self
.
extra_helper_paths
:
            
prefix
.
append
(
"
-
f
"
)
            
prefix
.
append
(
extra_path
)
        
return
prefix
    
def
abs_path
(
self
)
:
        
return
os
.
path
.
join
(
self
.
root
self
.
path
)
    
def
get_command
(
self
prefix
tempdir
)
:
        
cmd
=
prefix
+
self
.
jitflags
+
self
.
options
+
self
.
prefix_command
(
)
        
if
self
.
selfhosted_xdr_mode
!
=
"
off
"
:
            
self
.
selfhosted_xdr_path
=
os
.
path
.
join
(
tempdir
"
shell
.
xdr
"
)
            
cmd
+
=
[
                
"
-
-
selfhosted
-
xdr
-
path
"
                
self
.
selfhosted_xdr_path
                
"
-
-
selfhosted
-
xdr
-
mode
"
                
self
.
selfhosted_xdr_mode
            
]
        
if
self
.
test_reflect_stringify
is
not
None
:
            
cmd
+
=
[
self
.
test_reflect_stringify
"
-
-
check
"
self
.
abs_path
(
)
]
        
elif
self
.
is_module
:
            
cmd
+
=
[
"
-
-
module
"
self
.
abs_path
(
)
]
        
else
:
            
cmd
+
=
[
"
-
f
"
self
.
abs_path
(
)
]
        
for
flag
in
self
.
ignoredflags
:
            
if
flag
in
cmd
:
                
cmd
.
remove
(
flag
)
        
return
cmd
    
def
__str__
(
self
)
:
        
ans
=
self
.
path
        
if
not
self
.
enable
:
            
ans
+
=
"
skip
"
        
if
self
.
error
is
not
None
:
            
ans
+
=
"
error
=
"
+
self
.
error
        
if
not
self
.
expect
:
            
ans
+
=
"
fails
"
        
if
self
.
random
:
            
ans
+
=
"
random
"
        
if
self
.
slow
:
            
ans
+
=
"
slow
"
        
if
self
.
heavy
:
            
ans
+
=
"
heavy
"
        
if
"
-
d
"
in
self
.
options
:
            
ans
+
=
"
debugMode
"
        
return
ans
    
staticmethod
    
def
build_js_cmd_prefix
(
js_path
js_args
debugger_prefix
)
:
        
parts
=
[
]
        
if
debugger_prefix
:
            
parts
+
=
debugger_prefix
        
parts
.
append
(
js_path
)
        
if
js_args
:
            
parts
+
=
js_args
        
return
parts
    
def
__cmp__
(
self
other
)
:
        
if
self
.
path
=
=
other
.
path
:
            
return
0
        
elif
self
.
path
<
other
.
path
:
            
return
-
1
        
return
1
    
def
__hash__
(
self
)
:
        
return
self
.
path
.
__hash__
(
)
    
def
__repr__
(
self
)
:
        
return
"
<
lib
.
tests
.
RefTestCase
%
s
>
"
%
(
self
.
path
)
