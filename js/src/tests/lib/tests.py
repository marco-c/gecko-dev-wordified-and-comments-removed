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
    
'
all
'
:
[
        
[
]
        
[
'
-
-
ion
-
eager
'
'
-
-
ion
-
offthread
-
compile
=
off
'
]
        
[
'
-
-
ion
-
eager
'
'
-
-
ion
-
offthread
-
compile
=
off
'
         
'
-
-
ion
-
check
-
range
-
analysis
'
'
-
-
ion
-
extra
-
checks
'
'
-
-
no
-
sse3
'
'
-
-
no
-
threads
'
]
        
[
'
-
-
baseline
-
eager
'
]
        
[
'
-
-
no
-
baseline
'
'
-
-
no
-
ion
'
]
    
]
    
'
ion
'
:
[
        
[
'
-
-
baseline
-
eager
'
]
        
[
'
-
-
ion
-
eager
'
'
-
-
ion
-
offthread
-
compile
=
off
'
]
    
]
    
'
debug
'
:
[
        
[
]
        
[
'
-
-
ion
-
eager
'
'
-
-
ion
-
offthread
-
compile
=
off
'
]
        
[
'
-
-
baseline
-
eager
'
]
    
]
    
'
tsan
'
:
[
        
[
]
        
[
'
-
-
ion
-
eager
'
'
-
-
ion
-
check
-
range
-
analysis
'
'
-
-
ion
-
extra
-
checks
'
'
-
-
no
-
sse3
'
]
        
[
'
-
-
no
-
baseline
'
'
-
-
no
-
ion
'
]
    
]
    
'
baseline
'
:
[
        
[
'
-
-
no
-
ion
'
]
    
]
    
'
interp
'
:
[
        
[
'
-
-
no
-
baseline
'
'
-
-
no
-
asmjs
'
'
-
-
no
-
wasm
'
'
-
-
no
-
native
-
regexp
'
]
    
]
    
'
none
'
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
'
none
'
and
'
none
'
in
kwargs
:
        
return
kwargs
[
'
none
'
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
        
'
TZ
'
:
'
PST8PDT
'
        
'
LC_TIME
'
:
'
en_US
.
UTF
-
8
'
        
'
XRE_NO_WINDOWS_CRASH_DIALOG
'
:
'
1
'
    
}
    
if
sys
.
platform
.
startswith
(
'
linux
'
)
:
        
env
[
'
LD_LIBRARY_PATH
'
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
'
darwin
'
)
:
        
env
[
'
DYLD_LIBRARY_PATH
'
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
'
win
'
)
:
        
env
[
'
PATH
'
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
'
PATH
'
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
'
{
}
{
}
{
}
'
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
'
SC_NPROCESSORS_ONLN
'
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
'
NUMBER_OF_PROCESSORS
'
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
path
)
:
        
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
    
staticmethod
    
def
prefix_command
(
path
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
shell
.
js
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
        
prefix
=
[
]
        
while
path
!
=
'
'
:
            
assert
path
!
=
'
/
'
            
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
            
shell_path
=
os
.
path
.
join
(
path
'
shell
.
js
'
)
            
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
'
-
f
'
)
        
prefix
.
reverse
(
)
        
return
prefix
    
def
get_command
(
self
prefix
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
\
            
+
RefTestCase
.
prefix_command
(
self
.
path
)
        
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
path
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
path
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
path
]
        
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
'
skip
'
        
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
'
error
=
'
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
'
fails
'
        
if
self
.
random
:
            
ans
+
=
'
random
'
        
if
self
.
slow
:
            
ans
+
=
'
slow
'
        
if
'
-
d
'
in
self
.
options
:
            
ans
+
=
'
debugMode
'
        
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
