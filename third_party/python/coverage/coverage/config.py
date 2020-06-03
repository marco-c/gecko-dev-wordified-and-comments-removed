"
"
"
Config
file
for
coverage
.
py
"
"
"
import
collections
import
copy
import
os
import
os
.
path
import
re
from
coverage
import
env
from
coverage
.
backward
import
configparser
iitems
string_class
from
coverage
.
misc
import
contract
CoverageException
isolate_module
from
coverage
.
misc
import
substitute_variables
from
coverage
.
tomlconfig
import
TomlConfigParser
TomlDecodeError
os
=
isolate_module
(
os
)
class
HandyConfigParser
(
configparser
.
RawConfigParser
)
:
    
"
"
"
Our
specialization
of
ConfigParser
.
"
"
"
    
def
__init__
(
self
our_file
)
:
        
"
"
"
Create
the
HandyConfigParser
.
        
our_file
is
True
if
this
config
file
is
specifically
for
coverage
        
False
if
we
are
examining
another
config
file
(
tox
.
ini
setup
.
cfg
)
        
for
possible
settings
.
        
"
"
"
        
configparser
.
RawConfigParser
.
__init__
(
self
)
        
self
.
section_prefixes
=
[
"
coverage
:
"
]
        
if
our_file
:
            
self
.
section_prefixes
.
append
(
"
"
)
    
def
read
(
self
filenames
encoding
=
None
)
:
        
"
"
"
Read
a
file
name
as
UTF
-
8
configuration
data
.
"
"
"
        
kwargs
=
{
}
        
if
env
.
PYVERSION
>
=
(
3
2
)
:
            
kwargs
[
'
encoding
'
]
=
encoding
or
"
utf
-
8
"
        
return
configparser
.
RawConfigParser
.
read
(
self
filenames
*
*
kwargs
)
    
def
has_option
(
self
section
option
)
:
        
for
section_prefix
in
self
.
section_prefixes
:
            
real_section
=
section_prefix
+
section
            
has
=
configparser
.
RawConfigParser
.
has_option
(
self
real_section
option
)
            
if
has
:
                
return
has
        
return
False
    
def
has_section
(
self
section
)
:
        
for
section_prefix
in
self
.
section_prefixes
:
            
real_section
=
section_prefix
+
section
            
has
=
configparser
.
RawConfigParser
.
has_section
(
self
real_section
)
            
if
has
:
                
return
real_section
        
return
False
    
def
options
(
self
section
)
:
        
for
section_prefix
in
self
.
section_prefixes
:
            
real_section
=
section_prefix
+
section
            
if
configparser
.
RawConfigParser
.
has_section
(
self
real_section
)
:
                
return
configparser
.
RawConfigParser
.
options
(
self
real_section
)
        
raise
configparser
.
NoSectionError
    
def
get_section
(
self
section
)
:
        
"
"
"
Get
the
contents
of
a
section
as
a
dictionary
.
"
"
"
        
d
=
{
}
        
for
opt
in
self
.
options
(
section
)
:
            
d
[
opt
]
=
self
.
get
(
section
opt
)
        
return
d
    
def
get
(
self
section
option
*
args
*
*
kwargs
)
:
        
"
"
"
Get
a
value
replacing
environment
variables
also
.
        
The
arguments
are
the
same
as
RawConfigParser
.
get
but
in
the
found
        
value
WORD
or
{
WORD
}
are
replaced
by
the
value
of
the
        
environment
variable
WORD
.
        
Returns
the
finished
value
.
        
"
"
"
        
for
section_prefix
in
self
.
section_prefixes
:
            
real_section
=
section_prefix
+
section
            
if
configparser
.
RawConfigParser
.
has_option
(
self
real_section
option
)
:
                
break
        
else
:
            
raise
configparser
.
NoOptionError
        
v
=
configparser
.
RawConfigParser
.
get
(
self
real_section
option
*
args
*
*
kwargs
)
        
v
=
substitute_variables
(
v
os
.
environ
)
        
return
v
    
def
getlist
(
self
section
option
)
:
        
"
"
"
Read
a
list
of
strings
.
        
The
value
of
section
and
option
is
treated
as
a
comma
-
and
newline
-
        
separated
list
of
strings
.
Each
value
is
stripped
of
whitespace
.
        
Returns
the
list
of
strings
.
        
"
"
"
        
value_list
=
self
.
get
(
section
option
)
        
values
=
[
]
        
