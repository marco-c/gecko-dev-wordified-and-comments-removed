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
skipBulletListMarker
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
int
:
    
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
    
try
:
        
marker
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
        
return
-
1
    
pos
+
=
1
    
if
marker
not
in
(
"
*
"
"
-
"
"
+
"
)
:
        
return
-
1
    
if
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
:
            
return
-
1
    
return
pos
def
skipOrderedListMarker
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
int
:
    
start
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
    
pos
=
start
    
maximum
=
state
.
eMarks
[
startLine
]
    
if
pos
+
1
>
=
maximum
:
        
return
-
1
    
ch
=
state
.
src
[
pos
]
    
pos
+
=
1
    
ch_ord
=
ord
(
ch
)
    
if
ch_ord
<
0x30
or
ch_ord
>
0x39
:
        
return
-
1
    
while
True
:
        
if
pos
>
=
maximum
:
            
return
-
1
        
ch
=
state
.
src
[
pos
]
        
pos
+
=
1
        
ch_ord
=
ord
(
ch
)
        
if
ch_ord
>
=
0x30
and
ch_ord
<
=
0x39
:
            
if
pos
-
start
>
=
10
:
                
return
-
1
            
continue
        
if
ch
in
(
"
)
"
"
.
"
)
:
            
break
        
return
-
1
    
if
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
:
            
return
-
1
    
return
pos
def
markTightParagraphs
(
state
:
StateBlock
idx
:
int
)
-
>
None
:
    
level
=
state
.
level
+
2
    
i
=
idx
+
2
    
length
=
len
(
state
.
tokens
)
-
2
    
while
i
<
length
:
        
if
state
.
tokens
[
i
]
.
level
=
=
level
and
state
.
tokens
[
i
]
.
type
=
=
"
paragraph_open
"
:
            
state
.
tokens
[
i
+
2
]
.
hidden
=
True
            
state
.
tokens
[
i
]
.
hidden
=
True
            
i
+
=
2
        
i
+
=
1
def
list_block
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
list
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
    
isTerminatingParagraph
=
False
    
tight
=
True
    
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
    
if
(
        
state
.
listIndent
>
=
0
        
and
state
.
sCount
[
startLine
]
-
state
.
listIndent
>
=
4
        
and
state
.
sCount
[
startLine
]
<
state
.
blkIndent
    
)
:
        
return
False
    
if
(
        
silent
        
and
state
.
parentType
=
=
"
paragraph
"
        
and
state
.
sCount
[
startLine
]
>
=
state
.
blkIndent
    
)
:
        
isTerminatingParagraph
=
True
    
posAfterMarker
=
skipOrderedListMarker
(
state
startLine
)
    
if
posAfterMarker
>
=
0
:
        
isOrdered
=
True
        
start
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
        
markerValue
=
int
(
state
.
src
[
start
:
posAfterMarker
-
1
]
)
        
if
isTerminatingParagraph
and
markerValue
!
=
1
:
            
return
False
    
else
:
        
posAfterMarker
=
skipBulletListMarker
(
state
startLine
)
        
if
posAfterMarker
>
=
0
:
            
isOrdered
=
False
        
else
:
            
return
False
    
if
(
        
isTerminatingParagraph
        
and
state
.
skipSpaces
(
posAfterMarker
)
>
=
state
.
eMarks
[
startLine
]
    
)
:
        
return
False
    
markerChar
=
state
.
src
[
posAfterMarker
-
1
]
    
if
silent
:
        
return
True
    
listTokIdx
=
len
(
state
.
tokens
)
    
if
isOrdered
:
        
token
=
state
.
push
(
"
ordered_list_open
"
"
ol
"
1
)
        
if
markerValue
!
=
1
:
            
token
.
attrs
=
{
"
start
"
:
markerValue
}
    
else
:
        
token
=
state
.
push
(
"
bullet_list_open
"
"
ul
"
1
)
    
token
.
map
=
listLines
=
[
startLine
0
]
    
token
.
markup
=
markerChar
    
nextLine
=
startLine
    
prevEmptyEnd
=
False
    
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
list
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
list
"
    
while
nextLine
<
endLine
:
        
pos
=
posAfterMarker
        
maximum
=
state
.
eMarks
[
nextLine
]
        
initial
=
offset
=
(
            
state
.
sCount
[
nextLine
]
            
+
posAfterMarker
            
-
(
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
)
        
)
        
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
)
%
4
            
elif
ch
=
=
"
"
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
        
contentStart
=
pos
        
indentAfterMarker
=
1
if
contentStart
>
=
maximum
else
offset
-
initial
        
if
indentAfterMarker
>
4
:
            
indentAfterMarker
=
1
        
indent
=
initial
+
indentAfterMarker
        
token
=
state
.
push
(
"
list_item_open
"
"
li
"
1
)
        
token
.
markup
=
markerChar
        
token
.
map
=
itemLines
=
[
startLine
0
]
        
if
isOrdered
:
            
token
.
info
=
state
.
src
[
start
:
posAfterMarker
-
1
]
        
