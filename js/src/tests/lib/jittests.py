from
__future__
import
print_function
import
os
import
posixpath
import
re
import
sys
import
traceback
from
collections
import
namedtuple
from
datetime
import
datetime
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
or
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
    
from
tasks_unix
import
run_all_tests
else
:
    
from
tasks_win
import
run_all_tests
from
progressbar
import
ProgressBar
NullProgressBar
from
results
import
TestOutput
escape_cmdline
from
structuredlog
import
TestLogger
TESTS_LIB_DIR
=
os
.
path
.
dirname
(
os
.
path
.
abspath
(
__file__
)
)
JS_DIR
=
os
.
path
.
dirname
(
os
.
path
.
dirname
(
TESTS_LIB_DIR
)
)
TOP_SRC_DIR
=
os
.
path
.
dirname
(
os
.
path
.
dirname
(
JS_DIR
)
)
TEST_DIR
=
os
.
path
.
join
(
JS_DIR
'
jit
-
test
'
'
tests
'
)
LIB_DIR
=
os
.
path
.
join
(
JS_DIR
'
jit
-
test
'
'
lib
'
)
+
os
.
path
.
sep
MODULE_DIR
=
os
.
path
.
join
(
JS_DIR
'
jit
-
test
'
'
modules
'
)
+
os
.
path
.
sep
JS_TESTS_DIR
=
posixpath
.
join
(
JS_DIR
'
tests
'
)
def
_relpath
(
path
start
=
None
)
:
    
"
"
"
Return
a
relative
version
of
a
path
"
"
"
    
if
not
path
:
        
raise
ValueError
(
"
no
path
specified
"
)
    
if
start
is
None
:
        
start
=
os
.
curdir
    
start_list
=
os
.
path
.
abspath
(
start
)
.
split
(
os
.
sep
)
    
path_list
=
os
.
path
.
abspath
(
path
)
.
split
(
os
.
sep
)
    
i
=
len
(
os
.
path
.
commonprefix
(
[
start_list
path_list
]
)
)
    
rel_list
=
[
os
.
pardir
]
*
(
len
(
start_list
)
-
i
)
+
path_list
[
i
:
]
    
if
not
rel_list
:
        
return
os
.
curdir
    
return
os
.
path
.
join
(
*
rel_list
)
QUOTE_MAP
=
{
    
'
\
\
'
:
'
\
\
\
\
'
    
'
\
b
'
:
'
\
\
b
'
    
'
\
f
'
:
'
\
\
f
'
    
'
\
n
'
:
'
\
\
n
'
    
'
\
r
'
:
'
\
\
r
'
    
'
\
t
'
:
'
\
\
t
'
    
'
\
v
'
:
'
\
\
v
'
}
def
js_quote
(
quote
s
)
:
    
result
=
quote
    
for
c
in
s
:
        
if
c
=
=
quote
:
            
result
+
=
'
\
\
'
+
quote
        
elif
c
in
QUOTE_MAP
:
            
result
+
=
QUOTE_MAP
[
c
]
        
else
:
            
result
+
=
c
    
result
+
=
quote
    
return
result
os
.
path
.
relpath
=
_relpath
def
extend_condition
(
condition
value
)
:
    
if
condition
:
        
condition
+
=
"
|
|
"
    
condition
+
=
"
(
{
}
)
"
.
format
(
value
)
    
return
condition
class
JitTest
:
    
VALGRIND_CMD
=
[
]
    
paths
=
(
d
for
d
in
os
.
environ
[
'
PATH
'
]
.
split
(
os
.
pathsep
)
)
    
valgrinds
=
(
os
.
path
.
join
(
d
'
valgrind
'
)
for
d
in
paths
)
    
if
any
(
os
.
path
.
exists
(
p
)
for
p
in
valgrinds
)
:
        
VALGRIND_CMD
=
[
            
'
valgrind
'
'
-
q
'
'
-
-
smc
-
check
=
all
-
non
-
file
'
            
'
-
-
error
-
exitcode
=
1
'
'
-
-
gen
-
suppressions
=
all
'
            
'
-
-
show
-
possibly
-
lost
=
no
'
'
-
-
leak
-
check
=
full
'
        
]
        
if
os
.
uname
(
)
[
0
]
=
=
'
Darwin
'
:
            
VALGRIND_CMD
.
append
(
'
-
-
dsymutil
=
yes
'
)
    
del
paths
    
del
valgrinds
    
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
relpath_top
=
os
.
path
.
relpath
(
path
TOP_SRC_DIR
)
        
