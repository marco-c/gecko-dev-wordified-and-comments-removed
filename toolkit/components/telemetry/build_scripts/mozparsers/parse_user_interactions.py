import
atexit
import
re
import
yaml
from
.
shared_telemetry_utils
import
ParserError
atexit
.
register
(
ParserError
.
exit_func
)
BASE_DOC_URL
=
(
    
"
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
toolkit
/
components
/
"
    
+
"
telemetry
/
telemetry
/
collection
/
user_interactions
.
html
"
)
class
UserInteractionType
:
    
"
"
"
A
class
for
representing
a
UserInteraction
definition
.
"
"
"
    
def
__init__
(
self
category_name
user_interaction_name
definition
)
:
        
self
.
validate_names
(
category_name
user_interaction_name
)
        
self
.
_name
=
user_interaction_name
        
self
.
_category_name
=
category_name
        
self
.
validate_types
(
definition
)
        
self
.
_definition
=
definition
    
def
validate_names
(
self
category_name
user_interaction_name
)
:
        
"
"
"
Validate
the
category
and
UserInteraction
name
:
            
-
Category
name
must
be
alpha
-
numeric
+
'
.
'
no
leading
/
trailing
digit
or
'
.
'
.
            
-
UserInteraction
name
must
be
alpha
-
numeric
+
'
_
'
no
leading
/
trailing
digit
or
'
_
'
.
        
:
param
category_name
:
the
name
of
the
category
the
UserInteraction
is
in
.
        
:
param
user_interaction_name
:
the
name
of
the
UserInteraction
.
        
:
raises
ParserError
:
if
the
length
of
the
names
exceeds
the
limit
or
they
don
'
t
                
conform
our
name
specification
.
        
"
"
"
        
MAX_NAME_LENGTH
=
40
        
for
n
in
[
category_name
user_interaction_name
]
:
            
if
len
(
n
)
>
MAX_NAME_LENGTH
:
                
ParserError
(
                    
f
"
Name
'
{
n
}
'
exceeds
maximum
name
length
of
{
MAX_NAME_LENGTH
}
characters
.
\
n
"
                    
f
"
See
:
{
BASE_DOC_URL
}
#
the
-
yaml
-
definition
-
file
"
                
)
.
handle_later
(
)
        
def
check_name
(
name
error_msg_prefix
allowed_char_regexp
)
:
            
chars_regxp
=
r
"
^
[
a
-
zA
-
Z0
-
9
"
+
allowed_char_regexp
+
r
"
]
+
"
            
if
not
re
.
search
(
chars_regxp
name
)
:
                
ParserError
(
                    
(
                        
error_msg_prefix
+
"
name
must
be
alpha
-
numeric
.
Got
:
'
{
}
'
.
\
n
"
                        
"
See
:
{
}
#
the
-
yaml
-
definition
-
file
"
                    
)
.
format
(
name
BASE_DOC_URL
)
                
)
.
handle_later
(
)
            
if
re
.
search
(
r
"
(
^
[
\
d
\
.
_
]
)
|
(
[
\
d
\
.
_
]
)
"
name
)
:
                
ParserError
(
                    
(
                        
error_msg_prefix
+
"
name
must
not
have
a
leading
/
trailing
"
                        
"
digit
a
dot
or
underscore
.
Got
:
'
{
}
'
.
\
n
"
                        
"
See
:
{
}
#
the
-
yaml
-
definition
-
file
"
                    
)
.
format
(
name
BASE_DOC_URL
)
                
)
.
handle_later
(
)
        
check_name
(
category_name
"
Category
"
r
"
\
.
"
)
        
check_name
(
user_interaction_name
"
UserInteraction
"
r
"
_
"
)
    
def
validate_types
(
self
definition
)
:
        
"
"
"
This
function
performs
some
basic
sanity
checks
on
the
UserInteraction
           
definition
:
            
-
Checks
that
all
the
required
fields
are
available
.
            
-
Checks
that
all
the
fields
have
the
expected
types
.
        
:
param
definition
:
the
dictionary
containing
the
UserInteraction
               
properties
.
        
:
raises
ParserError
:
if
a
UserInteraction
definition
field
is
of
the
                
wrong
type
.
        
:
raises
ParserError
:
if
a
required
field
is
missing
or
unknown
fields
are
present
.
        
"
"
"
        
REQUIRED_FIELDS
=
{
            
"
bug_numbers
"
:
list
            
"
description
"
:
str
        
}
        
LIST_FIELDS_CONTENT
=
{
            
"
bug_numbers
"
:
int
        
}
        
ALL_FIELDS
=
REQUIRED_FIELDS
.
copy
(
)
        
missing_fields
=
[
f
for
f
in
REQUIRED_FIELDS
.
keys
(
)
if
f
not
in
definition
]
        
if
len
(
missing_fields
)
>
0
:
            
ParserError
(
                
self
.
_name
                
+
"
-
missing
required
fields
:
"
                
+
"
"
.
join
(
missing_fields
)
                
+
f
"
.
\
nSee
:
{
BASE_DOC_URL
}
#
required
-
fields
"
            
)
.
handle_later
(
)
        
