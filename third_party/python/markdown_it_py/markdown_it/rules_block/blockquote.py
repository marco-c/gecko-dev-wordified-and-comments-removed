from
__future__
import
annotations
import
logging
from
.
.
common
.
utils
import
isStrSpace
from
.
state_block
import
StateBlock
LOGGER
=
logging
.
getLogger
(
__name__
)
def
blockquote
(
state
:
StateBlock
startLine
:
int
endLine
:
int
silent
:
bool
)
-
>
bool
:
    
LOGGER
.
debug
(
        
"
entering
blockquote
:
%
s
%
s
%
s
%
s
"
state
startLine
endLine
silent
    
)
    
oldLineMax
=
state
.
lineMax
    
pos
=
state
.
bMarks
[
startLine
]
+
state
.
tShift
[
startLine
]
    
max
=
state
.
eMarks
[
startLine
]
    
if
state
.
is_code_block
(
startLine
)
:
        
return
False
    
try
:
        
if
state
.
src
[
pos
]
!
=
"
>
"
:
            
return
False
    
except
IndexError
:
        
return
False
    
pos
+
=
1
    
if
silent
:
        
return
True
    
initial
=
offset
=
state
.
sCount
[
startLine
]
+
1
    
try
:
        
second_char
:
str
|
None
=
state
.
src
[
pos
]
    
except
IndexError
:
        
second_char
=
None
    
if
second_char
=
=
"
"
:
        
pos
+
=
1
        
initial
+
=
1
        
offset
+
=
1
        
adjustTab
=
False
        
spaceAfterMarker
=
True
    
elif
second_char
=
=
"
\
t
"
:
        
spaceAfterMarker
=
True
        
if
(
state
.
bsCount
[
startLine
]
+
offset
)
%
4
=
=
3
:
            
pos
+
=
1
            
initial
+
=
1
            
offset
+
=
1
            
adjustTab
=
False
        
else
:
            
adjustTab
=
True
    
else
:
        
spaceAfterMarker
=
False
    
oldBMarks
=
[
state
.
bMarks
[
startLine
]
]
    
state
.
bMarks
[
startLine
]
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
isStrSpace
(
ch
)
:
            
if
ch
=
=
"
\
t
"
:
                
offset
+
=
(
                    
4
                    
-
(
offset
+
state
.
bsCount
[
startLine
]
+
(
1
if
adjustTab
else
0
)
)
%
4
                
)
            
else
:
                
offset
+
=
1
        
else
:
            
break
        
pos
+
=
1
    
oldBSCount
=
[
state
.
bsCount
[
startLine
]
]
    
state
.
bsCount
[
startLine
]
=
(
        
state
.
sCount
[
startLine
]
+
1
+
(
1
if
spaceAfterMarker
else
0
)
    
)
    
lastLineEmpty
=
pos
>
=
max
    
oldSCount
=
[
state
.
sCount
[
startLine
]
]
    
state
.
sCount
[
startLine
]
=
offset
-
initial
    
oldTShift
=
[
state
.
tShift
[
startLine
]
]
    
state
.
tShift
[
startLine
]
=
pos
-
state
.
bMarks
[
startLine
]
    
terminatorRules
=
state
.
md
.
block
.
ruler
.
getRules
(
"
blockquote
"
)
    
oldParentType
=
state
.
parentType
    
state
.
parentType
=
"
blockquote
"
    
nextLine
=
startLine
+
1
    
while
nextLine
<
endLine
:
        
isOutdented
=
state
.
sCount
[
nextLine
]
<
state
.
blkIndent
        
pos
=
state
.
bMarks
[
nextLine
]
+
state
.
tShift
[
nextLine
]
        
max
=
state
.
eMarks
[
nextLine
]
        
if
pos
>
=
max
:
            
break
        
evaluatesTrue
=
state
.
src
[
pos
]
=
=
"
>
"
and
not
isOutdented
        
pos
+
=
1
        
if
evaluatesTrue
:
            
initial
=
offset
=
state
.
sCount
[
nextLine
]
+
1
            
try
:
                
next_char
:
str
|
None
=
state
.
src
[
pos
]
            
except
IndexError
:
                
next_char
=
None
            
if
next_char
=
=
"
"
:
                
pos
+
=
1
                
initial
+
=
1
                
offset
+
=
1
                
adjustTab
=
False
                
spaceAfterMarker
=
True
            
elif
next_char
=
=
"
\
t
"
:
                
spaceAfterMarker
=
True
                
if
(
state
.
bsCount
[
nextLine
]
+
offset
)
%
4
=
=
3
:
                    
pos
+
=
1
                    
initial
+
=
1
                    
offset
+
=
1
                    
adjustTab
=
False
                
else
:
                    
adjustTab
=
True
            
else
:
                
spaceAfterMarker
=
False
            
oldBMarks
.
append
(
state
.
bMarks
[
nextLine
]
)
            
state
.
bMarks
[
nextLine
]
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
isStrSpace
(
ch
)
:
                    
if
ch
=
=
"
\
t
"
:
                        
offset
+
=
(
                            
4
                            
-
(
                                
offset
                                
+
state
.
bsCount
[
nextLine
]
                                
+
(
1
if
adjustTab
else
0
)
                            
)
                            
%
4
                        
)
                    
else
:
                        
offset
+
=
1
                
else
:
                    
break
                
pos
+
=
1
            
lastLineEmpty
=
pos
>
=
max
            
oldBSCount
.
append
(
state
.
bsCount
[
nextLine
]
)
            
state
.
bsCount
[
nextLine
]
=
(
                
state
.
sCount
[
nextLine
]
+
1
+
(
1
if
spaceAfterMarker
else
0
)
            
)
            