for
value_line
in
value_list
.
split
(
'
\
n
'
)
:
            
for
value
in
value_line
.
split
(
'
'
)
:
                
value
=
value
.
strip
(
)
                
if
value
:
                    
values
.
append
(
value
)
        
return
values
    
def
getregexlist
(
self
section
option
)
:
        
"
"
"
Read
a
list
of
full
-
line
regexes
.
        
The
value
of
section
and
option
is
treated
as
a
newline
-
separated
        
list
of
regexes
.
Each
value
is
stripped
of
whitespace
.
        
Returns
the
list
of
strings
.
        
"
"
"
        
line_list
=
self
.
get
(
section
option
)
        
value_list
=
[
]
        
for
value
in
line_list
.
splitlines
(
)
:
            
value
=
value
.
strip
(
)
            
try
:
                
re
.
compile
(
value
)
            
except
re
.
error
as
e
:
                
raise
CoverageException
(
                    
"
Invalid
[
%
s
]
.
%
s
value
%
r
:
%
s
"
%
(
section
option
value
e
)
                
)
            
if
value
:
                
value_list
.
append
(
value
)
        
return
value_list
DEFAULT_EXCLUDE
=
[
    
r
'
#
\
s
*
(
pragma
|
PRAGMA
)
[
:
\
s
]
?
\
s
*
(
no
|
NO
)
\
s
*
(
cover
|
COVER
)
'
]
DEFAULT_PARTIAL
=
[
    
r
'
#
\
s
*
(
pragma
|
PRAGMA
)
[
:
\
s
]
?
\
s
*
(
no
|
NO
)
\
s
*
(
branch
|
BRANCH
)
'
]
DEFAULT_PARTIAL_ALWAYS
=
[
    
'
while
(
True
|
1
|
False
|
0
)
:
'
    
'
if
(
True
|
1
|
False
|
0
)
:
'
]
class
CoverageConfig
(
object
)
:
    
"
"
"
Coverage
.
py
configuration
.
    
The
attributes
of
this
class
are
the
various
settings
that
control
the
    
operation
of
coverage
.
py
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
        
"
"
"
Initialize
the
configuration
attributes
to
their
defaults
.
"
"
"
        
self
.
attempted_config_files
=
[
]
        
self
.
config_files_read
=
[
]
        
self
.
config_file
=
None
        
self
.
_config_contents
=
None
        
self
.
_include
=
None
        
self
.
_omit
=
None
        
self
.
branch
=
False
        
self
.
command_line
=
None
        
self
.
concurrency
=
None
        
self
.
context
=
None
        
self
.
cover_pylib
=
False
        
self
.
data_file
=
"
.
coverage
"
        
self
.
debug
=
[
]
        
self
.
disable_warnings
=
[
]
        
self
.
dynamic_context
=
None
        
self
.
note
=
None
        
self
.
parallel
=
False
        
self
.
plugins
=
[
]
        
self
.
relative_files
=
False
        
self
.
run_include
=
None
        
self
.
run_omit
=
None
        
self
.
source
=
None
        
self
.
timid
=
False
        
self
.
_crash
=
None
        
self
.
exclude_list
=
DEFAULT_EXCLUDE
[
:
]
        
self
.
fail_under
=
0
.
0
        
self
.
ignore_errors
=
False
        
self
.
report_include
=
None
        
self
.
report_omit
=
None
        
self
.
partial_always_list
=
DEFAULT_PARTIAL_ALWAYS
[
:
]
        
self
.
partial_list
=
DEFAULT_PARTIAL
[
:
]
        
self
.
precision
=
0
        
self
.
report_contexts
=
None
        
self
.
show_missing
=
False
        
self
.
skip_covered
=
False
        
self
.
skip_empty
=
False
        
self
.
extra_css
=
None
        
self
.
html_dir
=
"
htmlcov
"
        
self
.
html_title
=
"
Coverage
report
"
        
self
.
show_contexts
=
False
        
self
.
xml_output
=
"
coverage
.
xml
"
        
self
.
xml_package_depth
=
99
        
self
.
json_output
=
"
coverage
.
json
"
        
self
.
json_pretty_print
=
False
        
self
.
json_show_contexts
=
False
        
self
.
paths
=
collections
.
OrderedDict
(
)
        
self
.
plugin_options
=
{
}
    
MUST_BE_LIST
=
[
        
"
debug
"
"
concurrency
"
"
plugins
"
        
"
report_omit
"
"
report_include
"
        
"
run_omit
"
"
run_include
"
    
]
    
