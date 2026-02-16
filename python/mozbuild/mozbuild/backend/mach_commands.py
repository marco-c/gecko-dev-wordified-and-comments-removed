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
ide
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
"
vscodium
"
"
zed
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
in
{
"
vscode
"
"
vscodium
"
"
zed
"
}
:
        
result
=
subprocess
.
run
(
            
[
sys
.
executable
"
mach
"
"
configure
"
]
            
check
=
False
            
cwd
=
command_context
.
topsrcdir
        
)
        
if
result
.
returncode
:
            
return
result
.
returncode
        
result
=
subprocess
.
run
(
            
[
sys
.
executable
"
mach
"
"
build
"
"
pre
-
export
"
"
export
"
"
pre
-
compile
"
]
            
check
=
False
            
cwd
=
command_context
.
topsrcdir
        
)
        
if
result
.
returncode
:
            
return
result
.
returncode
    
else
:
        
result
=
subprocess
.
run
(
            
[
sys
.
executable
"
mach
"
"
build
"
]
            
check
=
False
            
cwd
=
command_context
.
topsrcdir
        
)
        
if
result
.
returncode
:
            
return
result
.
returncode
    
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
in
{
"
vscode
"
"
vscodium
"
"
zed
"
}
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
backend
:
        
result
=
subprocess
.
run
(
            
[
sys
.
executable
"
mach
"
"
build
-
backend
"
"
-
b
"
backend
]
            
check
=
False
            
cwd
=
command_context
.
topsrcdir
        
)
        
if
result
.
returncode
:
            
return
result
.
returncode
    
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
in
{
"
vscode
"
"
vscodium
"
}
:
        
return
setup_vscode_or_vscodium
(
ide
command_context
interactive
)
    
elif
ide
=
=
"
zed
"
:
        
return
setup_zed
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
find_zed_cmd
(
)
:
    
for
variant
in
[
"
zed
"
"
zeditor
"
"
zedit
"
"
zed
-
editor
"
]
:
        
cmd
=
which
(
variant
)
        
if
cmd
:
            
return
cmd
    
return
None
def
setup_zed
(
command_context
interactive
)
:
    
try
:
        
import
json5
as
json
        
dump_extra
=
{
"
quote_keys
"
:
True
"
trailing_commas
"
:
False
}
    
except
ImportError
:
        
import
json
    
zed_cmd
=
find_zed_cmd
(
)
    
if
interactive
and
zed_cmd
is
None
:
        
choice
=
prompt_bool
(
"
Zed
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
    
print
(
"
Configuring
Zed
.
.
.
"
)
    
new_settings
=
{
}
    
if
not
command_context
.
config_environment
.
is_artifact_build
:
        
lsp_settings
=
{
}
        
for
key
value
in
setup_clangd_rust_in_vscode
(
command_context
)
.
items
(
)
:
            
key_chain
=
key
.
split
(
"
.
"
)
            
last_key
=
key_chain
[
-
1
]
            
section
=
(
                
"
binary
"
                
if
last_key
in
{
"
path
"
"
arguments
"
"
env
"
}
                
else
"
initialization_options
"
            
)
            
key_chain
.
insert
(
1
section
)
            
dest_dict
=
lsp_settings
            
for
k
in
key_chain
[
:
-
1
]
:
                
dest_dict
=
dest_dict
.
setdefault
(
k
{
}
)
            
dest_dict
[
last_key
]
=
value
        
rust_analyzer_binary_settings
=
lsp_settings
[
"
rust
-
analyzer
"
]
.
setdefault
(
            
"
binary
"
{
}
        
)
        
cargo_path
=
command_context
.
config_environment
.
substs
.
get
(
"
CARGO
"
)
        
rust_analyzer_path
=
mozpath
.
join
(
mozpath
.
dirname
(
cargo_path
)
"
rust
-
analyzer
"
)
        
if
os
.
path
.
exists
(
rust_analyzer_path
)
:
            
rust_analyzer_binary_settings
[
"
path
"
]
=
rust_analyzer_path
        
rust_analyzer_binary_env_settings
=
rust_analyzer_binary_settings
.
setdefault
(
            
"
env
"
{
}
        
)
        
for
env
in
[
"
CARGO
"
"
RUSTC
"
]
:
            
rust_analyzer_binary_env_settings
[
env
]
=
(
                
command_context
.
config_environment
.
substs
.
get
(
env
)
            
)
        
new_settings
[
"
lsp
"
]
=
lsp_settings
    
new_settings
[
"
languages
"
]
=
{
"
C
"
:
{
"
tab_size
"
:
2
}
"
C
+
+
"
:
{
"
tab_size
"
:
2
}
}
    
new_settings
[
"
file_types
"
]
=
{
        
"
Python
"
:
[
            
"
*
*
/
moz
.
build
"
            
"
*
*
/
*
.
configure
"
        
]
        
"
C
+
+
"
:
[
            
"
*
*
/
*
.
mm
"
        
]
    
}
    
zed_settings_dir
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
zed
"
)
    
