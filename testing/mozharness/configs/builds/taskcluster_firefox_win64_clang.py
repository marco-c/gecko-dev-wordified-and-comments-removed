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
clone
-
tools
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
exes
'
:
{
        
'
virtualenv
'
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
third_party
'
'
python
'
'
virtualenv
'
'
virtualenv
.
py
'
            
)
        
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
vcs_share_base
'
:
os
.
path
.
join
(
'
y
:
'
os
.
sep
'
hg
-
shared
'
)
    
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
      
os
.
path
.
join
(
os
.
environ
[
'
MOZILLABUILD
'
]
'
tooltool
.
py
'
)
    
]
    
'
tooltool_bootstrap
'
:
'
setup
.
sh
'
    
'
enable_count_ctors
'
:
False
    
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
static
-
analysis
'
]
    
'
base_name
'
:
'
WINNT_6
.
1_x86
-
64_
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
win64
'
    
'
stage_platform
'
:
'
win64
-
st
-
an
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
HG_SHARE_BASE_DIR
'
:
os
.
path
.
join
(
'
y
:
'
os
.
sep
'
hg
-
shared
'
)
        
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
10
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
        
'
MSYSTEM
'
:
'
MINGW32
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
localhost
'
        
'
UPLOAD_PATH
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
public
'
'
build
'
)
    
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
\
\
breakpad
\
\
win64
\
\
minidump_stackwalk
.
exe
'
        
'
MINIDUMP_SAVE_PATH
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
public
'
'
build
'
)
    
}
    
'
src_mozconfig
'
:
'
browser
\
\
config
\
\
mozconfigs
\
\
win64
\
\
clang
'
    
'
artifact_flag_build_variant_in_try
'
:
None
}
