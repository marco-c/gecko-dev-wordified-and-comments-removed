from
__future__
import
absolute_import
print_function
unicode_literals
import
argparse
import
logging
import
os
import
subprocess
from
mozbuild
.
base
import
MachCommandBase
from
mozbuild
.
build_commands
import
Build
from
mozfile
import
which
from
mach
.
decorators
import
CommandArgument
CommandProvider
Command
import
mozpack
.
path
as
mozpath
CommandProvider
class
MachCommands
(
MachCommandBase
)
:
    
Command
(
        
"
ide
"
        
category
=
"
devenv
"
        
description
=
"
Generate
a
project
and
launch
an
IDE
.
"
        
virtualenv_name
=
"
build
"
    
)
    
CommandArgument
(
"
ide
"
choices
=
[
"
eclipse
"
"
visualstudio
"
"
vscode
"
]
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
run
(
self
command_context
ide
args
)
:
        
if
ide
=
=
"
eclipse
"
:
            
backend
=
"
CppEclipse
"
        
elif
ide
=
=
"
visualstudio
"
:
            
backend
=
"
VisualStudio
"
        
elif
ide
=
=
"
vscode
"
:
            
backend
=
"
Clangd
"
        
if
ide
=
=
"
eclipse
"
and
not
which
(
"
eclipse
"
)
:
            
command_context
.
log
(
                
logging
.
ERROR
                
"
ide
"
                
{
}
                
"
Eclipse
CDT
8
.
4
or
later
must
be
installed
in
your
PATH
.
"
            
)
            
command_context
.
log
(
                
logging
.
ERROR
                
"
ide
"
                
{
}
                
"
Download
:
http
:
/
/
www
.
eclipse
.
org
/
cdt
/
downloads
.
php
"
            
)
            
return
1
        
if
ide
=
=
"
vscode
"
:
            
vscode_cmd
=
self
.
find_vscode_cmd
(
command_context
)
            
if
vscode_cmd
is
None
:
                
choice
=
prompt_bool
(
                    
"
VSCode
cannot
be
found
and
may
not
be
installed
.
Proceed
?
"
                
)
                
if
not
choice
:
                    
return
1
            
build_commands
=
Build
(
command_context
.
_mach_context
None
)
            
rc
=
build_commands
.
configure
(
command_context
)
            
if
rc
!
=
0
:
                
return
rc
            
rc
=
command_context
.
_run_make
(
                
directory
=
command_context
.
topobjdir
                
target
=
"
pre
-
export
"
                
line_handler
=
None
            
)
            
if
rc
!
=
0
:
                
return
rc
            
for
target
in
(
"
export
"
"
pre
-
compile
"
)
:
                
rc
=
command_context
.
_run_make
(
                    
directory
=
command_context
.
topobjdir
                    
target
=
target
                    
line_handler
=
None
                
)
                
if
rc
!
=
0
:
                    
return
rc
        
else
:
            
res
=
command_context
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
command_context
.
_mach_context
            
)
            
if
res
!
=
0
:
                
return
1
        
python
=
command_context
.
virtualenv_manager
.
python_path
        
config_status
=
os
.
path
.
join
(
command_context
.
topobjdir
"
config
.
status
"
)
        
args
=
[
python
config_status
"
-
-
backend
=
%
s
"
%
backend
]
        
res
=
command_context
.
_run_command_in_objdir
(
            
args
=
args
pass_thru
=
True
ensure_exit_code
=
False
        
)
        
if
res
!
=
0
:
            
return
1
        
if
ide
=
=
"
eclipse
"
:
            
eclipse_workspace_dir
=
self
.
get_eclipse_workspace_path
(
command_context
)
            
subprocess
.
check_call
(
[
"
eclipse
"
"
-
data
"
eclipse_workspace_dir
]
)
        
elif
ide
=
=
"
visualstudio
"
:
            
visual_studio_workspace_dir
=
self
.
get_visualstudio_workspace_path
(
                
command_context
            
)
            
subprocess
.
call
(
[
"
explorer
.
exe
"
visual_studio_workspace_dir
]
)
        
elif
ide
=
=
"
vscode
"
:
            
return
self
.
setup_vscode
(
command_context
vscode_cmd
)
    
def
get_eclipse_workspace_path
(
self
command_context
)
:
        
from
mozbuild
.
backend
.
cpp_eclipse
import
CppEclipseBackend
        
return
CppEclipseBackend
.
get_workspace_path
(
            
command_context
.
topsrcdir
command_context
.
topobjdir
        
)
    
def
get_visualstudio_workspace_path
(
self
command_context
)
:
        
return
os
.
path
.
normpath
(
            
os
.
path
.
join
(
command_context
.
topobjdir
"
msvc
"
"
mozilla
.
sln
"
)
        
)
    
def
find_vscode_cmd
(
self
command_context
)
:
        
import
shutil
        
path
=
shutil
.
which
(
"
code
"
)
        
if
path
is
not
None
:
            
return
[
path
]
        
