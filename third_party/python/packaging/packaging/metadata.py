from
__future__
import
annotations
import
email
.
feedparser
import
email
.
header
import
email
.
message
import
email
.
parser
import
email
.
policy
import
pathlib
import
sys
import
typing
from
typing
import
(
    
Any
    
Callable
    
Generic
    
Literal
    
TypedDict
    
cast
)
from
.
import
licenses
requirements
specifiers
utils
from
.
import
version
as
version_module
from
.
licenses
import
NormalizedLicenseExpression
T
=
typing
.
TypeVar
(
"
T
"
)
if
sys
.
version_info
>
=
(
3
11
)
:
    
ExceptionGroup
=
ExceptionGroup
else
:
    
class
ExceptionGroup
(
Exception
)
:
        
"
"
"
A
minimal
implementation
of
:
external
:
exc
:
ExceptionGroup
from
Python
3
.
11
.
        
If
:
external
:
exc
:
ExceptionGroup
is
already
defined
by
Python
itself
        
that
version
is
used
instead
.
        
"
"
"
        
message
:
str
        
exceptions
:
list
[
Exception
]
        
def
__init__
(
self
message
:
str
exceptions
:
list
[
Exception
]
)
-
>
None
:
            
self
.
message
=
message
            
self
.
exceptions
=
exceptions
        
def
__repr__
(
self
)
-
>
str
:
            
return
f
"
{
self
.
__class__
.
__name__
}
(
{
self
.
message
!
r
}
{
self
.
exceptions
!
r
}
)
"
class
InvalidMetadata
(
ValueError
)
:
    
"
"
"
A
metadata
field
contains
invalid
data
.
"
"
"
    
field
:
str
    
"
"
"
The
name
of
the
field
that
contains
invalid
data
.
"
"
"
    
def
__init__
(
self
field
:
str
message
:
str
)
-
>
None
:
        
self
.
field
=
field
        
super
(
)
.
__init__
(
message
)
class
RawMetadata
(
TypedDict
total
=
False
)
:
    
"
"
"
A
dictionary
of
raw
core
metadata
.
    
Each
field
in
core
metadata
maps
to
a
key
of
this
dictionary
(
when
data
is
    
provided
)
.
The
key
is
lower
-
case
and
underscores
are
used
instead
of
dashes
    
compared
to
the
equivalent
core
metadata
field
.
Any
core
metadata
field
that
    
can
be
specified
multiple
times
or
can
hold
multiple
values
in
a
single
    
field
have
a
key
with
a
plural
name
.
See
:
class
:
Metadata
whose
attributes
    
match
the
keys
of
this
dictionary
.
    
Core
metadata
fields
that
can
be
specified
multiple
times
are
stored
as
a
    
list
or
dict
depending
on
which
is
appropriate
for
the
field
.
Any
fields
    
which
hold
multiple
values
in
a
single
field
are
stored
as
a
list
.
    
"
"
"
    
metadata_version
:
str
    
name
:
str
    
version
:
str
    
platforms
:
list
[
str
]
    
summary
:
str
    
description
:
str
    
keywords
:
list
[
str
]
    
home_page
:
str
    
author
:
str
    
author_email
:
str
    
license
:
str
    
supported_platforms
:
list
[
str
]
    
download_url
:
str
    
classifiers
:
list
[
str
]
    
requires
:
list
[
str
]
    
provides
:
list
[
str
]
    
obsoletes
:
list
[
str
]
    
maintainer
:
str
    
maintainer_email
:
str
    
requires_dist
:
list
[
str
]
    
provides_dist
:
list
[
str
]
    
obsoletes_dist
:
list
[
str
]
    
requires_python
:
str
    
requires_external
:
list
[
str
]
    
project_urls
:
dict
[
str
str
]
    
description_content_type
:
str
    
provides_extra
:
list
[
str
]
    
dynamic
:
list
[
str
]
    
license_expression
:
str
    
