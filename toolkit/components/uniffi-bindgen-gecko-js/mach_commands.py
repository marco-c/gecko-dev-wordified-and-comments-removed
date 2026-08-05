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
textwrap
from
collections
import
namedtuple
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
SubCommand
from
mozbuild
.
backend
.
configenvironment
import
ConfigEnvironment
from
mozbuild
.
util
import
get_rust_build_kind
from
mozpack
.
copier
import
FileCopier
from
mozpack
.
files
import
FileFinder
CPP_PATH
=
"
toolkit
/
components
/
uniffi
-
js
/
GeneratedScaffolding
.
cpp
"
JS_DIR
=
"
toolkit
/
components
/
uniffi
-
bindgen
-
gecko
-
js
/
components
/
generated
"
FIXTURE_JS_DIR
=
"
toolkit
/
components
/
uniffi
-
bindgen
-
gecko
-
js
/
tests
/
generated
"
DOCS_PATH
=
"
docs
/
rust
-
components
/
api
/
js
/
"
UniffiTargets
=
namedtuple
(
    
"
UniffiTargets
"
    
[
        
"
binary_path
"
        
"
library_path
"
        
"
fixtures_library_path
"
        
"
embedded_uniffi_bindgen_path
"
        
"
megazord_path
"
    
]
)
def
_uniffi_objdir
(
topsrcdir
)
:
    
return
mozpath
.
join
(
topsrcdir
"
obj
-
uniffi
-
generate
"
)
def
_ensure_uniffi_mozconfig
(
uniffi_objdir
)
:
    
if
not
os
.
path
.
isdir
(
uniffi_objdir
)
:
        
os
.
makedirs
(
uniffi_objdir
)
    
mozconfig_path
=
mozpath
.
join
(
uniffi_objdir
"
mozconfig
"
)
    
contents
=
textwrap
.
dedent
(
        
f
"
"
"
\
        
ac_add_options
-
-
enable
-
application
=
browser
        
ac_add_options
-
-
enable
-
appservices
-
in
-
tree
        
mk_add_options
MOZ_OBJDIR
=
{
uniffi_objdir
}
        
"
"
"
    
)
    
if
os
.
path
.
isfile
(
mozconfig_path
)
:
        
with
open
(
mozconfig_path
encoding
=
"
utf
-
8
"
)
as
f
:
            
if
f
.
read
(
)
=
=
contents
:
                
return
mozconfig_path
    
with
open
(
mozconfig_path
"
w
"
encoding
=
"
utf
-
8
"
)
as
f
:
        
f
.
write
(
contents
)
    
return
mozconfig_path
def
build_uniffi_targets
(
command_context
)
:
    
uniffi_objdir
=
_uniffi_objdir
(
command_context
.
topsrcdir
)
    
mozconfig_path
=
_ensure_uniffi_mozconfig
(
uniffi_objdir
)
    
command_context
.
log
(
        
logging
.
WARNING
        
"
uniffi
-
generate
"
        
{
"
objdir
"
:
uniffi_objdir
}
        
"
Using
dedicated
uniffi
objdir
:
{
objdir
}
"
    
)
    
env
=
os
.
environ
.
copy
(
)
    
env
[
"
MOZCONFIG
"
]
=
mozconfig_path
    
mach_path
=
mozpath
.
join
(
command_context
.
topsrcdir
"
mach
"
)
    
subprocess
.
check_call
(
        
[
sys
.
executable
mach_path
"
configure
"
]
        
env
=
env
        
cwd
=
command_context
.
topsrcdir
    
)
    
subprocess
.
check_call
(
        
[
            
sys
.
executable
            
mach_path
            
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
recurse_uniffi
-
target
"
        
]
        
env
=
env
        
cwd
=
command_context
.
topsrcdir
    
)
    
config
=
ConfigEnvironment
.
from_config_status
(
        
mozpath
.
join
(
uniffi_objdir
"
config
.
status
"
)
    
)
    
substs
=
config
.
substs
    
rust_build_kind
=
get_rust_build_kind
(
substs
)
    
binary_path
=
mozpath
.
join
(
        
uniffi_objdir
"
dist
"
"
host
"
"
bin
"
"
uniffi
-
bindgen
-
gecko
-
js
"
    
)
    
