"
"
"
Requirements
file
parsing
"
"
"
from
__future__
import
absolute_import
import
optparse
import
os
import
re
import
shlex
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
filterfalse
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
.
urllib
import
parse
as
urllib_parse
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
import
cmdoptions
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
    
InstallationError
    
RequirementsFileParseError
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
req
.
constructors
import
(
    
install_req_from_editable
    
install_req_from_line
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
encoding
import
auto_decode
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
urls
import
get_url_scheme
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
(
        
Any
Callable
Iterator
List
NoReturn
Optional
Text
Tuple
    
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
import
InstallRequirement
    
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
network
.
session
import
PipSession
    
ReqFileLines
=
Iterator
[
Tuple
[
int
Text
]
]
    
LineParser
=
Callable
[
[
Text
]
Tuple
[
str
Values
]
]
__all__
=
[
'
parse_requirements
'
]
SCHEME_RE
=
re
.
compile
(
r
'
^
(
http
|
https
|
file
)
:
'
re
.
I
)
COMMENT_RE
=
re
.
compile
(
r
'
(
^
|
\
s
+
)
#
.
*
'
)
ENV_VAR_RE
=
re
.
compile
(
r
'
(
?
P
<
var
>
\
\
{
(
?
P
<
name
>
[
A
-
Z0
-
9_
]
+
)
\
}
)
'
)
SUPPORTED_OPTIONS
=
[
    
cmdoptions
.
index_url
    
cmdoptions
.
extra_index_url
    
cmdoptions
.
no_index
    
cmdoptions
.
constraints
    
cmdoptions
.
requirements
    
cmdoptions
.
editable
    
cmdoptions
.
find_links
    
cmdoptions
.
no_binary
    
cmdoptions
.
only_binary
    
cmdoptions
.
require_hashes
    
cmdoptions
.
pre
    
cmdoptions
.
trusted_host
    
cmdoptions
.
always_unzip
]
SUPPORTED_OPTIONS_REQ
=
[
    
cmdoptions
.
install_options
    
cmdoptions
.
global_options
    
cmdoptions
.
hash
]
SUPPORTED_OPTIONS_REQ_DEST
=
[
str
(
o
(
)
.
dest
)
for
o
in
SUPPORTED_OPTIONS_REQ
]
class
ParsedLine
(
object
)
:
    
def
__init__
(
        
self
        
filename
        
lineno
        
comes_from
        
args
        
opts
        
constraint
    
)
:
        
self
.
filename
=
filename
        
self
.
lineno
=
lineno
        
self
.
comes_from
=
comes_from
        
self
.
args
=
args
        
self
.
opts
=
opts
        
self
.
constraint
=
constraint
def
parse_requirements
(
    
filename
    
session
    
finder
=
None
    
comes_from
=
None
    
options
=
None
    
constraint
=
False
    
wheel_cache
=
None
    
use_pep517
=
None
)
:
    
"
"
"
Parse
a
requirements
file
and
yield
InstallRequirement
instances
.
    
:
param
filename
:
Path
or
url
of
requirements
file
.
    
:
param
session
:
PipSession
instance
.
    
:
param
finder
:
Instance
of
pip
.
index
.
PackageFinder
.
    
:
param
comes_from
:
Origin
description
of
requirements
.
    
:
param
options
:
cli
options
.
    
:
param
constraint
:
If
true
parsing
a
constraint
file
rather
than
        
requirements
file
.
    
:
param
wheel_cache
:
Instance
of
pip
.
wheel
.
WheelCache
    
:
param
use_pep517
:
Value
of
the
-
-
use
-
pep517
option
.
    
"
"
"
    
skip_requirements_regex
=
(
        
options
.
skip_requirements_regex
if
options
else
None
    
)
    
line_parser
=
get_line_parser
(
finder
)
    
parser
=
RequirementsFileParser
(
        
session
line_parser
comes_from
skip_requirements_regex
    
)
    
for
parsed_line
in
parser
.
parse
(
filename
constraint
)
:
        
req
=
handle_line
(
            
parsed_line
finder
options
session
wheel_cache
use_pep517
        
)
        
if
req
is
not
None
:
            
yield
req
def
preprocess
(
content
skip_requirements_regex
)
:
    
"
"
"
Split
filter
and
join
lines
and
return
a
line
iterator
    
:
param
content
:
the
content
of
the
requirements
file
    
:
param
options
:
cli
options
    
"
"
"
    
lines_enum
=
enumerate
(
content
.
splitlines
(
)
start
=
1
)
    
lines_enum
=
join_lines
(
lines_enum
)
    
lines_enum
=
ignore_comments
(
lines_enum
)
    
if
skip_requirements_regex
:
        
lines_enum
=
skip_regex
(
lines_enum
skip_requirements_regex
)
    
lines_enum
=
expand_env_variables
(
lines_enum
)
    
return
lines_enum
def
handle_line
(
    
line
    
finder
=
None
    
options
=
None
    
session
=
None
    
wheel_cache
=
None
    
use_pep517
=
None
)
:
    
"
"
"
Handle
a
single
parsed
requirements
line
;
This
can
result
in
    
creating
/
yielding
requirements
or
updating
the
finder
.
    
For
lines
that
contain
requirements
the
only
options
that
have
an
effect
    
are
from
SUPPORTED_OPTIONS_REQ
and
they
are
scoped
to
the
    
requirement
.
Other
options
from
SUPPORTED_OPTIONS
may
be
present
but
are
    
ignored
.
    
For
lines
that
do
not
contain
requirements
the
only
options
that
have
an
    
effect
are
from
SUPPORTED_OPTIONS
.
Options
from
SUPPORTED_OPTIONS_REQ
may
    
be
present
but
are
ignored
.
These
lines
may
contain
multiple
options
    
(
although
our
docs
imply
only
one
is
supported
)
and
all
our
parsed
and
    
affect
the
finder
.
    
"
"
"
    
line_comes_from
=
'
%
s
%
s
(
line
%
s
)
'
%
(
        
'
-
c
'
if
line
.
constraint
else
'
-
r
'
line
.
filename
line
.
lineno
    
)
    
if
line
.
args
:
        
isolated
=
options
.
isolated_mode
if
options
else
False
        
if
options
:
            
cmdoptions
.
check_install_build_global
(
options
line
.
opts
)
        
req_options
=
{
}
        
for
dest
in
SUPPORTED_OPTIONS_REQ_DEST
:
            
if
dest
in
line
.
opts
.
__dict__
and
line
.
opts
.
__dict__
[
dest
]
:
                
req_options
[
dest
]
=
line
.
opts
.
__dict__
[
dest
]
        
line_source
=
'
line
{
}
of
{
}
'
.
format
(
line
.
lineno
line
.
filename
)
        
return
install_req_from_line
(
            
line
.
args
            
comes_from
=
line_comes_from
            
use_pep517
=
use_pep517
            
isolated
=
isolated
            
options
=
req_options
            
wheel_cache
=
wheel_cache
            
constraint
=
line
.
constraint
            
line_source
=
line_source
        
)
    
elif
line
.
opts
.
editables
:
        
isolated
=
options
.
isolated_mode
if
options
else
False
        
return
install_req_from_editable
(
            
line
.
opts
.
editables
[
0
]
comes_from
=
line_comes_from
            
use_pep517
=
use_pep517
            
constraint
=
line
.
constraint
isolated
=
isolated
            
wheel_cache
=
wheel_cache
        
)
    
elif
line
.
opts
.
require_hashes
:
        
options
.
require_hashes
=
line
.
opts
.
require_hashes
    
elif
finder
:
        
find_links
=
finder
.
find_links
        
index_urls
=
finder
.
index_urls
        
if
line
.
opts
.
index_url
:
            
index_urls
=
[
line
.
opts
.
index_url
]
        
if
line
.
opts
.
no_index
is
True
:
            
index_urls
=
[
]
        
if
line
.
opts
.
extra_index_urls
:
            
index_urls
.
extend
(
line
.
opts
.
extra_index_urls
)
        
if
line
.
opts
.
find_links
:
            
value
=
line
.
opts
.
find_links
[
0
]
            
req_dir
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
abspath
(
line
.
filename
)
)
            
relative_to_reqs_file
=
os
.
path
.
join
(
req_dir
value
)
            
if
os
.
path
.
exists
(
relative_to_reqs_file
)
:
                
value
=
relative_to_reqs_file
            
find_links
.
append
(
value
)
        
search_scope
=
SearchScope
(
            
find_links
=
find_links
            
index_urls
=
index_urls
        
)
        
finder
.
search_scope
=
search_scope
        
if
line
.
opts
.
pre
:
            
finder
.
set_allow_all_prereleases
(
)
        
if
session
:
            
for
host
in
line
.
opts
.
trusted_hosts
or
[
]
:
                
source
=
'
line
{
}
of
{
}
'
.
format
(
line
.
lineno
line
.
filename
)
                
session
.
add_trusted_host
(
host
source
=
source
)
    
return
None
class
RequirementsFileParser
(
object
)
:
    
def
__init__
(
        
self
        
session
        
line_parser
        
comes_from
        
skip_requirements_regex
    
)
:
        
self
.
_session
=
session
        
self
.
_line_parser
=
line_parser
        
self
.
_comes_from
=
comes_from
        
self
.
_skip_requirements_regex
=
skip_requirements_regex
    
def
parse
(
self
filename
constraint
)
:
        
"
"
"
Parse
a
given
file
yielding
parsed
lines
.
        
"
"
"
        
for
line
in
self
.
_parse_and_recurse
(
filename
constraint
)
:
            
yield
line
    
def
_parse_and_recurse
(
self
filename
constraint
)
:
        
for
line
in
self
.
_parse_file
(
filename
constraint
)
:
            
if
(
                
not
line
.
args
and
                
not
line
.
opts
.
editables
and
                
(
line
.
opts
.
requirements
or
line
.
opts
.
constraints
)
            
)
:
                
if
line
.
opts
.
requirements
:
                    
req_path
=
line
.
opts
.
requirements
[
0
]
                    
nested_constraint
=
False
                
else
:
                    
req_path
=
line
.
opts
.
constraints
[
0
]
                    
nested_constraint
=
True
                
if
SCHEME_RE
.
search
(
filename
)
:
                    
req_path
=
urllib_parse
.
urljoin
(
filename
req_path
)
                
elif
not
SCHEME_RE
.
search
(
req_path
)
:
                    
req_path
=
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
dirname
(
filename
)
req_path
                    
)
                
