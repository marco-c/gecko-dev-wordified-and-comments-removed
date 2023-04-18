def
assert_browsing_context
(
info
children
context
url
parent
=
None
)
:
    
assert
"
children
"
in
info
    
if
children
is
not
None
:
        
assert
isinstance
(
info
[
"
children
"
]
list
)
    
assert
info
[
"
children
"
]
=
=
children
    
assert
"
context
"
in
info
    
assert
isinstance
(
info
[
"
context
"
]
str
)
    
if
context
is
not
None
:
        
assert
info
[
"
context
"
]
=
=
context
    
assert
"
parent
"
in
info
    
if
children
is
not
None
:
        
assert
isinstance
(
info
[
"
parent
"
]
str
)
    
assert
info
[
"
parent
"
]
=
=
parent
    
assert
"
url
"
in
info
    
assert
isinstance
(
info
[
"
url
"
]
str
)
    
assert
info
[
"
url
"
]
=
=
url
