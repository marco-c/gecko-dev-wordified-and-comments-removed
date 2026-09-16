from
.
state_inline
import
StateInline
_TerminatorChars
=
{
    
"
\
n
"
    
"
!
"
    
"
#
"
    
"
"
    
"
%
"
    
"
&
"
    
"
*
"
    
"
+
"
    
"
-
"
    
"
:
"
    
"
<
"
    
"
=
"
    
"
>
"
    
"
"
    
"
[
"
    
"
\
\
"
    
"
]
"
    
"
^
"
    
"
_
"
    
"
"
    
"
{
"
    
"
}
"
    
"
~
"
}
def
text
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
    
pos
=
state
.
pos
    
posMax
=
state
.
posMax
    
while
(
pos
<
posMax
)
and
state
.
src
[
pos
]
not
in
_TerminatorChars
:
        
pos
+
=
1
    
if
pos
=
=
state
.
pos
:
        
return
False
    
if
not
silent
:
        
state
.
pending
+
=
state
.
src
[
state
.
pos
:
pos
]
    
state
.
pos
=
pos
    
return
True