def
from_args
(
self
*
*
kwargs
)
:
        
"
"
"
Read
config
values
from
kwargs
.
"
"
"
        
for
k
v
in
iitems
(
kwargs
)
:
            
if
v
is
not
None
:
                
if
k
in
self
.
MUST_BE_LIST
and
isinstance
(
v
string_class
)
:
                    
v
=
[
v
]
                
setattr
(
self
k
v
)
    
contract
(
filename
=
str
)
    
def
from_file
(
self
filename
our_file
)
:
        
"
"
"
Read
configuration
from
a
.
rc
file
.
        
filename
is
a
file
name
to
read
.
        
our_file
is
True
if
this
config
file
is
specifically
for
coverage
        
False
if
we
are
examining
another
config
file
(
tox
.
ini
setup
.
cfg
)
        
for
possible
settings
.
        
Returns
True
or
False
whether
the
file
could
be
read
and
it
had
some
        
coverage
.
py
settings
in
it
.
        
"
"
"
        
_
ext
=
os
.
path
.
splitext
(
filename
)
        
if
ext
=
=
'
.
toml
'
:
            
cp
=
TomlConfigParser
(
our_file
)
        
else
:
            
cp
=
HandyConfigParser
(
our_file
)
        
self
.
attempted_config_files
.
append
(
filename
)
        
try
:
            
files_read
=
cp
.
read
(
filename
)
        
except
(
configparser
.
Error
TomlDecodeError
)
as
err
:
            
raise
CoverageException
(
"
Couldn
'
t
read
config
file
%
s
:
%
s
"
%
(
filename
err
)
)
        
if
not
files_read
:
            
return
False
        
self
.
config_files_read
.
extend
(
map
(
os
.
path
.
abspath
files_read
)
)
        
any_set
=
False
        
try
:
            
for
option_spec
in
self
.
CONFIG_FILE_OPTIONS
:
                
was_set
=
self
.
_set_attr_from_config_option
(
cp
*
option_spec
)
                
if
was_set
:
                    
any_set
=
True
        
except
ValueError
as
err
:
            
raise
CoverageException
(
"
Couldn
'
t
read
config
file
%
s
:
%
s
"
%
(
filename
err
)
)
        
all_options
=
collections
.
defaultdict
(
set
)
        
for
option_spec
in
self
.
CONFIG_FILE_OPTIONS
:
            
section
option
=
option_spec
[
1
]
.
split
(
"
:
"
)
            
all_options
[
section
]
.
add
(
option
)
        
for
section
options
in
iitems
(
all_options
)
:
            
real_section
=
cp
.
has_section
(
section
)
            
if
real_section
:
                
for
unknown
in
set
(
cp
.
options
(
section
)
)
-
options
:
                    
raise
CoverageException
(
                        
"
Unrecognized
option
'
[
%
s
]
%
s
=
'
in
config
file
%
s
"
%
(
                            
real_section
unknown
filename
                        
)
                    
)
        
if
cp
.
has_section
(
'
paths
'
)
:
            
for
option
in
cp
.
options
(
'
paths
'
)
:
                
self
.
paths
[
option
]
=
cp
.
getlist
(
'
paths
'
option
)
                
any_set
=
True
        
for
plugin
in
self
.
plugins
:
            
if
cp
.
has_section
(
plugin
)
:
                
self
.
plugin_options
[
plugin
]
=
cp
.
get_section
(
plugin
)
                
any_set
=
True
        
if
our_file
:
            
used
=
True
        
else
:
            
used
=
any_set
        
if
used
:
            
self
.
config_file
=
os
.
path
.
abspath
(
filename
)
            
with
open
(
filename
)
as
f
:
                
self
.
_config_contents
=
f
.
read
(
)
        
return
used
    
def
copy
(
self
)
:
        
"
"
"
Return
a
copy
of
the
configuration
.
"
"
"
        
return
copy
.
deepcopy
(
self
)
    