self
.
relpath_tests
=
os
.
path
.
relpath
(
path
TEST_DIR
)
        
self
.
jitflags
=
[
]
        
self
.
slow
=
False
        
self
.
allow_oom
=
False
        
self
.
allow_unhandlable_oom
=
False
        
self
.
allow_overrecursed
=
False
        
self
.
valgrind
=
False
        
self
.
tz_pacific
=
False
        
self
.
other_includes
=
[
]
        
self
.
test_also
=
[
]
        
self
.
test_join
=
[
]
        
self
.
expect_error
=
'
'
        
self
.
expect_status
=
0
        
self
.
expect_crash
=
False
        
self
.
is_module
=
False
        
self
.
is_binast
=
False
        
self
.
test_reflect_stringify
=
None
        
self
.
skip_if_cond
=
'
'
        
self
.
skip_variant_if_cond
=
{
}
        
self
.
enable
=
True
    
def
copy
(
self
)
:
        
t
=
JitTest
(
self
.
path
)
        
t
.
jitflags
=
self
.
jitflags
[
:
]
        
t
.
slow
=
self
.
slow
        
t
.
allow_oom
=
self
.
allow_oom
        
t
.
allow_unhandlable_oom
=
self
.
allow_unhandlable_oom
        
t
.
allow_overrecursed
=
self
.
allow_overrecursed
        
t
.
valgrind
=
self
.
valgrind
        
t
.
tz_pacific
=
self
.
tz_pacific
        
t
.
other_includes
=
self
.
other_includes
[
:
]
        
t
.
test_also
=
self
.
test_also
        
t
.
test_join
=
self
.
test_join
        
t
.
expect_error
=
self
.
expect_error
        
t
.
expect_status
=
self
.
expect_status
        
t
.
expect_crash
=
self
.
expect_crash
        
t
.
test_reflect_stringify
=
self
.
test_reflect_stringify
        
t
.
enable
=
True
        
t
.
is_module
=
self
.
is_module
        
t
.
is_binast
=
self
.
is_binast
        
t
.
skip_if_cond
=
self
.
skip_if_cond
        
t
.
skip_variant_if_cond
=
self
.
skip_variant_if_cond
        
return
t
    
def
copy_and_extend_jitflags
(
self
variant
)
:
        
t
=
self
.
copy
(
)
        
t
.
jitflags
.
extend
(
variant
)
        
for
flags
in
variant
:
            
if
flags
in
self
.
skip_variant_if_cond
:
                
t
.
skip_if_cond
=
extend_condition
(
t
.
skip_if_cond
self
.
skip_variant_if_cond
[
flags
]
)
        
return
t
    
def
copy_variants
(
self
variants
)
:
        
variants
=
variants
+
self
.
test_also
        
for
join_opts
in
self
.
test_join
:
            
variants
=
variants
+
[
opts
+
join_opts
for
opts
in
variants
]
        
return
[
self
.
copy_and_extend_jitflags
(
v
)
for
v
in
variants
]
    
COOKIE
=
'
|
jit
-
test
|
'
    
SKIPPED_EXIT_STATUS
=
59
    
Directives
=
{
}
    
classmethod
    
def
find_directives
(
cls
file_name
)
:
        
meta
=
'
'
        
line
=
open
(
file_name
)
.
readline
(
)
        
i
=
line
.
find
(
cls
.
COOKIE
)
        
if
i
!
=
-
1
:
            
meta
=
'
;
'
+
line
[
i
+
len
(
cls
.
COOKIE
)
:
]
.
strip
(
'
\
n
'
)
        
return
meta
    
classmethod
    
def
from_file
(
cls
path
options
)
:
        
test
=
cls
(
path
)
        
dir_meta
=
'
'
        
dir_name
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
dir_name
in
cls
.
Directives
:
            
dir_meta
=
cls
.
Directives
[
dir_name
]
        
else
:
            
meta_file_name
=
os
.
path
.
join
(
dir_name
"
directives
.
txt
"
)
            
if
os
.
path
.
exists
(
meta_file_name
)
:
                
dir_meta
=
cls
.
find_directives
(
meta_file_name
)
            
cls
.
Directives
[
dir_name
]
=
dir_meta
        
filename
file_extension
=
os
.
path
.
splitext
(
path
)
        
if
file_extension
=
=
'
.
binjs
'
:
            
meta_file_name
=
filename
+
'
.
dir
'
            
if
os
.
path
.
exists
(
meta_file_name
)
:
                
meta
=
cls
.
find_directives
(
meta_file_name
)
            
