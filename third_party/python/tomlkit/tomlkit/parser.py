from
__future__
import
annotations
import
datetime
import
re
import
string
from
tomlkit
.
_compat
import
decode
from
tomlkit
.
_utils
import
RFC_3339_LOOSE
from
tomlkit
.
_utils
import
_escaped
from
tomlkit
.
_utils
import
parse_rfc3339
from
tomlkit
.
container
import
Container
from
tomlkit
.
exceptions
import
EmptyKeyError
from
tomlkit
.
exceptions
import
EmptyTableNameError
from
tomlkit
.
exceptions
import
InternalParserError
from
tomlkit
.
exceptions
import
InvalidCharInStringError
from
tomlkit
.
exceptions
import
InvalidControlChar
from
tomlkit
.
exceptions
import
InvalidDateError
from
tomlkit
.
exceptions
import
InvalidDateTimeError
from
tomlkit
.
exceptions
import
InvalidNumberError
from
tomlkit
.
exceptions
import
InvalidTimeError
from
tomlkit
.
exceptions
import
InvalidUnicodeValueError
from
tomlkit
.
exceptions
import
ParseError
from
tomlkit
.
exceptions
import
UnexpectedCharError
from
tomlkit
.
exceptions
import
UnexpectedEofError
from
tomlkit
.
items
import
AoT
from
tomlkit
.
items
import
Array
from
tomlkit
.
items
import
Bool
from
tomlkit
.
items
import
BoolType
from
tomlkit
.
items
import
Comment
from
tomlkit
.
items
import
Date
from
tomlkit
.
items
import
DateTime
from
tomlkit
.
items
import
Float
from
tomlkit
.
items
import
InlineTable
from
tomlkit
.
items
import
Integer
from
tomlkit
.
items
import
Item
from
tomlkit
.
items
import
Key
from
tomlkit
.
items
import
KeyType
from
tomlkit
.
items
import
Null
from
tomlkit
.
items
import
SingleKey
from
tomlkit
.
items
import
String
from
tomlkit
.
items
import
StringType
from
tomlkit
.
items
import
Table
from
tomlkit
.
items
import
Time
from
tomlkit
.
items
import
Trivia
from
tomlkit
.
items
import
Whitespace
from
tomlkit
.
source
import
Source
from
tomlkit
.
toml_char
import
TOMLChar
from
tomlkit
.
toml_document
import
TOMLDocument
CTRL_I
=
0x09
CTRL_J
=
0x0A
CTRL_M
=
0x0D
CTRL_CHAR_LIMIT
=
0x1F
CHR_DEL
=
0x7F
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
:
str
)
-
>
None
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
:
list
[
Key
]
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
-
>
str
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
:
type
[
ParseError
]
|
None
=
None
)
-
>
bool
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
:
int
exception
:
type
[
ParseError
]
|
None
=
None
)
-
>
bool
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
-
>
bool
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
-
>
None
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
*
*
kwargs
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
*
*
kwargs
)
    
def
parse
(
self
)
-
>
TOMLDocument
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
(
key
is
not
None
and
key
.
is_multi
(
)
)
or
not
self
.
_merge_ws
(
value
body
)
:
                
try
:
                    
body
.
append
(
key
value
)
                
except
Exception
as
e
:
                    
raise
self
.
parse_error
(
ParseError
str
(
e
)
)
from
e
            
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
)
            
try
:
                
body
.
append
(
key
value
)
            
except
Exception
as
e
:
                
raise
self
.
parse_error
(
ParseError
str
(
e
)
)
from
e
        
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
:
Item
container
:
Container
)
-
>
bool
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
:
Key
child
:
Key
)
-
>
bool
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
parent
)
        
child_parts
=
tuple
(
child
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
_parse_item
(
self
)
-
>
tuple
[
Key
|
None
Item
]
|
None
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
parse_trail
:
bool
=
True
)
-
>
tuple
[
str
str
str
]
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
:
                    
code
=
ord
(
self
.
_current
)
                    
if
code
=
=
CHR_DEL
or
code
<
=
CTRL_CHAR_LIMIT
and
code
!
=
CTRL_I
:
                        
