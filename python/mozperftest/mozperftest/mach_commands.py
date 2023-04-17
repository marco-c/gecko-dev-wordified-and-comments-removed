import
os
import
sys
from
functools
import
partial
import
json
from
mach
.
decorators
import
Command
CommandArgument
from
mozbuild
.
base
import
MachCommandConditions
as
conditions
_TRY_PLATFORMS
=
{
    
"
g5
-
browsertime
"
:
"
perftest
-
android
-
hw
-
g5
-
browsertime
"
    
"
p2
-
browsertime
"
:
"
perftest
-
android
-
hw
-
p2
-
browsertime
"
    
"
linux
-
xpcshell
"
:
"
perftest
-
linux
-
try
-
xpcshell
"
    
"
mac
-
xpcshell
"
:
"
perftest
-
macosx
-
try
-
xpcshell
"
    
"
linux
-
browsertime
"
:
"
perftest
-
linux
-
try
-
browsertime
"
    
"
mac
-
browsertime
"
:
"
perftest
-
macosx
-
try
-
browsertime
"
    
"
win
-
browsertimee
"
:
"
perftest
-
windows
-
try
-
browsertime
"
}
HERE
=
os
.
path
.
dirname
(
__file__
)
def
get_perftest_parser
(
)
:
    
from
mozperftest
import
PerftestArgumentParser
    
return
PerftestArgumentParser
def
get_parser
(
)
:
    
return
run_perftest
.
_mach_command
.
_parser
Command
(
    
"
perftest
"
    
category
=
"
testing
"
    
conditions
=
[
partial
(
conditions
.
is_buildapp_in
apps
=
[
"
firefox
"
"
android
"
]
)
]
    
description
=
"
Run
any
flavor
of
perftest
"
    
parser
=
get_perftest_parser
)
def
run_perftest
(
command_context
*
*
kwargs
)
:
    
original_parser
=
get_parser
(
)
    
from
pathlib
import
Path
    
from
mozperftest
.
utils
import
ON_TRY
    
from
mozperftest
.
script
import
ScriptInfo
ScriptType
ParseError
    
if
not
ON_TRY
and
kwargs
.
get
(
"
tests
"
[
]
)
=
=
[
]
:
        
from
moztest
.
resolve
import
TestResolver
        
from
mozperftest
.
fzf
.
fzf
import
select
        
resolver
=
command_context
.
_spawn
(
TestResolver
)
        
test_objects
=
list
(
resolver
.
resolve_tests
(
paths
=
None
flavor
=
"
perftest
"
)
)
        
selected
=
select
(
test_objects
)
        
def
full_path
(
selection
)
:
            
__
script_name
__
location
=
selection
.
split
(
"
"
)
            
return
str
(
                
Path
(
                    
command_context
.
topsrcdir
.
rstrip
(
os
.
sep
)
                    
location
.
strip
(
os
.
sep
)
                    
script_name
                
)
            
)
        
kwargs
[
"
tests
"
]
=
[
full_path
(
s
)
for
s
in
selected
]
        
if
kwargs
[
"
tests
"
]
=
=
[
]
:
            
print
(
"
\
nNo
selection
.
Bye
!
"
)
            
return
    
if
len
(
kwargs
[
"
tests
"
]
)
>
1
:
        
print
(
"
\
nSorry
no
support
yet
for
multiple
local
perftest
"
)
        
return
    
sel
=
"
\
n
"
.
join
(
kwargs
[
"
tests
"
]
)
    
print
(
"
\
nGood
job
!
Best
selection
.
\
n
%
s
"
%
sel
)
    
try
:
        
script_info
=
ScriptInfo
(
kwargs
[
"
tests
"
]
[
0
]
)
    
except
ParseError
as
e
:
        
if
e
.
exception
is
IsADirectoryError
:
            
script_info
=
None
        
else
:
            
raise
    
else
:
        
if
script_info
.
script_type
=
=
ScriptType
.
xpcshell
:
            
kwargs
[
"
flavor
"
]
=
script_info
.
script_type
.
name
        
else
:
            
if
"
flavor
"
not
in
kwargs
:
                
kwargs
[
"
flavor
"
]
=
"
desktop
-
browser
"
    
push_to_try
=
kwargs
.
pop
(
"
push_to_try
"
False
)
    
if
push_to_try
:
        
sys
.
path
.
append
(
str
(
Path
(
command_context
.
topsrcdir
"
tools
"
"
tryselect
"
)
)
)
        
from
tryselect
.
push
import
push_to_try
        
perftest_parameters
=
{
}
        
args
=
script_info
.
update_args
(
*
*
original_parser
.
get_user_args
(
kwargs
)
)
        
platform
=
args
.
pop
(
"
try_platform
"
"
linux
"
)
        
if
isinstance
(
platform
str
)
:
            
platform
=
[
platform
]
        
platform
=
[
"
%
s
-
%
s
"
%
(
plat
script_info
.
script_type
.
name
)
for
plat
in
platform
]
        
for
plat
in
platform
:
            
if
plat
not
in
_TRY_PLATFORMS
:
                
raise
NotImplementedError
(
                    
"
%
r
doesn
'
t
exist
or
is
not
yet
supported
"
%
plat
                
)
        
def
relative
(
path
)
:
            
if
path
.
startswith
(
command_context
.
topsrcdir
)
:
                
return
path
[
len
(
command_context
.
topsrcdir
)
:
]
.
lstrip
(
os
.
sep
)
            
return
path
        
for
name
value
in
args
.
items
(
)
:
            
