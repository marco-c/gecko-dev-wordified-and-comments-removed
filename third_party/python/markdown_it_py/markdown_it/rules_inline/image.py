from
__future__
import
annotations
from
.
.
common
.
utils
import
isStrSpace
normalizeReference
from
.
.
token
import
Token
from
.
state_inline
import
StateInline
def
image
(
state
:
StateInline
silent
:
bool
)
-
>
bool
:
    
label
=
None
    
href
=
"
"
    
oldPos
=
state
.
pos
    
max
=
state
.
posMax
    
if
state
.
src
[
state
.
pos
]
!
=
"
!
"
:
        
return
False
    
if
state
.
pos
+
1
<
state
.
posMax
and
state
.
src
[
state
.
pos
+
1
]
!
=
"
[
"
:
        
return
False
    
labelStart
=
state
.
pos
+
2
    
labelEnd
=
state
.
md
.
helpers
.
parseLinkLabel
(
state
state
.
pos
+
1
False
)
    
if
labelEnd
<
0
:
        
return
False
    
pos
=
labelEnd
+
1
    
if
pos
<
max
and
state
.
src
[
pos
]
=
=
"
(
"
:
        
pos
+
=
1
        
while
pos
<
max
:
            
ch
=
state
.
src
[
pos
]
            
if
not
isStrSpace
(
ch
)
and
ch
!
=
"
\
n
"
:
                
break
            
pos
+
=
1
        
if
pos
>
=
max
:
            
return
False
        
start
=
pos
        
res
=
state
.
md
.
helpers
.
parseLinkDestination
(
state
.
src
pos
state
.
posMax
)
        
if
res
.
ok
:
            
href
=
state
.
md
.
normalizeLink
(
res
.
str
)
            
if
state
.
md
.
validateLink
(
href
)
:
                
pos
=
res
.
pos
            
else
:
                
href
=
"
"
        
start
=
pos
        
while
pos
<
max
:
            
ch
=
state
.
src
[
pos
]
            
if
not
isStrSpace
(
ch
)
and
ch
!
=
"
\
n
"
:
                
break
            
pos
+
=
1
        
res
=
state
.
md
.
helpers
.
parseLinkTitle
(
state
.
src
pos
state
.
posMax
)
        
if
pos
<
max
and
start
!
=
pos
and
res
.
ok
:
            
title
=
res
.
str
            
pos
=
res
.
pos
            
while
pos
<
max
:
                
ch
=
state
.
src
[
pos
]
                
if
not
isStrSpace
(
ch
)
and
ch
!
=
"
\
n
"
:
                    
break
                
pos
+
=
1
        
else
:
            
title
=
"
"
        
if
pos
>
=
max
or
state
.
src
[
pos
]
!
=
"
)
"
:
            
state
.
pos
=
oldPos
            
return
False
        
pos
+
=
1
    
else
:
        
if
"
references
"
not
in
state
.
env
:
            
return
False
        
if
pos
<
max
and
state
.
src
[
pos
]
=
=
"
[
"
:
            
start
=
pos
+
1
            
pos
=
state
.
md
.
helpers
.
parseLinkLabel
(
state
pos
)
            
if
pos
>
=
0
:
                
label
=
state
.
src
[
start
:
pos
]
                
pos
+
=
1
            
else
:
                
pos
=
labelEnd
+
1
        
else
:
            
pos
=
labelEnd
+
1
        
if
not
label
:
            
label
=
state
.
src
[
labelStart
:
labelEnd
]
        
label
=
normalizeReference
(
label
)
        
ref
=
state
.
env
[
"
references
"
]
.
get
(
label
None
)
        
if
not
ref
:
            
state
.
pos
=
oldPos
            
return
False
        
href
=
ref
[
"
href
"
]
        
title
=
ref
[
"
title
"
]
    
if
not
silent
:
        
content
=
state
.
src
[
labelStart
:
labelEnd
]
        
tokens
:
list
[
Token
]
=
[
]
        
state
.
md
.
inline
.
parse
(
content
state
.
md
state
.
env
tokens
)
        
token
=
state
.
push
(
"
image
"
"
img
"
0
)
        
token
.
attrs
=
{
"
src
"
:
href
"
alt
"
:
"
"
}
        
token
.
children
=
tokens
or
None
        
token
.
content
=
content
        
if
title
:
            
token
.
attrSet
(
"
title
"
title
)
        
if
label
and
state
.
md
.
options
.
get
(
"
store_labels
"
False
)
:
            
token
.
meta
[
"
label
"
]
=
label
    
state
.
pos
=
pos
    
state
.
posMax
=
max
    
return
True
