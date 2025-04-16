import
re
class
StringVersion
(
str
)
:
    
"
"
"
    
A
string
version
that
can
be
compared
with
comparison
operators
.
    
"
"
"
    
pat
=
re
.
compile
(
r
"
(
\
d
+
)
|
(
[
^
\
d
.
]
+
)
"
)
    
def
__init__
(
self
vstring
)
:
        
super
(
StringVersion
self
)
.
__init__
(
)
        
if
isinstance
(
vstring
bytes
)
:
            
vstring
=
vstring
.
decode
(
"
ascii
"
)
        
self
.
vstring
=
vstring
        
self
.
version
=
[
]
        
parts
=
self
.
pat
.
findall
(
vstring
)
        
for
i
obj
in
enumerate
(
parts
)
:
            
if
obj
[
0
]
:
                
self
.
version
.
append
(
obj
[
0
]
.
zfill
(
8
)
)
            
else
:
                
self
.
version
.
append
(
obj
[
1
]
)
    
def
__str__
(
self
)
:
        
return
self
.
vstring
    
def
__repr__
(
self
)
:
        
return
"
StringVersion
(
'
%
s
'
)
"
%
str
(
self
)
    
def
_cmp
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
StringVersion
)
:
            
other
=
StringVersion
(
other
)
        
if
self
.
version
=
=
other
.
version
:
            
return
0
        
if
self
.
version
<
other
.
version
:
            
return
-
1
        
if
self
.
version
>
other
.
version
:
            
return
1
    
def
__hash__
(
self
)
:
        
return
hash
(
self
.
version
)
    
def
__eq__
(
self
other
)
:
        
return
self
.
_cmp
(
other
)
=
=
0
    
def
__lt__
(
self
other
)
:
        
return
self
.
_cmp
(
other
)
<
0
    
def
__le__
(
self
other
)
:
        
return
self
.
_cmp
(
other
)
<
=
0
    
def
__gt__
(
self
other
)
:
        
return
self
.
_cmp
(
other
)
>
0
    
def
__ge__
(
self
other
)
:
        
return
self
.
_cmp
(
other
)
>
=
0
