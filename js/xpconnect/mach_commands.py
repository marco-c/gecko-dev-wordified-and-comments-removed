import
argparse
from
mach
.
decorators
import
Command
CommandArgument
Command
(
    
"
xpcshell
"
    
category
=
"
misc
"
    
description
=
"
Run
the
xpcshell
binary
"
)
CommandArgument
(
    
"
-
-
app
"
    
help
=
"
The
path
to
the
Firefox
binary
(
default
:
the
binary
in
TOPOBJDIR
)
"
    
dest
=
"
firefox_bin
"
)
CommandArgument
(
    
"
args
"
    
nargs
=
argparse
.
REMAINDER
    
help
=
"
Arguments
to
provide
to
xpcshell
"
)
def
xpcshell
(
command_context
*
firefox_bin
args
)
:
    
if
not
firefox_bin
:
        
firefox_bin
=
command_context
.
get_binary_path
(
"
app
"
)
    
command
=
[
str
(
firefox_bin
)
"
-
xpcshell
"
]
    
env
=
{
        
"
MOZ_DISABLE_SOCKET_PROCESS
"
:
"
1
"
    
}
    
if
args
:
        
command
.
extend
(
args
)
    
return
command_context
.
run_process
(
        
command
        
pass_thru
=
True
        
ensure_exit_code
=
False
        
append_env
=
env
    
)