license_files
:
list
[
str
]
_STRING_FIELDS
=
{
    
"
author
"
    
"
author_email
"
    
"
description
"
    
"
description_content_type
"
    
"
download_url
"
    
"
home_page
"
    
"
license
"
    
"
license_expression
"
    
"
maintainer
"
    
"
maintainer_email
"
    
"
metadata_version
"
    
"
name
"
    
"
requires_python
"
    
"
summary
"
    
"
version
"
}
_LIST_FIELDS
=
{
    
"
classifiers
"
    
"
dynamic
"
    
"
license_files
"
    
"
obsoletes
"
    
"
obsoletes_dist
"
    
"
platforms
"
    
"
provides
"
    
"
provides_dist
"
    
"
provides_extra
"
    
"
requires
"
    
"
requires_dist
"
    
"
requires_external
"
    
"
supported_platforms
"
}
_DICT_FIELDS
=
{
    
"
project_urls
"
}
def
_parse_keywords
(
data
:
str
)
-
>
list
[
str
]
:
    
"
"
"
Split
a
string
of
comma
-
separated
keywords
into
a
list
of
keywords
.
"
"
"
    
return
[
k
.
strip
(
)
for
k
in
data
.
split
(
"
"
)
]
def
_parse_project_urls
(
data
:
list
[
str
]
)
-
>
dict
[
str
str
]
:
    
"
"
"
Parse
a
list
of
label
/
URL
string
pairings
separated
by
a
comma
.
"
"
"
    
urls
=
{
}
    
for
pair
in
data
:
        
parts
=
[
p
.
strip
(
)
for
p
in
pair
.
split
(
"
"
1
)
]
        
parts
.
extend
(
[
"
"
]
*
(
max
(
0
2
-
len
(
parts
)
)
)
)
        
label
url
=
parts
        
if
label
in
urls
:
            
raise
KeyError
(
"
duplicate
labels
in
project
urls
"
)
        
urls
[
label
]
=
url
    
return
urls
def
_get_payload
(
msg
:
email
.
message
.
Message
source
:
bytes
|
str
)
-
>
str
:
    
"
"
"
Get
the
body
of
the
message
.
"
"
"
    
if
isinstance
(
source
str
)
:
        
payload
=
msg
.
get_payload
(
)
        
assert
isinstance
(
payload
str
)
        
return
payload
    
else
:
        
bpayload
=
msg
.
get_payload
(
decode
=
True
)
        
assert
isinstance
(
bpayload
bytes
)
        
try
:
            
return
bpayload
.
decode
(
"
utf8
"
"
strict
"
)
        
except
UnicodeDecodeError
as
exc
:
            
raise
ValueError
(
"
payload
in
an
invalid
encoding
"
)
from
exc
_EMAIL_TO_RAW_MAPPING
=
{
    
"
author
"
:
"
author
"
    
"
author
-
email
"
:
"
author_email
"
    
"
classifier
"
:
"
classifiers
"
    
"
description
"
:
"
description
"
    
"
description
-
content
-
type
"
:
"
description_content_type
"
    
"
download
-
url
"
:
"
download_url
"
    
"
dynamic
"
:
"
dynamic
"
    
"
home
-
page
"
:
"
home_page
"
    
"
keywords
"
:
"
keywords
"
    
"
license
"
:
"
license
"
    
"
license
-
expression
"
:
"
license_expression
"
    
"
license
-
file
"
:
"
license_files
"
    
"
maintainer
"
:
"
maintainer
"
    
"
maintainer
-
email
"
:
"
maintainer_email
"
    
"
metadata
-
version
"
:
"
metadata_version
"
    
"
name
"
:
"
name
"
    
"
obsoletes
"
:
"
obsoletes
"
    
"
obsoletes
-
dist
"
:
"
obsoletes_dist
"
    
"
platform
"
:
"
platforms
"
    
"
project
-
url
"
:
"
project_urls
"
    
"
provides
"
:
"
provides
"
    
"
provides
-
dist
"
:
"
provides_dist
"
    
"
provides
-
extra
"
:
"
provides_extra
"
    
"
requires
"
:
"
requires
"
    
"
requires
-
dist
"
:
"
requires_dist
"
    
"
requires
-
external
"
:
"
requires_external
"
    
"
requires
-
python
"
:
"
requires_python
"
    
"
summary
"
:
"
summary
"
    
"
supported
-
platform
"
:
"
supported_platforms
"
    
"
version
"
:
"
version
"
}
_RAW_TO_EMAIL_MAPPING
=
{
raw
:
email
for
email
raw
in
_EMAIL_TO_RAW_MAPPING
.
items
(
)
}
def
parse_email
(
data
:
bytes
|
str
)
-
>
tuple
[
RawMetadata
dict
[
str
list
[
str
]
]
]
:
    
