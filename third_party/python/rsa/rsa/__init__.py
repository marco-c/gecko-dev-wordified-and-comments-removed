"
"
"
RSA
module
Module
for
calculating
large
primes
and
RSA
encryption
decryption
signing
and
verification
.
Includes
generating
public
and
private
keys
.
WARNING
:
this
implementation
does
not
use
compression
of
the
cleartext
input
to
prevent
repetitions
or
other
common
security
improvements
.
Use
with
care
.
"
"
"
from
rsa
.
key
import
newkeys
PrivateKey
PublicKey
from
rsa
.
pkcs1
import
(
    
encrypt
    
decrypt
    
sign
    
verify
    
DecryptionError
    
VerificationError
    
find_signature_hash
    
sign_hash
    
compute_hash
)
__author__
=
"
Sybren
Stuvel
Barry
Mead
and
Yesudeep
Mangalapilly
"
__date__
=
"
2022
-
07
-
20
"
__version__
=
"
4
.
9
"
if
__name__
=
=
"
__main__
"
:
    
import
doctest
    
doctest
.
testmod
(
)
__all__
=
[
    
"
newkeys
"
    
"
encrypt
"
    
"
decrypt
"
    
"
sign
"
    
"
verify
"
    
"
PublicKey
"
    
"
PrivateKey
"
    
"
DecryptionError
"
    
"
VerificationError
"
    
"
find_signature_hash
"
    
"
compute_hash
"
    
"
sign_hash
"
]
