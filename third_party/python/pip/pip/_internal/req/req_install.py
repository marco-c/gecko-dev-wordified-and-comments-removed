import
logging
import
os
import
shutil
import
sys
import
uuid
import
zipfile
from
typing
import
Any
Dict
Iterable
List
Optional
Sequence
Union
from
pip
.
_vendor
import
pkg_resources
six
from
pip
.
_vendor
.
packaging
.
markers
import
Marker
from
pip
.
_vendor
.
packaging
.
requirements
import
Requirement
from
pip
.
_vendor
.
packaging
.
specifiers
import
SpecifierSet
from
pip
.
_vendor
.
packaging
.
utils
import
canonicalize_name
from
pip
.
_vendor
.
packaging
.
version
import
Version
from
pip
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
pip
.
_vendor
.
pep517
.
wrappers
import
Pep517HookCaller
from
pip
.
_vendor
.
pkg_resources
import
Distribution
from
pip
.
_internal
.
build_env
import
BuildEnvironment
NoOpBuildEnvironment
from
pip
.
_internal
.
exceptions
import
InstallationError
from
pip
.
_internal
.
locations
import
get_scheme
from
pip
.
_internal
.
models
.
link
import
Link
from
pip
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
pip
.
_internal
.
operations
.
build
.
metadata_legacy
import
(
    
generate_metadata
as
generate_metadata_legacy
)
from
pip
.
_internal
.
operations
.
install
.
editable_legacy
import
(
    
install_editable
as
install_editable_legacy
)
from
pip
.
_internal
.
operations
.
install
.
legacy
import
LegacyInstallFailure
from
pip
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
pip
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
pip
.
_internal
.
pyproject
import
load_pyproject_toml
make_pyproject_path
from
pip
.
_internal
.
req
.
req_uninstall
import
UninstallPathSet
from
pip
.
_internal
.
utils
.
deprecation
import
deprecated
from
pip
.
_internal
.
utils
.
direct_url_helpers
import
direct_url_from_link
from
pip
.
_internal
.
utils
.
hashes
import
Hashes
from
pip
.
_internal
.
utils
.
logging
import
indent_log
from
pip
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
    
get_distribution
    
hide_url
    
redact_auth_from_url
)
from
pip
.
_internal
.
utils
.
packaging
import
get_metadata
from
pip
.
_internal
.
utils
.
temp_dir
import
TempDirectory
tempdir_kinds
from
pip
.
_internal
.
utils
.
virtualenv
import
running_under_virtualenv
from
pip
.
_internal
.
vcs
import
vcs
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
:
str
)
-
>
Distribution
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
    
metadata
=
pkg_resources
.
PathMetadata
(
base_dir
dist_dir
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
.
split
(
"
-
"
)
[
0
]
    
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
:
Optional
[
Requirement
]
        
comes_from
:
Optional
[
Union
[
str
"
InstallRequirement
"
]
]
        
editable
:
bool
=
False
        
link
:
Optional
[
Link
]
=
None
        
markers
:
Optional
[
Marker
]
=
None
        
use_pep517
:
Optional
[
bool
]
=
None
        
isolated
:
bool
=
False
        
install_options
:
Optional
[
List
[
str
]
]
=
None
        
global_options
:
Optional
[
List
[
str
]
]
=
None
        
hash_options
:
Optional
[
Dict
[
str
List
[
str
]
]
]
=
None
        
constraint
:
bool
=
False
        
extras
:
Iterable
[
str
]
=
(
)
        
user_supplied
:
bool
=
False
    
)
-
>
None
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
        
self
.
editable
=
editable
        
self
.
legacy_install_reason
:
Optional
[
int
]
=
None
        
self
.
source_dir
:
Optional
[
str
]
=
None
        
if
self
.
editable
:
            
assert
link
            
if
link
.
is_file
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
link
.
file_path
)
                
)
        
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
original_link_is_in_wheel_cache
=
False
        
self
.
local_file_path
:
Optional
[
str
]
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
:
Optional
[
Distribution
]
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
:
Optional
[
TempDirectory
]
=
None
        
self
.
install_succeeded
:
Optional
[
bool
]
=
None
        
self
.
install_options
=
install_options
if
install_options
else
[
]
        
self
.
global_options
=
global_options
if
global_options
else
[
]
        
