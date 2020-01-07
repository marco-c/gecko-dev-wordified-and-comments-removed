from
__future__
import
absolute_import
print_function
unicode_literals
import
argparse
import
logging
import
os
import
sys
import
tempfile
from
concurrent
.
futures
import
(
    
ThreadPoolExecutor
    
as_completed
    
thread
)
import
mozinfo
from
manifestparser
import
TestManifest
from
manifestparser
import
filters
as
mpf
from
mozbuild
.
base
import
(
    
MachCommandBase
)
from
mach
.
decorators
import
(
    
CommandArgument
    
CommandProvider
    
Command
)
here
=
os
.
path
.
abspath
(
os
.
path
.
dirname
(
__file__
)
)
CommandProvider
class
MachCommands
(
MachCommandBase
)
:
    
Command
(
'
python
'
category
=
'
devenv
'
             
description
=
'
Run
Python
.
'
)
    
CommandArgument
(
'
-
-
no
-
virtualenv
'
action
=
'
store_true
'
                     
help
=
'
Do
not
set
up
a
virtualenv
'
)
    
CommandArgument
(
'
args
'
nargs
=
argparse
.
REMAINDER
)
    
def
python
(
self
no_virtualenv
args
)
:
        
self
.
log_manager
.
terminal_handler
.
setLevel
(
logging
.
CRITICAL
)
        
append_env
=
{
            
b
'
PYTHONDONTWRITEBYTECODE
'
:
str
(
'
1
'
)
        
}
        
if
no_virtualenv
:
            
python_path
=
sys
.
executable
            
append_env
[
b
'
PYTHONPATH
'
]
=
os
.
pathsep
.
join
(
sys
.
path
)
        
else
:
            
self
.
_activate_virtualenv
(
)
            
python_path
=
self
.
virtualenv_manager
.
python_path
        
return
self
.
run_process
(
[
python_path
]
+
args
                                
pass_thru
=
True
                                
ensure_exit_code
=
False
                                
append_env
=
append_env
)
    
Command
(
'
python
-
test
'
category
=
'
testing
'
             
description
=
'
Run
Python
unit
tests
with
an
appropriate
test
runner
.
'
)
    
CommandArgument
(
'
-
v
'
'
-
-
verbose
'
                     
default
=
False
                     
action
=
'
store_true
'
                     
help
=
'
Verbose
output
.
'
)
    
CommandArgument
(
'
-
-
python
'
                     
default
=
'
2
.
7
'
                     
help
=
'
Version
of
Python
for
Pipenv
to
use
.
When
given
a
'
                          
'
Python
version
Pipenv
will
automatically
scan
your
'
                          
'
system
for
a
Python
that
matches
that
given
version
.
'
)
    
CommandArgument
(
'
-
j
'
'
-
-
jobs
'
                     
default
=
1
                     
type
=
int
                     
help
=
'
Number
of
concurrent
jobs
to
run
.
Default
is
1
.
'
)
    
CommandArgument
(
'
-
-
subsuite
'
                     
default
=
None
                     
help
=
(
'
Python
subsuite
to
run
.
If
not
specified
all
subsuites
are
run
.
'
                           
'
Use
the
string
default
to
only
run
tests
without
a
subsuite
.
'
)
)
    
CommandArgument
(
'
tests
'
nargs
=
'
*
'
                     
metavar
=
'
TEST
'
                     
help
=
(
'
Tests
to
run
.
Each
test
can
be
a
single
file
or
a
directory
.
'
                           
'
Default
test
resolution
relies
on
PYTHON_UNITTEST_MANIFESTS
.
'
)
)
    
def
python_test
(
self
*
args
*
*
kwargs
)
:
        
try
:
            
tempdir
=
os
.
environ
[
b
'
PYTHON_TEST_TMP
'
]
=
str
(
tempfile
.
mkdtemp
(
suffix
=
'
-
python
-
test
'
)
)
            
return
self
.
run_python_tests
(
*
args
*
*
kwargs
)
        
finally
:
            
import
mozfile
            
mozfile
.
remove
(
tempdir
)
    
def
run_python_tests
(
self
                         
tests
=
None
                         
test_objects
=
None
                         
subsuite
=
None
                         
verbose
=
False
                         
jobs
=
1
                         
python
=
None
                         
*
*
kwargs
)
:
        
self
.
activate_pipenv
(
pipfile
=
None
populate
=
True
python
=
python
)
        
if
test_objects
is
None
:
            
from
moztest
.
resolve
import
TestResolver
            
resolver
=
self
.
_spawn
(
TestResolver
)
            
test_objects
=
resolver
.
resolve_tests
(
paths
=
tests
flavor
=
'
python
'
)
        
else
:
            
subsuite
=
None
        
mp
=
TestManifest
(
)
        
mp
.
tests
.
extend
(
test_objects
)
        
filters
=
[
]
        
if
subsuite
=
=
'
default
'
:
            
filters
.
append
(
mpf
.
subsuite
(
None
)
)
        