raise
self
.
parse_error
(
InvalidControlChar
code
"
comments
"
)
                    
if
not
self
.
inc
(
)
:
                        
break
                
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
        
trail
=
"
"
        
if
parse_trail
:
            
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
:
bool
=
False
)
-
>
tuple
[
Key
Item
]
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
        
if
not
found_equals
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
        
if
not
key
.
sep
:
            
key
.
sep
=
self
.
extract
(
)
        
else
:
            
key
.
sep
+
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
            
if
not
meta
.
comment_ws
:
                
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
-
>
Key
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
-
>
Key
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
        
original
=
self
.
extract
(
)
        
quote_style
=
self
.
_current
        
key_type
=
next
(
(
t
for
t
in
KeyType
if
t
.
value
=
=
quote_style
)
None
)
        
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
        
key_str
=
self
.
_parse_string
(
            
StringType
.
SLB
if
key_type
=
=
KeyType
.
Basic
else
StringType
.
SLL
        
)
        
if
key_str
.
_t
.
is_multiline
(
)
:
            
raise
self
.
parse_error
(
UnexpectedCharError
key_str
.
_t
.
value
)
        
original
+
=
key_str
.
as_string
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
        
original
+
=
self
.
extract
(
)
        
key
=
SingleKey
(
str
(
key_str
)
t
=
key_type
sep
=
"
"
original
=
original
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
            
key
=
key
.
concat
(
self
.
_parse_key
(
)
)
        
return
key
    
def
_parse_bare_key
(
self
)
-
>
Key
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
        
while
(
            
self
.
_current
.
is_bare_key_char
(
)
or
self
.
_current
.
is_spaces
(
)
        
)
and
self
.
inc
(
)
:
            
pass
        
original
=
self
.
extract
(
)
        
key
=
original
.
strip
(
)
        
if
not
key
:
            
raise
self
.
parse_error
(
EmptyKeyError
)
        
if
"
"
in
key
:
            
raise
self
.
parse_error
(
ParseError
f
'
Invalid
key
"
{
key
}
"
'
)
        
key
=
SingleKey
(
key
KeyType
.
Bare
"
"
original
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
            
key
=
key
.
concat
(
self
.
_parse_key
(
)
)
        
return
key
    
def
_parse_value
(
self
)
-
>
Item
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
                        
assert
isinstance
(
dt
datetime
.
datetime
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
                        
assert
isinstance
(
dt
datetime
.
date
)
                        
date
=
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
                        
self
.
mark
(
)
                        
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
                        
time_raw
=
self
.
extract
(
)
                        
time_part
=
time_raw
.
rstrip
(
)
                        
trivia
.
comment_ws
=
time_raw
[
len
(
time_part
)
:
]
                        
if
not
time_part
:
                            
return
date
                        
dt
=
parse_rfc3339
(
raw
+
time_part
)
                        
assert
isinstance
(
dt
datetime
.
datetime
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
+
time_part
                        
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
                        
assert
isinstance
(
t
datetime
.
time
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
:
BoolType
)
-
>
Bool
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
-
>
Array
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
:
list
[
Item
]
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
+
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
            
newline
=
set
(
TOMLChar
.
NL
)
&
set
(
indent
)
            
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
parse_trail
=
False
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
            
return
res
    
def
_parse_inline_table
(
self
)
-
>
InlineTable
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
(
                    
trailing_comma
is
False
                    
or
trailing_comma
is
None
                    
and
self
.
_current
=
=
"
"
                
)
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
or
self
.
_current
=
=
"
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
:
str
trivia
:
Trivia
)
-
>
Item
|
None
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
len
(
raw
)
>
1
and
(
            
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
"
0e
"
)
)
            
or
sign
            
and
raw
.
startswith
(
"
.
"
)
        
)
:
            
return
None
        
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
None
        
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
f
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
digits
}
)
_
(
?
=
{
digits
}
)
"
"
"
raw
)
.
lower
(
)
        
if
"
_
"
in
clean
:
            
return
None
        
if
(
            
clean
.
endswith
(
"
.
"
)
            
or
not
clean
.
startswith
(
"
0x
"
)
            
and
clean
.
split
(
"
e
"
1
)
[
0
]
.
endswith
(
"
.
"
)
        
)
:
            