self
.
hash_options
=
hash_options
if
hash_options
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
user_supplied
=
user_supplied
        
self
.
isolated
=
isolated
        
self
.
build_env
:
BuildEnvironment
=
NoOpBuildEnvironment
(
)
        
self
.
metadata_directory
:
Optional
[
str
]
=
None
        
self
.
pyproject_requires
:
Optional
[
List
[
str
]
]
=
None
        
self
.
requirements_to_check
:
List
[
str
]
=
[
]
        
self
.
pep517_backend
:
Optional
[
Pep517HookCaller
]
=
None
        
self
.
use_pep517
=
use_pep517
        
self
.
needs_more_preparation
=
False
    
def
__str__
(
self
)
-
>
str
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
{
}
'
.
format
(
redact_auth_from_url
(
self
.
link
.
url
)
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
{
}
'
.
format
(
display_path
(
self
.
satisfied_by
.
location
)
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
str
)
:
                
comes_from
:
Optional
[
str
]
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
f
'
(
from
{
comes_from
}
)
'
        
return
s
    
def
__repr__
(
self
)
-
>
str
:
        
return
'
<
{
}
object
:
{
}
editable
=
{
!
r
}
>
'
.
format
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
-
>
str
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
    
property
    
def
name
(
self
)
-
>
Optional
[
str
]
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
    
property
    
def
specifier
(
self
)
-
>
SpecifierSet
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
-
>
bool
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
    
def
match_markers
(
self
extras_requested
:
Optional
[
Iterable
[
str
]
]
=
None
)
-
>
bool
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
-
>
bool
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
hash_options
)
    
def
hashes
(
self
trust_internet
:
bool
=
True
)
-
>
Hashes
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
hash_options
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
-
>
Optional
[
str
]
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
str
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
:
str
autodelete
:
bool
parallel_builds
:
bool
    
)
-
>
str
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
tempdir_kinds
.
REQ_BUILD
globally_managed
=
True
            
)
            
return
self
.
_temp_build_dir
.
path
        
dir_name
:
str
=
canonicalize_name
(
self
.
name
)
        
if
parallel_builds
:
            
dir_name
=
f
"
{
dir_name
}
_
{
uuid
.
uuid4
(
)
.
hex
}
"
        
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
        
actual_build_dir
=
os
.
path
.
join
(
build_dir
dir_name
)
        
delete_arg
=
None
if
autodelete
else
False
        
return
TempDirectory
(
            
path
=
actual_build_dir
            
delete
=
delete_arg
            
kind
=
tempdir_kinds
.
REQ_BUILD
            
globally_managed
=
True
        
)
.
path
    
def
_set_requirement
(
self
)
-
>
None
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
-
>
None
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
check_if_exists
(
self
use_user_site
:
bool
)
-
>
None
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
        
existing_dist
=
get_distribution
(
self
.
req
.
name
)
        
if
not
existing_dist
:
            
return
        
existing_version
=
existing_dist
.
version
        
version_compatible
=
(
            
existing_version
is
not
None
and
            
self
.
req
.
specifier
.
contains
(
existing_version
prereleases
=
True
)
        
)
        
if
not
version_compatible
:
            
self
.
satisfied_by
=
None
            
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
{
}
in
{
}
"
.
format
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
            
else
:
                
self
.
satisfied_by
=
existing_dist
    
property
    
def
is_wheel
(
self
)
-
>
bool
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
-
>
str
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
-
>
str
:
        
assert
self
.
source_dir
f
"
No
source
dir
for
{
self
}
"
        
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
        
return
setup_py
    
property
    
def
pyproject_toml_path
(
self
)
-
>
str
:
        
assert
self
.
source_dir
f
"
No
source
dir
for
{
self
}
"
        
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
-
>
None
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
-
>
str
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
            
if
not
os
.
path
.
exists
(
self
.
setup_py_path
)
:
                
raise
InstallationError
(
                    
f
'
File
"
setup
.
py
"
not
found
for
legacy
project
{
self
}
.
'
                
)
            
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
f
"
from
{
self
.
link
}
"
            
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
-
>
None
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
-
>
Any
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
-
>
Distribution
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
-
>
None
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
:
str
        
autodelete
:
bool
=
False
        
parallel_builds
:
bool
=
False
    
)
-
>
None
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
                
