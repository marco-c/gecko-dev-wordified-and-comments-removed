import
os
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
enum
import
Enum
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
or
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
    
from
.
tasks_unix
import
run_all_tests
else
:
    
from
.
tasks_win
import
run_all_tests
from
.
progressbar
import
NullProgressBar
ProgressBar
from
.
results
import
escape_cmdline
from
.
structuredlog
import
TestLogger
from
.
tempfile
import
TemporaryDirectory
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
"
jit
-
test
"
"
tests
"
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
"
jit
-
test
"
"
lib
"
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
"
jit
-
test
"
"
modules
"
)
+
os
.
path
.
sep
SHELL_XDR
=
"
shell
.
xdr
"
class
OutputStatus
(
Enum
)
:
    
OK
=
1
    
SKIPPED
=
2
    
FAILED
=
3
    
def
__bool__
(
self
)
:
        
return
self
!
=
OutputStatus
.
FAILED
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
    
"
\
\
"
:
"
\
\
\
\
"
    
"
\
b
"
:
"
\
\
b
"
    
"
\
f
"
:
"
\
\
f
"
    
"
\
n
"
:
"
\
\
n
"
    
"
\
r
"
:
"
\
\
r
"
    
"
\
t
"
:
"
\
\
t
"
    
"
\
v
"
:
"
\
\
v
"
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
"
\
\
"
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
f
"
(
{
value
}
)
"
    
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
"
PATH
"
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
"
valgrind
"
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
            
"
valgrind
"
            
"
-
q
"
            
"
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
"
            
"
-
-
error
-
exitcode
=
1
"
            
"
-
-
gen
-
suppressions
=
all
"
            
"
-
-
show
-
possibly
-
lost
=
no
"
            
"
-
-
leak
-
check
=
full
"
        
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
"
Darwin
"
:
            
