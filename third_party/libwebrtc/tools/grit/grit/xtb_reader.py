'
'
'
Fast
and
efficient
parser
for
XTB
files
.
'
'
'
from
__future__
import
print_function
import
sys
import
xml
.
sax
import
xml
.
sax
.
handler
import
grit
.
node
.
base
class
XtbContentHandler
(
xml
.
sax
.
handler
.
ContentHandler
)
:
  
'
'
'
A
content
handler
that
calls
a
given
callback
function
for
each
  
translation
in
the
XTB
file
.
  
'
'
'
  
def
__init__
(
self
callback
defs
=
None
debug
=
False
target_platform
=
None
)
:
    
self
.
callback
=
callback
    
self
.
debug
=
debug
    
self
.
current_id
=
0
    
self
.
current_structure
=
[
]
    
self
.
language
=
'
'
    
self
.
if_expr
=
None
    
if
defs
:
      
self
.
defines
=
defs
    
else
:
      
self
.
defines
=
{
}
    
if
target_platform
:
      
self
.
target_platform
=
target_platform
    
else
:
      
self
.
target_platform
=
sys
.
platform
  
def
startElement
(
self
name
attrs
)
:
    
if
name
=
=
'
translation
'
:
      
assert
self
.
current_id
=
=
0
and
len
(
self
.
current_structure
)
=
=
0
(
              
"
Didn
'
t
expect
a
<
translation
>
element
here
.
"
)
      
self
.
current_id
=
attrs
.
getValue
(
'
id
'
)
    
elif
name
=
=
'
ph
'
:
      
assert
self
.
current_id
!
=
0
"
Didn
'
t
expect
a
<
ph
>
element
here
.
"
      
self
.
current_structure
.
append
(
(
True
attrs
.
getValue
(
'
name
'
)
)
)
    
elif
name
=
=
'
translationbundle
'
:
      
self
.
language
=
attrs
.
getValue
(
'
lang
'
)
    
elif
name
in
(
'
if
'
'
then
'
'
else
'
)
:
      
assert
self
.
if_expr
is
None
"
Can
'
t
nest
<
if
>
or
use
<
else
>
in
xtb
files
"
      
self
.
if_expr
=
attrs
.
getValue
(
'
expr
'
)
  
def
endElement
(
self
name
)
:
    
if
name
=
=
'
translation
'
:
      
assert
self
.
current_id
!
=
0
      
defs
=
self
.
defines
      
def
pp_ifdef
(
define
)
:
        
return
define
in
defs
      
def
pp_if
(
define
)
:
        
return
define
in
defs
and
defs
[
define
]
      
should_run_callback
=
True
      
if
self
.
if_expr
:
        
should_run_callback
=
grit
.
node
.
base
.
Node
.
EvaluateExpression
(
            
self
.
if_expr
self
.
defines
self
.
target_platform
)
      
if
should_run_callback
:
        
self
.
callback
(
self
.
current_id
self
.
current_structure
)
      
self
.
current_id
=
0
      
self
.
current_structure
=
[
]
    
elif
name
=
=
'
if
'
:
      
assert
self
.
if_expr
is
not
None
      
self
.
if_expr
=
None
  
def
characters
(
self
content
)
:
    
if
self
.
current_id
!
=
0
:
      
self
.
current_structure
.
append
(
(
False
content
)
)
class
XtbErrorHandler
(
xml
.
sax
.
handler
.
ErrorHandler
)
:
  
def
error
(
self
exception
)
:
    
pass
  
def
fatalError
(
self
exception
)
:
    
raise
exception
  
def
warning
(
self
exception
)
:
    
pass
def
Parse
(
xtb_file
callback_function
defs
=
None
debug
=
False
          
target_platform
=
None
)
:
  
'
'
'
Parse
xtb_file
making
a
call
to
callback_function
for
every
translation
  
in
the
XTB
file
.
  
The
callback
function
must
have
the
signature
as
described
below
.
The
'
parts
'
  
parameter
is
a
list
of
tuples
(
is_placeholder
text
)
.
The
'
text
'
part
is
  
either
the
raw
text
(
if
is_placeholder
is
False
)
or
the
name
of
the
placeholder
  
(
if
is_placeholder
is
True
)
.
  
Args
:
    
xtb_file
:
open
(
'
fr
.
xtb
'
'
rb
'
)
    
callback_function
:
def
Callback
(
msg_id
parts
)
:
pass
    
defs
:
None
or
a
dictionary
of
preprocessor
definitions
.
    
debug
:
Default
False
.
Set
True
for
verbose
debug
output
.
    
target_platform
:
None
or
a
sys
.
platform
-
like
identifier
of
the
build
                        
target
platform
.
  
Return
:
    
The
language
of
the
XTB
e
.
g
.
'
fr
'
  
'
'
'
  
front_of_file
=
xtb_file
.
read
(
1024
)
  
xtb_file
.
seek
(
front_of_file
.
find
(
b
'
<
translationbundle
'
)
)
  
handler
=
XtbContentHandler
(
callback
=
callback_function
defs
=
defs
                              
debug
=
debug
target_platform
=
target_platform
)
  
xml
.
sax
.
parse
(
xtb_file
handler
)
  
assert
handler
.
language
!
=
'
'
  
return
handler
.
language
