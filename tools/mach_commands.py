import
argparse
import
logging
import
subprocess
import
sys
from
datetime
import
datetime
timedelta
from
operator
import
itemgetter
from
mach
.
decorators
import
Command
CommandArgument
SubCommand
from
mozbuild
.
base
import
MozbuildObject
def
_get_busted_bugs
(
payload
)
:
    
import
requests
    
payload
=
dict
(
payload
)
    
payload
[
"
include_fields
"
]
=
"
id
summary
last_change_time
resolution
"
    
payload
[
"
blocks
"
]
=
1543241
    
response
=
requests
.
get
(
"
https
:
/
/
bugzilla
.
mozilla
.
org
/
rest
/
bug
"
payload
)
    
response
.
raise_for_status
(
)
    
return
response
.
json
(
)
.
get
(
"
bugs
"
[
]
)
Command
(
    
"
busted
"
    
category
=
"
misc
"
    
description
=
"
Query
known
bugs
in
our
tooling
and
file
new
ones
.
"
)
def
busted_default
(
command_context
)
:
    
unresolved
=
_get_busted_bugs
(
{
"
resolution
"
:
"
-
-
-
"
}
)
    
creation_time
=
datetime
.
now
(
)
-
timedelta
(
days
=
15
)
    
creation_time
=
creation_time
.
strftime
(
"
%
Y
-
%
m
-
%
dT
%
H
-
%
M
-
%
SZ
"
)
    
resolved
=
_get_busted_bugs
(
{
"
creation_time
"
:
creation_time
}
)
    
resolved
=
[
bug
for
bug
in
resolved
if
bug
[
"
resolution
"
]
]
    
all_bugs
=
sorted
(
        
unresolved
+
resolved
key
=
itemgetter
(
"
last_change_time
"
)
reverse
=
True
    
)
    
if
all_bugs
:
        
for
bug
in
all_bugs
:
            
print
(
                
"
[
%
s
]
Bug
%
s
-
%
s
"
                
%
(
                    
(
                        
"
UNRESOLVED
"
                        
if
not
bug
[
"
resolution
"
]
                        
else
"
RESOLVED
-
%
s
"
%
bug
[
"
resolution
"
]
                    
)
                    
bug
[
"
id
"
]
                    
bug
[
"
summary
"
]
                
)
            
)
    
else
:
        
print
(
"
No
known
tooling
issues
found
.
"
)
SubCommand
(
"
busted
"
"
file
"
description
=
"
File
a
bug
for
busted
tooling
.
"
)
CommandArgument
(
    
"
against
"
    
help
=
(
        
"
The
specific
mach
command
that
is
busted
(
i
.
e
.
if
you
encountered
"
        
"
an
error
with
mach
build
run
mach
busted
file
build
)
.
If
"
        
"
the
issue
is
not
connected
to
any
particular
mach
command
you
"
        
"
can
also
run
mach
busted
file
general
.
"
    
)
)
def
busted_file
(
command_context
against
)
:
    
import
webbrowser
    
if
(
        
against
!
=
"
general
"
        
and
against
not
in
command_context
.
_mach_context
.
commands
.
command_handlers
    
)
:
        
print
(
            
"
%
s
is
not
a
valid
value
for
against
.
against
must
be
"
            
"
the
name
of
a
mach
command
or
else
the
string
"
            
'
"
general
"
.
'
%
against
        
)
        
return
1
    
if
against
=
=
"
general
"
:
        
product
=
"
Firefox
Build
System
"
        
component
=
"
General
"
    
else
:
        
import
inspect
        
import
mozpack
.
path
as
mozpath
        
handler
=
command_context
.
_mach_context
.
commands
.
command_handlers
[
against
]
        
sourcefile
=
mozpath
.
relpath
(
            
inspect
.
getsourcefile
(
handler
.
func
)
command_context
.
topsrcdir
        
)
        
reader
=
command_context
.
mozbuild_reader
(
config_mode
=
"
empty
"
)
        
try
:
            
res
=
reader
.
files_info
(
[
sourcefile
]
)
[
sourcefile
]
[
"
BUG_COMPONENT
"
]
            
product
component
=
res
.
product
res
.
component
        
except
TypeError
:
            
product
=
"
Firefox
Build
System
"
            
component
=
"
General
"
    
uri
=
(
        
"
https
:
/
/
bugzilla
.
mozilla
.
org
/
enter_bug
.
cgi
?
"
        
"
product
=
%
s
&
component
=
%
s
&
blocked
=
1543241
"
%
(
product
component
)
    
)
    