for
inner_line
in
self
.
_parse_and_recurse
(
                    
req_path
nested_constraint
                
)
:
                    
yield
inner_line
            
else
:
                
yield
line
    
def
_parse_file
(
self
filename
constraint
)
:
        
_
content
=
get_file_content
(
            
filename
self
.
_session
comes_from
=
self
.
_comes_from
        
)
        
lines_enum
=
preprocess
(
content
self
.
_skip_requirements_regex
)
        
for
line_number
line
in
lines_enum
:
            
try
:
                
args_str
opts
=
self
.
_line_parser
(
line
)
            
except
OptionParsingError
as
e
:
                
msg
=
'
Invalid
requirement
:
%
s
\
n
%
s
'
%
(
line
e
.
msg
)
                
raise
RequirementsFileParseError
(
msg
)
            
yield
ParsedLine
(
                
filename
                
line_number
                
self
.
_comes_from
                
args_str
                
opts
                
constraint
            
)
def
get_line_parser
(
finder
)
:
    
def
parse_line
(
line
)
:
        
parser
=
build_parser
(
)
        
defaults
=
parser
.
get_default_values
(
)
        
defaults
.
index_url
=
None
        
if
finder
:
            
defaults
.
format_control
=
finder
.
format_control
        
args_str
options_str
=
break_args_options
(
line
)
        