lib_prefix
=
substs
[
"
LIB_PREFIX
"
]
    
lib_suffix
=
substs
[
"
LIB_SUFFIX
"
]
    
library_path
=
mozpath
.
join
(
        
uniffi_objdir
        
substs
[
"
RUST_TARGET
"
]
        
rust_build_kind
        
f
"
{
lib_prefix
}
gkrust_uniffi_components
.
{
lib_suffix
}
"
    
)
    
fixtures_library_path
=
mozpath
.
join
(
        
uniffi_objdir
        
substs
[
"
RUST_TARGET
"
]
        
rust_build_kind
        
f
"
{
lib_prefix
}
uniffi_bindgen_gecko_js_test_fixtures
.
{
lib_suffix
}
"
    
)
    
embedded_uniffi_bindgen_path
=
mozpath
.
join
(
        
uniffi_objdir
        
"
dist
"
        
"
host
"
        
"
bin
"
        
f
"
embedded
-
uniffi
-
bindgen
{
substs
[
'
HOST_BIN_SUFFIX
'
]
}
"
    
)
    
if
substs
.
get
(
"
OS_ARCH
"
)
=
=
"
WINNT
"
:
        
megazord_build_kind
=
get_rust_build_kind
(
substs
megazord
=
True
)
        
megazord_path
=
mozpath
.
join
(
            
uniffi_objdir
            
substs
[
"
RUST_TARGET
"
]
            
megazord_build_kind
            
f
"
{
lib_prefix
}
megazord
.
{
lib_suffix
}
"
        
)
    
else
:
        
dll_prefix
=
substs
[
"
DLL_PREFIX
"
]
        
dll_suffix
=
substs
[
"
DLL_SUFFIX
"
]
        
megazord_path
=
mozpath
.
join
(
            
uniffi_objdir
            
"
dist
"
            
"
bin
"
            
f
"
{
dll_prefix
}
megazord
{
dll_suffix
}
"
        
)
    
return
UniffiTargets
(
        
binary_path
=
binary_path
        
library_path
=
library_path
        
fixtures_library_path
=
fixtures_library_path
        
embedded_uniffi_bindgen_path
=
embedded_uniffi_bindgen_path
        
megazord_path
=
megazord_path
    
)
COMPONENT_MAPPING
=
{
    
"
mozilla
/
appservices
/
adsclient
"
:
"
components
/
ads
-
client
"
    
"
mozilla
/
appservices
/
autofill
"
:
"
components
/
autofill
"
    
"
mozilla
/
appservices
/
crashtest
"
:
"
components
/
crashtest
"
    
"
mozilla
/
appservices
/
errorsupport
"
:
"
components
/
errorsupport
"
    
"
mozilla
/
appservices
/
fxaclient
"
:
"
components
/
fxaclient
"
    
"
mozilla
/
appservices
/
init_rust_components
"
:
"
components
/
init_rust_components
"
    
"
mozilla
/
appservices
/
logins
"
:
"
components
/
logins
"
    
"
mozilla
/
appservices
/
merino
"
:
"
components
/
merino
"
    
"
mozilla
/
appservices
/
places
"
:
"
components
/
places
"
    
"
mozilla
/
appservices
/
push
"
:
"
components
/
push
"
    
"
mozilla
/
appservices
/
relay
"
:
"
components
/
relay
"
    
"
mozilla
/
appservices
/
remotesettings
"
:
"
components
/
remotesettings
"
    
"
mozilla
/
appservices
/
remotetabs
"
:
"
components
/
tabs
"
    
"
mozilla
/
appservices
/
rust_log_forwarder
"
:
"
components
/
rust
-
log
-
forwarder
"
    
"
mozilla
/
appservices
/
search
"
:
"
components
/
search
"
    
"
mozilla
/
appservices
/
suggest
"
:
"
components
/
suggest
"
    
"
mozilla
/
appservices
/
sync15
"
:
"
components
/
sync15
"
    
"
mozilla
/
appservices
/
syncmanager
"
:
"
components
/
syncmanager
"
    
"
mozilla
/
appservices
/
tracing
"
:
"
components
/
tracing
"
    
"
mozilla
/
appservices
/
viaduct
"
:
"
components
/
viaduct
"
    
"
org
/
mozilla
/
experiments
/
nimbus
"
:
"
components
/
nimbus
"
}
def
generate_android
(
command_context
uniffi_targets
)
:
    
