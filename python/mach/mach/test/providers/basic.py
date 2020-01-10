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
CommandProvider
class
ConditionsProvider
(
object
)
:
    
Command
(
'
cmd_foo
'
category
=
'
testing
'
)
    
def
run_foo
(
self
)
:
        
pass
    
Command
(
'
cmd_bar
'
category
=
'
testing
'
)
    
CommandArgument
(
'
-
-
baz
'
action
=
"
store_true
"
                     
help
=
'
Run
with
baz
'
)
    
def
run_bar
(
self
baz
=
None
)
:
        
pass
