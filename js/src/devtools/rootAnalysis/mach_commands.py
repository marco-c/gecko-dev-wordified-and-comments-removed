#
-
*
-
coding
:
utf
-
8
-
*
-
from
__future__
import
absolute_import
print_function
unicode_literals
import
argparse
import
json
import
os
import
textwrap
from
mach
.
base
import
FailedCommandError
MachError
from
mach
.
decorators
import
(
    
CommandArgument
    
CommandProvider
    
Command
    
SubCommand
)
from
mach
.
registrar
import
Registrar
from
mozbuild
.
mozconfig
import
MozconfigLoader
from
mozbuild
.
base
import
MachCommandBase
import
mozbuild
.
artifact_commands
import
mozbuild
.
build_commands
def
inherit_command_args
(
command
subcommand
=
None
)
:
    
"
"
"
Decorator
for
inheriting
all
command
-
line
arguments
from
mach
build
.
    
This
should
come
earlier
in
the
source
file
than
Command
or
SubCommand
    
because
it
relies
on
that
decorator
having
run
first
.
"
"
"
    
def
inherited
(
func
)
:
        
handler
=
Registrar
.
command_handlers
.
get
(
command
)
        
if
handler
is
not
None
and
subcommand
is
not
None
:
            
handler
=
handler
.
subcommand_handlers
.
get
(
subcommand
)
        
if
handler
is
None
:
            
raise
MachError
(
                
"
{
}
command
unknown
or
not
yet
loaded
"
.
format
(
                    
command
if
subcommand
is
None
else
command
+
"
"
+
subcommand
                
)
            
)
        
func
.
_mach_command
.
arguments
.
extend
(
handler
.
arguments
)
        
return
func
    
return
inherited
CommandProvider
class
MachCommands
(
MachCommandBase
)
:
    
property
    
def
state_dir
(
self
)
:
        
return
os
.
environ
.
get
(
"
MOZBUILD_STATE_PATH
"
os
.
path
.
expanduser
(
"
~
/
.
mozbuild
"
)
)
    
property
    
def
tools_dir
(
self
)
:
        
if
os
.
environ
.
get
(
"
MOZ_FETCHES_DIR
"
)
:
            
return
os
.
path
.
join
(
os
.
environ
[
"
HOME
"
]
os
.
environ
[
"
MOZ_FETCHES_DIR
"
]
)
        
return
os
.
path
.
join
(
self
.
state_dir
"
hazard
-
tools
"
)
    
property
    
def
sixgill_dir
(
self
)
:
        
return
os
.
path
.
join
(
self
.
tools_dir
"
sixgill
"
)
    
property
    
def
gcc_dir
(
self
)
:
        
return
os
.
path
.
join
(
self
.
tools_dir
"
gcc
"
)
    
property
    
def
script_dir
(
self
)
:
        
return
os
.
path
.
join
(
self
.
topsrcdir
"
js
/
src
/
devtools
/
rootAnalysis
"
)
    
def
work_dir
(
self
application
given
)
:
        
if
given
is
not
None
:
            
return
given
        
return
os
.
path
.
join
(
self
.
topsrcdir
"
haz
-
"
+
application
)
    
def
ensure_dir_exists
(
self
dir
)
:
        
os
.
makedirs
(
dir
exist_ok
=
True
)
        
return
dir
    
def
setup_env_for_tools
(
self
env
)
:
        
gccbin
=
os
.
path
.
join
(
self
.
gcc_dir
"
bin
"
)
        
env
[
"
CC
"
]
=
os
.
path
.
join
(
gccbin
"
gcc
"
)
        
env
[
"
CXX
"
]
=
os
.
path
.
join
(
gccbin
"
g
+
+
"
)
        
env
[
"
PATH
"
]
=
"
{
sixgill_dir
}
/
usr
/
bin
:
{
gccbin
}
:
{
PATH
}
"
.
format
(
            
sixgill_dir
=
self
.
sixgill_dir
gccbin
=
gccbin
PATH
=
env
[
"
PATH
"
]
        
)
        
env
[
"
LD_LIBRARY_PATH
"
]
=
"
{
}
/
lib64
"
.
format
(
self
.
gcc_dir
)
    