"
"
"
Parse
a
distribution
'
s
metadata
stored
as
email
headers
(
e
.
g
.
from
METADATA
)
.
    
This
function
returns
a
two
-
item
tuple
of
dicts
.
The
first
dict
is
of
    
recognized
fields
from
the
core
metadata
specification
.
Fields
that
can
be
    
parsed
and
translated
into
Python
'
s
built
-
in
types
are
converted
    
appropriately
.
All
other
fields
are
left
as
-
is
.
Fields
that
are
allowed
to
    
appear
multiple
times
are
stored
as
lists
.
    
The
second
dict
contains
all
other
fields
from
the
metadata
.
This
includes
    
any
unrecognized
fields
.
It
also
includes
any
fields
which
are
expected
to
    
be
parsed
into
a
built
-
in
type
but
were
not
formatted
appropriately
.
Finally
    
any
fields
that
are
expected
to
appear
only
once
but
are
repeated
are
    
included
in
this
dict
.
    
"
"
"
    
raw
:
dict
[
str
str
|
list
[
str
]
|
dict
[
str
str
]
]
=
{
}
    
unparsed
:
dict
[
str
list
[
str
]
]
=
{
}
    
if
isinstance
(
data
str
)
:
        
parsed
=
email
.
parser
.
Parser
(
policy
=
email
.
policy
.
compat32
)
.
parsestr
(
data
)
    
else
:
        
parsed
=
email
.
parser
.
BytesParser
(
policy
=
email
.
policy
.
compat32
)
.
parsebytes
(
data
)
    
for
name
in
frozenset
(
parsed
.
keys
(
)
)
:
        
name
=
name
.
lower
(
)
        
headers
=
parsed
.
get_all
(
name
)
or
[
]
        
value
=
[
]
        
valid_encoding
=
True
        
for
h
in
headers
:
            
assert
isinstance
(
h
(
email
.
header
.
Header
str
)
)
            
if
isinstance
(
h
email
.
header
.
Header
)
:
                
chunks
:
list
[
tuple
[
bytes
str
|
None
]
]
=
[
]
                
for
bin
encoding
in
email
.
header
.
decode_header
(
h
)
:
                    
try
:
                        
bin
.
decode
(
"
utf8
"
"
strict
"
)
                    
except
UnicodeDecodeError
:
                        
encoding
=
"
latin1
"
                        
valid_encoding
=
False
                    
else
:
                        
encoding
=
"
utf8
"
                    
chunks
.
append
(
(
bin
encoding
)
)
                
value
.
append
(
str
(
email
.
header
.
make_header
(
chunks
)
)
)
            
else
:
                
value
.
append
(
h
)
        
if
not
valid_encoding
:
            
unparsed
[
name
]
=
value
            
continue
        
raw_name
=
_EMAIL_TO_RAW_MAPPING
.
get
(
name
)
        
if
raw_name
is
None
:
            
unparsed
[
name
]
=
value
            
continue
        
if
raw_name
in
_STRING_FIELDS
and
len
(
value
)
=
=
1
:
            
raw
[
raw_name
]
=
value
[
0
]
        
elif
raw_name
in
_LIST_FIELDS
:
            
raw
[
raw_name
]
=
value
        
elif
raw_name
=
=
"
keywords
"
and
len
(
value
)
=
=
1
:
            
raw
[
raw_name
]
=
_parse_keywords
(
value
[
0
]
)
        
elif
raw_name
=
=
"
project_urls
"
:
            
try
:
                
raw
[
raw_name
]
=
_parse_project_urls
(
value
)
            
except
KeyError
:
                
unparsed
[
name
]
=
value
        
else
:
            
unparsed
[
name
]
=
value
    
try
:
        
payload
=
_get_payload
(
parsed
data
)
    
