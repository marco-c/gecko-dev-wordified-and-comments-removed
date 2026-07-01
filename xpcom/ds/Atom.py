class
Atom
:
    
def
__init__
(
self
ident
string
)
:
        
self
.
ident
=
ident
        
self
.
string
=
string
        
self
.
hash
=
hash_string
(
string
)
        
self
.
is_ascii_lowercase
=
is_ascii_lowercase
(
string
)
GOLDEN_RATIO_U32
=
0x9E3779B9
def
rotate_left_5
(
value
)
:
    
return
(
(
value
<
<
5
)
|
(
value
>
>
27
)
)
&
0xFFFFFFFF
def
wrapping_multiply
(
x
y
)
:
    
return
(
x
*
y
)
&
0xFFFFFFFF
def
hash_string
(
s
)
:
    
h
=
0
    
for
c
in
s
:
        
h
=
wrapping_multiply
(
GOLDEN_RATIO_U32
rotate_left_5
(
h
)
^
ord
(
c
)
)
    
return
h
def
is_ascii_lowercase
(
s
)
:
    
for
c
in
s
:
        
if
c
>
=
"
A
"
and
c
<
=
"
Z
"
:
            
return
False
    
return
True