Command
(
        
"
hazards
"
        
category
=
"
build
"
        
order
=
"
declaration
"
        
description
=
"
Commands
for
running
the
static
analysis
for
GC
rooting
hazards
"
    
)
    
def
hazards
(
self
)
:
        
"
"
"
Commands
related
to
performing
the
GC
rooting
hazard
analysis
"
"
"
        
print
(
"
See
mach
hazards
-
-
help
for
a
list
of
subcommands
"
)
    
inherit_command_args
(
"
artifact
"
"
toolchain
"
)
    
SubCommand
(
        
"
hazards
"
        
"
bootstrap
"
        
description
=
"
Install
prerequisites
for
the
hazard
analysis
"
    
)
    
def
bootstrap
(
self
*
*
kwargs
)
:
        
orig_dir
=
os
.
getcwd
(
)
        
os
.
chdir
(
self
.
ensure_dir_exists
(
self
.
tools_dir
)
)
        
try
:
            
kwargs
[
"
from_build
"
]
=
(
"
linux64
-
gcc
-
sixgill
"
"
linux64
-
gcc
-
8
"
)
            
self
.
_mach_context
.
commands
.
dispatch
(
                
"
artifact
"
self
.
_mach_context
subcommand
=
"
toolchain
"
*
*
kwargs
            
)
        
finally
:
            
os
.
chdir
(
orig_dir
)
    
inherit_command_args
(
"
build
"
)
    
SubCommand
(
        
"
hazards
"
"
build
-
shell
"
description
=
"
Build
a
shell
for
the
hazard
analysis
"
    
)
    
CommandArgument
(
        
"
-
-
mozconfig
"
        
default
=
None
        
metavar
=
"
FILENAME
"
        
help
=
"
Build
with
the
given
mozconfig
.
"
    
)
    
def
build_shell
(
self
*
*
kwargs
)
:
        
"
"
"
Build
a
JS
shell
to
use
to
run
the
rooting
hazard
analysis
.
"
"
"
        
default_mozconfig
=
"
js
/
src
/
devtools
/
rootAnalysis
/
mozconfig
.
haz_shell
"
        
mozconfig_path
=
(
            
kwargs
.
pop
(
"
mozconfig
"
None
)
            
or
os
.
environ
.
get
(
"
MOZCONFIG
"
)
            
or
default_mozconfig
        
)
        
mozconfig_path
=
os
.
path
.
join
(
self
.
topsrcdir
mozconfig_path
)
        
loader
=
MozconfigLoader
(
self
.
topsrcdir
)
        
mozconfig
=
loader
.
read_mozconfig
(
mozconfig_path
)
        
configure_args
=
mozconfig
[
"
configure_args
"
]
        
if
"
-
-
enable
-
ctypes
"
not
in
configure_args
:
            
raise
FailedCommandError
(
                
"
ctypes
required
in
hazard
JS
shell
mozconfig
=
"
+
mozconfig_path
            
)
        
os
.
environ
[
"
MOZCONFIG
"
]
=
mozconfig_path
        
self
.
setup_env_for_tools
(
os
.
environ
)
        
os
.
environ
.
setdefault
(
            
"
MOZ_OBJDIR
"
os
.
path
.
join
(
self
.
topsrcdir
"
obj
-
haz
-
shell
"
)
        
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
build
"
self
.
_mach_context
*
*
kwargs
        
)
    
def
check_application
(
self
requested_app
objdir
=
None
)
:
        
"
"
"
Verify
that
the
objdir
and
work
dir
are
for
the
expected
application
"
"
"
        
try
:
            
work_dir
=
self
.
work_dir
(
requested_app
)
            
filename
=
os
.
path
.
join
(
work_dir
"
app
.
json
"
)
            
work_dir_app
=
self
.
read_json_file
(
filename
)
[
"
application
"
]
            
if
work_dir_app
!
=
requested_app
:
                
raise
FailedCommandError
(
                    
"
work
dir
{
}
is
for
the
wrong
app
{
}
"
.
format
(
work_dir
work_dir_app
)
                
)
        
except
IOError
:
            
pass
        
try
:
            
if
not
objdir
:
                
