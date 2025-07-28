import
contextlib
import
json
import
os
import
pathlib
import
socket
SOCKET_ADDRESS
=
'
\
0chromium_build_server_socket
'
BUILD_SERVER_ENV_VARIABLE
=
'
INVOKED_BY_BUILD_SERVER
'
def
MaybeRunCommand
(
name
argv
stamp_file
force
)
:
  
"
"
"
Returns
True
if
the
command
was
successfully
sent
to
the
build
server
.
"
"
"
  
if
BUILD_SERVER_ENV_VARIABLE
in
os
.
environ
:
    
return
False
  
with
contextlib
.
closing
(
socket
.
socket
(
socket
.
AF_UNIX
)
)
as
sock
:
    
try
:
      
sock
.
connect
(
SOCKET_ADDRESS
)
      
sock
.
sendall
(
          
json
.
dumps
(
{
              
'
name
'
:
name
              
'
cmd
'
:
argv
              
'
cwd
'
:
os
.
getcwd
(
)
              
'
stamp_file
'
:
stamp_file
          
}
)
.
encode
(
'
utf8
'
)
)
    
except
socket
.
error
as
e
:
      
if
e
.
errno
=
=
111
:
        
if
force
:
          
raise
RuntimeError
(
              
'
\
n
\
nBuild
server
is
not
running
and
'
              
'
android_static_analysis
=
"
build_server
"
is
set
.
\
nPlease
run
'
              
'
this
command
in
a
separate
terminal
:
\
n
\
n
'
              
'
build
/
android
/
fast_local_dev_server
.
py
\
n
\
n
'
)
from
None
        
return
False
      
raise
e
  
pathlib
.
Path
(
stamp_file
)
.
touch
(
)
  
return
True
