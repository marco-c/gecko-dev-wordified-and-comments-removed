from
__future__
import
absolute_import
unicode_literals
import
six
import
logging
import
os
import
sys
from
mozbuild
.
base
import
(
    
MachCommandConditions
as
conditions
    
BinaryNotFoundException
)
from
mach
.
decorators
import
(
    
Command
)
def
setup_argument_parser_functional
(
)
:
    
from
firefox_ui_harness
.
arguments
.
base
import
FirefoxUIArguments
    
from
mozlog
.
structured
import
commandline
    
parser
=
FirefoxUIArguments
(
)
    
commandline
.
add_logging_group
(
parser
)
    
return
parser
def
run_firefox_ui_test
(
topsrcdir
=
None
*
*
kwargs
)
:
    
from
mozlog
.
structured
import
commandline
    
from
argparse
import
Namespace
    
import
firefox_ui_harness
    
parser
=
setup_argument_parser_functional
(
)
    
fxui_dir
=
os
.
path
.
join
(
topsrcdir
"
testing
"
"
firefox
-
ui
"
)
    
if
not
kwargs
[
"
server_root
"
]
:
        
kwargs
[
"
server_root
"
]
=
os
.
path
.
join
(
fxui_dir
"
resources
"
)
    
if
"
test_objects
"
in
kwargs
:
        
tests
=
[
]
        
for
obj
in
kwargs
[
"
test_objects
"
]
:
            
tests
.
append
(
obj
[
"
file_relpath
"
]
)
        
kwargs
[
"
tests
"
]
=
tests
    
elif
not
kwargs
.
get
(
"
tests
"
)
:
        
kwargs
[
"
tests
"
]
=
os
.
path
.
join
(
fxui_dir
"
tests
"
"
functional
"
"
manifest
.
ini
"
)
    
kwargs
[
"
logger
"
]
=
kwargs
.
pop
(
"
log
"
None
)
    
if
not
kwargs
[
"
logger
"
]
:
        
kwargs
[
"
logger
"
]
=
commandline
.
setup_logging
(
            
"
Firefox
UI
-
Functional
Tests
"
{
"
mach
"
:
sys
.
stdout
}
        
)
    
args
=
Namespace
(
)
    
for
k
v
in
six
.
iteritems
(
kwargs
)
:
        
setattr
(
args
k
v
)
    
parser
.
verify_usage
(
args
)
    
failed
=
firefox_ui_harness
.
cli_functional
.
cli
(
args
=
vars
(
args
)
)
    
if
failed
>
0
:
        
return
1
    
else
:
        
return
0
Command
(
    
"
firefox
-
ui
-
functional
"
    
category
=
"
testing
"
    
conditions
=
[
conditions
.
is_firefox
]
    
description
=
"
Run
the
functional
test
suite
of
Firefox
UI
tests
.
"
    
parser
=
setup_argument_parser_functional
)
def
run_firefox_ui_functional
(
command_context
*
*
kwargs
)
:
    
try
:
        
kwargs
[
"
binary
"
]
=
kwargs
[
"
binary
"
]
or
command_context
.
get_binary_path
(
"
app
"
)
    
except
BinaryNotFoundException
as
e
:
        
command_context
.
log
(
            
logging
.
ERROR
            
"
firefox
-
ui
-
functional
"
            
{
"
error
"
:
str
(
e
)
}
            
"
ERROR
:
{
error
}
"
        
)
        
command_context
.
log
(
            
logging
.
INFO
"
firefox
-
ui
-
functional
"
{
"
help
"
:
e
.
help
(
)
}
"
{
help
}
"
        
)
        
return
1
    
return
run_firefox_ui_test
(
topsrcdir
=
command_context
.
topsrcdir
*
*
kwargs
)