else
:
                
meta
=
'
'
            
test
.
is_binast
=
True
        
else
:
            
meta
=
cls
.
find_directives
(
path
)
        
if
meta
!
=
'
'
or
dir_meta
!
=
'
'
:
            
meta
=
meta
+
dir_meta
            
parts
=
meta
.
split
(
'
;
'
)
            
for
part
in
parts
:
                
part
=
part
.
strip
(
)
                
if
not
part
:
                    
continue
                
name
_
value
=
part
.
partition
(
'
:
'
)
                
if
value
:
                    
value
=
value
.
strip
(
)
                    
if
name
=
=
'
error
'
:
                        
test
.
expect_error
=
value
                    
elif
name
=
=
'
exitstatus
'
:
                        
try
:
                            
status
=
int
(
value
0
)
                            
if
status
=
=
test
.
SKIPPED_EXIT_STATUS
:
                                
print
(
"
warning
:
jit
-
tests
uses
{
}
as
a
sentinel
"
                                      
"
return
value
{
}
"
test
.
SKIPPED_EXIT_STATUS
path
)
                            
else
:
                                
test
.
expect_status
=
status
                        
except
ValueError
:
                            
print
(
"
warning
:
couldn
'
t
parse
exit
status
"
                                  
"
{
}
"
.
format
(
value
)
)
                    
elif
name
=
=
'
thread
-
count
'
:
                        
try
:
                            
test
.
jitflags
.
append
(
'
-
-
thread
-
count
=
{
}
'
.
format
(
                                
int
(
value
0
)
)
)
                        
except
ValueError
:
                            
print
(
"
warning
:
couldn
'
t
parse
thread
-
count
"
                                  
"
{
}
"
.
format
(
value
)
)
                    
elif
name
=
=
'
include
'
:
                        
test
.
other_includes
.
append
(
value
)
                    
elif
name
=
=
'
skip
-
if
'
:
                        
test
.
skip_if_cond
=
extend_condition
(
test
.
skip_if_cond
value
)
                    
elif
name
=
=
'
skip
-
variant
-
if
'
:
                        
try
:
                            
[
variant
condition
]
=
value
.
split
(
'
'
)
                            
test
.
skip_variant_if_cond
[
variant
]
=
extend_condition
(
                                
test
.
skip_if_cond
                                
condition
)
                        
except
ValueError
:
                            
print
(
"
warning
:
couldn
'
t
parse
skip
-
variant
-
if
"
)
                    
else
:
                        
print
(
'
{
}
:
warning
:
unrecognized
|
jit
-
test
|
attribute
'
                              
'
{
}
'
.
format
(
path
part
)
)
                
else
:
                    
if
name
=
=
'
slow
'
:
                        
test
.
slow
=
True
                    
elif
name
=
=
'
allow
-
oom
'
:
                        
test
.
allow_oom
=
True
                    
elif
name
=
=
'
allow
-
unhandlable
-
oom
'
:
                        
test
.
allow_unhandlable_oom
=
True
                    
elif
name
=
=
'
allow
-
overrecursed
'
:
                        
test
.
allow_overrecursed
=
True
                    
elif
name
=
=
'
valgrind
'
:
                        
test
.
valgrind
=
options
.
valgrind
                    
elif
name
=
=
'
tz
-
pacific
'
:
                        
test
.
tz_pacific
=
True
                    
elif
name
.
startswith
(
'
test
-
also
=
'
)
:
                        
test
.
test_also
.
append
(
re
.
split
(
r
'
\
s
+
'
name
[
len
(
'
test
-
also
=
'
)
:
]
)
)
                    
elif
name
.
startswith
(
'
test
-
join
=
'
)
:
                        
test
.
test_join
.
append
(
re
.
split
(
r
'
\
s
+
'
name
[
len
(
'
test
-
join
=
'
)
:
]
)
)
                    
elif
name
=
=
'
module
'
:
                        
test
.
is_module
=
True
                    
elif
name
=
=
'
crash
'
:
                        
test
.
expect_crash
=
True
                    
elif
name
.
startswith
(
'
-
-
'
)
:
                        
test
.
jitflags
.
append
(
name
)
                    
else
:
                        
print
(
'
{
}
:
warning
:
unrecognized
|
jit
-
test
|
attribute
'
                              
'
{
}
'
.
format
(
path
part
)
)
        
if
options
.
valgrind_all
:
            
test
.
valgrind
=
True
        
if
options
.
test_reflect_stringify
is
not
None
:
            
