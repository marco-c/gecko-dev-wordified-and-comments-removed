from
__future__
import
absolute_import
print_function
unicode_literals
import
ast
import
enum
import
functools
import
json
import
os
import
platform
import
shutil
import
site
import
subprocess
import
sys
from
pathlib
import
Path
import
tempfile
from
contextlib
import
contextmanager
from
typing
import
Optional
Callable
from
mach
.
requirements
import
(
    
MachEnvRequirements
)
PTH_FILENAME
=
"
mach
.
pth
"
METADATA_FILENAME
=
"
moz_virtualenv_metadata
.
json
"
class
VirtualenvOutOfDateException
(
Exception
)
:
    
pass
class
MozSiteMetadataOutOfDateError
(
Exception
)
:
    
pass
class
SitePackagesSource
(
enum
.
Enum
)
:
    
NONE
=
enum
.
auto
(
)
    
SYSTEM
=
enum
.
auto
(
)
    
VENV
=
enum
.
auto
(
)
class
MozSiteMetadata
:
    
"
"
"
Details
about
a
Moz
-
managed
python
site
    
When
a
Moz
-
managed
site
is
active
its
associated
metadata
is
available
    
at
"
MozSiteMetadata
.
current
"
.
    
Sites
that
have
associated
virtualenvs
(
so
those
that
aren
'
t
strictly
leaning
on
    
the
external
python
packages
)
will
have
their
metadata
written
to
    
<
prefix
>
/
moz_virtualenv_metadata
.
json
.
    
"
"
"
    
current
:
Optional
[
"
MozSiteMetadata
"
]
=
None
    
def
__init__
(
        
self
        
hex_version
:
int
        
site_name
:
str
        
site_packages_source
:
SitePackagesSource
        
mach_site_packages_source
:
SitePackagesSource
        
external_python
:
"
ExternalPythonSite
"
        
prefix
:
str
    
)
:
        
"
"
"
        
Args
:
            
hex_version
:
The
python
version
number
from
sys
.
hexversion
            
site_name
:
The
name
of
the
site
this
metadata
is
associated
with
            
site_packages_source
:
Where
this
site
imports
its
                
pip
-
installed
dependencies
from
            
mach_site_packages_source
:
Where
the
Mach
site
imports
                
its
pip
-
installed
dependencies
from
            
external_python
:
The
external
Python
site
that
was
                
used
to
invoke
Mach
.
Usually
the
system
Python
such
as
/
usr
/
bin
/
python3
            
prefix
:
The
same
value
as
"
sys
.
prefix
"
is
when
running
within
the
                
associated
Python
site
.
The
same
thing
as
the
"
virtualenv
root
"
.
        
"
"
"
        
self
.
hex_version
=
hex_version
        
self
.
site_name
=
site_name
        
self
.
site_packages_source
=
site_packages_source
        
self
.
mach_site_packages_source
=
mach_site_packages_source
        
self
.
external_python
=
external_python
        
self
.
prefix
=
prefix
    
def
write
(
self
is_finalized
)
:
        
raw
=
{
            
"
hex_version
"
:
self
.
hex_version
            
"
virtualenv_name
"
:
self
.
site_name
            
"
site_packages_source
"
:
self
.
site_packages_source
.
name
            
"
mach_site_packages_source
"
:
self
.
mach_site_packages_source
.
name
            
"
external_python_executable
"
:
self
.
external_python
.
python_path
            
"
is_finalized
"
:
is_finalized
        
}
        
with
open
(
os
.
path
.
join
(
self
.
prefix
METADATA_FILENAME
)
"
w
"
)
as
file
:
            
json
.
dump
(
raw
file
)
    
def
__eq__
(
self
other
)
:
        
return
(
            
type
(
self
)
=
=
type
(
other
)
            
and
self
.
hex_version
=
=
other
.
hex_version
            
and
self
.
site_name
=
=
other
.
site_name
            
and
self
.
site_packages_source
=
=
other
.
site_packages_source
            
and
self
.
mach_site_packages_source
=
=
other
.
mach_site_packages_source
            
and
self
.
external_python
.
python_path
=
=
other
.
external_python
.
python_path
        
)
    
classmethod
    
def
from_runtime
(
cls
)
:
        
if
cls
.
current
:
            
return
cls
.
current
        
return
cls
.
from_path
(
sys
.
prefix
)
    
classmethod
    
def
from_path
(
cls
prefix
)
:
        
metadata_path
=
os
.
path
.
join
(
prefix
METADATA_FILENAME
)
        
out_of_date_exception
=
MozSiteMetadataOutOfDateError
(
            
f
'
The
virtualenv
at
"
{
prefix
}
"
is
out
-
of
-
date
.
'
        
)
        
try
:
            
with
open
(
metadata_path
"
r
"
)
as
file
:
                
raw
=
json
.
load
(
file
)
            
if
not
raw
.
get
(
"
is_finalized
"
False
)
:
                
raise
out_of_date_exception
            
return
cls
(
                
raw
[
"
hex_version
"
]
                
raw
[
"
virtualenv_name
"
]
                
SitePackagesSource
[
raw
[
"
site_packages_source
"
]
]
                
SitePackagesSource
[
raw
[
"
mach_site_packages_source
"
]
]
                
ExternalPythonSite
(
raw
[
"
external_python_executable
"
]
)
                
metadata_path
            
)
        