except
ValueError
:
        
unparsed
.
setdefault
(
"
description
"
[
]
)
.
append
(
            
parsed
.
get_payload
(
decode
=
isinstance
(
data
bytes
)
)
        
)
    
else
:
        
if
payload
:
            
if
"
description
"
in
raw
:
                
description_header
=
cast
(
str
raw
.
pop
(
"
description
"
)
)
                
unparsed
.
setdefault
(
"
description
"
[
]
)
.
extend
(
                    
[
description_header
payload
]
                
)
            
elif
"
description
"
in
unparsed
:
                
unparsed
[
"
description
"
]
.
append
(
payload
)
            
else
:
                
raw
[
"
description
"
]
=
payload
    
return
cast
(
RawMetadata
raw
)
unparsed
_NOT_FOUND
=
object
(
)
_VALID_METADATA_VERSIONS
=
[
"
1
.
0
"
"
1
.
1
"
"
1
.
2
"
"
2
.
1
"
"
2
.
2
"
"
2
.
3
"
"
2
.
4
"
]
_MetadataVersion
=
Literal
[
"
1
.
0
"
"
1
.
1
"
"
1
.
2
"
"
2
.
1
"
"
2
.
2
"
"
2
.
3
"
"
2
.
4
"
]
_REQUIRED_ATTRS
=
frozenset
(
[
"
metadata_version
"
"
name
"
"
version
"
]
)
class
_Validator
(
Generic
[
T
]
)
:
    
"
"
"
Validate
a
metadata
field
.
    
All
_process_
*
(
)
methods
correspond
to
a
core
metadata
field
.
The
method
is
    
called
with
the
field
'
s
raw
value
.
If
the
raw
value
is
valid
it
is
returned
    
in
its
"
enriched
"
form
(
e
.
g
.
version
.
Version
for
the
Version
field
)
.
    
If
the
raw
value
is
invalid
:
exc
:
InvalidMetadata
is
raised
(
with
a
cause
    
as
appropriate
)
.
    
"
"
"
    
name
:
str
    
raw_name
:
str
    
added
:
_MetadataVersion
    
def
__init__
(
        
self
        
*
        
added
:
_MetadataVersion
=
"
1
.
0
"
    
)
-
>
None
:
        
self
.
added
=
added
    
def
__set_name__
(
self
_owner
:
Metadata
name
:
str
)
-
>
None
:
        
self
.
name
=
name
        
self
.
raw_name
=
_RAW_TO_EMAIL_MAPPING
[
name
]
    
def
__get__
(
self
instance
:
Metadata
_owner
:
type
[
Metadata
]
)
-
>
T
:
        
cache
=
instance
.
__dict__
        
value
=
instance
.
_raw
.
get
(
self
.
name
)
        
if
self
.
name
in
_REQUIRED_ATTRS
or
value
is
not
None
:
            
try
:
                
converter
:
Callable
[
[
Any
]
T
]
=
getattr
(
self
f
"
_process_
{
self
.
name
}
"
)
            
except
AttributeError
:
                
pass
            
else
:
                
value
=
converter
(
value
)
        
cache
[
self
.
name
]
=
value
        
try
:
            
del
instance
.
_raw
[
self
.
name
]
        
except
KeyError
:
            
pass
        
return
cast
(
T
value
)
    
def
_invalid_metadata
(
        
self
msg
:
str
cause
:
Exception
|
None
=
None
    
)
-
>
InvalidMetadata
:
        
exc
=
InvalidMetadata
(
            
self
.
raw_name
msg
.
format_map
(
{
"
field
"
:
repr
(
self
.
raw_name
)
}
)
        
)
        
exc
.
__cause__
=
cause
        
return
exc
    
def
_process_metadata_version
(
self
value
:
str
)
-
>
_MetadataVersion
:
        
if
value
not
in
_VALID_METADATA_VERSIONS
:
            
raise
self
.
_invalid_metadata
(
f
"
{
value
!
r
}
is
not
a
valid
metadata
version
"
)
        
return
cast
(
_MetadataVersion
value
)
    
def
_process_name
(
self
value
:
str
)
-
>
str
:
        
if
not
value
:
            
