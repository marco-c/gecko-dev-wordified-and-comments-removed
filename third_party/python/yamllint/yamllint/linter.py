import
io
import
re
import
yaml
from
yamllint
import
decoder
parser
PROBLEM_LEVELS
=
{
    
0
:
None
    
1
:
'
warning
'
    
2
:
'
error
'
    
None
:
0
    
'
warning
'
:
1
    
'
error
'
:
2
}
DISABLE_RULE_PATTERN
=
re
.
compile
(
r
'
^
#
yamllint
disable
(
rule
:
\
S
+
)
*
\
s
*
'
)
ENABLE_RULE_PATTERN
=
re
.
compile
(
r
'
^
#
yamllint
enable
(
rule
:
\
S
+
)
*
\
s
*
'
)
class
LintProblem
:
    
"
"
"
Represents
a
linting
problem
found
by
yamllint
.
"
"
"
    
def
__init__
(
self
line
column
desc
=
'
<
no
description
>
'
rule
=
None
)
:
        
self
.
line
=
line
        
self
.
column
=
column
        
self
.
desc
=
desc
        
self
.
rule
=
rule
        
self
.
level
=
None
    
property
    
def
message
(
self
)
:
        
if
self
.
rule
is
not
None
:
            
return
f
'
{
self
.
desc
}
(
{
self
.
rule
}
)
'
        
return
self
.
desc
    
def
__eq__
(
self
other
)
:
        
return
(
self
.
line
=
=
other
.
line
and
                
self
.
column
=
=
other
.
column
and
                
self
.
rule
=
=
other
.
rule
)
    
def
__lt__
(
self
other
)
:
        
return
(
self
.
line
<
other
.
line
or
                
(
self
.
line
=
=
other
.
line
and
self
.
column
<
other
.
column
)
)
    
def
__repr__
(
self
)
:
        
return
f
'
{
self
.
line
}
:
{
self
.
column
}
:
{
self
.
message
}
'
def
get_cosmetic_problems
(
buffer
conf
filepath
)
:
    
rules
=
conf
.
enabled_rules
(
filepath
)
    
token_rules
=
[
r
for
r
in
rules
if
r
.
TYPE
=
=
'
token
'
]
    
comment_rules
=
[
r
for
r
in
rules
if
r
.
TYPE
=
=
'
comment
'
]
    
line_rules
=
[
r
for
r
in
rules
if
r
.
TYPE
=
=
'
line
'
]
    
context
=
{
}
    
for
rule
in
token_rules
:
        
context
[
rule
.
ID
]
=
{
}
    
class
DisableDirective
:
        
def
__init__
(
self
)
:
            
self
.
rules
=
set
(
)
            
self
.
all_rules
=
{
r
.
ID
for
r
in
rules
}
        
def
process_comment
(
self
comment
)
:
            
comment
=
str
(
comment
)
            
if
DISABLE_RULE_PATTERN
.
match
(
comment
)
:
                
items
=
comment
[
18
:
]
.
rstrip
(
)
.
split
(
'
'
)
                
rules
=
[
item
[
5
:
]
for
item
in
items
]
[
1
:
]
                
if
len
(
rules
)
=
=
0
:
                    
self
.
rules
=
self
.
all_rules
.
copy
(
)
                
else
:
                    
for
id
in
rules
:
                        
if
id
in
self
.
all_rules
:
                            
self
.
rules
.
add
(
id
)
            
elif
ENABLE_RULE_PATTERN
.
match
(
comment
)
:
                
items
=
comment
[
17
:
]
.
rstrip
(
)
.
split
(
'
'
)
                
rules
=
[
item
[
5
:
]
for
item
in
items
]
[
1
:
]
                
if
len
(
rules
)
=
=
0
:
                    
self
.
rules
.
clear
(
)
                
else
:
                    
for
id
in
rules
:
                        
self
.
rules
.
discard
(
id
)
        
def
is_disabled_by_directive
(
self
problem
)
:
            
return
problem
.
rule
in
self
.
rules
    
class
DisableLineDirective
(
DisableDirective
)
:
        
def
process_comment
(
self
comment
)
:
            
comment
=
str
(
comment
)
            
if
re
.
match
(
r
'
^
#
yamllint
disable
-
line
(
rule
:
\
S
+
)
*
\
s
*
'
comment
)
:
                
items
=
comment
[
23
:
]
.
rstrip
(
)
.
split
(
'
'
)
                
rules
=
[
item
[
5
:
]
for
item
in
items
]
[
1
:
]
                
if
len
(
rules
)
=
=
0
:
                    
self
.
rules
=
self
.
all_rules
.
copy
(
)
                
else
:
                    
for
id
in
rules
:
                        
if
id
in
self
.
all_rules
:
                            
self
.
rules
.
add
(
id
)
    
