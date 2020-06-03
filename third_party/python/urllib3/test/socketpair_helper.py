import
socket
try
:
    
_CONNECT_ERROR
=
(
BlockingIOError
InterruptedError
)
except
NameError
:
    
try
:
        
_CONNECT_ERROR
=
(
WindowsError
OSError
socket
.
error
)
    
except
NameError
:
        
_CONNECT_ERROR
=
(
OSError
socket
.
error
)
if
hasattr
(
socket
"
socketpair
"
)
:
    
socketpair
=
socket
.
socketpair
else
:
    
def
socketpair
(
family
=
socket
.
AF_INET
type
=
socket
.
SOCK_STREAM
proto
=
0
)
:
        
"
"
"
A
socket
pair
usable
as
a
self
-
pipe
for
Windows
.
        
Origin
:
https
:
/
/
gist
.
github
.
com
/
4325783
by
Geert
Jansen
.
        
Public
domain
.
        
"
"
"
        
if
family
=
=
socket
.
AF_INET
:
            
host
=
"
127
.
0
.
0
.
1
"
        
elif
family
=
=
socket
.
AF_INET6
:
            
host
=
"
:
:
1
"
        
else
:
            
raise
ValueError
(
                
"
Only
AF_INET
and
AF_INET6
socket
address
families
are
supported
"
            
)
        
if
type
!
=
socket
.
SOCK_STREAM
:
            
raise
ValueError
(
"
Only
SOCK_STREAM
socket
type
is
supported
"
)
        
if
proto
!
=
0
:
            
raise
ValueError
(
"
Only
protocol
zero
is
supported
"
)
        
lsock
=
socket
.
socket
(
family
type
proto
)
        
try
:
            
lsock
.
bind
(
(
host
0
)
)
            
lsock
.
listen
(
1
)
            
addr
port
=
lsock
.
getsockname
(
)
[
:
2
]
            
csock
=
socket
.
socket
(
family
type
proto
)
            
try
:
                
csock
.
setblocking
(
False
)
                
try
:
                    
csock
.
connect
(
(
addr
port
)
)
                
except
_CONNECT_ERROR
:
                    
pass
                
csock
.
setblocking
(
True
)
                
ssock
_
=
lsock
.
accept
(
)
            
except
Exception
:
                
csock
.
close
(
)
                
raise
        
finally
:
            
lsock
.
close
(
)
        
return
(
ssock
csock
)
