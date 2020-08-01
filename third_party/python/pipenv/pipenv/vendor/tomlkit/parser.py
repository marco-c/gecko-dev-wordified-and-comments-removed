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
__future__
import
unicode_literals
import
re
import
string
from
.
_compat
import
chr
from
.
_compat
import
decode
from
.
_utils
import
_escaped
from
.
_utils
import
RFC_3339_LOOSE
from
.
_utils
import
parse_rfc3339
from
.
container
import
Container
from
.
exceptions
import
EmptyKeyError
from
.
exceptions
import
EmptyTableNameError
from
.
exceptions
import
InternalParserError
from
.
exceptions
import
InvalidCharInStringError
from
.
exceptions
import
InvalidDateTimeError
from
.
exceptions
import
InvalidDateError
from
.
exceptions
import
InvalidTimeError
from
.
exceptions
import
InvalidNumberError
from
.
exceptions
import
InvalidUnicodeValueError
from
.
exceptions
import
MixedArrayTypesError
from
.
exceptions
import
ParseError
from
.
exceptions
import
UnexpectedCharError
from
.
exceptions
import
UnexpectedEofError
from
.
items
import
AoT
from
.
items
import
Array
from
.
items
import
Bool
from
.
items
import
BoolType
from
.
items
import
Comment
from
.
items
import
Date
from
.
items
import
DateTime
from
.
items
import
Float
from
.
items
import
InlineTable
from
.
items
import
Integer
from
.
items
import
Item
from
.
items
import
Key
from
.
items
import
KeyType
from
.
items
import
Null
from
.
items
import
String
from
.
items
import
StringType
from
.
items
import
Table
from
.
items
import
Time
from
.
items
import
Trivia
from
.
items
import
Whitespace
from
.
source
import
Source
from
.
toml_char
import
TOMLChar
from
.
toml_document
import
TOMLDocument
class
Parser
:
    
"
"
"
    
Parser
for
TOML
documents
.
    
"
"
"
    
def
__init__
(
self
string
)
:
        
self
.
_src
=
Source
(
decode
(
string
)
)
        
self
.
_aot_stack
=
[
]
    
property
    
def
_state
(
self
)
:
        
return
self
.
_src
.
state
    
property
    
def
_idx
(
self
)
:
        
return
self
.
_src
.
idx
    
property
    
def
_current
(
self
)
:
        
return
self
.
_src
.
current
    
property
    
def
_marker
(
self
)
:
        
return
self
.
_src
.
marker
    
def
extract
(
self
)
:
        
"
"
"
        
Extracts
the
value
between
marker
and
index
        
"
"
"
        
return
self
.
_src
.
extract
(
)
    
def
inc
(
self
exception
=
None
)
:
        
"
"
"
        
Increments
the
parser
if
the
end
of
the
input
has
not
been
reached
.
        
Returns
whether
or
not
it
was
able
to
advance
.
        
"
"
"
        
return
self
.
_src
.
inc
(
exception
=
exception
)
    
def
inc_n
(
self
n
exception
=
None
)
:
        
"
"
"
        
Increments
the
parser
by
n
characters
        
if
the
end
of
the
input
has
not
been
reached
.
        
"
"
"
        
return
self
.
_src
.
inc_n
(
n
=
n
exception
=
exception
)
    
def
consume
(
self
chars
min
=
0
max
=
-
1
)
:
        
"
"
"
        
Consume
chars
until
min
/
max
is
satisfied
is
valid
.
        
"
"
"
        
return
self
.
_src
.
consume
(
chars
=
chars
min
=
min
max
=
max
)
    
def
end
(
self
)
:
        
"
"
"
        
Returns
True
if
the
parser
has
reached
the
end
of
the
input
.
        
"
"
"
        
return
self
.
_src
.
end
(
)
    
def
mark
(
self
)
:
        
"
"
"
        
Sets
the
marker
to
the
index
'
s
current
position
        
"
"
"
        
self
.
_src
.
mark
(
)
    
def
parse_error
(
self
exception
=
ParseError
*
args
)
:
        
"
"
"
        
Creates
a
generic
"
parse
error
"
at
the
current
position
.
        
"
"
"
        
return
self
.
_src
.
parse_error
(
exception
*
args
)
    
def
parse
(
self
)
:
        
body
=
TOMLDocument
(
True
)
        
while
not
self
.
end
(
)
:
            
