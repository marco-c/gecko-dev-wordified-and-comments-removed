from
__future__
import
absolute_import
import
datetime
import
hashlib
import
json
import
logging
import
os
.
path
import
sys
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
import
version
as
packaging_version
from
pipenv
.
patched
.
notpip
.
_vendor
.
six
import
ensure_binary
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
collector
import
LinkCollector
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
models
.
search_scope
import
SearchScope
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
utils
.
filesystem
import
(
    
adjacent_tmp_file
    
check_path_owner
    
replace
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
    
ensure_dir
    
get_installed_version
    
redact_auth_from_url
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
get_installer
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
    
import
optparse
    
from
optparse
import
Values
    
from
typing
import
Any
Dict
Text
Union
    
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
SELFCHECK_DATE_FMT
=
"
%
Y
-
%
m
-
%
dT
%
H
:
%
M
:
%
SZ
"
logger
=
logging
.
getLogger
(
__name__
)
def
make_link_collector
(
    
session
    
options
    
suppress_no_index
=
False
)
:
    
"
"
"
    
:
param
session
:
The
Session
to
use
to
make
requests
.
    
:
param
suppress_no_index
:
Whether
to
ignore
the
-
-
no
-
index
option
        
when
constructing
the
SearchScope
object
.
    
"
"
"
    
index_urls
=
[
options
.
index_url
]
+
options
.
extra_index_urls
    
if
options
.
no_index
and
not
suppress_no_index
:
        
logger
.
debug
(
            
'
Ignoring
indexes
:
%
s
'
            
'
'
.
join
(
redact_auth_from_url
(
url
)
for
url
in
index_urls
)
        
)
        
index_urls
=
[
]
    
find_links
=
options
.
find_links
or
[
]
    
search_scope
=
SearchScope
.
create
(
        
find_links
=
find_links
index_urls
=
index_urls
    
)
    
link_collector
=
LinkCollector
(
session
=
session
search_scope
=
search_scope
)
    
return
link_collector
def
_get_statefile_name
(
key
)
:
    
key_bytes
=
ensure_binary
(
key
)
    
name
=
hashlib
.
sha224
(
key_bytes
)
.
hexdigest
(
)
    
return
name
class
SelfCheckState
(
object
)
:
    
def
__init__
(
self
cache_dir
)
:
        
self
.
state
=
{
}
        
self
.
statefile_path
=
None
        
if
cache_dir
:
            
self
.
statefile_path
=
os
.
path
.
join
(
                
cache_dir
"
selfcheck
"
_get_statefile_name
(
self
.
key
)
            
)
            
try
:
                
with
open
(
self
.
statefile_path
)
as
statefile
:
                    
self
.
state
=
json
.
load
(
statefile
)
            
except
(
IOError
ValueError
KeyError
)
:
                
pass
    
property
    
def
key
(
self
)
:
        
return
sys
.
prefix
    
def
save
(
self
pypi_version
current_time
)
:
        
if
not
self
.
statefile_path
:
            
return
        
if
not
check_path_owner
(
os
.
path
.
dirname
(
self
.
statefile_path
)
)
:
            
return
        
ensure_dir
(
os
.
path
.
dirname
(
self
.
statefile_path
)
)
        
state
=
{
            
"
key
"
:
self
.
key
            
"
last_check
"
:
current_time
.
strftime
(
SELFCHECK_DATE_FMT
)
            
"
pypi_version
"
:
pypi_version
        
}
        
text
=
json
.
dumps
(
state
sort_keys
=
True
separators
=
(
"
"
"
:
"
)
)
        
with
adjacent_tmp_file
(
self
.
statefile_path
)
as
f
:
            
f
.
write
(
ensure_binary
(
text
)
)
        
try
:
            
replace
(
f
.
name
self
.
statefile_path
)
        
except
OSError
:
            
pass
def
was_installed_by_pip
(
pkg
)
:
    
"
"
"
Checks
whether
pkg
was
installed
by
pip
    
This
is
used
not
to
display
the
upgrade
message
when
pip
is
in
fact
    
installed
by
system
package
manager
such
as
dnf
on
Fedora
.
    
"
"
"
    
try
:
        
dist
=
pkg_resources
.
get_distribution
(
pkg
)
        
return
"
pip
"
=
=
get_installer
(
dist
)
    
except
pkg_resources
.
DistributionNotFound
:
        
return
False
def
pip_self_version_check
(
session
options
)
:
    
"
"
"
Check
for
an
update
for
pip
.
    
Limit
the
frequency
of
checks
to
once
per
week
.
State
is
stored
either
in
    
the
active
virtualenv
or
in
the
user
'
s
USER_CACHE_DIR
keyed
off
the
prefix
    
of
the
pip
script
path
.
    
"
"
"
    
installed_version
=
get_installed_version
(
"
pip
"
)
    
if
not
installed_version
:
        
return
    
pip_version
=
packaging_version
.
parse
(
installed_version
)
    
pypi_version
=
None
    
try
:
        
state
=
SelfCheckState
(
cache_dir
=
options
.
cache_dir
)
        
current_time
=
datetime
.
datetime
.
utcnow
(
)
        
if
"
last_check
"
in
state
.
state
and
"
pypi_version
"
in
state
.
state
:
            
last_check
=
datetime
.
datetime
.
strptime
(
                
state
.
state
[
"
last_check
"
]
                
SELFCHECK_DATE_FMT
            
)
            
if
(
current_time
-
last_check
)
.
total_seconds
(
)
<
7
*
24
*
60
*
60
:
                
pypi_version
=
state
.
state
[
"
pypi_version
"
]
        
if
pypi_version
is
None
:
            
link_collector
=
make_link_collector
(
                
session
                
options
=
options
                
suppress_no_index
=
True
            
)
            
selection_prefs
=
SelectionPreferences
(
                
allow_yanked
=
False
                
allow_all_prereleases
=
False
            
)
            
finder
=
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
            
)
            
best_candidate
=
finder
.
find_best_candidate
(
"
pip
"
)
.
best_candidate
            
if
best_candidate
is
None
:
                
return
            
pypi_version
=
str
(
best_candidate
.
version
)
            
state
.
save
(
pypi_version
current_time
)
        
remote_version
=
packaging_version
.
parse
(
pypi_version
)
        
local_version_is_older
=
(
            
pip_version
<
remote_version
and
            
pip_version
.
base_version
!
=
remote_version
.
base_version
and
            
was_installed_by_pip
(
'
pip
'
)
        
)
        
if
not
local_version_is_older
:
            
return
        
pip_cmd
=
"
{
}
-
m
pip
"
.
format
(
sys
.
executable
)
        
logger
.
warning
(
            
"
You
are
using
pip
version
%
s
;
however
version
%
s
is
"
            
"
available
.
\
nYou
should
consider
upgrading
via
the
"
            
"
'
%
s
install
-
-
upgrade
pip
'
command
.
"
            
pip_version
pypi_version
pip_cmd
        
)
    
except
Exception
:
        
logger
.
debug
(
            
"
There
was
an
error
checking
the
latest
version
of
pip
"
            
exc_info
=
True
        
)
