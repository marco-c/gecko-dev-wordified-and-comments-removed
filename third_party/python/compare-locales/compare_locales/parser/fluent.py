from
__future__
import
absolute_import
from
__future__
import
unicode_literals
import
re
from
fluent
.
syntax
import
FluentParser
as
FTLParser
from
fluent
.
syntax
import
ast
as
ftl
from
.
base
import
(
    
CAN_SKIP
    
EntityBase
Entity
Comment
Junk
Whitespace
    
Parser
)
class
FluentAttribute
(
EntityBase
)
:
    
ignored_fields
=
[
'
span
'
]
    
def
__init__
(
self
entity
attr_node
)
:
        
self
.
ctx
=
entity
.
ctx
        
self
.
attr
=
attr_node
        
self
.
key_span
=
(
attr_node
.
id
.
span
.
start
attr_node
.
id
.
span
.
end
)
        
self
.
val_span
=
(
attr_node
.
value
.
span
.
start
attr_node
.
value
.
span
.
end
)
    
def
equals
(
self
other
)
:
        
if
not
isinstance
(
other
FluentAttribute
)
:
            
return
False
        
return
self
.
attr
.
equals
(
            
other
.
attr
ignored_fields
=
self
.
ignored_fields
)
class
FluentEntity
(
Entity
)
:
    
ignored_fields
=
[
'
comment
'
'
span
'
]
    
def
__init__
(
self
ctx
entry
)
:
        
start
=
entry
.
span
.
start
        
end
=
entry
.
span
.
end
        
self
.
ctx
=
ctx
        
self
.
span
=
(
start
end
)
        
self
.
key_span
=
(
entry
.
id
.
span
.
start
entry
.
id
.
span
.
end
)
        
if
entry
.
value
is
not
None
:
            
self
.
val_span
=
(
entry
.
value
.
span
.
start
entry
.
value
.
span
.
end
)
        
else
:
            
self
.
val_span
=
None
        
self
.
entry
=
entry
        
self
.
pre_comment
=
None
    
property
    
def
root_node
(
self
)
:
        
'
'
'
AST
node
at
which
to
start
traversal
for
count_words
.
        
By
default
we
count
words
in
the
value
and
in
all
attributes
.
        
'
'
'
        
return
self
.
entry
    
_word_count
=
None
    
def
count_words
(
self
)
:
        
if
self
.
_word_count
is
None
:
            
self
.
_word_count
=
0
            
def
count_words
(
node
)
:
                
if
isinstance
(
node
ftl
.
TextElement
)
:
                    
self
.
_word_count
+
=
len
(
node
.
value
.
split
(
)
)
                
return
node
            
self
.
root_node
.
traverse
(
count_words
)
        
return
self
.
_word_count
    
def
equals
(
self
other
)
:
        
return
self
.
entry
.
equals
(
            
other
.
entry
ignored_fields
=
self
.
ignored_fields
)
    
def
value_position
(
self
offset
=
0
)
:
        
return
self
.
position
(
offset
)
    
property
    
def
attributes
(
self
)
:
        
for
attr_node
in
self
.
entry
.
attributes
:
            
yield
FluentAttribute
(
self
attr_node
)
class
FluentMessage
(
FluentEntity
)
:
    
pass
class
FluentTerm
(
FluentEntity
)
:
    
ignored_fields
=
[
'
attributes
'
'
comment
'
'
span
'
]
    
property
    
def
root_node
(
self
)
:
        
'
'
'
AST
node
at
which
to
start
traversal
for
count_words
.
        
In
Fluent
Terms
we
only
count
words
in
the
value
.
Attributes
are
        
private
and
do
not
count
towards
the
word
total
.
        
'
'
'
        
return
self
.
entry
.
value
class
FluentComment
(
Comment
)
:
    
def
__init__
(
self
ctx
span
entry
)
:
        
super
(
FluentComment
self
)
.
__init__
(
ctx
span
)
        
self
.
_val_cache
=
entry
.
content
class
FluentParser
(
Parser
)
:
    
capabilities
=
CAN_SKIP
    
def
__init__
(
self
)
:
        
super
(
FluentParser
self
)
.
__init__
(
)
        
self
.
ftl_parser
=
FTLParser
(
)
    
def
walk
(
self
only_localizable
=
False
)
:
        
if
not
self
.
ctx
:
            
return
        
resource
=
self
.
ftl_parser
.
parse
(
self
.
ctx
.
contents
)
        
last_span_end
=
0
        
for
entry
in
resource
.
body
:
            
if
not
only_localizable
:
                
if
entry
.
span
.
start
>
last_span_end
:
                    
yield
Whitespace
(
                        
self
.
ctx
(
last_span_end
entry
.
span
.
start
)
)
            
if
isinstance
(
entry
ftl
.
Message
)
:
                
yield
FluentMessage
(
self
.
ctx
entry
)
            
elif
isinstance
(
entry
ftl
.
Term
)
:
                
yield
FluentTerm
(
self
.
ctx
entry
)
            
elif
isinstance
(
entry
ftl
.
Junk
)
:
                
start
=
entry
.
span
.
start
                
end
=
entry
.
span
.
end
                
start
+
=
re
.
match
(
'
[
\
t
\
r
\
n
]
*
'
entry
.
content
)
.
end
(
)
                
ws
we
=
re
.
search
(
'
[
\
t
\
r
\
n
]
*
'
entry
.
content
)
.
span
(
)
                
end
-
=
we
-
ws
                
yield
Junk
(
self
.
ctx
(
start
end
)
)
            
elif
isinstance
(
entry
ftl
.
BaseComment
)
and
not
only_localizable
:
                
span
=
(
entry
.
span
.
start
entry
.
span
.
end
)
                
yield
FluentComment
(
self
.
ctx
span
entry
)
            
last_span_end
=
entry
.
span
.
end
        
if
not
only_localizable
:
            
eof_offset
=
len
(
self
.
ctx
.
contents
)
            
if
eof_offset
>
last_span_end
:
                
yield
Whitespace
(
self
.
ctx
(
last_span_end
eof_offset
)
)