cache
=
[
]
    
disabled
=
DisableDirective
(
)
    
disabled_for_line
=
DisableLineDirective
(
)
    
disabled_for_next_line
=
DisableLineDirective
(
)
    
for
elem
in
parser
.
token_or_comment_or_line_generator
(
buffer
)
:
        
if
isinstance
(
elem
parser
.
Token
)
:
            
for
rule
in
token_rules
:
                
rule_conf
=
conf
.
rules
[
rule
.
ID
]
                
for
problem
in
rule
.
check
(
rule_conf
                                          
elem
.
curr
elem
.
prev
elem
.
next
                                          
elem
.
nextnext
                                          
context
[
rule
.
ID
]
)
:
                    
problem
.
rule
=
rule
.
ID
                    
problem
.
level
=
rule_conf
[
'
level
'
]
                    
cache
.
append
(
problem
)
        
elif
isinstance
(
elem
parser
.
Comment
)
:
            
for
rule
in
comment_rules
:
                
rule_conf
=
conf
.
rules
[
rule
.
ID
]
                
for
problem
in
rule
.
check
(
rule_conf
elem
)
:
                    
problem
.
rule
=
rule
.
ID
                    
problem
.
level
=
rule_conf
[
'
level
'
]
                    
cache
.
append
(
problem
)
            
disabled
.
process_comment
(
elem
)
            
if
elem
.
is_inline
(
)
:
                
disabled_for_line
.
process_comment
(
elem
)
            
else
:
                
disabled_for_next_line
.
process_comment
(
elem
)
        
elif
isinstance
(
elem
parser
.
Line
)
:
            
for
rule
in
line_rules
:
                
rule_conf
=
conf
.
rules
[
rule
.
ID
]
                
for
problem
in
rule
.
check
(
rule_conf
elem
)
:
                    
problem
.
rule
=
rule
.
ID
                    
problem
.
level
=
rule_conf
[
'
level
'
]
                    
cache
.
append
(
problem
)
            
for
problem
in
cache
:
                
if
not
(
disabled_for_line
.
is_disabled_by_directive
(
problem
)
or
                        
disabled
.
is_disabled_by_directive
(
problem
)
)
:
                    
yield
problem
            
disabled_for_line
=
disabled_for_next_line
            
disabled_for_next_line
=
DisableLineDirective
(
)
            
cache
=
[
]
def
get_syntax_error
(
buffer
)
:
    
try
:
        
list
(
yaml
.
parse
(
buffer
Loader
=
yaml
.
BaseLoader
)
)
    
except
yaml
.
error
.
MarkedYAMLError
as
e
:
        
problem
=
LintProblem
(
e
.
problem_mark
.
line
+
1
                              
e
.
problem_mark
.
column
+
1
                              
'
syntax
error
:
'
+
e
.
problem
+
'
(
syntax
)
'
)
        
problem
.
level
=
'
error
'
        
return
problem
def
_run
(
buffer
conf
filepath
)
:
    
assert
hasattr
(
buffer
'
__getitem__
'
)
\
        
'
_run
(
)
argument
must
be
a
buffer
not
a
stream
'
    
if
isinstance
(
buffer
bytes
)
:
        
buffer
=
decoder
.
auto_decode
(
buffer
)
    
first_line
=
next
(
parser
.
line_generator
(
buffer
)
)
.
content
    
if
re
.
match
(
r
'
^
#
\
s
*
yamllint
disable
-
file
\
s
*
'
first_line
)
:
        
return
    
syntax_error
=
get_syntax_error
(
buffer
)
    
for
problem
in
get_cosmetic_problems
(
buffer
conf
filepath
)
:
        
if
(
syntax_error
and
syntax_error
.
line
<
=
problem
.
line
and
                
syntax_error
.
column
<
=
problem
.
column
)
:
            
yield
syntax_error
            
syntax_error
=
None
            
continue
        
yield
problem
    
if
syntax_error
:
        
yield
syntax_error
def
run
(
input
conf
filepath
=
None
)
:
    
"
"
"
Lints
a
YAML
source
.
    
Returns
a
generator
of
LintProblem
objects
.
    
:
param
input
:
buffer
string
or
stream
to
read
from
    
:
param
conf
:
yamllint
configuration
object
    
"
"
"
    
if
filepath
is
not
None
and
conf
.
is_file_ignored
(
filepath
)
:
        
return
(
)
    
if
isinstance
(
input
(
bytes
str
)
)
:
        
return
_run
(
input
conf
filepath
)
    
elif
isinstance
(
input
io
.
IOBase
)
:
        
content
=
input
.
read
(
)
        
return
_run
(
content
conf
filepath
)
    
else
:
        
raise
TypeError
(
'
input
should
be
a
string
or
a
stream
'
)
