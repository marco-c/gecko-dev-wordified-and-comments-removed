"
"
"
A
pywebsocket3
handler
which
runs
arbitrary
Python
code
and
returns
the
result
.
This
is
used
to
test
OS
specific
accessibility
APIs
which
can
'
t
be
tested
in
JS
.
It
is
intended
to
be
called
from
JS
browser
tests
.
"
"
"
import
json
import
math
import
os
import
sys
import
traceback
from
mod_pywebsocket
import
msgutil
def
web_socket_do_extra_handshake
(
request
)
:
    
pass
def
web_socket_transfer_data
(
request
)
:
    
def
send
(
*
args
)
:
        
"
"
"
Send
a
response
to
the
client
as
a
JSON
array
.
"
"
"
        
msgutil
.
send_message
(
request
json
.
dumps
(
args
)
)
    
cleanNamespace
=
{
}
    
testDir
=
None
    
if
sys
.
platform
=
=
"
win32
"
:
        
testDir
=
"
windows
"
    
elif
sys
.
platform
=
=
"
linux
"
:
        
testDir
=
"
atk
"
    
if
testDir
:
        
sys
.
path
.
append
(
            
os
.
path
.
join
(
                
os
.
getcwd
(
)
"
browser
"
"
accessible
"
"
tests
"
"
browser
"
testDir
            
)
        
)
        
try
:
            
import
a11y_setup
            
cleanNamespace
=
a11y_setup
.
__dict__
            
setupExc
=
None
        
except
Exception
:
            
setupExc
=
traceback
.
format_exc
(
)
        
sys
.
path
.
pop
(
)
    
def
info
(
message
)
:
        
"
"
"
Log
an
info
message
.
"
"
"
        
send
(
"
info
"
str
(
message
)
)
    
cleanNamespace
[
"
info
"
]
=
info
    
namespace
=
cleanNamespace
.
copy
(
)
    
while
True
:
        
code
=
msgutil
.
receive_message
(
request
)
        
if
not
code
:
            
return
        
if
code
=
=
"
__reset__
"
:
            
namespace
=
cleanNamespace
.
copy
(
)
            
send
(
"
return
"
None
)
            
continue
        
if
setupExc
:
            
send
(
"
exception
"
setupExc
)
            
continue
        
if
"
\
n
"
not
in
code
and
not
code
.
lstrip
(
)
.
startswith
(
"
return
"
)
:
            
code
=
f
"
run
=
lambda
:
{
code
}
"
        
else
:
            
lines
=
[
"
def
run
(
)
:
"
]
            
lines
.
extend
(
f
"
{
line
}
"
for
line
in
code
.
splitlines
(
)
)
            
code
=
"
\
n
"
.
join
(
lines
)
        
try
:
            
exec
(
code
namespace
)
            
ret
=
namespace
[
"
run
"
]
(
)
            
if
isinstance
(
ret
float
)
and
math
.
isnan
(
ret
)
:
                
ret
=
None
            
send
(
"
return
"
ret
)
        
except
Exception
:
            
send
(
"
exception
"
traceback
.
format_exc
(
)
)