if
"
linux
"
in
command_context
.
platform
[
0
]
:
            
cmd_and_path
=
[
                
{
"
path
"
:
"
/
usr
/
local
/
bin
/
code
"
"
cmd
"
:
[
"
/
usr
/
local
/
bin
/
code
"
]
}
                
{
"
path
"
:
"
/
snap
/
bin
/
code
"
"
cmd
"
:
[
"
/
snap
/
bin
/
code
"
]
}
                
{
"
path
"
:
"
/
usr
/
bin
/
code
"
"
cmd
"
:
[
"
/
usr
/
bin
/
code
"
]
}
                
{
"
path
"
:
"
/
usr
/
bin
/
code
-
insiders
"
"
cmd
"
:
[
"
/
usr
/
bin
/
code
-
insiders
"
]
}
            
]
        
elif
"
macos
"
in
command_context
.
platform
[
0
]
:
            
cmd_and_path
=
[
                
{
"
path
"
:
"
/
usr
/
local
/
bin
/
code
"
"
cmd
"
:
[
"
/
usr
/
local
/
bin
/
code
"
]
}
                
{
                    
"
path
"
:
"
/
Applications
/
Visual
Studio
Code
.
app
"
                    
"
cmd
"
:
[
"
open
"
"
/
Applications
/
Visual
Studio
Code
.
app
"
"
-
-
args
"
]
                
}
                
{
                    
"
path
"
:
"
/
Applications
/
Visual
Studio
Code
-
Insiders
.
app
"
                    
"
cmd
"
:
[
                        
"
open
"
                        
"
/
Applications
/
Visual
Studio
Code
-
Insiders
.
app
"
                        
"
-
-
args
"
                    
]
                
}
            
]
        
elif
"
win64
"
in
command_context
.
platform
[
0
]
:
            
from
pathlib
import
Path
            
vscode_path
=
mozpath
.
join
(
                
str
(
Path
.
home
(
)
)
                
"
AppData
"
                
"
Local
"
                
"
Programs
"
                
"
Microsoft
VS
Code
"
                
"
Code
.
exe
"
            
)
            
vscode_insiders_path
=
mozpath
.
join
(
                
str
(
Path
.
home
(
)
)
                
"
AppData
"
                
"
Local
"
                
"
Programs
"
                
"
Microsoft
VS
Code
Insiders
"
                
"
Code
-
Insiders
.
exe
"
            
)
            
cmd_and_path
=
[
                
{
"
path
"
:
vscode_path
"
cmd
"
:
[
vscode_path
]
}
                
{
"
path
"
:
vscode_insiders_path
"
cmd
"
:
[
vscode_insiders_path
]
}
            
]
        
for
element
in
cmd_and_path
:
            
if
os
.
path
.
exists
(
element
[
"
path
"
]
)
:
                
return
element
[
"
cmd
"
]
        
return
None
    
def
setup_vscode
(
self
command_context
vscode_cmd
)
:
        
vscode_settings
=
mozpath
.
join
(
            
command_context
.
topsrcdir
"
.
vscode
"
"
settings
.
json
"
        
)
        
clangd_cc_path
=
mozpath
.
join
(
command_context
.
topobjdir
"
clangd
"
)
        
clang_tools_path
=
mozpath
.
join
(
            
command_context
.
_mach_context
.
state_dir
"
clang
-
tools
"
        
)
        
clang_tidy_bin
=
mozpath
.
join
(
clang_tools_path
"
clang
-
tidy
"
"
bin
"
)
        
clangd_path
=
mozpath
.
join
(
            
clang_tidy_bin
            
"
clangd
"
+
command_context
.
config_environment
.
substs
.
get
(
"
BIN_SUFFIX
"
"
"
)
        
)
        
if
not
os
.
path
.
exists
(
clangd_path
)
:
            
command_context
.
log
(
                
logging
.
ERROR
                
"
ide
"
                
{
}
                
"
Unable
to
locate
clangd
in
{
}
.
"
.
format
(
clang_tidy_bin
)
            
)
            
rc
=
self
.
_get_clang_tools
(
command_context
clang_tools_path
)
            
if
rc
!
=
0
:
                
return
rc
        
import
multiprocessing
        
import
json
        
import
difflib
        
from
mozbuild
.
code_analysis
.
utils
import
ClangTidyConfig
        
clang_tidy_cfg
=
ClangTidyConfig
(
command_context
.
topsrcdir
)
        
clangd_json
=
{
            
"
clangd
.
path
"
:
clangd_path
            
"
clangd
.
arguments
"
:
[
                
"
-
-
compile
-
commands
-
dir
"
                
clangd_cc_path
                
"
-
j
"
                
str
(
multiprocessing
.
cpu_count
(
)
/
/
2
)
                
"
-
-
limit
-
results
"
                
"
0
"
                
"
-
-
completion
-
style
"
                
"
detailed
"
                
"
-
-
background
-
index
"
                
"
-
-
all
-
scopes
-
completion
"
                
"
-
-
log
"
                
"
info
"
                
"
-
-
pch
-
storage
"
                
"
memory
"
                
"
-
-
clang
-
tidy
"
                
"
-
-
clang
-
tidy
-
checks
"
                
"
"
.
join
(
clang_tidy_cfg
.
checks
)
            
]
        
}
        
