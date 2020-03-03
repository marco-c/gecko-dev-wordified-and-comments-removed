#
-
*
-
coding
:
utf
-
8
-
*
-
"
"
"
Use
this
rule
to
force
comments
to
be
indented
like
content
.
.
.
rubric
:
:
Examples
#
.
With
comments
-
indentation
:
{
}
   
the
following
code
snippet
would
*
*
PASS
*
*
:
   
:
:
    
#
Fibonacci
    
[
0
1
1
2
3
5
]
   
the
following
code
snippet
would
*
*
FAIL
*
*
:
   
:
:
      
#
Fibonacci
    
[
0
1
1
2
3
5
]
   
the
following
code
snippet
would
*
*
PASS
*
*
:
   
:
:
    
list
:
        
-
2
        
-
3
        
#
-
4
        
-
5
   
the
following
code
snippet
would
*
*
FAIL
*
*
:
   
:
:
    
list
:
        
-
2
        
-
3
    
#
-
4
        
-
5
   
the
following
code
snippet
would
*
*
PASS
*
*
:
   
:
:
    
#
This
is
the
first
object
    
obj1
:
      
-
item
A
      
#
-
item
B
    
#
This
is
the
second
object
    
obj2
:
[
]
   
the
following
code
snippet
would
*
*
PASS
*
*
:
   
:
:
    
#
This
sentence
    
#
is
a
block
comment
   
the
following
code
snippet
would
*
*
FAIL
*
*
:
   
:
:
    
#
This
sentence
     
#
is
a
block
comment
"
"
"
import
yaml
from
yamllint
.
linter
import
LintProblem
from
yamllint
.
rules
.
common
import
get_line_indent
ID
=
'
comments
-
indentation
'
TYPE
=
'
comment
'
def
check
(
conf
comment
)
:
    
if
(
not
isinstance
(
comment
.
token_before
yaml
.
StreamStartToken
)
and
            
comment
.
token_before
.
end_mark
.
line
+
1
=
=
comment
.
line_no
)
:
        
return
    
next_line_indent
=
comment
.
token_after
.
start_mark
.
column
    
if
isinstance
(
comment
.
token_after
yaml
.
StreamEndToken
)
:
        
next_line_indent
=
0
    
if
isinstance
(
comment
.
token_before
yaml
.
StreamStartToken
)
:
        
prev_line_indent
=
0
    
else
:
        
prev_line_indent
=
get_line_indent
(
comment
.
token_before
)
    
if
prev_line_indent
<
=
next_line_indent
:
        
prev_line_indent
=
next_line_indent
    
if
(
comment
.
comment_before
is
not
None
and
            
not
comment
.
comment_before
.
is_inline
(
)
)
:
        
prev_line_indent
=
comment
.
comment_before
.
column_no
-
1
    
if
(
comment
.
column_no
-
1
!
=
prev_line_indent
and
            
comment
.
column_no
-
1
!
=
next_line_indent
)
:
        
yield
LintProblem
(
comment
.
line_no
comment
.
column_no
                          
'
comment
not
indented
like
content
'
)