if
self
.
_current
=
=
"
[
"
:
                
break
            
item
=
self
.
_parse_item
(
)
            
if
not
item
:
                
break
            
key
value
=
item
            
if
key
is
not
None
and
key
.
is_dotted
(
)
:
                
self
.
_handle_dotted_key
(
body
key
value
)
            
elif
not
self
.
_merge_ws
(
value
body
)
:
                
body
.
append
(
key
value
)
            
self
.
mark
(
)
        
while
not
self
.
end
(
)
:
            
key
value
=
self
.
_parse_table
(
)
            
if
isinstance
(
value
Table
)
and
value
.
is_aot_element
(
)
:
                
value
=
self
.
_parse_aot
(
value
key
.
key
)
            
body
.
append
(
key
value
)
        
body
.
parsing
(
False
)
        
return
body
    
def
_merge_ws
(
self
item
container
)
:
        
"
"
"
        
Merges
the
given
Item
with
the
last
one
currently
in
the
given
Container
if
        
both
are
whitespace
items
.
        
Returns
True
if
the
items
were
merged
.
        
"
"
"
        
last
=
container
.
last_item
(
)
        
if
not
last
:
            
return
False
        
if
not
isinstance
(
item
Whitespace
)
or
not
isinstance
(
last
Whitespace
)
:
            
return
False
        
start
=
self
.
_idx
-
(
len
(
last
.
s
)
+
len
(
item
.
s
)
)
        
container
.
body
[
-
1
]
=
(
            
container
.
body
[
-
1
]
[
0
]
            
Whitespace
(
self
.
_src
[
start
:
self
.
_idx
]
)
        
)
        
return
True
    
def
_is_child
(
self
parent
child
)
:
        
"
"
"
        
Returns
whether
a
key
is
strictly
a
child
of
another
key
.
        
AoT
siblings
are
not
considered
children
of
one
another
.
        
"
"
"
        
parent_parts
=
tuple
(
self
.
_split_table_name
(
parent
)
)
        
child_parts
=
tuple
(
self
.
_split_table_name
(
child
)
)
        
if
parent_parts
=
=
child_parts
:
            
return
False
        
return
parent_parts
=
=
child_parts
[
:
len
(
parent_parts
)
]
    
def
_split_table_name
(
self
name
)
:
        
in_name
=
False
        
current
=
"
"
        
t
=
KeyType
.
Bare
        
parts
=
0
        
for
c
in
name
.
strip
(
)
:
            
c
=
TOMLChar
(
c
)
            
if
c
=
=
"
.
"
:
                
if
in_name
:
                    
current
+
=
c
                    
continue
                
if
not
current
:
                    
raise
self
.
parse_error
(
)
                
yield
Key
(
current
.
strip
(
)
t
=
t
sep
=
"
"
)
                
parts
+
=
1
                
current
=
"
"
                
t
=
KeyType
.
Bare
                
continue
            
elif
c
in
{
"
'
"
'
"
'
}
:
                
if
in_name
:
                    
if
(
                        
t
=
=
KeyType
.
Literal
                        
and
c
=
=
'
"
'
                        
or
t
=
=
KeyType
.
Basic
                        
and
c
=
=
"
'
"
                    
)
:
                        
current
+
=
c
                        
continue
                    
if
c
!
=
t
.
value
:
                        
raise
self
.
parse_error
(
)
                    
in_name
=
False
                
else
:
                    
if
current
and
TOMLChar
(
current
[
-
1
]
)
.
is_spaces
(
)
and
not
parts
:
                        
raise
self
.
parse_error
(
)
                    
in_name
=
True
                    
t
=
KeyType
.
Literal
if
c
=
=
"
'
"
else
KeyType
.
Basic
                
continue
            
elif
in_name
or
c
.
is_bare_key_char
(
)
:
                
if
(
                    
not
in_name
                    
and
current
                    
and
TOMLChar
(
current
[
-
1
]
)
.
is_spaces
(
)
                    
and
not
parts
                
)
:
                    
raise
self
.
parse_error
(
)
                
current
+
=
c
            
elif
c
.
is_spaces
(
)
:
                
current
+
=
c
                
continue
            
else
:
                
raise
self
.
parse_error
(
)
        
if
current
.
strip
(
)
:
            
yield
Key
(
current
.
strip
(
)
t
=
t
sep
=
"
"
)
    
def
_parse_item
(
self
)
:
        
"
"
"
        
Attempts
to
parse
the
next
item
and
returns
it
along
with
its
key
        
if
the
item
is
value
-
like
.
        
"
"
"
        
self
.
mark
(
)
        
with
self
.
_state
as
state
:
            
while
True
:
                
c
=
self
.
_current
                
if
c
=
=
"
\
n
"
:
                    
self
.
inc
(
)
                    
return
None
Whitespace
(
self
.
extract
(
)
)
                
elif
c
in
"
\
t
\
r
"
:
                    
if
not
self
.
inc
(
)
:
                        
return
None
Whitespace
(
self
.
extract
(
)
)
                
elif
c
=
=
"
#
"
:
                    
indent
=
self
.
extract
(
)
                    
cws
comment
trail
=
self
.
_parse_comment_trail
(
)
                    
return
None
Comment
(
Trivia
(
indent
cws
comment
trail
)
)
                
elif
c
=
=
"
[
"
:
                    
return
                
else
:
                    
state
.
restore
=
True
                    
break
        
return
self
.
_parse_key_value
(
True
)
    
def
_parse_comment_trail
(
self
)
:
        
"
"
"
        
Returns
(
comment_ws
comment
trail
)
        
If
there
is
no
comment
comment_ws
and
comment
will
        
simply
be
empty
.
        
"
"
"
        
if
self
.
end
(
)
:
            
return
"
"
"
"
"
"
        
comment
=
"
"
        
comment_ws
=
"
"
        
self
.
mark
(
)
        
while
True
:
            
c
=
self
.
_current
            
if
c
=
=
"
\
n
"
:
                
break
            
elif
c
=
=
"
#
"
:
                
comment_ws
=
self
.
extract
(
)
                
self
.
mark
(
)
                
self
.
inc
(
)
                
while
not
self
.
end
(
)
and
not
self
.
_current
.
is_nl
(
)
and
self
.
inc
(
)
:
                    
pass
                
comment
=
self
.
extract
(
)
                
self
.
mark
(
)
                
break
            
elif
c
in
"
\
t
\
r
"
:
                
self
.
inc
(
)
            
else
:
                
raise
self
.
parse_error
(
UnexpectedCharError
c
)
            
if
self
.
end
(
)
:
                
break
        
while
self
.
_current
.
is_spaces
(
)
and
self
.
inc
(
)
:
            
pass
        
if
self
.
_current
=
=
"
\
r
"
:
            
self
.
inc
(
)
        
if
self
.
_current
=
=
"
\
n
"
:
            
self
.
inc
(
)
        
trail
=
"
"
        
if
self
.
_idx
!
=
self
.
_marker
or
self
.
_current
.
is_ws
(
)
:
            
trail
=
self
.
extract
(
)
        
return
comment_ws
comment
trail
    
def
_parse_key_value
(
self
parse_comment
=
False
)
:
        
self
.
mark
(
)
        
while
self
.
_current
.
is_spaces
(
)
and
self
.
inc
(
)
:
            
pass
        
indent
=
self
.
extract
(
)
        
key
=
self
.
_parse_key
(
)
        
if
not
key
.
key
.
strip
(
)
:
            
raise
self
.
parse_error
(
EmptyKeyError
)
        
self
.
mark
(
)
        
found_equals
=
self
.
_current
=
=
"
=
"
        
while
self
.
_current
.
is_kv_sep
(
)
and
self
.
inc
(
)
:
            
if
self
.
_current
=
=
"
=
"
:
                
if
found_equals
:
                    
raise
self
.
parse_error
(
UnexpectedCharError
"
=
"
)
                
else
:
                    
found_equals
=
True
            
pass
        
key
.
sep
=
self
.
extract
(
)
        
val
=
self
.
_parse_value
(
)
        
if
parse_comment
:
            
cws
comment
trail
=
self
.
_parse_comment_trail
(
)
            
meta
=
val
.
trivia
            
meta
.
comment_ws
=
cws
            
meta
.
comment
=
comment
            
meta
.
trail
=
trail
        
else
:
            
val
.
trivia
.
trail
=
"
"
        
val
.
trivia
.
indent
=
indent
        
return
key
val
    
def
_parse_key
(
self
)
:
        
"
"
"
        
Parses
a
Key
at
the
current
position
;
        
WS
before
the
key
must
be
exhausted
first
at
the
callsite
.
        
"
"
"
        
if
self
.
_current
in
"
\
"
'
"
:
            
return
self
.
_parse_quoted_key
(
)
        
else
:
            
return
self
.
_parse_bare_key
(
)
    
def
_parse_quoted_key
(
self
)
:
        
"
"
"
        
Parses
a
key
enclosed
in
either
single
or
double
quotes
.
        
"
"
"
        
quote_style
=
self
.
_current
        
key_type
=
None
        
dotted
=
False
        
for
t
in
KeyType
:
            
if
t
.
value
=
=
quote_style
:
                
key_type
=
t
                
break
        
if
key_type
is
None
:
            
raise
RuntimeError
(
"
Should
not
have
entered
_parse_quoted_key
(
)
"
)
        
self
.
inc
(
)
        
self
.
mark
(
)
        
while
self
.
_current
!
=
quote_style
and
self
.
inc
(
)
:
            
pass
        
key
=
self
.
extract
(
)
        
if
self
.
_current
=
=
"
.
"
:
            
self
.
inc
(
)
            
dotted
=
True
            
key
+
=
"
.
"
+
self
.
_parse_key
(
)
.
as_string
(
)
            
key_type
=
KeyType
.
Bare
        
else
:
            
self
.
inc
(
)
        
return
Key
(
key
key_type
"
"
dotted
)
    
def
_parse_bare_key
(
self
)
:
        
"
"
"
        
Parses
a
bare
key
.
        
"
"
"
        
key_type
=
None
        
dotted
=
False
        
self
.
mark
(
)
        
while
self
.
_current
.
is_bare_key_char
(
)
and
self
.
inc
(
)
:
            
pass
        
key
=
self
.
extract
(
)
        
if
self
.
_current
=
=
"
.
"
:
            
self
.
inc
(
)
            
dotted
=
True
            
key
+
=
"
.
"
+
self
.
_parse_key
(
)
.
as_string
(
)
            
key_type
=
KeyType
.
Bare
        
return
Key
(
key
key_type
"
"
dotted
)
    
def
_handle_dotted_key
(
        
self
container
key
value
    
)
:
        
names
=
tuple
(
self
.
_split_table_name
(
key
.
key
)
)
        
name
=
names
[
0
]
        
name
.
_dotted
=
True
        
if
name
in
container
:
            
if
isinstance
(
container
Table
)
:
                
table
=
container
.
value
.
item
(
name
)
            
else
:
                
table
=
container
.
item
(
name
)
        
else
:
            
table
=
Table
(
Container
(
True
)
Trivia
(
)
False
is_super_table
=
True
)
            
if
isinstance
(
container
Table
)
:
                
container
.
raw_append
(
name
table
)
            
else
:
                
container
.
append
(
name
table
)
        
for
i
_name
in
enumerate
(
names
[
1
:
]
)
:
            
if
i
=
=
len
(
names
)
-
2
:
                
_name
.
sep
=
key
.
sep
                
table
.
append
(
_name
value
)
            
else
:
                
_name
.
_dotted
=
True
                
if
_name
in
table
.
value
:
                    
table
=
table
.
value
.
item
(
_name
)
                
else
:
                    
table
.
append
(
                        
_name
                        
Table
(
                            
Container
(
True
)
                            
Trivia
(
)
                            
False
                            
is_super_table
=
i
<
len
(
names
)
-
2
                        
)
                    
)
                    
table
=
table
[
_name
]
    
def
_parse_value
(
self
)
:
        
"
"
"
        
Attempts
to
parse
a
value
at
the
current
position
.
        
"
"
"
        
self
.
mark
(
)
        
c
=
self
.
_current
        
trivia
=
Trivia
(
)
        
if
c
=
=
StringType
.
SLB
.
value
:
            
return
self
.
_parse_basic_string
(
)
        
elif
c
=
=
StringType
.
SLL
.
value
:
            
return
self
.
_parse_literal_string
(
)
        
elif
c
=
=
BoolType
.
TRUE
.
value
[
0
]
:
            
return
self
.
_parse_true
(
)
        
elif
c
=
=
BoolType
.
FALSE
.
value
[
0
]
:
            
return
self
.
_parse_false
(
)
        
elif
c
=
=
"
[
"
:
            
return
self
.
_parse_array
(
)
        
elif
c
=
=
"
{
"
:
            
return
self
.
_parse_inline_table
(
)
        
elif
c
in
"
+
-
"
or
self
.
_peek
(
4
)
in
{
            
"
+
inf
"
            
"
-
inf
"
            
"
inf
"
            
"
+
nan
"
            
"
-
nan
"
            
"
nan
"
        
}
:
            
while
self
.
_current
not
in
"
\
t
\
n
\
r
#
]
}
"
and
self
.
inc
(
)
:
                
pass
            
raw
=
self
.
extract
(
)
            
item
=
self
.
_parse_number
(
raw
trivia
)
            
if
item
is
not
None
:
                
return
item
            
raise
self
.
parse_error
(
InvalidNumberError
)
        
elif
c
in
string
.
digits
:
            
while
self
.
_current
not
in
"
\
t
\
n
\
r
#
]
}
"
and
self
.
inc
(
)
:
                
