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
control
the
indentation
.
.
.
rubric
:
:
Options
*
spaces
defines
the
indentation
width
in
spaces
.
Set
either
to
an
integer
  
(
e
.
g
.
2
or
4
representing
the
number
of
spaces
in
an
indentation
  
level
)
or
to
consistent
to
allow
any
number
as
long
as
it
remains
the
  
same
within
the
file
.
*
indent
-
sequences
defines
whether
block
sequences
should
be
indented
or
  
not
(
when
in
a
mapping
this
indentation
is
not
mandatory
-
-
some
people
  
perceive
the
-
as
part
of
the
indentation
)
.
Possible
values
:
true
  
false
whatever
and
consistent
.
consistent
requires
either
  
all
block
sequences
to
be
indented
or
none
to
be
.
whatever
means
either
  
indenting
or
not
indenting
individual
block
sequences
is
OK
.
*
check
-
multi
-
line
-
strings
defines
whether
to
lint
indentation
in
  
multi
-
line
strings
.
Set
to
true
to
enable
false
to
disable
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
indentation
:
{
spaces
:
1
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
    
history
:
     
-
name
:
Unix
       
date
:
1969
     
-
name
:
Linux
       
date
:
1991
    
nest
:
     
recurse
:
      
-
haystack
:
         
needle
#
.
With
indentation
:
{
spaces
:
4
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
    
history
:
        
-
name
:
Unix
          
date
:
1969
        
-
name
:
Linux
          
date
:
1991
    
nest
:
        
recurse
:
            
-
haystack
:
                  
needle
   
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
    
history
:
      
-
name
:
Unix
        
date
:
1969
      
-
name
:
Linux
        
date
:
1991
    
nest
:
      
recurse
:
        
-
haystack
:
            
needle
#
.
With
indentation
:
{
spaces
:
consistent
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
    
history
:
       
-
name
:
Unix
         
date
:
1969
       
-
name
:
Linux
         
date
:
1991
    
nest
:
       
recurse
:
          
-
haystack
:
               
needle
   
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
    
some
:
      
Russian
:
          
dolls
#
.
With
indentation
:
{
spaces
:
2
indent
-
sequences
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
    
list
:
    
-
flying
    
-
spaghetti
    
-
monster
   
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
flying
      
-
spaghetti
      
-
monster
#
.
With
indentation
:
{
spaces
:
2
indent
-
sequences
:
whatever
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
    
list
:
    
-
flying
:
      
-
spaghetti
      
-
monster
    
-
not
flying
:
        
-
spaghetti
        
-
sauce
#
.
With
indentation
:
{
spaces
:
2
indent
-
sequences
:
consistent
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
flying
:
      
-
spaghetti
      
-
monster
    
-
not
flying
:
      
-
spaghetti
      
-
sauce
   
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
flying
:
        
-
spaghetti
        
-
monster
    
-
not
flying
:
      
-
spaghetti
      
-
sauce
#
.
With
indentation
:
{
spaces
:
4
check
-
multi
-
line
-
strings
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
    
Blaise
Pascal
:
        
Je
vous
cris
une
longue
lettre
parce
que
        
je
n
'
ai
pas
le
temps
d
'
en
crire
une
courte
.
   
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
    
Blaise
Pascal
:
Je
vous
cris
une
longue
lettre
parce
que
                   
je
n
'
ai
pas
le
temps
d
'
en
crire
une
courte
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
    
Blaise
Pascal
:
Je
vous
cris
une
longue
lettre
parce
que
      
je
n
'
ai
pas
le
temps
d
'
en
crire
une
courte
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
    
C
code
:
        
void
main
(
)
{
            
printf
(
"
foo
"
)
;
        
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
    
C
code
:
        
void
main
(
)
{
        
printf
(
"
bar
"
)
;
        
}
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
get_real_end_line
is_explicit_key
ID
=
'
indentation
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
spaces
'
:
(
int
'
consistent
'
)
        
'
indent
-
sequences
'
:
(
bool
'
whatever
'
'
consistent
'
)
        
'
check
-
multi
-
line
-
strings
'
:
bool
}
DEFAULT
=
{
'
spaces
'
:
'
consistent
'
           
'
indent
-
sequences
'
:
True
           
'
check
-
multi
-
line
-
strings
'
:
False
}
ROOT
B_MAP
F_MAP
B_SEQ
F_SEQ
B_ENT
KEY
VAL
=
range
(
8
)
labels
=
(
'
ROOT
'
'
B_MAP
'
'
F_MAP
'
'
B_SEQ
'
'
F_SEQ
'
'
B_ENT
'
'
KEY
'
'
VAL
'
)
class
Parent
(
object
)
:
    
def
__init__
(
self
type
indent
line_indent
=
None
)
:
        
self
.
type
=
type
        
self
.
indent
=
indent
        
self
.
line_indent
=
line_indent
        
self
.
explicit_key
=
False
        
self
.
implicit_block_seq
=
False
    
def
__repr__
(
self
)
:
        
return
'
%
s
:
%
d
'
%
(
labels
[
self
.
type
]
self
.
indent
)
def
check_scalar_indentation
(
conf
token
context
)
:
    
if
token
.
start_mark
.
line
=
=
token
.
end_mark
.
line
:
        
return
    
def
compute_expected_indent
(
found_indent
)
:
        
def
detect_indent
(
base_indent
)
:
            
if
not
isinstance
(
context
[
'
spaces
'
]
int
)
:
                
context
[
'
spaces
'
]
=
found_indent
-
base_indent
            
return
base_indent
+
context
[
'
spaces
'
]
        
if
token
.
plain
:
            
return
token
.
start_mark
.
column
        
elif
token
.
style
in
(
'
"
'
"
'
"
)
:
            
return
token
.
start_mark
.
column
+
1
        
elif
token
.
style
in
(
'
>
'
'
|
'
)
:
            
if
context
[
'
stack
'
]
[
-
1
]
.
type
=
=
B_ENT
:
                
return
detect_indent
(
token
.
start_mark
.
column
)
            
elif
context
[
'
stack
'
]
[
-
1
]
.
type
=
=
KEY
:
                
assert
context
[
'
stack
'
]
[
-
1
]
.
explicit_key
                
return
detect_indent
(
token
.
start_mark
.
column
)
            
elif
context
[
'
stack
'
]
[
-
1
]
.
type
=
=
VAL
:
                
if
token
.
start_mark
.
line
+
1
>
context
[
'
cur_line
'
]
:
                    
return
detect_indent
(
context
[
'
stack
'
]
[
-
1
]
.
indent
)
                
elif
context
[
'
stack
'
]
[
-
2
]
.
explicit_key
:
                    
return
detect_indent
(
token
.
start_mark
.
column
)
                
else
:
                    
return
detect_indent
(
context
[
'
stack
'
]
[
-
2
]
.
indent
)
            
else
:
                
return
detect_indent
(
context
[
'
stack
'
]
[
-
1
]
.
indent
)
    
expected_indent
=
None
    
line_no
=
token
.
start_mark
.
line
+
1
    
line_start
=
token
.
start_mark
.
pointer
    
while
True
:
        
line_start
=
token
.
start_mark
.
buffer
.
find
(
            
'
\
n
'
line_start
token
.
end_mark
.
pointer
-
1
)
+
1
        
if
line_start
=
=
0
:
            
break
        
line_no
+
=
1
        
indent
=
0
        
while
token
.
start_mark
.
buffer
[
line_start
+
indent
]
=
=
'
'
:
            
indent
+
=
1
        
if
token
.
start_mark
.
buffer
[
line_start
+
indent
]
=
=
'
\
n
'
:
            
continue
        
if
expected_indent
is
None
:
            
expected_indent
=
compute_expected_indent
(
indent
)
        
if
indent
!
=
expected_indent
:
            
yield
LintProblem
(
line_no
indent
+
1
                              
'
wrong
indentation
:
expected
%
d
but
found
%
d
'
%
                              
(
expected_indent
indent
)
)
def
_check
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
'
stack
'
not
in
context
:
        
context
[
'
stack
'
]
=
[
Parent
(
ROOT
0
)
]
        
context
[
'
cur_line
'
]
=
-
1
        
context
[
'
spaces
'
]
=
conf
[
'
spaces
'
]
        
context
[
'
indent
-
sequences
'
]
=
conf
[
'
indent
-
sequences
'
]
    
is_visible
=
(
        
not
isinstance
(
token
(
yaml
.
StreamStartToken
yaml
.
StreamEndToken
)
)
and
        
not
isinstance
(
token
yaml
.
BlockEndToken
)
and
        
not
(
isinstance
(
token
yaml
.
ScalarToken
)
and
token
.
value
=
=
'
'
)
)
    
first_in_line
=
(
is_visible
and
                     
token
.
start_mark
.
line
+
1
>
context
[
'
cur_line
'
]
)
    
def
detect_indent
(
base_indent
next
)
:
        
if
not
isinstance
(
context
[
'
spaces
'
]
int
)
:
            
context
[
'
spaces
'
]
=
next
.
start_mark
.
column
-
base_indent
        
return
base_indent
+
context
[
'
spaces
'
]
    
if
first_in_line
:
        
found_indentation
=
token
.
start_mark
.
column
        
expected
=
context
[
'
stack
'
]
[
-
1
]
.
indent
        
if
isinstance
(
token
(
yaml
.
FlowMappingEndToken
                              
yaml
.
FlowSequenceEndToken
)
)
:
            
expected
=
context
[
'
stack
'
]
[
-
1
]
.
line_indent
        
elif
(
context
[
'
stack
'
]
[
-
1
]
.
type
=
=
KEY
and
                
context
[
'
stack
'
]
[
-
1
]
.
explicit_key
and
                
not
isinstance
(
token
yaml
.
ValueToken
)
)
:
            
expected
=
detect_indent
(
expected
token
)
        
if
found_indentation
!
=
expected
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
found_indentation
+
1
                              
'
wrong
indentation
:
expected
%
d
but
found
%
d
'
%
                              
(
expected
found_indentation
)
)
    
if
(
isinstance
(
token
yaml
.
ScalarToken
)
and
            
conf
[
'
check
-
multi
-
line
-
strings
'
]
)
:
        
for
problem
in
check_scalar_indentation
(
conf
token
context
)
:
            
yield
problem
    
if
is_visible
:
        
context
[
'
cur_line
'
]
=
get_real_end_line
(
token
)
        
if
first_in_line
:
            
context
[
'
cur_line_indent
'
]
=
found_indentation
    
if
isinstance
(
token
yaml
.
BlockMappingStartToken
)
:
        
assert
isinstance
(
next
yaml
.
KeyToken
)
        
assert
next
.
start_mark
.
line
=
=
token
.
start_mark
.
line
        
indent
=
token
.
start_mark
.
column
        
context
[
'
stack
'
]
.
append
(
Parent
(
B_MAP
indent
)
)
    
elif
isinstance
(
token
yaml
.
FlowMappingStartToken
)
:
        
if
next
.
start_mark
.
line
=
=
token
.
start_mark
.
line
:
            
indent
=
next
.
start_mark
.
column
        
else
:
            
indent
=
detect_indent
(
context
[
'
cur_line_indent
'
]
next
)
        
context
[
'
stack
'
]
.
append
(
Parent
(
F_MAP
indent
                                       
line_indent
=
context
[
'
cur_line_indent
'
]
)
)
    
elif
isinstance
(
token
yaml
.
BlockSequenceStartToken
)
:
        
assert
isinstance
(
next
yaml
.
BlockEntryToken
)
        
assert
next
.
start_mark
.
line
=
=
token
.
start_mark
.
line
        
indent
=
token
.
start_mark
.
column
        
context
[
'
stack
'
]
.
append
(
Parent
(
B_SEQ
indent
)
)
    
elif
(
isinstance
(
token
yaml
.
BlockEntryToken
)
and
            
not
isinstance
(
next
(
yaml
.
BlockEntryToken
yaml
.
BlockEndToken
)
)
)
:
        
if
context
[
'
stack
'
]
[
-
1
]
.
type
!
=
B_SEQ
:
            
context
[
'
stack
'
]
.
append
(
Parent
(
B_SEQ
token
.
start_mark
.
column
)
)
            
context
[
'
stack
'
]
[
-
1
]
.
implicit_block_seq
=
True
        
if
next
.
start_mark
.
line
=
=
token
.
end_mark
.
line
:
            
indent
=
next
.
start_mark
.
column
        
elif
next
.
start_mark
.
column
=
=
token
.
start_mark
.
column
:
            
indent
=
next
.
start_mark
.
column
        
else
:
            
indent
=
detect_indent
(
token
.
start_mark
.
column
next
)
        
context
[
'
stack
'
]
.
append
(
Parent
(
B_ENT
indent
)
)
    
elif
isinstance
(
token
yaml
.
FlowSequenceStartToken
)
:
        
if
next
.
start_mark
.
line
=
=
token
.
start_mark
.
line
:
            
indent
=
next
.
start_mark
.
column
        
else
:
            
indent
=
detect_indent
(
context
[
'
cur_line_indent
'
]
next
)
        
context
[
'
stack
'
]
.
append
(
Parent
(
F_SEQ
indent
                                       
line_indent
=
context
[
'
cur_line_indent
'
]
)
)
    
elif
isinstance
(
token
yaml
.
KeyToken
)
:
        
indent
=
context
[
'
stack
'
]
[
-
1
]
.
indent
        
context
[
'
stack
'
]
.
append
(
Parent
(
KEY
indent
)
)
        
context
[
'
stack
'
]
[
-
1
]
.
explicit_key
=
is_explicit_key
(
token
)
    
elif
isinstance
(
token
yaml
.
ValueToken
)
:
        
assert
context
[
'
stack
'
]
[
-
1
]
.
type
=
=
KEY
        
if
isinstance
(
next
(
yaml
.
AnchorToken
yaml
.
TagToken
)
)
:
            
if
(
next
.
start_mark
.
line
=
=
prev
.
start_mark
.
line
and
                    
next
.
start_mark
.
line
<
nextnext
.
start_mark
.
line
)
:
                
next
=
nextnext
        
if
not
isinstance
(
next
(
yaml
.
BlockEndToken
                                 
yaml
.
FlowMappingEndToken
                                 
yaml
.
FlowSequenceEndToken
                                 
yaml
.
KeyToken
)
)
:
            
if
context
[
'
stack
'
]
[
-
1
]
.
explicit_key
:
                
indent
=
detect_indent
(
context
[
'
stack
'
]
[
-
1
]
.
indent
next
)
            
elif
next
.
start_mark
.
line
=
=
prev
.
start_mark
.
line
:
                
indent
=
next
.
start_mark
.
column
            
elif
isinstance
(
next
(
yaml
.
BlockSequenceStartToken
                                   
yaml
.
BlockEntryToken
)
)
:
                
if
context
[
'
indent
-
sequences
'
]
is
False
:
                    
indent
=
context
[
'
stack
'
]
[
-
1
]
.
indent
                
elif
context
[
'
indent
-
sequences
'
]
is
True
:
                    
if
(
context
[
'
spaces
'
]
=
=
'
consistent
'
and
                            
next
.
start_mark
.
column
-
                            
context
[
'
stack
'
]
[
-
1
]
.
indent
=
=
0
)
:
                        
indent
=
2
                    
else
:
                        
indent
=
detect_indent
(
context
[
'
stack
'
]
[
-
1
]
.
indent
                                               
next
)
                
else
:
                    
if
next
.
start_mark
.
column
=
=
context
[
'
stack
'
]
[
-
1
]
.
indent
:
                        
if
context
[
'
indent
-
sequences
'
]
=
=
'
consistent
'
:
                            
context
[
'
indent
-
sequences
'
]
=
False
                        
indent
=
context
[
'
stack
'
]
[
-
1
]
.
indent
                    
else
:
                        
if
context
[
'
indent
-
sequences
'
]
=
=
'
consistent
'
:
                            
context
[
'
indent
-
sequences
'
]
=
True
                        
indent
=
detect_indent
(
context
[
'
stack
'
]
[
-
1
]
.
indent
                                               
next
)
            
else
:
                
indent
=
detect_indent
(
context
[
'
stack
'
]
[
-
1
]
.
indent
next
)
            
context
[
'
stack
'
]
.
append
(
Parent
(
VAL
indent
)
)
    
consumed_current_token
=
False
    
while
True
:
        
if
(
context
[
'
stack
'
]
[
-
1
]
.
type
=
=
F_SEQ
and
                
isinstance
(
token
yaml
.
FlowSequenceEndToken
)
and
                
not
consumed_current_token
)
:
            
context
[
'
stack
'
]
.
pop
(
)
            
consumed_current_token
=
True
        
elif
(
context
[
'
stack
'
]
[
-
1
]
.
type
=
=
F_MAP
and
                
isinstance
(
token
yaml
.
FlowMappingEndToken
)
and
                
not
consumed_current_token
)
:
            
context
[
'
stack
'
]
.
pop
(
)
            
consumed_current_token
=
True
        
elif
(
context
[
'
stack
'
]
[
-
1
]
.
type
in
(
B_MAP
B_SEQ
)
and
                
isinstance
(
token
yaml
.
BlockEndToken
)
and
                
not
context
[
'
stack
'
]
[
-
1
]
.
implicit_block_seq
and
                
not
consumed_current_token
)
:
            
context
[
'
stack
'
]
.
pop
(
)
            
consumed_current_token
=
True
        
elif
(
context
[
'
stack
'
]
[
-
1
]
.
type
=
=
B_ENT
and
                
not
isinstance
(
token
yaml
.
BlockEntryToken
)
and
                
context
[
'
stack
'
]
[
-
2
]
.
implicit_block_seq
and
                
not
isinstance
(
token
(
yaml
.
AnchorToken
yaml
.
TagToken
)
)
and
                
not
isinstance
(
next
yaml
.
BlockEntryToken
)
)
:
            
context
[
'
stack
'
]
.
pop
(
)
            
context
[
'
stack
'
]
.
pop
(
)
        
elif
(
context
[
'
stack
'
]
[
-
1
]
.
type
=
=
B_ENT
and
                
isinstance
(
next
(
yaml
.
BlockEntryToken
yaml
.
BlockEndToken
)
)
)
:
            
context
[
'
stack
'
]
.
pop
(
)
        
elif
(
context
[
'
stack
'
]
[
-
1
]
.
type
=
=
VAL
and
                
not
isinstance
(
token
yaml
.
ValueToken
)
and
                
not
isinstance
(
token
(
yaml
.
AnchorToken
yaml
.
TagToken
)
)
)
:
            
assert
context
[
'
stack
'
]
[
-
2
]
.
type
=
=
KEY
            
context
[
'
stack
'
]
.
pop
(
)
            
context
[
'
stack
'
]
.
pop
(
)
        
elif
(
context
[
'
stack
'
]
[
-
1
]
.
type
=
=
KEY
and
                
isinstance
(
next
(
yaml
.
BlockEndToken
                                  
yaml
.
FlowMappingEndToken
                                  
yaml
.
FlowSequenceEndToken
                                  
yaml
.
KeyToken
)
)
)
:
            
context
[
'
stack
'
]
.
pop
(
)
        
else
:
            
break
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
    
try
:
        
for
problem
in
_check
(
conf
token
prev
next
nextnext
context
)
:
            
yield
problem
    
except
AssertionError
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
cannot
infer
indentation
:
unexpected
token
'
)