uniffi_objdir
=
_uniffi_objdir
(
command_context
.
topsrcdir
)
    
android_objdir
=
mozpath
.
join
(
        
uniffi_objdir
"
toolkit
/
components
/
uniffi
-
bindgen
-
gecko
-
js
/
android
"
    
)
    
cmdline
=
[
        
uniffi_targets
.
embedded_uniffi_bindgen_path
        
"
generate
"
        
"
-
-
no
-
format
"
        
"
-
-
language
"
        
"
kotlin
"
        
"
-
-
out
-
dir
"
        
android_objdir
        
uniffi_targets
.
megazord_path
    
]
    
subprocess
.
check_call
(
cmdline
cwd
=
command_context
.
topsrcdir
)
    
copier
=
FileCopier
(
)
    
for
source_dir
target_component
in
COMPONENT_MAPPING
.
items
(
)
:
        
source_base
=
mozpath
.
join
(
android_objdir
source_dir
)
        
if
not
os
.
path
.
isdir
(
source_base
)
:
            
raise
Exception
(
                
f
"
COMPONENT_MAPPING
entry
'
{
source_dir
}
'
has
no
generated
bindings
"
                
f
"
at
'
{
source_base
}
'
.
The
mapping
is
out
of
sync
with
the
megazord
.
"
            
)
        
target_base
=
mozpath
.
join
(
            
target_component
            
"
android
/
src
/
main
/
java
"
            
source_dir
        
)
        
for
p
f
in
FileFinder
(
source_base
)
.
find
(
"
*
*
"
)
:
            
copier
.
add
(
mozpath
.
join
(
target_base
p
)
f
)
    
copier
.
copy
(
        
mozpath
.
join
(
            
command_context
.
topsrcdir
            
"
toolkit
/
components
/
uniffi
-
bindgen
-
gecko
-
js
/
android
"
        
)
    
)
Command
(
    
"
uniffi
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
JS
bindings
using
uniffi
-
bindgen
-
gecko
-
js
"
)
def
uniffi
(
command_context
*
runargs
*
*
lintargs
)
:
    
"
"
"
Run
uniffi
.
"
"
"
    
command_context
.
_sub_mach
(
[
"
help
"
"
uniffi
"
]
)
    
return
1
SubCommand
(
    
"
uniffi
"
    
"
generate
"
    
description
=
"
Generate
/
regenerate
bindings
"
)
def
generate_command
(
command_context
)
:
    
uniffi_targets
=
build_uniffi_targets
(
command_context
)
    
cmdline
=
[
        
uniffi_targets
.
binary_path
        
"
-
-
library
-
path
"
        
uniffi_targets
.
library_path
        
"
-
-
fixtures
-
library
-
path
"
        
uniffi_targets
.
fixtures_library_path
        
"
generate
"
        
"
-
-
js
-
dir
"
        
JS_DIR
        
"
-
-
fixture
-
js
-
dir
"
        
FIXTURE_JS_DIR
        
"
-
-
cpp
-
path
"
        
CPP_PATH
        
"
-
-
docs
-
path
"
        
DOCS_PATH
    
]
    
subprocess
.
check_call
(
cmdline
cwd
=
command_context
.
topsrcdir
)
    
generate_android
(
command_context
uniffi_targets
)
    
return
0
SubCommand
(
    
"
uniffi
"
    
"
pipeline
"
    
description
=
"
Inspect
UniFFI
bindings
pipeline
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
pipeline_command
(
command_context
args
)
:
    
uniffi_targets
=
build_uniffi_targets
(
command_context
)
    
cmdline
=
[
        
uniffi_targets
.
binary_path
        
"
-
-
library
-
path
"
        
uniffi_targets
.
library_path
        
"
-
-
fixtures
-
library
-
path
"
        
uniffi_targets
.
fixtures_library_path
        
"
pipeline
"
    
]
+
args
    
subprocess
.
check_call
(
cmdline
cwd
=
command_context
.
topsrcdir
)
    
return
0
