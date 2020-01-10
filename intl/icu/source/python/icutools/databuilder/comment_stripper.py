import
io
class
CommentStripper
(
object
)
:
    
"
"
"
Removes
lines
starting
with
"
/
/
"
from
a
file
stream
.
"
"
"
    
def
__init__
(
self
f
)
:
        
self
.
f
=
f
        
self
.
state
=
0
    
def
read
(
self
size
=
-
1
)
:
        
bytes
=
self
.
f
.
read
(
size
)
        
return
"
"
.
join
(
self
.
_strip_comments
(
bytes
)
)
    
def
_strip_comments
(
self
bytes
)
:
        
for
byte
in
bytes
:
            
if
self
.
state
=
=
0
:
                
if
byte
=
=
"
/
"
:
                    
self
.
state
=
1
                
elif
byte
=
=
"
\
n
"
:
                    
self
.
state
=
0
                    
yield
byte
                
else
:
                    
self
.
state
=
2
                    
yield
byte
            
elif
self
.
state
=
=
1
:
                
if
byte
=
=
"
/
"
:
                    
self
.
state
=
3
                
elif
byte
=
=
"
\
n
"
:
                    
self
.
state
=
0
                    
yield
"
/
"
                    
yield
"
\
n
"
                
else
:
                    
self
.
state
=
2
                    
yield
"
/
"
                    
yield
byte
            
elif
self
.
state
=
=
2
:
                
if
byte
=
=
"
\
n
"
:
                    
self
.
state
=
0
                
yield
byte
            
elif
self
.
state
=
=
3
:
                
if
byte
=
=
"
\
n
"
:
                    
self
.
state
=
0
