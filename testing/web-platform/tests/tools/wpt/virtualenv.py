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
pathlib
import
Path
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
    
property
    
def
bin_path
(
self
)
:
        
if
sys
.
platform
in
(
"
win32
"
"
cygwin
"
)
:
            
return
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
Scripts
"
)
        
return
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
bin
"
)
    
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
        
base
=
self
.
path
        
IS_PYPY
=
hasattr
(
sys
"
pypy_version_info
"
)
        
IS_JYTHON
=
sys
.
platform
.
startswith
(
"
java
"
)
        
if
IS_JYTHON
:
            
site_packages
=
os
.
path
.
join
(
base
"
Lib
"
"
site
-
packages
"
)
        
elif
IS_PYPY
:
            
site_packages
=
os
.
path
.
join
(
base
"
site
-
packages
"
)
        
else
:
            
IS_WIN
=
sys
.
platform
=
=
"
win32
"
            
if
IS_WIN
:
                
site_packages
=
os
.
path
.
join
(
base
"
Lib
"
"
site
-
packages
"
)
            
else
:
                
version
=
f
"
{
sys
.
version_info
.
major
}
.
{
sys
.
version_info
.
minor
}
"
                
site_packages
=
os
.
path
.
join
(
base
"
lib
"
f
"
python
{
version
}
"
"
site
-
packages
"
)
        
return
site_packages
    
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
'
darwin
'
:
            
os
.
environ
.
pop
(
'
__PYVENV_LAUNCHER__
'
None
)
        
bin_dir
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
bin
"
)
        
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
        
schemes
=
sysconfig
.
get_scheme_names
(
)
        
if
"
venv
"
in
schemes
:
            
scheme
=
"
venv
"
        
else
:
            
scheme
=
"
nt
"
if
os
.
name
=
=
"
nt
"
else
"
posix_user
"
        
sys_paths
=
sysconfig
.
get_paths
(
scheme
)
        
data_path
=
sys_paths
[
"
data
"
]
        
added
=
set
(
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
            
host_path
=
Path
(
sys_paths
[
key
]
)
            
relative_path
=
host_path
.
relative_to
(
data_path
)
            
site_dir
=
os
.
path
.
normpath
(
os
.
path
.
normcase
(
Path
(
self
.
path
)
/
relative_path
)
)
            
if
site_dir
not
in
added
:
                
site
.
addsitedir
(
site_dir
)
                
added
.
add
(
site_dir
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
real_prefix
=
sys
.
prefix
        
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