if
original_parser
.
get_default
(
name
)
=
=
value
:
                
continue
            
if
name
=
=
"
tests
"
:
                
value
=
[
relative
(
path
)
for
path
in
value
]
            
perftest_parameters
[
name
]
=
value
        
parameters
=
{
            
"
try_task_config
"
:
{
                
"
tasks
"
:
[
_TRY_PLATFORMS
[
plat
]
for
plat
in
platform
]
                
"
perftest
-
options
"
:
perftest_parameters
            
}
            
"
try_mode
"
:
"
try_task_config
"
        
}
        
task_config
=
{
"
parameters
"
:
parameters
"
version
"
:
2
}
        
if
args
.
get
(
"
verbose
"
)
:
            
print
(
"
Pushing
run
to
try
.
.
.
"
)
            
print
(
json
.
dumps
(
task_config
indent
=
4
sort_keys
=
True
)
)
        
push_to_try
(
"
perftest
"
"
perftest
"
try_task_config
=
task_config
)
        
return
    
from
mozperftest
.
runner
import
run_tests
    
run_tests
(
command_context
kwargs
original_parser
.
get_user_args
(
kwargs
)
)
    
print
(
"
\
nFirefox
.
Fast
For
Good
.
\
n
"
)
Command
(
    
"
perftest
-
test
"
    
category
=
"
testing
"
    
description
=
"
Run
perftest
tests
"
    
virtualenv_name
=
"
python
-
test
"
)
CommandArgument
(
    
"
tests
"
default
=
None
nargs
=
"
*
"
help
=
"
Tests
to
run
.
By
default
will
run
all
"
)
CommandArgument
(
    
"
-
s
"
    
"
-
-
skip
-
linters
"
    
action
=
"
store_true
"
    
default
=
False
    
help
=
"
Skip
flake8
and
black
"
)
CommandArgument
(
    
"
-
v
"
"
-
-
verbose
"
action
=
"
store_true
"
default
=
False
help
=
"
Verbose
mode
"
)
def
run_tests
(
command_context
*
*
kwargs
)
:
    
command_context
.
activate_virtualenv
(
)
    
from
pathlib
import
Path
    
from
mozperftest
.
utils
import
temporary_env
    
with
temporary_env
(
        
COVERAGE_RCFILE
=
str
(
Path
(
HERE
"
.
coveragerc
"
)
)
RUNNING_TESTS
=
"
YES
"
    
)
:
        
_run_tests
(
command_context
*
*
kwargs
)
def
_run_tests
(
command_context
*
*
kwargs
)
:
    
from
pathlib
import
Path
    
from
mozperftest
.
runner
import
_setup_path
    
from
mozperftest
.
utils
import
(
        
install_package
        
ON_TRY
        
checkout_script
        
checkout_python_script
    
)
    
venv
=
command_context
.
virtualenv_manager
    
skip_linters
=
kwargs
.
get
(
"
skip_linters
"
False
)
    
verbose
=
kwargs
.
get
(
"
verbose
"
False
)
    
_setup_path
(
)
    
try
:
        
import
coverage
    
except
ImportError
:
        
pydeps
=
Path
(
command_context
.
topsrcdir
"
third_party
"
"
python
"
)
        
vendors
=
[
"
coverage
"
]
        
if
not
ON_TRY
:
            
vendors
.
append
(
"
attrs
"
)
        
for
dep
in
vendors
:
            
install_package
(
command_context
.
virtualenv_manager
str
(
Path
(
pydeps
dep
)
)
)
    
if
not
ON_TRY
and
not
skip_linters
:
        
cmd
=
"
.
/
mach
lint
"
        
if
verbose
:
            
cmd
+
=
"
-
v
"
        
cmd
+
=
"
"
+
str
(
HERE
)
        
if
not
checkout_script
(
cmd
label
=
"
linters
"
display
=
verbose
verbose
=
verbose
)
:
            
raise
AssertionError
(
"
Please
fix
your
code
.
"
)
    
tests_dir
=
Path
(
HERE
"
tests
"
)
.
resolve
(
)
    
tests
=
kwargs
.
get
(
"
tests
"
[
]
)
    
if
tests
=
=
[
]
:
        
tests
=
str
(
tests_dir
)
        
run_coverage_check
=
not
skip_linters
    
else
:
        
run_coverage_check
=
False
        
def
_get_test
(
test
)
:
            
if
Path
(
test
)
.
exists
(
)
:
                
return
str
(
test
)
            
return
str
(
tests_dir
/
test
)
        
tests
=
"
"
.
join
(
[
_get_test
(
test
)
for
test
in
tests
]
)
    
if
sys
.
platform
=
=
"
darwin
"
and
ON_TRY
:
        
run_coverage_check
=
False
    
import
pytest
    
options
=
"
-
xs
"
    
if
kwargs
.
get
(
"
verbose
"
)
:
        
options
+
=
"
v
"
    
if
run_coverage_check
:
        
assert
checkout_python_script
(
            
venv
"
coverage
"
[
"
erase
"
]
label
=
"
remove
old
coverage
data
"
        
)
    
args
=
[
"
run
"
pytest
.
__file__
options
"
-
-
duration
"
"
10
"
tests
]
    
assert
checkout_python_script
(
        
venv
"
coverage
"
args
label
=
"
running
tests
"
verbose
=
verbose
    
)
    
if
run_coverage_check
and
not
checkout_python_script
(
        
venv
"
coverage
"
[
"
report
"
]
display
=
True
    
)
:
        
raise
ValueError
(
"
Coverage
is
too
low
!
"
)
