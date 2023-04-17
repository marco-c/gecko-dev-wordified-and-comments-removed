"
"
"
Prepares
a
distribution
for
installation
"
"
"
import
logging
import
mimetypes
import
os
import
shutil
from
typing
import
Dict
Iterable
List
Optional
Tuple
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
pkg_resources
import
Distribution
from
pip
.
_internal
.
distributions
import
make_distribution_for_install_requirement
from
pip
.
_internal
.
distributions
.
installed
import
InstalledDistribution
from
pip
.
_internal
.
exceptions
import
(
    
DirectoryUrlHashUnsupported
    
HashMismatch
    
HashUnpinned
    
InstallationError
    
NetworkConnectionError
    
PreviousBuildDirError
    
VcsHashUnsupported
)
from
pip
.
_internal
.
index
.
package_finder
import
PackageFinder
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
models
.
wheel
import
Wheel
from
pip
.
_internal
.
network
.
download
import
BatchDownloader
Downloader
from
pip
.
_internal
.
network
.
lazy_wheel
import
(
    
HTTPRangeRequestUnsupported
    
dist_from_wheel_url
)
from
pip
.
_internal
.
network
.
session
import
PipSession
from
pip
.
_internal
.
req
.
req_install
import
InstallRequirement
from
pip
.
_internal
.
req
.
req_tracker
import
RequirementTracker
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
filesystem
import
copy2_fixed
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
MissingHashes
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
display_path
hide_url
is_installable_dir
rmtree
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
from
pip
.
_internal
.
utils
.
unpacking
import
unpack_file
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
_get_prepared_distribution
(
    
req
    
req_tracker
    
finder
    
build_isolation
)
:
    
"
"
"
Prepare
a
distribution
for
installation
.
"
"
"
    
abstract_dist
=
make_distribution_for_install_requirement
(
req
)
    
with
req_tracker
.
track
(
req
)
:
        
abstract_dist
.
prepare_distribution_metadata
(
finder
build_isolation
)
    
return
abstract_dist
.
get_pkg_resources_distribution
(
)
def
unpack_vcs_link
(
link
location
)
:
    
vcs_backend
=
vcs
.
get_backend_for_scheme
(
link
.
scheme
)
    
assert
vcs_backend
is
not
None
    
vcs_backend
.
unpack
(
location
url
=
hide_url
(
link
.
url
)
)
class
File
:
    
def
__init__
(
self
path
content_type
)
:
        
self
.
path
=
path
        
if
content_type
is
None
:
            
self
.
content_type
=
mimetypes
.
guess_type
(
path
)
[
0
]
        
else
:
            
self
.
content_type
=
content_type
def
get_http_url
(
    
link
    
download
    
download_dir
=
None
    
hashes
=
None
)
:
    
temp_dir
=
TempDirectory
(
kind
=
"
unpack
"
globally_managed
=
True
)
    
already_downloaded_path
=
None
    
if
download_dir
:
        
already_downloaded_path
=
_check_download_dir
(
            
link
download_dir
hashes
        
)
    
if
already_downloaded_path
:
        
from_path
=
already_downloaded_path
        
content_type
=
None
    
else
:
        
from_path
content_type
=
download
(
link
temp_dir
.
path
)
        
if
hashes
:
            
hashes
.
check_against_path
(
from_path
)
    
return
File
(
from_path
content_type
)
def
_copy2_ignoring_special_files
(
src
dest
)
:
    
"
"
"
Copying
special
files
is
not
supported
but
as
a
convenience
to
users
    
we
skip
errors
copying
them
.
This
supports
tools
that
may
create
e
.
g
.
    
socket
files
in
the
project
source
directory
.
    
"
"
"
    
try
:
        
copy2_fixed
(
src
dest
)
    
except
shutil
.
SpecialFileError
as
e
:
        
logger
.
warning
(
            
"
Ignoring
special
file
error
'
%
s
'
encountered
copying
%
s
to
%
s
.
"
            
str
(
e
)
            
src
            
dest
        
)
def
_copy_source_tree
(
source
target
)
:
    
target_abspath
=
os
.
path
.
abspath
(
target
)
    
target_basename
=
os
.
path
.
basename
(
target_abspath
)
    