pass
            
raw
=
self
.
extract
(
)
            
m
=
RFC_3339_LOOSE
.
match
(
raw
)
            
if
m
:
                
if
m
.
group
(
1
)
and
m
.
group
(
5
)
:
                    
try
:
                        
dt
=
parse_rfc3339
(
raw
)
                        
return
DateTime
(
                            
dt
.
year
                            
dt
.
month
                            
dt
.
day
                            
dt
.
hour
                            
dt
.
minute
                            
dt
.
second
                            
dt
.
microsecond
                            
dt
.
tzinfo
                            
trivia
                            
raw
                        
)
                    
except
ValueError
:
                        
raise
self
.
parse_error
(
InvalidDateTimeError
)
                
if
m
.
group
(
1
)
:
                    
try
:
                        
dt
=
parse_rfc3339
(
raw
)
                        
return
Date
(
dt
.
year
dt
.
month
dt
.
day
trivia
raw
)
                    
except
ValueError
:
                        
raise
self
.
parse_error
(
InvalidDateError
)
                
if
m
.
group
(
5
)
:
                    
try
:
                        
t
=
parse_rfc3339
(
raw
)
                        
return
Time
(
                            
t
.
hour
                            
t
.
minute
                            
t
.
second
                            
t
.
microsecond
                            
t
.
tzinfo
                            
trivia
                            
raw
                        
)
                    
