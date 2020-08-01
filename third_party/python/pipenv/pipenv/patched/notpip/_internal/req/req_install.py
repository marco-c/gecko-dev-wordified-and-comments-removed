from
__future__
import
absolute_import
import
logging
import
os
import
shutil
import
sys
import
zipfile
from
pipenv
.
patched
.
notpip
.
_vendor
import
pkg_resources
six
from
pipenv
.
patched
.
notpip
.
_vendor
.
packaging
.
requirements
import
Requirement
from
pipenv
.
patched
.
notpip
.
_vendor
.
packaging
.
utils
import
canonicalize_name
from
pipenv
.
patched
.
notpip
.
_vendor
.
packaging
.
version
import
Version
from
pipenv
.
patched
.
notpip
.
_vendor
.
packaging
.
version
import
parse
as
parse_version
from
pipenv
.
patched
.
notpip
.
_vendor
.
pep517
.
wrappers
import
Pep517HookCaller
from
pipenv
.
patched
.
notpip
.
_internal
import
pep425tags
from
pipenv
.
patched
.
notpip
.
_internal
.
build_env
import
NoOpBuildEnvironment
from
pipenv
.
patched
.
notpip
.
_internal
.
exceptions
import
InstallationError
from
pipenv
.
patched
.
notpip
.
_internal
.
locations
import
get_scheme
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
metadata
import
generate_metadata
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
metadata_legacy
import
\
    
generate_metadata
as
generate_metadata_legacy
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
install
.
editable_legacy
import
\
    
