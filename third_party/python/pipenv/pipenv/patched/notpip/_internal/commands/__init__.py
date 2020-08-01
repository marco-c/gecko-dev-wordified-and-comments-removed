"
"
"
Package
containing
all
pip
commands
"
"
"
from
__future__
import
absolute_import
import
importlib
from
collections
import
OrderedDict
namedtuple
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
typing
import
MYPY_CHECK_RUNNING
if
MYPY_CHECK_RUNNING
:
    
from
typing
import
Any
    
from
pipenv
.
patched
.
notpip
.
_internal
.
cli
.
base_command
import
Command
CommandInfo
=
namedtuple
(
'
CommandInfo
'
'
module_path
class_name
summary
'
)
commands_dict
=
OrderedDict
(
[
    
(
'
install
'
CommandInfo
(
        
'
pipenv
.
patched
.
notpip
.
_internal
.
commands
.
install
'
'
InstallCommand
'
        
'
Install
packages
.
'
    
)
)
    
(
'
download
'
CommandInfo
(
        
'
pipenv
.
patched
.
notpip
.
_internal
.
commands
.
download
'
'
DownloadCommand
'
        
'
Download
packages
.
'
    
)
)
    
(
'
uninstall
'
CommandInfo
(
        
'
pipenv
.
patched
.
notpip
.
_internal
.
commands
.
uninstall
'
'
UninstallCommand
'
        
'
Uninstall
packages
.
'
    
)
)
    
(
'
freeze
'
CommandInfo
(
        
'
pipenv
.
patched
.
notpip
.
_internal
.
commands
.
freeze
'
'
FreezeCommand
'
        
'
Output
installed
packages
in
requirements
format
.
'
    
)
)
    
(
'
list
'
CommandInfo
(
        
'
pipenv
.
patched
.
notpip
.
_internal
.
commands
.
list
'
'
ListCommand
'
        
'
List
installed
packages
.
'
    
)
)
    
(
'
show
'
CommandInfo
(
        
'
pipenv
.
patched
.
notpip
.
_internal
.
commands
.
show
'
'
ShowCommand
'
        
'
Show
information
about
installed
packages
.
'
    
)
)
    
(
'
check
'
CommandInfo
(
        
'
pipenv
.
patched
.
notpip
.
_internal
.
commands
.
check
'
'
CheckCommand
'
        
'
Verify
installed
packages
have
compatible
dependencies
.
'
    
)
)
    
(
'
config
'
CommandInfo
(
        
'
pipenv
.
patched
.
notpip
.
_internal
.
commands
.
configuration
'
'
ConfigurationCommand
'
        
'
Manage
local
and
global
configuration
.
'
    
)
)
    
(
'
search
'
CommandInfo
(
        
'
pipenv
.
patched
.
notpip
.
_internal
.
commands
.
search
'
'
SearchCommand
'
        
'
Search
PyPI
for
packages
.
'
    
)
)
    
(
'
wheel
'
CommandInfo
(
        
'
pipenv
.
patched
.
notpip
.
_internal
.
commands
.
wheel
'
'
WheelCommand
'
        
'
Build
wheels
from
your
requirements
.
'
    
)
)
    
(
'
hash
'
CommandInfo
(
        
'
pipenv
.
patched
.
notpip
.
_internal
.
commands
.
hash
'
'
HashCommand
'
        
'
Compute
hashes
of
package
archives
.
'
    
)
)
    
(
'
completion
'
CommandInfo
(
        
'
pipenv
.
patched
.
notpip
.
_internal
.
commands
.
completion
'
'
CompletionCommand
'
        
'
A
helper
command
used
for
command
completion
.
'
    
)
)
    
(
'
debug
'
CommandInfo
(
        
'
pipenv
.
patched
.
notpip
.
_internal
.
commands
.
debug
'
'
DebugCommand
'
        
'
Show
information
useful
for
debugging
.
'
    
)
)
    
(
'
help
'
CommandInfo
(
        
'
pipenv
.
patched
.
notpip
.
_internal
.
commands
.
help
'
'
HelpCommand
'
        
'
Show
help
for
commands
.
'
    
)
)
]
)
def
create_command
(
name
*
*
kwargs
)
:
    
"
"
"
    
Create
an
instance
of
the
Command
class
with
the
given
name
.
    
"
"
"
    
module_path
class_name
summary
=
commands_dict
[
name
]
    
module
=
importlib
.
import_module
(
module_path
)
    
command_class
=
getattr
(
module
class_name
)
    
command
=
command_class
(
name
=
name
summary
=
summary
*
*
kwargs
)
    
return
command
def
get_similar_commands
(
name
)
:
    
"
"
"
Command
name
auto
-
correct
.
"
"
"
    
from
difflib
import
get_close_matches
    
name
=
name
.
lower
(
)
    
close_commands
=
get_close_matches
(
name
commands_dict
.
keys
(
)
)
    
if
close_commands
:
        
return
close_commands
[
0
]
    
else
:
        
return
False