try
:
            
with
open
(
vscode_settings
)
as
fh
:
                
old_settings_str
=
fh
.
read
(
)
        
except
FileNotFoundError
:
            
print
(
"
Configuration
for
{
}
will
be
created
.
"
.
format
(
vscode_settings
)
)
            
old_settings_str
=
None
        
if
old_settings_str
is
None
:
            
with
open
(
vscode_settings
"
w
"
)
as
fh
:
                
json
.
dump
(
clangd_json
fh
indent
=
4
)
        
else
:
            
try
:
                
old_settings
=
json
.
loads
(
old_settings_str
)
                
prompt_prefix
=
"
"
            
except
ValueError
:
                
old_settings
=
{
}
                
prompt_prefix
=
(
                    
"
\
n
*
*
WARNING
*
*
:
Parsing
of
existing
settings
file
failed
.
"
                    
"
Existing
settings
will
be
lost
!
"
                
)
            
settings
=
{
*
*
old_settings
*
*
clangd_json
}
            
if
old_settings
!
=
settings
:
                
new_settings_str
=
json
.
dumps
(
settings
indent
=
4
)
                
print
(
                    
"
\
nThe
following
modifications
to
{
settings
}
will
occur
:
\
n
{
diff
}
"
.
format
(
                        
settings
=
vscode_settings
                        
diff
=
"
"
.
join
(
                            
difflib
.
unified_diff
(
                                
old_settings_str
.
splitlines
(
keepends
=
True
)
                                
new_settings_str
.
splitlines
(
keepends
=
True
)
                                
"
a
/
.
vscode
/
settings
.
json
"
                                
"
b
/
.
vscode
/
settings
.
json
"
                                
n
=
30
                            
)
                        
)
                    
)
                
)
                
choice
=
prompt_bool
(
                    
"
{
}
\
nProceed
with
modifications
to
{
}
?
"
.
format
(
                        
prompt_prefix
vscode_settings
                    
)
                
)
                
if
not
choice
:
                    
return
1
                
with
open
(
vscode_settings
"
w
"
)
as
fh
:
                    
fh
.
write
(
new_settings_str
)
        
if
vscode_cmd
is
None
:
            
print
(
                
"
Please
open
VS
Code
manually
and
load
directory
:
{
}
"
.
format
(
                    
command_context
.
topsrcdir
                
)
            
)
            
return
0
        
rc
=
subprocess
.
call
(
vscode_cmd
+
[
command_context
.
topsrcdir
]
)
        
if
rc
!
=
0
:
            
command_context
.
log
(
                
logging
.
ERROR
                
"
ide
"
                
{
}
                
"
Unable
to
open
VS
Code
.
Please
open
VS
Code
manually
and
load
"
                
"
directory
:
{
}
"
.
format
(
command_context
.
topsrcdir
)
            
)
            
return
rc
        
return
0
    
def
_get_clang_tools
(
self
command_context
clang_tools_path
)
:
        
import
shutil
        
if
os
.
path
.
isdir
(
clang_tools_path
)
:
            
shutil
.
rmtree
(
clang_tools_path
)
        
os
.
mkdir
(
clang_tools_path
)
        
from
mozbuild
.
artifact_commands
import
PackageFrontend
        
_artifact_manager
=
PackageFrontend
(
command_context
.
_mach_context
)
        
job
_
=
command_context
.
platform
        
if
job
is
None
:
            
command_context
.
log
(
                
logging
.
ERROR
                
"
ide
"
                
{
}
                
"
The
current
platform
isn
'
t
supported
.
"
                
"
Currently
only
the
following
platforms
are
"
                
"
supported
:
win32
/
win64
linux64
and
macosx64
.
"
            
)
            
return
1
        
job
+
=
"
-
clang
-
tidy
"
        
currentWorkingDir
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
clang_tools_path
)
        
rc
=
_artifact_manager
.
artifact_toolchain
(
            
command_context
verbose
=
False
from_build
=
[
job
]
no_unpack
=
False
retry
=
0
        
)
        
os
.
chdir
(
currentWorkingDir
)
        
return
rc
def
prompt_bool
(
prompt
limit
=
5
)
:
    
"
"
"
Prompts
the
user
with
prompt
and
requires
a
boolean
value
.
"
"
"
    
from
distutils
.
util
import
strtobool
    
for
_
in
range
(
limit
)
:
        
try
:
            
return
strtobool
(
input
(
prompt
+
"
[
Y
/
N
]
\
n
"
)
)
        
except
ValueError
:
            
print
(
                
"
ERROR
!
Please
enter
a
valid
option
!
Please
use
any
of
the
following
:
"
                
"
Y
N
True
False
1
0
"
            
)
    
return
False
