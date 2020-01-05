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
upload
-
files
'
        
'
sendchange
'
        
'
check
-
test
'
        
'
generate
-
build
-
stats
'
        
'
update
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
True
    
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
'
obj
-
firefox
'
    
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
enable_talos_sendchange
'
:
True
    
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
s
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
'
    
'
publish_nightly_en_US_routes
'
:
True
    
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
'
obj
-
firefox
'
        
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
01
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
PDBSTR_PATH
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
Windows
Kits
/
8
.
0
/
Debuggers
/
x64
/
srcsrv
/
pdbstr
.
exe
'
        
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
c
:
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
    
}
    
'
upload_env
'
:
{
        
'
UPLOAD_HOST
'
:
'
%
(
stage_server
)
s
'
        
'
UPLOAD_USER
'
:
'
%
(
stage_username
)
s
'
        
'
UPLOAD_SSH_KEY
'
:
'
/
c
/
Users
/
cltbld
/
.
ssh
/
%
(
stage_ssh_key
)
s
'
        
'
UPLOAD_TO_TEMP
'
:
'
1
'
    
}
    
"
check_test_env
"
:
{
        
'
MINIDUMP_STACKWALK
'
:
'
%
(
abs_tools_dir
)
s
/
breakpad
/
win32
/
minidump_stackwalk
.
exe
'
        
'
MINIDUMP_SAVE_PATH
'
:
'
%
(
base_work_dir
)
s
/
minidumps
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
nightly
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
