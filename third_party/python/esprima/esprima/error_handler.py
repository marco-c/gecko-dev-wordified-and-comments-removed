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
from
__future__
import
unicode_literals
from
.
compat
import
unicode
class
Error
(
Exception
)
:
    
def
__init__
(
self
message
name
=
None
index
=
None
lineNumber
=
None
column
=
None
description
=
None
)
:
        
super
(
Error
self
)
.
__init__
(
message
)
        
self
.
message
=
message
        
self
.
name
=
name
        
self
.
index
=
index
        
self
.
lineNumber
=
lineNumber
        
self
.
column
=
column
    
def
toString
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
s
'
%
(
self
.
__class__
.
__name__
self
)
    
def
toDict
(
self
)
:
        
d
=
dict
(
(
unicode
(
k
)
v
)
for
k
v
in
self
.
__dict__
.
items
(
)
if
v
is
not
None
)
        
d
[
'
message
'
]
=
self
.
toString
(
)
        
return
d
class
ErrorHandler
:
    
def
__init__
(
self
)
:
        
self
.
errors
=
[
]
        
self
.
tolerant
=
False
    
def
recordError
(
self
error
)
:
        
self
.
errors
.
append
(
error
.
toDict
(
)
)
    
def
tolerate
(
self
error
)
:
        
if
self
.
tolerant
:
            
self
.
recordError
(
error
)
        
else
:
            
raise
error
    
def
createError
(
self
index
line
col
description
)
:
        
msg
=
'
Line
%
s
:
%
s
'
%
(
line
description
)
        
return
Error
(
msg
index
=
index
lineNumber
=
line
column
=
col
description
=
description
)
    
def
throwError
(
self
index
line
col
description
)
:
        
raise
self
.
createError
(
index
line
col
description
)
    
def
tolerateError
(
self
index
line
col
description
)
:
        
error
=
self
.
createError
(
index
line
col
description
)
        
if
self
.
tolerant
:
            
self
.
recordError
(
error
)
        
else
:
            
raise
error