except
FileNotFoundError
:
            
return
None
        
except
KeyError
:
            
raise
out_of_date_exception
    
contextmanager
    
def
update_current_site
(
self
executable
)
:
        
"
"
"
Updates
necessary
global
state
when
a
site
is
activated
        
Due
to
needing
to
fetch
some
state
before
the
actual
activation
happens
this
        
is
represented
as
a
context
manager
and
should
be
used
as
follows
:
        
with
metadata
.
update_current_site
(
executable
)
:
            
#
Perform
the
actual
implementation
of
changing
the
site
whether
that
is
            
#
by
exec
-
ing
"
activate_this
.
py
"
in
a
virtualenv
modifying
the
sys
.
path
            
#
directly
or
some
other
means
            
.
.
.
        
"
"
"
        
try
:
            
import
pkg_resources
        
except
ModuleNotFoundError
:
            
pkg_resources
=
None
        
yield
        
MozSiteMetadata
.
current
=
self
        
sys
.
executable
=
executable
        
if
pkg_resources
:
            
pkg_resources
.
_initialize_master_working_set
(
)
class
MachSiteManager
:
    
"
"
"
Represents
the
activate
-
able
"
import
scope
"
Mach
needs
    
Whether
running
independently
using
the
system
packages
or
automatically
managing
    
dependencies
with
"
pip
install
"
this
class
provides
an
easy
handle
to
verify
    
that
the
"
site
"
is
up
-
to
-
date
(
whether
than
means
that
system
packages
don
'
t
    
collide
with
vendored
packages
or
that
the
on
-
disk
virtualenv
needs
rebuilding
)
.
    
Note
that
this
is
a
*
virtual
*
site
:
an
on
-
disk
Python
virtualenv
    
is
only
created
if
there
will
be
"
pip
installs
"
into
the
Mach
site
.
    
"
"
"
    
def
__init__
(
        
self
        
topsrcdir
:
str
        
state_dir
:
Optional
[
str
]
        
requirements
:
MachEnvRequirements
        
external_python
:
"
ExternalPythonSite
"
        
site_packages_source
:
SitePackagesSource
    
)
:
        
"
"
"
        
Args
:
            
topsrcdir
:
The
path
to
the
Firefox
repo
            
state_dir
:
The
path
to
the
state_dir
generally
~
/
.
mozbuild
            
requirements
:
The
requirements
associated
with
the
Mach
site
parsed
from
                
the
file
at
build
/
mach_virtualenv_packages
.
txt
            
external_python
:
The
external
Python
site
that
was
used
to
invoke
Mach
.
                
Usually
the
system
Python
such
as
/
usr
/
bin
/
python3
            
site_packages_source
:
Where
the
Mach
site
will
import
its
pip
-
installed
                
dependencies
from
        
"
"
"
        
self
.
_topsrcdir
=
topsrcdir
        
self
.
_external_python
=
external_python
        
self
.
_site_packages_source
=
site_packages_source
        
self
.
_requirements
=
requirements
        
self
.
_virtualenv_root
=
_mach_virtualenv_root
(
state_dir
)
if
state_dir
else
None
        
self
.
_metadata
=
MozSiteMetadata
(
            
sys
.
hexversion
            
"
mach
"
            
site_packages_source
            
site_packages_source
            
external_python
            
self
.
_virtualenv_root
        
)
    
classmethod
    
def
from_environment
(
cls
topsrcdir
:
str
get_state_dir
:
Callable
[
[
]
str
]
)
:
        
"
"
"
        
Args
:
            
topsrcdir
:
The
path
to
the
Firefox
repo
            
get_state_dir
:
A
function
that
resolve
the
path
to
the
workdir
-
scoped
                
state_dir
generally
~
/
.
mozbuild
/
srcdirs
/
<
worktree
-
based
-
dir
>
/
        
"
"
"
        
requirements
=
resolve_requirements
(
topsrcdir
"
mach
"
)
        
assert
(
            
not
requirements
.
pypi_requirements
        
)
"
Mach
pip
package
requirements
must
be
optional
.
"
        
active_metadata
=
MozSiteMetadata
.
from_runtime
(
)
        
if
active_metadata
:
            
external_python
=
active_metadata
.
external_python
        
else
:
            
external_python
=
ExternalPythonSite
(
sys
.
executable
)
        
if
not
_system_python_env_variable_present
(
)
:
            
source
=
SitePackagesSource
.
VENV
            
state_dir
=
get_state_dir
(
)
        
elif
not
external_python
.
has_pip
(
)
:
            
source
=
SitePackagesSource
.
NONE
            
state_dir
=
None
        
else
:
            
source
=
(
                
SitePackagesSource
.
SYSTEM
                
if
external_python
.
provides_any_package
(
"
mach
"
requirements
)
                
else
SitePackagesSource
.
NONE
            
)
            
state_dir
=
None
        
return
cls
(
            
topsrcdir
            
state_dir
            
requirements
            
external_python
            
source
        
)
    
def
up_to_date
(
self
)
:
        
if
self
.
_site_packages_source
=
=
SitePackagesSource
.
NONE
:
            
return
True
        
elif
self
.
_site_packages_source
=
=
SitePackagesSource
.
SYSTEM
:
            
