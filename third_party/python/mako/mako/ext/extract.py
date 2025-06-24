from
io
import
BytesIO
from
io
import
StringIO
import
re
from
mako
import
lexer
from
mako
import
parsetree
class
MessageExtractor
:
    
use_bytes
=
True
    
def
process_file
(
self
fileobj
)
:
        
template_node
=
lexer
.
Lexer
(
            
fileobj
.
read
(
)
input_encoding
=
self
.
config
[
"
encoding
"
]
        
)
.
parse
(
)
        
yield
from
self
.
extract_nodes
(
template_node
.
get_children
(
)
)
    
def
extract_nodes
(
self
nodes
)
:
        
translator_comments
=
[
]
        
in_translator_comments
=
False
        
input_encoding
=
self
.
config
[
"
encoding
"
]
or
"
ascii
"
        
comment_tags
=
list
(
            
filter
(
None
re
.
split
(
r
"
\
s
+
"
self
.
config
[
"
comment
-
tags
"
]
)
)
        
)
        
for
node
in
nodes
:
            
child_nodes
=
None
            
if
(
                
in_translator_comments
                
and
isinstance
(
node
parsetree
.
Text
)
                
and
not
node
.
content
.
strip
(
)
            
)
:
                
continue
            
if
isinstance
(
node
parsetree
.
Comment
)
:
                
value
=
node
.
text
.
strip
(
)
                
if
in_translator_comments
:
                    
translator_comments
.
extend
(
                        
self
.
_split_comment
(
node
.
lineno
value
)
                    
)
                    
continue
                
for
comment_tag
in
comment_tags
:
                    
if
value
.
startswith
(
comment_tag
)
:
                        
in_translator_comments
=
True
                        
translator_comments
.
extend
(
                            
self
.
_split_comment
(
node
.
lineno
value
)
                        
)
                
continue
            
if
isinstance
(
node
parsetree
.
DefTag
)
:
                
code
=
node
.
function_decl
.
code
                
child_nodes
=
node
.
nodes
            
elif
isinstance
(
node
parsetree
.
BlockTag
)
:
                
code
=
node
.
body_decl
.
code
                
child_nodes
=
node
.
nodes
            
elif
isinstance
(
node
parsetree
.
CallTag
)
:
                
code
=
node
.
code
.
code
                
child_nodes
=
node
.
nodes
            
elif
isinstance
(
node
parsetree
.
PageTag
)
:
                
code
=
node
.
body_decl
.
code
            
elif
isinstance
(
node
parsetree
.
CallNamespaceTag
)
:
                
code
=
node
.
expression
                
child_nodes
=
node
.
nodes
            
elif
isinstance
(
node
parsetree
.
ControlLine
)
:
                
if
node
.
isend
:
                    
in_translator_comments
=
False
                    
continue
                
code
=
node
.
text
            
elif
isinstance
(
node
parsetree
.
Code
)
:
                
in_translator_comments
=
False
                
code
=
node
.
code
.
code
            
elif
isinstance
(
node
parsetree
.
Expression
)
:
                
code
=
node
.
code
.
code
            
else
:
                
continue
            
if
(
                
translator_comments
                
and
translator_comments
[
-
1
]
[
0
]
<
node
.
lineno
-
1
            
)
:
                
translator_comments
=
[
]
            
translator_strings
=
[
                
comment
[
1
]
for
comment
in
translator_comments
            
]
            
if
isinstance
(
code
str
)
and
self
.
use_bytes
:
                
code
=
code
.
encode
(
input_encoding
"
backslashreplace
"
)
            
used_translator_comments
=
False
            
if
self
.
use_bytes
:
                
code
=
BytesIO
(
b
"
\
n
"
+
code
)
            
else
:
                
code
=
StringIO
(
"
\
n
"
+
code
)
            
for
message
in
self
.
process_python
(
                
code
node
.
lineno
-
1
translator_strings
            
)
:
                
yield
message
                
used_translator_comments
=
True
            
if
used_translator_comments
:
                
translator_comments
=
[
]
            
in_translator_comments
=
False
            
if
child_nodes
:
                
yield
from
self
.
extract_nodes
(
child_nodes
)
    
staticmethod
    
def
_split_comment
(
lineno
comment
)
:
        
"
"
"
Return
the
multiline
comment
at
lineno
split
into
a
list
of
        
comment
line
numbers
and
the
accompanying
comment
line
"
"
"
        
return
[
            
(
lineno
+
index
line
)
            
for
index
line
in
enumerate
(
comment
.
splitlines
(
)
)
        
]
