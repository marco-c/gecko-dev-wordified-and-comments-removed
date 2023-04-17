import
sys
def
IsWindows
(
)
:
  
return
sys
.
platform
in
[
'
win32
'
'
cygwin
'
]
def
IsLinux
(
)
:
  
return
sys
.
platform
.
startswith
(
(
'
linux
'
'
freebsd
'
'
netbsd
'
'
openbsd
'
)
)
def
IsMac
(
)
:
  
return
sys
.
platform
=
=
'
darwin
'
def
host_os
(
)
:
  
"
"
"
  
Returns
a
string
representing
the
host_os
of
the
current
system
.
  
Possible
values
:
'
win
'
'
mac
'
'
linux
'
'
unknown
'
.
  
"
"
"
  
if
IsWindows
(
)
:
    
return
'
win
'
  
elif
IsLinux
(
)
:
    
return
'
linux
'
  
elif
IsMac
(
)
:
    
return
'
mac
'
  
else
:
    
return
'
unknown
'