raise
self
.
_invalid_metadata
(
"
{
field
}
is
a
required
field
"
)
        
try
:
            
utils
.
canonicalize_name
(
value
validate
=
True
)
        
except
utils
.
InvalidName
as
exc
:
            
raise
self
.
_invalid_metadata
(
                
f
"
{
value
!
r
}
is
invalid
for
{
{
field
}
}
"
cause
=
exc
            
)
from
exc
        
else
:
            
return
value
    
def
_process_version
(
self
value
:
str
)
-
>
version_module
.
Version
:
        
if
not
value
:
            
raise
self
.
_invalid_metadata
(
"
{
field
}
is
a
required
field
"
)
        
try
:
            
return
version_module
.
parse
(
value
)
        
except
version_module
.
InvalidVersion
as
exc
:
            
raise
self
.
_invalid_metadata
(
                
f
"
{
value
!
r
}
is
invalid
for
{
{
field
}
}
"
cause
=
exc
            
)
from
exc
    
def
_process_summary
(
self
value
:
str
)
-
>
str
:
        
"
"
"
Check
the
field
contains
no
newlines
.
"
"
"
        
if
"
\
n
"
in
value
:
            
raise
self
.
_invalid_metadata
(
"
{
field
}
must
be
a
single
line
"
)
        
return
value
    
def
_process_description_content_type
(
self
value
:
str
)
-
>
str
:
        
content_types
=
{
"
text
/
plain
"
"
text
/
x
-
rst
"
"
text
/
markdown
"
}
        
message
=
email
.
message
.
EmailMessage
(
)
        
message
[
"
content
-
type
"
]
=
value
        
content_type
parameters
=
(
            
message
.
get_content_type
(
)
.
lower
(
)
            
message
[
"
content
-
type
"
]
.
params
        
)
        
if
content_type
not
in
content_types
or
content_type
not
in
value
.
lower
(
)
:
            
raise
self
.
_invalid_metadata
(
                
f
"
{
{
field
}
}
must
be
one
of
{
list
(
content_types
)
}
not
{
value
!
r
}
"
            
)
        
charset
=
parameters
.
get
(
"
charset
"
"
UTF
-
8
"
)
        
if
charset
!
=
"
UTF
-
8
"
:
            
raise
self
.
_invalid_metadata
(
                
f
"
{
{
field
}
}
can
only
specify
the
UTF
-
8
charset
not
{
list
(
charset
)
}
"
            
)
        
markdown_variants
=
{
"
GFM
"
"
CommonMark
"
}
        
variant
=
parameters
.
get
(
"
variant
"
"
GFM
"
)
        
if
content_type
=
=
"
text
/
markdown
"
and
variant
not
in
markdown_variants
:
            
raise
self
.
_invalid_metadata
(
                
f
"
valid
Markdown
variants
for
{
{
field
}
}
are
{
list
(
markdown_variants
)
}
"
                
f
"
not
{
variant
!
r
}
"
            
)
        
return
value
    
def
_process_dynamic
(
self
value
:
list
[
str
]
)
-
>
list
[
str
]
:
        
for
dynamic_field
in
map
(
str
.
lower
value
)
:
            
if
dynamic_field
in
{
"
name
"
"
version
"
"
metadata
-
version
"
}
:
                
raise
self
.
_invalid_metadata
(
                    
f
"
{
dynamic_field
!
r
}
is
not
allowed
as
a
dynamic
field
"
                
)
            
elif
dynamic_field
not
in
_EMAIL_TO_RAW_MAPPING
:
                
raise
self
.
_invalid_metadata
(
                    
f
"
{
dynamic_field
!
r
}
is
not
a
valid
dynamic
field
"
                
)
        
return
list
(
map
(
str
.
lower
value
)
)
    
def
_process_provides_extra
(
        
self
        
value
:
list
[
str
]
    
)
-
>
list
[
utils
.
NormalizedName
]
:
        
normalized_names
=
[
]
        
try
:
            
for
name
in
value
:
                
normalized_names
.
append
(
utils
.
canonicalize_name
(
name
validate
=
True
)
)
        
except
utils
.
InvalidName
as
exc
:
            
