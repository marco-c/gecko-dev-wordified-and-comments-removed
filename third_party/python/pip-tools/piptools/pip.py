import
optparse
from
.
_compat
import
Command
cmdoptions
class
PipCommand
(
Command
)
:
    
name
=
"
PipCommand
"
def
get_pip_command
(
)
:
    
pip_command
=
PipCommand
(
)
    
pip_command
.
parser
.
add_option
(
cmdoptions
.
no_binary
(
)
)
    
pip_command
.
parser
.
add_option
(
cmdoptions
.
only_binary
(
)
)
    
index_opts
=
cmdoptions
.
make_option_group
(
        
cmdoptions
.
index_group
pip_command
.
parser
    
)
    
pip_command
.
parser
.
insert_option_group
(
0
index_opts
)
    
pip_command
.
parser
.
add_option
(
        
optparse
.
Option
(
"
-
-
pre
"
action
=
"
store_true
"
default
=
False
)
    
)
    
return
pip_command
pip_command
=
get_pip_command
(
)
pip_defaults
=
pip_command
.
parser
.
get_default_values
(
)
