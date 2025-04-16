"
"
"
tests
for
mozfile
.
NamedTemporaryFile
"
"
"
import
os
import
unittest
import
mozfile
import
mozunit
class
TestNamedTemporaryFile
(
unittest
.
TestCase
)
:
    
"
"
"
test
our
fix
for
NamedTemporaryFile
"
"
"
    
def
test_named_temporary_file
(
self
)
:
        
"
"
"
Ensure
the
fix
for
re
-
opening
a
NamedTemporaryFile
works
        
Refer
to
https
:
/
/
bugzilla
.
mozilla
.
org
/
show_bug
.
cgi
?
id
=
818777
        
and
https
:
/
/
bugzilla
.
mozilla
.
org
/
show_bug
.
cgi
?
id
=
821362
        
"
"
"
        
test_string
=
b
"
A
simple
test
"
        
with
mozfile
.
NamedTemporaryFile
(
)
as
temp
:
            
temp
.
write
(
test_string
)
            
temp
.
flush
(
)
            
self
.
assertEqual
(
open
(
temp
.
name
"
rb
"
)
.
read
(
)
test_string
)
    
def
test_iteration
(
self
)
:
        
"
"
"
ensure
the
line
iterator
works
"
"
"
        
tf
=
mozfile
.
NamedTemporaryFile
(
)
        
notes
=
[
b
"
doe
"
b
"
rae
"
b
"
mi
"
]
        
for
note
in
notes
:
            
tf
.
write
(
b
"
%
s
\
n
"
%
note
)
        
tf
.
flush
(
)
        
tf
.
seek
(
0
)
        
lines
=
[
line
.
rstrip
(
b
"
\
n
"
)
for
line
in
tf
.
readlines
(
)
]
        
self
.
assertEqual
(
lines
notes
)
        
lines
=
[
]
        
for
line
in
tf
:
            
lines
.
append
(
line
.
strip
(
)
)
        
self
.
assertEqual
(
lines
[
]
)
        
tf
.
seek
(
0
)
        
lines
=
[
]
        
for
line
in
tf
:
            
lines
.
append
(
line
.
strip
(
)
)
        
self
.
assertEqual
(
lines
notes
)
    
def
test_delete
(
self
)
:
        
"
"
"
ensure
delete
=
True
/
False
works
as
expected
"
"
"
        
path
=
None
        
with
mozfile
.
NamedTemporaryFile
(
delete
=
True
)
as
tf
:
            
path
=
tf
.
name
        
self
.
assertTrue
(
isinstance
(
path
(
str
)
)
)
        
self
.
assertFalse
(
os
.
path
.
exists
(
path
)
)
        
tf
=
mozfile
.
NamedTemporaryFile
(
delete
=
True
)
        
path
=
tf
.
name
        
self
.
assertTrue
(
os
.
path
.
exists
(
path
)
)
        
del
tf
        
self
.
assertFalse
(
os
.
path
.
exists
(
path
)
)
        
path
=
None
        
try
:
            
with
mozfile
.
NamedTemporaryFile
(
delete
=
False
)
as
tf
:
                
path
=
tf
.
name
            
self
.
assertTrue
(
os
.
path
.
exists
(
path
)
)
        
finally
:
            
if
path
and
os
.
path
.
exists
(
path
)
:
                
os
.
remove
(
path
)
        
path
=
None
        
try
:
            
tf
=
mozfile
.
NamedTemporaryFile
(
delete
=
False
)
            
path
=
tf
.
name
            
self
.
assertTrue
(
os
.
path
.
exists
(
path
)
)
            
del
tf
            
self
.
assertTrue
(
os
.
path
.
exists
(
path
)
)
        
finally
:
            
if
path
and
os
.
path
.
exists
(
path
)
:
                
os
.
remove
(
path
)
if
__name__
=
=
"
__main__
"
:
    
mozunit
.
main
(
)