raise
self
.
_invalid_metadata
(
                
f
"
{
name
!
r
}
is
invalid
for
{
{
field
}
}
"
cause
=
exc
            
)
from
exc
        
else
:
            
return
normalized_names
    
def
_process_requires_python
(
self
value
:
str
)
-
>
specifiers
.
SpecifierSet
:
        
try
:
            
return
specifiers
.
SpecifierSet
(
value
)
        
except
specifiers
.
InvalidSpecifier
as
exc
:
            
raise
self
.
_invalid_metadata
(
                
f
"
{
value
!
r
}
is
invalid
for
{
{
field
}
}
"
cause
=
exc
            
)
from
exc
    
def
_process_requires_dist
(
        
self
        
value
:
list
[
str
]
    
)
-
>
list
[
requirements
.
Requirement
]
:
        
reqs
=
[
]
        
try
:
            
for
req
in
value
:
                
reqs
.
append
(
requirements
.
Requirement
(
req
)
)
        
except
requirements
.
InvalidRequirement
as
exc
:
            
raise
self
.
_invalid_metadata
(
                
f
"
{
req
!
r
}
is
invalid
for
{
{
field
}
}
"
cause
=
exc
            
)
from
exc
        
else
:
            
return
reqs
    
def
_process_license_expression
(
        
self
value
:
str
    
)
-
>
NormalizedLicenseExpression
|
None
:
        
try
:
            
return
licenses
.
canonicalize_license_expression
(
value
)
        
except
ValueError
as
exc
:
            
raise
self
.
_invalid_metadata
(
                
f
"
{
value
!
r
}
is
invalid
for
{
{
field
}
}
"
cause
=
exc
            
)
from
exc
    
def
_process_license_files
(
self
value
:
list
[
str
]
)
-
>
list
[
str
]
:
        
paths
=
[
]
        
for
path
in
value
:
            
if
"
.
.
"
in
path
:
                
raise
self
.
_invalid_metadata
(
                    
f
"
{
path
!
r
}
is
invalid
for
{
{
field
}
}
"
                    
"
parent
directory
indicators
are
not
allowed
"
                
)
            
if
"
*
"
in
path
:
                
raise
self
.
_invalid_metadata
(
                    
f
"
{
path
!
r
}
is
invalid
for
{
{
field
}
}
paths
must
be
resolved
"
                
)
            
if
(
                
pathlib
.
PurePosixPath
(
path
)
.
is_absolute
(
)
                
or
pathlib
.
PureWindowsPath
(
path
)
.
is_absolute
(
)
            
)
:
                
raise
self
.
_invalid_metadata
(
                    
f
"
{
path
!
r
}
is
invalid
for
{
{
field
}
}
paths
must
be
relative
"
                
)
            
if
pathlib
.
PureWindowsPath
(
path
)
.
as_posix
(
)
!
=
path
:
                
raise
self
.
_invalid_metadata
(
                    
f
"
{
path
!
r
}
is
invalid
for
{
{
field
}
}
paths
must
use
'
/
'
delimiter
"
                
)
            
paths
.
append
(
path
)
        
return
paths
class
Metadata
:
    
"
"
"
Representation
of
distribution
metadata
.
    
Compared
to
:
class
:
RawMetadata
this
class
provides
objects
representing
    
metadata
fields
instead
of
only
using
built
-
in
types
.
Any
invalid
metadata
    
will
cause
:
exc
:
InvalidMetadata
to
be
raised
(
with
a
    
:
py
:
attr
:
~
BaseException
.
__cause__
attribute
as
appropriate
)
.
    
"
"
"
    
_raw
:
RawMetadata
    
classmethod
    
def
from_raw
(
cls
data
:
RawMetadata
*
validate
:
bool
=
True
)
-
>
Metadata
:
        
"
"
"
Create
an
instance
from
:
class
:
RawMetadata
.
        
If
*
validate
*
is
true
all
metadata
will
be
validated
.
All
exceptions
        
related
to
validation
will
be
gathered
and
raised
as
an
:
class
:
ExceptionGroup
.
        
"
"
"
        
ins
=
cls
(
)
        
ins
.
_raw
=
data
.
copy
(
)
        
if
validate
:
            
