import
re
from
docutils
.
nodes
import
Text
paragraph
reference
from
sphinx
.
transforms
import
SphinxTransform
class
ConvertBugsToLinks
(
SphinxTransform
)
:
    
default_priority
=
400
    
bz_url
=
"
https
:
/
/
bugzilla
.
mozilla
.
org
/
show_bug
.
cgi
?
id
=
{
0
}
"
    
bz_reg
=
r
"
bug
[
'
'
]
[
0
-
9
]
\
d
*
"
    
def
apply
(
self
)
:
        
def
check_if_paragraph
(
o
)
:
            
return
isinstance
(
o
paragraph
)
        
def
check_if_text
(
o
)
:
            
return
(
                
not
isinstance
(
o
.
parent
reference
)
                
and
isinstance
(
o
Text
)
                
and
re
.
search
(
self
.
bz_reg
o
re
.
IGNORECASE
)
            
)
        
changed
=
True
        
while
changed
:
            
changed
=
self
.
textToReferences
(
check_if_paragraph
check_if_text
)
    
def
textToReferences
(
self
check_if_paragraph
check_if_text
)
:
        
for
node
in
self
.
document
.
traverse
(
check_if_paragraph
)
:
            
for
text
in
node
.
traverse
(
check_if_text
)
:
                
bugs
=
re
.
findall
(
self
.
bz_reg
text
re
.
IGNORECASE
)
                
if
len
(
bugs
)
=
=
0
:
                    
continue
                
bug
=
bugs
[
0
]
                
txtparts
=
text
.
split
(
bug
1
)
                
new_ref
=
reference
(
                    
bug
                    
bug
                    
refuri
=
self
.
bz_url
.
format
(
bug
.
split
(
)
[
1
]
)
                
)
                
txt_0
=
Text
(
txtparts
[
0
]
)
                
txt_1
=
Text
(
txtparts
[
1
]
)
                
text
.
parent
.
replace
(
text
[
txt_0
new_ref
txt_1
]
)
                
if
len
(
bugs
)
>
1
:
                    
return
True
        
return
False
def
setup
(
app
)
:
    
app
.
add_transform
(
ConvertBugsToLinks
)
