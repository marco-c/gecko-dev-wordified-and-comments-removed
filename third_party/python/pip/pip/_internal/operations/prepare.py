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
mimetypes
import
os
import
shutil
from
dataclasses
import
dataclass
from
pathlib
import
Path
from
typing
import
Dict
Iterable
List
Optional
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
    
MetadataInconsistent
    
NetworkConnectionError
    
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
metadata
import
BaseDistribution
get_metadata_distribution
from
pip
.
_internal
.
models
.
direct_url
import
ArchiveInfo
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
operations
.
build
.
build_tracker
import
BuildTracker
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
utils
.
_log
import
getLogger
from
pip
.
_internal
.
utils
.
direct_url_helpers
import
(
    
direct_url_for_editable
    
direct_url_from_link
)
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
(
    
display_path
    
hash_file
    
hide_url
    
redact_auth_from_requirement
)
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
getLogger
(
__name__
)
def
_get_prepared_distribution
(
    
req
:
InstallRequirement
    
build_tracker
:
BuildTracker
    
finder
:
PackageFinder
    
build_isolation
:
bool
    
check_build_deps
:
bool
)
-
>
BaseDistribution
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
    
tracker_id
=
abstract_dist
.
build_tracker_id
    
if
tracker_id
is
not
None
:
        
with
build_tracker
.
track
(
req
tracker_id
)
:
            
abstract_dist
.
prepare_distribution_metadata
(
                
finder
build_isolation
check_build_deps
            
)
    
return
abstract_dist
.
get_metadata_distribution
(
)
def
unpack_vcs_link
(
link
:
Link
location
:
str
verbosity
:
int
)
-
>
None
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
verbosity
=
verbosity
)
dataclass
class
File
:
    
path
:
str
    
content_type
:
Optional
[
str
]
=
None
    
def
__post_init__
(
self
)
-
>
None
:
        
if
self
.
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
self
.
path
)
[
0
]
def
get_http_url
(
    
link
:
Link
    
download
:
Downloader
    
download_dir
:
Optional
[
str
]
=
None
    
hashes
:
Optional
[
Hashes
]
=
None
)
-
>
File
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
get_file_url
(
    
link
:
Link
download_dir
:
Optional
[
str
]
=
None
hashes
:
Optional
[
Hashes
]
=
None
)
-
>
File
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
:
Link
    
location
:
str
    
download
:
Downloader
    
verbosity
:
int
    
download_dir
:
Optional
[
str
]
=
None
    
hashes
:
Optional
[
Hashes
]
=
None
)
-
>
Optional
[
File
]
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
verbosity
=
verbosity
)
        
return
None
    
assert
not
link
.
is_existing_dir
(
)
    
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
:
Link
    
download_dir
:
str
    
hashes
:
Optional
[
Hashes
]
    
warn_on_hash_mismatch
:
bool
=
True
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
"
File
was
already
downloaded
%
s
"
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
            
if
warn_on_hash_mismatch
:
                
logger
.
warning
(
                    
"
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
Re
-
downloading
.
"
                    
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
:
str
        
download_dir
:
Optional
[
str
]
        
src_dir
:
str
        
build_isolation
:
bool
        
check_build_deps
:
bool
        
build_tracker
:
BuildTracker
        
session
:
PipSession
        
progress_bar
:
str
        
finder
:
PackageFinder
        
require_hashes
:
bool
        
use_user_site
:
bool
        
lazy_wheel
:
bool
        
verbosity
:
int
        
legacy_resolver
:
bool
    
)
-
>
None
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
build_tracker
=
build_tracker
        
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
check_build_deps
=
check_build_deps
        
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
verbosity
=
verbosity
        
self
.
legacy_resolver
=
legacy_resolver
        
self
.
_downloaded
:
Dict
[
str
str
]
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
:
InstallRequirement
)
-
>
None
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
is_wheel_from_cache
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
redact_auth_from_requirement
(
req
.
req
)
if
req
.
req
else
str
(
req
)
        
if
req
.
req
and
req
.
comes_from
:
            
if
isinstance
(
req
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
req
.
comes_from
            
else
:
                
comes_from
=
req
.
comes_from
.
from_path
(
)
            
if
comes_from
:
                
information
+
=
f
"
(
from
{
comes_from
}
)
"
        
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
is_wheel_from_cache
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
:
InstallRequirement
parallel_builds
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
        
req
.
ensure_pristine_source_checkout
(
)
    
def
_get_linked_req_hashes
(
self
req
:
InstallRequirement
)
-
>
Hashes
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
not
req
.
is_direct
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
_fetch_metadata_only
(
        
self
        
req
:
InstallRequirement
    
)
-
>
Optional
[
BaseDistribution
]
:
        
if
self
.
legacy_resolver
:
            
logger
.
debug
(
                
"
Metadata
-
only
fetching
is
not
used
in
the
legacy
resolver
"
            
)
            
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
                
"
Metadata
-
only
fetching
is
not
used
as
hash
checking
is
required
"
            
)
            
return
None
        
return
self
.
_fetch_metadata_using_link_data_attr
(
            
req
        
)
or
self
.
_fetch_metadata_using_lazy_wheel
(
req
.
link
)
    
def
_fetch_metadata_using_link_data_attr
(
        
self
        
req
:
InstallRequirement
    
)
-
>
Optional
[
BaseDistribution
]
:
        
"
"
"
Fetch
metadata
from
the
data
-
dist
-
info
-
metadata
attribute
if
possible
.
"
"
"
        
metadata_link
=
req
.
link
.
metadata_link
(
)
        
if
metadata_link
is
None
:
            
return
None
        
assert
req
.
req
is
not
None
        
logger
.
verbose
(
            
"
Obtaining
dependency
information
for
%
s
from
%
s
"
            
req
.
req
            
metadata_link
        
)
        