webbrowser
.
open_new_tab
(
uri
)
def
pastebin_create_parser
(
)
:
    
parser
=
argparse
.
ArgumentParser
(
)
    
parser
.
add_argument
(
"
argv
"
nargs
=
argparse
.
REMAINDER
help
=
argparse
.
SUPPRESS
)
    
return
parser
Command
(
    
"
pastebin
"
    
category
=
"
misc
"
    
hidden
=
True
    
parser
=
pastebin_create_parser
)
def
pastebin
(
command_context
argv
)
:
    
"
"
"
Obsolete
command
line
interface
to
paste
.
mozilla
.
org
.
"
"
"
    
print
(
        
"
pastebin
.
mozilla
.
org
has
been
decommissioned
.
\
n
"
        
"
Please
use
your
favorite
search
engine
to
find
alternatives
.
"
    
)
    
return
1
class
PypiBasedTool
:
    
"
"
"
    
Helper
for
loading
a
tool
that
is
hosted
on
pypi
.
The
package
is
expected
    
to
expose
a
mach_interface
module
which
has
new_release_on_pypi
    
parser
and
run
functions
.
    
"
"
"
    
def
__init__
(
self
module_name
pypi_name
=
None
)
:
        
self
.
name
=
module_name
        
self
.
pypi_name
=
pypi_name
or
module_name
    
def
_import
(
self
)
:
        
import
importlib
        
try
:
            
return
importlib
.
import_module
(
"
%
s
.
mach_interface
"
%
self
.
name
)
        
except
ImportError
:
            
return
None
    
def
create_parser
(
self
subcommand
=
None
)
:
        
cmd
=
MozbuildObject
.
from_environment
(
)
        
cmd
.
activate_virtualenv
(
)
        
tool
=
self
.
_import
(
)
        
if
not
tool
:
            
cmd
.
virtualenv_manager
.
install_pip_package
(
self
.
pypi_name
)
            
print
(
                
"
%
s
was
installed
.
please
re
-
run
your
"
                
"
command
.
If
you
keep
getting
this
message
please
"
                
"
manually
run
:
'
pip
install
-
U
%
s
'
.
"
%
(
self
.
pypi_name
self
.
pypi_name
)
            
)
        
else
:
            
release
=
tool
.
new_release_on_pypi
(
)
            
if
release
:
                
print
(
release
)
                
subprocess
.
check_call
(
                    
[
                        
cmd
.
virtualenv_manager
.
python_path
                        
"
-
m
"
                        
"
pip
"
                        
"
install
"
                        
f
"
{
self
.
pypi_name
}
=
=
{
release
}
"
                    
]
                
)
                
print
(
                    
"
%
s
was
updated
to
version
%
s
.
please
"
                    
"
re
-
run
your
command
.
"
%
(
self
.
pypi_name
release
)
                
)
            
elif
subcommand
:
                
return
tool
.
parser
(
subcommand
)
            
else
:
                
return
tool
.
parser
(
)
        
sys
.
exit
(
0
)
    
def
run
(
self
*
*
options
)
:
        
tool
=
self
.
_import
(
)
        
tool
.
run
(
options
)
def
mozregression_create_parser
(
)
:
    
loader
=
PypiBasedTool
(
"
mozregression
"
)
    
return
loader
.
create_parser
(
)
Command
(
    
"
mozregression
"
    
category
=
"
misc
"
    
description
=
"
Regression
range
finder
for
nightly
and
inbound
builds
.
"
    
parser
=
mozregression_create_parser
)
def
run
(
command_context
*
*
options
)
:
    
command_context
.
activate_virtualenv
(
)
    
mozregression
=
PypiBasedTool
(
"
mozregression
"
)
    
mozregression
.
run
(
*
*
options
)
Command
(
    
"
node
"
    
category
=
"
devenv
"
    
description
=
"
Run
the
NodeJS
interpreter
used
for
building
.
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
)
def
node
(
command_context
args
)
:
    
from
mozbuild
.
nodeutil
import
find_node_executable
    
command_context
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
    
node_path
_
=
find_node_executable
(
)
    
return
command_context
.
run_process
(
        
[
node_path
]
+
args
        
pass_thru
=
True
        
ensure_exit_code
=
False
    
)
Command
(
    
"
npm
"
    
category
=
"
devenv
"
    
description
=
"
Run
the
npm
executable
from
the
NodeJS
used
for
building
.
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
)
def
npm
(
command_context
args
)
:
    
