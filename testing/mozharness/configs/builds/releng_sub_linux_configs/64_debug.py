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
        
'
update
'
    
]
    
'
stage_platform
'
:
'
linux64
-
debug
'
    
'
debug_build
'
:
True
    
'
enable_signing
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
usr
/
local
/
bin
:
/
usr
/
lib64
/
ccache
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
        
'
LD_LIBRARY_PATH
'
:
'
%
(
abs_obj_dir
)
s
/
dist
/
bin
'
        
'
TINDERBOX_OUTPUT
'
:
'
1
'
    
}
    
'
mozconfig_variant
'
:
'
debug
'
}
