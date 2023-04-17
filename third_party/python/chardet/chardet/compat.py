import
sys
if
sys
.
version_info
<
(
3
0
)
:
    
PY2
=
True
    
PY3
=
False
    
string_types
=
(
str
unicode
)
    
text_type
=
unicode
    
iteritems
=
dict
.
iteritems
else
:
    
PY2
=
False
    
PY3
=
True
    
string_types
=
(
bytes
str
)
    
text_type
=
str
    
iteritems
=
dict
.
items
