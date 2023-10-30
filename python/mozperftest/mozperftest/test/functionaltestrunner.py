import
pathlib
import
sys
import
mozlog
from
mozperftest
.
utils
import
load_class_from_path
class
FunctionalTestProcessor
(
mozlog
.
handlers
.
StreamHandler
)
:
    
"
"
"
Used
for
capturing
the
perfMetrics
output
from
a
mach
test
run
.
"
"
"
    
def
__init__
(
self
*
args
*
*
kwargs
)
:
        
self
.
_match
=
[
]
        
super
(
FunctionalTestProcessor
self
)
.
__init__
(
*
args
*
*
kwargs
)
    
def
__call__
(
self
data
)
:
        
formatted
=
self
.
formatter
(
data
)
        
if
formatted
is
not
None
and
"
perfMetrics
"
in
formatted
:
            
self
.
match
.
append
(
formatted
)
    
property
    
def
match
(
self
)
:
        
return
self
.
_match
class
FunctionalTestRunner
:
    
def
test
(
command_context
what
extra_args
*
*
log_args
)
:
        
"
"
"
Run
tests
from
names
or
paths
.
        
Based
on
the
mach
test
command
in
testing
/
mach_commands
.
py
.
It
uses
        
the
same
logic
but
with
less
features
for
logging
and
a
custom
log
        
handler
to
capture
the
perfMetrics
output
.
        
"
"
"
        
from
mozlog
.
commandline
import
setup_logging
        
from
moztest
.
resolve
import
TestResolver
        
resolver
=
command_context
.
_spawn
(
TestResolver
)
        
run_suites
run_tests
=
resolver
.
resolve_metadata
(
what
)
        
if
not
run_suites
and
not
run_tests
:
            
print
(
                
"
Could
not
find
the
requested
test
.
Ensure
that
it
works
with
.
/
mach
test
.
"
            
)
            
return
1
None
        
setup_logging
(
            
"
mach
-
test
"
            
log_args
            
{
"
mach
"
:
sys
.
stdout
}
            
{
"
level
"
:
"
info
"
"
verbose
"
:
True
"
compact
"
:
False
}
        
)
        
log_processor
=
FunctionalTestProcessor
(
            
stream
=
sys
.
stdout
            
formatter
=
mozlog
.
formatters
.
MachFormatter
(
                
verbose
=
True
disable_colors
=
False
            
)
        
)
        
machtestrunner
=
load_class_from_path
(
            
"
MachTestRunner
"
            
pathlib
.
Path
(
command_context
.
topsrcdir
"
testing
/
mach_commands
.
py
"
)
        
)
        
command_context
.
_mach_context
.
settings
=
{
            
"
test
"
:
{
                
"
level
"
:
"
info
"
                
"
verbose
"
:
True
                
"
compact
"
:
False
                
"
format
"
:
"
mach
"
            
}
        
}
        
log_args
[
"
custom_handler
"
]
=
log_processor
        
status
=
machtestrunner
.
test
(
command_context
what
extra_args
*
*
log_args
)
        
return
status
log_processor
