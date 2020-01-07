"
"
"
Low
-
level
helpers
for
the
SecureTransport
bindings
.
These
are
Python
functions
that
are
not
directly
related
to
the
high
-
level
APIs
but
are
necessary
to
get
them
to
work
.
They
include
a
whole
bunch
of
low
-
level
CoreFoundation
messing
about
and
memory
management
.
The
concerns
in
this
module
are
almost
entirely
about
trying
to
avoid
memory
leaks
and
providing
appropriate
and
useful
assistance
to
the
higher
-
level
code
.
"
"
"
import
base64
import
ctypes
import
itertools
import
re
import
os
import
ssl
import
tempfile
from
.
bindings
import
Security
CoreFoundation
CFConst
_PEM_CERTS_RE
=
re
.
compile
(
    
b
"
-
-
-
-
-
BEGIN
CERTIFICATE
-
-
-
-
-
\
n
(
.
*
?
)
\
n
-
-
-
-
-
END
CERTIFICATE
-
-
-
-
-
"
re
.
DOTALL
)
def
_cf_data_from_bytes
(
bytestring
)
:
    
"
"
"
    
Given
a
bytestring
create
a
CFData
object
from
it
.
This
CFData
object
must
    
be
CFReleased
by
the
caller
.
    
"
"
"
    
return
CoreFoundation
.
CFDataCreate
(
        
CoreFoundation
.
kCFAllocatorDefault
bytestring
len
(
bytestring
)
    
)
def
_cf_dictionary_from_tuples
(
tuples
)
:
    
"
"
"
    
Given
a
list
of
Python
tuples
create
an
associated
CFDictionary
.
    
"
"
"
    
dictionary_size
=
len
(
tuples
)
    
keys
=
(
t
[
0
]
for
t
in
tuples
)
    
values
=
(
t
[
1
]
for
t
in
tuples
)
    
cf_keys
=
(
CoreFoundation
.
CFTypeRef
*
dictionary_size
)
(
*
keys
)
    
cf_values
=
(
CoreFoundation
.
CFTypeRef
*
dictionary_size
)
(
*
values
)
    
return
CoreFoundation
.
CFDictionaryCreate
(
        
CoreFoundation
.
kCFAllocatorDefault
        
cf_keys
        
cf_values
        
dictionary_size
        
CoreFoundation
.
kCFTypeDictionaryKeyCallBacks
        
CoreFoundation
.
kCFTypeDictionaryValueCallBacks
    
)
def
_cf_string_to_unicode
(
value
)
:
    
"
"
"
    
Creates
a
Unicode
string
from
a
CFString
object
.
Used
entirely
for
error
    
reporting
.
    
Yes
it
annoys
me
quite
a
lot
that
this
function
is
this
complex
.
    
"
"
"
    
value_as_void_p
=
ctypes
.
cast
(
value
ctypes
.
POINTER
(
ctypes
.
c_void_p
)
)
    
string
=
CoreFoundation
.
CFStringGetCStringPtr
(
        
value_as_void_p
        
CFConst
.
kCFStringEncodingUTF8
    
)
    
if
string
is
None
:
        
buffer
=
ctypes
.
create_string_buffer
(
1024
)
        
result
=
CoreFoundation
.
CFStringGetCString
(
            
value_as_void_p
            
buffer
            
1024
            
CFConst
.
kCFStringEncodingUTF8
        
)
        
if
not
result
:
            
raise
OSError
(
'
Error
copying
C
string
from
CFStringRef
'
)
        
string
=
buffer
.
value
    
if
string
is
not
None
:
        
string
=
string
.
decode
(
'
utf
-
8
'
)
    
return
string
def
_assert_no_error
(
error
exception_class
=
None
)
:
    
"
"
"
    
Checks
the
return
code
and
throws
an
exception
if
there
is
an
error
to
    
report
    
"
"
"
    
if
error
=
=
0
:
        
return
    
cf_error_string
=
Security
.
SecCopyErrorMessageString
(
error
None
)
    
output
=
_cf_string_to_unicode
(
cf_error_string
)
    
