import
logging
import
os
import
shutil
import
site
import
sys
import
sysconfig
from
shutil
import
which
try
:
    
import
pkg_resources
as
_pkg_resources
    
get_pkg_resources
=
lambda
:
_pkg_resources
except
ImportError
:
    
def
get_pkg_resources
(
)
:
        
raise
ValueError
(
"
The
Python
module
virtualenv
is
not
installed
.
"
)
from
tools
.
wpt
.
utils
import
call
logger
=
logging
.
getLogger
(
__name__
)
class
Virtualenv
:
    
def
__init__
(
self
path
skip_virtualenv_setup
)
:
        
self
.
path
=
path
        
self
.
skip_virtualenv_setup
=
skip_virtualenv_setup
        
if
not
skip_virtualenv_setup
:
            
self
.
virtualenv
=
[
sys
.
executable
"
-
m
"
"
venv
"
]
            
self
.
_working_set
=
None
    
property
    
def
exists
(
self
)
:
        
return
os
.
path
.
isdir
(
self
.
path
)
and
os
.
path
.
isdir
(
self
.
lib_path
)
    
property
    
def
broken_link
(
self
)
:
        
python_link
=
os
.
path
.
join
(
self
.
path
"
.
Python
"
)
        
return
os
.
path
.
lexists
(
python_link
)
and
not
os
.
path
.
exists
(
python_link
)
    
def
create
(
self
)
:
        
if
os
.
path
.
exists
(
self
.
path
)
:
            
shutil
.
rmtree
(
self
.
path
ignore_errors
=
True
)
            
self
.
_working_set
=
None
        
call
(
*
self
.
virtualenv
self
.
path
)
    
def
get_paths
(
self
)
:
        
"
"
"
Wrapper
around
sysconfig
.
get_paths
(
)
returning
the
appropriate
paths
for
the
env
.
"
"
"
        
if
"
venv
"
in
sysconfig
.
get_scheme_names
(
)
:
            
scheme
=
"
venv
"
        
elif
os
.
name
=
=
"
nt
"
:
            
scheme
=
"
nt
"
        
elif
os
.
name
=
=
"
posix
"
:
            
scheme
=
"
posix_prefix
"
        
elif
sys
.
version_info
>
=
(
3
10
)
:
            
scheme
=
sysconfig
.
get_default_scheme
(
)
        
else
:
            
scheme
=
sysconfig
.
_get_default_scheme
(
)
        
vars
=
{
            
"
base
"
:
self
.
path
            
"
platbase
"
:
self
.
path
            
"
installed_base
"
:
self
.
path
            
"
installed_platbase
"
:
self
.
path
        
}
        
return
sysconfig
.
get_paths
(
scheme
vars
)
    
property
    
def
bin_path
(
self
)
:
        
return
self
.
get_paths
(
)
[
"
scripts
"
]
    
property
    
def
pip_path
(
self
)
:
        
path
=
which
(
"
pip3
"
path
=
self
.
bin_path
)
        
if
path
is
None
:
            
path
=
which
(
"
pip
"
path
=
self
.
bin_path
)
        
if
path
is
None
:
            
raise
ValueError
(
"
pip3
or
pip
not
found
"
)
        
return
path
    
property
    
def
lib_path
(
self
)
:
        
return
self
.
get_paths
(
)
[
"
platlib
"
]
    
property
    
def
working_set
(
self
)
:
        
if
not
self
.
exists
:
            
raise
ValueError
(
"
trying
to
read
working_set
when
venv
doesn
'
t
exist
"
)
        
if
self
.
_working_set
is
None
:
            
self
.
_working_set
=
get_pkg_resources
(
)
.
WorkingSet
(
(
self
.
lib_path
)
)
        
return
self
.
_working_set
    
def
activate
(
self
)
:
        
if
sys
.
platform
=
=
"
darwin
"
:
            
os
.
environ
.
pop
(
"
__PYVENV_LAUNCHER__
"
None
)
        
paths
=
self
.
get_paths
(
)
        
bin_dir
=
paths
[
"
scripts
"
]
        
os
.
environ
[
"
PATH
"
]
=
os
.
pathsep
.
join
(
[
bin_dir
]
+
os
.
environ
.
get
(
"
PATH
"
"
"
)
.
split
(
os
.
pathsep
)
)
        
os
.
environ
[
"
VIRTUAL_ENV
"
]
=
self
.
path
        
prev_length
=
len
(
sys
.
path
)
        
for
key
in
[
"
purelib
"
"
platlib
"
]
:
            
site
.
addsitedir
(
paths
[
key
]
)
        
sys
.
path
[
:
]
=
sys
.
path
[
prev_length
:
]
+
sys
.
path
[
0
:
prev_length
]
        
sys
.
exec_prefix
=
self
.
path
        
sys
.
prefix
=
self
.
path
    
def
start
(
self
)
:
        
if
not
self
.
exists
or
self
.
broken_link
:
            
self
.
create
(
)
        
self
.
activate
(
)
    
def
install
(
self
*
requirements
)
:
        
try
:
            
self
.
working_set
.
require
(
*
requirements
)
        
except
Exception
:
            
pass
        
else
:
            
return
        
call
(
self
.
pip_path
"
install
"
"
-
-
prefer
-
binary
"
*
requirements
)
    
def
install_requirements
(
self
*
requirements_paths
)
:
        
install
=
[
]
        
for
requirements_path
in
requirements_paths
:
            
with
open
(
requirements_path
)
as
f
:
                
try
:
                    
self
.
working_set
.
require
(
f
.
read
(
)
)
                
except
Exception
:
                    
install
.
append
(
requirements_path
)
        
if
install
:
            
cmd
=
[
self
.
pip_path
"
install
"
"
-
-
prefer
-
binary
"
]
            
for
path
in
install
:
                
cmd
.
extend
(
[
"
-
r
"
path
]
)
            
call
(
*
cmd
)