test
.
expect_error
=
'
'
            
test
.
expect_status
=
0
        
return
test
    
def
command
(
self
prefix
libdir
moduledir
remote_prefix
=
None
)
:
        
path
=
self
.
path
        
if
remote_prefix
:
            
path
=
self
.
path
.
replace
(
TEST_DIR
remote_prefix
)
        
scriptdir_var
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
not
scriptdir_var
.
endswith
(
'
/
'
)
:
            
scriptdir_var
+
=
'
/
'
        
if
remote_prefix
:
            
quotechar
=
'
"
'
        
else
:
            
quotechar
=
"
'
"
        
exprs
=
[
"
const
platform
=
{
}
"
.
format
(
js_quote
(
quotechar
sys
.
platform
)
)
                 
"
const
libdir
=
{
}
"
.
format
(
js_quote
(
quotechar
libdir
)
)
                 
"
const
scriptdir
=
{
}
"
.
format
(
js_quote
(
quotechar
scriptdir_var
)
)
]
        
cmd
=
prefix
+
[
]
        
cmd
+
=
list
(
set
(
self
.
jitflags
)
)
        
for
expr
in
exprs
:
            
cmd
+
=
[
'
-
e
'
expr
]
        
for
inc
in
self
.
other_includes
:
            
cmd
+
=
[
'
-
f
'
libdir
+
inc
]
        
if
self
.
skip_if_cond
:
            
cmd
+
=
[
'
-
e
'
"
if
(
{
}
)
quit
(
{
}
)
"
.
format
(
self
.
skip_if_cond
self
.
SKIPPED_EXIT_STATUS
)
]
        
cmd
+
=
[
'
-
-
module
-
load
-
path
'
moduledir
]
        
if
self
.
is_module
:
            
cmd
+
=
[
'
-
-
module
'
path
]
        
elif
self
.
is_binast
:
            
cmd
+
=
[
'
-
B
'
path
]
        
elif
self
.
test_reflect_stringify
is
None
:
            
cmd
+
=
[
'
-
f
'
path
]
        
else
:
            
cmd
+
=
[
'
-
-
'
self
.
test_reflect_stringify
"
-
-
check
"
path
]
        
if
self
.
valgrind
:
            
cmd
=
self
.
VALGRIND_CMD
+
cmd
        
if
self
.
allow_unhandlable_oom
or
self
.
expect_crash
:
            
cmd
+
=
[
'
-
-
suppress
-
minidump
'
]
        
return
cmd
    
js_cmd_prefix
=
None
    
def
get_command
(
self
prefix
)
:
        
"
"
"
Shim
for
the
test
runner
.
"
"
"
        
return
self
.
command
(
prefix
LIB_DIR
MODULE_DIR
)
def
find_tests
(
substring
=
None
run_binast
=
False
)
:
    
ans
=
[
]
    
for
dirpath
dirnames
filenames
in
os
.
walk
(
TEST_DIR
)
:
        
dirnames
.
sort
(
)
        
filenames
.
sort
(
)
        
if
dirpath
=
=
'
.
'
:
            
continue
        
if
not
run_binast
:
            
if
os
.
path
.
join
(
'
binast
'
'
lazy
'
)
in
dirpath
:
                
continue
            
if
os
.
path
.
join
(
'
binast
'
'
nonlazy
'
)
in
dirpath
:
                
continue
            
if
os
.
path
.
join
(
'
binast
'
'
invalid
'
)
in
dirpath
:
                
continue
        
for
filename
in
filenames
:
            
if
not
(
filename
.
endswith
(
'
.
js
'
)
or
filename
.
endswith
(
'
.
binjs
'
)
)
:
                
continue
            
if
filename
in
(
'
shell
.
js
'
'
browser
.
js
'
)
:
                
continue
            
test
=
os
.
path
.
join
(
dirpath
filename
)
            
if
substring
is
None
\
               
or
substring
in
os
.
path
.
relpath
(
test
TEST_DIR
)
:
                
ans
.
append
(
test
)
    
return
ans
def
run_test_remote
(
test
device
prefix
options
)
:
    
from
mozdevice
import
ADBDevice
ADBProcessError
    
if
options
.
test_reflect_stringify
:
        
raise
ValueError
(
"
can
'
t
run
Reflect
.
stringify
tests
remotely
"
)
    
cmd
=
test
.
command
(
prefix
                       
posixpath
.
join
(
options
.
remote_test_root
'
lib
/
'
)
                       
posixpath
.
join
(
options
.
remote_test_root
'
modules
/
'
)
                       
posixpath
.
join
(
options
.
remote_test_root
'
tests
'
)
)
    