pthfile_lines
=
[
                
*
self
.
_requirements
.
pths_as_absolute
(
self
.
_topsrcdir
)
                
*
self
.
_external_python
.
all_site_packages_dirs
(
)
            
]
            
_assert_pip_check
(
self
.
_topsrcdir
pthfile_lines
"
mach
"
)
            
return
True
        
elif
self
.
_site_packages_source
=
=
SitePackagesSource
.
VENV
:
            
environment
=
self
.
_virtualenv
(
)
            
return
_is_venv_up_to_date
(
                
self
.
_topsrcdir
                
environment
                
self
.
_pthfile_lines
(
environment
)
                
self
.
_requirements
                
self
.
_metadata
            
)
    
def
ensure
(
self
*
force
=
False
)
:
        
up_to_date
=
self
.
up_to_date
(
)
        
if
force
or
not
up_to_date
:
            
if
Path
(
sys
.
prefix
)
=
=
Path
(
self
.
_metadata
.
prefix
)
:
                
raise
VirtualenvOutOfDateException
(
)
            
self
.
_build
(
)
        
return
up_to_date
    
def
activate
(
self
)
:
        
assert
not
MozSiteMetadata
.
current
        
self
.
ensure
(
)
        
with
self
.
_metadata
.
update_current_site
(
            
self
.
_virtualenv
(
)
.
python_path
            
if
self
.
_site_packages_source
=
=
SitePackagesSource
.
VENV
            
else
sys
.
executable
        
)
:
            
if
self
.
_site_packages_source
=
=
SitePackagesSource
.
SYSTEM
:
                
sys
.
path
[
0
:
0
]
=
self
.
_requirements
.
pths_as_absolute
(
self
.
_topsrcdir
)
            
elif
self
.
_site_packages_source
=
=
SitePackagesSource
.
NONE
:
                
sys
.
path
=
[
                    
path
                    
for
path
in
sys
.
path
                    
if
path
                    
not
in
ExternalPythonSite
(
sys
.
executable
)
.
all_site_packages_dirs
(
)
                
]
                
sys
.
path
[
0
:
0
]
=
self
.
_requirements
.
pths_as_absolute
(
self
.
_topsrcdir
)
            
elif
self
.
_site_packages_source
=
=
SitePackagesSource
.
VENV
:
                
if
Path
(
sys
.
prefix
)
!
=
Path
(
self
.
_metadata
.
prefix
)
:
                    
sys
.
path
=
[
                        
path
                        
for
path
in
sys
.
path
                        
if
path
                        
not
in
ExternalPythonSite
(
                            
sys
.
executable
                        
)
.
all_site_packages_dirs
(
)
                    
]
                    
activate_path
=
self
.
_virtualenv
(
)
.
activate_path
                    
exec
(
open
(
activate_path
)
.
read
(
)
dict
(
__file__
=
activate_path
)
)
    
def
_build
(
self
)
:
        
if
self
.
_site_packages_source
!
=
SitePackagesSource
.
VENV
:
            
return
        
environment
=
self
.
_virtualenv
(
)
        
_create_venv_with_pthfile
(
            
self
.
_topsrcdir
            
environment
            
self
.
_pthfile_lines
(
environment
)
            
self
.
_site_packages_source
            
self
.
_requirements
            
self
.
_metadata
        
)
    
def
_pthfile_lines
(
self
environment
)
:
        
return
[
            
*
self
.
_requirements
.
pths_as_absolute
(
self
.
_topsrcdir
)
            
*
_deprioritize_venv_packages
(
environment
.
site_packages_dir
(
)
)
        
]
    
def
_virtualenv
(
self
)
:
        
assert
self
.
_site_packages_source
=
=
SitePackagesSource
.
VENV
        
return
PythonVirtualenv
(
self
.
_metadata
.
prefix
)
class
CommandSiteManager
:
    
"
"
"
Activate
sites
and
ad
-
hoc
-
install
pip
packages
    
Provides
tools
to
ensure
that
a
command
'
s
scope
will
have
expected
compatible
    
packages
.
Manages
prioritization
of
the
import
scope
and
ensures
consistency
    
regardless
of
how
a
virtualenv
is
used
(
whether
via
in
-
process
activation
or
when
    
used
standalone
to
invoke
a
script
)
.
    
A
few
notes
:
    
*
The
command
environment
always
inherits
Mach
'
s
import
scope
.
This
is
because
      
"
unloading
"
packages
in
Python
is
error
-
prone
so
in
-
process
activations
will
always
      
carry
Mach
'
s
dependencies
along
with
it
.
Accordingly
compatibility
between
each
      
command
environment
and
the
Mach
environment
must
be
maintained
    
*
Unlike
the
Mach
environment
command
environments
*
always
*
have
an
associated
      
physical
virtualenv
on
-
disk
.
This
is
because
some
commands
invoke
child
Python
      
processes
and
that
child
process
should
have
the
same
import
scope
.
    
"
"
"
    
def
__init__
(
        
self
        
topsrcdir
:
str
        
state_dir
:
str
        
virtualenv_root
:
str
        
site_name
:
str
        
active_metadata
:
MozSiteMetadata
        
site_packages_source
:
SitePackagesSource
        
requirements
:
MachEnvRequirements
    
)
:
        
"
"
"
        
Args
:
            
topsrcdir
:
The
path
to
the
Firefox
repo
            
state_dir
:
The
path
to
the
state_dir
generally
~
/
.
mozbuild
            
