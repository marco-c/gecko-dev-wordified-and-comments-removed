from
__future__
import
absolute_import
print_function
import
json
import
os
import
subprocess
import
sys
from
pathlib
import
Path
from
textwrap
import
dedent
import
requests
import
six
.
moves
.
urllib
.
parse
as
urllib_parse
from
mozbuild
.
base
import
BuildEnvironmentNotFoundException
MozbuildObject
from
mozbuild
.
settings
import
TelemetrySettings
from
mozbuild
.
telemetry
import
filter_args
from
mozversioncontrol
import
InvalidRepoPath
get_repository_object
from
six
.
moves
import
configparser
input
from
mach
.
config
import
ConfigSettings
from
mach
.
site
import
MozSiteMetadata
from
mach
.
telemetry_interface
import
GleanTelemetry
NoopTelemetry
from
mach
.
util
import
get_state_dir
MACH_METRICS_PATH
=
(
Path
(
__file__
)
/
"
.
.
"
/
"
.
.
"
/
"
metrics
.
yaml
"
)
.
resolve
(
)
def
create_telemetry_from_environment
(
settings
)
:
    
"
"
"
Creates
and
a
Telemetry
instance
based
on
system
details
.
    
If
telemetry
isn
'
t
enabled
the
current
interpreter
isn
'
t
Python
3
or
Glean
    
can
'
t
be
imported
then
a
"
mock
"
telemetry
instance
is
returned
that
doesn
'
t
    
set
or
record
any
data
.
This
allows
consumers
to
optimistically
set
telemetry
    
data
without
needing
to
specifically
handle
the
case
where
the
current
system
    
doesn
'
t
support
it
.
    
"
"
"
    
active_metadata
=
MozSiteMetadata
.
from_runtime
(
)
    
is_mach_virtualenv
=
active_metadata
and
active_metadata
.
site_name
=
=
"
mach
"
    
if
not
(
        
is_applicable_telemetry_environment
(
)
        
and
sys
.
version_info
>
=
(
3
0
)
        
and
is_mach_virtualenv
    
)
:
        
return
NoopTelemetry
(
False
)
    
is_enabled
=
is_telemetry_enabled
(
settings
)
    
try
:
        
from
glean
import
Glean
    
except
ImportError
:
        
return
NoopTelemetry
(
is_enabled
)
    
from
pathlib
import
Path
    
Glean
.
initialize
(
        
"
mozilla
.
mach
"
        
"
Unknown
"
        
is_enabled
        
data_dir
=
Path
(
get_state_dir
(
)
)
/
"
glean
"
    
)
    
return
GleanTelemetry
(
)
def
report_invocation_metrics
(
telemetry
command
)
:
    
metrics
=
telemetry
.
metrics
(
MACH_METRICS_PATH
)
    
metrics
.
mach
.
command
.
set
(
command
)
    
metrics
.
mach
.
duration
.
start
(
)
    
try
:
        
instance
=
MozbuildObject
.
from_environment
(
)
    
except
BuildEnvironmentNotFoundException
:
        
return
    
metrics
.
mach
.
argv
.
set
(
        
filter_args
(
command
sys
.
argv
instance
.
topsrcdir
instance
.
topobjdir
)
    
)
def
is_applicable_telemetry_environment
(
)
:
    
if
os
.
environ
.
get
(
"
MACH_MAIN_PID
"
)
!
=
str
(
os
.
getpid
(
)
)
:
        
return
False
    
if
any
(
e
in
os
.
environ
for
e
in
(
"
MOZ_AUTOMATION
"
"
TASK_ID
"
)
)
:
        
return
False
    
return
True
def
is_telemetry_enabled
(
settings
)
:
    
if
os
.
environ
.
get
(
"
DISABLE_TELEMETRY
"
)
=
=
"
1
"
:
        
return
False
    
return
settings
.
mach_telemetry
.
is_enabled
def
arcrc_path
(
)
:
    
if
sys
.
platform
.
startswith
(
"
win32
"
)
or
sys
.
platform
.
startswith
(
"
msys
"
)
:
        
