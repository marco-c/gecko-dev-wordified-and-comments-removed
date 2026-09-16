#
-
*
-
coding
:
utf
-
8
-
*
-
from
packageurl
import
PackageURL
def
purl_to_lookups
(
purl_str
encode
=
True
include_empty_fields
=
False
)
:
    
"
"
"
    
Return
a
lookups
dictionary
built
from
the
provided
purl
(
Package
URL
)
string
.
    
These
lookups
can
be
used
as
QuerySet
filters
.
    
If
include_empty_fields
is
provided
the
resulting
dictionary
will
include
fields
    
with
empty
values
.
This
is
useful
to
get
exact
match
.
    
Note
that
empty
values
are
always
returned
as
empty
strings
as
the
model
fields
    
are
defined
with
blank
=
True
and
null
=
False
.
    
"
"
"
    
if
not
purl_str
.
startswith
(
"
pkg
:
"
)
:
        
purl_str
=
"
pkg
:
"
+
purl_str
    
try
:
        
package_url
=
PackageURL
.
from_string
(
purl_str
)
    
except
ValueError
:
        
return
    
package_url_dict
=
package_url
.
to_dict
(
encode
=
encode
empty
=
"
"
)
    
if
include_empty_fields
:
        
return
package_url_dict
    
else
:
        
return
without_empty_values
(
package_url_dict
)
def
without_empty_values
(
input_dict
)
:
    
"
"
"
    
Return
a
new
dict
not
including
empty
value
entries
from
input_dict
.
    
None
empty
string
empty
list
and
empty
dict
/
set
are
cleaned
.
    
0
and
False
values
are
kept
.
    
"
"
"
    
empty_values
=
(
[
]
(
)
{
}
"
"
None
)
    
return
{
key
:
value
for
key
value
in
input_dict
.
items
(
)
if
value
not
in
empty_values
}
