import
os
BUILD_DIR
=
"
mozilla
-
central
"
L10N_REPO_PATH
=
"
l10n
-
central
"
OBJDIR
=
"
objdir
-
droid
"
MOZCONFIG
=
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
mozconfig
"
)
config
=
{
    
"
work_dir
"
:
"
.
"
    
"
log_name
"
:
"
multilocale
"
    
"
objdir
"
:
OBJDIR
    
"
locales_file
"
:
"
%
s
/
mobile
/
locales
/
l10n
-
changesets
.
json
"
%
BUILD_DIR
    
"
locales_platform
"
:
"
android
-
multilocale
"
    
"
locales_dir
"
:
"
mobile
/
android
/
locales
"
    
"
ignore_locales
"
:
[
"
en
-
US
"
"
multi
"
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
l10n_repos
"
:
[
]
    
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
%
s
"
%
L10N_REPO_PATH
    
"
hg_l10n_tag
"
:
"
default
"
    
"
l10n_dir
"
:
"
l10n
"
    
"
mozilla_dir
"
:
BUILD_DIR
    
"
mozconfig
"
:
MOZCONFIG
    
"
default_actions
"
:
[
        
"
pull
-
locale
-
source
"
        
"
build
"
        
"
package
-
en
-
US
"
        
"
backup
-
objdir
"
        
"
restore
-
objdir
"
        
"
add
-
locales
"
        
"
android
-
assemble
-
app
"
        
"
package
-
multi
"
        
"
summary
"
    
]
}