oldSCount
.
append
(
state
.
sCount
[
nextLine
]
)
            
state
.
sCount
[
nextLine
]
=
offset
-
initial
            
oldTShift
.
append
(
state
.
tShift
[
nextLine
]
)
            
state
.
tShift
[
nextLine
]
=
pos
-
state
.
bMarks
[
nextLine
]
            
nextLine
+
=
1
            
continue
        
if
lastLineEmpty
:
            
break
        
terminate
=
False
        
for
terminatorRule
in
terminatorRules
:
            
if
terminatorRule
(
state
nextLine
endLine
True
)
:
                
terminate
=
True
                
break
        
if
terminate
:
            
state
.
lineMax
=
nextLine
            
if
state
.
blkIndent
!
=
0
:
                
oldBMarks
.
append
(
state
.
bMarks
[
nextLine
]
)
                
oldBSCount
.
append
(
state
.
bsCount
[
nextLine
]
)
                
oldTShift
.
append
(
state
.
tShift
[
nextLine
]
)
                
oldSCount
.
append
(
state
.
sCount
[
nextLine
]
)
                
state
.
sCount
[
nextLine
]
-
=
state
.
blkIndent
            
break
        
oldBMarks
.
append
(
state
.
bMarks
[
nextLine
]
)
        
oldBSCount
.
append
(
state
.
bsCount
[
nextLine
]
)
        
oldTShift
.
append
(
state
.
tShift
[
nextLine
]
)
        
oldSCount
.
append
(
state
.
sCount
[
nextLine
]
)
        
state
.
sCount
[
nextLine
]
=
-
1
        
nextLine
+
=
1
    
oldIndent
=
state
.
blkIndent
    
state
.
blkIndent
=
0
    
alert_kind
=
None
    
if
state
.
md
.
options
.
get
(
"
alerts
"
False
)
and
nextLine
>
startLine
:
        
alert_kind
=
_detect_alert
(
state
startLine
)
    
lines
=
[
startLine
0
]
    
if
alert_kind
is
not
None
:
        
alert_lower
=
alert_kind
.
lower
(
)
        
token
=
state
.
push
(
"
alert_open
"
"
div
"
1
)
        
token
.
markup
=
"
>
"
        
token
.
attrSet
(
"
class
"
f
"
markdown
-
alert
markdown
-
alert
-
{
alert_lower
}
"
)
        
token
.
map
=
lines
        
token
.
info
=
alert_kind
        
token
.
meta
=
{
"
kind
"
:
alert_kind
}
        
token
=
state
.
push
(
"
alert_title_open
"
"
p
"
1
)
        
token
.
attrSet
(
"
class
"
"
markdown
-
alert
-
title
"
)
        
title_token
=
state
.
push
(
"
inline
"
"
"
0
)
        
title_token
.
content
=
alert_kind
.
capitalize
(
)
        
title_token
.
children
=
[
]
        
token
=
state
.
push
(
"
alert_title_close
"
"
p
"
-
1
)
        
contentStart
=
startLine
+
1
        
if
contentStart
<
nextLine
:
            
state
.
md
.
block
.
tokenize
(
state
contentStart
nextLine
)
        
else
:
            
state
.
line
=
nextLine
        
token
=
state
.
push
(
"
alert_close
"
"
div
"
-
1
)
        
token
.
markup
=
"
>
"
    
else
:
        
token
=
state
.
push
(
"
blockquote_open
"
"
blockquote
"
1
)
        
token
.
markup
=
"
>
"
        
token
.
map
=
lines
        
state
.
md
.
block
.
tokenize
(
state
startLine
nextLine
)
        
token
=
state
.
push
(
"
blockquote_close
"
"
blockquote
"
-
1
)
        
token
.
markup
=
"
>
"
    
state
.
lineMax
=
oldLineMax
    
state
.
parentType
=
oldParentType
    
lines
[
1
]
=
state
.
line
    
for
i
item
in
enumerate
(
oldTShift
)
:
        
state
.
bMarks
[
i
+
startLine
]
=
oldBMarks
[
i
]
        
state
.
tShift
[
i
+
startLine
]
=
item
        
state
.
sCount
[
i
+
startLine
]
=
oldSCount
[
i
]
        
state
.
bsCount
[
i
+
startLine
]
=
oldBSCount
[
i
]
    
state
.
blkIndent
=
oldIndent
    
return
True
_ALERT_TYPES
=
{
"
NOTE
"
"
TIP
"
"
IMPORTANT
"
"
WARNING
"
"
CAUTION
"
}
def
_detect_alert
(
state
:
StateBlock
startLine
:
int
)
-
>
str
|
None
:
    
"
"
"
Detect
[
!
TYPE
]
on
*
startLine
*
(
after
>
prefix
has
been
stripped
)
.
    
Returns
the
alert
type
string
(
e
.
g
.
"
NOTE
"
)
or
None
.
    
"
"
"
    
pos
=
state
.
bMarks
[
startLine
]
+
state
.
tShift
[
startLine
]
    
maximum
=
state
.
eMarks
[
startLine
]
    
src
=
state
.
src
    
while
maximum
>
pos
and
src
[
maximum
-
1
]
in
(
"
"
"
\
t
"
)
:
        
maximum
-
=
1
    
if
maximum
-
pos
<
4
:
        
return
None
    
if
src
[
pos
]
!
=
"
[
"
or
src
[
pos
+
1
]
!
=
"
!
"
:
        
return
None
    
if
src
[
maximum
-
1
]
!
=
"
]
"
:
        
return
None
    
type_str
=
src
[
pos
+
2
:
maximum
-
1
]
.
upper
(
)
    
if
type_str
not
in
_ALERT_TYPES
:
        
return
None
    
return
type_str
