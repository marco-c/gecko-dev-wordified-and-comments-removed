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
build
"
        
"
multi
-
l10n
"
    
]
    
"
max_build_output_timeout
"
:
0
    
"
secret_files
"
:
[
        
{
            
"
filename
"
:
"
/
builds
/
gls
-
gapi
.
data
"
            
"
secret_name
"
:
"
project
/
releng
/
gecko
/
build
/
level
-
%
(
scm
-
level
)
s
/
gls
-
gapi
.
data
"
            
"
min_scm_level
"
:
1
        
}
        
{
            
"
filename
"
:
"
/
builds
/
sb
-
gapi
.
data
"
            
"
secret_name
"
:
"
project
/
releng
/
gecko
/
build
/
level
-
%
(
scm
-
level
)
s
/
sb
-
gapi
.
data
"
            
"
min_scm_level
"
:
1
        
}
        
{
            
"
filename
"
:
"
/
builds
/
mozilla
-
fennec
-
geoloc
-
api
.
key
"
            
"
secret_name
"
:
"
project
/
releng
/
gecko
/
build
/
level
-
%
(
scm
-
level
)
s
/
mozilla
-
fennec
-
geoloc
-
api
.
key
"
            
"
min_scm_level
"
:
2
            
"
default
"
:
"
try
-
build
-
has
-
no
-
secrets
"
        
}
    
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
multi_locale
"
:
True
    
"
platform
"
:
"
android
"
    
"
stage_platform
"
:
"
android
"
    
"
enable_max_vsize
"
:
False
    
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
"
        
"
SHIP_LICENSED_FONTS
"
:
"
1
"
    
}
    
"
src_mozconfig
"
:
"
mobile
/
android
/
config
/
mozconfigs
/
android
/
nightly
"
    
"
disable_package_metrics
"
:
True
}
