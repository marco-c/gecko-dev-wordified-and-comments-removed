import
os
import
sys
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
exes
'
:
{
        
'
python2
.
7
'
:
sys
.
executable
        
"
buildbot
"
:
[
            
sys
.
executable
            
'
c
:
\
\
mozilla
-
build
\
\
buildbotve
\
\
scripts
\
\
buildbot
'
        
]
        
"
make
"
:
[
            
sys
.
executable
            
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
build
'
'
src
'
'
build
'
'
pymake
'
'
make
.
py
'
            
)
        
]
        
'
virtualenv
'
:
[
            
sys
.
executable
            
'
c
:
/
mozilla
-
build
/
buildbotve
/
virtualenv
.
py
'
        
]
    
}
    
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
enable_ccache
'
:
False
    
'
vcs_share_base
'
:
'
C
:
/
builds
/
hg
-
shared
'
    
'
objdir
'
:
MOZ_OBJDIR
    
'
tooltool_script
'
:
[
sys
.
executable
                        
'
C
:
/
mozilla
-
build
/
tooltool
.
py
'
]
    
'
tooltool_bootstrap
'
:
"
setup
.
sh
"
    
'
enable_count_ctors
'
:
False
    
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
max_build_output_timeout
'
:
60
*
80
    
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
WINNT_5
.
2_
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
win32
'
    
'
stage_platform
'
:
'
win32
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
MOZ_AUTOMATION
'
:
'
1
'
        
'
BINSCOPE
'
:
'
C
:
/
Program
Files
(
x86
)
/
Microsoft
/
SDL
BinScope
/
BinScope
.
exe
'
        
'
HG_SHARE_BASE_DIR
'
:
'
C
:
/
builds
/
hg
-
shared
'
        
'
MOZ_CRASHREPORTER_NO_REPORT
'
:
'
1
'
        
'
MOZ_OBJDIR
'
:
MOZ_OBJDIR
        
'
PATH
'
:
'
C
:
/
mozilla
-
build
/
nsis
-
3
.
0b1
;
C
:
/
mozilla
-
build
/
python27
;
'
                
'
C
:
/
mozilla
-
build
/
buildbotve
/
scripts
;
'
                
'
%
s
'
%
(
os
.
environ
.
get
(
'
path
'
)
)
        
'
PROPERTIES_FILE
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
buildprops
.
json
'
)
        
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
c
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
c
/
builds
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
    
}
    
'
enable_pymake
'
:
True
    
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
win32
/
debug
-
artifact
'
    
'
tooltool_manifest_src
'
:
"
browser
/
config
/
tooltool
-
manifests
/
win32
/
releng
.
manifest
"
}