target_dirname
=
os
.
path
.
dirname
(
target_abspath
)
    
def
ignore
(
d
names
)
:
        
skipped
=
[
]
        
if
d
=
=
source
:
            
skipped
+
=
[
'
.
tox
'
'
.
nox
'
]
        
if
os
.
path
.
abspath
(
d
)
=
=
target_dirname
:
            
skipped
+
=
[
target_basename
]
        
return
skipped
    
shutil
.
copytree
(
        
source
        
target
        
ignore
=
ignore
        
symlinks
=
True
        
copy_function
=
_copy2_ignoring_special_files
    
)
def
get_file_url
(
    
link
    
download_dir
=
None
    
hashes
=
None
)
:
    
"
"
"
Get
file
and
optionally
check
its
hash
.
    
"
"
"
    
already_downloaded_path
=
None
    
if
download_dir
:
        
already_downloaded_path
=
_check_download_dir
(
            
link
download_dir
hashes
        
)
    
if
already_downloaded_path
:
        
from_path
=
already_downloaded_path
    
else
:
        
from_path
=
link
.
file_path
    
if
hashes
:
        
hashes
.
check_against_path
(
from_path
)
    
return
File
(
from_path
None
)
def
unpack_url
(
    
link
    
location
    
download
    
download_dir
=
None
    
hashes
=
None
)
:
    
"
"
"
Unpack
link
into
location
downloading
if
required
.
    
:
param
hashes
:
A
Hashes
object
one
of
whose
embedded
hashes
must
match
        
or
HashMismatch
will
be
raised
.
If
the
Hashes
is
empty
no
matches
are
        
required
and
unhashable
types
of
requirements
(
like
VCS
ones
which
        
would
ordinarily
raise
HashUnsupported
)
are
allowed
.
    
"
"
"
    
if
link
.
is_vcs
:
        
unpack_vcs_link
(
link
location
)
        
return
None
    
if
link
.
is_existing_dir
(
)
:
        
deprecated
(
            
"
A
future
pip
version
will
change
local
packages
to
be
built
"
            
"
in
-
place
without
first
copying
to
a
temporary
directory
.
"
            
"
We
recommend
you
use
-
-
use
-
feature
=
in
-
tree
-
build
to
test
"
            
"
your
packages
with
this
new
behavior
before
it
becomes
the
"
            
"
default
.
\
n
"
            
replacement
=
None
            
gone_in
=
"
21
.
3
"
            
issue
=
7555
        
)
        
if
os
.
path
.
isdir
(
location
)
:
            
rmtree
(
location
)
        
_copy_source_tree
(
link
.
file_path
location
)
        
return
None
    
if
link
.
is_file
:
        
file
=
get_file_url
(
link
download_dir
hashes
=
hashes
)
    
else
:
        
file
=
get_http_url
(
            
link
            
download
            
download_dir
            
hashes
=
hashes
        
)
    
if
not
link
.
is_wheel
:
        
unpack_file
(
file
.
path
location
file
.
content_type
)
    
return
file
def
_check_download_dir
(
link
download_dir
hashes
)
:
    
"
"
"
Check
download_dir
for
previously
downloaded
file
with
correct
hash
        
If
a
correct
file
is
found
return
its
path
else
None
    
"
"
"
    
download_path
=
os
.
path
.
join
(
download_dir
link
.
filename
)
    
if
not
os
.
path
.
exists
(
download_path
)
:
        
return
None
    
logger
.
info
(
'
File
was
already
downloaded
%
s
'
download_path
)
    
if
hashes
:
        
try
:
            
hashes
.
check_against_path
(
download_path
)
        
except
HashMismatch
:
            
logger
.
warning
(
                
'
Previously
-
downloaded
file
%
s
has
bad
hash
.
'
                
'
Re
-
downloading
.
'
                
download_path
            
)
            
os
.
unlink
(
download_path
)
            
return
None
    
return
download_path
class
RequirementPreparer
:
    
"
"
"
Prepares
a
Requirement
    
"
"
"
    
def
__init__
(
        
self
        
build_dir
        
download_dir
        
src_dir
        
build_isolation
        
req_tracker
        
session
        
progress_bar
        
finder
        
require_hashes
        
use_user_site
        
lazy_wheel
        
in_tree_build
    
)
:
        
