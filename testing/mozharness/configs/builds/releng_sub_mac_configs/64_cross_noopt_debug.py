import
os
MOZ_OBJDIR
=
'
obj
-
firefox
'
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
upload
-
files
'
        
'
sendchange
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
macosx64
-
noopt
-
debug
'
    
'
debug_build
'
:
True
    
'
objdir
'
:
'
obj
-
firefox
'
    
'
enable_talos_sendchange
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
obj
-
firefox
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
tools
/
buildbot
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
src_mozconfig
'
:
'
browser
/
config
/
mozconfigs
/
macosx64
/
cross
-
noopt
-
debug
'
    
'
artifact_flag_build_variant_in_try
'
:
'
cross
-
debug
-
artifact
'
}