exceptions
:
list
[
Exception
]
=
[
]
            
try
:
                
metadata_version
=
ins
.
metadata_version
                
metadata_age
=
_VALID_METADATA_VERSIONS
.
index
(
metadata_version
)
            
except
InvalidMetadata
as
metadata_version_exc
:
                
exceptions
.
append
(
metadata_version_exc
)
                
metadata_version
=
None
            
fields_to_check
=
frozenset
(
ins
.
_raw
)
|
_REQUIRED_ATTRS
            
fields_to_check
-
=
{
"
metadata_version
"
}
            
for
key
in
fields_to_check
:
                
try
:
                    
if
metadata_version
:
                        
try
:
                            
field_metadata_version
=
cls
.
__dict__
[
key
]
.
added
                        
except
KeyError
:
                            
exc
=
InvalidMetadata
(
key
f
"
unrecognized
field
:
{
key
!
r
}
"
)
                            
exceptions
.
append
(
exc
)
                            
continue
                        
field_age
=
_VALID_METADATA_VERSIONS
.
index
(
                            
field_metadata_version
                        
)
                        
if
field_age
>
metadata_age
:
                            
field
=
_RAW_TO_EMAIL_MAPPING
[
key
]
                            
exc
=
InvalidMetadata
(
                                
field
                                
f
"
{
field
}
introduced
in
metadata
version
"
                                
f
"
{
field_metadata_version
}
not
{
metadata_version
}
"
                            
)
                            
exceptions
.
append
(
exc
)
                            
continue
                    
getattr
(
ins
key
)
                
except
InvalidMetadata
as
exc
:
                    
exceptions
.
append
(
exc
)
            
if
exceptions
:
                
raise
ExceptionGroup
(
"
invalid
metadata
"
exceptions
)
        
return
ins
    
classmethod
    
def
from_email
(
cls
data
:
bytes
|
str
*
validate
:
bool
=
True
)
-
>
Metadata
:
        
"
"
"
Parse
metadata
from
email
headers
.
        
If
*
validate
*
is
true
the
metadata
will
be
validated
.
All
exceptions
        
related
to
validation
will
be
gathered
and
raised
as
an
:
class
:
ExceptionGroup
.
        
"
"
"
        
raw
unparsed
=
parse_email
(
data
)
        
if
validate
:
            
exceptions
:
list
[
Exception
]
=
[
]
            
for
unparsed_key
in
unparsed
:
                
if
unparsed_key
in
_EMAIL_TO_RAW_MAPPING
:
                    
message
=
f
"
{
unparsed_key
!
r
}
has
invalid
data
"
                
else
:
                    
message
=
f
"
unrecognized
field
:
{
unparsed_key
!
r
}
"
                
exceptions
.
append
(
InvalidMetadata
(
unparsed_key
message
)
)
            
if
exceptions
:
                
raise
ExceptionGroup
(
"
unparsed
"
exceptions
)
        
try
:
            
return
cls
.
from_raw
(
raw
validate
=
validate
)
        
except
ExceptionGroup
as
exc_group
:
            
raise
ExceptionGroup
(
                
"
invalid
or
unparsed
metadata
"
exc_group
.
exceptions
            
)
from
None
    
