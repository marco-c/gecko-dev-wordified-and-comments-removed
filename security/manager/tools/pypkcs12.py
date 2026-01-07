"
"
"
Reads
a
specification
from
stdin
or
a
file
and
outputs
a
PKCS12
file
with
the
desired
properties
.
The
input
format
currently
consists
of
a
pycert
certificate
specification
(
see
pycert
.
py
)
.
Currently
keys
other
than
the
default
key
are
not
supported
.
The
password
that
is
used
to
encrypt
and
authenticate
the
file
is
"
password
"
.
"
"
"
import
base64
import
os
import
shutil
import
subprocess
import
sys
import
mozinfo
import
pycert
import
pykey
from
mozfile
import
NamedTemporaryFile
class
Error
(
Exception
)
:
    
"
"
"
Base
class
for
exceptions
in
this
module
.
"
"
"
    
pass
class
OpenSSLError
(
Error
)
:
    
"
"
"
Class
for
handling
errors
when
calling
OpenSSL
.
"
"
"
    
def
__init__
(
self
status
)
:
        
super
(
)
.
__init__
(
)
        
self
.
status
=
status
    
def
__str__
(
self
)
:
        
return
"
Error
running
openssl
:
%
s
"
%
self
.
status
def
runUtil
(
util
args
)
:
    
env
=
os
.
environ
.
copy
(
)
    
if
mozinfo
.
os
=
=
"
linux
"
:
        
pathvar
=
"
LD_LIBRARY_PATH
"
        
app_path
=
os
.
path
.
dirname
(
util
)
        
if
pathvar
in
env
:
            
env
[
pathvar
]
=
"
%
s
%
s
%
s
"
%
(
app_path
os
.
pathsep
env
[
pathvar
]
)
        
else
:
            
env
[
pathvar
]
=
app_path
    
proc
=
subprocess
.
run
(
        
[
util
]
+
args
        
check
=
False
        
env
=
env
        
text
=
True
    
)
    
return
proc
.
returncode
class
PKCS12
:
    
"
"
"
Utility
class
for
reading
a
specification
and
generating
    
a
PKCS12
file
"
"
"
    
def
__init__
(
self
paramStream
)
:
        
self
.
cert
=
pycert
.
Certificate
(
paramStream
)
        
self
.
key
=
pykey
.
keyFromSpecification
(
"
default
"
)
    
def
toDER
(
self
)
:
        
with
(
            
NamedTemporaryFile
(
mode
=
"
wt
+
"
)
as
certTmp
            
NamedTemporaryFile
(
mode
=
"
wt
+
"
)
as
keyTmp
            
NamedTemporaryFile
(
mode
=
"
rb
+
"
)
as
pkcs12Tmp
        
)
:
            
certTmp
.
write
(
self
.
cert
.
toPEM
(
)
)
            
certTmp
.
flush
(
)
            
keyTmp
.
write
(
self
.
key
.
toPEM
(
)
)
            
keyTmp
.
flush
(
)
            
openssl
=
shutil
.
which
(
"
openssl
"
)
            
status
=
runUtil
(
                
openssl
                
[
                    
"
pkcs12
"
                    
"
-
export
"
                    
"
-
inkey
"
                    
keyTmp
.
name
                    
"
-
in
"
                    
certTmp
.
name
                    
"
-
out
"
                    
pkcs12Tmp
.
name
                    
"
-
passout
"
                    
"
pass
:
password
"
                
]
            
)
            
if
status
!
=
0
:
                
raise
OpenSSLError
(
status
)
            
return
pkcs12Tmp
.
read
(
)
    
def
toPEM
(
self
)
:
        
output
=
"
-
-
-
-
-
BEGIN
PKCS12
-
-
-
-
-
"
        
der
=
self
.
toDER
(
)
        
b64
=
base64
.
b64encode
(
der
)
.
decode
(
)
        
while
b64
:
            
output
+
=
"
\
n
"
+
b64
[
:
64
]
            
b64
=
b64
[
64
:
]
        
output
+
=
"
\
n
-
-
-
-
-
END
PKCS12
-
-
-
-
-
"
        
return
output
def
main
(
output
inputPath
)
:
    
with
open
(
inputPath
)
as
configStream
:
        
output
.
write
(
PKCS12
(
configStream
)
.
toDER
(
)
)
if
__name__
=
=
"
__main__
"
:
    
print
(
PKCS12
(
sys
.
stdin
)
.
toPEM
(
)
)
