"
"
"
Orchestrator
for
building
wheels
from
InstallRequirements
.
"
"
"
import
logging
import
os
.
path
import
re
import
shutil
from
pipenv
.
patched
.
notpip
.
_internal
.
models
.
link
import
Link
from
pipenv
.
patched
.
notpip
.
_internal
.
operations
.
build
.
wheel
import
build_wheel_pep517
from
pipenv
.
patched
.
notpip
.
_internal
.
operations
.
build
.
wheel_legacy
import
build_wheel_legacy
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
logging
import
indent_log
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
misc
import
ensure_dir
hash_file
is_wheel_installed
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
setuptools_build
import
make_setuptools_clean_args
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
subprocess
import
call_subprocess
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
temp_dir
import
TempDirectory
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
typing
import
MYPY_CHECK_RUNNING
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
urls
import
path_to_url
from
pipenv
.
patched
.
notpip
.
_internal
.
vcs
import
vcs
if
MYPY_CHECK_RUNNING
:
    
from
typing
import
(
        
Any
Callable
Iterable
List
Optional
Pattern
Tuple
    
)
    
from
pipenv
.
patched
.
notpip
.
_internal
.
cache
import
WheelCache
    
from
pipenv
.
patched
.
notpip
.
_internal
.
req
.
req_install
import
InstallRequirement
    
BinaryAllowedPredicate
=
Callable
[
[
InstallRequirement
]
bool
]
    
BuildResult
=
Tuple
[
List
[
InstallRequirement
]
List
[
InstallRequirement
]
]
logger
=
logging
.
getLogger
(
__name__
)
def
_contains_egg_info
(
        
s
_egg_info_re
=
re
.
compile
(
r
'
(
[
a
-
z0
-
9_
.
]
+
)
-
(
[
a
-
z0
-
9_
.
!
+
-
]
+
)
'
re
.
I
)
)
:
    
"
"
"
Determine
whether
the
string
looks
like
an
egg_info
.
    
:
param
s
:
The
string
to
parse
.
E
.
g
.
foo
-
2
.
1
    
"
"
"
    
return
bool
(
_egg_info_re
.
search
(
s
)
)
def
_should_build
(
    
req
    
need_wheel
    
check_binary_allowed
)
:
    
"
"
"
Return
whether
an
InstallRequirement
should
be
built
into
a
wheel
.
"
"
"
    
if
req
.
constraint
:
        
return
False
    
if
req
.
is_wheel
:
        
if
need_wheel
:
            
logger
.
info
(
                
'
Skipping
%
s
due
to
already
being
wheel
.
'
req
.
name
            
)
        
return
False
    
if
need_wheel
:
        
return
True
    
if
not
req
.
use_pep517
and
not
is_wheel_installed
(
)
:
        
return
False
    
if
req
.
editable
or
not
req
.
source_dir
:
        
return
False
    
if
not
check_binary_allowed
(
req
)
:
        
logger
.
info
(
            
"
Skipping
wheel
build
for
%
s
due
to
binaries
"
            
"
being
disabled
for
it
.
"
req
.
name
        
)
        
return
False
    
return
True
def
should_build_for_wheel_command
(
    
req
)
:
    
return
_should_build
(
        
req
need_wheel
=
True
check_binary_allowed
=
_always_true
    
)
def
should_build_for_install_command
(
    
req
    
check_binary_allowed
)
:
    
return
_should_build
(
        
req
need_wheel
=
False
check_binary_allowed
=
check_binary_allowed
    
)
def
_should_cache
(
    
req
)
:
    
"
"
"
    
Return
whether
a
built
InstallRequirement
can
be
stored
in
the
persistent
    
wheel
cache
assuming
the
wheel
cache
is
available
and
_should_build
(
)
    
has
determined
a
wheel
needs
to
be
built
.
    
"
"
"
    
if
not
should_build_for_install_command
(
        
req
check_binary_allowed
=
_always_true
    
)
:
        
return
False
    
if
req
.
link
and
req
.
link
.
is_vcs
:
        
assert
not
req
.
editable
        
assert
req
.
source_dir
        
vcs_backend
=
vcs
.
get_backend_for_scheme
(
req
.
link
.
scheme
)
        
assert
vcs_backend
        
if
vcs_backend
.
is_immutable_rev_checkout
(
req
.
link
.
url
req
.
source_dir
)
:
            
return
True
        
return
False
    
base
ext
=
req
.
link
.
splitext
(
)
    
if
_contains_egg_info
(
base
)
:
        
return
True
    
return
False
def
_get_cache_dir
(
    
req
    
wheel_cache
)
:
    
"
"
"
Return
the
persistent
or
temporary
cache
directory
where
the
built
    
wheel
need
to
be
stored
.
    
"
"
"
    
cache_available
=
bool
(
wheel_cache
.
cache_dir
)
    
if
cache_available
and
_should_cache
(
req
)
:
        
