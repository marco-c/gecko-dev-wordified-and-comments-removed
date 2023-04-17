import
hashlib
from
typing
import
TYPE_CHECKING
BinaryIO
Dict
Iterator
List
from
pip
.
_internal
.
exceptions
import
HashMismatch
HashMissing
InstallationError
from
pip
.
_internal
.
utils
.
misc
import
read_chunks
if
TYPE_CHECKING
:
    
from
hashlib
import
_Hash
    
from
typing
import
NoReturn
FAVORITE_HASH
=
"
sha256
"
STRONG_HASHES
=
[
"
sha256
"
"
sha384
"
"
sha512
"
]
class
Hashes
:
    
"
"
"
A
wrapper
that
builds
multiple
hashes
at
once
and
checks
them
against
    
known
-
good
values
    
"
"
"
    
def
__init__
(
self
hashes
=
None
)
:
        
"
"
"
        
:
param
hashes
:
A
dict
of
algorithm
names
pointing
to
lists
of
allowed
            
hex
digests
        
"
"
"
        
allowed
=
{
}
        
if
hashes
is
not
None
:
            
for
alg
keys
in
hashes
.
items
(
)
:
                
allowed
[
alg
]
=
sorted
(
keys
)
        
self
.
_allowed
=
allowed
    
def
__and__
(
self
other
)
:
        
if
not
isinstance
(
other
Hashes
)
:
            
return
NotImplemented
        
if
not
other
:
            
return
self
        
if
not
self
:
            
return
other
        
new
=
{
}
        
for
alg
values
in
other
.
_allowed
.
items
(
)
:
            
if
alg
not
in
self
.
_allowed
:
                
continue
            
new
[
alg
]
=
[
v
for
v
in
values
if
v
in
self
.
_allowed
[
alg
]
]
        
return
Hashes
(
new
)
    
property
    
def
digest_count
(
self
)
:
        
return
sum
(
len
(
digests
)
for
digests
in
self
.
_allowed
.
values
(
)
)
    
def
is_hash_allowed
(
        
self
        
hash_name
        
hex_digest
    
)
:
        
"
"
"
Return
whether
the
given
hex
digest
is
allowed
.
"
"
"
        
return
hex_digest
in
self
.
_allowed
.
get
(
hash_name
[
]
)
    
def
check_against_chunks
(
self
chunks
)
:
        
"
"
"
Check
good
hashes
against
ones
built
from
iterable
of
chunks
of
        
data
.
        
Raise
HashMismatch
if
none
match
.
        
"
"
"
        
gots
=
{
}
        
for
hash_name
in
self
.
_allowed
.
keys
(
)
:
            
try
:
                
gots
[
hash_name
]
=
hashlib
.
new
(
hash_name
)
            
except
(
ValueError
TypeError
)
:
                
raise
InstallationError
(
f
"
Unknown
hash
name
:
{
hash_name
}
"
)
        
for
chunk
in
chunks
:
            
for
hash
in
gots
.
values
(
)
:
                
hash
.
update
(
chunk
)
        
for
hash_name
got
in
gots
.
items
(
)
:
            
if
got
.
hexdigest
(
)
in
self
.
_allowed
[
hash_name
]
:
                
return
        
self
.
_raise
(
gots
)
    
def
_raise
(
self
gots
)
:
        
raise
HashMismatch
(
self
.
_allowed
gots
)
    
def
check_against_file
(
self
file
)
:
        
"
"
"
Check
good
hashes
against
a
file
-
like
object
        
Raise
HashMismatch
if
none
match
.
        
"
"
"
        
return
self
.
check_against_chunks
(
read_chunks
(
file
)
)
    
def
check_against_path
(
self
path
)
:
        
with
open
(
path
"
rb
"
)
as
file
:
            
return
self
.
check_against_file
(
file
)
    
def
__nonzero__
(
self
)
:
        
"
"
"
Return
whether
I
know
any
known
-
good
hashes
.
"
"
"
        
return
bool
(
self
.
_allowed
)
    
def
__bool__
(
self
)
:
        
return
self
.
__nonzero__
(
)
    
def
__eq__
(
self
other
)
:
        
if
not
isinstance
(
other
Hashes
)
:
            
return
NotImplemented
        
return
self
.
_allowed
=
=
other
.
_allowed
    
def
__hash__
(
self
)
:
        
return
hash
(
            
"
"
.
join
(
                
sorted
(
                    
"
:
"
.
join
(
(
alg
digest
)
)
                    
for
alg
digest_list
in
self
.
_allowed
.
items
(
)
                    
for
digest
in
digest_list
                
)
            
)
        
)
class
MissingHashes
(
Hashes
)
:
    
"
"
"
A
workalike
for
Hashes
used
when
we
'
re
missing
a
hash
for
a
requirement
    
It
computes
the
actual
hash
of
the
requirement
and
raises
a
HashMissing
    
exception
showing
it
to
the
user
.
    
"
"
"
    
def
__init__
(
self
)
:
        
"
"
"
Don
'
t
offer
the
hashes
kwarg
.
"
"
"
        
super
(
)
.
__init__
(
hashes
=
{
FAVORITE_HASH
:
[
]
}
)
    
def
_raise
(
self
gots
)
:
        
raise
HashMissing
(
gots
[
FAVORITE_HASH
]
.
hexdigest
(
)
)