CoreFoundation
.
CFRelease
(
cf_error_string
)
    
if
output
is
None
or
output
=
=
u
'
'
:
        
output
=
u
'
OSStatus
%
s
'
%
error
    
if
exception_class
is
None
:
        
exception_class
=
ssl
.
SSLError
    
raise
exception_class
(
output
)
def
_cert_array_from_pem
(
pem_bundle
)
:
    
"
"
"
    
Given
a
bundle
of
certs
in
PEM
format
turns
them
into
a
CFArray
of
certs
    
that
can
be
used
to
validate
a
cert
chain
.
    
"
"
"
    
der_certs
=
[
        
base64
.
b64decode
(
match
.
group
(
1
)
)
        
for
match
in
_PEM_CERTS_RE
.
finditer
(
pem_bundle
)
    
]
    
if
not
der_certs
:
        
raise
ssl
.
SSLError
(
"
No
root
certificates
specified
"
)
    
cert_array
=
CoreFoundation
.
CFArrayCreateMutable
(
        
CoreFoundation
.
kCFAllocatorDefault
        
0
        
ctypes
.
byref
(
CoreFoundation
.
kCFTypeArrayCallBacks
)
    
)
    
if
not
cert_array
:
        
raise
ssl
.
SSLError
(
"
Unable
to
allocate
memory
!
"
)
    
try
:
        
for
der_bytes
in
der_certs
:
            
certdata
=
_cf_data_from_bytes
(
der_bytes
)
            
if
not
certdata
:
                
raise
ssl
.
SSLError
(
"
Unable
to
allocate
memory
!
"
)
            
cert
=
Security
.
SecCertificateCreateWithData
(
                
CoreFoundation
.
kCFAllocatorDefault
certdata
            
)
            
CoreFoundation
.
CFRelease
(
certdata
)
            
if
not
cert
:
                
raise
ssl
.
SSLError
(
"
Unable
to
build
cert
object
!
"
)
            
CoreFoundation
.
CFArrayAppendValue
(
cert_array
cert
)
            
CoreFoundation
.
CFRelease
(
cert
)
    
except
Exception
:
        
CoreFoundation
.
CFRelease
(
cert_array
)
    
return
cert_array
def
_is_cert
(
item
)
:
    
"
"
"
    
Returns
True
if
a
given
CFTypeRef
is
a
certificate
.
    
"
"
"
    
expected
=
Security
.
SecCertificateGetTypeID
(
)
    
return
CoreFoundation
.
CFGetTypeID
(
item
)
=
=
expected
def
_is_identity
(
item
)
:
    
"
"
"
    
Returns
True
if
a
given
CFTypeRef
is
an
identity
.
    
"
"
"
    
expected
=
Security
.
SecIdentityGetTypeID
(
)
    
return
CoreFoundation
.
CFGetTypeID
(
item
)
=
=
expected
def
_temporary_keychain
(
)
:
    
"
"
"
    
This
function
creates
a
temporary
Mac
keychain
that
we
can
use
to
work
with
    
credentials
.
This
keychain
uses
a
one
-
time
password
and
a
temporary
file
to
    
store
the
data
.
We
expect
to
have
one
keychain
per
socket
.
The
returned
    
SecKeychainRef
must
be
freed
by
the
caller
including
calling
    
SecKeychainDelete
.
    
Returns
a
tuple
of
the
SecKeychainRef
and
the
path
to
the
temporary
    
directory
that
contains
it
.
    
"
"
"
    
random_bytes
=
os
.
urandom
(
40
)
    
filename
=
base64
.
b64encode
(
random_bytes
[
:
8
]
)
.
decode
(
'
utf
-
8
'
)
    
password
=
base64
.
b64encode
(
random_bytes
[
8
:
]
)
    
tempdirectory
=
tempfile
.
mkdtemp
(
)
    
keychain_path
=
os
.
path
.
join
(
tempdirectory
filename
)
.
encode
(
'
utf
-
8
'
)
    
keychain
=
Security
.
SecKeychainRef
(
)
    