super
(
)
.
__init__
(
)
        
self
.
src_dir
=
src_dir
        
self
.
build_dir
=
build_dir
        
self
.
req_tracker
=
req_tracker
        
self
.
_session
=
session
        
self
.
_download
=
Downloader
(
session
progress_bar
)
        
self
.
_batch_download
=
BatchDownloader
(
session
progress_bar
)
        
self
.
finder
=
finder
        
self
.
download_dir
=
download_dir
        
self
.
build_isolation
=
build_isolation
        
self
.
require_hashes
=
require_hashes
        
self
.
use_user_site
=
use_user_site
        
self
.
use_lazy_wheel
=
lazy_wheel
        
self
.
in_tree_build
=
in_tree_build
        
self
.
_downloaded
=
{
}
        
self
.
_previous_requirement_header
=
(
"
"
"
"
)
    
def
_log_preparing_link
(
self
req
)
:
        
"
"
"
Provide
context
for
the
requirement
being
prepared
.
"
"
"
        
if
req
.
link
.
is_file
and
not
req
.
original_link_is_in_wheel_cache
:
            
message
=
"
Processing
%
s
"
            
information
=
str
(
display_path
(
req
.
link
.
file_path
)
)
        
else
:
            
message
=
"
Collecting
%
s
"
            
information
=
str
(
req
.
req
or
req
)
        
if
(
message
information
)
!
=
self
.
_previous_requirement_header
:
            
self
.
_previous_requirement_header
=
(
message
information
)
            
logger
.
info
(
message
information
)
        
if
req
.
original_link_is_in_wheel_cache
:
            
with
indent_log
(
)
:
                
logger
.
info
(
"
Using
cached
%
s
"
req
.
link
.
filename
)
    
def
_ensure_link_req_src_dir
(
self
req
parallel_builds
)
:
        
"
"
"
Ensure
source_dir
of
a
linked
InstallRequirement
.
"
"
"
        
if
req
.
link
.
is_wheel
:
            
return
        
assert
req
.
source_dir
is
None
        
if
req
.
link
.
is_existing_dir
(
)
and
self
.
in_tree_build
:
            
req
.
source_dir
=
req
.
link
.
file_path
            
return
        
req
.
ensure_has_source_dir
(
            
self
.
build_dir
            
autodelete
=
True
            
parallel_builds
=
parallel_builds
        
)
        
if
is_installable_dir
(
req
.
source_dir
)
:
            
raise
PreviousBuildDirError
(
                
"
pip
can
'
t
proceed
with
requirements
'
{
}
'
due
to
a
"
                
"
pre
-
existing
build
directory
(
{
}
)
.
This
is
likely
"
                
"
due
to
a
previous
installation
that
failed
.
pip
is
"
                
"
being
responsible
and
not
assuming
it
can
delete
this
.
"
                
"
Please
delete
it
and
try
again
.
"
.
format
(
req
req
.
source_dir
)
            
)
    
def
_get_linked_req_hashes
(
self
req
)
:
        
if
not
self
.
require_hashes
:
            
return
req
.
hashes
(
trust_internet
=
True
)
        
if
req
.
link
.
is_vcs
:
            
raise
VcsHashUnsupported
(
)
        
if
req
.
link
.
is_existing_dir
(
)
:
            
raise
DirectoryUrlHashUnsupported
(
)
        
if
req
.
original_link
is
None
and
not
req
.
is_pinned
:
            
raise
HashUnpinned
(
)
        
return
req
.
hashes
(
trust_internet
=
False
)
or
MissingHashes
(
)
    
def
_fetch_metadata_using_lazy_wheel
(
self
link
)
:
        
"
"
"
Fetch
metadata
using
lazy
wheel
if
possible
.
"
"
"
        
if
not
self
.
use_lazy_wheel
:
            
return
None
        
if
self
.
require_hashes
:
            
logger
.
debug
(
'
Lazy
wheel
is
not
used
as
hash
checking
is
required
'
)
            
return
None
        
if
link
.
is_file
or
not
link
.
is_wheel
:
            
logger
.
debug
(
                
'
Lazy
wheel
is
not
used
as
'
                
'
%
r
does
not
points
to
a
remote
wheel
'
                
link
            
)
            