zed_settings_file
=
mozpath
.
join
(
zed_settings_dir
"
settings
.
json
"
)
    
if
not
os
.
path
.
isdir
(
zed_settings_dir
)
:
        
os
.
mkdir
(
zed_settings_dir
)
    
old_settings
=
{
}
    
if
os
.
path
.
exists
(
zed_settings_file
)
:
        
try
:
            
with
open
(
zed_settings_file
)
as
fh
:
                
old_settings
=
json
.
load
(
fh
)
        
except
ValueError
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
                
f
"
Failed
to
parse
{
zed_settings_file
}
refusing
to
override
"
            
)
            
return
1
    
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
    
with
open
(
zed_settings_file
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
settings
fh
indent
=
4
*
*
dump_extra
)
    
if
interactive
and
zed_cmd
:
        
subprocess
.
call
(
[
zed_cmd
command_context
.
topsrcdir
]
)
def
rust_analyzer_config
(
command_context
)
:
    
rust_analyzer_extra_includes
=
[
command_context
.
topobjdir
]
    
if
windows_rs_dir
:
=
command_context
.
config_environment
.
substs
.
get
(
        
"
MOZ_WINDOWS_RS_DIR
"
    
)
:
        
rust_analyzer_extra_includes
.
append
(
windows_rs_dir
)
    
commtopsrcdir
=
command_context
.
substs
.
get
(
"
commtopsrcdir
"
)
    
if
commtopsrcdir
:
        
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
.
.
/
.
.
/
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
.
/
.
.
/
mach
"
]
    
elif
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
    
config
=
{
        
"
cargo
"
:
{
            
"
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
buildScripts
"
:
{
                
"
overrideCommand
"
:
cargo_check_command
            
}
        
}
        
"
vfs
"
:
{
            
"
extraIncludes
"
:
rust_analyzer_extra_includes
        
}
        
"
check
"
:
{
            
"
overrideCommand
"
:
cargo_check_command
        
}
    
}
    
if
commtopsrcdir
:
        
config
[
"
linkedProjects
"
]
=
[
os
.
path
.
join
(
commtopsrcdir
"
rust
"
"
Cargo
.
toml
"
)
]
    