elif
subsuite
:
            
filters
.
append
(
mpf
.
subsuite
(
subsuite
)
)
        
tests
=
mp
.
active_tests
(
            
filters
=
filters
            
disabled
=
False
            
python
=
self
.
virtualenv_manager
.
version_info
[
0
]
            
*
*
mozinfo
.
info
)
        
if
not
tests
:
            
submsg
=
"
for
subsuite
'
{
}
'
"
.
format
(
subsuite
)
if
subsuite
else
"
"
            
message
=
"
TEST
-
UNEXPECTED
-
FAIL
|
No
tests
collected
"
+
\
                      
"
{
}
(
Not
in
PYTHON_UNITTEST_MANIFESTS
?
)
"
.
format
(
submsg
)
            
self
.
log
(
logging
.
WARN
'
python
-
test
'
{
}
message
)
            
return
1
        
parallel
=
[
]
        
sequential
=
[
]
        
for
test
in
tests
:
            
if
test
.
get
(
'
sequential
'
)
:
                
sequential
.
append
(
test
)
            
else
:
                
parallel
.
append
(
test
)
        
self
.
jobs
=
jobs
        
self
.
terminate
=
False
        
self
.
verbose
=
verbose
        
return_code
=
0
        
def
on_test_finished
(
result
)
:
            
output
ret
test_path
=
result
            
for
line
in
output
:
                
self
.
log
(
logging
.
INFO
'
python
-
test
'
{
'
line
'
:
line
.
rstrip
(
)
}
'
{
line
}
'
)
            
if
ret
and
not
return_code
:
                
self
.
log
(
logging
.
ERROR
'
python
-
test
'
{
'
test_path
'
:
test_path
'
ret
'
:
ret
}
                         
'
Setting
retcode
to
{
ret
}
from
{
test_path
}
'
)
            
return
return_code
or
ret
        
with
ThreadPoolExecutor
(
max_workers
=
self
.
jobs
)
as
executor
:
            
futures
=
[
executor
.
submit
(
self
.
_run_python_test
test
[
'
path
'
]
)
                       
for
test
in
parallel
]
            
try
:
                
for
future
in
as_completed
(
futures
)
:
                    
return_code
=
on_test_finished
(
future
.
result
(
)
)
            
except
KeyboardInterrupt
:
                
executor
.
_threads
.
clear
(
)
                
thread
.
_threads_queues
.
clear
(
)
                
raise
        
for
test
in
sequential
:
            
return_code
=
on_test_finished
(
self
.
_run_python_test
(
test
[
'
path
'
]
)
)
        
self
.
log
(
logging
.
INFO
'
python
-
test
'
{
'
return_code
'
:
return_code
}
                 
'
Return
code
from
mach
python
-
test
:
{
return_code
}
'
)
        
return
return_code
    
def
_run_python_test
(
self
test_path
)
:
        
from
mozprocess
import
ProcessHandler
        
output
=
[
]
        
def
_log
(
line
)
:
            
if
self
.
jobs
>
1
:
                
output
.
append
(
line
)
            
else
:
                
self
.
log
(
logging
.
INFO
'
python
-
test
'
{
'
line
'
:
line
.
rstrip
(
)
}
'
{
line
}
'
)
        
file_displayed_test
=
[
]
        
def
_line_handler
(
line
)
:
            
if
not
file_displayed_test
:
                
output
=
(
'
Ran
'
in
line
or
'
collected
'
in
line
or
                          
line
.
startswith
(
'
TEST
-
'
)
)
                
if
output
:
                    
file_displayed_test
.
append
(
True
)
            
if
'
FAILED
'
in
line
.
rsplit
(
'
'
1
)
[
-
1
]
:
                
line
=
line
.
replace
(
'
FAILED
'
'
TEST
-
UNEXPECTED
-
FAIL
'
)
            
_log
(
line
)
        
_log
(
test_path
)
        
cmd
=
[
self
.
virtualenv_manager
.
python_path
test_path
]
        
env
=
os
.
environ
.
copy
(
)
        
env
[
b
'
PYTHONDONTWRITEBYTECODE
'
]
=
b
'
1
'
        
proc
=
ProcessHandler
(
cmd
env
=
env
processOutputLine
=
_line_handler
storeOutput
=
False
)
        
proc
.
run
(
)
        
return_code
=
proc
.
wait
(
)
        
if
not
file_displayed_test
:
            
_log
(
'
TEST
-
UNEXPECTED
-
FAIL
|
No
test
output
(
missing
mozunit
.
main
(
)
'
                 
'
call
?
)
:
{
}
'
.
format
(
test_path
)
)
        
if
self
.
verbose
:
            
if
return_code
!
=
0
:
                
_log
(
'
Test
failed
:
{
}
'
.
format
(
test_path
)
)
            
else
:
                
_log
(
'
Test
passed
:
{
}
'
.
format
(
test_path
)
)
        
return
output
return_code
test_path
