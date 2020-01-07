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
    
base_str
=
(
str
unicode
)
    
text_type
=
unicode
else
:
    
PY2
=
False
    
PY3
=
True
    
base_str
=
(
bytes
str
)
    
text_type
=
str
