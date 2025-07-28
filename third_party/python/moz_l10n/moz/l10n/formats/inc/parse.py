from
__future__
import
annotations
from
re
import
compile
from
.
.
.
model
import
Comment
Entry
Message
PatternMessage
Resource
Section
from
.
.
import
Format
re_define
=
compile
(
r
"
#
define
[
\
t
]
+
(
\
w
+
)
(
?
:
[
\
t
]
(
.
*
)
)
?
"
)
def
inc_parse
(
source
:
str
|
bytes
)
-
>
Resource
[
Message
]
:
    
"
"
"
    
Parse
a
.
inc
file
into
a
message
resource
.
    
Directives
such
as
#
filter
and
#
unfilter
will
be
stored
as
standalone
comments
.
    
The
parsed
resource
will
not
include
any
metadata
.
    
"
"
"
    
entries
:
list
[
Entry
[
Message
]
|
Comment
]
=
[
]
    
comment
:
str
=
"
"
    
if
not
isinstance
(
source
str
)
:
        
source
=
str
(
source
"
utf8
"
)
    
for
line
in
source
.
splitlines
(
)
:
        
if
not
line
or
line
.
isspace
(
)
:
            
if
comment
:
                
entries
.
append
(
Comment
(
comment
)
)
                
comment
=
"
"
        
elif
line
.
startswith
(
"
#
"
)
:
            
nc
=
line
[
2
:
]
.
lstrip
(
)
            
if
nc
.
startswith
(
"
#
"
)
:
                
nc
=
line
            
comment
=
f
"
{
comment
}
\
n
{
nc
}
"
if
comment
else
nc
        
else
:
            
match
=
re_define
.
fullmatch
(
line
)
            
if
match
:
                
name
value
=
match
.
groups
(
)
                
entries
.
append
(
                    
Entry
(
                        
(
name
)
                        
PatternMessage
(
[
value
]
if
value
else
[
]
)
                        
comment
=
comment
                    
)
                
)
                
comment
=
"
"
            
elif
line
.
startswith
(
"
#
"
)
:
                
if
comment
:
                    
entries
.
append
(
Comment
(
comment
)
)
                    
comment
=
"
"
                
entries
.
append
(
Comment
(
line
)
)
            
else
:
                
raise
ValueError
(
f
"
Unsupported
content
:
{
line
}
"
)
    
if
comment
:
        
entries
.
append
(
Comment
(
comment
)
)
    
return
Resource
(
Format
.
inc
[
Section
(
(
)
entries
)
]
)
