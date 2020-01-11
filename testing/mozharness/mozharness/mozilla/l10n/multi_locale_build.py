"
"
"
multi_locale_build
.
py
This
should
be
a
mostly
generic
multilocale
build
script
.
"
"
"
import
os
import
sys
from
mozharness
.
base
.
errors
import
MakefileErrorList
from
mozharness
.
base
.
vcs
.
vcsbase
import
MercurialScript
from
mozharness
.
mozilla
.
l10n
.
locales
import
LocalesMixin
sys
.
path
.
insert
(
1
os
.
path
.
dirname
(
os
.
path
.
dirname
(
sys
.
path
[
0
]
)
)
)
class
MultiLocaleBuild
(
LocalesMixin
MercurialScript
)
:
    
"
"
"
This
class
targets
Fennec
multilocale
builds
.
        
We
were
considering
this
for
potential
Firefox
desktop
multilocale
.
        
Now
that
we
have
a
different
approach
for
B2G
multilocale
        
it
'
s
most
likely
misnamed
.
"
"
"
    
config_options
=
[
[
        
[
"
-
-
locale
"
]
        
{
"
action
"
:
"
extend
"
         
"
dest
"
:
"
locales
"
         
"
type
"
:
"
string
"
         
"
help
"
:
"
Specify
the
locale
(
s
)
to
repack
"
         
}
    
]
[
        
[
"
-
-
objdir
"
]
        
{
"
action
"
:
"
store
"
         
"
dest
"
:
"
objdir
"
         
"
type
"
:
"
string
"
         
"
default
"
:
"
objdir
"
         
"
help
"
:
"
Specify
the
objdir
"
         
}
    
]
[
        
[
"
-
-
l10n
-
base
"
]
        
{
"
action
"
:
"
store
"
         
"
dest
"
:
"
hg_l10n_base
"
         
"
type
"
:
"
string
"
         
"
help
"
:
"
Specify
the
L10n
repo
base
directory
"
         
}
    
]
[
        
[
"
-
-
l10n
-
tag
"
]
        
{
"
action
"
:
"
store
"
         
"
dest
"
:
"
hg_l10n_tag
"
         
"
type
"
:
"
string
"
         
"
help
"
:
"
Specify
the
L10n
tag
"
         
}
    
]
[
        
[
"
-
-
tag
-
override
"
]
        
{
"
action
"
:
"
store
"
         
"
dest
"
:
"
tag_override
"
         
"
type
"
:
"
string
"
         
"
help
"
:
"
Override
the
tags
set
for
all
repos
"
         
}
    
]
[
        
[
"
-
-
l10n
-
dir
"
]
        
{
"
action
"
:
"
store
"
         
"
dest
"
:
"
l10n_dir
"
         
"
type
"
:
"
string
"
         
"
default
"
:
"
l10n
"
         
"
help
"
:
"
Specify
the
l10n
dir
name
"
         
}
    
]
]
    
def
__init__
(
self
require_config_file
=
True
)
:
        
LocalesMixin
.
__init__
(
self
)
        
MercurialScript
.
__init__
(
self
config_options
=
self
.
config_options
                                 
all_actions
=
[
'
pull
-
locale
-
source
'
                                              
'
package
-
multi
'
                                              
'
summary
'
]
                                 
require_config_file
=
require_config_file
)
    
def
_run_mach_command
(
self
args
)
:
        
dirs
=
self
.
query_abs_dirs
(
)
        
topsrcdir
=
os
.
path
.
join
(
dirs
[
'
abs_work_dir
'
]
'
src
'
)
        
mach
=
[
sys
.
executable
'
mach
'
]
        
return_code
=
self
.
run_command
(
            
command
=
mach
+
[
'
-
-
log
-
no
-
times
'
]
+
args
            
cwd
=
topsrcdir
        
)
        
if
return_code
:
            
self
.
fatal
(
"
'
mach
%
s
'
did
not
run
successfully
.
Please
check
"
                       
"
log
for
errors
.
"
%
'
'
.
join
(
args
)
)
    
def
package_multi
(
self
)
:
        
dirs
=
self
.
query_abs_dirs
(
)
        
objdir
=
dirs
[
'
abs_objdir
'
]
        
locales
=
list
(
sorted
(
self
.
query_locales
(
)
)
)
        
self
.
_run_mach_command
(
[
'
package
-
multi
-
locale
'
                                
'
-
-
locales
'
]
+
locales
)
        
command
=
"
make
package
-
tests
AB_CD
=
multi
"
        
self
.
run_command
(
command
                         
cwd
=
objdir
                         
error_list
=
MakefileErrorList
                         
halt_on_failure
=
True
)
if
__name__
=
=
'
__main__
'
:
    
pass