metadata_file
=
get_http_url
(
            
metadata_link
            
self
.
_download
            
hashes
=
metadata_link
.
as_hashes
(
)
        
)
        
with
open
(
metadata_file
.
path
"
rb
"
)
as
f
:
            
metadata_contents
=
f
.
read
(
)
        
metadata_dist
=
get_metadata_distribution
(
            
metadata_contents
            
req
.
link
.
filename
            
req
.
req
.
name
        
)
        
if
canonicalize_name
(
metadata_dist
.
raw_name
)
!
=
canonicalize_name
(
req
.
req
.
name
)
:
            
raise
MetadataInconsistent
(
                
req
"
Name
"
req
.
req
.
name
metadata_dist
.
raw_name
            
)
        
return
metadata_dist
    
def
_fetch_metadata_using_lazy_wheel
(
        
self
        
link
:
Link
    
)
-
>
Optional
[
BaseDistribution
]
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
                
"
Lazy
wheel
is
not
used
as
%
r
does
not
point
to
a
remote
wheel
"
                
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
            
"
Obtaining
dependency
information
from
%
s
%
s
"
            
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
"
#
"
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
"
%
s
does
not
support
range
requests
"
url
)
            
return
None
    
def
_complete_partial_requirements
(
        
self
        
partially_downloaded_reqs
:
Iterable
[
InstallRequirement
]
        
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
:
Dict
[
Link
InstallRequirement
]
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
filepath
            
if
not
req
.
is_wheel
:
                
req
.
needs_unpacked_archive
(
Path
(
filepath
)
)
        
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
:
InstallRequirement
parallel_builds
:
bool
=
False
    
)
-
>
BaseDistribution
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
                    
warn_on_hash_mismatch
=
not
req
.
is_wheel_from_cache
                
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
            
else
:
                
metadata_dist
=
self
.
_fetch_metadata_only
(
req
)
                
if
metadata_dist
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
metadata_dist
            
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
:
Iterable
[
InstallRequirement
]
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
                    
req
.
needs_more_preparation
=
False
        
partially_downloaded_reqs
:
List
[
InstallRequirement
]
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
:
InstallRequirement
parallel_builds
:
bool
    
)
-
>
BaseDistribution
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
        
hashes
=
self
.
_get_linked_req_hashes
(
req
)
        
if
hashes
and
req
.
is_wheel_from_cache
:
            
assert
req
.
download_info
is
not
None
            
assert
link
.
is_wheel
            
assert
link
.
is_file
            
if
(
                
isinstance
(
req
.
download_info
.
info
ArchiveInfo
)
                
and
req
.
download_info
.
info
.
hashes
                
and
hashes
.
has_one_of
(
req
.
download_info
.
info
.
hashes
)
            
)
:
                
hashes
=
None
            
else
:
                
logger
.
warning
(
                    
"
The
hashes
of
the
source
archive
found
in
cache
entry
"
                    
"
don
'
t
match
ignoring
cached
built
wheel
"
                    
"
and
re
-
downloading
source
.
"
                
)
                
req
.
link
=
req
.
cached_wheel_source_link
                
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
        
if
link
.
is_existing_dir
(
)
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
verbosity
                    
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
                    
f
"
Could
not
install
requirement
{
req
}
because
of
HTTP
"
                    
f
"
error
{
exc
}
for
URL
{
link
}
"
                
)
        
else
:
            
file_path
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
=
None
)
        
if
req
.
download_info
is
None
:
            
assert
not
req
.
editable
            
req
.
download_info
=
direct_url_from_link
(
link
req
.
source_dir
)
            
if
(
                
isinstance
(
req
.
download_info
.
info
ArchiveInfo
)
                
and
not
req
.
download_info
.
info
.
hashes
                
and
local_file
            
)
:
                
hash
=
hash_file
(
local_file
.
path
)
[
0
]
.
hexdigest
(
)
                
req
.
download_info
.
info
.
hash
=
f
"
sha256
=
{
hash
}
"
        
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
build_tracker
            
self
.
finder
            
self
.
build_isolation
            
self
.
check_build_deps
        
)
        
return
dist
    
def
save_linked_requirement
(
self
req
:
InstallRequirement
)
-
>
None
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
                
"
Not
copying
link
to
destination
directory
"
                
"
since
it
is
a
directory
:
%
s
"
                
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
"
Saved
%
s
"
download_path
)
    
def
prepare_editable_requirement
(
        
self
        
req
:
InstallRequirement
    
)
-
>
BaseDistribution
:
        
"
"
"
Prepare
an
editable
requirement
.
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
"
Obtaining
%
s
"
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
                    
f
"
The
editable
requirement
{
req
}
cannot
be
installed
when
"
                    
"
requiring
hashes
because
there
is
no
single
file
to
"
                    
"
hash
.
"
                
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
            
assert
req
.
source_dir
            
req
.
download_info
=
direct_url_for_editable
(
req
.
unpacked_source_directory
)
            
dist
=
_get_prepared_distribution
(
                
req
                
self
.
build_tracker
                
self
.
finder
                
self
.
build_isolation
                
self
.
check_build_deps
            
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
:
InstallRequirement
        
skip_reason
:
str
    
)
-
>
BaseDistribution
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
.
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
            
f
"
is
set
to
{
req
.
satisfied_by
}
"
        
)
        
logger
.
info
(
            
"
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
"
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
                    
"
Since
it
is
already
installed
we
are
trusting
this
"
                    
"
package
without
checking
its
hash
.
To
ensure
a
"
                    
"
completely
repeatable
environment
install
into
an
"
                    
"
empty
virtualenv
.
"
                
)
            
return
InstalledDistribution
(
req
)
.
get_metadata_distribution
(
)
