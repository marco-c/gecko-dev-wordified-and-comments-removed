import
re
import
sys
REVISION_MATCHER
=
re
.
compile
(
r
"
remote
:
.
*
/
try
/
rev
/
(
[
\
w
]
*
)
[
\
t
]
*
"
)
class
LogProcessor
:
    
def
__init__
(
self
)
:
        
self
.
buf
=
"
"
        
self
.
stdout
=
sys
.
__stdout__
        
self
.
_revision
=
None
    
property
    
def
revision
(
self
)
:
        
return
self
.
_revision
    
def
write
(
self
buf
)
:
        
while
buf
:
            
try
:
                
newline_index
=
buf
.
index
(
"
\
n
"
)
            
except
ValueError
:
                
self
.
buf
+
=
buf
                
break
            
data
=
self
.
buf
+
buf
[
:
newline_index
+
1
]
            
buf
=
buf
[
newline_index
+
1
:
]
            
self
.
buf
=
"
"
            
if
data
.
strip
(
)
=
=
"
"
:
                
continue
            
self
.
stdout
.
write
(
data
.
strip
(
"
\
n
"
)
+
"
\
n
"
)
            
match
=
REVISION_MATCHER
.
match
(
data
)
            
if
match
:
                
self
.
_revision
=
match
.
group
(
1
)