return
Path
(
os
.
environ
.
get
(
"
APPDATA
"
"
"
)
)
/
"
.
arcrc
"
    
else
:
        
return
Path
(
"
~
/
.
arcrc
"
)
.
expanduser
(
)
def
resolve_setting_from_arcconfig
(
topsrcdir
:
Path
setting
)
:
    
git_path
=
topsrcdir
/
"
.
git
"
    
if
git_path
.
is_file
(
)
:
        
git_path
=
subprocess
.
check_output
(
            
[
"
git
"
"
rev
-
parse
"
"
-
-
git
-
common
-
dir
"
]
            
cwd
=
str
(
topsrcdir
)
            
universal_newlines
=
True
        
)
        
git_path
=
Path
(
git_path
)
    
for
arcconfig_path
in
[
        
topsrcdir
/
"
.
hg
"
/
"
.
arcconfig
"
        
git_path
/
"
.
arcconfig
"
        
topsrcdir
/
"
.
arcconfig
"
    
]
:
        
try
:
            
with
open
(
arcconfig_path
"
r
"
)
as
arcconfig_file
:
                
arcconfig
=
json
.
load
(
arcconfig_file
)
        
except
(
json
.
JSONDecodeError
FileNotFoundError
)
:
            
continue
        
value
=
arcconfig
.
get
(
setting
)
        
if
value
:
            
return
value
def
resolve_is_employee_by_credentials
(
topsrcdir
:
Path
)
:
    
phabricator_uri
=
resolve_setting_from_arcconfig
(
topsrcdir
"
phabricator
.
uri
"
)
    
if
not
phabricator_uri
:
        
return
None
    
try
:
        
with
open
(
arcrc_path
(
)
"
r
"
)
as
arcrc_file
:
            
arcrc
=
json
.
load
(
arcrc_file
)
    
except
(
json
.
JSONDecodeError
FileNotFoundError
)
:
        
return
None
    
phabricator_token
=
(
        
arcrc
.
get
(
"
hosts
"
{
}
)
        
.
get
(
urllib_parse
.
urljoin
(
phabricator_uri
"
api
/
"
)
{
}
)
        
.
get
(
"
token
"
)
    
)
    
if
not
phabricator_token
:
        
return
None
    
bmo_uri
=
(
        
resolve_setting_from_arcconfig
(
topsrcdir
"
bmo_url
"
)
        
or
"
https
:
/
/
bugzilla
.
mozilla
.
org
"
    
)
    
bmo_api_url
=
urllib_parse
.
urljoin
(
bmo_uri
"
rest
/
whoami
"
)
    
bmo_result
=
requests
.
get
(
        
bmo_api_url
headers
=
{
"
X
-
PHABRICATOR
-
TOKEN
"
:
phabricator_token
}
    
)
    
return
"
mozilla
-
employee
-
confidential
"
in
bmo_result
.
json
(
)
.
get
(
"
groups
"
[
]
)
def
resolve_is_employee_by_vcs
(
topsrcdir
:
Path
)
:
    
try
:
        
vcs
=
get_repository_object
(
str
(
topsrcdir
)
)
    
except
InvalidRepoPath
:
        
return
None
    
email
=
vcs
.
get_user_email
(
)
    
if
not
email
:
        
return
None
    
return
"
mozilla
.
com
"
in
email
def
resolve_is_employee
(
topsrcdir
:
Path
)
:
    
"
"
"
Detect
whether
or
not
the
current
user
is
a
Mozilla
employee
.
    
Checks
using
Bugzilla
authentication
if
possible
.
Otherwise
falls
back
to
checking
    
if
email
configured
in
VCS
is
"
mozilla
.
com
"
.
    
Returns
True
if
the
user
could
be
identified
as
an
employee
False
if
the
user
    
is
confirmed
as
not
being
an
employee
or
None
if
the
user
couldn
'
t
be
    
identified
.
    
"
"
"
    
is_employee
=
resolve_is_employee_by_credentials
(
topsrcdir
)
    