return
config
def
setup_vscode_or_vscodium
(
ide
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
find_vscode_or_vscodium_cmd
    
if
interactive
:
        
vscode_cmd
=
find_vscode_or_vscodium_cmd
(
ide
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
        
return_value
=
setup_clangd_rust_in_vscode
(
command_context
)
        
if
isinstance
(
return_value
int
)
:
            
return
return_value
        
new_settings
=
return_value
    
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
sjs
"
:
"
javascript
"
        
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
    
prettier_languages
=
[
        
"
javascript
"
        
"
javascriptreact
"
        
"
typescript
"
        
"
typescriptreact
"
        
"
json
"
        
"
jsonc
"
        
"
html
"
        
"
css
"
    
]
    
for
lang
in
prettier_languages
:
        
new_settings
[
f
"
[
{
lang
}
]
"
]
=
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
    
new_settings
=
{
        
*
*
new_settings
        
"
terminalLinks
.
matchers
"
:
[
            
{
                
"
regex
"
:
"
\
\
b
[
Bb
]
ug
\
\
s
*
(
\
\
d
+
)
\
\
b
"
                
"
uri
"
:
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
show_bug
.
cgi
?
id
=
1
"
            
}
            
{
                
"
regex
"
:
"
\
\
b
(
D
\
\
d
+
)
\
\
b
"
                
"
uri
"
:
"
https
:
/
/
phabricator
.
services
.
mozilla
.
com
/
1
"
            
}
            
{
                
"
regex
"
:
"
\
\
bmoz
-
src
:
/
/
\
\
w
*
/
(
[
^
\
\
s
:
\
"
'
\
\
)
\
\
}
\
\
]
>
]
+
)
(
?
:
[
\
\
s
:
\
"
'
]
+
)
(
\
\
d
+
)
"
                
"
uri
"
:
"
vscode
:
/
/
file
{
workspaceFolder
}
/
1
:
2
"
            
}
            
{
                
"
regex
"
:
"
\
\
bmoz
-
src
:
/
/
\
\
w
*
/
(
[
^
\
\
s
:
\
"
'
\
\
)
\
\
}
\
\
]
>
]
+
)
"
                
"
uri
"
:
"
vscode
:
/
/
file
{
workspaceFolder
}
/
1
"
            
}
        
]
    
}
    
import
difflib
    
try
:
        
import
json5
as
json
        
dump_extra
=
{
"
quote_keys
"
:
True
"
trailing_commas
"
:
False
}
    
except
ImportError
:
        
import
json
        
dump_extra
=
{
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
f
"
Configuration
for
{
vscode_settings
}
will
be
created
.
{
artifact_prefix
}
"
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
*
*
dump_extra
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
            
"
rust
-
analyzer
.
server
.
extraEnv
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
*
*
dump_extra
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
                    
f
"
{
artifact_prefix
}
{
prompt_prefix
}
\
nProceed
with
modifications
to
{
vscode_settings
}
?
"
                
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
            
f
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
command_context
.
topsrcdir
}
"
        
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
            
f
"
directory
:
{
command_context
.
topsrcdir
}
"
        
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
HOST_BIN_SUFFIX
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
        
from
mozbuild
.
bootstrap
import
bootstrap_toolchain
        
bootstrap_toolchain
(
"
clang
-
tools
/
clang
-
tidy
"
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
                
f
"
Unable
to
locate
clangd
in
{
clang_tidy_bin
}
.
"
            
)
            
return
1
    
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
    
config
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
    
}
    
rust_analyzer_cfg
=
rust_analyzer_config
(
command_context
)
    
def
add_flattened_keys
(
prefix
d
)
:
        
for
key
value
in
d
.
items
(
)
:
            
full_key
=
f
"
{
prefix
}
.
{
key
}
"
            
if
isinstance
(
value
dict
)
:
                
add_flattened_keys
(
full_key
value
)
            
else
:
                
config
[
full_key
]
=
value
    
add_flattened_keys
(
"
rust
-
analyzer
"
rust_analyzer_cfg
)
    
return
config
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
Command
(
    
"
rust
-
analyzer
-
config
"
    
category
=
"
devenv
"
    
description
=
"
Output
rust
-
analyzer
configuration
in
json
format
.
"
    
virtualenv_name
=
"
common
"
)
CommandArgument
(
"
-
-
output
"
"
-
o
"
type
=
str
help
=
"
Output
to
the
given
file
.
"
)
def
rust_analyzer_config_cmd
(
command_context
output
)
:
    
import
json
    
config
=
rust_analyzer_config
(
command_context
)
    
result
=
json
.
dumps
(
config
indent
=
2
)
    
if
output
:
        
with
open
(
output
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
result
)
    
else
:
        
print
(
result
)
