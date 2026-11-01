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
"
pull
-
locale
-
source
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
        
mach
=
[
sys
.
executable
"
mach
"
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
"
-
-
log
-
no
-
times
"
]
+
args
            
cwd
=
dirs
[
"
abs_src_dir
"
]
        
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
"
"
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
"
package
-
multi
-
locale
"
"
-
-
package
-
tests
"
"
-
-
locales
"
]
+
locales
        
)
if
__name__
=
=
"
__main__
"
:
    
pass