virtualenv_root
:
The
path
to
the
virtualenv
associated
with
this
site
            
site_name
:
The
name
of
this
site
such
as
"
build
"
            
active_metadata
:
The
currently
-
active
moz
-
managed
site
            
site_packages_source
:
Where
this
site
will
import
its
pip
-
installed
                
dependencies
from
            
requirements
:
The
requirements
associated
with
this
site
parsed
from
                
the
file
at
build
/
<
site_name
>
_virtualenv_packages
.
txt
        
"
"
"
        
self
.
_topsrcdir
=
topsrcdir
        
self
.
_state_dir
=
state_dir
        
self
.
virtualenv_root
=
virtualenv_root
        
self
.
_site_name
=
site_name
        
self
.
_virtualenv
=
PythonVirtualenv
(
self
.
virtualenv_root
)
        
self
.
python_path
=
self
.
_virtualenv
.
python_path
        
self
.
bin_path
=
self
.
_virtualenv
.
bin_path
        
self
.
_site_packages_source
=
site_packages_source
        
self
.
_mach_site_packages_source
=
active_metadata
.
mach_site_packages_source
        
self
.
_external_python
=
active_metadata
.
external_python
        
self
.
_requirements
=
requirements
        
self
.
_metadata
=
MozSiteMetadata
(
            
sys
.
hexversion
            
site_name
            
site_packages_source
            
active_metadata
.
mach_site_packages_source
            
active_metadata
.
external_python
            
virtualenv_root
        
)
    
classmethod
    
def
from_environment
(
        
cls
        
topsrcdir
:
str
        
state_dir
:
str
        
site_name
:
str
        
command_virtualenvs_dir
:
str
    
)
:
        
"
"
"
        
Args
:
            
topsrcdir
:
The
path
to
the
Firefox
repo
            
state_dir
:
The
path
to
the
state_dir
generally
~
/
.
mozbuild
            
site_name
:
The
name
of
this
site
such
as
"
build
"
            
command_virtualenvs_dir
:
The
location
under
which
this
site
'
s
virtualenv
            
should
be
created
        
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
        
assert
(
            
active_metadata
        
)
"
A
Mach
-
managed
site
must
be
active
before
doing
work
with
command
sites
"
        
requirements
=
resolve_requirements
(
topsrcdir
site_name
)
        
if
not
_system_python_env_variable_present
(
)
or
site_name
!
=
"
build
"
:
            
source
=
SitePackagesSource
.
VENV
        
elif
not
active_metadata
.
external_python
.
has_pip
(
)
:
            
if
requirements
.
pypi_requirements
:
                
raise
Exception
(
                    
f
'
The
"
{
site_name
}
"
site
requires
pip
'
                    
"
packages
and
Mach
has
been
told
to
find
such
pip
packages
in
"
                    
"
the
system
environment
but
it
can
'
t
because
the
system
doesn
'
t
"
                    
'
have
"
pip
"
installed
.
'
                
)
            
source
=
SitePackagesSource
.
NONE
        
else
:
            
source
=
(
                
SitePackagesSource
.
SYSTEM
                
if
active_metadata
.
external_python
.
provides_any_package
(
                    
site_name
requirements
                
)
                
else
SitePackagesSource
.
NONE
            
)
        
return
cls
(
            
topsrcdir
            
state_dir
            
os
.
path
.
join
(
command_virtualenvs_dir
site_name
)
            
site_name
            
active_metadata
            
source
            
requirements
        
)
    
def
ensure
(
self
)
:
        
"
"
"
Ensure
that
this
virtualenv
is
built
up
-
to
-
date
and
ready
for
use
        
If
using
a
virtualenv
Python
binary
directly
it
'
s
useful
to
call
this
function
        
first
to
ensure
that
the
virtualenv
doesn
'
t
have
obsolete
references
or
packages
.
        
"
"
"
        
if
not
self
.
_up_to_date
(
)
:
            
_create_venv_with_pthfile
(
                
self
.
_topsrcdir
                
self
.
_virtualenv
                
self
.
_pthfile_lines
(
)
                
self
.
_site_packages_source
                
self
.
_requirements
                
self
.
_metadata
            
)
    
def
activate
(
self
)
:
        
"
"
"
Activate
this
site
in
the
current
Python
context
.
        
If
you
run
a
random
Python
script
and
wish
to
"
activate
"
the
        
site
you
can
simply
instantiate
an
instance
of
this
class
        
and
call
.
activate
(
)
to
make
the
virtualenv
active
.
        
"
"
"
        
self
.
ensure
(
)
        
with
self
.
_metadata
.
update_current_site
(
self
.
_virtualenv
.
python_path
)
:
            
activate_path
=
self
.
_virtualenv
.
activate_path
            
exec
(
open
(
activate_path
)
.
read
(
)
dict
(
__file__
=
activate_path
)
)
    
def
install_pip_package
(
self
package
)
:
        
"
"
"
Install
a
package
via
pip
.
        
The
supplied
package
is
specified
using
a
pip
requirement
specifier
.
        
e
.
g
.
'
foo
'
or
'
foo
=
=
1
.
0
'
.
        
If
the
package
is
already
installed
this
is
a
no
-
op
.
        
"
"
"
        
if
Path
(
sys
.
prefix
)
=
=
Path
(
self
.
virtualenv_root
)
:
            
