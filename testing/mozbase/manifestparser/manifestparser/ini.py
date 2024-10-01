import
io
import
os
import
sys
__all__
=
[
"
read_ini
"
"
combine_fields
"
]
class
IniParseError
(
Exception
)
:
    
def
__init__
(
self
fp
linenum
msg
)
:
        
if
isinstance
(
fp
str
)
:
            
path
=
fp
        
elif
hasattr
(
fp
"
name
"
)
:
            
path
=
fp
.
name
        
else
:
            
path
=
getattr
(
fp
"
path
"
"
unknown
"
)
        
msg
=
"
Error
parsing
manifest
file
'
{
}
'
line
{
}
:
{
}
"
.
format
(
path
linenum
msg
)
        
super
(
IniParseError
self
)
.
__init__
(
msg
)
def
read_ini
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
    
document
=
False
    
add_line_no
=
False
)
:
    
"
"
"
    
read
an
.
ini
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
    
-
add_line_no
:
whether
to
include
the
line
number
that
points
to
the
test
in
the
generated
ini
file
.
    
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
    
key
=
value
=
None
    
section_names
=
set
(
)
    
if
isinstance
(
fp
str
)
:
        
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
    
section
=
default
    
current_section
=
{
}
    
current_section_name
=
"
"
    
key_indent
=
0
    
for
linenum
line
in
enumerate
(
fp
.
read
(
)
.
splitlines
(
)
start
=
1
)
:
        
stripped
=
line
.
strip
(
)
        
if
not
stripped
:
            
key
=
value
=
None
            
continue
        
if
any
(
stripped
.
startswith
(
c
)
for
c
in
comments
)
:
            
continue
        
comment_start
=
sys
.
maxsize
        
inline_prefixes
=
{
p
:
-
1
for
p
in
comments
}
        
while
comment_start
=
=
sys
.
maxsize
and
inline_prefixes
:
            
next_prefixes
=
{
}
            
for
prefix
i
in
inline_prefixes
.
items
(
)
:
                
index
=
stripped
.
find
(
prefix
i
+
1
)
                
if
index
=
=
-
1
:
                    
continue
                
next_prefixes
[
prefix
]
=
index
                
if
index
=
=
0
or
(
index
>
0
and
stripped
[
index
-
1
]
.
isspace
(
)
)
:
                    
comment_start
=
min
(
comment_start
index
)
            
inline_prefixes
=
next_prefixes
        
if
comment_start
!
=
sys
.
maxsize
:
            
stripped
=
stripped
[
:
comment_start
]
.
rstrip
(
)
        
if
len
(
stripped
)
>
2
and
stripped
[
0
]
=
=
"
[
"
and
stripped
[
-
1
]
=
=
"
]
"
:
            
section
=
stripped
[
1
:
-
1
]
.
strip
(
)
            
key
=
value
=
None
            
key_indent
=
0
            
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
                
if
strict
:
                    
assert
default
not
in
section_names
                
section_names
.
add
(
default
)
                
current_section
=
default_section
                
current_section_name
=
"
DEFAULT
"
                
continue
            
if
strict
:
                
assert
(
                    
section
not
in
section_names
                
)
"
Section
'
%
s
'
already
found
in
'
%
s
'
"
%
(
section
section_names
)
            
section_names
.
add
(
section
)
            
current_section
=
{
}
            
current_section_name
=
section
            
sections
.
append
(
(
section
current_section
)
)
            
continue
        
if
not
section_names
:
            
raise
IniParseError
(
                
fp
                
linenum
                
"
Expected
a
comment
or
section
"
"
instead
found
'
{
}
'
"
.
format
(
stripped
)
            
)
        
line_indent
=
len
(
line
)
-
len
(
line
.
lstrip
(
"
"
)
)
        
if
key
and
line_indent
>
key_indent
:
            
value
=
"
%
s
%
s
%
s
"
%
(
value
os
.
linesep
stripped
)
            
if
strict
:
                
if
"
=
"
in
value
:
                    
raise
IniParseError
(
                        
fp
                        
linenum
                        
"
Should
not
assign
in
{
}
condition
for
{
}
"
.
format
(
                            
key
current_section_name
                        
)
                    
)
            
current_section
[
key
]
=
value
            
continue
        
for
separator
in
separators
:
            
if
separator
in
stripped
:
                
key
value
=
stripped
.
split
(
separator
1
)
                
key
=
key
.
strip
(
)
                
value
=
value
.
strip
(
)
                
key_indent
=
line_indent
                
if
key
:
                    
assert
(
                        
key
not
in
current_section
                    
)
f
"
Found
duplicate
key
{
key
}
in
section
{
section
}
"
                
if
strict
:
                    
assert
key
                    
if
"
=
"
in
value
:
                        
raise
IniParseError
(
                            
fp
                            
linenum
                            
"
Should
not
assign
in
{
}
condition
for
{
}
"
.
format
(
                                
key
current_section_name
                            
)
                        
)
                
current_section
[
key
]
=
value
                
break
        
else
:
            
raise
IniParseError
(
fp
linenum
"
Unexpected
line
'
{
}
'
"
.
format
(
stripped
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
None
def
combine_fields
(
global_vars
local_vars
)
:
    
"
"
"
    
Combine
the
given
manifest
entries
according
to
the
semantics
of
specific
fields
.
    
This
is
used
to
combine
manifest
level
defaults
with
a
per
-
test
definition
.
    
"
"
"
    
if
not
global_vars
:
        
return
local_vars
    
if
not
local_vars
:
        
return
global_vars
.
copy
(
)
    
field_patterns
=
{
        
"
args
"
:
"
%
s
%
s
"
        
"
prefs
"
:
"
%
s
%
s
"
        
"
skip
-
if
"
:
"
%
s
\
n
%
s
"
        
"
support
-
files
"
:
"
%
s
%
s
"
        
"
tags
"
:
"
%
s
%
s
"
    
}
    
final_mapping
=
global_vars
.
copy
(
)
    
for
field_name
value
in
local_vars
.
items
(
)
:
        
if
field_name
not
in
field_patterns
or
field_name
not
in
global_vars
:
            
final_mapping
[
field_name
]
=
value
            
continue
        
global_value
=
global_vars
[
field_name
]
        
pattern
=
field_patterns
[
field_name
]
        
final_mapping
[
field_name
]
=
pattern
%
(
global_value
value
)
    
return
final_mapping