except
ValueError
:
                        
raise
self
.
parse_error
(
InvalidTimeError
)
            
item
=
self
.
_parse_number
(
raw
trivia
)
            
if
item
is
not
None
:
                
return
item
            
raise
self
.
parse_error
(
InvalidNumberError
)
        
else
:
            
raise
self
.
parse_error
(
UnexpectedCharError
c
)
    
def
_parse_true
(
self
)
:
        
return
self
.
_parse_bool
(
BoolType
.
TRUE
)
    
def
_parse_false
(
self
)
:
        
return
self
.
_parse_bool
(
BoolType
.
FALSE
)
    
def
_parse_bool
(
self
style
)
:
        
with
self
.
_state
:
            
style
=
BoolType
(
style
)
            
for
c
in
style
:
                
self
.
consume
(
c
min
=
1
max
=
1
)
            
return
Bool
(
style
Trivia
(
)
)
    
def
_parse_array
(
self
)
:
        
self
.
inc
(
exception
=
UnexpectedEofError
)
        
elems
=
[
]
        
prev_value
=
None
        
while
True
:
            
mark
=
self
.
_idx
            
self
.
consume
(
TOMLChar
.
SPACES
)
            
newline
=
self
.
consume
(
TOMLChar
.
NL
)
            
indent
=
self
.
_src
[
mark
:
self
.
_idx
]
            