if
options
.
show_cmd
:
        
print
(
escape_cmdline
(
cmd
)
)
    
env
=
{
}
    
if
test
.
tz_pacific
:
        
env
[
'
TZ
'
]
=
'
PST8PDT
'
    
env
[
'
LD_LIBRARY_PATH
'
]
=
options
.
remote_test_root
    
cmd
=
ADBDevice
.
_escape_command_line
(
cmd
)
    
start
=
datetime
.
now
(
)
    
try
:
        
out
=
device
.
shell_output
(
cmd
env
=
env
                                  
cwd
=
options
.
remote_test_root
                                  
timeout
=
int
(
options
.
timeout
)
)
        
returncode
=
0
    
except
ADBProcessError
as
e
:
        
out
=
str
(
e
.
adb_process
.
stdout
)
        
returncode
=
e
.
adb_process
.
exitcode
        
re_ignore
=
re
.
compile
(
r
'
error
:
(
closed
|
device
.
*
not
found
)
'
)
        
if
returncode
=
=
1
and
re_ignore
.
search
(
out
)
:
            
print
(
"
Skipping
{
}
due
to
ignorable
adb
error
{
}
"
.
format
(
test
.
path
out
)
)
            
test
.
skip_if_cond
=
"
true
"
            
returncode
=
test
.
SKIPPED_EXIT_STATUS
    
elapsed
=
(
datetime
.
now
(
)
-
start
)
.
total_seconds
(
)
    
return
TestOutput
(
test
cmd
out
out
returncode
elapsed
False
)
def
check_output
(
out
err
rc
timed_out
test
options
)
:
    
if
test
.
skip_if_cond
:
        
if
rc
=
=
test
.
SKIPPED_EXIT_STATUS
:
            
return
True
    
if
timed_out
:
        
if
os
.
path
.
normpath
(
test
.
relpath_tests
)
.
replace
(
os
.
sep
'
/
'
)
\
                
in
options
.
ignore_timeouts
:
            
return
True
        
if
sys
.
platform
=
=
'
win32
'
:
            
ver
=
sys
.
getwindowsversion
(
)
            
if
ver
.
major
=
=
6
and
ver
.
minor
<
=
1
:
                
return
True
        
return
False
    
if
test
.
expect_error
:
        
if
sys
.
platform
in
[
'
win32
'
'
cygwin
'
]
:
            
if
rc
!
=
3
and
rc
!
=
0
:
                
return
False
        
else
:
            
if
rc
!
=
3
:
                
return
False
        
return
test
.
expect_error
in
err
    
for
line
in
out
.
split
(
'
\
n
'
)
:
        
if
line
.
startswith
(
'
Trace
stats
check
failed
'
)
:
            
return
False
    
for
line
in
err
.
split
(
'
\
n
'
)
:
        
if
'
Assertion
failed
:
'
in
line
:
            
return
False
    
if
test
.
expect_crash
:
        
if
sys
.
platform
=
=
'
win32
'
and
rc
=
=
3
-
2
*
*
31
:
            
return
True
        
if
sys
.
platform
!
=
'
win32
'
and
rc
=
=
-
11
:
            
return
True
        
if
rc
=
=
1
and
(
"
Hit
MOZ_CRASH
"
in
err
or
"
Assertion
failure
:
"
in
err
)
:
            
return
True
        
if
rc
=
=
139
:
            
return
True
    
if
rc
!
=
test
.
expect_status
:
        
if
sys
.
platform
in
[
'
win32
'
'
cygwin
'
]
and
rc
=
=
0
:
            
return
True
        
if
test
.
allow_oom
and
'
out
of
memory
'
in
err
\
           
and
'
Assertion
failure
'
not
in
err
and
'
MOZ_CRASH
'
not
in
err
:
            
return
True
        
if
test
.
allow_unhandlable_oom
\
           
and
'
Assertion
failure
:
[
unhandlable
oom
]
'
in
err
:
            
return
True
        
if
test
.
allow_overrecursed
and
'
too
much
recursion
'
in
err
\
           
and
'
Assertion
failure
'
not
in
err
:
            
return
True
        
if
test
.
expect_status
!
=
0
and
options
.
unusable_error_status
:
            
return
True
        
return
False
    
return
True
def
print_automation_format
(
ok
res
slog
)
:
    
result
=
"
TEST
-
PASS
"
if
ok
else
"
TEST
-
UNEXPECTED
-
FAIL
"
    