autodelete
=
autodelete
                
parallel_builds
=
parallel_builds
            
)
    
def
update_editable
(
self
)
-
>
None
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
        
vcs_backend
=
vcs
.
get_backend_for_scheme
(
self
.
link
.
scheme
)
        
assert
vcs_backend
f
"
Unsupported
VCS
URL
{
self
.
link
.
url
}
"
        
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
    
def
uninstall
(
        
self
auto_confirm
:
bool
=
False
verbose
:
bool
=
False
    
)
-
>
Optional
[
UninstallPathSet
]
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
        
dist
=
get_distribution
(
self
.
req
.
name
)
        
if
not
dist
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
:
str
parentdir
:
str
rootdir
:
str
)
-
>
str
:
        
def
_clean_zip_name
(
name
:
str
prefix
:
str
)
-
>
str
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
                
f
"
name
{
name
!
r
}
doesn
'
t
start
with
prefix
{
prefix
!
r
}
"
            
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
:
Optional
[
str
]
)
-
>
None
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
        
if
build_dir
is
None
:
            
return
        
create_archive
=
True
        
archive_name
=
'
{
}
-
{
}
.
zip
'
.
format
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
{
}
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
'
                
'
(
b
)
ackup
(
a
)
bort
'
.
format
(
                    
display_path
(
archive_path
)
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
:
List
[
str
]
        
global_options
:
Optional
[
Sequence
[
str
]
]
=
None
        
root
:
Optional
[
str
]
=
None
        
home
:
Optional
[
str
]
=
None
        
prefix
:
Optional
[
str
]
=
None
        
warn_script_location
:
bool
=
True
        
use_user_site
:
bool
=
False
        
pycompile
:
bool
=
True
    
)
-
>
None
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
            
direct_url
=
None
            
if
self
.
original_link
:
                
direct_url
=
direct_url_from_link
(
                    
self
.
original_link
                    
self
.
source_dir
                    
self
.
original_link_is_in_wheel_cache
                
)
            
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
                
direct_url
=
direct_url
                
requested
=
self
.
user_supplied
            
)
            
self
.
install_succeeded
=
True
            
return
        
global_options
=
list
(
global_options
)
+
self
.
global_options
        
install_options
=
list
(
install_options
)
+
self
.
install_options
        
try
:
            
success
=
install_legacy
(
                
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
                
req_name
=
self
.
name
                
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
                
req_description
=
str
(
self
.
req
)
            
)
        
except
LegacyInstallFailure
as
exc
:
            
self
.
install_succeeded
=
False
            
six
.
reraise
(
*
exc
.
parent
)
        
except
Exception
:
            
self
.
install_succeeded
=
True
            
raise
        
self
.
install_succeeded
=
success
        
if
success
and
self
.
legacy_install_reason
=
=
8368
:
            
deprecated
(
                
reason
=
(
                    
"
{
}
was
installed
using
the
legacy
'
setup
.
py
install
'
"
                    
"
method
because
a
wheel
could
not
be
built
for
it
.
"
.
                    
format
(
self
.
name
)
                
)
                
replacement
=
"
to
fix
the
wheel
build
issue
reported
above
"
                
gone_in
=
None
                
issue
=
8368
            
)
def
check_invalid_constraint_type
(
req
:
InstallRequirement
)
-
>
str
:
    
problem
=
"
"
    
if
not
req
.
name
:
        
problem
=
"
Unnamed
requirements
are
not
allowed
as
constraints
"
    
elif
req
.
editable
:
        
problem
=
"
Editable
requirements
are
not
allowed
as
constraints
"
    
elif
req
.
extras
:
        
problem
=
"
Constraints
cannot
have
extras
"
    
if
problem
:
        
deprecated
(
            
reason
=
(
                
"
Constraints
are
only
allowed
to
take
the
form
of
a
package
"
                
"
name
and
a
version
specifier
.
Other
forms
were
originally
"
                
"
permitted
as
an
accident
of
the
implementation
but
were
"
                
"
undocumented
.
The
new
implementation
of
the
resolver
no
"
                
"
longer
supports
these
forms
.
"
            
)
            
replacement
=
"
replacing
the
constraint
with
a
requirement
"
            
gone_in
=
None
            
issue
=
8210
        
)
    
return
problem
