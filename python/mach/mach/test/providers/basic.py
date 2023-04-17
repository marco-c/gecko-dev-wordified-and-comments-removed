from
__future__
import
absolute_import
from
__future__
import
unicode_literals
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
from
mozbuild
.
base
import
MachCommandBase
CommandProvider
class
ConditionsProvider
(
MachCommandBase
)
:
    
Command
(
"
cmd_foo
"
category
=
"
testing
"
)
    
def
run_foo
(
self
command_context
)
:
        
pass
    
Command
(
"
cmd_bar
"
category
=
"
testing
"
)
    
CommandArgument
(
"
-
-
baz
"
action
=
"
store_true
"
help
=
"
Run
with
baz
"
)
    
def
run_bar
(
self
command_context
baz
=
None
)
:
        
pass