checkboxLen
=
0
        
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
tasklists
"
False
)
and
contentStart
<
maximum
:
            
checked
=
_detect_task_checkbox
(
state
.
src
contentStart
maximum
)
            
if
checked
is
not
None
:
                
token
.
meta
=
{
"
checked
"
:
checked
}
                
checkboxLen
=
4
        
oldTight
=
state
.
tight
        
oldBMark
=
state
.
bMarks
[
startLine
]
        
oldTShift
=
state
.
tShift
[
startLine
]
        
oldSCount
=
state
.
sCount
[
startLine
]
        
oldListIndent
=
state
.
listIndent
        
state
.
listIndent
=
state
.
blkIndent
        
state
.
blkIndent
=
indent
        
state
.
tight
=
True
        
state
.
tShift
[
startLine
]
=
contentStart
-
state
.
bMarks
[
startLine
]
        
state
.
sCount
[
startLine
]
=
offset
        
if
checkboxLen
:
            
state
.
bMarks
[
startLine
]
=
contentStart
+
checkboxLen
            
state
.
tShift
[
startLine
]
=
0
        
if
contentStart
>
=
maximum
and
state
.
isEmpty
(
startLine
+
1
)
:
            
state
.
line
=
min
(
state
.
line
+
2
endLine
)
        
else
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
startLine
endLine
)
        
if
(
not
state
.
tight
)
or
prevEmptyEnd
:
            
tight
=
False
        
prevEmptyEnd
=
(
state
.
line
-
startLine
)
>
1
and
state
.
isEmpty
(
state
.
line
-
1
)
        
state
.
blkIndent
=
state
.
listIndent
        
state
.
listIndent
=
oldListIndent
        
if
checkboxLen
:
            
state
.
bMarks
[
startLine
]
=
oldBMark
        
state
.
tShift
[
startLine
]
=
oldTShift
        
state
.
sCount
[
startLine
]
=
oldSCount
        
state
.
tight
=
oldTight
        
token
=
state
.
push
(
"
list_item_close
"
"
li
"
-
1
)
        
token
.
markup
=
markerChar
        
nextLine
=
startLine
=
state
.
line
        
itemLines
[
1
]
=
nextLine
        
if
nextLine
>
=
endLine
:
            
break
        
contentStart
=
state
.
bMarks
[
startLine
]
        
if
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
:
            
break
        
if
state
.
is_code_block
(
startLine
)
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
            
break
        
if
isOrdered
:
            
posAfterMarker
=
skipOrderedListMarker
(
state
nextLine
)
            
if
posAfterMarker
<
0
:
                
break
            
start
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
        
else
:
            
posAfterMarker
=
skipBulletListMarker
(
state
nextLine
)
            
if
posAfterMarker
<
0
:
                
break
        
if
markerChar
!
=
state
.
src
[
posAfterMarker
-
1
]
:
            
break
    
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
tasklists
"
False
)
:
        
containsTask
=
False
        
level
=
state
.
tokens
[
listTokIdx
]
.
level
        
for
j
in
range
(
listTokIdx
+
1
len
(
state
.
tokens
)
)
:
            
tok
=
state
.
tokens
[
j
]
            
if
(
                
tok
.
level
=
=
level
+
1
                
and
tok
.
type
=
=
"
list_item_open
"
                
and
tok
.
meta
                
and
"
checked
"
in
tok
.
meta
            
)
:
                
tok
.
attrJoin
(
"
class
"
"
task
-
list
-
item
"
)
                
containsTask
=
True
        
if
containsTask
:
            
state
.
tokens
[
listTokIdx
]
.
attrJoin
(
"
class
"
"
contains
-
task
-
list
"
)
    
if
isOrdered
:
        
token
=
state
.
push
(
"
ordered_list_close
"
"
ol
"
-
1
)
    
else
:
        
token
=
state
.
push
(
"
bullet_list_close
"
"
ul
"
-
1
)
    
token
.
markup
=
markerChar
    
listLines
[
1
]
=
nextLine
    
state
.
line
=
nextLine
    
state
.
parentType
=
oldParentType
    
if
tight
:
        
markTightParagraphs
(
state
listTokIdx
)
    
return
True
def
_detect_task_checkbox
(
src
:
str
pos
:
int
maximum
:
int
)
-
>
bool
|
None
:
    
"
"
"
Detect
[
]
[
x
]
or
[
X
]
at
*
pos
*
followed
by
whitespace
.
    
Returns
True
(
checked
)
False
(
unchecked
)
or
None
(
no
match
)
.
    
"
"
"
    
if
pos
+
4
>
maximum
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
:
        
return
None
    
inner
=
src
[
pos
+
1
]
    
if
src
[
pos
+
2
]
!
=
"
]
"
:
        
return
None
    
if
inner
=
=
"
"
:
        
checked
=
False
    
elif
inner
in
(
"
x
"
"
X
"
)
:
        
checked
=
True
    
else
:
        
return
None
    
if
src
[
pos
+
3
]
not
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
        
return
None
    
return
checked
