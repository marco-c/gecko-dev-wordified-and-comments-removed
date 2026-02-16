import
argparse
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
MachCommandBase
class
EvalCommand
(
MachCommandBase
)
:
    
"
"
"
Forward
eval
runs
to
mozperftest
and
mochitests
.
"
"
"
    
Command
(
        
"
eval
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
evaluation
tests
backed
by
perftests
and
mochitests
.
"
    
)
    
CommandArgument
(
        
"
test_path
"
        
help
=
"
The
path
to
an
individual
test
relative
to
the
repo
root
.
The
test
must
"
        
"
be
an
evaluation
test
located
in
a
browser_eval
folder
.
Multiple
tests
are
not
"
        
"
supported
.
"
    
)
    
CommandArgument
(
        
"
extra_args
"
        
nargs
=
argparse
.
REMAINDER
        
help
=
"
Additional
mochitest
arguments
passed
through
to
perftest
.
"
    
)
    
def
run_eval
(
self
test_path
:
str
extra_args
:
Optional
[
list
]
=
None
)
:
        
perftest_args
=
[
test_path
]
        
if
extra_args
:
            
extra_args
=
[
arg
.
lstrip
(
"
-
"
)
for
arg
in
extra_args
]
            
perftest_args
.
extend
(
[
"
-
-
mochitest
-
extra
-
args
"
*
extra_args
]
)
        
return
self
.
_mach_context
.
commands
.
dispatch
(
            
"
perftest
"
            
self
.
_mach_context
            
perftest_args
        
)