from
pip
.
_internal
.
req
.
constructors
import
install_req_from_line
            
req
=
install_req_from_line
(
package
)
            
req
.
check_if_exists
(
use_user_site
=
False
)
            
if
req
.
satisfied_by
is
not
None
:
                
return
        
self
.
_virtualenv
.
pip_install
(
[
package
]
)
    
def
install_pip_requirements
(
self
path
require_hashes
=
True
quiet
=
False
)
:
        
"
"
"
Install
a
pip
requirements
.
txt
file
.
        
The
supplied
path
is
a
text
file
containing
pip
requirement
        
specifiers
.
        
If
require_hashes
is
True
each
specifier
must
contain
the
        
expected
hash
of
the
downloaded
package
.
See
:
        
https
:
/
/
pip
.
pypa
.
io
/
en
/
stable
/
reference
/
pip_install
/
#
hash
-
checking
-
mode
        
"
"
"
        
if
not
os
.
path
.
isabs
(
path
)
:
            
path
=
os
.
path
.
join
(
self
.
_topsrcdir
path
)
        
args
=
[
"
-
-
requirement
"
path
]
        
if
require_hashes
:
            
args
.
append
(
"
-
-
require
-
hashes
"
)
        
if
quiet
:
            
args
.
append
(
"
-
-
quiet
"
)
        
self
.
_virtualenv
.
pip_install
(
args
)
    
def
_pthfile_lines
(
self
)
:
        
"
"
"
Generate
the
prioritized
import
scope
to
encode
in
the
venv
'
s
pthfile
        
The
import
priority
looks
like
this
:
        
1
.
Mach
'
s
vendored
/
first
-
party
modules
        
2
.
Mach
'
s
site
-
package
source
(
the
Mach
virtualenv
the
system
Python
or
neither
)
        
3
.
The
command
'
s
vendored
/
first
-
party
modules
        
4
.
The
command
'
s
site
-
package
source
(
either
the
virtualenv
or
the
system
Python
           
if
it
'
s
not
already
added
)
        
Note
that
when
using
the
system
Python
it
may
either
be
prioritized
before
or
        
after
the
command
'
s
vendored
/
first
-
party
modules
.
This
is
a
symptom
of
us
        
attempting
to
avoid
conflicting
with
the
system
packages
.
        
For
example
there
'
s
at
least
one
job
in
CI
that
operates
with
an
ancient
        
environment
with
a
bunch
of
old
packages
many
of
whom
conflict
with
our
vendored
        
packages
.
However
the
specific
command
that
we
'
re
running
for
the
job
doesn
'
t
        
need
any
of
the
system
'
s
packages
so
we
'
re
safe
to
insulate
ourselves
.
        
Mach
doesn
'
t
know
the
command
being
run
when
it
'
s
preparing
its
import
scope
        
so
it
has
to
be
defensive
.
Therefore
:
        
1
.
If
Mach
needs
a
system
package
:
system
packages
are
higher
priority
.
        
2
.
If
Mach
doesn
'
t
need
a
system
package
but
the
current
command
does
:
system
           
packages
are
still
be
in
the
list
albeit
at
a
lower
priority
.
        
"
"
"
        
lines
=
resolve_requirements
(
self
.
_topsrcdir
"
mach
"
)
.
pths_as_absolute
(
            
self
.
_topsrcdir
        
)
        
mach_site_packages_source
=
self
.
_mach_site_packages_source
        
if
mach_site_packages_source
=
=
SitePackagesSource
.
SYSTEM
:
            
lines
.
extend
(
self
.
_external_python
.
all_site_packages_dirs
(
)
)
        
elif
mach_site_packages_source
=
=
SitePackagesSource
.
VENV
:
            
lines
.
append
(
                
PythonVirtualenv
(
                    
_mach_virtualenv_root
(
self
.
_state_dir
)
                
)
.
site_packages_dir
(
)
            
)
        
lines
.
extend
(
self
.
_requirements
.
pths_as_absolute
(
self
.
_topsrcdir
)
)
        
if
(
            
self
.
_site_packages_source
=
=
SitePackagesSource
.
SYSTEM
            
and
not
mach_site_packages_source
=
=
SitePackagesSource
.
SYSTEM
        
)
:
            
lines
.
extend
(
self
.
_external_python
.
all_site_packages_dirs
(
)
)
        
elif
self
.
_site_packages_source
=
=
SitePackagesSource
.
VENV
:
            
site_packages_dir
=
self
.
_virtualenv
.
site_packages_dir
(
)
            
lines
.
extend
(
_deprioritize_venv_packages
(
site_packages_dir
)
)
        
return
lines
    
def
_up_to_date
(
self
)
:
        
if
self
.
_site_packages_source
=
=
SitePackagesSource
.
SYSTEM
:
            
_assert_pip_check
(
self
.
_topsrcdir
self
.
_pthfile_lines
(
)
self
.
_site_name
)
        
return
_is_venv_up_to_date
(
            
self
.
_topsrcdir
            
self
.
_virtualenv
            
self
.
_pthfile_lines
(
)
            
self
.
_requirements
            
self
.
_metadata
        
)
class
PythonVirtualenv
:
    
"
"
"
Calculates
paths
of
interest
for
general
python
virtual
environments
"
"
"
    
def
__init__
(
self
prefix
)
:
        
