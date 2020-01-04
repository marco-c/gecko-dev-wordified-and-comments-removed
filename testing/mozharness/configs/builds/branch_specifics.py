_BUG1218570_OVERRIDES
=
{
    
'
macosx64
-
mulet
'
:
{
        
'
stage_server
'
:
'
stage
.
mozilla
.
org
'
    
}
    
'
win32
-
mulet
'
:
{
        
'
stage_server
'
:
'
stage
.
mozilla
.
org
'
    
}
}
config
=
{
    
"
mozilla
-
central
"
:
{
        
"
repo_path
"
:
'
mozilla
-
central
'
        
"
update_channel
"
:
"
nightly
"
        
"
graph_server_branch_name
"
:
"
Firefox
"
        
'
use_branch_in_symbols_extra_buildid
'
:
False
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
        
'
platform_overrides
'
:
_BUG1218570_OVERRIDES
    
}
    
'
mozilla
-
release
'
:
{
        
'
repo_path
'
:
'
releases
/
mozilla
-
release
'
        
'
update_channel
'
:
'
release
'
        
'
branch_uses_per_checkin_strategy
'
:
True
        
'
use_branch_in_symbols_extra_buildid
'
:
False
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
    
}
    
'
mozilla
-
beta
'
:
{
        
'
repo_path
'
:
'
releases
/
mozilla
-
beta
'
        
'
update_channel
'
:
'
beta
'
        
'
branch_uses_per_checkin_strategy
'
:
True
        
'
use_branch_in_symbols_extra_buildid
'
:
False
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
    
}
    
'
mozilla
-
aurora
'
:
{
        
'
repo_path
'
:
'
releases
/
mozilla
-
aurora
'
        
'
update_channel
'
:
'
aurora
'
        
'
branch_uses_per_checkin_strategy
'
:
True
        
'
use_branch_in_symbols_extra_buildid
'
:
False
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
    
}
    
'
try
'
:
{
        
'
repo_path
'
:
'
try
'
        
'
clone_by_revision
'
:
True
        
'
clone_with_purge
'
:
True
        
'
tinderbox_build_dir
'
:
'
%
(
who
)
s
-
%
(
got_revision
)
s
'
        
'
to_tinderbox_dated
'
:
False
        
'
include_post_upload_builddir
'
:
True
        
'
release_to_try_builds
'
:
True
        
'
use_branch_in_symbols_extra_buildid
'
:
False
        
'
stage_server
'
:
'
upload
.
trybld
.
productdelivery
.
prod
.
mozaws
.
net
'
        
'
stage_username
'
:
'
trybld
'
        
'
stage_ssh_key
'
:
'
trybld_dsa
'
        
'
branch_supports_uploadsymbols
'
:
False
        
'
use_clobberer
'
:
False
        
'
platform_overrides
'
:
_BUG1218570_OVERRIDES
    
}
    
'
b2g
-
inbound
'
:
{
        
'
repo_path
'
:
'
integration
/
b2g
-
inbound
'
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
        
'
platform_overrides
'
:
_BUG1218570_OVERRIDES
    
}
    
'
fx
-
team
'
:
{
        
'
repo_path
'
:
'
integration
/
fx
-
team
'
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
        
'
platform_overrides
'
:
_BUG1218570_OVERRIDES
    
}
    
'
gum
'
:
{
        
'
branch_uses_per_checkin_strategy
'
:
True
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
    
}
    
'
mozilla
-
inbound
'
:
{
        
'
repo_path
'
:
'
integration
/
mozilla
-
inbound
'
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
        
'
platform_overrides
'
:
_BUG1218570_OVERRIDES
    
}
    
'
services
-
central
'
:
{
        
'
repo_path
'
:
'
services
/
services
-
central
'
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
    
}
    
'
ux
'
:
{
        
"
graph_server_branch_name
"
:
"
UX
"
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
    
}
    
'
date
'
:
{
        
'
enable_release_promotion
'
:
1
        
'
platform_overrides
'
:
{
            
'
linux
'
:
{
                
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
linux32
/
beta
'
            
}
            
'
linux64
'
:
{
                
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
linux64
/
beta
'
            
}
            
'
macosx64
'
:
{
                
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
macosx
-
universal
/
beta
'
            
}
            
'
win32
'
:
{
                
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
beta
'
            
}
            
'
win64
'
:
{
                
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
win64
/
beta
'
            
}
        
}
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
    
}
    
'
cypress
'
:
{
        
'
branch_uses_per_checkin_strategy
'
:
True
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
    
}
    
'
alder
'
:
{
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
        
'
platform_overrides
'
:
_BUG1218570_OVERRIDES
    
}
    
'
ash
'
:
{
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
        
'
platform_overrides
'
:
_BUG1218570_OVERRIDES
    
}
    
'
birch
'
:
{
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
    
}
    
'
cedar
'
:
{
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
    
}
    
'
elm
'
:
{
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
    
}
    
'
fig
'
:
{
}
    
'
jamun
'
:
{
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
    
}
    
'
larch
'
:
{
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
    
}
    
'
oak
'
:
{
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
        
'
platform_overrides
'
:
_BUG1218570_OVERRIDES
    
}
    
'
pine
'
:
{
        
'
stage_server
'
:
'
upload
.
ffxbld
.
productdelivery
.
prod
.
mozaws
.
net
'
        
'
platform_overrides
'
:
_BUG1218570_OVERRIDES
    
}
}
