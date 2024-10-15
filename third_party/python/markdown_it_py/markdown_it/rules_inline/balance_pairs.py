"
"
"
Balance
paired
characters
(
*
_
etc
)
in
inline
tokens
.
"
"
"
from
__future__
import
annotations
from
.
state_inline
import
Delimiter
StateInline
def
processDelimiters
(
state
:
StateInline
delimiters
:
list
[
Delimiter
]
)
-
>
None
:
    
"
"
"
For
each
opening
emphasis
-
like
marker
find
a
matching
closing
one
.
"
"
"
    
if
not
delimiters
:
        
return
    
openersBottom
=
{
}
    
maximum
=
len
(
delimiters
)
    
headerIdx
=
0
    
lastTokenIdx
=
-
2
    
jumps
:
list
[
int
]
=
[
]
    
closerIdx
=
0
    
while
closerIdx
<
maximum
:
        
closer
=
delimiters
[
closerIdx
]
        
jumps
.
append
(
0
)
        
if
(
            
delimiters
[
headerIdx
]
.
marker
!
=
closer
.
marker
            
or
lastTokenIdx
!
=
closer
.
token
-
1
        
)
:
            
headerIdx
=
closerIdx
        
lastTokenIdx
=
closer
.
token
        
closer
.
length
=
closer
.
length
or
0
        
if
not
closer
.
close
:
            
closerIdx
+
=
1
            
continue
        
if
closer
.
marker
not
in
openersBottom
:
            
openersBottom
[
closer
.
marker
]
=
[
-
1
-
1
-
1
-
1
-
1
-
1
]
        
minOpenerIdx
=
openersBottom
[
closer
.
marker
]
[
            
(
3
if
closer
.
open
else
0
)
+
(
closer
.
length
%
3
)
        
]
        
openerIdx
=
headerIdx
-
jumps
[
headerIdx
]
-
1
        
newMinOpenerIdx
=
openerIdx
        
while
openerIdx
>
minOpenerIdx
:
            
opener
=
delimiters
[
openerIdx
]
            
if
opener
.
marker
!
=
closer
.
marker
:
                
openerIdx
-
=
jumps
[
openerIdx
]
+
1
                
continue
            
if
opener
.
open
and
opener
.
end
<
0
:
                
isOddMatch
=
False
                
if
(
                    
(
opener
.
close
or
closer
.
open
)
                    
and
(
(
opener
.
length
+
closer
.
length
)
%
3
=
=
0
)
                    
and
(
opener
.
length
%
3
!
=
0
or
closer
.
length
%
3
!
=
0
)
                
)
:
                    
isOddMatch
=
True
                
if
not
isOddMatch
:
                    
if
openerIdx
>
0
and
not
delimiters
[
openerIdx
-
1
]
.
open
:
                        
lastJump
=
jumps
[
openerIdx
-
1
]
+
1
                    
else
:
                        
lastJump
=
0
                    
jumps
[
closerIdx
]
=
closerIdx
-
openerIdx
+
lastJump
                    
jumps
[
openerIdx
]
=
lastJump
                    
closer
.
open
=
False
                    
opener
.
end
=
closerIdx
                    
opener
.
close
=
False
                    
newMinOpenerIdx
=
-
1
                    
lastTokenIdx
=
-
2
                    
break
            
openerIdx
-
=
jumps
[
openerIdx
]
+
1
        
if
newMinOpenerIdx
!
=
-
1
:
            
openersBottom
[
closer
.
marker
]
[
                
(
3
if
closer
.
open
else
0
)
+
(
(
closer
.
length
or
0
)
%
3
)
            
]
=
newMinOpenerIdx
        
closerIdx
+
=
1
def
link_pairs
(
state
:
StateInline
)
-
>
None
:
    
tokens_meta
=
state
.
tokens_meta
    
maximum
=
len
(
state
.
tokens_meta
)
    
processDelimiters
(
state
state
.
delimiters
)
    
curr
=
0
    
while
curr
<
maximum
:
        
curr_meta
=
tokens_meta
[
curr
]
        
if
curr_meta
and
"
delimiters
"
in
curr_meta
:
            
processDelimiters
(
state
curr_meta
[
"
delimiters
"
]
)
        
curr
+
=
1
