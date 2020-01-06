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
setup
-
mock
'
        
'
package
-
source
'
        
'
generate
-
source
-
signing
-
manifest
'
    
]
    
'
stage_platform
'
:
'
source
'
    
'
buildbot_json_path
'
:
'
buildprops
.
json
'
    
'
app_ini_path
'
:
'
FAKE
'
    
'
env
'
:
{
        
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
LC_ALL
'
:
'
C
'
    
}
    
'
mozconfig_variant
'
:
'
source
'
}