if
sys
.
version_info
<
(
2
7
3
)
:
            
options_str
=
options_str
.
encode
(
'
utf8
'
)
        
opts
_
=
parser
.
parse_args
(
            
shlex
.
split
(
options_str
)
defaults
)
        
return
args_str
opts
    
return
parse_line
def
break_args_options
(
line
)
:
    
"
"
"
Break
up
the
line
into
an
args
and
options
string
.
We
only
want
to
shlex
    
(
and
then
optparse
)
the
options
not
the
args
.
args
can
contain
markers
    
which
are
corrupted
by
shlex
.
    
"
"
"
    
tokens
=
line
.
split
(
'
'
)
    
args
=
[
]
    
options
=
tokens
[
:
]
    
for
token
in
tokens
:
        
if
token
.
startswith
(
'
-
'
)
or
token
.
startswith
(
'
-
-
'
)
:
            
break
        
else
:
            
args
.
append
(
token
)
            
options
.
pop
(
0
)
    
return
'
'
.
join
(
args
)
'
'
.
join
(
options
)
class
OptionParsingError
(
Exception
)
:
    
def
__init__
(
self
msg
)
:
        
self
.
msg
=
msg
def
build_parser
(
)
:
    
"
"
"
    
Return
a
parser
for
parsing
requirement
lines
    
"
"
"
    
parser
=
optparse
.
OptionParser
(
add_help_option
=
False
)
    
option_factories
=
SUPPORTED_OPTIONS
+
SUPPORTED_OPTIONS_REQ
    
for
option_factory
in
option_factories
:
        
option
=
option_factory
(
)
        
parser
.
add_option
(
option
)
    
def
parser_exit
(
self
msg
)
:
        
raise
OptionParsingError
(
msg
)
    
parser
.
exit
=
parser_exit
    
return
parser
def
join_lines
(
lines_enum
)
:
    
"
"
"
Joins
a
line
ending
in
'
\
'
with
the
previous
line
(
except
when
following
    
comments
)
.
The
joined
line
takes
on
the
index
of
the
first
line
.
    
"
"
"
    
primary_line_number
=
None
    
new_line
=
[
]
    
for
line_number
line
in
lines_enum
:
        
if
not
line
.
endswith
(
'
\
\
'
)
or
COMMENT_RE
.
match
(
line
)
:
            
if
COMMENT_RE
.
match
(
line
)
:
                
line
=
'
'
+
line
            
