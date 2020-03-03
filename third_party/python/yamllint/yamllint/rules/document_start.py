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
require
or
forbid
the
use
of
document
start
marker
(
-
-
-
)
.
.
.
rubric
:
:
Options
*
Set
present
to
true
when
the
document
start
marker
is
required
or
to
  
false
when
it
is
forbidden
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
document
-
start
:
{
present
:
true
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
    
-
-
-
    
this
:
      
is
:
[
a
document
]
    
-
-
-
    
-
this
    
-
is
:
another
one
   
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
    
this
:
      
is
:
[
a
document
]
    
-
-
-
    
-
this
    
-
is
:
another
one
#
.
With
document
-
start
:
{
present
:
false
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
    
this
:
      
is
:
[
a
document
]
    
.
.
.
   
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
    
-
-
-
    
this
:
      
is
:
[
a
document
]
    
.
.
.
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
ID
=
'
document
-
start
'
TYPE
=
'
token
'
CONF
=
{
'
present
'
:
bool
}
DEFAULT
=
{
'
present
'
:
True
}
def
check
(
conf
token
prev
next
nextnext
context
)
:
    
if
conf
[
'
present
'
]
:
        
if
(
isinstance
(
prev
(
yaml
.
StreamStartToken
                              
yaml
.
DocumentEndToken
                              
yaml
.
DirectiveToken
)
)
and
            
not
isinstance
(
token
(
yaml
.
DocumentStartToken
                                   
yaml
.
DirectiveToken
                                   
yaml
.
StreamEndToken
)
)
)
:
            
yield
LintProblem
(
token
.
start_mark
.
line
+
1
1
                              
'
missing
document
start
"
-
-
-
"
'
)
    
else
:
        
if
isinstance
(
token
yaml
.
DocumentStartToken
)
:
            
yield
LintProblem
(
token
.
start_mark
.
line
+
1
                              
token
.
start_mark
.
column
+
1
                              
'
found
forbidden
document
start
"
-
-
-
"
'
)
