import
os
import
sys
config
=
{
    
'
default_actions
'
:
[
        
'
clobber
'
        
'
clone
-
tools
'
        
'
checkout
-
sources
'
        
'
build
'
        
'
sendchange
'
    
]
    
"
buildbot_json_path
"
:
"
buildprops
.
json
"
    
'
app_ini_path
'
:
'
%
(
obj_dir
)
s
/
dist
/
bin
/
application
.
ini
'
    
'
enable_signing
'
:
False
    
'
vcs_share_base
'
:
'
/
builds
/
hg
-
shared
'
    
'
debug_build
'
:
True
    
'
enable_talos_sendchange
'
:
False
    
'
enable_unittest_sendchange
'
:
True
    
'
perfherder_extra_options
'
:
[
'
artifact
'
]
    
'
base_name
'
:
'
OS
X
10
.
7
%
(
branch
)
s_Artifact_build
'
    
'
platform
'
:
'
macosx64
'
    
'
stage_platform
'
:
'
macosx64
-
debug
'
    
'
publish_nightly_en_US_routes
'
:
False
    
'
env
'
:
{
        
'
MOZBUILD_STATE_PATH
'
:
os
.
path
.
join
(
os
.
getcwd
(
)
'
.
mozbuild
'
)
        
'
HG_SHARE_BASE_DIR
'
:
'
/
builds
/
hg
-
shared
'
        
'
MOZ_OBJDIR
'
:
'
%
(
abs_obj_dir
)
s
'
        
'
TINDERBOX_OUTPUT
'
:
'
1
'
        
'
TOOLTOOL_CACHE
'
:
'
/
builds
/
tooltool_cache
'
        
'
TOOLTOOL_HOME
'
:
'
/
builds
'
        
'
MOZ_CRASHREPORTER_NO_REPORT
'
:
'
1
'
        
'
CCACHE_DIR
'
:
'
/
builds
/
ccache
'
        
'
CCACHE_COMPRESS
'
:
'
1
'
        
'
CCACHE_UMASK
'
:
'
002
'
        
'
LC_ALL
'
:
'
C
'
        
'
XPCOM_DEBUG_BREAK
'
:
'
stack
-
and
-
abort
'
        
'
PATH
'
:
'
/
tools
/
python
/
bin
:
/
opt
/
local
/
bin
:
/
usr
/
bin
:
'
                
'
/
bin
:
/
usr
/
sbin
:
/
sbin
:
/
usr
/
local
/
bin
:
/
usr
/
X11
/
bin
'
    
}
    
'
mozconfig_variant
'
:
'
debug
-
artifact
'
}
