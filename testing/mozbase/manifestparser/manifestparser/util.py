import
ast
import
os
def
normsep
(
path
)
:
    
"
"
"
    
Normalize
path
separators
by
using
forward
slashes
instead
of
whatever
    
:
py
:
const
:
os
.
sep
is
.
    
"
"
"
    
if
os
.
sep
!
=
"
/
"
:
        
if
isinstance
(
path
bytes
)
:
            
path
=
path
.
replace
(
os
.
sep
.
encode
(
"
ascii
"
)
b
"
/
"
)
        
else
:
            
path
=
path
.
replace
(
os
.
sep
"
/
"
)
    
if
os
.
altsep
and
os
.
altsep
!
=
"
/
"
:
        
if
isinstance
(
path
bytes
)
:
            
path
=
path
.
replace
(
os
.
altsep
.
encode
(
"
ascii
"
)
b
"
/
"
)
        
else
:
            
path
=
path
.
replace
(
os
.
altsep
"
/
"
)
    
return
path
def
evaluate_list_from_string
(
list_string
)
:
    
"
"
"
    
This
is
a
utility
function
for
converting
a
string
obtained
from
a
manifest
    
into
a
list
.
If
the
string
is
not
a
valid
list
when
converted
an
error
will
be
    
raised
from
ast
.
eval_literal
.
For
example
you
can
convert
entries
like
this
    
into
a
list
:
    
        
test_settings
=
            
[
"
hello
"
"
world
"
]
            
[
1
10
100
]
        
values
=
            
5
            
6
            
7
            
8
    
    
"
"
"
    
parts
=
[
        
x
.
strip
(
"
"
)
        
for
x
in
list_string
.
strip
(
"
"
)
.
replace
(
"
\
r
"
"
"
)
.
split
(
"
\
n
"
)
        
if
x
.
strip
(
)
    
]
    
return
ast
.
literal_eval
(
"
[
"
+
"
"
.
join
(
parts
)
+
"
]
"
)