unknown_fields
=
[
f
for
f
in
definition
.
keys
(
)
if
f
not
in
ALL_FIELDS
]
        
if
len
(
unknown_fields
)
>
0
:
            
ParserError
(
                
self
.
_name
                
+
"
-
unknown
fields
:
"
                
+
"
"
.
join
(
unknown_fields
)
                
+
f
"
.
\
nSee
:
{
BASE_DOC_URL
}
#
required
-
fields
"
            
)
.
handle_later
(
)
        
wrong_type_names
=
[
            
f
"
{
f
}
must
be
{
str
(
ALL_FIELDS
[
f
]
)
}
"
            
for
f
in
definition
.
keys
(
)
            
if
not
isinstance
(
definition
[
f
]
ALL_FIELDS
[
f
]
)
        
]
        
if
len
(
wrong_type_names
)
>
0
:
            
ParserError
(
                
self
.
_name
                
+
"
-
"
                
+
"
"
.
join
(
wrong_type_names
)
                
+
f
"
.
\
nSee
:
{
BASE_DOC_URL
}
#
required
-
fields
"
            
)
.
handle_later
(
)
        
list_fields
=
[
f
for
f
in
definition
if
isinstance
(
definition
[
f
]
list
)
]
        
for
field
in
list_fields
:
            
if
len
(
definition
[
field
]
)
=
=
0
:
                
ParserError
(
                    
(
                        
"
Field
'
{
}
'
for
probe
'
{
}
'
must
not
be
empty
"
                        
+
"
.
\
nSee
:
{
}
#
required
-
fields
)
"
                    
)
.
format
(
field
self
.
_name
BASE_DOC_URL
)
                
)
.
handle_later
(
)
            
broken_types
=
[
                
not
isinstance
(
v
LIST_FIELDS_CONTENT
[
field
]
)
for
v
in
definition
[
field
]
            
]
            
if
any
(
broken_types
)
:
                
ParserError
(
                    
f
"
Field
'
{
field
}
'
for
probe
'
{
self
.
_name
}
'
must
only
contain
values
of
type
{
str
(
LIST_FIELDS_CONTENT
[
field
]
)
}
"
                    
f
"
.
\
nSee
:
{
BASE_DOC_URL
}
#
the
-
yaml
-
definition
-
file
)
"
                
)
.
handle_later
(
)
    
property
    
def
category
(
self
)
:
        
"
"
"
Get
the
category
name
"
"
"
        
return
self
.
_category_name
    
property
    
def
name
(
self
)
:
        
"
"
"
Get
the
UserInteraction
name
"
"
"
        
return
self
.
_name
    
property
    
def
label
(
self
)
:
        
"
"
"
Get
the
UserInteraction
label
generated
from
the
UserInteraction
        
and
category
names
.
        
"
"
"
        
return
self
.
_category_name
+
"
.
"
+
self
.
_name
    
property
    
def
bug_numbers
(
self
)
:
        
"
"
"
Get
the
list
of
related
bug
numbers
"
"
"
        
return
self
.
_definition
[
"
bug_numbers
"
]
    
property
    
def
description
(
self
)
:
        
"
"
"
Get
the
UserInteraction
description
"
"
"
        
return
self
.
_definition
[
"
description
"
]
def
load_user_interactions
(
filename
)
:
    
"
"
"
Parses
a
YAML
file
containing
the
UserInteraction
definition
.
    
:
param
filename
:
the
YAML
file
containing
the
UserInteraction
definition
.
    
:
raises
ParserError
:
if
the
UserInteraction
file
cannot
be
opened
or
            
parsed
.
    
"
"
"
    
user_interactions
=
None
    
try
:
        
with
open
(
filename
encoding
=
"
utf
-
8
"
)
as
f
:
            
user_interactions
=
yaml
.
safe_load
(
f
)
    
except
OSError
as
e
:
        
ParserError
(
"
Error
opening
"
+
filename
+
"
:
"
+
str
(
e
)
)
.
handle_now
(
)
    
except
ValueError
as
e
:
        
ParserError
(
            
f
"
Error
parsing
UserInteractions
in
{
filename
}
:
{
e
}
"
            
f
"
.
\
nSee
:
{
BASE_DOC_URL
}
"
        
)
.
handle_now
(
)
    
user_interaction_list
=
[
]
    
for
category_name
in
sorted
(
user_interactions
)
:
        
category
=
user_interactions
[
category_name
]
        
if
not
category
or
len
(
category
)
=
=
0
:
            
ParserError
(
                
f
'
Category
"
{
category_name
}
"
must
have
at
least
one
UserInteraction
in
it
'
                
f
"
.
\
nSee
:
{
BASE_DOC_URL
}
"
            
)
.
handle_later
(
)
        
for
user_interaction_name
in
sorted
(
category
)
:
            
user_interaction_info
=
category
[
user_interaction_name
]
            
user_interaction_list
.
append
(
                
UserInteractionType
(
                    
category_name
user_interaction_name
user_interaction_info
                
)
            
)
    
return
user_interaction_list
def
from_files
(
filenames
)
:
    
all_user_interactions
=
[
]
    
for
filename
in
filenames
:
        
all_user_interactions
+
=
load_user_interactions
(
filename
)
    
yield
from
all_user_interactions