if
is_employee
is
not
None
:
        
return
is_employee
    
return
resolve_is_employee_by_vcs
(
topsrcdir
)
or
False
def
record_telemetry_settings
(
    
main_settings
    
state_dir
:
Path
    
is_enabled
)
:
    
settings_path
=
state_dir
/
"
machrc
"
    
file_settings
=
ConfigSettings
(
)
    
file_settings
.
register_provider
(
TelemetrySettings
)
    
try
:
        
file_settings
.
load_file
(
settings_path
)
    
except
configparser
.
Error
as
error
:
        
print
(
            
f
"
Your
mach
configuration
file
at
{
settings_path
}
cannot
be
parsed
:
\
n
{
error
}
"
        
)
        
return
    
file_settings
.
mach_telemetry
.
is_enabled
=
is_enabled
    
file_settings
.
mach_telemetry
.
is_set_up
=
True
    
with
open
(
settings_path
"
w
"
)
as
f
:
        
file_settings
.
write
(
f
)
    
main_settings
.
mach_telemetry
.
is_enabled
=
is_enabled
    
main_settings
.
mach_telemetry
.
is_set_up
=
True
TELEMETRY_DESCRIPTION_PREAMBLE
=
"
"
"
Mozilla
collects
data
to
improve
the
developer
experience
.
To
learn
more
about
the
data
we
intend
to
collect
read
here
:
  
https
:
/
/
firefox
-
source
-
docs
.
mozilla
.
org
/
build
/
buildsystem
/
telemetry
.
html
If
you
have
questions
please
ask
in
#
build
on
Matrix
:
  
https
:
/
/
chat
.
mozilla
.
org
/
#
/
room
/
#
build
:
mozilla
.
org
"
"
"
.
strip
(
)
def
print_telemetry_message_employee
(
)
:
    
message_template
=
dedent
(
        
"
"
"
    
%
s
    
As
a
Mozilla
employee
telemetry
has
been
automatically
enabled
.
    
"
"
"
    
)
.
strip
(
)
    
print
(
message_template
%
TELEMETRY_DESCRIPTION_PREAMBLE
)
    
return
True
def
prompt_telemetry_message_contributor
(
)
:
    
while
True
:
        
prompt
=
(
            
dedent
(
                
"
"
"
        
%
s
        
If
you
'
d
like
to
opt
out
of
data
collection
select
(
N
)
at
the
prompt
.
        
Would
you
like
to
enable
build
system
telemetry
?
(
Yn
)
:
"
"
"
            
)
            
%
TELEMETRY_DESCRIPTION_PREAMBLE
        
)
.
strip
(
)
        
choice
=
input
(
prompt
)
        
choice
=
choice
.
strip
(
)
.
lower
(
)
        
if
choice
=
=
"
"
:
            
return
True
        
if
choice
not
in
(
"
y
"
"
n
"
)
:
            
print
(
"
ERROR
!
Please
enter
y
or
n
!
"
)
        
else
:
            
return
choice
=
=
"
y
"
def
initialize_telemetry_setting
(
settings
topsrcdir
:
str
state_dir
:
str
)
:
    
"
"
"
Enables
telemetry
for
employees
or
prompts
the
user
.
"
"
"
    
if
topsrcdir
is
not
None
:
        
topsrcdir
=
Path
(
topsrcdir
)
    
if
state_dir
is
not
None
:
        
state_dir
=
Path
(
state_dir
)
    
if
os
.
environ
.
get
(
"
DISABLE_TELEMETRY
"
)
=
=
"
1
"
:
        
return
    
try
:
        
is_employee
=
resolve_is_employee
(
topsrcdir
)
    
except
requests
.
exceptions
.
RequestException
:
        
return
    
if
is_employee
:
        
is_enabled
=
True
        
print_telemetry_message_employee
(
)
    
else
:
        
is_enabled
=
prompt_telemetry_message_contributor
(
)
    
record_telemetry_settings
(
settings
state_dir
is_enabled
)