CONFIG_FILE_OPTIONS
=
[
        
(
'
branch
'
'
run
:
branch
'
'
boolean
'
)
        
(
'
command_line
'
'
run
:
command_line
'
)
        
(
'
concurrency
'
'
run
:
concurrency
'
'
list
'
)
        
(
'
context
'
'
run
:
context
'
)
        
(
'
cover_pylib
'
'
run
:
cover_pylib
'
'
boolean
'
)
        
(
'
data_file
'
'
run
:
data_file
'
)
        
(
'
debug
'
'
run
:
debug
'
'
list
'
)
        
(
'
disable_warnings
'
'
run
:
disable_warnings
'
'
list
'
)
        
(
'
dynamic_context
'
'
run
:
dynamic_context
'
)
        
(
'
note
'
'
run
:
note
'
)
        
(
'
parallel
'
'
run
:
parallel
'
'
boolean
'
)
        
(
'
plugins
'
'
run
:
plugins
'
'
list
'
)
        
(
'
relative_files
'
'
run
:
relative_files
'
'
boolean
'
)
        
(
'
run_include
'
'
run
:
include
'
'
list
'
)
        
(
'
run_omit
'
'
run
:
omit
'
'
list
'
)
        
(
'
source
'
'
run
:
source
'
'
list
'
)
        
(
'
timid
'
'
run
:
timid
'
'
boolean
'
)
        
(
'
_crash
'
'
run
:
_crash
'
)
        
(
'
exclude_list
'
'
report
:
exclude_lines
'
'
regexlist
'
)
        
(
'
fail_under
'
'
report
:
fail_under
'
'
float
'
)
        
(
'
ignore_errors
'
'
report
:
ignore_errors
'
'
boolean
'
)
        
(
'
partial_always_list
'
'
report
:
partial_branches_always
'
'
regexlist
'
)
        
(
'
partial_list
'
'
report
:
partial_branches
'
'
regexlist
'
)
        
(
'
precision
'
'
report
:
precision
'
'
int
'
)
        
(
'
report_contexts
'
'
report
:
contexts
'
'
list
'
)
        
(
'
report_include
'
'
report
:
include
'
'
list
'
)
        
(
'
report_omit
'
'
report
:
omit
'
'
list
'
)
        
(
'
show_missing
'
'
report
:
show_missing
'
'
boolean
'
)
        
(
'
skip_covered
'
'
report
:
skip_covered
'
'
boolean
'
)
        
(
'
skip_empty
'
'
report
:
skip_empty
'
'
boolean
'
)
        
(
'
sort
'
'
report
:
sort
'
)
        
(
'
extra_css
'
'
html
:
extra_css
'
)
        
(
'
html_dir
'
'
html
:
directory
'
)
        
(
'
html_title
'
'
html
:
title
'
)
        
(
'
show_contexts
'
'
html
:
show_contexts
'
'
boolean
'
)
        
(
'
xml_output
'
'
xml
:
output
'
)
        
(
'
xml_package_depth
'
'
xml
:
package_depth
'
'
int
'
)
        
(
'
json_output
'
'
json
:
output
'
)
        
(
'
json_pretty_print
'
'
json
:
pretty_print
'
'
boolean
'
)
        
(
'
json_show_contexts
'
'
json
:
show_contexts
'
'
boolean
'
)
    
]
    
def
_set_attr_from_config_option
(
self
cp
attr
where
type_
=
'
'
)
:
        
"
"
"
Set
an
attribute
on
self
if
it
exists
in
the
ConfigParser
.
        
Returns
True
if
the
attribute
was
set
.
        
"
"
"
        
section
option
=
where
.
split
(
"
:
"
)
        
if
cp
.
has_option
(
section
option
)
:
            
method
=
getattr
(
cp
'
get
'
+
type_
)
            
setattr
(
self
attr
method
(
section
option
)
)
            
return
True
        
return
False
    
def
get_plugin_options
(
self
plugin
)
:
        
"
"
"
Get
a
dictionary
of
options
for
the
plugin
named
plugin
.
"
"
"
        
return
self
.
plugin_options
.
get
(
plugin
{
}
)
    
def
set_option
(
self
option_name
value
)
:
        
"
"
"
Set
an
option
in
the
configuration
.
        
option_name
is
a
colon
-
separated
string
indicating
the
section
and
        
option
name
.
For
example
the
branch
option
in
the
[
run
]
        
section
of
the
config
file
would
be
indicated
with
"
run
:
branch
"
.
        
value
is
the
new
value
for
the
option
.
        
"
"
"
        
if
option_name
=
=
"
paths
"
:
            
self
.
paths
=
value
            
return
        
for
option_spec
in
self
.
CONFIG_FILE_OPTIONS
:
            
attr
where
=
option_spec
[
:
2
]
            
if
where
=
=
option_name
:
                
setattr
(
self
attr
value
)
                
