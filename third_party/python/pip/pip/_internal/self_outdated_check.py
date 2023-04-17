import
datetime
import
hashlib
import
json
import
logging
import
optparse
import
os
.
path
import
sys
from
typing
import
Any
Dict
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
_internal
.
index
.
collector
import
LinkCollector
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
get_default_environment
from
pip
.
_internal
.
models
.
selection_prefs
import
SelectionPreferences
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
utils
.
filesystem
import
adjacent_tmp_file
check_path_owner
replace
from
pip
.
_internal
.
utils
.
misc
import
ensure_dir
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
_get_statefile_name
(
key
)
:
    
key_bytes
=
key
.
encode
(
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
encoding
=
"
utf
-
8
"
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
OSError
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
text
.
encode
(
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
    
dist
=
get_default_environment
(
)
.
get_distribution
(
pkg
)
    
return
dist
is
not
None
and
"
pip
"
=
=
dist
.
installer
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
    
installed_dist
=
get_default_environment
(
)
.
get_distribution
(
"
pip
"
)
    
if
not
installed_dist
:
        
return
    
pip_version
=
installed_dist
.
version
    
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
LinkCollector
.
create
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
parse_version
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
f
"
{
sys
.
executable
}
-
m
pip
"
        
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