VALGRIND_CMD
.
append
(
"
-
-
dsymutil
=
yes
"
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
heavy
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
other_lib_includes
=
[
]
        
self
.
other_script_includes
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
"
"
        
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
test_reflect_stringify
=
None
        
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
skip_if_cond
=
"
"
        
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
heavy
=
self
.
heavy
        
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
other_lib_includes
=
self
.
other_lib_includes
[
:
]
        
t
.
other_script_includes
=
self
.
other_script_includes
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
selfhosted_xdr_path
=
self
.
selfhosted_xdr_path
        
t
.
selfhosted_xdr_mode
=
self
.
selfhosted_xdr_mode
        
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
b
"
|
jit
-
test
|
"
    
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
"
"
        
line
=
open
(
file_name
"
rb
"
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
"
;
"
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
decode
(
errors
=
"
strict
"
)
.
strip
(
"
\
n
"
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
"
"
        
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
"
"
or
dir_meta
!
=
"
"
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
"
;
"
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
"
:
"
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
"
error
"
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
"
exitstatus
"
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
f
"
{
value
}
"
)
                    
elif
name
=
=
"
thread
-
count
"
:
                        
try
:
                            
test
.
jitflags
.
append
(
f
"
-
-
thread
-
count
=
{
int
(
value
0
)
}
"
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
f
"
{
value
}
"
)
                    
elif
name
=
=
"
include
"
:
                        
test
.
other_lib_includes
.
append
(
value
)
                    
elif
name
=
=
"
local
-
include
"
:
                        
test
.
other_script_includes
.
append
(
value
)
                    
elif
name
=
=
"
skip
-
if
"
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
"
skip
-
variant
-
if
"
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
"
"
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
                            
f
"
{
path
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
"
                            
f
"
{
part
}
"
                        
)
                
else
:
                    
if
name
=
=
"
slow
"
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
"
heavy
"
:
                        
test
.
heavy
=
True
                    
elif
name
=
=
"
allow
-
oom
"
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
"
allow
-
unhandlable
-
oom
"
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
"
allow
-
overrecursed
"
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
"
valgrind
"
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
"
tz
-
pacific
"
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
"
test
-
also
=
"
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
"
\
s
+
"
name
[
len
(
"
test
-
also
=
"
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
"
test
-
join
=
"
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
"
\
s
+
"
name
[
len
(
"
test
-
join
=
"
)
:
]
)
                        
)
                    
elif
name
=
=
"
module
"
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
"
crash
"
:
                        
assert
(
                            
"
self
-
test
"
in
path
                        
)
f
"
{
path
}
:
has
an
unexpected
crash
annotation
.
"
                        
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
"
-
-
"
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
                    
elif
name
.
startswith
(
"
-
P
"
)
:
                        
prefAndValue
=
name
.
split
(
)
                        
assert
(
                            
len
(
prefAndValue
)
=
=
2
                        
)
f
"
{
name
}
:
failed
to
parse
preference
"
                        
test
.
jitflags
.
append
(
"
-
-
setpref
=
"
+
prefAndValue
[
1
]
)
                    
else
:
                        
print
(
                            
f
"
{
path
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
"
                            
f
"
{
part
}
"
                        
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
"
"
            
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
tempdir
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
"
/
"
)
:
            
scriptdir_var
+
=
"
/
"
        
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
SHELL_XDR
)
        
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
            
f
"
const
platform
=
{
js_quote
(
quotechar
sys
.
platform
)
}
"
            
f
"
const
libdir
=
{
js_quote
(
quotechar
libdir
)
}
"
            
f
"
const
scriptdir
=
{
js_quote
(
quotechar
scriptdir_var
)
}
"
        
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
dict
.
fromkeys
(
self
.
jitflags
)
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
        
for
expr
in
exprs
:
            
cmd
+
=
[
"
-
e
"
expr
]
        
for
inc
in
self
.
other_lib_includes
:
            
cmd
+
=
[
"
-
f
"
libdir
+
inc
]
        
for
inc
in
self
.
other_script_includes
:
            
cmd
+
=
[
"
-
f
"
scriptdir_var
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
                
"
-
e
"
                
f
"
if
(
{
self
.
skip_if_cond
}
)
quit
(
{
self
.
SKIPPED_EXIT_STATUS
}
)
"
            
]
        
cmd
+
=
[
"
-
-
module
-
load
-
path
"
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
"
-
-
module
"
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
"
-
f
"
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
-
"
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
"
-
-
suppress
-
minidump
"
]
        
return
cmd
    
def
get_command
(
self
prefix
tempdir
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
tempdir
)
def
find_tests
(
substring
=
None
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
"
.
"
:
            
continue
        
for
filename
in
filenames
:
            
if
not
filename
.
endswith
(
"
.
js
"
)
:
                
continue
            
if
filename
in
(
"
shell
.
js
"
"
browser
.
js
"
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
OutputStatus
.
SKIPPED
    
if
timed_out
:
        
relpath
=
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
"
/
"
)
        
if
relpath
in
options
.
ignore_timeouts
:
            
return
OutputStatus
.
OK
        
return
OutputStatus
.
FAILED
    
if
test
.
expect_error
:
        
if
rc
!
=
3
:
            
return
OutputStatus
.
FAILED
        
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
"
\
n
"
)
:
        
if
line
.
startswith
(
"
Trace
stats
check
failed
"
)
:
            
return
OutputStatus
.
FAILED
    
for
line
in
err
.
split
(
"
\
n
"
)
:
        
if
"
Assertion
failed
:
"
in
line
:
            
return
OutputStatus
.
FAILED
    
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
"
win32
"
and
rc
in
(
3
-
2
*
*
31
3
+
2
*
*
31
)
:
            
return
OutputStatus
.
OK
        
if
sys
.
platform
!
=
"
win32
"
and
rc
=
=
-
11
:
            
return
OutputStatus
.
OK
        
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
OutputStatus
.
OK
        
if
rc
=
=
139
or
rc
=
=
138
:
            
return
OutputStatus
.
OK
        
return
OutputStatus
.
FAILED
    
if
rc
!
=
test
.
expect_status
:
        
if
(
            
test
.
allow_oom
            
and
"
out
of
memory
"
in
err
            
and
"
Assertion
failure
"
not
in
err
            
and
"
MOZ_CRASH
"
not
in
err
        
)
:
            
return
OutputStatus
.
OK
        
if
test
.
allow_unhandlable_oom
and
"
MOZ_CRASH
(
[
unhandlable
oom
]
"
in
err
:
            
return
OutputStatus
.
OK
        
if
(
            
test
.
allow_overrecursed
            
and
"
too
much
recursion
"
in
err
            
and
"
Assertion
failure
"
not
in
err
        
)
:
            
return
OutputStatus
.
OK
        
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
OutputStatus
.
OK
        
return
OutputStatus
.
FAILED
    
return
OutputStatus
.
OK
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
        
f
'
{
result
}
|
{
res
.
test
.
relpath_top
}
|
{
message
}
(
code
{
res
.
rc
}
args
"
{
jitflags
}
"
)
[
{
res
.
dt
:
.
1f
}
s
]
'
    
)
    
details
=
{
        
"
message
"
:
message
        
"
extra
"
:
{
            
"
jitflags
"
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
"
extra
"
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
"
PASS
"
if
ok
else
"
FAIL
"
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
f
"
INFO
exit
-
status
:
{
res
.
rc
}
"
)
    
print
(
f
"
INFO
timed
-
out
:
{
res
.
timed_out
}
"
)
    
warnings
=
[
]
    
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
        
if
line
.
startswith
(
"
WARNING
"
)
and
"
unused
DT
entry
"
in
line
:
            
warnings
.
append
(
line
)
            
continue
        
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
        
if
line
.
startswith
(
"
WARNING
"
)
and
"
unused
DT
entry
"
in
line
:
            
warnings
.
append
(
line
)
            
continue
        
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
    
for
line
in
warnings
:
        
print
(
"
INFO
(
warn
-
stderr
)
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
slow_tests
doing
options
)
:
    
def
test_details
(
res
)
:
        
if
options
.
show_failed
:
            
return
escape_cmdline
(
res
.
cmd
)
        
return
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
+
[
res
.
test
.
relpath_tests
]
)
    
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
"
w
"
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
"
\
n
"
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
"
Exit
code
:
"
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
OSError
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
                    
f
"
file
'
{
options
.
write_failures
}
'
\
n
"
                
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
"
-
-
-
\
n
"
)
        
print
(
"
FAILURES
:
"
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
                
print
(
"
"
+
test_details
(
res
)
)
        
print
(
"
TIMEOUTS
:
"
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
                
print
(
"
"
+
test_details
(
res
)
)
    
else
:
        
print
(
            
"
PASSED
ALL
"
            
+
(
"
"
if
complete
else
f
"
(
partial
run
-
-
interrupted
by
user
{
doing
}
)
"
)
        
)
    
if
options
.
format
=
=
"
automation
"
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
"
Result
summary
:
"
)
        
print
(
f
"
Passed
:
{
num_tests
-
num_failures
:
d
}
"
)
        
print
(
f
"
Failed
:
{
num_failures
:
d
}
"
)
    
if
num_tests
!
=
0
and
options
.
show_slow
:
        
threshold
=
options
.
slow_test_threshold
        
fraction_fast
=
1
-
len
(
slow_tests
)
/
num_tests
        
print
(
f
"
{
fraction_fast
*
100
:
5
.
2f
}
%
of
tests
ran
in
under
{
threshold
}
s
"
)
        
print
(
f
"
Slowest
tests
that
took
longer
than
{
threshold
}
s
:
"
)
        
slow_tests
.
sort
(
key
=
lambda
res
:
res
.
dt
reverse
=
True
)
        
any
=
False
        
for
i
in
range
(
min
(
len
(
slow_tests
)
20
)
)
:
            
res
=
slow_tests
[
i
]
            
print
(
f
"
{
res
.
dt
:
6
.
2f
}
{
test_details
(
res
)
}
"
)
            
any
=
True
        
if
not
any
:
            
print
(
"
None
"
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
(
        
not
options
.
hide_progress
        
and
not
options
.
show_cmd
        
and
ProgressBar
.
conservative_isatty
(
)
    
)
:
        
fmt
=
[
            
{
"
value
"
:
"
PASS
"
"
color
"
:
"
green
"
}
            
{
"
value
"
:
"
FAIL
"
"
color
"
:
"
red
"
}
            
{
"
value
"
:
"
TIMEOUT
"
"
color
"
:
"
blue
"
}
            
{
"
value
"
:
"
SKIP
"
"
color
"
:
"
brightgray
"
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
    
skipped
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
"
before
starting
"
    
slow_tests
=
[
]
    
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
slow_tests
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
            
status
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
status
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
f
"
Exit
code
:
{
res
.
rc
}
\
n
"
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
f
"
FAIL
-
OUTPUT
DIFFERS
{
res
.
test
.
relpath_tests
}
"
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
f
"
after
{
res
.
test
.
relpath_tests
}
"
            
if
status
=
=
OutputStatus
.
SKIPPED
:
                
skipped
+
=
1
            
elif
status
=
=
OutputStatus
.
FAILED
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
f
"
TIMEOUT
-
{
res
.
test
.
relpath_tests
}
"
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
f
"
FAIL
-
{
res
.
test
.
relpath_tests
}
"
)
            
if
options
.
format
=
=
"
automation
"
:
                
print_automation_format
(
status
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
                    
"
PASS
"
:
n
-
len
(
failures
)
                    
"
FAIL
"
:
len
(
failures
)
                    
"
TIMEOUT
"
:
timeouts
                    
"
SKIP
"
:
skipped
                
}
            
)
            
if
res
.
dt
>
options
.
slow_test_threshold
:
                
slow_tests
.
append
(
res
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
slow_tests
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
"
automation
"
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
            
"
use_xdr
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
        
options
.
use_xdr
    
)
    
with
TemporaryDirectory
(
)
as
tempdir
:
        
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
tempdir
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
ADBError
ADBTimeoutError
    
from
.
tasks_adb_remote
import
get_remote_results
    
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
prefix
pb
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
if
__name__
=
=
"
__main__
"
:
    
print
(
"
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
"
)
