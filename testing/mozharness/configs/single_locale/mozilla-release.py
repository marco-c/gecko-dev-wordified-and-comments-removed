import
os
config
=
{
    
"
nightly_build
"
:
True
    
"
branch
"
:
"
mozilla
-
release
"
    
"
en_us_binary_url
"
:
"
http
:
/
/
ftp
.
mozilla
.
org
/
pub
/
mozilla
.
org
/
firefox
/
nightly
/
latest
-
mozilla
-
release
/
"
    
"
update_channel
"
:
"
release
"
    
"
hg_l10n_base
"
:
"
https
:
/
/
hg
.
mozilla
.
org
/
l10n
-
central
"
    
"
mar_tools_url
"
:
os
.
environ
[
"
MAR_TOOLS_URL
"
]
    
"
repos
"
:
[
{
        
"
vcs
"
:
"
hg
"
        
"
repo
"
:
"
https
:
/
/
hg
.
mozilla
.
org
/
build
/
tools
"
        
"
branch
"
:
"
default
"
        
"
dest
"
:
"
tools
"
    
}
{
        
"
vcs
"
:
"
hg
"
        
"
repo
"
:
"
https
:
/
/
hg
.
mozilla
.
org
/
releases
/
mozilla
-
release
"
        
"
revision
"
:
"
%
(
revision
)
s
"
        
"
dest
"
:
"
mozilla
-
release
"
        
"
clone_upstream_url
"
:
"
https
:
/
/
hg
.
mozilla
.
org
/
mozilla
-
unified
"
    
}
]
    
'
purge_minsize
'
:
12
    
'
is_automation
'
:
True
    
'
default_actions
'
:
[
        
"
clobber
"
        
"
pull
"
        
"
clone
-
locales
"
        
"
list
-
locales
"
        
"
setup
"
        
"
repack
"
        
"
taskcluster
-
upload
"
        
"
summary
"
    
]
}
