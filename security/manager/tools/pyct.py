"
"
"
Helper
library
for
creating
a
Signed
Certificate
Timestamp
given
the
details
of
a
signing
key
when
to
sign
and
the
certificate
data
to
sign
.
Currently
only
supports
precert_entry
types
.
See
RFC
6962
.
"
"
"
import
binascii
import
calendar
import
hashlib
from
struct
import
pack
import
pykey
from
pyasn1
.
codec
.
der
import
encoder
class
InvalidKeyError
(
Exception
)
:
    
"
"
"
Helper
exception
to
handle
unknown
key
types
.
"
"
"
    
def
__init__
(
self
key
)
:
        
self
.
key
=
key
    
def
__str__
(
self
)
:
        
return
'
Invalid
key
:
"
%
s
"
'
%
str
(
self
.
key
)
class
SCT
(
object
)
:
    
"
"
"
SCT
represents
a
Signed
Certificate
Timestamp
.
"
"
"
    
def
__init__
(
self
key
date
tbsCertificate
issuerKey
)
:
        
self
.
key
=
key
        
self
.
timestamp
=
calendar
.
timegm
(
date
.
timetuple
(
)
)
*
1000
        
self
.
tbsCertificate
=
tbsCertificate
        
self
.
issuerKey
=
issuerKey
    
def
signAndEncode
(
self
)
:
        
"
"
"
Returns
a
signed
and
encoded
representation
of
the
SCT
as
a
        
string
.
"
"
"
        
timestamp
=
pack
(
"
!
Q
"
self
.
timestamp
)
        
hasher
=
hashlib
.
sha256
(
)
        
hasher
.
update
(
encoder
.
encode
(
self
.
issuerKey
.
asSubjectPublicKeyInfo
(
)
)
)
        
issuer_key_hash
=
hasher
.
digest
(
)
        
len_prefix
=
pack
(
"
!
L
"
len
(
self
.
tbsCertificate
)
)
[
1
:
]
        
data
=
(
            
b
"
\
0
\
0
"
            
+
timestamp
            
+
b
"
\
0
\
1
"
            
+
issuer_key_hash
            
+
len_prefix
            
+
self
.
tbsCertificate
            
+
b
"
\
0
\
0
"
        
)
        
if
isinstance
(
self
.
key
pykey
.
ECCKey
)
:
            
signatureByte
=
b
"
\
3
"
        
elif
isinstance
(
self
.
key
pykey
.
RSAKey
)
:
            
signatureByte
=
b
"
\
1
"
        
else
:
            
raise
InvalidKeyError
(
self
.
key
)
        
hexSignature
=
self
.
key
.
sign
(
data
pykey
.
HASH_SHA256
)
        
signature
=
binascii
.
unhexlify
(
hexSignature
[
1
:
-
2
]
)
        
hasher
=
hashlib
.
sha256
(
)
        
hasher
.
update
(
encoder
.
encode
(
self
.
key
.
asSubjectPublicKeyInfo
(
)
)
)
        
key_id
=
hasher
.
digest
(
)
        
signature_len_prefix
=
pack
(
"
!
H
"
len
(
signature
)
)
        
return
(
            
b
"
\
0
"
            
+
key_id
            
+
timestamp
            
+
b
"
\
0
\
0
\
4
"
            
+
signatureByte
            
+
signature_len_prefix
            
+
signature
        
)
