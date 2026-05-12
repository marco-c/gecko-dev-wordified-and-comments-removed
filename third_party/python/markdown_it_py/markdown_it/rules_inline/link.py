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
state_inline
import
StateInline
def
link
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
    
href
=
"
"
    
title
=
"
"
    
label
=
None
    
oldPos
=
state
.
pos
    
maximum
=
state
.
posMax
    
start
=
state
.
pos
    
parseReference
=
True
    
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
1
    
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
True
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
maximum
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
        
parseReference
=
False
        
pos
+
=
1
        
while
pos
<
maximum
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
maximum
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
maximum
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
maximum
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
maximum
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
maximum
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
            
parseReference
=
True
        
pos
+
=
1
    
if
parseReference
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
maximum
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
(
            
state
.
env
[
"
references
"
]
[
label
]
if
label
in
state
.
env
[
"
references
"
]
else
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
        
state
.
pos
=
labelStart
        
state
.
posMax
=
labelEnd
        
token
=
state
.
push
(
"
link_open
"
"
a
"
1
)
        
token
.
attrs
=
{
"
href
"
:
href
}
        
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
linkLevel
+
=
1
        
state
.
md
.
inline
.
tokenize
(
state
)
        
state
.
linkLevel
-
=
1
        
token
=
state
.
push
(
"
link_close
"
"
a
"
-
1
)
    
state
.
pos
=
pos
    
state
.
posMax
=
maximum
    
return
True
