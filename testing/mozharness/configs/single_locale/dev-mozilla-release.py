config
=
{
    
"
branch
"
:
"
jamun
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
release
-
dev
"
    
"
latest_mar_dir
"
:
'
fake_kill_me
'
    
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
releases
/
l10n
/
mozilla
-
release
"
    
"
mozilla_dir
"
:
"
jamun
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
jamun
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
jamun
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
