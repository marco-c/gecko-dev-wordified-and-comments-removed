import
argparse
import
logging
import
os
import
subprocess
import
sys
import
mozpack
.
path
as
mozpath
from
mach
.
decorators
import
Command
CommandArgument
from
mozfile
import
which
from
mozbuild
import
build_commands
from
mozbuild
.
util
import
cpu_count
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
-
-
no
-
interactive
"
    
default
=
False
    
action
=
"
store_true
"
    
help
=
"
Just
generate
the
configuration
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
run
(
command_context
ide
no_interactive
args
)
:
    
interactive
=
not
no_interactive
    
backend
=
None
    
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
        
if
not
command_context
.
config_environment
.
is_artifact_build
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
    
if
backend
:
        
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
setup_vscode
(
command_context
interactive
)
def
get_eclipse_workspace_path
(
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
setup_vscode
(
command_context
interactive
)
:
    
from
mozbuild
.
backend
.
clangd
import
find_vscode_cmd
    
if
interactive
:
        
vscode_cmd
=
find_vscode_cmd
(
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
    
new_settings
=
{
}
    
artifact_prefix
=
"
"
    
if
command_context
.
config_environment
.
is_artifact_build
:
        
artifact_prefix
=
(
            
"
\
nArtifact
build
configured
:
Skipping
clang
and
rust
setup
.
"
            
"
If
you
later
switch
to
a
full
build
please
re
-
run
this
command
.
"
        
)
    
else
:
        
new_settings
=
setup_clangd_rust_in_vscode
(
command_context
)
    
relobjdir
=
mozpath
.
relpath
(
command_context
.
topobjdir
command_context
.
topsrcdir
)
    
new_settings
=
{
        
*
*
new_settings
        
"
files
.
associations
"
:
{
            
"
*
.
jsm
"
:
"
javascript
"
            
"
*
.
sjs
"
:
"
javascript
"
        
}
        
"
[
javascript
]
[
javascriptreact
]
[
typescript
]
[
typescriptreact
]
[
json
]
[
jsonc
]
[
html
]
"
:
{
            
"
editor
.
defaultFormatter
"
:
"
esbenp
.
prettier
-
vscode
"
            
"
editor
.
formatOnSave
"
:
True
        
}
        
"
files
.
exclude
"
:
{
"
obj
-
*
"
:
True
relobjdir
:
True
}
        
"
files
.
watcherExclude
"
:
{
"
obj
-
*
"
:
True
relobjdir
:
True
}
    
}
    
import
difflib
    
import
json
    
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
{
}
"
.
format
(
                
vscode_settings
artifact_prefix
            
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
new_settings
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
        
deprecated
=
[
            
"
[
javascript
]
[
javascriptreact
]
[
typescript
]
[
typescriptreact
]
"
            
"
[
javascript
]
[
javascriptreact
]
[
typescript
]
[
typescriptreact
]
[
json
]
"
            
"
[
javascript
]
[
javascriptreact
]
[
typescript
]
[
typescriptreact
]
[
json
]
[
html
]
"
        
]
        
for
entry
in
deprecated
:
            
if
entry
in
old_settings
:
                
old_settings
.
pop
(
entry
)
        
settings
=
{
*
*
old_settings
*
*
new_settings
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
            
if
interactive
:
                
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
                        
artifact_prefix
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
not
interactive
:
        
return
0
    
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
setup_clangd_rust_in_vscode
(
command_context
)
:
    
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
get_clang_tools
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
    
if
sys
.
platform
=
=
"
win32
"
:
        
cargo_check_command
=
[
sys
.
executable
"
mach
"
]
    
else
:
        
cargo_check_command
=
[
"
.
/
mach
"
]
    
cargo_check_command
+
=
[
        
"
-
-
log
-
no
-
times
"
        
"
cargo
"
        
"
check
"
        
"
-
j
"
        
str
(
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
all
-
crates
"
        
"
-
-
message
-
format
-
json
"
    
]
    
clang_tidy
=
{
}
    
clang_tidy
[
"
Checks
"
]
=
"
"
.
join
(
clang_tidy_cfg
.
checks
)
    
clang_tidy
.
update
(
clang_tidy_cfg
.
checks_config
)
    
import
yaml
    
with
open
(
"
.
clang
-
tidy
"
"
w
"
)
as
file
:
        
yaml
.
dump
(
clang_tidy
file
)
    
clangd_cfg
=
{
        
"
CompileFlags
"
:
{
            
"
CompilationDatabase
"
:
clangd_cc_path
        
}
    
}
    
with
open
(
"
.
clangd
"
"
w
"
)
as
file
:
        
yaml
.
dump
(
clangd_cfg
file
)
    
return
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
j
"
            
str
(
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
disk
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
header
-
insertion
=
never
"
        
]
        
"
rust
-
analyzer
.
server
.
extraEnv
"
:
{
            
"
CARGO_TARGET_DIR
"
:
command_context
.
topobjdir
        
}
        
"
rust
-
analyzer
.
cargo
.
buildScripts
.
overrideCommand
"
:
cargo_check_command
        
"
rust
-
analyzer
.
check
.
overrideCommand
"
:
cargo_check_command
    
}
def
get_clang_tools
(
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
artifact_toolchain
    
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
mach
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