return
None
        
wheel
=
Wheel
(
link
.
filename
)
        
name
=
canonicalize_name
(
wheel
.
name
)
        
logger
.
info
(
            
'
Obtaining
dependency
information
from
%
s
%
s
'
            
name
wheel
.
version
        
)
        
url
=
link
.
url
.
split
(
'
#
'
1
)
[
0
]
        
try
:
            
return
dist_from_wheel_url
(
name
url
self
.
_session
)
        
except
HTTPRangeRequestUnsupported
:
            
logger
.
debug
(
'
%
s
does
not
support
range
requests
'
url
)
            
return
None
    
def
_complete_partial_requirements
(
        
self
        
partially_downloaded_reqs
        
parallel_builds
=
False
    
)
:
        
"
"
"
Download
any
requirements
which
were
only
fetched
by
metadata
.
"
"
"
        
temp_dir
=
TempDirectory
(
kind
=
"
unpack
"
globally_managed
=
True
)
.
path
        
links_to_fully_download
=
{
}
        
for
req
in
partially_downloaded_reqs
:
            
assert
req
.
link
            
links_to_fully_download
[
req
.
link
]
=
req
        
batch_download
=
self
.
_batch_download
(
            
links_to_fully_download
.
keys
(
)
            
temp_dir
        
)
        
for
link
(
filepath
_
)
in
batch_download
:
            
logger
.
debug
(
"
Downloading
link
%
s
to
%
s
"
link
filepath
)
            
req
=
links_to_fully_download
[
link
]
            
req
.
local_file_path
=
filepath
        
for
req
in
partially_downloaded_reqs
:
            
self
.
_prepare_linked_requirement
(
req
parallel_builds
)
    
def
prepare_linked_requirement
(
self
req
parallel_builds
=
False
)
:
        
"
"
"
Prepare
a
requirement
to
be
obtained
from
req
.
link
.
"
"
"
        
assert
req
.
link
        
link
=
req
.
link
        
self
.
_log_preparing_link
(
req
)
        
with
indent_log
(
)
:
            
file_path
=
None
            
if
self
.
download_dir
is
not
None
and
link
.
is_wheel
:
                
hashes
=
self
.
_get_linked_req_hashes
(
req
)
                
file_path
=
_check_download_dir
(
req
.
link
self
.
download_dir
hashes
)
            
if
file_path
is
not
None
:
                
self
.
_downloaded
[
req
.
link
.
url
]
=
file_path
None
            
else
:
                
wheel_dist
=
self
.
_fetch_metadata_using_lazy_wheel
(
link
)
                
if
wheel_dist
is
not
None
:
                    
req
.
needs_more_preparation
=
True
                    
return
wheel_dist
            
return
self
.
_prepare_linked_requirement
(
req
parallel_builds
)
    
def
prepare_linked_requirements_more
(
self
reqs
parallel_builds
=
False
)
:
        
"
"
"
Prepare
linked
requirements
more
if
needed
.
"
"
"
        
reqs
=
[
req
for
req
in
reqs
if
req
.
needs_more_preparation
]
        
for
req
in
reqs
:
            
if
self
.
download_dir
is
not
None
and
req
.
link
.
is_wheel
:
                
hashes
=
self
.
_get_linked_req_hashes
(
req
)
                
file_path
=
_check_download_dir
(
req
.
link
self
.
download_dir
hashes
)
                
if
file_path
is
not
None
:
                    
self
.
_downloaded
[
req
.
link
.
url
]
=
file_path
None
                    
req
.
needs_more_preparation
=
False
        
partially_downloaded_reqs
=
[
]
        
for
req
in
reqs
:
            
if
req
.
needs_more_preparation
:
                
partially_downloaded_reqs
.
append
(
req
)
            
else
:
                
self
.
_prepare_linked_requirement
(
req
parallel_builds
)
        
self
.
_complete_partial_requirements
(
            
partially_downloaded_reqs
parallel_builds
=
parallel_builds
        
)
    
def
_prepare_linked_requirement
(
self
req
parallel_builds
)
:
        
assert
req
.
link
        
link
=
req
.
link
        
self
.
_ensure_link_req_src_dir
(
req
parallel_builds
)
        
