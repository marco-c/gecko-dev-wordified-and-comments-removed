config
=
{
    
"
branch
"
:
"
date
"
    
"
nightly_build
"
:
True
    
"
update_channel
"
:
"
aurora
-
dev
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
mozilla_dir
"
:
"
date
"
    
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
projects
/
date
"
        
"
branch
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
date
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
is_automation
'
:
True
    
'
purge_minsize
'
:
12
    
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