message
=
"
Success
"
if
ok
else
res
.
describe_failure
(
)
    
jitflags
=
"
"
.
join
(
res
.
test
.
jitflags
)
    
print
(
"
{
}
|
{
}
|
{
}
(
code
{
}
args
\
"
{
}
\
"
)
[
{
:
.
1f
}
s
]
"
.
format
(
        
result
res
.
test
.
relpath_top
message
res
.
rc
jitflags
res
.
dt
)
)
    
details
=
{
        
'
message
'
:
message
        
'
extra
'
:
{
            
'
jitflags
'
:
jitflags
        
}
    
}
    
if
res
.
extra
:
        
details
[
'
extra
'
]
.
update
(
res
.
extra
)
    
slog
.
test
(
res
.
test
.
relpath_tests
'
PASS
'
if
ok
else
'
FAIL
'
res
.
dt
*
*
details
)
    
if
ok
:
        
return
    
print
(
"
INFO
exit
-
status
:
{
}
"
.
format
(
res
.
rc
)
)
    
print
(
"
INFO
timed
-
out
:
{
}
"
.
format
(
res
.
timed_out
)
)
    
for
line
in
res
.
out
.
splitlines
(
)
:
        
print
(
"
INFO
stdout
>
"
+
line
.
strip
(
)
)
    
for
line
in
res
.
err
.
splitlines
(
)
:
        
print
(
"
INFO
stderr
2
>
"
+
line
.
strip
(
)
)
def
print_test_summary
(
num_tests
failures
complete
doing
options
)
:
    
if
failures
:
        
if
options
.
write_failures
:
            
try
:
                
out
=
open
(
options
.
write_failures
'
w
'
)
                
written
=
set
(
)
                
for
res
in
failures
:
                    
if
res
.
test
.
path
not
in
written
:
                        
out
.
write
(
os
.
path
.
relpath
(
res
.
test
.
path
TEST_DIR
)
                                  
+
'
\
n
'
)
                        
if
options
.
write_failure_output
:
                            
out
.
write
(
res
.
out
)
                            
out
.
write
(
res
.
err
)
                            
out
.
write
(
'
Exit
code
:
'
+
str
(
res
.
rc
)
+
"
\
n
"
)
                        
written
.
add
(
res
.
test
.
path
)
                
out
.
close
(
)
            
except
IOError
:
                
sys
.
stderr
.
write
(
"
Exception
thrown
trying
to
write
failure
"
                                 
"
file
'
{
}
'
\
n
"
.
format
(
options
.
write_failures
)
)
                
traceback
.
print_exc
(
)
                
sys
.
stderr
.
write
(
'
-
-
-
\
n
'
)
        
def
show_test
(
res
)
:
            
if
options
.
show_failed
:
                
print
(
'
'
+
escape_cmdline
(
res
.
cmd
)
)
            
else
:
                
print
(
'
'
+
'
'
.
join
(
res
.
test
.
jitflags
+
[
res
.
test
.
relpath_tests
]
)
)
        
print
(
'
FAILURES
:
'
)
        
for
res
in
failures
:
            
if
not
res
.
timed_out
:
                
show_test
(
res
)
        
print
(
'
TIMEOUTS
:
'
)
        
for
res
in
failures
:
            
if
res
.
timed_out
:
                
show_test
(
res
)
    
else
:
        
print
(
'
PASSED
ALL
'
              
+
(
'
'
if
complete
                 
else
'
(
partial
run
-
-
interrupted
by
user
{
}
)
'
.
format
(
doing
)
)
)
    
if
options
.
format
=
=
'
automation
'
:
        
num_failures
=
len
(
failures
)
if
failures
else
0
        
print
(
'
Result
summary
:
'
)
        
print
(
'
Passed
:
{
:
d
}
'
.
format
(
num_tests
-
num_failures
)
)
        
print
(
'
Failed
:
{
:
d
}
'
.
format
(
num_failures
)
)
    
return
not
failures
def
create_progressbar
(
num_tests
options
)
:
    
if
not
options
.
hide_progress
and
not
options
.
show_cmd
\
       
and
ProgressBar
.
conservative_isatty
(
)
:
        
fmt
=
[
            
{
'
value
'
:
'
PASS
'
'
color
'
:
'
green
'
}
            
{
'
value
'
:
'
FAIL
'
'
color
'
:
'
red
'
}
            
{
'
value
'
:
'
TIMEOUT
'
'
color
'
:
'
blue
'
}
            
{
'
value
'
:
'
SKIP
'
'
color
'
:
'
brightgray
'
}
        
]
        
