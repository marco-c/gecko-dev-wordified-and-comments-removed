config
=
{
    
"
default_actions
"
:
[
"
package
-
source
"
]
    
"
stage_platform
"
:
"
source
"
    
"
env
"
:
{
        
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
TINDERBOX_OUTPUT
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
    
}
    
"
src_mozconfig
"
:
"
browser
/
config
/
mozconfigs
/
linux64
/
source
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
/
"
    
}
}