from
mozbuild
.
nodeutil
import
find_npm_executable
    
command_context
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
    
import
os
    
npm_path
_
=
find_npm_executable
(
)
    
if
not
npm_path
:
        
print
(
"
error
:
could
not
find
npm
executable
"
)
        
sys
.
exit
(
-
1
)
    
path
=
os
.
path
.
abspath
(
os
.
path
.
dirname
(
npm_path
)
)
    
os
.
environ
[
"
PATH
"
]
=
"
{
}
{
}
{
}
"
.
format
(
path
os
.
pathsep
os
.
environ
[
"
PATH
"
]
)
    
firefox_bin
=
command_context
.
get_binary_path
(
validate_exists
=
False
)
    
if
os
.
path
.
exists
(
firefox_bin
)
:
        
os
.
environ
[
"
FIREFOX_BIN
"
]
=
firefox_bin
    
return
command_context
.
run_process
(
        
[
npm_path
"
-
-
scripts
-
prepend
-
node
-
path
=
auto
"
]
+
args
        
pass_thru
=
True
        
ensure_exit_code
=
False
    
)
def
logspam_create_parser
(
subcommand
)
:
    
loader
=
PypiBasedTool
(
"
logspam
"
"
mozilla
-
log
-
spam
"
)
    
return
loader
.
create_parser
(
subcommand
)
from
functools
import
partial
Command
(
    
"
logspam
"
    
category
=
"
misc
"
    
description
=
"
Warning
categorizer
for
treeherder
test
runs
.
"
)
def
logspam
(
command_context
)
:
    
pass
SubCommand
(
"
logspam
"
"
report
"
parser
=
partial
(
logspam_create_parser
"
report
"
)
)
def
report
(
command_context
*
*
options
)
:
    
command_context
.
activate_virtualenv
(
)
    
logspam
=
PypiBasedTool
(
"
logspam
"
)
    
logspam
.
run
(
command
=
"
report
"
*
*
options
)
SubCommand
(
"
logspam
"
"
bisect
"
parser
=
partial
(
logspam_create_parser
"
bisect
"
)
)
def
bisect
(
command_context
*
*
options
)
:
    
command_context
.
activate_virtualenv
(
)
    
logspam
=
PypiBasedTool
(
"
logspam
"
)
    
logspam
.
run
(
command
=
"
bisect
"
*
*
options
)
SubCommand
(
"
logspam
"
"
file
"
parser
=
partial
(
logspam_create_parser
"
file
"
)
)
def
create
(
command_context
*
*
options
)
:
    
command_context
.
activate_virtualenv
(
)
    
logspam
=
PypiBasedTool
(
"
logspam
"
)
    
logspam
.
run
(
command
=
"
file
"
*
*
options
)
mots_loader
=
PypiBasedTool
(
"
mots
"
)
def
mots_create_parser
(
subcommand
=
None
)
:
    
return
mots_loader
.
create_parser
(
subcommand
)
def
mots_run_subcommand
(
command
command_context
*
*
options
)
:
    
command_context
.
activate_virtualenv
(
)
    
mots_loader
.
run
(
command
=
command
*
*
options
)
class
motsSubCommand
(
SubCommand
)
:
    
"
"
"
A
helper
subclass
that
reduces
repitition
when
defining
subcommands
.
"
"
"
    
def
__init__
(
self
subcommand
)
:
        
super
(
)
.
__init__
(
            
"
mots
"
            
subcommand
            
parser
=
partial
(
mots_create_parser
subcommand
)
        
)
Command
(
    
"
mots
"
    
category
=
"
misc
"
    
description
=
"
Manage
module
information
in
-
tree
using
the
mots
CLI
.
"
    
parser
=
mots_create_parser
)
def
mots
(
command_context
*
*
options
)
:
    
"
"
"
The
main
mots
command
call
.
"
"
"
    
command_context
.
activate_virtualenv
(
)
    
mots_loader
.
run
(
*
*
options
)
for
sc
in
(
    
"
clean
"
    
"
check
-
hashes
"
    
"
export
"
    
"
export
-
and
-
clean
"
    
"
module
"
    
"
query
"
    
"
settings
"
    
"
user
"
    
"
validate
"
)
:
    
motsSubCommand
(
sc
)
(
lambda
*
a
*
*
kw
:
mots_run_subcommand
(
sc
*
a
*
*
kw
)
)
