import
io
import
os
import
re
from
tomlkit
import
parse
from
tomlkit
.
exceptions
import
ParseError
from
tomlkit
.
items
import
Array
from
.
ini
import
combine_fields
__all__
=
[
"
read_toml
"
]
def
read_toml
(
    
fp
    
defaults
=
None
    
default
=
"
DEFAULT
"
    
comments
=
None
    
separators
=
None
    
strict
=
True
    
handle_defaults
=
True
)
:
    
"
"
"
    
read
a
.
toml
file
and
return
a
list
of
[
(
section
values
)
]
    
-
fp
:
file
pointer
or
path
to
read
    
-
defaults
:
default
set
of
variables
    
-
default
:
name
of
the
section
for
the
default
section
    
-
comments
:
characters
that
if
they
start
a
line
denote
a
comment
    
-
separators
:
strings
that
denote
key
value
separation
in
order
    
-
strict
:
whether
to
be
strict
about
parsing
    
-
handle_defaults
:
whether
to
incorporate
defaults
into
each
section
    
"
"
"
    
defaults
=
defaults
or
{
}
    
default_section
=
{
}
    
comments
=
comments
or
(
"
#
"
)
    
separators
=
separators
or
(
"
=
"
"
:
"
)
    
sections
=
[
]
    
if
isinstance
(
fp
str
)
:
        
filename
=
fp
        
fp
=
io
.
open
(
fp
encoding
=
"
utf
-
8
"
)
    
elif
hasattr
(
fp
"
name
"
)
:
        
filename
=
fp
.
name
    
else
:
        
filename
=
"
unknown
"
    
contents
=
fp
.
read
(
)
    
inline_comment_rx
=
re
.
compile
(
r
"
\
s
#
.
*
"
)
    
try
:
        
manifest
=
parse
(
contents
)
    
except
ParseError
as
pe
:
        
raise
IOError
(
f
"
Error
parsing
TOML
manifest
file
{
filename
}
:
{
pe
}
"
)
    
for
section
in
manifest
.
keys
(
)
:
        
current_section
=
{
}
        
for
key
in
manifest
[
section
]
.
keys
(
)
:
            
val
=
manifest
[
section
]
[
key
]
            
if
isinstance
(
val
bool
)
:
                
if
val
:
                    
val
=
"
true
"
                
else
:
                    
val
=
"
false
"
            
elif
isinstance
(
val
Array
)
:
                
new_vals
=
"
"
                
for
v
in
val
:
                    
if
len
(
new_vals
)
>
0
:
                        
new_vals
+
=
os
.
linesep
                    
new_val
=
str
(
v
)
.
strip
(
)
                    
comment_found
=
inline_comment_rx
.
search
(
new_val
)
                    
if
comment_found
:
                        
new_val
=
new_val
[
0
:
comment_found
.
span
(
)
[
0
]
]
                    
if
"
=
"
in
new_val
:
                        
raise
Exception
(
                            
f
"
Should
not
assign
in
{
key
}
condition
for
{
section
}
"
                        
)
                    
new_vals
+
=
new_val
                
val
=
new_vals
            
else
:
                
val
=
str
(
val
)
.
strip
(
)
                
comment_found
=
inline_comment_rx
.
search
(
val
)
                
if
comment_found
:
                    
val
=
val
[
0
:
comment_found
.
span
(
)
[
0
]
]
                
if
"
=
"
in
val
:
                    
raise
Exception
(
                        
f
"
Should
not
assign
in
{
key
}
condition
for
{
section
}
"
                    
)
            
current_section
[
key
]
=
val
        
if
section
.
lower
(
)
=
=
default
.
lower
(
)
:
            
default_section
=
current_section
        
else
:
            
sections
.
append
(
(
section
current_section
)
)
    
defaults
=
combine_fields
(
defaults
default_section
)
    
if
handle_defaults
:
        
sections
=
[
(
i
combine_fields
(
defaults
j
)
)
for
i
j
in
sections
]
    
return
sections
defaults