if
newline
:
                
elems
.
append
(
Whitespace
(
indent
)
)
                
continue
            
if
self
.
_current
=
=
"
#
"
:
                
cws
comment
trail
=
self
.
_parse_comment_trail
(
)
                
elems
.
append
(
Comment
(
Trivia
(
indent
cws
comment
trail
)
)
)
                
continue
            
if
indent
:
                
elems
.
append
(
Whitespace
(
indent
)
)
                
continue
            
if
not
prev_value
:
                
try
:
                    
elems
.
append
(
self
.
_parse_value
(
)
)
                    
prev_value
=
True
                    
continue
                
except
UnexpectedCharError
:
                    
pass
            
if
prev_value
and
self
.
_current
=
=
"
"
:
                
self
.
inc
(
exception
=
UnexpectedEofError
)
                
elems
.
append
(
Whitespace
(
"
"
)
)
                
prev_value
=
False
                
continue
            
if
self
.
_current
=
=
"
]
"
:
                
self
.
inc
(
)
                
break
            
raise
self
.
parse_error
(
UnexpectedCharError
self
.
_current
)
        
try
:
            
res
=
Array
(
elems
Trivia
(
)
)
        
except
ValueError
:
            
pass
        
else
:
            
if
res
.
is_homogeneous
(
)
:
                
return
res
        
raise
self
.
parse_error
(
MixedArrayTypesError
)
    
def
_parse_inline_table
(
self
)
:
        
self
.
inc
(
exception
=
UnexpectedEofError
)
        
elems
=
Container
(
True
)
        
trailing_comma
=
None
        
while
True
:
            
mark
=
self
.
_idx
            
self
.
consume
(
TOMLChar
.
SPACES
)
            
raw
=
self
.
_src
[
mark
:
self
.
_idx
]
            
if
raw
:
                
elems
.
add
(
Whitespace
(
raw
)
)
            
if
not
trailing_comma
:
                
if
self
.
_current
=
=
"
}
"
:
                    
self
.
inc
(
)
                    
break
                
if
trailing_comma
is
False
:
                    
raise
self
.
parse_error
(
UnexpectedCharError
self
.
_current
)
            
else
:
                
if
self
.
_current
=
=
"
}
"
:
                    
raise
self
.
parse_error
(
UnexpectedCharError
self
.
_current
)
            
key
val
=
self
.
_parse_key_value
(
False
)
            
elems
.
add
(
key
val
)
            
mark
=
self
.
_idx
            
self
.
consume
(
TOMLChar
.
SPACES
)
            
raw
=
self
.
_src
[
mark
:
self
.
_idx
]
            
if
raw
:
                
elems
.
add
(
Whitespace
(
raw
)
)
            
trailing_comma
=
self
.
_current
=
=
"
"
            
if
trailing_comma
:
                
self
.
inc
(
exception
=
UnexpectedEofError
)
        
return
InlineTable
(
elems
Trivia
(
)
)
    
def
_parse_number
(
self
raw
trivia
)
:
        
sign
=
"
"
        
if
raw
.
startswith
(
(
"
+
"
"
-
"
)
)
:
            
sign
=
raw
[
0
]
            
raw
=
raw
[
1
:
]
        
if
(
            
len
(
raw
)
>
1
            
and
raw
.
startswith
(
"
0
"
)
            
and
not
raw
.
startswith
(
(
"
0
.
"
"
0o
"
"
0x
"
"
0b
"
)
)
        
)
:
            
return
        
if
raw
.
startswith
(
(
"
0o
"
"
0x
"
"
0b
"
)
)
and
sign
:
            
return
        
digits
=
"
[
0
-
9
]
"
        
base
=
10
        
if
raw
.
startswith
(
"
0b
"
)
:
            
digits
=
"
[
01
]
"
            
