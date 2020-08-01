"
"
"
Contains
the
Command
base
classes
that
depend
on
PipSession
.
The
classes
in
this
module
are
in
a
separate
module
so
the
commands
not
needing
download
/
PackageFinder
capability
don
'
t
unnecessarily
import
the
PackageFinder
machinery
and
all
its
vendored
dependencies
etc
.
"
"
"
import
logging
import
os
from
functools
import
partial
from
pipenv
.
patched
.
notpip
.
_internal
.
cli
.
base_command
import
Command
from
pipenv
.
patched
.
notpip
.
_internal
.
cli
.
command_context
import
CommandContextMixIn
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
CommandError
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
_internal
.
legacy_resolve
import
Resolver
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
selection_prefs
import
SelectionPreferences
from
pipenv
.
patched
.
notpip
.
_internal
.
network
.
download
import
Downloader
from
pipenv
.
patched
.
notpip
.
_internal
.
network
.
session
import
PipSession
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
prepare
import
RequirementPreparer
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
constructors
import
(
    
install_req_from_editable
    
install_req_from_line
    
install_req_from_req_string
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
req
.
req_file
import
parse_requirements
from
pipenv
.
patched
.
notpip
.
_internal
.
self_outdated_check
import
(
    
make_link_collector
    
pip_self_version_check
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
typing
import
MYPY_CHECK_RUNNING
if
MYPY_CHECK_RUNNING
:
    
from
optparse
import
Values
    
from
typing
import
List
Optional
Tuple
    
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
models
.
target_python
import
TargetPython
    
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
req_set
import
RequirementSet
    
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
req_tracker
import
RequirementTracker
    
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
logger
=
logging
.
getLogger
(
__name__
)
class
SessionCommandMixin
(
CommandContextMixIn
)
:
    
"
"
"
    
A
class
mixin
for
command
classes
needing
_build_session
(
)
.
    
"
"
"
    
def
__init__
(
self
)
:
        
super
(
SessionCommandMixin
self
)
.
__init__
(
)
        
self
.
_session
=
None
    
classmethod
    
def
_get_index_urls
(
cls
options
)
:
        
"
"
"
Return
a
list
of
index
urls
from
user
-
provided
options
.
"
"
"
        
index_urls
=
[
]
        
if
not
getattr
(
options
"
no_index
"
False
)
:
            
url
=
getattr
(
options
"
index_url
"
None
)
            
if
url
:
                
index_urls
.
append
(
url
)
        
urls
=
getattr
(
options
"
extra_index_urls
"
None
)
        
if
urls
:
            
index_urls
.
extend
(
urls
)
        
return
index_urls
or
None
    
def
get_default_session
(
self
options
)
:
        
"
"
"
Get
a
default
-
managed
session
.
"
"
"
        
if
self
.
_session
is
None
:
            
self
.
_session
=
self
.
enter_context
(
self
.
_build_session
(
options
)
)
            
assert
self
.
_session
is
not
None
        
return
self
.
_session
    
def
_build_session
(
self
options
retries
=
None
timeout
=
None
)
:
        
assert
not
options
.
cache_dir
or
os
.
path
.
isabs
(
options
.
cache_dir
)
        
session
=
PipSession
(
            
cache
=
(
                
os
.
path
.
join
(
options
.
cache_dir
"
http
"
)
                
if
options
.
cache_dir
else
None
            
)
            
retries
=
retries
if
retries
is
not
None
else
options
.
retries
            
trusted_hosts
=
options
.
trusted_hosts
            
index_urls
=
self
.
_get_index_urls
(
options
)
        
)
        
if
options
.
cert
:
            
session
.
verify
=
options
.
cert
        
if
options
.
client_cert
:
            
session
.
cert
=
options
.
client_cert
        
if
options
.
timeout
or
timeout
:
            
session
.
timeout
=
(
                
timeout
if
timeout
is
not
None
else
options
.
timeout
            
)
        
if
options
.
proxy
:
            
session
.
proxies
=
{
                
"
http
"
:
options
.
proxy
                
"
https
"
:
options
.
proxy
            
}
        
session
.
auth
.
prompting
=
not
options
.
no_input
        
return
session
class
IndexGroupCommand
(
Command
SessionCommandMixin
)
:
    
"
"
"
    
Abstract
base
class
for
commands
with
the
index_group
options
.
    
This
also
corresponds
to
the
commands
that
permit
the
pip
version
check
.
    
"
"
"
    
def
handle_pip_version_check
(
self
options
)
:
        
"
"
"
        
Do
the
pip
version
check
if
not
disabled
.
        
This
overrides
the
default
behavior
of
not
doing
the
check
.
        
"
"
"
        
assert
hasattr
(
options
'
no_index
'
)
        
if
options
.
disable_pip_version_check
or
options
.
no_index
:
            
return
        
session
=
self
.
_build_session
(
            
options
            
retries
=
0
            
timeout
=
min
(
5
options
.
timeout
)
        
)
        
with
session
:
            
pip_self_version_check
(
session
options
)
class
RequirementCommand
(
IndexGroupCommand
)
:
    
staticmethod
    
def
make_requirement_preparer
(
        
temp_build_dir
        
options
        
req_tracker
        
session
        
finder
        
use_user_site
        
download_dir
=
None
        
wheel_download_dir
=
None
    
)
:
        
"
"
"
        
Create
a
RequirementPreparer
instance
for
the
given
parameters
.
        
"
"
"
        
downloader
=
Downloader
(
session
progress_bar
=
options
.
progress_bar
)
        
temp_build_dir_path
=
temp_build_dir
.
path
        
assert
temp_build_dir_path
is
not
None
        
return
RequirementPreparer
(
            
build_dir
=
temp_build_dir_path
            
src_dir
=
options
.
src_dir
            
download_dir
=
download_dir
            
wheel_download_dir
=
wheel_download_dir
            
build_isolation
=
options
.
build_isolation
            
req_tracker
=
req_tracker
            
downloader
=
downloader
            
finder
=
finder
            
require_hashes
=
options
.
require_hashes
            
use_user_site
=
use_user_site
        
)
    
staticmethod
    
def
make_resolver
(
        
preparer
        
finder
        
options
        
wheel_cache
=
None
        
use_user_site
=
False
        
ignore_installed
=
True
        
ignore_requires_python
=
False
        
force_reinstall
=
False
        
upgrade_strategy
=
"
to
-
satisfy
-
only
"
        
use_pep517
=
None
        
py_version_info
=
None
    
)
:
        
"
"
"
        
Create
a
Resolver
instance
for
the
given
parameters
.
        
"
"
"
        
make_install_req
=
partial
(
            
install_req_from_req_string
            
isolated
=
options
.
isolated_mode
            
wheel_cache
=
wheel_cache
            
use_pep517
=
use_pep517
        
)
        
return
Resolver
(
            
preparer
=
preparer
            
finder
=
finder
            
make_install_req
=
make_install_req
            
use_user_site
=
use_user_site
            
ignore_dependencies
=
options
.
ignore_dependencies
            
ignore_installed
=
ignore_installed
            
ignore_requires_python
=
ignore_requires_python
            
force_reinstall
=
force_reinstall
            
upgrade_strategy
=
upgrade_strategy
            
py_version_info
=
py_version_info
        
)
    
def
populate_requirement_set
(
        
self
        
requirement_set
        
args
        
options
        
finder
        
session
        
wheel_cache
    
)
:
        
"
"
"
        
Marshal
cmd
line
args
into
a
requirement
set
.
        
"
"
"
        
for
filename
in
options
.
constraints
:
            
for
req_to_add
in
parse_requirements
(
                    
filename
                    
constraint
=
True
finder
=
finder
options
=
options
                    
session
=
session
wheel_cache
=
wheel_cache
)
:
                
req_to_add
.
is_direct
=
True
                
requirement_set
.
add_requirement
(
req_to_add
)
        
for
req
in
args
:
            
req_to_add
=
install_req_from_line
(
                
req
None
isolated
=
options
.
isolated_mode
                
use_pep517
=
options
.
use_pep517
                
wheel_cache
=
wheel_cache
            
)
            
req_to_add
.
is_direct
=
True
            
requirement_set
.
add_requirement
(
req_to_add
)
        
for
req
in
options
.
editables
:
            
req_to_add
=
install_req_from_editable
(
                
req
                
isolated
=
options
.
isolated_mode
                
use_pep517
=
options
.
use_pep517
                
wheel_cache
=
wheel_cache
            
)
            
req_to_add
.
is_direct
=
True
            
requirement_set
.
add_requirement
(
req_to_add
)
        
for
filename
in
options
.
requirements
:
            
for
req_to_add
in
parse_requirements
(
                    
filename
                    
finder
=
finder
options
=
options
session
=
session
                    
wheel_cache
=
wheel_cache
                    
use_pep517
=
options
.
use_pep517
)
:
                
req_to_add
.
is_direct
=
True
                
requirement_set
.
add_requirement
(
req_to_add
)
        
requirements
=
(
            
requirement_set
.
unnamed_requirements
+
            
list
(
requirement_set
.
requirements
.
values
(
)
)
        
)
        
if
any
(
req
.
has_hash_options
for
req
in
requirements
)
:
            
options
.
require_hashes
=
True
        
if
not
(
args
or
options
.
editables
or
options
.
requirements
)
:
            
opts
=
{
'
name
'
:
self
.
name
}
            
if
options
.
find_links
:
                
raise
CommandError
(
                    
'
You
must
give
at
least
one
requirement
to
%
(
name
)
s
'
                    
'
(
maybe
you
meant
"
pip
%
(
name
)
s
%
(
links
)
s
"
?
)
'
%
                    
dict
(
opts
links
=
'
'
.
join
(
options
.
find_links
)
)
)
            
else
:
                
raise
CommandError
(
                    
'
You
must
give
at
least
one
requirement
to
%
(
name
)
s
'
                    
'
(
see
"
pip
help
%
(
name
)
s
"
)
'
%
opts
)
    
staticmethod
    
def
trace_basic_info
(
finder
)
:
        
"
"
"
        
Trace
basic
information
about
the
provided
objects
.
        
"
"
"
        
search_scope
=
finder
.
search_scope
        
locations
=
search_scope
.
get_formatted_locations
(
)
        
if
locations
:
            
logger
.
info
(
locations
)
    
def
_build_package_finder
(
        
self
        
options
        
session
        
target_python
=
None
        
ignore_requires_python
=
None
    
)
:
        
"
"
"
        
Create
a
package
finder
appropriate
to
this
requirement
command
.
        
:
param
ignore_requires_python
:
Whether
to
ignore
incompatible
            
"
Requires
-
Python
"
values
in
links
.
Defaults
to
False
.
        
"
"
"
        
link_collector
=
make_link_collector
(
session
options
=
options
)
        
selection_prefs
=
SelectionPreferences
(
            
allow_yanked
=
True
            
format_control
=
options
.
format_control
            
allow_all_prereleases
=
options
.
pre
            
prefer_binary
=
options
.
prefer_binary
            
ignore_requires_python
=
ignore_requires_python
        
)
        
return
PackageFinder
.
create
(
            
link_collector
=
link_collector
            
selection_prefs
=
selection_prefs
            
target_python
=
target_python
        
)
