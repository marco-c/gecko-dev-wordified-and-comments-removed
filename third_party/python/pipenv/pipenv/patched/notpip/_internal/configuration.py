"
"
"
Configuration
management
setup
Some
terminology
:
-
name
  
As
written
in
config
files
.
-
value
  
Value
associated
with
a
name
-
key
  
Name
combined
with
it
'
s
section
(
section
.
name
)
-
variant
  
A
single
word
describing
where
the
configuration
key
-
value
pair
came
from
"
"
"
import
locale
import
logging
import
os
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
.
six
.
moves
import
configparser
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
(
    
ConfigurationError
    
ConfigurationFileCouldNotBeLoaded
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
import
appdirs
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
compat
import
WINDOWS
expanduser
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
enum
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
typing
import
(
        
Any
Dict
Iterable
List
NewType
Optional
Tuple
    
)
    
RawConfigParser
=
configparser
.
RawConfigParser
    
Kind
=
NewType
(
"
Kind
"
str
)
logger
=
logging
.
getLogger
(
__name__
)
def
_normalize_name
(
name
)
:
    
"
"
"
Make
a
name
consistent
regardless
of
source
(
environment
or
file
)
    
"
"
"
    
name
=
name
.
lower
(
)
.
replace
(
'
_
'
'
-
'
)
    
if
name
.
startswith
(
'
-
-
'
)
:
        
name
=
name
[
2
:
]
    
return
name
def
_disassemble_key
(
name
)
:
    
if
"
.
"
not
in
name
:
        
error_message
=
(
            
"
Key
does
not
contain
dot
separated
section
and
key
.
"
            
"
Perhaps
you
wanted
to
use
'
global
.
{
}
'
instead
?
"
        
)
.
format
(
name
)
        
raise
ConfigurationError
(
error_message
)
    
return
name
.
split
(
"
.
"
1
)
kinds
=
enum
(
    
USER
=
"
user
"
    
GLOBAL
=
"
global
"
    
SITE
=
"
site
"
    
ENV
=
"
env
"
    
ENV_VAR
=
"
env
-
var
"
)
CONFIG_BASENAME
=
'
pip
.
ini
'
if
WINDOWS
else
'
pip
.
conf
'
def
get_configuration_files
(
)
:
    
global_config_files
=
[
        
os
.
path
.
join
(
path
CONFIG_BASENAME
)
        
for
path
in
appdirs
.
site_config_dirs
(
'
pip
'
)
    
]
    
site_config_file
=
os
.
path
.
join
(
sys
.
prefix
CONFIG_BASENAME
)
    
legacy_config_file
=
os
.
path
.
join
(
        
expanduser
(
'
~
'
)
        
'
pip
'
if
WINDOWS
else
'
.
pip
'
        
CONFIG_BASENAME
    
)
    
new_config_file
=
os
.
path
.
join
(
        
appdirs
.
user_config_dir
(
"
pip
"
)
CONFIG_BASENAME
    
)
    
return
{
        
kinds
.
GLOBAL
:
global_config_files
        
kinds
.
SITE
:
[
site_config_file
]
        
kinds
.
USER
:
[
legacy_config_file
new_config_file
]
    
}
class
Configuration
(
object
)
:
    
"
"
"
Handles
management
of
configuration
.
    
Provides
an
interface
to
accessing
and
managing
configuration
files
.
    
This
class
converts
provides
an
API
that
takes
"
section
.
key
-
name
"
style
    
keys
and
stores
the
value
associated
with
it
as
"
key
-
name
"
under
the
    
section
"
section
"
.
    
This
allows
for
a
clean
interface
wherein
the
both
the
section
and
the
    
key
-
name
are
preserved
in
an
easy
to
manage
form
in
the
configuration
files
    
and
the
data
stored
is
also
nice
.
    
"
"
"
    
def
__init__
(
self
isolated
load_only
=
None
)
:
        
super
(
Configuration
self
)
.
__init__
(
)
        
_valid_load_only
=
[
kinds
.
USER
kinds
.
GLOBAL
kinds
.
SITE
None
]
        
if
load_only
not
in
_valid_load_only
:
            
raise
ConfigurationError
(
                
"
Got
invalid
value
for
load_only
-
should
be
one
of
{
}
"
.
format
(
                    
"
"
.
join
(
map
(
repr
_valid_load_only
[
:
-
1
]
)
)
                
)
            
)
        
self
.
isolated
=
isolated
        
self
.
load_only
=
load_only
        
self
.
_override_order
=
[
            
kinds
.
GLOBAL
kinds
.
USER
kinds
.
SITE
kinds
.
ENV
kinds
.
ENV_VAR
        
]
        
self
.
_ignore_env_names
=
[
"
version
"
"
help
"
]
        
self
.
_parsers
=
{
            
variant
:
[
]
for
variant
in
self
.
_override_order
        
}
        
self
.
_config
=
{
            
variant
:
{
}
for
variant
in
self
.
_override_order
        
}
        
self
.
_modified_parsers
=
[
]
    
def
load
(
self
)
:
        
"
"
"
Loads
configuration
from
configuration
files
and
environment
        
"
"
"
        
self
.
_load_config_files
(
)
        
if
not
self
.
isolated
:
            
self
.
_load_environment_vars
(
)
    
def
get_file_to_edit
(
self
)
:
        
"
"
"
Returns
the
file
with
highest
priority
in
configuration
        
"
"
"
        
assert
self
.
load_only
is
not
None
\
            
"
Need
to
be
specified
a
file
to
be
editing
"
        
try
:
            
return
self
.
_get_parser_to_modify
(
)
[
0
]
        
except
IndexError
:
            
return
None
    
def
items
(
self
)
:
        
"
"
"
Returns
key
-
value
pairs
like
dict
.
items
(
)
representing
the
loaded
        
configuration
        
"
"
"
        
return
self
.
_dictionary
.
items
(
)
    
def
get_value
(
self
key
)
:
        
"
"
"
Get
a
value
from
the
configuration
.
        
"
"
"
        
try
:
            
return
self
.
_dictionary
[
key
]
        
except
KeyError
:
            
raise
ConfigurationError
(
"
No
such
key
-
{
}
"
.
format
(
key
)
)
    
def
set_value
(
self
key
value
)
:
        
"
"
"
Modify
a
value
in
the
configuration
.
        
"
"
"
        
self
.
_ensure_have_load_only
(
)
        
fname
parser
=
self
.
_get_parser_to_modify
(
)
        
if
parser
is
not
None
:
            
section
name
=
_disassemble_key
(
key
)
            
if
not
parser
.
has_section
(
section
)
:
                
parser
.
add_section
(
section
)
            
parser
.
set
(
section
name
value
)
        
self
.
_config
[
self
.
load_only
]
[
key
]
=
value
        
self
.
_mark_as_modified
(
fname
parser
)
    
def
unset_value
(
self
key
)
:
        
"
"
"
Unset
a
value
in
the
configuration
.
        
"
"
"
        
self
.
_ensure_have_load_only
(
)
        
if
key
not
in
self
.
_config
[
self
.
load_only
]
:
            
raise
ConfigurationError
(
"
No
such
key
-
{
}
"
.
format
(
key
)
)
        
fname
parser
=
self
.
_get_parser_to_modify
(
)
        
if
parser
is
not
None
:
            
section
name
=
_disassemble_key
(
key
)
            
modified_something
=
False
            
if
parser
.
has_section
(
section
)
:
                
modified_something
=
parser
.
remove_option
(
section
name
)
            
if
modified_something
:
                
section_iter
=
iter
(
parser
.
items
(
section
)
)
                
try
:
                    
val
=
next
(
section_iter
)
                
except
StopIteration
:
                    
val
=
None
                
if
val
is
None
:
                    
parser
.
remove_section
(
section
)
                
self
.
_mark_as_modified
(
fname
parser
)
            
else
:
                
raise
ConfigurationError
(
                    
"
Fatal
Internal
error
[
id
=
1
]
.
Please
report
as
a
bug
.
"
                
)
        
del
self
.
_config
[
self
.
load_only
]
[
key
]
    
def
save
(
self
)
:
        
"
"
"
Save
the
current
in
-
memory
state
.
        
"
"
"
        
self
.
_ensure_have_load_only
(
)
        
for
fname
parser
in
self
.
_modified_parsers
:
            
logger
.
info
(
"
Writing
to
%
s
"
fname
)
            
ensure_dir
(
os
.
path
.
dirname
(
fname
)
)
            
with
open
(
fname
"
w
"
)
as
f
:
                
parser
.
write
(
f
)
    
def
_ensure_have_load_only
(
self
)
:
        
if
self
.
load_only
is
None
:
            
raise
ConfigurationError
(
"
Needed
a
specific
file
to
be
modifying
.
"
)
        
logger
.
debug
(
"
Will
be
working
with
%
s
variant
only
"
self
.
load_only
)
    
property
    
def
_dictionary
(
self
)
:
        
"
"
"
A
dictionary
representing
the
loaded
configuration
.
        
"
"
"
        
retval
=
{
}
        
for
variant
in
self
.
_override_order
:
            
retval
.
update
(
self
.
_config
[
variant
]
)
        
return
retval
    
def
_load_config_files
(
self
)
:
        
"
"
"
Loads
configuration
from
configuration
files
        
"
"
"
        
config_files
=
dict
(
self
.
_iter_config_files
(
)
)
        
if
config_files
[
kinds
.
ENV
]
[
0
:
1
]
=
=
[
os
.
devnull
]
:
            
logger
.
debug
(
                
"
Skipping
loading
configuration
files
due
to
"
                
"
environment
'
s
PIP_CONFIG_FILE
being
os
.
devnull
"
            
)
            
return
        
for
variant
files
in
config_files
.
items
(
)
:
            
for
fname
in
files
:
                
if
self
.
load_only
is
not
None
and
variant
!
=
self
.
load_only
:
                    
logger
.
debug
(
                        
"
Skipping
file
'
%
s
'
(
variant
:
%
s
)
"
fname
variant
                    
)
                    
continue
                
parser
=
self
.
_load_file
(
variant
fname
)
                
self
.
_parsers
[
variant
]
.
append
(
(
fname
parser
)
)
    
def
_load_file
(
self
variant
fname
)
:
        
logger
.
debug
(
"
For
variant
'
%
s
'
will
try
loading
'
%
s
'
"
variant
fname
)
        
parser
=
self
.
_construct_parser
(
fname
)
        
for
section
in
parser
.
sections
(
)
:
            
items
=
parser
.
items
(
section
)
            
self
.
_config
[
variant
]
.
update
(
self
.
_normalized_keys
(
section
items
)
)
        
return
parser
    
def
_construct_parser
(
self
fname
)
:
        
parser
=
configparser
.
RawConfigParser
(
)
        
if
os
.
path
.
exists
(
fname
)
:
            
try
:
                
parser
.
read
(
fname
)
            
except
UnicodeDecodeError
:
                
raise
ConfigurationFileCouldNotBeLoaded
(
                    
reason
=
"
contains
invalid
{
}
characters
"
.
format
(
                        
locale
.
getpreferredencoding
(
False
)
                    
)
                    
fname
=
fname
                
)
            
except
configparser
.
Error
as
error
:
                
raise
ConfigurationFileCouldNotBeLoaded
(
error
=
error
)
        
return
parser
    
def
_load_environment_vars
(
self
)
:
        
"
"
"
Loads
configuration
from
environment
variables
        
"
"
"
        
self
.
_config
[
kinds
.
ENV_VAR
]
.
update
(
            
self
.
_normalized_keys
(
"
:
env
:
"
self
.
_get_environ_vars
(
)
)
        
)
    
def
_normalized_keys
(
self
section
items
)
:
        
"
"
"
Normalizes
items
to
construct
a
dictionary
with
normalized
keys
.
        
This
routine
is
where
the
names
become
keys
and
are
made
the
same
        
regardless
of
source
-
configuration
files
or
environment
.
        
"
"
"
        
normalized
=
{
}
        
for
name
val
in
items
:
            
key
=
section
+
"
.
"
+
_normalize_name
(
name
)
            
normalized
[
key
]
=
val
        
return
normalized
    
def
_get_environ_vars
(
self
)
:
        
"
"
"
Returns
a
generator
with
all
environmental
vars
with
prefix
PIP_
"
"
"
        
for
key
val
in
os
.
environ
.
items
(
)
:
            
should_be_yielded
=
(
                
key
.
startswith
(
"
PIP_
"
)
and
                
key
[
4
:
]
.
lower
(
)
not
in
self
.
_ignore_env_names
            
)
            
if
should_be_yielded
:
                
yield
key
[
4
:
]
.
lower
(
)
val
    
def
_iter_config_files
(
self
)
:
        
"
"
"
Yields
variant
and
configuration
files
associated
with
it
.
        
This
should
be
treated
like
items
of
a
dictionary
.
        
"
"
"
        
config_file
=
os
.
environ
.
get
(
'
PIP_CONFIG_FILE
'
None
)
        
if
config_file
is
not
None
:
            
yield
kinds
.
ENV
[
config_file
]
        
else
:
            
yield
kinds
.
ENV
[
]
        
config_files
=
get_configuration_files
(
)
        
yield
kinds
.
GLOBAL
config_files
[
kinds
.
GLOBAL
]
        
should_load_user_config
=
not
self
.
isolated
and
not
(
            
config_file
and
os
.
path
.
exists
(
config_file
)
        
)
        
if
should_load_user_config
:
            
yield
kinds
.
USER
config_files
[
kinds
.
USER
]
        
yield
kinds
.
SITE
config_files
[
kinds
.
SITE
]
    
def
_get_parser_to_modify
(
self
)
:
        
parsers
=
self
.
_parsers
[
self
.
load_only
]
        
if
not
parsers
:
            
raise
ConfigurationError
(
                
"
Fatal
Internal
error
[
id
=
2
]
.
Please
report
as
a
bug
.
"
            
)
        
return
parsers
[
-
1
]
    
def
_mark_as_modified
(
self
fname
parser
)
:
        
file_parser_tuple
=
(
fname
parser
)
        
if
file_parser_tuple
not
in
self
.
_modified_parsers
:
            
self
.
_modified_parsers
.
append
(
file_parser_tuple
)
