import
os
from
datetime
import
datetime
timedelta
from
compare_locales
import
parser
from
compare_locales
.
lint
.
linter
import
L10nLinter
from
compare_locales
.
lint
.
util
import
l10n_base_reference_and_tests
from
compare_locales
.
paths
import
ProjectFiles
TOMLParser
from
mach
import
util
as
mach_util
from
mozlint
import
pathutils
result
from
mozpack
import
path
as
mozpath
from
mozversioncontrol
import
MissingVCSTool
from
mozversioncontrol
.
repoupdate
import
update_git_repo
update_mercurial_repo
L10N_SOURCE_NAME
=
"
l10n
-
source
"
L10N_SOURCE_REPO
=
"
https
:
/
/
github
.
com
/
mozilla
-
l10n
/
firefox
-
l10n
-
source
.
git
"
STRINGS_NAME
=
"
gecko
-
strings
"
STRINGS_REPO
=
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
/
gecko
-
strings
"
PULL_AFTER
=
timedelta
(
days
=
2
)
def
lint
(
paths
lintconfig
*
*
lintargs
)
:
    
extra_args
=
lintargs
.
get
(
"
extra_args
"
)
or
[
]
    
name
=
L10N_SOURCE_NAME
if
"
-
-
l10n
-
git
"
in
extra_args
else
STRINGS_NAME
    
return
lint_strings
(
name
paths
lintconfig
*
*
lintargs
)
def
lint_strings
(
name
paths
lintconfig
*
*
lintargs
)
:
    
l10n_base
=
mach_util
.
get_state_dir
(
)
    
root
=
lintargs
[
"
root
"
]
    
exclude
=
lintconfig
.
get
(
"
exclude
"
)
    
extensions
=
lintconfig
.
get
(
"
extensions
"
)
    
l10nconfigs
=
load_configs
(
lintconfig
root
l10n_base
name
)
    
if
lintconfig
[
"
path
"
]
in
paths
:
        
results
=
validate_linter_includes
(
lintconfig
l10nconfigs
lintargs
)
        
paths
.
remove
(
lintconfig
[
"
path
"
]
)
    
else
:
        
results
=
[
]
    
all_files
=
[
]
    
for
p
in
paths
:
        
fp
=
pathutils
.
FilterPath
(
p
)
        
if
fp
.
isdir
:
            
for
_
fileobj
in
fp
.
finder
:
                
all_files
.
append
(
fileobj
.
path
)
        
if
fp
.
isfile
:
            
all_files
.
append
(
p
)
    
all_files
_
=
pathutils
.
filterpaths
(
        
lintargs
[
"
root
"
]
        
all_files
        
lintconfig
[
"
include
"
]
        
exclude
=
exclude
        
extensions
=
extensions
    
)
    
skips
=
{
p
for
p
in
all_files
if
not
parser
.
hasParser
(
p
)
}
    
results
.
extend
(
        
result
.
from_config
(
            
lintconfig
            
level
=
"
warning
"
            
path
=
path
            
message
=
"
file
format
not
supported
in
compare
-
locales
"
        
)
        
for
path
in
skips
    
)
    
all_files
=
[
p
for
p
in
all_files
if
p
not
in
skips
]
    
files
=
ProjectFiles
(
name
l10nconfigs
)
    
get_reference_and_tests
=
l10n_base_reference_and_tests
(
files
)
    
linter
=
MozL10nLinter
(
lintconfig
)
    
results
+
=
linter
.
lint
(
all_files
get_reference_and_tests
)
    
return
results
def
gecko_strings_setup
(
*
*
lint_args
)
:
    
extra_args
=
lint_args
.
get
(
"
extra_args
"
)
or
[
]
    
if
"
-
-
l10n
-
git
"
in
extra_args
:
        
return
source_repo_setup
(
L10N_SOURCE_REPO
L10N_SOURCE_NAME
)
    
else
:
        
return
strings_repo_setup
(
STRINGS_REPO
STRINGS_NAME
)
def
source_repo_setup
(
repo
:
str
name
:
str
)
:
    
gs
=
mozpath
.
join
(
mach_util
.
get_state_dir
(
)
name
)
    
marker
=
mozpath
.
join
(
gs
"
.
git
"
"
l10n_pull_marker
"
)
    
try
:
        
last_pull
=
datetime
.
fromtimestamp
(
os
.
stat
(
marker
)
.
st_mtime
)
        
