import
os
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
build
'
        
'
check
-
test
'
    
]
    
'
stage_platform
'
:
'
linux64
-
fuzzing
-
cov
'
    
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
MOZ_AUTOMATION
'
:
'
1
'
        
'
DISPLAY
'
:
'
:
2
'
        
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
LC_ALL
'
:
'
C
'
        
'
ASAN_OPTIONS
'
:
'
detect_leaks
=
0
'
        
'
PATH
'
:
'
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
\
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
'
    
}
    
'
mozconfig_variant
'
:
'
nightly
-
fuzzing
-
cov
'
}