status
=
Security
.
SecKeychainCreate
(
        
keychain_path
        
len
(
password
)
        
password
        
False
        
None
        
ctypes
.
byref
(
keychain
)
    
)
    
_assert_no_error
(
status
)
    
return
keychain
tempdirectory
def
_load_items_from_file
(
keychain
path
)
:
    
"
"
"
    
Given
a
single
file
loads
all
the
trust
objects
from
it
into
arrays
and
    
the
keychain
.
    
Returns
a
tuple
of
lists
:
the
first
list
is
a
list
of
identities
the
    
second
a
list
of
certs
.
    
"
"
"
    
certificates
=
[
]
    
identities
=
[
]
    
result_array
=
None
    
with
open
(
path
'
rb
'
)
as
f
:
        
raw_filedata
=
f
.
read
(
)
    
try
:
        
filedata
=
CoreFoundation
.
CFDataCreate
(
            
CoreFoundation
.
kCFAllocatorDefault
            
raw_filedata
            
len
(
raw_filedata
)
        
)
        
result_array
=
CoreFoundation
.
CFArrayRef
(
)
        
result
=
Security
.
SecItemImport
(
            
filedata
            
None
            
None
            
None
            
0
            
None
            
keychain
            
ctypes
.
byref
(
result_array
)
        
)
        
_assert_no_error
(
result
)
        
result_count
=
CoreFoundation
.
CFArrayGetCount
(
result_array
)
        
for
index
in
range
(
result_count
)
:
            
item
=
CoreFoundation
.
CFArrayGetValueAtIndex
(
                
result_array
index
            
)
            
item
=
ctypes
.
cast
(
item
CoreFoundation
.
CFTypeRef
)
            
if
_is_cert
(
item
)
:
                
CoreFoundation
.
CFRetain
(
item
)
                
certificates
.
append
(
item
)
            
elif
_is_identity
(
item
)
:
                
CoreFoundation
.
CFRetain
(
item
)
                
identities
.
append
(
item
)
    
finally
:
        
if
result_array
:
            
CoreFoundation
.
CFRelease
(
result_array
)
        
CoreFoundation
.
CFRelease
(
filedata
)
    
return
(
identities
certificates
)
def
_load_client_cert_chain
(
keychain
*
paths
)
:
    
"
"
"
    
Load
certificates
and
maybe
keys
from
a
number
of
files
.
Has
the
end
goal
    
of
returning
a
CFArray
containing
one
SecIdentityRef
and
then
zero
or
more
    
SecCertificateRef
objects
suitable
for
use
as
a
client
certificate
trust
    
chain
.
    
"
"
"
    
certificates
=
[
]
    
identities
=
[
]
    
paths
=
(
path
for
path
in
paths
if
path
)
    
try
:
        
for
file_path
in
paths
:
            
new_identities
new_certs
=
_load_items_from_file
(
                
keychain
file_path
            
)
            
identities
.
extend
(
new_identities
)
            
certificates
.
extend
(
new_certs
)
        
if
not
identities
:
            
new_identity
=
Security
.
SecIdentityRef
(
)
            
status
=
Security
.
SecIdentityCreateWithCertificate
(
                
keychain
                
certificates
[
0
]
                
ctypes
.
byref
(
new_identity
)
            
)
            
_assert_no_error
(
status
)
            
identities
.
append
(
new_identity
)
            
CoreFoundation
.
CFRelease
(
certificates
.
pop
(
0
)
)
        
trust_chain
=
CoreFoundation
.
CFArrayCreateMutable
(
            
CoreFoundation
.
kCFAllocatorDefault
            
0
            
ctypes
.
byref
(
CoreFoundation
.
kCFTypeArrayCallBacks
)
        
)
        
for
item
in
itertools
.
chain
(
identities
certificates
)
:
            
CoreFoundation
.
CFArrayAppendValue
(
trust_chain
item
)
        
return
trust_chain
    
finally
:
        
for
obj
in
itertools
.
chain
(
identities
certificates
)
:
            
CoreFoundation
.
CFRelease
(
obj
)