objdir
=
self
.
topobjdir
            
mozinfo
=
self
.
read_json_file
(
os
.
path
.
join
(
objdir
"
mozinfo
.
json
"
)
)
            
if
mozinfo
.
get
(
"
buildapp
"
)
!
=
requested_app
:
                
raise
FailedCommandError
(
                    
"
objdir
{
}
is
for
the
wrong
app
{
}
clobber
required
"
.
format
(
                        
objdir
mozinfo
.
get
(
"
buildapp
"
)
                    
)
                
)
        
except
(
OSError
IOError
)
:
            
pass
    
def
read_json_file
(
self
filename
)
:
        
with
open
(
filename
)
as
fh
:
            
return
json
.
load
(
fh
)
    
def
ensure_shell
(
self
objdir
)
:
        
try
:
            
binaries
=
self
.
read_json_file
(
os
.
path
.
join
(
objdir
"
binaries
.
json
"
)
)
            
info
=
[
b
for
b
in
binaries
[
"
programs
"
]
if
b
[
"
program
"
]
=
=
"
js
"
]
[
0
]
            
return
os
.
path
.
join
(
objdir
info
[
"
install_target
"
]
"
js
"
)
        
except
(
OSError
KeyError
)
:
            
raise
FailedCommandError
(
                
"
"
"
\
no
shell
found
in
%
s
-
-
must
build
the
JS
shell
with
mach
hazards
build
-
shell
first
"
"
"
                
%
objdir
            
)
    
inherit_command_args
(
"
build
"
)
    
SubCommand
(
        
"
hazards
"
        
"
gather
"
        
description
=
"
Gather
analysis
data
by
compiling
the
given
application
"
    
)
    
CommandArgument
(
        
"
-
-
application
"
default
=
"
browser
"
help
=
"
Build
the
given
application
.
"
    
)
    
CommandArgument
(
        
"
-
-
shell
-
objdir
"
        
default
=
"
"
        
help
=
"
objdir
containing
the
optimized
JS
shell
for
running
the
analysis
.
"
    
)
    
def
gather_hazard_data
(
self
application
shell_objdir
)
:
        
"
"
"
Gather
analysis
information
by
compiling
the
tree
"
"
"
        
if
shell_objdir
=
=
"
"
:
            
shell_objdir
=
os
.
path
.
join
(
self
.
topsrcdir
"
obj
-
haz
-
shell
"
)
        
shell_path
=
self
.
ensure_shell
(
shell_objdir
)
        
objdir
=
os
.
path
.
join
(
self
.
topsrcdir
"
obj
-
analyzed
-
"
+
application
)
        
self
.
check_application
(
application
objdir
)
        
with
open
(
os
.
path
.
join
(
work_dir
"
app
.
json
"
)
"
wt
"
)
as
fh
:
            
json
.
dump
(
{
"
application
"
:
application
}
fh
)
        
work_dir
=
self
.
work_dir
(
application
kwargs
[
"
work_dir
"
]
)
        
self
.
ensure_dir_exists
(
work_dir
)
        
with
open
(
os
.
path
.
join
(
work_dir
"
defaults
.
py
"
)
"
wt
"
)
as
fh
:
            
data
=
textwrap
.
dedent
(
                
"
"
"
\
                
js
=
"
{
js
}
"
                
analysis_scriptdir
=
"
{
script_dir
}
"
                
objdir
=
"
{
objdir
}
"
                
source
=
"
{
srcdir
}
"
                
sixgill
=
"
{
sixgill_dir
}
/
usr
/
libexec
/
sixgill
"
                
sixgill_bin
=
"
{
sixgill_dir
}
/
usr
/
bin
"
                
gcc_bin
=
"
{
gcc_dir
}
/
bin
"
            
"
"
"
            
)
.
format
(
                
js
=
shell_path
                
script_dir
=
self
.
script_dir
                
objdir
=
objdir
                
srcdir
=
self
.
topsrcdir
                
sixgill_dir
=
self
.
sixgill_dir
                
gcc_dir
=
self
.
gcc_dir
            
)
            
fh
.
write
(
data
)
        