is_windows
=
sys
.
platform
=
=
"
cygwin
"
or
(
            
sys
.
platform
=
=
"
win32
"
and
os
.
sep
=
=
"
\
\
"
        
)
        
if
is_windows
:
            
self
.
bin_path
=
os
.
path
.
join
(
prefix
"
Scripts
"
)
            
self
.
python_path
=
os
.
path
.
join
(
self
.
bin_path
"
python
.
exe
"
)
        
else
:
            
self
.
bin_path
=
os
.
path
.
join
(
prefix
"
bin
"
)
            
self
.
python_path
=
os
.
path
.
join
(
self
.
bin_path
"
python
"
)
        
self
.
activate_path
=
os
.
path
.
join
(
self
.
bin_path
"
activate_this
.
py
"
)
        
self
.
prefix
=
prefix
    
functools
.
lru_cache
(
maxsize
=
None
)
    
def
site_packages_dir
(
self
)
:
        
from
distutils
import
dist
        
normalized_venv_root
=
os
.
path
.
normpath
(
self
.
prefix
)
        
distribution
=
dist
.
Distribution
(
{
"
script_args
"
:
"
-
-
no
-
user
-
cfg
"
}
)
        
installer
=
distribution
.
get_command_obj
(
"
install
"
)
        
installer
.
prefix
=
normalized_venv_root
        
installer
.
finalize_options
(
)
        
path
=
installer
.
install_purelib
        
local_folder
=
os
.
path
.
join
(
normalized_venv_root
"
local
"
)
        
if
path
.
startswith
(
local_folder
)
:
            
path
=
os
.
path
.
join
(
normalized_venv_root
path
[
len
(
local_folder
)
+
1
:
]
)
        
return
path
    
def
pip_install
(
self
pip_install_args
)
:
        
env
=
os
.
environ
.
copy
(
)
        
env
.
setdefault
(
"
ARCHFLAGS
"
"
-
arch
{
}
"
.
format
(
platform
.
machine
(
)
)
)
        
subprocess
.
run
(
            
[
self
.
python_path
"
-
m
"
"
pip
"
"
install
"
]
+
pip_install_args
            
env
=
env
            
universal_newlines
=
True
            
stderr
=
subprocess
.
STDOUT
            
check
=
True
        
)
class
ExternalSitePackageValidationResult
:
    
def
__init__
(
self
)
:
        
self
.
_package_discrepancies
=
[
]
        
self
.
has_all_packages
=
True
        
self
.
provides_any_package
=
False
    
def
add_discrepancy
(
self
requirement
found
)
:
        
self
.
_package_discrepancies
.
append
(
(
requirement
found
)
)
        
self
.
has_all_packages
=
False
    
def
report
(
self
)
:
        
lines
=
[
]
        
for
requirement
found
in
self
.
_package_discrepancies
:
            
if
found
:
                
error
=
f
'
Installed
with
unexpected
version
"
{
found
}
"
'
            
else
:
                
error
=
"
Not
installed
"
            
lines
.
append
(
f
"
{
requirement
}
:
{
error
}
"
)
        
return
"
\
n
"
.
join
(
lines
)
class
ExternalPythonSite
:
    
"
"
"
Represents
the
Python
site
that
is
executing
Mach
    
The
external
Python
site
could
be
a
virtualenv
(
created
by
venv
or
virtualenv
)
or
    
the
system
Python
itself
so
we
can
'
t
make
any
significant
assumptions
on
its
    
structure
.
    
"
"
"
    
def
__init__
(
self
python_executable
)
:
        
self
.
_prefix
=
os
.
path
.
dirname
(
os
.
path
.
dirname
(
python_executable
)
)
        
self
.
python_path
=
python_executable
    
functools
.
lru_cache
(
maxsize
=
None
)
    
def
all_site_packages_dirs
(
self
)
:
        
if
self
.
_prefix
=
=
sys
.
prefix
:
            
return
[
site
.
getusersitepackages
(
)
]
+
site
.
getsitepackages
(
)
        
else
:
            
paths_string
=
subprocess
.
check_output
(
                
[
                    
self
.
python_path
                    
"
-
c
"
                    
"
import
site
;
print
(
[
site
.
getusersitepackages
(
)
]
"
                    
"
+
site
.
getsitepackages
(
)
)
"
                
]
                
env
=
{
k
:
v
for
k
v
in
os
.
environ
.
items
(
)
if
k
!
=
"
VIRTUAL_ENV
"
}
                
universal_newlines
=
True
            
)
            
return
ast
.
literal_eval
(
paths_string
)
    
functools
.
lru_cache
(
maxsize
=
None
)
    
def
has_pip
(
self
)
:
        
return
(
            
subprocess
.
run
(
                
[
self
.
python_path
"
-
c
"
"
import
pip
"
]
stderr
=
subprocess
.
DEVNULL
            
)
.
returncode
            
=
=
0
        
)
    
def
provides_any_package
(
self
virtualenv_name
requirements
)
:
        
system_packages
=
self
.
_resolve_installed_packages
(
)
        
result
=
ExternalSitePackageValidationResult
(
)
        
for
pkg
in
requirements
.
pypi_requirements
:
            
installed_version
=
system_packages
.
get
(
pkg
.
requirement
.
name
)
            
if
not
installed_version
or
not
pkg
.
requirement
.
specifier
.
contains
(
                
installed_version
            
)
:
                