base
=
2
        
elif
raw
.
startswith
(
"
0o
"
)
:
            
digits
=
"
[
0
-
7
]
"
            
base
=
8
        
elif
raw
.
startswith
(
"
0x
"
)
:
            
digits
=
"
[
0
-
9a
-
f
]
"
            
base
=
16
        
clean
=
re
.
sub
(
"
(
?
i
)
(
?
<
=
{
}
)
_
(
?
=
{
}
)
"
.
format
(
digits
digits
)
"
"
raw
)
        
if
"
_
"
in
clean
:
            
return
        
if
clean
.
endswith
(
"
.
"
)
:
            
return
        
try
:
            
return
Integer
(
int
(
sign
+
clean
base
)
trivia
sign
+
raw
)
        
except
ValueError
:
            
try
:
                
return
Float
(
float
(
sign
+
clean
)
trivia
sign
+
raw
)
            
except
ValueError
:
                
return
    
def
_parse_literal_string
(
self
)
:
        
with
self
.
_state
:
            
return
self
.
_parse_string
(
StringType
.
SLL
)
    
def
_parse_basic_string
(
self
)
:
        
with
self
.
_state
:
            
return
self
.
_parse_string
(
StringType
.
SLB
)
    
def
_parse_escaped_char
(
self
multiline
)
:
        
if
multiline
and
self
.
_current
.
is_ws
(
)
:
            
tmp
=
"
"
            
while
self
.
_current
.
is_ws
(
)
:
                
tmp
+
=
self
.
_current
                
self
.
inc
(
exception
=
UnexpectedEofError
)
                
continue
            
if
"
\
n
"
not
in
tmp
:
                
raise
self
.
parse_error
(
InvalidCharInStringError
self
.
_current
)
            
return
"
"
        
if
self
.
_current
in
_escaped
:
            
c
=
_escaped
[
self
.
_current
]
            
self
.
inc
(
exception
=
UnexpectedEofError
)
            
return
c
        
if
self
.
_current
in
{
"
u
"
"
U
"
}
:
            
u
ue
=
self
.
_peek_unicode
(
self
.
_current
=
=
"
U
"
)
            
if
u
is
not
None
:
                
self
.
inc_n
(
len
(
ue
)
+
1
)
                
return
u
            
raise
self
.
parse_error
(
InvalidUnicodeValueError
)
        
raise
self
.
parse_error
(
InvalidCharInStringError
self
.
_current
)
    
def
_parse_string
(
self
delim
)
:
        
if
self
.
_current
!
=
delim
.
unit
:
            
raise
self
.
parse_error
(
                
InternalParserError
                
"
Invalid
character
for
string
type
{
}
"
.
format
(
delim
)
            
)
        
self
.
inc
(
exception
=
UnexpectedEofError
)
        
if
self
.
_current
=
=
delim
.
unit
:
            
if
not
self
.
inc
(
)
or
self
.
_current
!
=
delim
.
unit
:
                
return
String
(
delim
"
"
"
"
Trivia
(
)
)
            
self
.
inc
(
exception
=
UnexpectedEofError
)
            
delim
=
delim
.
toggle
(
)
        
self
.
mark
(
)
        
value
=
"
"
        
if
delim
.
is_multiline
(
)
and
self
.
_current
=
=
"
\
n
"
:
            
self
.
inc
(
exception
=
UnexpectedEofError
)
        
escaped
=
False
        
while
True
:
            
if
delim
.
is_singleline
(
)
and
self
.
_current
.
is_nl
(
)
:
                
raise
self
.
parse_error
(
InvalidCharInStringError
self
.
_current
)
            
elif
not
escaped
and
self
.
_current
=
=
delim
.
unit
:
                
original
=
self
.
extract
(
)
                
close
=
"
"
                
if
delim
.
is_multiline
(
)
:
                    
for
last
in
[
False
False
True
]
:
                        
if
self
.
_current
!
=
delim
.
unit
:
                            
value
+
=
close
                            
close
=
"
"
                            
break
                        
close
+
=
delim
.
unit
                        
self
.
inc
(
exception
=
UnexpectedEofError
if
not
last
else
None
)
                    
if
not
close
:
                        
continue
                
else
:
                    
self
.
inc
(
)
                
return
String
(
delim
value
original
Trivia
(
)
)
            
elif
delim
.
is_basic
(
)
and
escaped
:
                
value
+
=
self
.
_parse_escaped_char
(
delim
.
is_multiline
(
)
)
                
escaped
=
False
            
elif
delim
.
is_basic
(
)
and
self
.
_current
=
=
"
\
\
"
:
                
escaped
=
True
                
self
.
inc
(
exception
=
UnexpectedEofError
)
            
else
:
                
value
+
=
self
.
_current
                
self
.
inc
(
exception
=
UnexpectedEofError
)
    
def
_parse_table
(
        
self
parent_name
=
None
    
)
:
        
"
"
"
        
Parses
a
table
element
.
        
