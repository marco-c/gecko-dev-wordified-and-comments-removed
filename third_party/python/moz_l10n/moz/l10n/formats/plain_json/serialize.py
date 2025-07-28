from
__future__
import
annotations
from
collections
import
defaultdict
from
collections
.
abc
import
Iterator
from
json
import
dumps
from
typing
import
Any
from
.
.
.
model
import
Entry
Message
PatternMessage
Resource
def
plain_json_serialize
(
    
resource
:
Resource
[
str
]
|
Resource
[
Message
]
    
trim_comments
:
bool
=
False
)
-
>
Iterator
[
str
]
:
    
"
"
"
    
Serialize
a
resource
as
a
nested
JSON
object
.
    
Comments
and
metadata
are
not
supported
.
    
Yields
the
entire
JSON
result
as
a
single
string
.
    
"
"
"
    
def
check
(
comment
:
str
|
None
meta
:
Any
)
-
>
None
:
        
if
trim_comments
:
            
return
        
if
comment
:
            
raise
ValueError
(
"
Resource
and
section
comments
are
not
supported
"
)
        
if
meta
:
            
raise
ValueError
(
"
Metadata
is
not
supported
"
)
    
def
ddict
(
)
-
>
dict
[
str
Any
]
:
        
return
defaultdict
(
ddict
)
    
check
(
resource
.
comment
resource
.
meta
)
    
root
=
ddict
(
)
    
for
section
in
resource
.
sections
:
        
check
(
section
.
comment
section
.
meta
)
        
section_parent
=
root
        
for
part
in
section
.
id
:
            
section_parent
=
section_parent
[
part
]
        
for
entry
in
section
.
entries
:
            
if
isinstance
(
entry
Entry
)
:
                
check
(
entry
.
comment
entry
.
meta
)
                
if
not
entry
.
id
:
                    
raise
ValueError
(
f
"
Unsupported
empty
identifier
in
{
section
.
id
}
"
)
                
msg
=
entry
.
value
                
if
isinstance
(
msg
str
)
:
                    
value
=
msg
                
elif
isinstance
(
msg
PatternMessage
)
and
all
(
                    
isinstance
(
p
str
)
for
p
in
msg
.
pattern
                
)
:
                    
value
=
"
"
.
join
(
msg
.
pattern
)
                
else
:
                    
raise
ValueError
(
                        
f
"
Unsupported
message
for
{
section
.
id
+
entry
.
id
}
:
{
msg
}
"
                    
)
                
parent
=
section_parent
                
for
part
in
entry
.
id
[
:
-
1
]
:
                    
parent
=
parent
[
part
]
                
parent
[
entry
.
id
[
-
1
]
]
=
value
            
else
:
                
check
(
entry
.
comment
None
)
    
yield
dumps
(
root
indent
=
2
ensure_ascii
=
False
)
    
yield
"
\
n
"