skip_clone
=
datetime
.
now
(
)
<
last_pull
+
PULL_AFTER
    
except
OSError
:
        
skip_clone
=
False
    
if
skip_clone
:
        
return
    
try
:
        
update_git_repo
(
repo
gs
)
    
except
MissingVCSTool
:
        
if
os
.
environ
.
get
(
"
MOZ_AUTOMATION
"
)
:
            
raise
        
print
(
"
warning
:
l10n
linter
requires
Git
but
was
unable
to
find
'
git
'
"
)
        
return
1
    
with
open
(
marker
"
w
"
)
as
fh
:
        
fh
.
flush
(
)
def
strings_repo_setup
(
repo
:
str
name
:
str
)
:
    
gs
=
mozpath
.
join
(
mach_util
.
get_state_dir
(
)
name
)
    
marker
=
mozpath
.
join
(
gs
"
.
hg
"
"
l10n_pull_marker
"
)
    
try
:
        
last_pull
=
datetime
.
fromtimestamp
(
os
.
stat
(
marker
)
.
st_mtime
)
        
skip_clone
=
datetime
.
now
(
)
<
last_pull
+
PULL_AFTER
    
except
OSError
:
        
skip_clone
=
False
    
if
skip_clone
:
        
return
    
try
:
        
update_mercurial_repo
(
repo
gs
)
    
except
MissingVCSTool
:
        
if
os
.
environ
.
get
(
"
MOZ_AUTOMATION
"
)
:
            
raise
        
print
(
"
warning
:
l10n
linter
requires
Mercurial
but
was
unable
to
find
'
hg
'
"
)
        
return
1
    
with
open
(
marker
"
w
"
)
as
fh
:
        
fh
.
flush
(
)
def
load_configs
(
lintconfig
root
l10n_base
locale
)
:
    
"
"
"
Load
l10n
configuration
files
specified
in
the
linter
configuration
.
"
"
"
    
configs
=
[
]
    
env
=
{
"
l10n_base
"
:
l10n_base
}
    
for
toml
in
lintconfig
[
"
l10n_configs
"
]
:
        
cfg
=
TOMLParser
(
)
.
parse
(
            
mozpath
.
join
(
root
toml
)
env
=
env
ignore_missing_includes
=
True
        
)
        
cfg
.
set_locales
(
[
locale
]
deep
=
True
)
        
configs
.
append
(
cfg
)
    
return
configs
def
validate_linter_includes
(
lintconfig
l10nconfigs
lintargs
)
:
    
"
"
"
Check
l10n
.
yml
config
against
l10n
.
toml
configs
.
"
"
"
    
reference_paths
=
set
(
        
mozpath
.
relpath
(
p
[
"
reference
"
]
.
prefix
lintargs
[
"
root
"
]
)
        
for
project
in
l10nconfigs
        
for
config
in
project
.
configs
        
for
p
in
config
.
paths
    
)
    
reference_dirs
=
sorted
(
p
for
p
in
reference_paths
if
os
.
path
.
isdir
(
p
)
)
    
missing_in_yml
=
[
        
refd
for
refd
in
reference_dirs
if
refd
not
in
lintconfig
[
"
include
"
]
    
]
    
missing_in_yml
=
[
        
d
        
for
d
in
missing_in_yml
        
if
not
any
(
d
.
startswith
(
parent
+
"
/
"
)
for
parent
in
lintconfig
[
"
include
"
]
)
    
]
    
if
missing_in_yml
:
        
dirs
=
"
"
.
join
(
missing_in_yml
)
        
return
[
            
result
.
from_config
(
                
lintconfig
                
path
=
lintconfig
[
"
path
"
]
                
message
=
"
l10n
.
yml
out
of
sync
with
l10n
.
toml
add
:
"
+
dirs
            
)
        
]
    
return
[
]
class
MozL10nLinter
(
L10nLinter
)
:
    
"
"
"
Subclass
linter
to
generate
the
right
result
type
.
"
"
"
    
def
__init__
(
self
lintconfig
)
:
        
super
(
MozL10nLinter
self
)
.
__init__
(
)
        
self
.
lintconfig
=
lintconfig
    
def
lint
(
self
files
get_reference_and_tests
)
:
        
return
[
            
result
.
from_config
(
self
.
lintconfig
*
*
result_data
)
            
for
result_data
in
super
(
MozL10nLinter
self
)
.
lint
(
                
files
get_reference_and_tests
            
)
        
]
