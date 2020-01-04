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
mozpack
.
path
as
mozpath
import
os
import
platform
import
subprocess
import
sys
import
which
from
distutils
.
version
import
LooseVersion
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
ESLINT_NOT_FOUND_MESSAGE
=
'
'
'
Could
not
find
eslint
!
We
looked
at
the
-
-
binary
option
at
the
ESLINT
environment
variable
and
then
at
your
path
.
Install
eslint
and
needed
plugins
with
mach
eslint
-
-
setup
and
try
again
.
'
'
'
.
strip
(
)
NODE_NOT_FOUND_MESSAGE
=
'
'
'
nodejs
v4
.
2
.
3
is
either
not
installed
or
is
installed
to
a
non
-
standard
path
.
Please
install
nodejs
from
https
:
/
/
nodejs
.
org
and
try
again
.
Valid
installation
paths
:
'
'
'
.
strip
(
)
NPM_NOT_FOUND_MESSAGE
=
'
'
'
Node
Package
Manager
(
npm
)
is
either
not
installed
or
installed
to
a
non
-
standard
path
.
Please
install
npm
from
https
:
/
/
nodejs
.
org
(
it
comes
as
an
option
in
the
node
installation
)
and
try
again
.
Valid
installation
paths
:
'
'
'
.
strip
(
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
        
self
.
_activate_virtualenv
(
)
        
return
self
.
run_process
(
[
self
.
virtualenv_manager
.
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
stop
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
Stop
running
tests
after
the
first
error
or
failure
.
'
)
    
CommandArgument
(
'
-
-
path
-
only
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
(
'
Collect
all
tests
under
given
path
instead
of
default
'
              
'
test
resolution
.
Supports
pytest
-
style
tests
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
PYTHON_UNIT_TESTS
.
'
)
)
    
def
python_test
(
self
                    
tests
=
[
]
                    
test_objects
=
None
                    
subsuite
=
None
                    
verbose
=
False
                    
path_only
=
False
                    
stop
=
False
)
:
        
self
.
_activate_virtualenv
(
)
        
def
find_tests_by_path
(
)
:
            
import
glob
            
files
=
[
]
            
for
t
in
tests
:
                
if
t
.
endswith
(
'
.
py
'
)
and
os
.
path
.
isfile
(
t
)
:
                    
files
.
append
(
t
)
                
elif
os
.
path
.
isdir
(
t
)
:
                    
for
root
_
_
in
os
.
walk
(
t
)
:
                        
files
+
=
glob
.
glob
(
mozpath
.
join
(
root
'
test
*
.
py
'
)
)
                        
files
+
=
glob
.
glob
(
mozpath
.
join
(
root
'
unit
*
.
py
'
)
)
                
else
:
                    
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
'
test
'
:
t
}
                                 
'
TEST
-
UNEXPECTED
-
FAIL
|
Invalid
test
:
{
test
}
'
)
                    
if
stop
:
                        
break
            
return
files
        
return_code
=
0
        
found_tests
=
False
        
if
test_objects
is
None
:
            
if
path_only
:
                
if
tests
:
                    
self
.
virtualenv_manager
.
install_pip_package
(
                       
'
pytest
=
=
2
.
9
.
1
'
                    
)
                    
test_objects
=
[
{
'
path
'
:
p
}
for
p
in
find_tests_by_path
(
)
]
                
else
:
                    
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
                             
'
TEST
-
UNEXPECTED
-
FAIL
|
No
tests
specified
'
)
                    
test_objects
=
[
]
            
else
:
                
from
mozbuild
.
testing
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
                
if
tests
:
                    
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
                    
test_objects
=
resolver
.
resolve_tests
(
flavor
=
'
python
'
)
        
for
test
in
test_objects
:
            
found_tests
=
True
            
f
=
test
[
'
path
'
]
            
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
            
inner_return_code
=
self
.
run_process
(
                
[
self
.
virtualenv_manager
.
python_path
f
]
                
ensure_exit_code
=
False
                
log_name
=
'
python
-
test
'
                
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
                
line_handler
=
_line_handler
)
            
return_code
+
=
inner_return_code
            
if
not
file_displayed_test
:
                
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
'
file
'
:
f
}
                         
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
call
?
)
:
{
file
}
'
)
            
if
verbose
:
                
if
inner_return_code
!
=
0
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
file
'
:
f
}
                             
'
Test
failed
:
{
file
}
'
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
file
'
:
f
}
                             
'
Test
passed
:
{
file
}
'
)
            