return
None
        
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
None
    
def
_parse_literal_string
(
self
)
-
>
String
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
-
>
String
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
:
StringType
)
-
>
String
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
                
f
"
Invalid
character
for
string
type
{
delim
}
"
            
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
:
            
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
exception
=
UnexpectedEofError
)
            
else
:
                
cur
=
self
.
_current
                
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
                    
if
self
.
inc
(
)
:
                        
cur
+
=
self
.
_current
                
if
cur
=
=
"
\
r
\
n
"
:
                    
self
.
inc_n
(
2
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
            
code
=
ord
(
self
.
_current
)
            
if
(
                
delim
.
is_singleline
(
)
                
and
not
escaped
                
and
(
code
=
=
CHR_DEL
or
code
<
=
CTRL_CHAR_LIMIT
and
code
!
=
CTRL_I
)
            
)
or
(
                
delim
.
is_multiline
(
)
                
and
not
escaped
                
and
(
                    
code
=
=
CHR_DEL
                    
or
code
<
=
CTRL_CHAR_LIMIT
                    
and
code
not
in
[
CTRL_I
CTRL_J
CTRL_M
]
                
)
            
)
:
                
raise
self
.
parse_error
(
InvalidControlChar
code
"
strings
"
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
                    
close
=
"
"
                    
while
self
.
_current
=
=
delim
.
unit
:
                        
close
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
                    
if
len
(
close
)
<
3
:
                        
value
+
=
close
                        
continue
                    
if
len
(
close
)
=
=
3
:
                        
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
                    
if
len
(
close
)
>
=
6
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
                    
value
+
=
close
[
:
-
3
]
                    
original
+
=
close
[
:
-
3
]
                    
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
:
Key
|
None
=
None
parent
:
Table
|
None
=
None
    
)
-
>
tuple
[
Key
Table
|
AoT
]
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
        
try
:
            
key
=
self
.
_parse_key
(
)
        
except
EmptyKeyError
:
            
raise
self
.
parse_error
(
EmptyTableNameError
)
from
None
        
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
        
elif
self
.
_current
!
=
"
]
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
.
sep
=
"
"
        
full_key
=
key
        
name_parts
=
tuple
(
key
)
        
if
any
(
"
"
in
part
.
key
.
strip
(
)
and
part
.
is_bare
(
)
for
part
in
name_parts
)
:
            
raise
self
.
parse_error
(
                
ParseError
f
'
Invalid
table
name
"
{
full_key
.
as_string
(
)
}
"
'
            
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
parent_name
)
        
else
:
            
parent_name_parts
=
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
name_parts
[
0
]
.
key
if
name_parts
else
key
.
key
            
display_name
=
full_key
.
as_string
(
)
            
is_super_table
=
False
        
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
"
"
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
                
child
=
table
.
get
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
)
-
2
                        
is_super_table
=
i
<
len
(
name_parts
)
-
2
                        
name
=
_name
.
key
                        
display_name
=
full_key
.
as_string
(
)
                        
if
i
=
=
len
(
name_parts
)
-
2
                        
else
None
                    
)
                
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
)
-
2
:
                    
table
.
raw_append
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
raw_append
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
                    
_
key_next
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
full_key
key_next
)
:
                        
key_next
table_next
=
self
.
_parse_table
(
full_key
table
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
key_next
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
full_key
key_next
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
full_key
table
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
full_key
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
full_key
)
        
return
key
result
    
def
_peek_table
(
self
)
-
>
tuple
[
bool
Key
]
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
            
try
:
                
return
is_aot
self
.
_parse_key
(
)
            
except
EmptyKeyError
:
                
raise
self
.
parse_error
(
EmptyTableNameError
)
from
None
    
def
_parse_aot
(
self
first
:
Table
name_first
:
Key
)
-
>
AoT
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
:
int
)
-
>
str
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
+
self
.
_src
.
EOF
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
:
bool
)
-
>
tuple
[
str
|
None
str
|
None
]
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
(
ValueError
OverflowError
)
:
                    
value
=
None
            
return
value
extracted