"
"
"
        
if
self
.
_current
!
=
"
[
"
:
            
raise
self
.
parse_error
(
                
InternalParserError
"
_parse_table
(
)
called
on
non
-
bracket
character
.
"
            
)
        
indent
=
self
.
extract
(
)
        
self
.
inc
(
)
        
if
self
.
end
(
)
:
            
raise
self
.
parse_error
(
UnexpectedEofError
)
        
is_aot
=
False
        
if
self
.
_current
=
=
"
[
"
:
            
if
not
self
.
inc
(
)
:
                
raise
self
.
parse_error
(
UnexpectedEofError
)
            
is_aot
=
True
        
self
.
mark
(
)
        
while
self
.
_current
.
is_spaces
(
)
and
self
.
inc
(
)
:
            
pass
        
ws_prefix
=
self
.
extract
(
)
        
if
self
.
_current
in
[
StringType
.
SLL
.
value
StringType
.
SLB
.
value
]
:
            
delimiter
=
(
                
StringType
.
SLL
                
if
self
.
_current
=
=
StringType
.
SLL
.
value
                
else
StringType
.
SLB
            
)
            
name
=
self
.
_parse_string
(
delimiter
)
            
name
=
"
{
delimiter
}
{
name
}
{
delimiter
}
"
.
format
(
                
delimiter
=
delimiter
.
value
name
=
name
            
)
            
self
.
mark
(
)
            
while
self
.
_current
!
=
"
]
"
and
self
.
inc
(
)
:
                
if
self
.
end
(
)
:
                    
raise
self
.
parse_error
(
UnexpectedEofError
)
                
pass
            
ws_suffix
=
self
.
extract
(
)
            
name
+
=
ws_suffix
        
else
:
            
self
.
mark
(
)
            
while
self
.
_current
!
=
"
]
"
and
self
.
inc
(
)
:
                
if
self
.
end
(
)
:
                    
raise
self
.
parse_error
(
UnexpectedEofError
)
                
pass
            
name
=
self
.
extract
(
)
        
name
=
ws_prefix
+
name
        
if
not
name
.
strip
(
)
:
            
raise
self
.
parse_error
(
EmptyTableNameError
)
        
key
=
Key
(
name
sep
=
"
"
)
        
name_parts
=
tuple
(
self
.
_split_table_name
(
name
)
)
        
missing_table
=
False
        
if
parent_name
:
            
parent_name_parts
=
tuple
(
self
.
_split_table_name
(
parent_name
)
)
        
else
:
            
parent_name_parts
=
tuple
(
)
        
if
len
(
name_parts
)
>
len
(
parent_name_parts
)
+
1
:
            
missing_table
=
True
        
name_parts
=
name_parts
[
len
(
parent_name_parts
)
:
]
        
values
=
Container
(
True
)
        
self
.
inc
(
)
        
if
is_aot
:
            
self
.
inc
(
)
        
cws
comment
trail
=
self
.
_parse_comment_trail
(
)
        
result
=
Null
(
)
        
table
=
Table
(
            
values
            
Trivia
(
indent
cws
comment
trail
)
            
is_aot
            
name
=
name
            
display_name
=
name
        
)
        
if
len
(
name_parts
)
>
1
:
            
if
missing_table
:
                
table
=
Table
(
                    
Container
(
True
)
                    
Trivia
(
indent
cws
comment
trail
)
                    
is_aot
and
name_parts
[
0
]
.
key
in
self
.
_aot_stack
                    
is_super_table
=
True
                    
name
=
name_parts
[
0
]
.
key
                
)
                
result
=
table
                
key
=
name_parts
[
0
]
                
for
i
_name
in
enumerate
(
name_parts
[
1
:
]
)
:
                    
if
_name
in
table
:
                        
child
=
table
[
_name
]
                    
else
:
                        
child
=
Table
(
                            
Container
(
True
)
                            
Trivia
(
indent
cws
comment
trail
)
                            
is_aot
and
i
=
=
len
(
name_parts
[
1
:
]
)
-
1
                            
is_super_table
=
i
<
len
(
name_parts
[
1
:
]
)
-
1
                            
name
=
_name
.
key
                            
display_name
=
name
if
i
=
=
len
(
name_parts
[
1
:
]
)
-
1
else
None
                        
)
                    
if
is_aot
and
i
=
=
len
(
name_parts
[
1
:
]
)
-
1
:
                        
table
.
append
(
_name
AoT
(
[
child
]
name
=
table
.
name
parsed
=
True
)
)
                    
else
:
                        
table
.
append
(
_name
child
)
                    
table
=
child
                    
values
=
table
.
value
        
else
:
            
if
name_parts
:
                
key
=
name_parts
[
0
]
        
while
not
self
.
end
(
)
:
            
item
=
self
.
_parse_item
(
)
            
if
item
:
                
_key
item
=
item
                
if
not
self
.
_merge_ws
(
item
values
)
:
                    