buildscript
=
"
{
srcdir
}
/
mach
hazards
compile
-
-
application
=
{
app
}
"
.
format
(
            
srcdir
=
self
.
topsrcdir
app
=
application
        
)
        
args
=
[
            
os
.
path
.
join
(
self
.
script_dir
"
analyze
.
py
"
)
            
"
dbs
"
            
"
-
-
upto
"
            
"
dbs
"
            
"
-
v
"
            
"
-
-
buildcommand
=
"
+
buildscript
        
]
        
return
self
.
run_process
(
args
=
args
cwd
=
work_dir
pass_thru
=
True
)
    
inherit_command_args
(
"
build
"
)
    
SubCommand
(
"
hazards
"
"
compile
"
description
=
argparse
.
SUPPRESS
)
    
CommandArgument
(
        
"
-
-
mozconfig
"
        
default
=
None
        
metavar
=
"
FILENAME
"
        
help
=
"
Build
with
the
given
mozconfig
.
"
    
)
    
CommandArgument
(
        
"
-
-
application
"
default
=
"
browser
"
help
=
"
Build
the
given
application
.
"
    
)
    
def
inner_compile
(
self
*
*
kwargs
)
:
        
"
"
"
Build
a
source
tree
and
gather
analysis
information
while
running
        
under
the
influence
of
the
analysis
collection
server
.
"
"
"
        
env
=
os
.
environ
        
if
"
XGILL_CONFIG
"
not
in
env
:
            
raise
Exception
(
                
"
no
sixgill
manager
detected
.
mach
hazards
compile
"
                
+
"
should
only
be
run
from
mach
hazards
gather
"
            
)
        
app
=
kwargs
.
pop
(
"
application
"
)
        
default_mozconfig
=
"
js
/
src
/
devtools
/
rootAnalysis
/
mozconfig
.
%
s
"
%
app
        
mozconfig_path
=
(
            
kwargs
.
pop
(
"
mozconfig
"
None
)
or
env
.
get
(
"
MOZCONFIG
"
)
or
default_mozconfig
        
)
        
mozconfig_path
=
os
.
path
.
join
(
self
.
topsrcdir
mozconfig_path
)
        
loader
=
MozconfigLoader
(
self
.
topsrcdir
)
        
mozconfig
=
loader
.
read_mozconfig
(
mozconfig_path
)
        
self
.
check_application
(
app
mozconfig
[
"
topobjdir
"
]
)
        
configure_args
=
mozconfig
[
"
configure_args
"
]
        
if
"
-
-
enable
-
application
=
%
s
"
%
app
not
in
configure_args
:
            
raise
Exception
(
"
mozconfig
%
s
builds
wrong
project
"
%
mozconfig_path
)
        
if
not
any
(
"
-
-
with
-
compiler
-
wrapper
"
in
a
for
a
in
configure_args
)
:
            
raise
Exception
(
"
mozconfig
must
wrap
compiles
"
)
        
env
[
"
MOZCONFIG
"
]
=
os
.
path
.
join
(
self
.
topsrcdir
mozconfig_path
)
        
env
[
"
MOZBUILD_STATE_PATH
"
]
=
self
.
state_dir
        
self
.
setup_env_for_tools
(
env
)
        
if
"
haz_objdir
"
in
kwargs
:
            
env
[
"
MOZ_OBJDIR
"
]
=
kwargs
.
pop
(
"
haz_objdir
"
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
build
"
self
.
_mach_context
*
*
kwargs
        
)
    
SubCommand
(
        
"
hazards
"
"
analyze
"
description
=
"
Analyzed
gathered
data
for
rooting
hazards
"
    
)
    
CommandArgument
(
        
"
-
-
application
"
        
default
=
"
browser
"
        
help
=
"
Analyze
the
output
for
the
given
application
.
"
    
)
    
def
analyze
(
self
application
)
:
        
"
"
"
Analyzed
gathered
data
for
rooting
hazards
"
"
"
        
args
=
[
            
os
.
path
.
join
(
self
.
script_dir
"
analyze
.
py
"
)
            
"
gcTypes
"
            
"
-
v
"
        
]
        
return
self
.
run_process
(
            
args
=
args
cwd
=
self
.
work_dir
(
application
)
pass_thru
=
True
        
)