if
stop
and
return_code
>
0
:
                
return
1
        
if
not
found_tests
:
            
message
=
'
TEST
-
UNEXPECTED
-
FAIL
|
No
tests
collected
'
            
if
not
path_only
:
                 
message
+
=
'
(
Not
in
PYTHON_UNIT_TESTS
?
Try
-
-
path
-
only
?
)
'
            
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
        
return
0
if
return_code
=
=
0
else
1
    
Command
(
'
eslint
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
eslint
or
help
configure
eslint
for
optimal
development
.
'
)
    
CommandArgument
(
'
-
s
'
'
-
-
setup
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
configure
eslint
for
optimal
development
.
'
)
    
CommandArgument
(
'
-
e
'
'
-
-
ext
'
default
=
'
[
.
js
.
jsm
.
jsx
.
xml
.
html
]
'
        
help
=
'
Filename
extensions
to
lint
default
:
"
[
.
js
.
jsm
.
jsx
.
xml
.
html
]
"
.
'
)
    
CommandArgument
(
'
-
b
'
'
-
-
binary
'
default
=
None
        
help
=
'
Path
to
eslint
binary
.
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
eslint
(
self
setup
ext
=
None
binary
=
None
args
=
None
)
:
        
'
'
'
Run
eslint
.
'
'
'
        
nodePath
=
self
.
getNodeOrNpmPath
(
"
node
"
LooseVersion
(
"
4
.
2
.
3
"
)
)
        
if
not
nodePath
:
            
return
1
        
if
setup
:
            
return
self
.
eslint_setup
(
)
        
if
not
binary
:
            
binary
=
os
.
environ
.
get
(
'
ESLINT
'
None
)
            
if
not
binary
:
                
try
:
                    
binary
=
which
.
which
(
'
eslint
'
)
                
except
which
.
WhichError
:
                    
npmPath
=
self
.
getNodeOrNpmPath
(
"
npm
"
)
                    
if
npmPath
:
                        
try
:
                            
output
=
subprocess
.
check_output
(
[
npmPath
"
bin
"
"
-
g
"
]
                                                             
stderr
=
subprocess
.
STDOUT
)
                            
if
output
:
                                
base
=
output
.
split
(
"
\
n
"
)
[
0
]
.
strip
(
)
                                
binary
=
os
.
path
.
join
(
base
"
eslint
"
)
                                
if
not
os
.
path
.
isfile
(
binary
)
:
                                    
binary
=
None
                        
except
(
subprocess
.
CalledProcessError
WindowsError
)
:
                            
pass
        
if
not
binary
:
            
print
(
ESLINT_NOT_FOUND_MESSAGE
)
            
return
1
        
self
.
log
(
logging
.
INFO
'
eslint
'
{
'
binary
'
:
binary
'
args
'
:
args
}
            
'
Running
{
binary
}
'
)
        
args
=
args
or
[
'
.
'
]
        
cmd_args
=
[
binary
                    
'
-
-
plugin
'
'
html
'
                    
'
-
-
ext
'
ext
                    
]
+
args
        
success
=
self
.
run_process
(
cmd_args
            
pass_thru
=
True
            
ensure_exit_code
=
False
            
require_unix_environment
=
True
        
)
        
self
.
log
(
logging
.
INFO
'
eslint
'
{
'
msg
'
:
(
'
No
errors
'
if
success
=
=
0
else
'
Errors
'
)
}
            
'
Finished
eslint
.
{
msg
}
encountered
.
'
)
        
return
success
    
def
eslint_setup
(
self
update_only
=
False
)
:
        
"
"
"
Ensure
eslint
is
optimally
configured
.
        
This
command
will
inspect
your
eslint
configuration
and
        
guide
you
through
an
interactive
wizard
helping
you
configure
        
eslint
for
optimal
use
on
Mozilla
projects
.
        
"
"
"
        
sys
.
path
.
append
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
        
npmPath
=
self
.
getNodeOrNpmPath
(
"
npm
"
)
        
if
not
npmPath
:
            
return
1
        
success
=
self
.
callProcess
(
"
eslint
"
                                   
[
npmPath
"
install
"
"
eslint
2
.
9
.
0
"
"
-
g
"
]
)
        
if
not
success
:
            
return
1
        
success
=
self
.
callProcess
(
"
eslint
-
plugin
-
mozilla
"
                                   
[
npmPath
"
link
"
]
                                   
"
testing
/
eslint
-
plugin
-
mozilla
"
)
        
if
not
success
:
            
return
1
        
success
=
self
.
callProcess
(
"
eslint
-
plugin
-
html
"
                                   
[
npmPath
"
install
"
"
eslint
-
plugin
-
html
1
.
4
.
0
"
"
-
g
"
]
)
        
if
not
success
:
            
return
1
        
success
=
self
.
callProcess
(
"
eslint
-
plugin
-
react
"
                                   
[
npmPath
"
install
"
"
eslint
-
plugin
-
react
4
.
2
.
3
"
"
-
g
"
]
)
        
if
not
success
:
            
return
1
        
print
(
"
\
nESLint
and
approved
plugins
installed
successfully
!
"
)
    
def
callProcess
(
self
name
cmd
cwd
=
None
)
:
        
print
(
"
\
nInstalling
%
s
using
\
"
%
s
\
"
.
.
.
"
%
(
name
"
"
.
join
(
cmd
)
)
)
        
try
:
            
with
open
(
os
.
devnull
"
w
"
)
as
fnull
:
                
subprocess
.
check_call
(
cmd
cwd
=
cwd
stdout
=
fnull
)
        
except
subprocess
.
CalledProcessError
:
            
if
cwd
:
                
print
(
"
\
nError
installing
%
s
in
the
%
s
folder
aborting
.
"
%
(
name
cwd
)
)
            
else
:
                
print
(
"
\
nError
installing
%
s
aborting
.
"
%
name
)
            
return
False
        
return
True
    
def
getPossibleNodePathsWin
(
self
)
:
        
"
"
"
        
Return
possible
nodejs
paths
on
Windows
.
        
"
"
"
        
if
platform
.
system
(
)
!
=
"
Windows
"
:
            
return
[
]
        
return
list
(
{
            
"
%
s
\
\
nodejs
"
%
os
.
environ
.
get
(
"
SystemDrive
"
)
            
os
.
path
.
join
(
os
.
environ
.
get
(
"
ProgramFiles
"
)
"
nodejs
"
)
            
os
.
path
.
join
(
os
.
environ
.
get
(
"
PROGRAMW6432
"
)
"
nodejs
"
)
            
os
.
path
.
join
(
os
.
environ
.
get
(
"
PROGRAMFILES
"
)
"
nodejs
"
)
        
}
)
    
def
getNodeOrNpmPath
(
self
filename
minversion
=
None
)
:
        
"
"
"
        
Return
the
nodejs
or
npm
path
.
        
"
"
"
        
if
platform
.
system
(
)
=
=
"
Windows
"
:
            
for
ext
in
[
"
.
cmd
"
"
.
exe
"
"
"
]
:
                
try
:
                    
nodeOrNpmPath
=
which
.
which
(
filename
+
ext
                                                
path
=
self
.
getPossibleNodePathsWin
(
)
)
                    
if
self
.
is_valid
(
nodeOrNpmPath
minversion
)
:
                        
return
nodeOrNpmPath
                
except
which
.
WhichError
:
                    
pass
        
else
:
            
try
:
                
nodeOrNpmPath
=
which
.
which
(
filename
)
                
if
self
.
is_valid
(
nodeOrNpmPath
minversion
)
:
                    
return
nodeOrNpmPath
            
except
which
.
WhichError
:
                
pass
        
if
filename
=
=
"
node
"
:
            
print
(
NODE_NOT_FOUND_MESSAGE
)
        
elif
filename
=
=
"
npm
"
:
            
print
(
NPM_NOT_FOUND_MESSAGE
)
        
if
platform
.
system
(
)
=
=
"
Windows
"
:
            
appPaths
=
self
.
getPossibleNodePathsWin
(
)
            
for
p
in
appPaths
:
                
print
(
"
-
%
s
"
%
p
)
        
elif
platform
.
system
(
)
=
=
"
Darwin
"
:
            
print
(
"
-
/
usr
/
local
/
bin
/
node
"
)
        
elif
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
            
print
(
"
-
/
usr
/
bin
/
nodejs
"
)
        
return
None
    
def
is_valid
(
self
path
minversion
=
None
)
:
        
try
:
            
version_str
=
subprocess
.
check_output
(
[
path
"
-
-
version
"
]
                                                  
stderr
=
subprocess
.
STDOUT
)
            
if
minversion
:
                
version
=
LooseVersion
(
version_str
.
lstrip
(
'
v
'
)
)
                
return
version
>
=
minversion
            
return
True
        
except
(
subprocess
.
CalledProcessError
WindowsError
)
:
            
return
False
