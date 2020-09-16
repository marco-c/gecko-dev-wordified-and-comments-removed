from
collections
import
defaultdict
import
re
import
textwrap
from
pathlib
import
Path
from
enum
import
Enum
import
esprima
METADATA
=
[
    
(
"
setUp
"
False
)
    
(
"
tearDown
"
False
)
    
(
"
test
"
True
)
    
(
"
owner
"
True
)
    
(
"
author
"
False
)
    
(
"
name
"
True
)
    
(
"
description
"
True
)
    
(
"
longDescription
"
False
)
    
(
"
usage
"
False
)
    
(
"
supportedBrowsers
"
False
)
    
(
"
supportedPlatforms
"
False
)
    
(
"
filename
"
True
)
]
_INFO
=
"
"
"
\
%
(
filename
)
s
%
(
filename_underline
)
s
%
(
description
)
s
Owner
:
%
(
owner
)
s
Test
Name
:
%
(
name
)
s
Usage
:
%
(
usage
)
s
Description
:
%
(
longDescription
)
s
"
"
"
XPCSHELL_FUNCS
=
"
add_task
"
"
run_test
"
"
run_next_test
"
class
MissingFieldError
(
Exception
)
:
    
def
__init__
(
self
script
field
)
:
        
super
(
)
.
__init__
(
f
"
Missing
metadata
{
field
}
"
)
        
self
.
script
=
script
        
self
.
field
=
field
class
ParseError
(
Exception
)
:
    
def
__init__
(
self
script
exception
)
:
        
super
(
)
.
__init__
(
f
"
Cannot
parse
{
script
}
"
)
        
self
.
script
=
script
        
self
.
exception
=
exception
class
ScriptType
(
Enum
)
:
    
xpcshell
=
1
    
browsertime
=
2
class
ScriptInfo
(
defaultdict
)
:
    
"
"
"
Loads
and
parses
a
Browsertime
test
script
.
"
"
"
    
def
__init__
(
self
path
)
:
        
super
(
ScriptInfo
self
)
.
__init__
(
)
        
try
:
            
self
.
_parse_file
(
path
)
        
except
Exception
as
e
:
            
raise
ParseError
(
path
e
)
        
for
field
required
in
METADATA
:
            
if
not
required
:
                
continue
            
if
field
not
in
self
:
                
raise
MissingFieldError
(
path
field
)
    
def
_parse_file
(
self
path
)
:
        
self
.
script
=
Path
(
path
)
        
self
[
"
filename
"
]
=
str
(
self
.
script
)
        
self
.
script_type
=
ScriptType
.
browsertime
        
with
self
.
script
.
open
(
)
as
f
:
            
self
.
parsed
=
esprima
.
parseScript
(
f
.
read
(
)
)
        
for
stmt
in
self
.
parsed
.
body
:
            
if
(
                
stmt
.
type
=
=
"
ExpressionStatement
"
                
and
stmt
.
expression
is
not
None
                
and
stmt
.
expression
.
callee
is
not
None
                
and
stmt
.
expression
.
callee
.
type
=
=
"
Identifier
"
                
and
stmt
.
expression
.
callee
.
name
in
XPCSHELL_FUNCS
            
)
:
                
self
[
"
test
"
]
=
"
xpcshell
"
                
self
.
script_type
=
ScriptType
.
xpcshell
                
continue
            
if
stmt
.
type
=
=
"
FunctionDeclaration
"
and
stmt
.
id
.
name
in
XPCSHELL_FUNCS
:
                
self
[
"
test
"
]
=
"
xpcshell
"
                
self
.
script_type
=
ScriptType
.
xpcshell
                
continue
            
if
stmt
.
type
=
=
"
VariableDeclaration
"
:
                
for
decl
in
stmt
.
declarations
:
                    
if
(
                        
decl
.
type
!
=
"
VariableDeclarator
"
                        
or
decl
.
id
.
type
!
=
"
Identifier
"
                        
or
decl
.
id
.
name
!
=
"
perfMetadata
"
                        
or
decl
.
init
is
None
                    
)
:
                        
continue
                    
self
.
scan_properties
(
decl
.
init
.
properties
)
                    
continue
            
if
(
                
stmt
.
type
!
=
"
ExpressionStatement
"
                
or
stmt
.
expression
.
left
is
None
                
or
stmt
.
expression
.
left
.
property
is
None
                
or
stmt
.
expression
.
left
.
property
.
name
!
=
"
exports
"
                
or
stmt
.
expression
.
right
is
None
                
or
stmt
.
expression
.
right
.
properties
is
None
            
)
:
                
continue
            
self
.
scan_properties
(
stmt
.
expression
.
right
.
properties
)
    
def
scan_properties
(
self
properties
)
:
        
for
prop
in
properties
:
            
if
prop
.
value
.
type
=
=
"
Identifier
"
:
                
value
=
prop
.
value
.
name
            
elif
prop
.
value
.
type
=
=
"
Literal
"
:
                
value
=
prop
.
value
.
value
            
elif
prop
.
value
.
type
=
=
"
TemplateLiteral
"
:
                
value
=
prop
.
value
.
quasis
[
0
]
.
value
.
cooked
.
replace
(
"
\
n
"
"
"
)
                
value
=
re
.
sub
(
r
"
\
s
+
"
"
"
value
)
.
strip
(
)
            
elif
prop
.
value
.
type
=
=
"
ArrayExpression
"
:
                
value
=
[
e
.
value
for
e
in
prop
.
value
.
elements
]
            
else
:
                
raise
ValueError
(
prop
.
value
.
type
)
            
self
[
prop
.
key
.
name
]
=
value
    
def
__str__
(
self
)
:
        
"
"
"
Used
to
generate
docs
.
"
"
"
        
d
=
defaultdict
(
lambda
:
"
N
/
A
"
)
        
for
field
value
in
self
.
items
(
)
:
            
if
field
=
=
"
filename
"
:
                
d
[
field
]
=
self
.
script
.
name
                
continue
            
if
isinstance
(
value
str
)
:
                
value
=
"
\
n
"
.
join
(
textwrap
.
wrap
(
value
break_on_hyphens
=
False
)
)
            
elif
isinstance
(
value
list
)
:
                
value
=
"
"
.
join
(
value
)
            
d
[
field
]
=
value
        
d
[
"
filename_underline
"
]
=
"
=
"
*
len
(
d
[
"
filename
"
]
)
        
return
_INFO
%
d
    
def
__missing__
(
self
key
)
:
        
return
"
N
/
A
"
    
classmethod
    
def
detect_type
(
cls
path
)
:
        
return
cls
(
path
)
.
script_type