return
        
plugin_name
_
key
=
option_name
.
partition
(
"
:
"
)
        
if
key
and
plugin_name
in
self
.
plugins
:
            
self
.
plugin_options
.
setdefault
(
plugin_name
{
}
)
[
key
]
=
value
            
return
        
raise
CoverageException
(
"
No
such
option
:
%
r
"
%
option_name
)
    
def
get_option
(
self
option_name
)
:
        
"
"
"
Get
an
option
from
the
configuration
.
        
option_name
is
a
colon
-
separated
string
indicating
the
section
and
        
option
name
.
For
example
the
branch
option
in
the
[
run
]
        
section
of
the
config
file
would
be
indicated
with
"
run
:
branch
"
.
        
Returns
the
value
of
the
option
.
        
"
"
"
        
if
option_name
=
=
"
paths
"
:
            
return
self
.
paths
        
for
option_spec
in
self
.
CONFIG_FILE_OPTIONS
:
            
attr
where
=
option_spec
[
:
2
]
            
if
where
=
=
option_name
:
                
return
getattr
(
self
attr
)
        
plugin_name
_
key
=
option_name
.
partition
(
"
:
"
)
        
if
key
and
plugin_name
in
self
.
plugins
:
            
return
self
.
plugin_options
.
get
(
plugin_name
{
}
)
.
get
(
key
)
        
raise
CoverageException
(
"
No
such
option
:
%
r
"
%
option_name
)
def
config_files_to_try
(
config_file
)
:
    
"
"
"
What
config
files
should
we
try
to
read
?
    
Returns
a
list
of
tuples
:
        
(
filename
is_our_file
was_file_specified
)
    
"
"
"
    
if
config_file
=
=
"
.
coveragerc
"
:
        
config_file
=
True
    
specified_file
=
(
config_file
is
not
True
)
    
if
not
specified_file
:
        
config_file
=
os
.
environ
.
get
(
'
COVERAGE_RCFILE
'
)
        
if
config_file
:
            
specified_file
=
True
    
if
not
specified_file
:
        
config_file
=
"
.
coveragerc
"
    
files_to_try
=
[
        
(
config_file
True
specified_file
)
        
(
"
setup
.
cfg
"
False
False
)
        
(
"
tox
.
ini
"
False
False
)
        
(
"
pyproject
.
toml
"
False
False
)
    
]
    
return
files_to_try
def
read_coverage_config
(
config_file
*
*
kwargs
)
:
    
"
"
"
Read
the
coverage
.
py
configuration
.
    
Arguments
:
        
config_file
:
a
boolean
or
string
see
the
Coverage
class
for
the
            
tricky
details
.
        
all
others
:
keyword
arguments
from
the
Coverage
class
used
for
            
setting
values
in
the
configuration
.
    
Returns
:
        
config
:
            
config
is
a
CoverageConfig
object
read
from
the
appropriate
            
configuration
file
.
    
"
"
"
    
config
=
CoverageConfig
(
)
    
if
config_file
:
        
files_to_try
=
config_files_to_try
(
config_file
)
        
for
fname
our_file
specified_file
in
files_to_try
:
            
config_read
=
config
.
from_file
(
fname
our_file
=
our_file
)
            
if
config_read
:
                
break
            
if
specified_file
:
                
raise
CoverageException
(
"
Couldn
'
t
read
'
%
s
'
as
a
config
file
"
%
fname
)
    
env_data_file
=
os
.
environ
.
get
(
'
COVERAGE_FILE
'
)
    
if
env_data_file
:
        
config
.
data_file
=
env_data_file
    
debugs
=
os
.
environ
.
get
(
'
COVERAGE_DEBUG
'
)
    
if
debugs
:
        
config
.
debug
.
extend
(
d
.
strip
(
)
for
d
in
debugs
.
split
(
"
"
)
)
    
config
.
from_args
(
*
*
kwargs
)
    
config
.
data_file
=
os
.
path
.
expanduser
(
config
.
data_file
)
    
config
.
html_dir
=
os
.
path
.
expanduser
(
config
.
html_dir
)
    
config
.
xml_output
=
os
.
path
.
expanduser
(
config
.
xml_output
)
    
config
.
paths
=
collections
.
OrderedDict
(
        
(
k
[
os
.
path
.
expanduser
(
f
)
for
f
in
v
]
)
        
for
k
v
in
config
.
paths
.
items
(
)
    
)
    
return
config