install_editable
as
install_editable_legacy
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
install
.
legacy
import
install
as
install_legacy
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
install
.
wheel
import
install_wheel
from
pipenv
.
patched
.
notpip
.
_internal
.
pyproject
import
load_pyproject_toml
make_pyproject_path
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
req_uninstall
import
UninstallPathSet
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
deprecation
import
deprecated
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
hashes
import
Hashes
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
marker_files
import
(
    
PIP_DELETE_MARKER_FILENAME
    
has_delete_marker_file
    
write_delete_marker_file
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
utils
.
misc
import
(
    
ask_path_exists
    
backup_dir
    
display_path
    
dist_in_site_packages
    
dist_in_usersite
    
get_installed_version
    
hide_url
    
redact_auth_from_url
    
rmtree
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
utils
.
packaging
import
get_metadata
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
virtualenv
import
running_under_virtualenv
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
Dict
Iterable
List
Optional
Sequence
Union
    
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
build_env
import
BuildEnvironment
    
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
index
.
package_finder
import
PackageFinder
    
from
pipenv
.
patched
.
notpip
.
_vendor
.
pkg_resources
import
Distribution
    
from
pipenv
.
patched
.
notpip
.
_vendor
.
packaging
.
specifiers
import
SpecifierSet
    
from
pipenv
.
patched
.
notpip
.
_vendor
.
packaging
.
markers
import
Marker
logger
=
logging
.
getLogger
(
__name__
)
def
_get_dist
(
metadata_directory
)
:
    
"
"
"
Return
a
pkg_resources
.
Distribution
for
the
provided
    
metadata
directory
.
    
"
"
"
    
dist_dir
=
metadata_directory
.
rstrip
(
os
.
sep
)
    
if
dist_dir
.
endswith
(
"
.
egg
-
info
"
)
:
        
dist_cls
=
pkg_resources
.
Distribution
    
else
:
        
assert
dist_dir
.
endswith
(
"
.
dist
-
info
"
)
        
dist_cls
=
pkg_resources
.
DistInfoDistribution
    
base_dir
dist_dir_name
=
os
.
path
.
split
(
dist_dir
)
    
dist_name
=
os
.
path
.
splitext
(
dist_dir_name
)
[
0
]
    
metadata
=
pkg_resources
.
PathMetadata
(
base_dir
dist_dir
)
    
return
dist_cls
(
        
base_dir
        
project_name
=
dist_name
        
metadata
=
metadata
    
)
class
InstallRequirement
(
object
)
:
    
"
"
"
    
Represents
something
that
may
be
installed
later
on
may
have
information
    
about
where
to
fetch
the
relevant
requirement
and
also
contains
logic
for
    
installing
the
said
requirement
.
    
"
"
"
    
def
__init__
(
        
self
        
req
        
comes_from
        
source_dir
=
None
        
editable
=
False
        
link
=
None
        
markers
=
None
        
use_pep517
=
None
        
isolated
=
False
        
options
=
None
        
wheel_cache
=
None
        
constraint
=
False
        
extras
=
(
)
    
)
:
        
assert
req
is
None
or
isinstance
(
req
Requirement
)
req
        
self
.
req
=
req
        
self
.
comes_from
=
comes_from
        
self
.
constraint
=
constraint
        
if
source_dir
is
None
:
            
self
.
source_dir
=
None
        
else
:
            
self
.
source_dir
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
abspath
(
source_dir
)
)
        
self
.
editable
=
editable
        
self
.
_wheel_cache
=
wheel_cache
        
if
link
is
None
and
req
and
req
.
url
:
            
link
=
Link
(
req
.
url
)
        
self
.
link
=
self
.
original_link
=
link
        
self
.
local_file_path
=
None
        
if
self
.
link
and
self
.
link
.
is_file
:
            
self
.
local_file_path
=
self
.
link
.
file_path
        
if
extras
:
            
self
.
extras
=
extras
        
elif
req
:
            
self
.
extras
=
{
                
pkg_resources
.
safe_extra
(
extra
)
for
extra
in
req
.
extras
            
}
        
else
:
            
self
.
extras
=
set
(
)
        
if
markers
is
None
and
req
:
            
markers
=
req
.
marker
        
self
.
markers
=
markers
        
self
.
satisfied_by
=
None
        
self
.
should_reinstall
=
False
        
self
.
_temp_build_dir
=
None
        
self
.
install_succeeded
=
None
        
self
.
options
=
options
if
options
else
{
}
        
self
.
prepared
=
False
        
self
.
is_direct
=
False
        
self
.
isolated
=
isolated
        
self
.
build_env
=
NoOpBuildEnvironment
(
)
        
self
.
metadata_directory
=
None
        
self
.
pyproject_requires
=
None
        
self
.
requirements_to_check
=
[
]
        
self
.
pep517_backend
=
None
        
self
.
use_pep517
=
use_pep517
    
def
__str__
(
self
)
:
        
if
self
.
req
:
            
s
=
str
(
self
.
req
)
            
if
self
.
link
:
                
s
+
=
'
from
%
s
'
%
redact_auth_from_url
(
self
.
link
.
url
)
        
elif
self
.
link
:
            
s
=
redact_auth_from_url
(
self
.
link
.
url
)
        
else
:
            
s
=
'
<
InstallRequirement
>
'
        
if
self
.
satisfied_by
is
not
None
:
            
s
+
=
'
in
%
s
'
%
display_path
(
self
.
satisfied_by
.
location
)
        
if
self
.
comes_from
:
            
if
isinstance
(
self
.
comes_from
six
.
string_types
)
:
                
comes_from
=
self
.
comes_from
            
else
:
                
comes_from
=
self
.
comes_from
.
from_path
(
)
            
if
comes_from
:
                
s
+
=
'
(
from
%
s
)
'
%
comes_from
        
return
s
    
def
__repr__
(
self
)
:
        
return
'
<
%
s
object
:
%
s
editable
=
%
r
>
'
%
(
            
self
.
__class__
.
__name__
str
(
self
)
self
.
editable
)
    
def
format_debug
(
self
)
:
        
"
"
"
An
un
-
tested
helper
for
getting
state
for
debugging
.
        
"
"
"
        
attributes
=
vars
(
self
)
        
names
=
sorted
(
attributes
)
        
state
=
(
            
"
{
}
=
{
!
r
}
"
.
format
(
attr
attributes
[
attr
]
)
for
attr
in
sorted
(
names
)
        
)
        
return
'
<
{
name
}
object
:
{
{
{
state
}
}
}
>
'
.
format
(
            
name
=
self
.
__class__
.
__name__
            
state
=
"
"
.
join
(
state
)
        
)
    
def
populate_link
(
self
finder
upgrade
require_hashes
)
:
        
"
"
"
Ensure
that
if
a
link
can
be
found
for
this
that
it
is
found
.
        
Note
that
self
.
link
may
still
be
None
-
if
Upgrade
is
False
and
the
        
requirement
is
already
installed
.
        
If
require_hashes
is
True
don
'
t
use
the
wheel
cache
because
cached
        
wheels
always
built
locally
have
different
hashes
than
the
files
        
downloaded
from
the
index
server
and
thus
throw
false
hash
mismatches
.
        
Furthermore
cached
wheels
at
present
have
undeterministic
contents
due
        
to
file
modification
times
.
        
"
"
"
        
if
self
.
link
is
None
:
            
self
.
link
=
finder
.
find_requirement
(
self
upgrade
)
        
if
self
.
_wheel_cache
is
not
None
and
not
require_hashes
:
            
old_link
=
self
.
link
            
supported_tags
=
pep425tags
.
get_supported
(
)
            
self
.
link
=
self
.
_wheel_cache
.
get
(
                
link
=
self
.
link
                
package_name
=
self
.
name
                
supported_tags
=
supported_tags
            
)
            
if
old_link
!
=
self
.
link
:
                
logger
.
debug
(
'
Using
cached
wheel
link
:
%
s
'
self
.
link
)
    
property
    
def
name
(
self
)
:
        
if
self
.
req
is
None
:
            
return
None
        
return
six
.
ensure_str
(
pkg_resources
.
safe_name
(
self
.
req
.
name
)
)
    
property
    
def
specifier
(
self
)
:
        
return
self
.
req
.
specifier
    
property
    
def
is_pinned
(
self
)
:
        
"
"
"
Return
whether
I
am
pinned
to
an
exact
version
.
        
For
example
some
-
package
=
=
1
.
2
is
pinned
;
some
-
package
>
1
.
2
is
not
.
        
"
"
"
        
specifiers
=
self
.
specifier
        
return
(
len
(
specifiers
)
=
=
1
and
                
next
(
iter
(
specifiers
)
)
.
operator
in
{
'
=
=
'
'
=
=
=
'
}
)
    
property
    
def
installed_version
(
self
)
:
        
return
get_installed_version
(
self
.
name
)
    
def
match_markers
(
self
extras_requested
=
None
)
:
        
if
not
extras_requested
:
            
extras_requested
=
(
'
'
)
        
if
self
.
markers
is
not
None
:
            
return
any
(
                
self
.
markers
.
evaluate
(
{
'
extra
'
:
extra
}
)
                
for
extra
in
extras_requested
)
        
else
:
            
return
True
    
property
    
def
has_hash_options
(
self
)
:
        
"
"
"
Return
whether
any
known
-
good
hashes
are
specified
as
options
.
        
These
activate
-
-
require
-
hashes
mode
;
hashes
specified
as
part
of
a
        
URL
do
not
.
        
"
"
"
        
return
bool
(
self
.
options
.
get
(
'
hashes
'
{
}
)
)
    
def
hashes
(
self
trust_internet
=
True
)
:
        
"
"
"
Return
a
hash
-
comparer
that
considers
my
option
-
and
URL
-
based
        
hashes
to
be
known
-
good
.
        
Hashes
in
URLs
-
-
ones
embedded
in
the
requirements
file
not
ones
        
downloaded
from
an
index
server
-
-
are
almost
peers
with
ones
from
        
flags
.
They
satisfy
-
-
require
-
hashes
(
whether
it
was
implicitly
or
        
explicitly
activated
)
but
do
not
activate
it
.
md5
and
sha224
are
not
        
allowed
in
flags
which
should
nudge
people
toward
good
algos
.
We
        
always
OR
all
hashes
together
even
ones
from
URLs
.
        
:
param
trust_internet
:
Whether
to
trust
URL
-
based
(
#
md5
=
.
.
.
)
hashes
            
downloaded
from
the
internet
as
by
populate_link
(
)
        
"
"
"
        
good_hashes
=
self
.
options
.
get
(
'
hashes
'
{
}
)
.
copy
(
)
        
link
=
self
.
link
if
trust_internet
else
self
.
original_link
        
if
link
and
link
.
hash
:
            
good_hashes
.
setdefault
(
link
.
hash_name
[
]
)
.
append
(
link
.
hash
)
        
return
Hashes
(
good_hashes
)
    
def
from_path
(
self
)
:
        
"
"
"
Format
a
nice
indicator
to
show
where
this
"
comes
from
"
        
"
"
"
        
if
self
.
req
is
None
:
            
return
None
        
s
=
str
(
self
.
req
)
        
if
self
.
comes_from
:
            
if
isinstance
(
self
.
comes_from
six
.
string_types
)
:
                
comes_from
=
self
.
comes_from
            
else
:
                
comes_from
=
self
.
comes_from
.
from_path
(
)
            
if
comes_from
:
                
s
+
=
'
-
>
'
+
comes_from
        
return
s
    
def
ensure_build_location
(
self
build_dir
)
:
        
assert
build_dir
is
not
None
        
if
self
.
_temp_build_dir
is
not
None
:
            
assert
self
.
_temp_build_dir
.
path
            
return
self
.
_temp_build_dir
.
path
        
if
self
.
req
is
None
:
            
self
.
_temp_build_dir
=
TempDirectory
(
kind
=
"
req
-
build
"
)
            
return
self
.
_temp_build_dir
.
path
        
if
self
.
editable
:
            
name
=
self
.
name
.
lower
(
)
        
else
:
            
name
=
self
.
name
        
if
not
os
.
path
.
exists
(
build_dir
)
:
            
logger
.
debug
(
'
Creating
directory
%
s
'
build_dir
)
            
os
.
makedirs
(
build_dir
)
            
write_delete_marker_file
(
build_dir
)
        
return
os
.
path
.
join
(
build_dir
name
)
    
def
_set_requirement
(
self
)
:
        
"
"
"
Set
requirement
after
generating
metadata
.
        
"
"
"
        
assert
self
.
req
is
None
        
assert
self
.
metadata
is
not
None
        
assert
self
.
source_dir
is
not
None
        
if
isinstance
(
parse_version
(
self
.
metadata
[
"
Version
"
]
)
Version
)
:
            
op
=
"
=
=
"
        
else
:
            
op
=
"
=
=
=
"
        
self
.
req
=
Requirement
(
            
"
"
.
join
(
[
                
self
.
metadata
[
"
Name
"
]
                
op
                
self
.
metadata
[
"
Version
"
]
            
]
)
        
)
    
def
warn_on_mismatching_name
(
self
)
:
        
metadata_name
=
canonicalize_name
(
self
.
metadata
[
"
Name
"
]
)
        
if
canonicalize_name
(
self
.
req
.
name
)
=
=
metadata_name
:
            
return
        
logger
.
warning
(
            
'
Generating
metadata
for
package
%
s
'
            
'
produced
metadata
for
project
name
%
s
.
Fix
your
'
            
'
#
egg
=
%
s
fragments
.
'
            
self
.
name
metadata_name
self
.
name
        
)
        
self
.
req
=
Requirement
(
metadata_name
)
    
def
remove_temporary_source
(
self
)
:
        
"
"
"
Remove
the
source
files
from
this
requirement
if
they
are
marked
        
for
deletion
"
"
"
        
if
self
.
source_dir
and
has_delete_marker_file
(
self
.
source_dir
)
:
            
logger
.
debug
(
'
Removing
source
in
%
s
'
self
.
source_dir
)
            
rmtree
(
self
.
source_dir
)
        
self
.
source_dir
=
None
        
if
self
.
_temp_build_dir
:
            
self
.
_temp_build_dir
.
cleanup
(
)
            
self
.
_temp_build_dir
=
None
        
self
.
build_env
.
cleanup
(
)
    
def
check_if_exists
(
self
use_user_site
)
:
        
"
"
"
Find
an
installed
distribution
that
satisfies
or
conflicts
        
with
this
requirement
and
set
self
.
satisfied_by
or
        
self
.
should_reinstall
appropriately
.
        
"
"
"
        
if
self
.
req
is
None
:
            
return
        
no_marker
=
Requirement
(
str
(
self
.
req
)
)
        
no_marker
.
marker
=
None
        
try
:
            
self
.
satisfied_by
=
pkg_resources
.
get_distribution
(
str
(
no_marker
)
)
        
except
pkg_resources
.
DistributionNotFound
:
            
return
        
except
pkg_resources
.
VersionConflict
:
            
existing_dist
=
pkg_resources
.
get_distribution
(
                
self
.
req
.
name
            
)
            
if
use_user_site
:
                
if
dist_in_usersite
(
existing_dist
)
:
                    
self
.
should_reinstall
=
True
                
elif
(
running_under_virtualenv
(
)
and
                        
dist_in_site_packages
(
existing_dist
)
)
:
                    
raise
InstallationError
(
                        
"
Will
not
install
to
the
user
site
because
it
will
"
                        
"
lack
sys
.
path
precedence
to
%
s
in
%
s
"
%
                        
(
existing_dist
.
project_name
existing_dist
.
location
)
                    
)
            
else
:
                
self
.
should_reinstall
=
True
        
else
:
            
if
self
.
editable
and
self
.
satisfied_by
:
                
self
.
should_reinstall
=
True
                
self
.
satisfied_by
=
None
    
property
    
def
is_wheel
(
self
)
:
        
if
not
self
.
link
:
            
return
False
        
return
self
.
link
.
is_wheel
    
property
    
def
unpacked_source_directory
(
self
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
source_dir
            
self
.
link
and
self
.
link
.
subdirectory_fragment
or
'
'
)
    
property
    
def
setup_py_path
(
self
)
:
        
assert
self
.
source_dir
"
No
source
dir
for
%
s
"
%
self
        
setup_py
=
os
.
path
.
join
(
self
.
unpacked_source_directory
'
setup
.
py
'
)
        
if
six
.
PY2
and
isinstance
(
setup_py
six
.
text_type
)
:
            
setup_py
=
setup_py
.
encode
(
sys
.
getfilesystemencoding
(
)
)
        
return
setup_py
    
property
    
def
pyproject_toml_path
(
self
)
:
        
assert
self
.
source_dir
"
No
source
dir
for
%
s
"
%
self
        
return
make_pyproject_path
(
self
.
unpacked_source_directory
)
    
def
load_pyproject_toml
(
self
)
:
        
"
"
"
Load
the
pyproject
.
toml
file
.
        
After
calling
this
routine
all
of
the
attributes
related
to
PEP
517
        
processing
for
this
requirement
have
been
set
.
In
particular
the
        
use_pep517
attribute
can
be
used
to
determine
whether
we
should
        
follow
the
PEP
517
or
legacy
(
setup
.
py
)
code
path
.
        
"
"
"
        
pyproject_toml_data
=
load_pyproject_toml
(
            
self
.
use_pep517
            
self
.
pyproject_toml_path
            
self
.
setup_py_path
            
str
(
self
)
        
)
        
if
pyproject_toml_data
is
None
:
            
self
.
use_pep517
=
False
            
return
        
self
.
use_pep517
=
True
        
requires
backend
check
backend_path
=
pyproject_toml_data
        
self
.
requirements_to_check
=
check
        
self
.
pyproject_requires
=
requires
        
self
.
pep517_backend
=
Pep517HookCaller
(
            
self
.
unpacked_source_directory
backend
backend_path
=
backend_path
        
)
    
def
_generate_metadata
(
self
)
:
        
"
"
"
Invokes
metadata
generator
functions
with
the
required
arguments
.
        
"
"
"
        
if
not
self
.
use_pep517
:
            
assert
self
.
unpacked_source_directory
            
return
generate_metadata_legacy
(
                
build_env
=
self
.
build_env
                
setup_py_path
=
self
.
setup_py_path
                
source_dir
=
self
.
unpacked_source_directory
                
editable
=
self
.
editable
                
isolated
=
self
.
isolated
                
details
=
self
.
name
or
"
from
{
}
"
.
format
(
self
.
link
)
            
)
        
assert
self
.
pep517_backend
is
not
None
        
return
generate_metadata
(
            
build_env
=
self
.
build_env
            
backend
=
self
.
pep517_backend
        
)
    
def
prepare_metadata
(
self
)
:
        
"
"
"
Ensure
that
project
metadata
is
available
.
        
Under
PEP
517
call
the
backend
hook
to
prepare
the
metadata
.
        
Under
legacy
processing
call
setup
.
py
egg
-
info
.
        
"
"
"
        
assert
self
.
source_dir
        
with
indent_log
(
)
:
            
self
.
metadata_directory
=
self
.
_generate_metadata
(
)
        
if
not
self
.
name
:
            
self
.
_set_requirement
(
)
        
else
:
            
self
.
warn_on_mismatching_name
(
)
        
self
.
assert_source_matches_version
(
)
    
property
    
def
metadata
(
self
)
:
        
if
not
hasattr
(
self
'
_metadata
'
)
:
            
self
.
_metadata
=
get_metadata
(
self
.
get_dist
(
)
)
        
return
self
.
_metadata
    
def
get_dist
(
self
)
:
        
return
_get_dist
(
self
.
metadata_directory
)
    
def
assert_source_matches_version
(
self
)
:
        
assert
self
.
source_dir
        
version
=
self
.
metadata
[
'
version
'
]
        
if
self
.
req
.
specifier
and
version
not
in
self
.
req
.
specifier
:
            
logger
.
warning
(
                
'
Requested
%
s
but
installing
version
%
s
'
                
self
                
version
            
)
        
else
:
            
logger
.
debug
(
                
'
Source
in
%
s
has
version
%
s
which
satisfies
requirement
%
s
'
                
display_path
(
self
.
source_dir
)
                
version
                
self
            
)
    
def
ensure_has_source_dir
(
self
parent_dir
)
:
        
"
"
"
Ensure
that
a
source_dir
is
set
.
        
This
will
create
a
temporary
build
dir
if
the
name
of
the
requirement
        
isn
'
t
known
yet
.
        
:
param
parent_dir
:
The
ideal
pip
parent_dir
for
the
source_dir
.
            
Generally
src_dir
for
editables
and
build_dir
for
sdists
.
        
:
return
:
self
.
source_dir
        
"
"
"
        
if
self
.
source_dir
is
None
:
            
self
.
source_dir
=
self
.
ensure_build_location
(
parent_dir
)
    
def
update_editable
(
self
obtain
=
True
)
:
        
if
not
self
.
link
:
            
logger
.
debug
(
                
"
Cannot
update
repository
at
%
s
;
repository
location
is
"
                
"
unknown
"
                
self
.
source_dir
            
)
            
return
        
assert
self
.
editable
        
assert
self
.
source_dir
        
if
self
.
link
.
scheme
=
=
'
file
'
:
            
return
        
assert
'
+
'
in
self
.
link
.
url
"
bad
url
:
%
r
"
%
self
.
link
.
url
        
vc_type
url
=
self
.
link
.
url
.
split
(
'
+
'
1
)
        
vcs_backend
=
vcs
.
get_backend
(
vc_type
)
        
if
vcs_backend
:
            
if
not
self
.
link
.
is_vcs
:
                
reason
=
(
                    
"
This
form
of
VCS
requirement
is
being
deprecated
:
{
}
.
"
                
)
.
format
(
                    
self
.
link
.
url
                
)
                
replacement
=
None
                
if
self
.
link
.
url
.
startswith
(
"
git
+
git
"
)
:
                    
replacement
=
(
                        
"
git
+
https
:
/
/
git
example
.
com
/
.
.
.
"
                        
"
git
+
ssh
:
/
/
git
example
.
com
/
.
.
.
"
                        
"
or
the
insecure
git
+
git
:
/
/
git
example
.
com
/
.
.
.
"
                    
)
                
deprecated
(
reason
replacement
gone_in
=
"
21
.
0
"
issue
=
7554
)
            
hidden_url
=
hide_url
(
self
.
link
.
url
)
            
if
obtain
:
                
vcs_backend
.
obtain
(
self
.
source_dir
url
=
hidden_url
)
            
else
:
                
vcs_backend
.
export
(
self
.
source_dir
url
=
hidden_url
)
        
else
:
            
assert
0
(
                
'
Unexpected
version
control
type
(
in
%
s
)
:
%
s
'
                
%
(
self
.
link
vc_type
)
)
    
def
uninstall
(
self
auto_confirm
=
False
verbose
=
False
)
:
        
"
"
"
        
Uninstall
the
distribution
currently
satisfying
this
requirement
.
        
Prompts
before
removing
or
modifying
files
unless
        
auto_confirm
is
True
.
        
Refuses
to
delete
or
modify
files
outside
of
sys
.
prefix
-
        
thus
uninstallation
within
a
virtual
environment
can
only
        
modify
that
virtual
environment
even
if
the
virtualenv
is
        
linked
to
global
site
-
packages
.
        
"
"
"
        
assert
self
.
req
        
try
:
            
dist
=
pkg_resources
.
get_distribution
(
self
.
req
.
name
)
        
except
pkg_resources
.
DistributionNotFound
:
            
logger
.
warning
(
"
Skipping
%
s
as
it
is
not
installed
.
"
self
.
name
)
            
return
None
        
else
:
            
logger
.
info
(
'
Found
existing
installation
:
%
s
'
dist
)
        
uninstalled_pathset
=
UninstallPathSet
.
from_dist
(
dist
)
        
uninstalled_pathset
.
remove
(
auto_confirm
verbose
)
        
return
uninstalled_pathset
    
def
_get_archive_name
(
self
path
parentdir
rootdir
)
:
        
def
_clean_zip_name
(
name
prefix
)
:
            
assert
name
.
startswith
(
prefix
+
os
.
path
.
sep
)
(
                
"
name
%
r
doesn
'
t
start
with
prefix
%
r
"
%
(
name
prefix
)
            
)
            
name
=
name
[
len
(
prefix
)
+
1
:
]
            
name
=
name
.
replace
(
os
.
path
.
sep
'
/
'
)
            
return
name
        
path
=
os
.
path
.
join
(
parentdir
path
)
        
name
=
_clean_zip_name
(
path
rootdir
)
        
return
self
.
name
+
'
/
'
+
name
    
def
archive
(
self
build_dir
)
:
        
"
"
"
Saves
archive
to
provided
build_dir
.
        
Used
for
saving
downloaded
VCS
requirements
as
part
of
pip
download
.
        
"
"
"
        
assert
self
.
source_dir
        
create_archive
=
True
        
archive_name
=
'
%
s
-
%
s
.
zip
'
%
(
self
.
name
self
.
metadata
[
"
version
"
]
)
        
archive_path
=
os
.
path
.
join
(
build_dir
archive_name
)
        
if
os
.
path
.
exists
(
archive_path
)
:
            
response
=
ask_path_exists
(
                
'
The
file
%
s
exists
.
(
i
)
gnore
(
w
)
ipe
(
b
)
ackup
(
a
)
bort
'
%
                
display_path
(
archive_path
)
(
'
i
'
'
w
'
'
b
'
'
a
'
)
)
            
if
response
=
=
'
i
'
:
                
create_archive
=
False
            
elif
response
=
=
'
w
'
:
                
logger
.
warning
(
'
Deleting
%
s
'
display_path
(
archive_path
)
)
                
os
.
remove
(
archive_path
)
            
elif
response
=
=
'
b
'
:
                
dest_file
=
backup_dir
(
archive_path
)
                
logger
.
warning
(
                    
'
Backing
up
%
s
to
%
s
'
                    
display_path
(
archive_path
)
                    
display_path
(
dest_file
)
                
)
                
shutil
.
move
(
archive_path
dest_file
)
            
elif
response
=
=
'
a
'
:
                
sys
.
exit
(
-
1
)
        
if
not
create_archive
:
            
return
        
zip_output
=
zipfile
.
ZipFile
(
            
archive_path
'
w
'
zipfile
.
ZIP_DEFLATED
allowZip64
=
True
        
)
        
with
zip_output
:
            
dir
=
os
.
path
.
normcase
(
                
os
.
path
.
abspath
(
self
.
unpacked_source_directory
)
            
)
            
for
dirpath
dirnames
filenames
in
os
.
walk
(
dir
)
:
                
if
'
pip
-
egg
-
info
'
in
dirnames
:
                    
dirnames
.
remove
(
'
pip
-
egg
-
info
'
)
                
for
dirname
in
dirnames
:
                    
dir_arcname
=
self
.
_get_archive_name
(
                        
dirname
parentdir
=
dirpath
rootdir
=
dir
                    
)
                    
zipdir
=
zipfile
.
ZipInfo
(
dir_arcname
+
'
/
'
)
                    
zipdir
.
external_attr
=
0x1ED
<
<
16
                    
zip_output
.
writestr
(
zipdir
'
'
)
                
for
filename
in
filenames
:
                    
if
filename
=
=
PIP_DELETE_MARKER_FILENAME
:
                        
continue
                    
file_arcname
=
self
.
_get_archive_name
(
                        
filename
parentdir
=
dirpath
rootdir
=
dir
                    
)
                    
filename
=
os
.
path
.
join
(
dirpath
filename
)
                    
zip_output
.
write
(
filename
file_arcname
)
        
logger
.
info
(
'
Saved
%
s
'
display_path
(
archive_path
)
)
    
def
install
(
        
self
        
install_options
        
global_options
=
None
        
root
=
None
        
home
=
None
        
prefix
=
None
        
warn_script_location
=
True
        
use_user_site
=
False
        
pycompile
=
True
    
)
:
        
scheme
=
get_scheme
(
            
self
.
name
            
user
=
use_user_site
            
home
=
home
            
root
=
root
            
isolated
=
self
.
isolated
            
prefix
=
prefix
        
)
        
global_options
=
global_options
if
global_options
is
not
None
else
[
]
        
if
self
.
editable
:
            
install_editable_legacy
(
                
install_options
                
global_options
                
prefix
=
prefix
                
home
=
home
                
use_user_site
=
use_user_site
                
name
=
self
.
name
                
setup_py_path
=
self
.
setup_py_path
                
isolated
=
self
.
isolated
                
build_env
=
self
.
build_env
                
unpacked_source_directory
=
self
.
unpacked_source_directory
            
)
            
self
.
install_succeeded
=
True
            
return
        
if
self
.
is_wheel
:
            
assert
self
.
local_file_path
            
install_wheel
(
                
self
.
name
                
self
.
local_file_path
                
scheme
=
scheme
                
req_description
=
str
(
self
.
req
)
                
pycompile
=
pycompile
                
warn_script_location
=
warn_script_location
            
)
            
self
.
install_succeeded
=
True
            
return
        
install_legacy
(
            
self
            
install_options
=
install_options
            
global_options
=
global_options
            
root
=
root
            
home
=
home
            
prefix
=
prefix
            
use_user_site
=
use_user_site
            
pycompile
=
pycompile
            
scheme
=
scheme
        
)
