"
"
"
fx_desktop_build
.
py
.
script
harness
to
build
nightly
firefox
within
Mozilla
'
s
build
environment
and
developer
machines
alike
"
"
"
import
os
import
sys
sys
.
path
.
insert
(
1
os
.
path
.
dirname
(
sys
.
path
[
0
]
)
)
import
mozharness
.
base
.
script
as
script
from
mozharness
.
mozilla
.
building
.
buildbase
import
(
    
BUILD_BASE_CONFIG_OPTIONS
    
BuildingConfig
    
BuildScript
)
class
FxDesktopBuild
(
BuildScript
object
)
:
    
def
__init__
(
self
)
:
        
buildscript_kwargs
=
{
            
"
config_options
"
:
BUILD_BASE_CONFIG_OPTIONS
            
"
all_actions
"
:
[
                
"
get
-
secrets
"
                
"
clobber
"
                
"
build
"
                
"
static
-
analysis
-
autotest
"
                
"
valgrind
-
test
"
                
"
multi
-
l10n
"
                
"
package
-
source
"
            
]
            
"
require_config_file
"
:
True
            
"
config
"
:
{
                
"
is_automation
"
:
True
                
"
debug_build
"
:
False
                
"
nightly_build
"
:
False
                
"
clone_upstream_url
"
:
"
https
:
/
/
hg
.
mozilla
.
org
/
mozilla
-
unified
"
                
"
repo_base
"
:
"
https
:
/
/
hg
.
mozilla
.
org
"
                
"
profile_build_resources_path
"
:
"
%
(
upload_path
)
s
/
profile_build_resources
.
json
"
                
"
nightly_promotion_branches
"
:
[
"
mozilla
-
central
"
"
mozilla
-
aurora
"
]
                
"
clone_with_purge
"
:
False
                
"
clone_by_revision
"
:
False
                
"
virtualenv_modules
"
:
[
                    
"
requests
=
=
2
.
8
.
1
"
                
]
                
"
virtualenv_path
"
:
"
venv
"
            
}
            
"
ConfigClass
"
:
BuildingConfig
        
}
        
super
(
FxDesktopBuild
self
)
.
__init__
(
*
*
buildscript_kwargs
)
    
def
query_abs_dirs
(
self
)
:
        
if
self
.
abs_dirs
:
            
return
self
.
abs_dirs
        
abs_dirs
=
super
(
FxDesktopBuild
self
)
.
query_abs_dirs
(
)
        
dirs
=
{
            
"
abs_obj_dir
"
:
os
.
path
.
join
(
abs_dirs
[
"
abs_work_dir
"
]
self
.
_query_objdir
(
)
)
            
"
upload_path
"
:
self
.
config
[
"
upload_env
"
]
[
"
UPLOAD_PATH
"
]
        
}
        
abs_dirs
.
update
(
dirs
)
        
self
.
abs_dirs
=
abs_dirs
        
return
self
.
abs_dirs
    
script
.
PreScriptRun
    
def
suppress_windows_modal_dialogs
(
self
*
args
*
*
kwargs
)
:
        
if
self
.
_is_windows
(
)
:
            
import
ctypes
            
ctypes
.
windll
.
kernel32
.
SetErrorMode
(
0x8001
)
if
__name__
=
=
"
__main__
"
:
    
fx_desktop_build
=
FxDesktopBuild
(
)
    
fx_desktop_build
.
run_and_exit
(
)
