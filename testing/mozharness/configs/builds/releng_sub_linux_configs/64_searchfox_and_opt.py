import
os
config
=
{
    
"
default_actions
"
:
[
        
"
clobber
"
        
"
build
"
    
]
    
"
vcs_share_base
"
:
"
/
builds
/
hg
-
shared
"
    
"
upload_env
"
:
{
        
"
UPLOAD_PATH
"
:
"
/
builds
/
worker
/
artifacts
"
    
}
    
"
env
"
:
{
        
"
MOZBUILD_STATE_PATH
"
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
"
.
mozbuild
"
)
        
"
DISPLAY
"
:
"
:
2
"
        
"
HG_SHARE_BASE_DIR
"
:
"
/
builds
/
hg
-
shared
"
        
"
MOZ_OBJDIR
"
:
"
%
(
abs_obj_dir
)
s
"
        
"
TINDERBOX_OUTPUT
"
:
"
1
"
        
"
TOOLTOOL_CACHE
"
:
"
/
builds
/
worker
/
tooltool
-
cache
"
        
"
TOOLTOOL_HOME
"
:
"
/
builds
"
        
"
MOZ_CRASHREPORTER_NO_REPORT
"
:
"
1
"
        
"
LC_ALL
"
:
"
C
"
        
"
PATH
"
:
"
/
usr
/
local
/
bin
:
/
bin
:
/
usr
/
bin
:
/
usr
/
local
/
sbin
:
/
usr
/
sbin
:
/
sbin
"
    
}
    
"
mozconfig_variant
"
:
"
opt
-
searchfox
-
clang
"
    
"
platform
"
:
"
linux64
"
    
"
stage_platform
"
:
"
linux64
-
searchfox
-
opt
"
    
"
mozconfig_platform
"
:
"
linux64
"
}
