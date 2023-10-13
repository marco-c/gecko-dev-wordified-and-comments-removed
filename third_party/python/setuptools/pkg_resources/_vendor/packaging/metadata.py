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
sys
import
typing
from
typing
import
Dict
List
Optional
Tuple
Union
cast
if
sys
.
version_info
>
=
(
3
8
)
:
    
from
typing
import
TypedDict
else
:
    
if
typing
.
TYPE_CHECKING
:
        
from
typing_extensions
import
TypedDict
    
else
:
        
try
:
            
from
typing_extensions
import
TypedDict
        
except
ImportError
:
            
class
TypedDict
:
                
def
__init_subclass__
(
*
_args
*
*
_kwargs
)
:
                    
pass
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
List
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
List
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
List
[
str
]
    
download_url
:
str
    
classifiers
:
List
[
str
]
    
requires
:
List
[
str
]
    
provides
:
List
[
str
]
    
obsoletes
:
List
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
List
[
str
]
    
provides_dist
:
List
[
str
]
    
obsoletes_dist
:
List
[
str
]
    
requires_python
:
str
    
requires_external
:
List
[
str
]
    
project_urls
:
Dict
[
str
str
]
    
description_content_type
:
str
    
provides_extra
:
List
[
str
]
    
dynamic
:
List
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
_LIST_STRING_FIELDS
=
{
    
"
classifiers
"
    
"
dynamic
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
def
_parse_keywords
(
data
:
str
)
-
>
List
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
separate
keyboards
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
List
[
str
]
)
-
>
Dict
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
Union
[
bytes
str
]
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
:
str
=
msg
.
get_payload
(
)
        
return
payload
    
else
:
        
bpayload
:
bytes
=
msg
.
get_payload
(
decode
=
True
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
def
parse_email
(
data
:
Union
[
bytes
str
]
)
-
>
Tuple
[
RawMetadata
Dict
[
str
List
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
Dict
[
str
Union
[
str
List
[
str
]
Dict
[
str
str
]
]
]
=
{
}
    
unparsed
:
Dict
[
str
List
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
List
[
Tuple
[
bytes
Optional
[
str
]
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
_LIST_STRING_FIELDS
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