hashes
=
self
.
_get_linked_req_hashes
(
req
)
        
if
link
.
is_existing_dir
(
)
and
self
.
in_tree_build
:
            
local_file
=
None
        
elif
link
.
url
not
in
self
.
_downloaded
:
            
try
:
                
local_file
=
unpack_url
(
                    
link
req
.
source_dir
self
.
_download
                    
self
.
download_dir
hashes
                
)
            
except
NetworkConnectionError
as
exc
:
                
raise
InstallationError
(
                    
'
Could
not
install
requirement
{
}
because
of
HTTP
'
                    
'
error
{
}
for
URL
{
}
'
.
format
(
req
exc
link
)
                
)
        
else
:
            
file_path
content_type
=
self
.
_downloaded
[
link
.
url
]
            
if
hashes
:
                
hashes
.
check_against_path
(
file_path
)
            
local_file
=
File
(
file_path
content_type
)
        
if
local_file
:
            
req
.
local_file_path
=
local_file
.
path
        
dist
=
_get_prepared_distribution
(
            
req
self
.
req_tracker
self
.
finder
self
.
build_isolation
        
)
        
return
dist
    
def
save_linked_requirement
(
self
req
)
:
        
assert
self
.
download_dir
is
not
None
        
assert
req
.
link
is
not
None
        
link
=
req
.
link
        
if
link
.
is_vcs
or
(
link
.
is_existing_dir
(
)
and
req
.
editable
)
:
            
req
.
archive
(
self
.
download_dir
)
            
return
        
if
link
.
is_existing_dir
(
)
:
            
logger
.
debug
(
                
'
Not
copying
link
to
destination
directory
'
                
'
since
it
is
a
directory
:
%
s
'
link
            
)
            
return
        
if
req
.
local_file_path
is
None
:
            
return
        
download_location
=
os
.
path
.
join
(
self
.
download_dir
link
.
filename
)
        
if
not
os
.
path
.
exists
(
download_location
)
:
            
shutil
.
copy
(
req
.
local_file_path
download_location
)
            
download_path
=
display_path
(
download_location
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
download_path
)
    
def
prepare_editable_requirement
(
        
self
        
req
    
)
:
        
"
"
"
Prepare
an
editable
requirement
        
"
"
"
        
assert
req
.
editable
"
cannot
prepare
a
non
-
editable
req
as
editable
"
        
logger
.
info
(
'
Obtaining
%
s
'
req
)
        
with
indent_log
(
)
:
            
if
self
.
require_hashes
:
                
raise
InstallationError
(
                    
'
The
editable
requirement
{
}
cannot
be
installed
when
'
                    
'
requiring
hashes
because
there
is
no
single
file
to
'
                    
'
hash
.
'
.
format
(
req
)
                
)
            
req
.
ensure_has_source_dir
(
self
.
src_dir
)
            
req
.
update_editable
(
)
            
dist
=
_get_prepared_distribution
(
                
req
self
.
req_tracker
self
.
finder
self
.
build_isolation
            
)
            
req
.
check_if_exists
(
self
.
use_user_site
)
        
return
dist
    
def
prepare_installed_requirement
(
        
self
        
req
        
skip_reason
    
)
:
        
"
"
"
Prepare
an
already
-
installed
requirement
        
"
"
"
        
assert
req
.
satisfied_by
"
req
should
have
been
satisfied
but
isn
'
t
"
        
assert
skip_reason
is
not
None
(
            
"
did
not
get
skip
reason
skipped
but
req
.
satisfied_by
"
            
"
is
set
to
{
}
"
.
format
(
req
.
satisfied_by
)
        
)
        
logger
.
info
(
            
'
Requirement
%
s
:
%
s
(
%
s
)
'
            
skip_reason
req
req
.
satisfied_by
.
version
        
)
        
with
indent_log
(
)
:
            
if
self
.
require_hashes
:
                
logger
.
debug
(
                    
'
Since
it
is
already
installed
we
are
trusting
this
'
                    
'
package
without
checking
its
hash
.
To
ensure
a
'
                    
'
completely
repeatable
environment
install
into
an
'
                    
'
empty
virtualenv
.
'
                
)
            
return
InstalledDistribution
(
req
)
.
get_pkg_resources_distribution
(
)