return
ProgressBar
(
num_tests
fmt
)
    
return
NullProgressBar
(
)
def
process_test_results
(
results
num_tests
pb
options
slog
)
:
    
failures
=
[
]
    
timeouts
=
0
    
complete
=
False
    
output_dict
=
{
}
    
doing
=
'
before
starting
'
    
if
num_tests
=
=
0
:
        
pb
.
finish
(
True
)
        
complete
=
True
        
return
print_test_summary
(
num_tests
failures
complete
doing
options
)
    
try
:
        
for
i
res
in
enumerate
(
results
)
:
            
ok
=
check_output
(
res
.
out
res
.
err
res
.
rc
res
.
timed_out
                              
res
.
test
options
)
            
if
ok
:
                
show_output
=
options
.
show_output
and
not
options
.
failed_only
            
else
:
                
show_output
=
options
.
show_output
or
not
options
.
no_show_failed
            
if
show_output
:
                
pb
.
beginline
(
)
                
sys
.
stdout
.
write
(
res
.
out
)
                
sys
.
stdout
.
write
(
res
.
err
)
                
sys
.
stdout
.
write
(
'
Exit
code
:
{
}
\
n
'
.
format
(
res
.
rc
)
)
            
if
res
.
test
.
valgrind
and
not
show_output
:
                
pb
.
beginline
(
)
                
sys
.
stdout
.
write
(
res
.
err
)
            
if
options
.
check_output
:
                
if
res
.
test
.
path
in
output_dict
.
keys
(
)
:
                    
if
output_dict
[
res
.
test
.
path
]
!
=
res
.
out
:
                        
pb
.
message
(
"
FAIL
-
OUTPUT
DIFFERS
{
}
"
.
format
(
res
.
test
.
relpath_tests
)
)
                
else
:
                    
output_dict
[
res
.
test
.
path
]
=
res
.
out
            
doing
=
'
after
{
}
'
.
format
(
res
.
test
.
relpath_tests
)
            
if
not
ok
:
                
failures
.
append
(
res
)
                
if
res
.
timed_out
:
                    
pb
.
message
(
"
TIMEOUT
-
{
}
"
.
format
(
res
.
test
.
relpath_tests
)
)
                    
timeouts
+
=
1
                
else
:
                    
pb
.
message
(
"
FAIL
-
{
}
"
.
format
(
res
.
test
.
relpath_tests
)
)
            
if
options
.
format
=
=
'
automation
'
:
                
print_automation_format
(
ok
res
slog
)
            
n
=
i
+
1
            
pb
.
update
(
n
{
                
'
PASS
'
:
n
-
len
(
failures
)
                
'
FAIL
'
:
len
(
failures
)
                
'
TIMEOUT
'
:
timeouts
                
'
SKIP
'
:
0
            
}
)
        
complete
=
True
    
except
KeyboardInterrupt
:
        
print
(
"
TEST
-
UNEXPECTED
-
FAIL
|
jit_test
.
py
"
+
              
"
:
Test
execution
interrupted
by
user
"
)
    
pb
.
finish
(
True
)
    
return
print_test_summary
(
num_tests
failures
complete
doing
options
)
def
run_tests
(
tests
num_tests
prefix
options
remote
=
False
)
:
    
slog
=
None
    
if
options
.
format
=
=
'
automation
'
:
        
slog
=
TestLogger
(
"
jittests
"
)
        
slog
.
suite_start
(
)
    
if
remote
:
        
ok
=
run_tests_remote
(
tests
num_tests
prefix
options
slog
)
    
else
:
        
ok
=
run_tests_local
(
tests
num_tests
prefix
options
slog
)
    
if
slog
:
        
slog
.
suite_end
(
)
    
return
ok
def
run_tests_local
(
tests
num_tests
prefix
options
slog
)
:
    
AdaptorOptions
=
namedtuple
(
"
AdaptorOptions
"
[
        
"
worker_count
"
"
passthrough
"
"
timeout
"
"
output_fp
"
        
"
hide_progress
"
"
run_skipped
"
"
show_cmd
"
]
)
    
shim_options
=
AdaptorOptions
(
options
.
max_jobs
False
options
.
timeout
                                  
sys
.
stdout
False
True
options
.
show_cmd
)
    
JitTest
.
js_cmd_prefix
=
prefix
    
pb
=
create_progressbar
(
num_tests
options
)
    
gen
=
run_all_tests
(
tests
prefix
pb
shim_options
)
    