result
.
add_discrepancy
(
pkg
.
requirement
installed_version
)
            
elif
installed_version
:
                
result
.
provides_any_package
=
True
        
for
pkg
in
requirements
.
pypi_optional_requirements
:
            
installed_version
=
system_packages
.
get
(
pkg
.
requirement
.
name
)
            
if
installed_version
and
not
pkg
.
requirement
.
specifier
.
contains
(
                
installed_version
            
)
:
                
result
.
add_discrepancy
(
pkg
.
requirement
installed_version
)
            
elif
installed_version
:
                
result
.
provides_any_package
=
True
        
if
not
result
.
has_all_packages
:
            
print
(
result
.
report
(
)
)
            
raise
Exception
(
                
f
'
The
Python
packages
associated
with
"
{
self
.
python_path
}
"
aren
\
'
t
'
                
f
'
compatible
with
the
"
{
virtualenv_name
}
"
virtualenv
'
            
)
        
return
result
.
provides_any_package
    
functools
.
lru_cache
(
maxsize
=
None
)
    
def
_resolve_installed_packages
(
self
)
:
        
pip_json
=
subprocess
.
check_output
(
            
[
                
self
.
python_path
                
"
-
m
"
                
"
pip
"
                
"
list
"
                
"
-
-
format
"
                
"
json
"
                
"
-
-
disable
-
pip
-
version
-
check
"
            
]
            
universal_newlines
=
True
        
)
        
installed_packages
=
json
.
loads
(
pip_json
)
        
return
{
package
[
"
name
"
]
:
package
[
"
version
"
]
for
package
in
installed_packages
}
functools
.
lru_cache
(
maxsize
=
None
)
def
resolve_requirements
(
topsrcdir
virtualenv_name
)
:
    
manifest_path
=
os
.
path
.
join
(
        
topsrcdir
"
build
"
f
"
{
virtualenv_name
}
_virtualenv_packages
.
txt
"
    
)
    
if
not
os
.
path
.
exists
(
manifest_path
)
:
        
raise
Exception
(
            
f
'
The
current
command
is
using
the
"
{
virtualenv_name
}
"
'
            
"
virtualenv
.
However
that
virtualenv
is
missing
its
associated
"
            
f
'
requirements
definition
file
at
"
{
manifest_path
}
"
.
'
        
)
    
thunderbird_dir
=
os
.
path
.
join
(
topsrcdir
"
comm
"
)
    
is_thunderbird
=
os
.
path
.
exists
(
thunderbird_dir
)
and
bool
(
        
os
.
listdir
(
thunderbird_dir
)
    
)
    
return
MachEnvRequirements
.
from_requirements_definition
(
        
topsrcdir
        
is_thunderbird
        
virtualenv_name
in
(
"
mach
"
"
build
"
)
        
manifest_path
    
)
def
_virtualenv_py_path
(
topsrcdir
)
:
    
return
os
.
path
.
join
(
        
topsrcdir
"
third_party
"
"
python
"
"
virtualenv
"
"
virtualenv
.
py
"
    
)
def
_system_python_env_variable_present
(
)
:
    
return
any
(
        
os
.
environ
.
get
(
var
)
for
var
in
(
"
MACH_USE_SYSTEM_PYTHON
"
"
MOZ_AUTOMATION
"
)
    
)
def
_assert_pip_check
(
topsrcdir
pthfile_lines
virtualenv_name
)
:
    
"
"
"
Check
if
the
provided
pthfile
lines
have
a
package
incompatibility
    
If
there
'
s
an
incompatibility
raise
an
exception
and
allow
it
to
bubble
up
since
    
it
will
require
user
intervention
to
resolve
.
    
"
"
"
    
if
os
.
environ
.
get
(
        
f
"
MACH_SYSTEM_ASSERTED_COMPATIBLE_WITH_
{
virtualenv_name
.
upper
(
)
}
_SITE
"
None
    
)
:
        
return
    
if
(
        
virtualenv_name
=
=
"
mach
"
        
and
os
.
environ
.
get
(
"
MACH_USE_SYSTEM_PYTHON
"
)
        
and
not
os
.
environ
.
get
(
"
MOZ_AUTOMATION
"
)
    
)
:
        
print
(
            
"
Since
Mach
has
been
requested
to
use
the
system
Python
"
            
"
environment
it
will
need
to
verify
compatibility
before
"
            
"
running
the
current
command
.
This
may
take
a
couple
seconds
.
\
n
"
            
"
Note
:
you
can
avoid
this
delay
by
unsetting
the
"
            
"
MACH_USE_SYSTEM_PYTHON
environment
variable
.
"
        
)
    
with
tempfile
.
TemporaryDirectory
(
)
as
check_env_path
:
        
subprocess
.
check_call
(
            
[
                
sys
.
executable
                
_virtualenv_py_path
(
topsrcdir
)
                
"
-
-
no
-
download
"
                
check_env_path
            
]
            
stdout
=
subprocess
.
DEVNULL
        
)
        
check_env
=
PythonVirtualenv
(
check_env_path
)
        
with
open
(
            
os
.
path
.
join
(
os
.
path
.
join
(
check_env
.
site_packages_dir
(
)
)
PTH_FILENAME
)
            
"
w
"
        
)
as
f
:
            
