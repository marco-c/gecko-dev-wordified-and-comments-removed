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
{
            
'
android
-
api
-
16
-
old
-
id
'
:
{
                
"
update_channel
"
:
"
nightly
-
old
-
id
"
            
}
            
'
android
-
x86
-
old
-
id
'
:
{
                
"
update_channel
"
:
"
nightly
-
old
-
id
"
            
}
        
}
    
}
    
'
mozilla
-
release
'
:
{
        
'
enable_release_promotion
'
:
True
        
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
{
            
'
linux
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
                
'
force_clobber
'
:
True
            
}
            
'
linux64
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
                
'
force_clobber
'
:
True
            
}
            
'
macosx64
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
                
'
force_clobber
'
:
True
            
}
            
'
win32
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
                
'
force_clobber
'
:
True
            
}
            
'
win64
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
                
'
force_clobber
'
:
True
            
}
            
'
linux
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
linux64
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
linux64
-
asan
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
linux64
-
asan
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
linux64
-
st
-
an
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
linux64
-
st
-
an
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
linux64
-
add
-
on
-
devel
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
macosx64
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
macosx64
-
st
-
an
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
macosx64
-
st
-
an
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
macosx64
-
add
-
on
-
devel
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
win32
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
win32
-
add
-
on
-
devel
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
win64
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
win64
-
add
-
on
-
devel
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
        
}
    
}
    
'
mozilla
-
beta
'
:
{
        
'
enable_release_promotion
'
:
1
        
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
{
            
'
linux
'
:
{
                
'
mozconfig_variant
'
:
'
beta
'
                
'
force_clobber
'
:
True
            
}
            
'
linux64
'
:
{
                
'
mozconfig_variant
'
:
'
beta
'
                
'
force_clobber
'
:
True
            
}
            
'
macosx64
'
:
{
                
'
mozconfig_variant
'
:
'
beta
'
                
'
force_clobber
'
:
True
            
}
            
'
win32
'
:
{
                
'
mozconfig_variant
'
:
'
beta
'
                
'
force_clobber
'
:
True
            
}
            
'
win64
'
:
{
                
'
mozconfig_variant
'
:
'
beta
'
                
'
force_clobber
'
:
True
            
}
            
'
linux
-
devedition
'
:
{
                
"
update_channel
"
:
"
aurora
"
            
}
            
'
linux64
-
devedition
'
:
{
                
"
update_channel
"
:
"
aurora
"
            
}
            
'
macosx64
-
devedition
'
:
{
                
"
update_channel
"
:
"
aurora
"
            
}
            
'
win32
-
devedition
'
:
{
                
"
update_channel
"
:
"
aurora
"
            
}
            
'
win64
-
devedition
'
:
{
                
"
update_channel
"
:
"
aurora
"
            
}
            
'
linux
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
linux64
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
linux64
-
asan
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
linux64
-
asan
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
linux64
-
st
-
an
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
linux64
-
st
-
an
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
linux64
-
add
-
on
-
devel
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
macosx64
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
macosx64
-
st
-
an
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
macosx64
-
st
-
an
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
macosx64
-
add
-
on
-
devel
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
win32
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
win32
-
add
-
on
-
devel
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
win64
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
win64
-
add
-
on
-
devel
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
        
}
    
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
    
}
    
'
autoland
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
autoland
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
update_channel
'
:
'
nightly
-
date
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
{
            
'
android
-
api
-
16
-
old
-
id
'
:
{
                
"
update_channel
"
:
"
nightly
-
old
-
id
"
            
}
            
'
android
-
x86
-
old
-
id
'
:
{
                
"
update_channel
"
:
"
nightly
-
old
-
id
"
            
}
        
}
    
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
graphics
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
jamun
'
:
{
        
'
update_channel
'
:
'
beta
'
        
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
mozconfig_variant
'
:
'
release
'
            
}
            
'
linux
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
linux64
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
            
}
            
'
linux64
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
linux64
-
asan
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
linux64
-
asan
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
linux64
-
st
-
an
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
linux64
-
st
-
an
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
macosx64
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
            
}
            
'
macosx64
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
macosx64
-
st
-
an
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
macosx64
-
st
-
an
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
win32
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
            
}
            
'
win32
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
win64
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
            
}
            
'
win64
-
debug
'
:
{
                
'
update_channel
'
:
'
default
'
            
}
            
'
linux
-
devedition
'
:
{
                
"
update_channel
"
:
"
aurora
"
            
}
            
'
linux64
-
devedition
'
:
{
                
"
update_channel
"
:
"
aurora
"
            
}
            
'
macosx64
-
devedition
'
:
{
                
"
update_channel
"
:
"
aurora
"
            
}
            
'
win32
-
devedition
'
:
{
                
"
update_channel
"
:
"
aurora
"
            
}
            
'
win64
-
devedition
'
:
{
                
"
update_channel
"
:
"
aurora
"
            
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
    
}
}