ok
=
process_test_results
(
gen
num_tests
pb
options
slog
)
    
return
ok
def
get_remote_results
(
tests
device
prefix
options
)
:
    
try
:
        
for
i
in
xrange
(
0
options
.
repeat
)
:
            
for
test
in
tests
:
                
yield
run_test_remote
(
test
device
prefix
options
)
    
except
Exception
as
e
:
        
sys
.
stderr
.
write
(
"
Error
running
remote
tests
:
{
}
"
.
format
(
e
.
message
)
)
def
push_libs
(
options
device
)
:
    
required_libs
=
[
'
libnss3
.
so
'
'
libmozglue
.
so
'
'
libnspr4
.
so
'
                     
'
libplc4
.
so
'
'
libplds4
.
so
'
]
    
for
file
in
os
.
listdir
(
options
.
local_lib
)
:
        
if
file
in
required_libs
:
            
remote_file
=
posixpath
.
join
(
options
.
remote_test_root
file
)
            
device
.
push
(
os
.
path
.
join
(
options
.
local_lib
file
)
remote_file
)
            
device
.
chmod
(
remote_file
root
=
True
)
def
push_progs
(
options
device
progs
)
:
    
for
local_file
in
progs
:
        
remote_file
=
posixpath
.
join
(
options
.
remote_test_root
                                     
os
.
path
.
basename
(
local_file
)
)
        
device
.
push
(
local_file
remote_file
)
        
device
.
chmod
(
remote_file
root
=
True
)
def
init_remote_dir
(
device
path
root
=
True
)
:
    
device
.
rm
(
path
recursive
=
True
force
=
True
root
=
root
)
    
device
.
mkdir
(
path
parents
=
True
root
=
root
)
    
device
.
chmod
(
path
recursive
=
True
root
=
root
)
def
run_tests_remote
(
tests
num_tests
prefix
options
slog
)
:
    
from
mozdevice
import
ADBDevice
ADBError
ADBTimeoutError
    
try
:
        
device
=
ADBDevice
(
device
=
options
.
device_serial
                           
test_root
=
options
.
remote_test_root
)
        
init_remote_dir
(
device
options
.
remote_test_root
)
        
jit_tests_dir
=
posixpath
.
join
(
options
.
remote_test_root
'
jit
-
tests
'
)
        
options
.
remote_test_root
=
posixpath
.
join
(
jit_tests_dir
'
jit
-
tests
'
)
        
init_remote_dir
(
device
jit_tests_dir
)
        
push_libs
(
options
device
)
        
push_progs
(
options
device
[
prefix
[
0
]
]
)
        
device
.
chmod
(
options
.
remote_test_root
recursive
=
True
root
=
True
)
        
jtd_tests
=
posixpath
.
join
(
jit_tests_dir
'
tests
'
)
        
init_remote_dir
(
device
jtd_tests
)
        
device
.
push
(
JS_TESTS_DIR
jtd_tests
timeout
=
600
)
        
device
.
chmod
(
jtd_tests
recursive
=
True
root
=
True
)
        
device
.
push
(
os
.
path
.
dirname
(
TEST_DIR
)
options
.
remote_test_root
                    
timeout
=
600
)
        
device
.
chmod
(
options
.
remote_test_root
recursive
=
True
root
=
True
)
        
prefix
[
0
]
=
os
.
path
.
join
(
options
.
remote_test_root
'
js
'
)
    
except
(
ADBError
ADBTimeoutError
)
:
        
print
(
"
TEST
-
UNEXPECTED
-
FAIL
|
jit_test
.
py
"
+
              
"
:
Device
initialization
failed
"
)
        
raise
    
pb
=
create_progressbar
(
num_tests
options
)
    
try
:
        
gen
=
get_remote_results
(
tests
device
prefix
options
)
        
ok
=
process_test_results
(
gen
num_tests
pb
options
slog
)
    
except
(
ADBError
ADBTimeoutError
)
:
        
print
(
"
TEST
-
UNEXPECTED
-
FAIL
|
jit_test
.
py
"
+
              
"
:
Device
error
during
test
"
)
        
raise
    
return
ok
def
platform_might_be_android
(
)
:
    
try
:
        
import
android
        
return
True
    
except
ImportError
:
        
return
False
def
stdio_might_be_broken
(
)
:
    
return
platform_might_be_android
(
)
if
__name__
=
=
'
__main__
'
:
    
print
(
'
Use
.
.
/
jit
-
test
/
jit_test
.
py
to
run
these
tests
.
'
)