metadata_version
:
_Validator
[
_MetadataVersion
]
=
_Validator
(
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
metadata
-
version
    
(
required
;
validated
to
be
a
valid
metadata
version
)
"
"
"
    
name
:
_Validator
[
str
]
=
_Validator
(
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
name
    
(
required
;
validated
using
:
func
:
~
packaging
.
utils
.
canonicalize_name
and
its
    
*
validate
*
parameter
)
"
"
"
    
version
:
_Validator
[
version_module
.
Version
]
=
_Validator
(
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
version
(
required
)
"
"
"
    
dynamic
:
_Validator
[
list
[
str
]
|
None
]
=
_Validator
(
        
added
=
"
2
.
2
"
    
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
dynamic
    
(
validated
against
core
metadata
field
names
and
lowercased
)
"
"
"
    
platforms
:
_Validator
[
list
[
str
]
|
None
]
=
_Validator
(
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
platform
"
"
"
    
supported_platforms
:
_Validator
[
list
[
str
]
|
None
]
=
_Validator
(
added
=
"
1
.
1
"
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
supported
-
platform
"
"
"
    
summary
:
_Validator
[
str
|
None
]
=
_Validator
(
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
summary
(
validated
to
contain
no
newlines
)
"
"
"
    
description
:
_Validator
[
str
|
None
]
=
_Validator
(
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
description
"
"
"
    
description_content_type
:
_Validator
[
str
|
None
]
=
_Validator
(
added
=
"
2
.
1
"
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
description
-
content
-
type
(
validated
)
"
"
"
    
keywords
:
_Validator
[
list
[
str
]
|
None
]
=
_Validator
(
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
keywords
"
"
"
    
home_page
:
_Validator
[
str
|
None
]
=
_Validator
(
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
home
-
page
"
"
"
    
download_url
:
_Validator
[
str
|
None
]
=
_Validator
(
added
=
"
1
.
1
"
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
download
-
url
"
"
"
    
author
:
_Validator
[
str
|
None
]
=
_Validator
(
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
author
"
"
"
    
author_email
:
_Validator
[
str
|
None
]
=
_Validator
(
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
author
-
email
"
"
"
    
maintainer
:
_Validator
[
str
|
None
]
=
_Validator
(
added
=
"
1
.
2
"
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
maintainer
"
"
"
    
maintainer_email
:
_Validator
[
str
|
None
]
=
_Validator
(
added
=
"
1
.
2
"
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
maintainer
-
email
"
"
"
    
license
:
_Validator
[
str
|
None
]
=
_Validator
(
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
license
"
"
"
    
license_expression
:
_Validator
[
NormalizedLicenseExpression
|
None
]
=
_Validator
(
        
added
=
"
2
.
4
"
    
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
license
-
expression
"
"
"
    
license_files
:
_Validator
[
list
[
str
]
|
None
]
=
_Validator
(
added
=
"
2
.
4
"
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
license
-
file
"
"
"
    
classifiers
:
_Validator
[
list
[
str
]
|
None
]
=
_Validator
(
added
=
"
1
.
1
"
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
classifier
"
"
"
    
requires_dist
:
_Validator
[
list
[
requirements
.
Requirement
]
|
None
]
=
_Validator
(
        
added
=
"
1
.
2
"
    
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
requires
-
dist
"
"
"
    
requires_python
:
_Validator
[
specifiers
.
SpecifierSet
|
None
]
=
_Validator
(
        
added
=
"
1
.
2
"
    
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
requires
-
python
"
"
"
    
requires_external
:
_Validator
[
list
[
str
]
|
None
]
=
_Validator
(
added
=
"
1
.
2
"
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
requires
-
external
"
"
"
    
project_urls
:
_Validator
[
dict
[
str
str
]
|
None
]
=
_Validator
(
added
=
"
1
.
2
"
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
project
-
url
"
"
"
    
provides_extra
:
_Validator
[
list
[
utils
.
NormalizedName
]
|
None
]
=
_Validator
(
        
added
=
"
2
.
1
"
    
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
provides
-
extra
"
"
"
    
provides_dist
:
_Validator
[
list
[
str
]
|
None
]
=
_Validator
(
added
=
"
1
.
2
"
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
provides
-
dist
"
"
"
    
obsoletes_dist
:
_Validator
[
list
[
str
]
|
None
]
=
_Validator
(
added
=
"
1
.
2
"
)
    
"
"
"
:
external
:
ref
:
core
-
metadata
-
obsoletes
-
dist
"
"
"
    
requires
:
_Validator
[
list
[
str
]
|
None
]
=
_Validator
(
added
=
"
1
.
1
"
)
    
"
"
"
Requires
(
deprecated
)
"
"
"
    
provides
:
_Validator
[
list
[
str
]
|
None
]
=
_Validator
(
added
=
"
1
.
1
"
)
    
"
"
"
Provides
(
deprecated
)
"
"
"
    
obsoletes
:
_Validator
[
list
[
str
]
|
None
]
=
_Validator
(
added
=
"
1
.
1
"
)
    
"
"
"
Obsoletes
(
deprecated
)
"
"
"