if
new_line
:
                
new_line
.
append
(
line
)
                
yield
primary_line_number
'
'
.
join
(
new_line
)
                
new_line
=
[
]
            
else
:
                
yield
line_number
line
        
else
:
            
if
not
new_line
:
                
primary_line_number
=
line_number
            
new_line
.
append
(
line
.
strip
(
'
\
\
'
)
)
    
if
new_line
:
        
yield
primary_line_number
'
'
.
join
(
new_line
)
def
ignore_comments
(
lines_enum
)
:
    
"
"
"
    
Strips
comments
and
filter
empty
lines
.
    
"
"
"
    
for
line_number
line
in
lines_enum
:
        
line
=
COMMENT_RE
.
sub
(
'
'
line
)
        
line
=
line
.
strip
(
)
        
if
line
:
            
yield
line_number
line
def
skip_regex
(
lines_enum
pattern
)
:
    
"
"
"
    
Skip
lines
that
match
the
provided
pattern
    
Note
:
the
regex
pattern
is
only
built
once
    
"
"
"
    
matcher
=
re
.
compile
(
pattern
)
    
lines_enum
=
filterfalse
(
lambda
e
:
matcher
.
search
(
e
[
1
]
)
lines_enum
)
    
return
lines_enum
def
expand_env_variables
(
lines_enum
)
:
    
"
"
"
Replace
all
environment
variables
that
can
be
retrieved
via
os
.
getenv
.
    
The
only
allowed
format
for
environment
variables
defined
in
the
    
requirement
file
is
{
MY_VARIABLE_1
}
to
ensure
two
things
:
    
1
.
Strings
that
contain
a
aren
'
t
accidentally
(
partially
)
expanded
.
    
2
.
Ensure
consistency
across
platforms
for
requirement
files
.
    
These
points
are
the
result
of
a
discussion
on
the
github
pull
    
request
#
3514
<
https
:
/
/
github
.
com
/
pypa
/
pip
/
pull
/
3514
>
_
.
    
Valid
characters
in
variable
names
follow
the
POSIX
standard
    
<
http
:
/
/
pubs
.
opengroup
.
org
/
onlinepubs
/
9699919799
/
>
_
and
are
limited
    
to
uppercase
letter
digits
and
the
_
(
underscore
)
.
    
"
"
"
    
for
line_number
line
in
lines_enum
:
        
for
env_var
var_name
in
ENV_VAR_RE
.
findall
(
line
)
:
            
value
=
os
.
getenv
(
var_name
)
            
if
not
value
:
                
continue
            
line
=
line
.
replace
(
env_var
value
)
        
yield
line_number
line
def
get_file_content
(
url
session
comes_from
=
None
)
:
    
"
"
"
Gets
the
content
of
a
file
;
it
may
be
a
filename
file
:
URL
or
    
http
:
URL
.
Returns
(
location
content
)
.
Content
is
unicode
.
    
Respects
#
-
*
-
coding
:
declarations
on
the
retrieved
files
.
    
:
param
url
:
File
path
or
url
.
    
:
param
session
:
PipSession
instance
.
    
:
param
comes_from
:
Origin
description
of
requirements
.
    
"
"
"
    
scheme
=
get_url_scheme
(
url
)
    
if
scheme
in
[
'
http
'
'
https
'
]
:
        
resp
=
session
.
get
(
url
)
        
resp
.
raise_for_status
(
)
        
return
resp
.
url
resp
.
text
    
elif
scheme
=
=
'
file
'
:
        
if
comes_from
and
comes_from
.
startswith
(
'
http
'
)
:
            
raise
InstallationError
(
                
'
Requirements
file
%
s
references
URL
%
s
which
is
local
'
                
%
(
comes_from
url
)
)
        
path
=
url
.
split
(
'
:
'
1
)
[
1
]
        
path
=
path
.
replace
(
'
\
\
'
'
/
'
)
        
match
=
_url_slash_drive_re
.
match
(
path
)
        
if
match
:
            
path
=
match
.
group
(
1
)
+
'
:
'
+
path
.
split
(
'
|
'
1
)
[
1
]
        
path
=
urllib_parse
.
unquote
(
path
)
        
if
path
.
startswith
(
'
/
'
)
:
            
path
=
'
/
'
+
path
.
lstrip
(
'
/
'
)
        
url
=
path
    
try
:
        
with
open
(
url
'
rb
'
)
as
f
:
            
content
=
auto_decode
(
f
.
read
(
)
)
    
except
IOError
as
exc
:
        
raise
InstallationError
(
            
'
Could
not
open
requirements
file
:
%
s
'
%
str
(
exc
)
        
)
    
return
url
content
_url_slash_drive_re
=
re
.
compile
(
r
'
/
*
(
[
a
-
z
]
)
\
|
'
re
.
I
)