cache_dir
=
wheel_cache
.
get_path_for_link
(
req
.
link
)
    
else
:
        
cache_dir
=
wheel_cache
.
get_ephem_path_for_link
(
req
.
link
)
    
return
cache_dir
def
_always_true
(
_
)
:
    
return
True
def
_build_one
(
    
req
    
output_dir
    
build_options
    
global_options
)
:
    
"
"
"
Build
one
wheel
.
    
:
return
:
The
filename
of
the
built
wheel
or
None
if
the
build
failed
.
    
"
"
"
    
try
:
        
ensure_dir
(
output_dir
)
    
except
OSError
as
e
:
        
logger
.
warning
(
            
"
Building
wheel
for
%
s
failed
:
%
s
"
            
req
.
name
e
        
)
        
return
None
    
with
req
.
build_env
:
        
return
_build_one_inside_env
(
            
req
output_dir
build_options
global_options
        
)
def
_build_one_inside_env
(
    
req
    
output_dir
    
build_options
    
global_options
)
:
    
with
TempDirectory
(
kind
=
"
wheel
"
)
as
temp_dir
:
        
if
req
.
use_pep517
:
            
wheel_path
=
build_wheel_pep517
(
                
name
=
req
.
name
                
backend
=
req
.
pep517_backend
                
metadata_directory
=
req
.
metadata_directory
                
build_options
=
build_options
                
tempd
=
temp_dir
.
path
            
)
        
else
:
            
wheel_path
=
build_wheel_legacy
(
                
name
=
req
.
name
                
setup_py_path
=
req
.
setup_py_path
                
source_dir
=
req
.
unpacked_source_directory
                
global_options
=
global_options
                
build_options
=
build_options
                
tempd
=
temp_dir
.
path
            
)
        
if
wheel_path
is
not
None
:
            
wheel_name
=
os
.
path
.
basename
(
wheel_path
)
            
dest_path
=
os
.
path
.
join
(
output_dir
wheel_name
)
            
try
:
                
wheel_hash
length
=
hash_file
(
wheel_path
)
                
shutil
.
move
(
wheel_path
dest_path
)
                
logger
.
info
(
'
Created
wheel
for
%
s
:
'
                            
'
filename
=
%
s
size
=
%
d
sha256
=
%
s
'
                            
req
.
name
wheel_name
length
                            
wheel_hash
.
hexdigest
(
)
)
                
logger
.
info
(
'
Stored
in
directory
:
%
s
'
output_dir
)
                
return
dest_path
            
except
Exception
as
e
:
                
logger
.
warning
(
                    
"
Building
wheel
for
%
s
failed
:
%
s
"
                    
req
.
name
e
                
)
        
if
not
req
.
use_pep517
:
            
_clean_one_legacy
(
req
global_options
)
        
return
None
def
_clean_one_legacy
(
req
global_options
)
:
    
clean_args
=
make_setuptools_clean_args
(
        
req
.
setup_py_path
        
global_options
=
global_options
    
)
    
logger
.
info
(
'
Running
setup
.
py
clean
for
%
s
'
req
.
name
)
    
try
:
        
call_subprocess
(
clean_args
cwd
=
req
.
source_dir
)
        
return
True
    
except
Exception
:
        
logger
.
error
(
'
Failed
cleaning
build
dir
for
%
s
'
req
.
name
)
        
return
False
def
build
(
    
requirements
    
wheel_cache
    
build_options
    
global_options
)
:
    
"
"
"
Build
wheels
.
    
:
return
:
The
list
of
InstallRequirement
that
succeeded
to
build
and
        
the
list
of
InstallRequirement
that
failed
to
build
.
    
"
"
"
    
if
not
requirements
:
        
return
[
]
[
]
    
logger
.
info
(
        
'
Building
wheels
for
collected
packages
:
%
s
'
        
'
'
.
join
(
req
.
name
for
req
in
requirements
)
    
)
    
with
indent_log
(
)
:
        
build_successes
build_failures
=
[
]
[
]
        
for
req
in
requirements
:
            
cache_dir
=
_get_cache_dir
(
req
wheel_cache
)
            
wheel_file
=
_build_one
(
                
req
cache_dir
build_options
global_options
            
)
            
if
wheel_file
:
                
req
.
link
=
Link
(
path_to_url
(
wheel_file
)
)
                
req
.
local_file_path
=
req
.
link
.
file_path
                
assert
req
.
link
.
is_wheel
                
build_successes
.
append
(
req
)
            
else
:
                
build_failures
.
append
(
req
)
    
if
build_successes
:
        
logger
.
info
(
            
'
Successfully
built
%
s
'
            
'
'
.
join
(
[
req
.
name
for
req
in
build_successes
]
)
        
)
    
if
build_failures
:
        
logger
.
info
(
            
'
Failed
to
build
%
s
'
            
'
'
.
join
(
[
req
.
name
for
req
in
build_failures
]
)
        
)
    
return
build_successes
build_failures