if
_key
is
not
None
and
_key
.
is_dotted
(
)
:
                        
self
.
_handle_dotted_key
(
table
_key
item
)
                    
else
:
                        
table
.
raw_append
(
_key
item
)
            
else
:
                
if
self
.
_current
=
=
"
[
"
:
                    
is_aot_next
name_next
=
self
.
_peek_table
(
)
                    
if
self
.
_is_child
(
name
name_next
)
:
                        
key_next
table_next
=
self
.
_parse_table
(
name
)
                        
table
.
raw_append
(
key_next
table_next
)
                        
while
not
self
.
end
(
)
:
                            
_
name_next
=
self
.
_peek_table
(
)
                            
if
not
self
.
_is_child
(
name
name_next
)
:
                                
break
                            
key_next
table_next
=
self
.
_parse_table
(
name
)
                            
table
.
raw_append
(
key_next
table_next
)
                    
break
                
else
:
                    
raise
self
.
parse_error
(
                        
InternalParserError
                        
"
_parse_item
(
)
returned
None
on
a
non
-
bracket
character
.
"
                    
)
        
if
isinstance
(
result
Null
)
:
            
result
=
table
            
if
is_aot
and
(
not
self
.
_aot_stack
or
name
!
=
self
.
_aot_stack
[
-
1
]
)
:
                
result
=
self
.
_parse_aot
(
result
name
)
        
return
key
result
    
def
_peek_table
(
self
)
:
        
"
"
"
        
Peeks
ahead
non
-
intrusively
by
cloning
then
restoring
the
        
initial
state
of
the
parser
.
        
Returns
the
name
of
the
table
about
to
be
parsed
        
as
well
as
whether
it
is
part
of
an
AoT
.
        
"
"
"
        
with
self
.
_state
(
save_marker
=
True
restore
=
True
)
:
            
if
self
.
_current
!
=
"
[
"
:
                
raise
self
.
parse_error
(
                    
InternalParserError
                    
"
_peek_table
(
)
entered
on
non
-
bracket
character
"
                
)
            
self
.
inc
(
)
            
is_aot
=
False
            
if
self
.
_current
=
=
"
[
"
:
                
self
.
inc
(
)
                
is_aot
=
True
            
self
.
mark
(
)
            
while
self
.
_current
!
=
"
]
"
and
self
.
inc
(
)
:
                
table_name
=
self
.
extract
(
)
            
return
is_aot
table_name
    
def
_parse_aot
(
self
first
name_first
)
:
        
"
"
"
        
Parses
all
siblings
of
the
provided
table
first
and
bundles
them
into
        
an
AoT
.
        
"
"
"
        
payload
=
[
first
]
        
self
.
_aot_stack
.
append
(
name_first
)
        
while
not
self
.
end
(
)
:
            
is_aot_next
name_next
=
self
.
_peek_table
(
)
            
if
is_aot_next
and
name_next
=
=
name_first
:
                
_
table
=
self
.
_parse_table
(
name_first
)
                
payload
.
append
(
table
)
            
else
:
                
break
        
self
.
_aot_stack
.
pop
(
)
        
return
AoT
(
payload
parsed
=
True
)
    
def
_peek
(
self
n
)
:
        
"
"
"
        
Peeks
ahead
n
characters
.
        
n
is
the
max
number
of
characters
that
will
be
peeked
.
        
"
"
"
        
with
self
.
_state
(
restore
=
True
)
:
            
buf
=
"
"
            
for
_
in
range
(
n
)
:
                
if
self
.
_current
not
in
"
\
t
\
n
\
r
#
]
}
"
:
                    
buf
+
=
self
.
_current
                    
self
.
inc
(
)
                    
continue
                
break
            
return
buf
    
def
_peek_unicode
(
        
self
is_long
    
)
:
        
"
"
"
        
Peeks
ahead
non
-
intrusively
by
cloning
then
restoring
the
        
initial
state
of
the
parser
.
        
Returns
the
unicode
value
is
it
'
s
a
valid
one
else
None
.
        
"
"
"
        
with
self
.
_state
(
save_marker
=
True
restore
=
True
)
:
            
if
self
.
_current
not
in
{
"
u
"
"
U
"
}
:
                
raise
self
.
parse_error
(
                    
InternalParserError
"
_peek_unicode
(
)
entered
on
non
-
unicode
value
"
                
)
            
self
.
inc
(
)
            
self
.
mark
(
)
            
if
is_long
:
                
chars
=
8
            
else
:
                
chars
=
4
            
if
not
self
.
inc_n
(
chars
)
:
                
value
extracted
=
None
None
            
else
:
                
extracted
=
self
.
extract
(
)
                
if
extracted
[
0
]
.
lower
(
)
=
=
"
d
"
and
extracted
[
1
]
.
strip
(
"
01234567
"
)
:
                    
return
None
None
                
try
:
                    
value
=
chr
(
int
(
extracted
16
)
)
                
except
ValueError
:
                    
value
=
None
            
return
value
extracted