f
.
write
(
"
\
n
"
.
join
(
pthfile_lines
)
)
        
pip
=
[
check_env
.
python_path
"
-
m
"
"
pip
"
]
        
check_result
=
subprocess
.
run
(
            
pip
+
[
"
check
"
]
            
stdout
=
subprocess
.
PIPE
            
stderr
=
subprocess
.
STDOUT
            
universal_newlines
=
True
        
)
        
if
check_result
.
returncode
:
            
print
(
check_result
.
stdout
file
=
sys
.
stderr
)
            
subprocess
.
check_call
(
pip
+
[
"
list
"
"
-
v
"
]
stdout
=
sys
.
stderr
)
            
raise
Exception
(
                
'
According
to
"
pip
check
"
the
current
Python
'
                
"
environment
has
package
-
compatibility
issues
.
"
            
)
        
os
.
environ
[
            
f
"
MACH_SYSTEM_ASSERTED_COMPATIBLE_WITH_
{
virtualenv_name
.
upper
(
)
}
_SITE
"
        
]
=
"
1
"
def
_deprioritize_venv_packages
(
site_packages_dir
)
:
    
return
(
        
"
import
sys
;
sys
.
path
=
[
p
for
p
in
sys
.
path
if
"
        
f
"
p
.
lower
(
)
!
=
{
repr
(
site_packages_dir
)
}
.
lower
(
)
]
"
        
f
"
import
sys
;
sys
.
path
.
append
(
{
repr
(
site_packages_dir
)
}
)
"
    
)
def
_create_venv_with_pthfile
(
    
topsrcdir
    
target_venv
    
pthfile_lines
    
site_packages_source
    
requirements
    
metadata
)
:
    
virtualenv_root
=
target_venv
.
prefix
    
if
os
.
path
.
exists
(
virtualenv_root
)
:
        
shutil
.
rmtree
(
virtualenv_root
)
    
os
.
makedirs
(
virtualenv_root
)
    
metadata
.
write
(
is_finalized
=
False
)
    
subprocess
.
check_call
(
        
[
            
sys
.
executable
            
_virtualenv_py_path
(
topsrcdir
)
            
"
-
-
no
-
seed
"
            
virtualenv_root
        
]
    
)
    
os
.
utime
(
target_venv
.
activate_path
None
)
    
site_packages_dir
=
target_venv
.
site_packages_dir
(
)
    
pthfile_contents
=
"
\
n
"
.
join
(
pthfile_lines
)
    
with
open
(
os
.
path
.
join
(
site_packages_dir
PTH_FILENAME
)
"
w
"
)
as
f
:
        
f
.
write
(
pthfile_contents
)
    
if
site_packages_source
=
=
SitePackagesSource
.
VENV
:
        
for
requirement
in
requirements
.
pypi_requirements
:
            
target_venv
.
pip_install
(
[
str
(
requirement
.
requirement
)
]
)
        
for
requirement
in
requirements
.
pypi_optional_requirements
:
            
try
:
                
target_venv
.
pip_install
(
[
str
(
requirement
.
requirement
)
]
)
            
except
subprocess
.
CalledProcessError
:
                
print
(
                    
f
"
Could
not
install
{
requirement
.
requirement
.
name
}
so
"
                    
f
"
{
requirement
.
repercussion
}
.
Continuing
.
"
                
)
    
os
.
utime
(
target_venv
.
activate_path
None
)
    
metadata
.
write
(
is_finalized
=
True
)
def
_is_venv_up_to_date
(
    
topsrcdir
    
target_venv
    
expected_pthfile_lines
    
requirements
    
expected_metadata
)
:
    
if
not
os
.
path
.
exists
(
target_venv
.
prefix
)
or
not
os
.
path
.
exists
(
        
target_venv
.
activate_path
    
)
:
        
return
False
    
virtualenv_package
=
os
.
path
.
join
(
        
topsrcdir
        
"
third_party
"
        
"
python
"
        
"
virtualenv
"
        
"
virtualenv
"
        
"
version
.
py
"
    
)
    
deps
=
[
virtualenv_package
]
+
requirements
.
requirements_paths
    
activate_mtime
=
os
.
path
.
getmtime
(
target_venv
.
activate_path
)
    
dep_mtime
=
max
(
os
.
path
.
getmtime
(
p
)
for
p
in
deps
)
    
if
dep_mtime
>
activate_mtime
:
        
return
False
    
try
:
        
existing_metadata
=
MozSiteMetadata
.
from_path
(
target_venv
.
prefix
)
    
except
MozSiteMetadataOutOfDateError
:
        
return
False
    
if
existing_metadata
!
=
expected_metadata
:
        
return
False
    
site_packages_dir
=
target_venv
.
site_packages_dir
(
)
    
try
:
        
with
open
(
os
.
path
.
join
(
site_packages_dir
PTH_FILENAME
)
)
as
file
:
            
current_pthfile_contents
=
file
.
read
(
)
.
strip
(
)
    
except
FileNotFoundError
:
        
return
False
    
expected_pthfile_contents
=
"
\
n
"
.
join
(
expected_pthfile_lines
)
    
if
current_pthfile_contents
!
=
expected_pthfile_contents
:
        
return
False
    
return
True
def
_mach_virtualenv_root
(
state_dir
)
:
    
return
os
.
path
.
join
(
state_dir
"
_virtualenvs
"
"
mach
"
)
