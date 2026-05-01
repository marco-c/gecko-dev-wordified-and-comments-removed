import
argparse
import
collections
import
difflib
import
hashlib
import
io
import
itertools
import
json
import
logging
import
os
.
path
import
re
import
subprocess
import
sys
import
textwrap
from
urllib
.
parse
import
urlparse
from
xml
.
sax
import
saxutils
import
requests
logging
.
basicConfig
(
level
=
logging
.
WARNING
)
ALL_ANDROID_TARGETS
=
[
    
"
armv7
-
linux
-
androideabi
"
    
"
aarch64
-
linux
-
android
"
    
"
aarch64
-
apple
-
darwin
"
    
"
x86_64
-
linux
-
android
"
    
"
x86_64
-
unknown
-
linux
-
gnu
"
    
"
x86_64
-
apple
-
darwin
"
    
"
x86_64
-
pc
-
windows
-
msvc
"
    
"
x86_64
-
pc
-
windows
-
gnu
"
]
ALL_IOS_TARGETS
=
(
    
[
"
fake
-
target
-
for
-
ios
"
]
    
if
sys
.
platform
!
=
"
darwin
"
    
else
[
"
x86_64
-
apple
-
ios
"
"
aarch64
-
apple
-
ios
"
]
)
ALL_TARGETS
=
ALL_ANDROID_TARGETS
+
ALL_IOS_TARGETS
LICENSES_IN_PREFERENCE_ORDER
=
[
    
"
MPL
-
2
.
0
"
    
"
Apache
-
2
.
0
"
    
"
MIT
"
    
"
CC0
-
1
.
0
"
    
"
ISC
"
    
"
BSD
-
2
-
Clause
"
    
"
BSD
-
3
-
Clause
"
    
"
Zlib
"
    
"
Unicode
-
3
.
0
"
    
"
EXT
-
OPENSSL
"
    
"
EXT
-
SQLITE
"
]
EXCLUDED_PACKAGES
=
set
(
    
[
        
"
cloudabi
"
        
"
fuchsia
-
cprng
"
        
"
fuchsia
-
zircon
"
        
"
fuchsia
-
zircon
-
sys
"
    
]
)
EXTRA_PACKAGE_METADATA
=
{
    
"
ext
-
jna
"
:
{
        
"
name
"
:
"
jna
"
        
"
repository
"
:
"
https
:
/
/
github
.
com
/
java
-
native
-
access
/
jna
"
        
"
license
"
:
"
Apache
-
2
.
0
"
        
"
license_file
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
java
-
native
-
access
/
jna
/
master
/
AL2
.
0
"
    
}
    
"
ext
-
protobuf
"
:
{
        
"
name
"
:
"
protobuf
"
        
"
repository
"
:
"
https
:
/
/
github
.
com
/
protocolbuffers
/
protobuf
"
        
"
license
"
:
"
BSD
-
3
-
Clause
"
        
"
license_file
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
protocolbuffers
/
protobuf
/
master
/
LICENSE
"
    
}
    
"
ext
-
nss
"
:
{
        
"
name
"
:
"
NSS
"
        
"
repository
"
:
"
https
:
/
/
hg
.
mozilla
.
org
/
projects
/
nss
"
        
"
license
"
:
"
MPL
-
2
.
0
"
        
"
license_file
"
:
"
https
:
/
/
hg
.
mozilla
.
org
/
projects
/
nss
/
raw
-
file
/
tip
/
COPYING
"
    
}
    
"
ext
-
nspr
"
:
{
        
"
name
"
:
"
NSPR
"
        
"
repository
"
:
"
https
:
/
/
hg
.
mozilla
.
org
/
projects
/
nspr
"
        
"
license
"
:
"
MPL
-
2
.
0
"
        
"
license_file
"
:
"
https
:
/
/
hg
.
mozilla
.
org
/
projects
/
nspr
/
raw
-
file
/
tip
/
LICENSE
"
    
}
    
"
ext
-
openssl
"
:
{
        
"
name
"
:
"
openssl
"
        
"
repository
"
:
"
https
:
/
/
www
.
openssl
.
org
/
source
/
"
        
"
license
"
:
"
EXT
-
OPENSSL
"
        
"
license_file
"
:
"
https
:
/
/
openssl
-
library
.
org
/
source
/
license
/
license
-
openssl
-
ssleay
.
txt
"
        
"
license_url
"
:
"
https
:
/
/
www
.
openssl
.
org
/
source
/
license
.
html
"
    
}
    
"
ext
-
ring
"
:
{
        
"
name
"
:
"
ring
"
        
"
repository
"
:
"
https
:
/
/
github
.
com
/
briansmith
/
ring
"
        
"
license
"
:
"
ISC
"
        
"
license_file
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
briansmith
/
ring
/
master
/
LICENSE
"
        
"
license_url
"
:
"
https
:
/
/
github
.
com
/
briansmith
/
ring
/
blob
/
master
/
LICENSE
"
        
"
license_text
"
:
textwrap
.
dedent
(
            
r
"
"
"
            
Copyright
2015
-
2016
Brian
Smith
.
            
Permission
to
use
copy
modify
and
/
or
distribute
this
software
for
any
            
purpose
with
or
without
fee
is
hereby
granted
provided
that
the
above
            
copyright
notice
and
this
permission
notice
appear
in
all
copies
.
            
THE
SOFTWARE
IS
PROVIDED
"
AS
IS
"
AND
THE
AUTHORS
DISCLAIM
ALL
WARRANTIES
            
WITH
REGARD
TO
THIS
SOFTWARE
INCLUDING
ALL
IMPLIED
WARRANTIES
OF
            
MERCHANTABILITY
AND
FITNESS
.
IN
NO
EVENT
SHALL
THE
AUTHORS
BE
LIABLE
FOR
ANY
            
SPECIAL
DIRECT
INDIRECT
OR
CONSEQUENTIAL
DAMAGES
OR
ANY
DAMAGES
            
WHATSOEVER
RESULTING
FROM
LOSS
OF
USE
DATA
OR
PROFITS
WHETHER
IN
AN
ACTION
            
OF
CONTRACT
NEGLIGENCE
OR
OTHER
TORTIOUS
ACTION
ARISING
OUT
OF
OR
IN
            
CONNECTION
WITH
THE
USE
OR
PERFORMANCE
OF
THIS
SOFTWARE
.
        
"
"
"
        
)
    
}
    
"
ext
-
sqlite
"
:
{
        
"
name
"
:
"
sqlite
"
        
"
repository
"
:
"
https
:
/
/
www
.
sqlite
.
org
/
"
        
"
license
"
:
"
EXT
-
SQLITE
"
        
"
license_file
"
:
"
https
:
/
/
sqlite
.
org
/
copyright
.
html
"
        
"
license_text
"
:
"
This
software
makes
use
of
the
'
SQLite
'
database
engine
and
we
are
very
"
        
"
grateful
to
D
.
Richard
Hipp
and
team
for
producing
it
.
"
    
}
}
PACKAGES_WITH_EXTRA_DEPENDENCIES
=
{
    
"
nss_sys
"
:
[
"
ext
-
nss
"
"
ext
-
nspr
"
]
    
"
openssl
-
sys
"
:
[
"
ext
-
openssl
"
]
    
"
rusqlite
"
:
[
"
ext
-
sqlite
"
]
    
"
rc_crypto
"
:
[
"
ext
-
ring
"
]
}
PACKAGE_METADATA_FIXUPS
=
{
    
"
adler32
"
:
{
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
remram44
/
adler32
-
rs
/
master
/
LICENSE
"
        
}
    
}
    
"
bincode
"
:
{
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
git
.
sr
.
ht
/
~
stygianentity
/
bincode
/
blob
/
trunk
/
LICENSE
.
md
"
        
}
    
}
    
"
tracing
"
:
{
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
tokio
-
rs
/
tracing
/
master
/
LICENSE
"
        
}
    
}
    
"
tracing
-
futures
"
:
{
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
tokio
-
rs
/
tracing
/
master
/
LICENSE
"
        
}
    
}
    
"
publicsuffix
"
:
{
        
"
license
"
:
{
"
check
"
:
"
MIT
/
Apache
-
2
.
0
"
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
LICENSE
-
APACHE
"
        
}
    
}
    
"
siphasher
"
:
{
        
"
license
"
:
{
"
check
"
:
"
MIT
/
Apache
-
2
.
0
"
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
COPYING
"
        
}
    
}
    
"
futures
-
task
"
:
{
        
"
license
"
:
{
"
check
"
:
"
MIT
OR
Apache
-
2
.
0
"
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
rust
-
lang
/
futures
-
rs
/
master
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
typenum
"
:
{
        
"
license
"
:
{
"
check
"
:
"
MIT
OR
Apache
-
2
.
0
"
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
LICENSE
-
APACHE
"
        
}
    
}
    
"
ohttp
"
:
{
        
"
license
"
:
{
"
check
"
:
"
MIT
OR
Apache
-
2
.
0
"
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
martinthomson
/
ohttp
/
main
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
openssl
"
:
{
        
"
license
"
:
{
"
check
"
:
"
Apache
-
2
.
0
"
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
sfackler
/
rust
-
openssl
/
refs
/
heads
/
master
/
openssl
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
bhttp
"
:
{
        
"
license
"
:
{
"
check
"
:
"
MIT
OR
Apache
-
2
.
0
"
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
martinthomson
/
ohttp
/
main
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
backtrace
-
sys
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
alexcrichton
/
backtrace
-
rs
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
rust
-
lang
/
backtrace
-
rs
/
master
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
base16
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
thomcc
/
rust
-
base16
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
thomcc
/
rust
-
base16
/
master
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
bitvec
"
:
{
        
"
license
"
:
{
            
"
check
"
:
"
MIT
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
bitvecto
-
rs
/
bitvec
/
develop
/
LICENSE
.
txt
"
        
}
    
}
    
"
cargo
-
platform
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
rust
-
lang
/
cargo
"
        
}
        
"
license
"
:
{
"
check
"
:
"
MIT
OR
Apache
-
2
.
0
"
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
rust
-
lang
/
cargo
/
master
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
failure_derive
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
rust
-
lang
-
nursery
/
failure
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
rust
-
lang
-
nursery
/
failure
/
master
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
funty
"
:
{
        
"
license
"
:
{
            
"
check
"
:
"
MIT
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
myrrlyn
/
funty
/
master
/
LICENSE
.
txt
"
        
}
    
}
    
"
fxhash
"
:
{
        
"
license
"
:
{
"
check
"
:
"
Apache
-
2
.
0
/
MIT
"
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
www
.
apache
.
org
/
licenses
/
LICENSE
-
2
.
0
.
txt
"
        
}
    
}
    
"
hawk
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
taskcluster
/
rust
-
hawk
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
taskcluster
/
rust
-
hawk
/
main
/
LICENSE
"
        
}
    
}
    
"
libm
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
rust
-
lang
/
libm
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
rust
-
lang
/
libm
/
blob
/
master
/
libm
/
LICENSE
.
txt
"
        
}
    
}
    
"
oneshot
-
uniffi
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
faern
/
oneshot
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
www
.
apache
.
org
/
licenses
/
LICENSE
-
2
.
0
.
txt
"
        
}
    
}
    
"
windows
-
sys
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
microsoft
/
windows
-
rs
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
microsoft
/
windows
-
rs
/
master
/
license
-
mit
"
        
}
    
}
    
"
windows
-
targets
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
microsoft
/
windows
-
rs
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
microsoft
/
windows
-
rs
/
master
/
license
-
mit
"
        
}
    
}
    
"
windows_x86_64_msvc
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
microsoft
/
windows
-
rs
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
microsoft
/
windows
-
rs
/
master
/
license
-
mit
"
        
}
    
}
    
"
windows_x86_64_gnu
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
microsoft
/
windows
-
rs
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
microsoft
/
windows
-
rs
/
master
/
license
-
mit
"
        
}
    
}
    
"
kernel32
-
sys
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
retep998
/
winapi
-
rs
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
retep998
/
winapi
-
rs
/
0
.
3
/
LICENSE
-
MIT
"
        
}
    
}
    
"
libsqlite3
-
sys
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
rusqlite
/
rusqlite
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
rusqlite
/
rusqlite
/
master
/
LICENSE
"
        
}
    
}
    
"
miniz_oxide
"
:
{
        
"
license
"
:
{
"
check
"
:
"
MIT
OR
Zlib
OR
Apache
-
2
.
0
"
"
fixup
"
:
"
MIT
"
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
Frommi
/
miniz_oxide
/
master
/
miniz_oxide
/
LICENSE
-
MIT
.
md
"
        
}
    
}
    
"
parking_lot_core
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
Amanieu
/
parking_lot
"
        
}
        
"
licence
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
Apache
-
2
.
0
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
Amanieu
/
parking_lot
/
blob
/
master
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
phf
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
sfackler
/
rust
-
phf
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
sfackler
/
rust
-
phf
/
master
/
LICENSE
"
        
}
    
}
    
"
phf_codegen
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
sfackler
/
rust
-
phf
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
sfackler
/
rust
-
phf
/
master
/
LICENSE
"
        
}
    
}
    
"
phf_generator
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
sfackler
/
rust
-
phf
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
sfackler
/
rust
-
phf
/
master
/
LICENSE
"
        
}
    
}
    
"
phf_shared
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
sfackler
/
rust
-
phf
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
sfackler
/
rust
-
phf
/
master
/
LICENSE
"
        
}
    
}
    
"
prost
-
build
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
tokio
-
rs
/
prost
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
tokio
-
rs
/
prost
/
master
/
LICENSE
"
        
}
    
}
    
"
prost
-
derive
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
tokio
-
rs
/
prost
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
tokio
-
rs
/
prost
/
master
/
LICENSE
"
        
}
    
}
    
"
prost
-
types
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
tokio
-
rs
/
prost
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
tokio
-
rs
/
prost
/
master
/
LICENSE
"
        
}
    
}
    
"
radium
"
:
{
        
"
license
"
:
{
"
check
"
:
"
MIT
"
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
bitvecto
-
rs
/
radium
/
master
/
LICENSE
.
txt
"
        
}
    
}
    
"
security
-
framework
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
kornelski
/
rust
-
security
-
framework
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
kornelski
/
rust
-
security
-
framework
/
master
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
security
-
framework
-
sys
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
kornelski
/
rust
-
security
-
framework
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
kornelski
/
rust
-
security
-
framework
/
master
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
shlex
"
:
{
        
"
repository
"
:
{
"
check
"
:
"
https
:
/
/
github
.
com
/
comex
/
rust
-
shlex
"
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
www
.
apache
.
org
/
licenses
/
LICENSE
-
2
.
0
.
txt
"
        
}
    
}
    
"
tinyvec_macros
"
:
{
        
"
license
"
:
{
"
check
"
:
"
MIT
OR
Apache
-
2
.
0
OR
Zlib
"
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
Soveu
/
tinyvec_macros
/
master
/
LICENSE
-
APACHE
.
md
"
        
}
    
}
    
"
url_serde
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
servo
/
rust
-
url
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
servo
/
rust
-
url
/
master
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
winapi
-
build
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
retep998
/
winapi
-
rs
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
retep998
/
winapi
-
rs
/
0
.
3
/
LICENSE
-
MIT
"
        
}
    
}
    
"
winapi
-
x86_64
-
pc
-
windows
-
gnu
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
retep998
/
winapi
-
rs
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
retep998
/
winapi
-
rs
/
0
.
3
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
ws2_32
-
sys
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
retep998
/
winapi
-
rs
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
retep998
/
winapi
-
rs
/
0
.
3
/
LICENSE
-
MIT
"
        
}
    
}
    
"
wyz
"
:
{
        
"
license
"
:
{
            
"
check
"
:
"
MIT
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
myrrlyn
/
wyz
/
main
/
LICENSE
.
txt
"
        
}
    
}
    
"
proc
-
macro
-
error
"
:
{
        
"
license
"
:
{
"
check
"
:
"
MIT
OR
Apache
-
2
.
0
"
}
        
"
repository
"
:
{
"
check
"
:
"
https
:
/
/
gitlab
.
com
/
CreepySkeleton
/
proc
-
macro
-
error
"
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
gitlab
.
com
/
CreepySkeleton
/
proc
-
macro
-
error
/
-
/
raw
/
master
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
proc
-
macro
-
error
-
attr
"
:
{
        
"
license
"
:
{
"
check
"
:
"
MIT
OR
Apache
-
2
.
0
"
}
        
"
repository
"
:
{
"
check
"
:
"
https
:
/
/
gitlab
.
com
/
CreepySkeleton
/
proc
-
macro
-
error
"
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
gitlab
.
com
/
CreepySkeleton
/
proc
-
macro
-
error
/
-
/
raw
/
master
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
minimal
-
lexical
"
:
{
        
"
license
"
:
{
            
"
check
"
:
"
MIT
/
Apache
-
2
.
0
"
        
}
        
"
repository
"
:
{
"
check
"
:
"
https
:
/
/
github
.
com
/
Alexhuszagh
/
minimal
-
lexical
"
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
Alexhuszagh
/
minimal
-
lexical
/
blob
/
main
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
c2
-
chacha
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
cryptocorrosion
/
cryptocorrosion
"
        
}
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
cryptocorrosion
/
cryptocorrosion
/
blob
/
master
/
stream
-
ciphers
/
chacha
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
ffi
-
support
"
:
{
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
mozilla
/
ffi
-
support
/
main
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
mime
"
:
{
        
"
version
"
:
{
            
"
check
"
:
"
0
.
3
.
17
"
        
}
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
hyperium
/
mime
/
blob
/
v0
.
3
.
17
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
ppv
-
lite86
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
cryptocorrosion
/
cryptocorrosion
"
        
}
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
cryptocorrosion
/
cryptocorrosion
/
blob
/
master
/
utils
-
simd
/
ppv
-
lite86
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
time
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
time
-
rs
/
time
"
        
}
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
time
-
rs
/
time
/
blob
/
master
/
LICENSE
-
Apache
"
        
}
    
}
    
"
winapi
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
"
https
:
/
/
github
.
com
/
retep998
/
winapi
-
rs
"
        
}
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
retep998
/
winapi
-
rs
/
blob
/
master
/
LICENSE
-
MIT
"
        
}
    
}
    
"
tinyvec
"
:
{
        
"
repository
"
:
{
"
check
"
:
"
https
:
/
/
github
.
com
/
Lokathor
/
tinyvec
"
}
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
Lokathor
/
tinyvec
/
blob
/
main
/
LICENSE
-
ZLIB
.
md
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
Lokathor
/
tinyvec
/
main
/
LICENSE
-
ZLIB
.
md
"
        
}
    
}
    
"
glean
-
core
"
:
{
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
mozilla
/
glean
/
blob
/
main
/
LICENSE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
mozilla
/
glean
/
main
/
LICENSE
"
        
}
    
}
    
"
glean
-
ffi
"
:
{
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
mozilla
/
glean
/
blob
/
main
/
LICENSE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
mozilla
/
glean
/
main
/
LICENSE
"
        
}
    
}
    
"
lmdb
-
rkv
-
sys
"
:
{
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
mozilla
/
lmdb
-
rs
/
blob
/
master
/
LICENSE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
mozilla
/
lmdb
-
rs
/
master
/
LICENSE
"
        
}
    
}
    
"
uniffi_bindgen
"
:
{
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
mozilla
/
uniffi
-
rs
/
blob
/
main
/
LICENSE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
mozilla
/
uniffi
-
rs
/
main
/
LICENSE
"
        
}
    
}
    
"
uniffi_build
"
:
{
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
mozilla
/
uniffi
-
rs
/
blob
/
main
/
LICENSE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
mozilla
/
uniffi
-
rs
/
main
/
LICENSE
"
        
}
    
}
    
"
uniffi_checksum_derive
"
:
{
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
mozilla
/
uniffi
-
rs
/
blob
/
main
/
LICENSE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
mozilla
/
uniffi
-
rs
/
main
/
LICENSE
"
        
}
    
}
    
"
uniffi_core
"
:
{
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
mozilla
/
uniffi
-
rs
/
blob
/
main
/
LICENSE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
mozilla
/
uniffi
-
rs
/
main
/
LICENSE
"
        
}
    
}
    
"
uniffi_internal_macros
"
:
{
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
mozilla
/
uniffi
-
rs
/
blob
/
main
/
LICENSE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
mozilla
/
uniffi
-
rs
/
main
/
LICENSE
"
        
}
    
}
    
"
uniffi_macros
"
:
{
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
mozilla
/
uniffi
-
rs
/
blob
/
main
/
LICENSE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
mozilla
/
uniffi
-
rs
/
main
/
LICENSE
"
        
}
    
}
    
"
uniffi_meta
"
:
{
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
mozilla
/
uniffi
-
rs
/
blob
/
main
/
LICENSE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
mozilla
/
uniffi
-
rs
/
main
/
LICENSE
"
        
}
    
}
    
"
uniffi_pipeline
"
:
{
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
mozilla
/
uniffi
-
rs
/
blob
/
main
/
LICENSE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
mozilla
/
uniffi
-
rs
/
main
/
LICENSE
"
        
}
    
}
    
"
uniffi_testing
"
:
{
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
mozilla
/
uniffi
-
rs
/
blob
/
main
/
LICENSE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
mozilla
/
uniffi
-
rs
/
main
/
LICENSE
"
        
}
    
}
    
"
uniffi_udl
"
:
{
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
mozilla
/
uniffi
-
rs
/
blob
/
main
/
LICENSE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
mozilla
/
uniffi
-
rs
/
main
/
LICENSE
"
        
}
    
}
    
"
uniffi
"
:
{
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
mozilla
/
uniffi
-
rs
/
blob
/
main
/
LICENSE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
mozilla
/
uniffi
-
rs
/
main
/
LICENSE
"
        
}
    
}
    
"
jexl
-
eval
"
:
{
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
mozilla
/
jexl
-
rs
/
blob
/
main
/
LICENSE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
mozilla
/
jexl
-
rs
/
main
/
LICENSE
"
        
}
    
}
    
"
jexl
-
parser
"
:
{
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
mozilla
/
jexl
-
rs
/
blob
/
main
/
LICENSE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
mozilla
/
jexl
-
rs
/
main
/
LICENSE
"
        
}
    
}
    
"
lalrpop
-
util
"
:
{
        
"
license
"
:
{
            
"
check
"
:
"
Apache
-
2
.
0
/
MIT
"
        
}
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
lalrpop
/
lalrpop
/
blob
/
master
/
LICENSE
-
APACHE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
lalrpop
/
lalrpop
/
master
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
humansize
"
:
{
        
"
license
"
:
{
            
"
check
"
:
"
MIT
/
Apache
-
2
.
0
"
        
}
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
LeopoldArkham
/
humansize
/
blob
/
master
/
LICENSE
-
APACHE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
LeopoldArkham
/
humansize
/
master
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
encoding_rs
"
:
{
        
"
license
"
:
{
            
"
check
"
:
"
(
Apache
-
2
.
0
OR
MIT
)
AND
BSD
-
3
-
Clause
"
        
}
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
hsivonen
/
encoding_rs
/
blob
/
master
/
COPYRIGHT
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
hsivonen
/
encoding_rs
/
master
/
COPYRIGHT
"
        
}
    
}
    
"
enum_variant_macros_macros
"
:
{
        
"
license
"
:
{
            
"
check
"
:
"
MIT
OR
Apache
-
2
.
0
"
        
}
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
MisterEggnog
/
enum
-
variant
-
macros
/
blob
/
trunk
/
LICENSE
-
APACHE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
MisterEggnog
/
enum
-
variant
-
macros
/
trunk
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
extension
-
trait
"
:
{
        
"
license
"
:
{
            
"
check
"
:
"
MIT
OR
Apache
-
2
.
0
"
        
}
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
gitlab
.
com
/
KonradBorowski
/
extension
-
trait
/
-
/
blob
/
master
/
LICENSE
-
APACHE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
gitlab
.
com
/
KonradBorowski
/
extension
-
trait
/
-
/
raw
/
master
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
unicode
-
ident
"
:
{
        
"
license
"
:
{
            
"
check
"
:
"
(
MIT
OR
Apache
-
2
.
0
)
AND
Unicode
-
3
.
0
"
        
}
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
dtolnay
/
unicode
-
ident
/
LICENSE
-
APACHE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
dtolnay
/
unicode
-
ident
/
master
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
xshell
-
macros
"
:
{
        
"
license
"
:
{
            
"
check
"
:
"
MIT
OR
Apache
-
2
.
0
"
        
}
        
"
license_url
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
matklad
/
xshell
/
blob
/
master
/
LICENSE
-
APACHE
"
        
}
        
"
license_file
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
matklad
/
xshell
/
master
/
LICENSE
-
APACHE
"
        
}
    
}
    
"
openssl
-
macros
"
:
{
        
"
repository
"
:
{
            
"
check
"
:
None
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
sfackler
/
rust
-
openssl
"
        
}
    
}
    
"
windows
-
link
"
:
{
        
"
license_url
"
:
{
            
"
fixup
"
:
"
https
:
/
/
github
.
com
/
microsoft
/
windows
-
rs
/
blob
/
master
/
license
-
apache
-
2
.
0
"
        
}
        
"
license_file
"
:
{
            
"
fixup
"
:
"
https
:
/
/
raw
.
githubusercontent
.
com
/
microsoft
/
windows
-
rs
/
master
/
license
-
apache
-
2
.
0
"
        
}
    
}
}
COMMON_LICENSE_FILE_NAME_ROOTS
=
{
    
"
"
:
[
"
license
"
"
licence
"
]
    
"
Apache
-
2
.
0
"
:
[
"
license
-
apache
"
"
licence
-
apache
"
]
    
"
MIT
"
:
[
"
license
-
mit
"
"
licence
-
mit
"
]
    
"
CC0
"
:
[
"
license
-
cc0
"
"
licence
-
cc0
"
]
    
"
Zlib
"
:
[
"
license
-
zlib
"
"
license
-
zlib
"
]
}
COMMON_LICENSE_FILE_NAME_SUFFIXES
=
[
"
"
"
.
md
"
"
.
txt
"
]
COMMON_LICENSE_FILE_NAMES
=
{
}
for
license
in
COMMON_LICENSE_FILE_NAME_ROOTS
:
    
COMMON_LICENSE_FILE_NAMES
[
license
]
=
set
(
)
    
for
suffix
in
COMMON_LICENSE_FILE_NAME_SUFFIXES
:
        
for
root
in
COMMON_LICENSE_FILE_NAME_ROOTS
[
license
]
:
            
COMMON_LICENSE_FILE_NAMES
[
license
]
.
add
(
root
+
suffix
)
        
for
root
in
COMMON_LICENSE_FILE_NAME_ROOTS
[
"
"
]
:
            
COMMON_LICENSE_FILE_NAMES
[
license
]
.
add
(
root
+
suffix
)
def
subprocess_run_cargo
(
args
)
:
    
"
"
"
Run
cargo
as
a
subprocess
returning
stdout
.
"
"
"
    
env
=
os
.
environ
.
copy
(
)
    
p
=
subprocess
.
run
(
        
(
"
cargo
"
)
+
args
        
env
=
env
        
stdout
=
subprocess
.
PIPE
        
text
=
True
        
check
=
False
    
)
    
p
.
check_returncode
(
)
    
return
p
.
stdout
def
get_workspace_metadata
(
)
:
    
"
"
"
Get
metadata
for
all
dependencies
in
the
workspace
.
"
"
"
    
return
WorkspaceMetadata
(
        
json
.
loads
(
            
subprocess_run_cargo
(
(
"
metadata
"
"
-
-
locked
"
"
-
-
format
-
version
"
"
1
"
)
)
        
)
    
)
class
WorkspaceMetadata
:
    
"
"
"
Package
metadata
for
all
dependencies
in
the
workspace
.
    
This
uses
cargo
metadata
to
load
the
complete
set
of
package
metadata
for
the
dependency
tree
    
of
our
workspace
.
This
typically
lists
too
many
packages
because
it
does
a
union
of
all
features
    
required
by
all
packages
in
the
workspace
.
Use
the
get_package_dependencies
to
obtain
the
    
set
of
dependencies
for
a
specific
package
based
on
its
build
plan
.
    
For
the
JSON
data
format
ref
https
:
/
/
doc
.
rust
-
lang
.
org
/
cargo
/
commands
/
cargo
-
metadata
.
html
    
"
"
"
    
def
__init__
(
self
metadata
)
:
        
self
.
metadata
=
metadata
        
self
.
pkgInfoById
=
{
}
        
self
.
pkgInfoByManifestPath
=
{
}
        
self
.
workspaceMembersByName
=
{
}
        
for
info
in
metadata
[
"
packages
"
]
:
            
if
info
[
"
name
"
]
in
EXCLUDED_PACKAGES
:
                
continue
            
if
info
[
"
name
"
]
in
PACKAGE_METADATA_FIXUPS
:
                
fixups
=
PACKAGE_METADATA_FIXUPS
[
info
[
"
name
"
]
]
                
for
key
change
in
fixups
.
items
(
)
:
                    
if
info
.
get
(
key
)
!
=
change
.
get
(
"
check
"
)
:
                        
assert
False
"
Fixup
check
failed
for
{
}
.
{
}
:
{
}
!
=
{
}
"
.
format
(
                            
info
[
"
name
"
]
key
info
.
get
(
key
None
)
change
[
"
check
"
]
                        
)
                    
if
"
fixup
"
in
change
:
                        
info
[
key
]
=
change
[
"
fixup
"
]
            
assert
info
[
"
id
"
]
not
in
self
.
pkgInfoById
            
self
.
pkgInfoById
[
info
[
"
id
"
]
]
=
info
            
assert
info
[
"
manifest_path
"
]
not
in
self
.
pkgInfoByManifestPath
            
self
.
pkgInfoByManifestPath
[
info
[
"
manifest_path
"
]
]
=
info
        
for
name
info
in
EXTRA_PACKAGE_METADATA
.
items
(
)
:
            
assert
name
not
in
self
.
pkgInfoById
            
self
.
pkgInfoById
[
name
]
=
info
.
copy
(
)
        
for
id
in
metadata
[
"
workspace_members
"
]
:
            
name
=
self
.
pkgInfoById
[
id
]
[
"
name
"
]
            
assert
name
not
in
self
.
workspaceMembersByName
            
self
.
workspaceMembersByName
[
name
]
=
id
    
def
has_package
(
self
id
)
:
        
return
id
in
self
.
pkgInfoById
    
def
get_package_by_id
(
self
id
)
:
        
return
self
.
pkgInfoById
[
id
]
    
def
get_package_by_manifest_path
(
self
path
)
:
        
return
self
.
pkgInfoByManifestPath
[
path
]
    
def
get_dependency_summary
(
self
packages
targets
=
None
)
:
        
"
"
"
Get
dependency
and
license
summary
information
.
        
This
method
will
yield
dependency
summary
information
for
the
named
package
.
When
the
targets
        
argument
is
specified
it
will
yield
information
for
the
named
package
when
compiled
for
just
        
those
targets
.
        
"
"
"
        
deps
=
set
(
)
        
for
package
in
packages
:
            
deps
|
=
self
.
get_package_dependencies
(
package
targets
)
        
for
id
in
deps
:
            
if
not
self
.
is_external_dependency
(
id
)
:
                
continue
            
yield
self
.
get_license_info
(
id
)
    
def
get_package_dependencies
(
self
name
targets
=
None
)
:
        
"
"
"
Get
the
set
of
dependencies
for
the
named
package
when
compiling
for
the
specified
targets
.
        
This
implementation
uses
cargo
build
-
-
build
-
plan
to
list
all
inputs
to
the
build
process
.
        
It
has
the
advantage
of
being
guaranteed
to
correspond
to
what
'
s
included
in
the
actual
build
        
but
requires
using
unstable
cargo
features
and
hence
cargo
nightly
.
        
"
"
"
        
targets
=
self
.
get_compatible_targets_for_package
(
name
targets
)
        
cargo_args
=
(
            
"
+
nightly
-
2025
-
11
-
08
"
            
"
-
Z
"
            
"
unstable
-
options
"
            
"
build
"
            
"
-
-
build
-
plan
"
            
"
-
-
quiet
"
            
"
-
-
locked
"
            
"
-
-
package
"
            
name
        
)
        
deps
=
set
(
)
        
for
target
in
targets
:
            
this_target
=
(
                
"
x86_64
-
apple
-
darwin
"
if
target
=
=
"
fake
-
target
-
for
-
ios
"
else
target
            
)
            
buildPlan
=
subprocess_run_cargo
(
                
cargo_args
                
+
(
                    
"
-
-
target
"
                    
this_target
                
)
            
)
            
buildPlan
=
json
.
loads
(
buildPlan
)
            
for
manifestPath
in
buildPlan
[
"
inputs
"
]
:
                
info
=
self
.
get_package_by_manifest_path
(
manifestPath
)
                
deps
.
add
(
info
[
"
id
"
]
)
        
deps
|
=
self
.
get_extra_dependencies_not_managed_by_cargo
(
name
targets
deps
)
        
return
deps
    
def
get_extra_dependencies_not_managed_by_cargo
(
self
name
targets
deps
)
:
        
"
"
"
Get
additional
dependencies
for
things
managed
outside
of
cargo
.
        
This
includes
optional
C
libraries
like
SQLCipher
as
well
as
platform
-
specific
        
dependencies
for
our
various
language
bindings
.
        
"
"
"
        
extras
=
set
(
)
        
for
target
in
targets
:
            
if
self
.
target_is_android
(
target
)
:
                
extras
.
add
(
"
ext
-
jna
"
)
                
extras
.
add
(
"
ext
-
protobuf
"
)
        
for
dep
in
deps
:
            
name
=
self
.
pkgInfoById
[
dep
]
[
"
name
"
]
            
if
name
in
PACKAGES_WITH_EXTRA_DEPENDENCIES
:
                
extras
|
=
set
(
PACKAGES_WITH_EXTRA_DEPENDENCIES
[
name
]
)
        
return
extras
    
def
get_compatible_targets_for_package
(
self
name
targets
=
None
)
:
        
"
"
"
Get
the
set
of
targets
that
are
compatible
with
the
named
package
.
        
Some
targets
(
e
.
g
.
iOS
)
cannot
build
certains
types
of
package
(
e
.
g
.
cdylib
)
        
so
we
use
this
method
to
filter
the
set
of
targets
based
on
package
type
.
        
"
"
"
        
if
not
targets
:
            
targets
=
ALL_TARGETS
        
elif
isinstance
(
targets
str
)
:
            
targets
=
(
targets
)
        
pkgInfo
=
self
.
pkgInfoById
[
self
.
workspaceMembersByName
[
name
]
]
        
for
buildTarget
in
pkgInfo
[
"
targets
"
]
:
            
if
"
cdylib
"
in
buildTarget
[
"
kind
"
]
:
                
targets
=
[
                    
target
for
target
in
targets
if
not
self
.
target_is_ios
(
target
)
                
]
        
return
targets
    
def
target_is_android
(
self
target
)
:
        
"
"
"
Determine
whether
the
given
build
target
is
for
an
android
platform
.
"
"
"
        
if
target
.
endswith
(
"
-
android
"
)
or
target
.
endswith
(
"
-
androideabi
"
)
:
            
return
True
        
return
False
    
def
target_is_ios
(
self
target
)
:
        
"
"
"
Determine
whether
the
given
build
target
is
for
an
iOS
platform
.
"
"
"
        
if
target
.
endswith
(
"
-
ios
"
)
:
            
return
True
        
return
False
    
def
is_external_dependency
(
self
id
)
:
        
"
"
"
Check
whether
the
named
package
is
an
external
dependency
.
"
"
"
        
pkgInfo
=
self
.
pkgInfoById
[
id
]
        
try
:
            
if
pkgInfo
[
"
source
"
]
is
not
None
:
                
return
True
        
except
KeyError
:
            
return
True
        
manifest
=
pkgInfo
[
"
manifest_path
"
]
        
root
=
os
.
path
.
commonprefix
(
[
manifest
self
.
metadata
[
"
workspace_root
"
]
]
)
        
if
root
!
=
self
.
metadata
[
"
workspace_root
"
]
:
            
return
True
        
return
False
    
def
get_manifest_path
(
self
id
)
:
        
"
"
"
Get
the
path
to
a
package
'
s
Cargo
manifest
.
"
"
"
        
return
self
.
pkgInfoById
[
id
]
[
"
manifest_path
"
]
    
def
get_license_info
(
self
id
)
:
        
"
"
"
Get
the
licensing
info
for
the
named
dependency
or
error
if
it
can
'
t
be
determined
.
"
"
"
        
pkgInfo
=
self
.
pkgInfoById
[
id
]
        
chosenLicense
=
self
.
pick_most_acceptable_license
(
id
pkgInfo
[
"
license
"
]
)
        
licenseFile
=
self
.
_find_license_file
(
id
chosenLicense
pkgInfo
)
        
assert
pkgInfo
[
"
name
"
]
is
not
None
        
assert
pkgInfo
[
"
repository
"
]
is
not
None
        
return
{
            
"
name
"
:
pkgInfo
[
"
name
"
]
            
"
id
"
:
pkgInfo
.
get
(
                
"
id
"
pkgInfo
[
"
name
"
]
            
)
            
"
repository
"
:
pkgInfo
[
"
repository
"
]
            
"
license
"
:
chosenLicense
            
"
license_file
"
:
licenseFile
            
"
license_text
"
:
self
.
_fetch_license_text
(
id
licenseFile
pkgInfo
)
            
"
license_url
"
:
self
.
_find_license_url
(
                
id
chosenLicense
licenseFile
pkgInfo
            
)
        
}
    
def
pick_most_acceptable_license
(
self
id
licenseId
)
:
        
"
"
"
Select
the
best
license
under
which
to
redistribute
a
dependency
.
        
This
parses
the
SPDX
-
style
license
identifiers
included
in
our
dependencies
        
and
selects
the
best
license
for
our
needs
where
"
best
"
is
a
subjective
judgement
        
based
on
whether
it
'
s
acceptable
at
all
and
then
how
convenient
it
is
to
work
with
        
here
in
the
license
summary
tool
.
.
.
        
"
"
"
        
if
licenseId
=
=
"
(
Apache
-
2
.
0
OR
MIT
)
AND
BSD
-
3
-
Clause
"
:
            
return
licenseId
        
if
licenseId
=
=
"
(
MIT
OR
Apache
-
2
.
0
)
AND
Unicode
-
3
.
0
"
:
            
return
licenseId
        
licenses
=
set
(
l
.
strip
(
)
for
l
in
re
.
split
(
r
"
\
s
*
(
?
:
/
|
\
sOR
\
s
)
\
s
*
"
licenseId
)
)
        
for
license
in
LICENSES_IN_PREFERENCE_ORDER
:
            
if
license
in
licenses
:
                
return
license
        
raise
RuntimeError
(
            
f
"
Could
not
determine
acceptable
license
for
{
id
}
;
license
is
'
{
licenseId
}
'
"
        
)
    
def
_find_license_file
(
self
id
license
pkgInfo
)
:
        
logging
.
info
(
"
finding
license
file
for
%
s
"
id
)
        
licenseFile
=
pkgInfo
.
get
(
"
license_file
"
None
)
        
if
licenseFile
is
not
None
:
            
return
licenseFile
        
pkgRoot
=
os
.
path
.
dirname
(
pkgInfo
[
"
manifest_path
"
]
)
        
try
:
            
licenseFileNames
=
COMMON_LICENSE_FILE_NAMES
[
license
]
        
except
KeyError
:
            
licenseFileNames
=
COMMON_LICENSE_FILE_NAMES
[
"
"
]
        
logging
.
debug
(
"
candidate
license
filenames
:
%
s
"
licenseFileNames
)
        
foundLicenseFiles
=
[
            
nm
for
nm
in
os
.
listdir
(
pkgRoot
)
if
nm
.
lower
(
)
in
licenseFileNames
        
]
        
if
len
(
foundLicenseFiles
)
=
=
1
:
            
return
foundLicenseFiles
[
0
]
        
if
len
(
foundLicenseFiles
)
>
1
:
            
err
=
"
Multiple
ambiguous
license
files
found
for
'
{
}
'
.
\
n
"
.
format
(
                
pkgInfo
[
"
name
"
]
            
)
            
err
+
=
"
Please
select
the
correct
license
file
and
add
it
to
PACKAGE_METADATA_FIXUPS
.
\
n
"
            
err
+
=
f
"
Potential
license
files
:
{
foundLicenseFiles
}
"
        
else
:
            
err
=
"
Could
not
find
license
file
for
'
{
}
'
.
\
n
"
.
format
(
pkgInfo
[
"
name
"
]
)
            
err
+
=
"
Please
locate
the
correct
license
file
and
add
it
to
PACKAGE_METADATA_FIXUPS
.
\
n
"
            
err
+
=
"
You
may
need
to
poke
around
in
the
source
repository
at
{
}
"
.
format
(
                
pkgInfo
[
"
repository
"
]
            
)
        
raise
RuntimeError
(
err
)
    
def
_fetch_license_text
(
self
id
licenseFile
pkgInfo
)
:
        
if
"
license_text
"
in
pkgInfo
:
            
return
pkgInfo
[
"
license_text
"
]
        
if
licenseFile
.
startswith
(
"
https
:
/
/
"
)
:
            
r
=
requests
.
get
(
licenseFile
)
            
r
.
raise_for_status
(
)
            
return
r
.
content
.
decode
(
"
utf8
"
)
        
else
:
            
pkgRoot
=
os
.
path
.
dirname
(
pkgInfo
[
"
manifest_path
"
]
)
            
with
open
(
os
.
path
.
join
(
pkgRoot
licenseFile
)
)
as
f
:
                
return
f
.
read
(
)
    
def
_find_license_url
(
self
id
chosenLicense
licenseFile
pkgInfo
)
:
        
"
"
"
Find
an
appropriate
URL
at
which
humans
can
view
a
project
'
s
license
.
"
"
"
        
licenseUrl
=
pkgInfo
.
get
(
"
license_url
"
)
        
if
licenseUrl
is
not
None
:
            
return
licenseUrl
        
if
urlparse
(
licenseFile
)
.
scheme
:
            
licenseUrl
=
licenseFile
        
else
:
            
repo
=
pkgInfo
[
"
repository
"
]
            
if
repo
:
                
if
repo
.
startswith
(
"
http
:
/
/
github
.
com
/
"
)
:
                    
repo
=
repo
.
replace
(
"
http
:
/
/
"
"
https
:
/
/
"
)
                
if
repo
.
startswith
(
"
https
:
/
/
github
.
com
/
"
)
:
                    
for
strip_suffix
in
[
                        
"
.
git
"
                        
"
/
tree
/
main
/
{
}
"
.
format
(
pkgInfo
[
"
name
"
]
)
                        
"
/
tree
/
master
/
{
}
"
.
format
(
pkgInfo
[
"
name
"
]
)
                    
]
:
                        
if
repo
.
endswith
(
strip_suffix
)
:
                            
repo
=
repo
[
:
-
len
(
strip_suffix
)
]
                    
for
path
in
[
                        
"
/
main
/
"
                        
"
/
master
/
"
                        
"
/
main
/
{
}
/
"
.
format
(
pkgInfo
[
"
name
"
]
)
                        
"
/
master
/
{
}
/
"
.
format
(
pkgInfo
[
"
name
"
]
)
                    
]
:
                        
licenseUrl
=
repo
.
replace
(
                            
"
github
.
com
"
"
raw
.
githubusercontent
.
com
"
                        
)
                        
licenseUrl
+
=
path
+
licenseFile
                        
r
=
requests
.
get
(
licenseUrl
)
                        
if
r
.
status_code
=
=
200
:
                            
break
                    
else
:
                        
licenseUrl
=
None
        
if
licenseUrl
is
None
:
            
err
=
"
Could
not
infer
license
URL
for
'
{
}
'
.
\
n
"
.
format
(
pkgInfo
[
"
name
"
]
)
            
err
+
=
"
Please
locate
the
correct
license
URL
and
add
it
to
PACKAGE_METADATA_FIXUPS
.
\
n
"
            
err
+
=
f
"
You
may
need
to
poke
around
in
the
source
repository
at
{
repo
}
"
            
err
+
=
f
"
for
a
{
chosenLicense
}
license
file
named
{
licenseFile
}
.
"
            
raise
RuntimeError
(
err
)
        
if
licenseUrl
.
startswith
(
"
https
:
/
/
raw
.
githubusercontent
.
com
/
"
)
:
            
licenseUrl
=
re
.
sub
(
                
r
"
raw
.
githubusercontent
.
com
/
(
[
^
/
]
+
)
/
(
[
^
/
]
+
)
/
"
                
r
"
github
.
com
/
\
1
/
\
2
/
blob
/
"
                
licenseUrl
            
)
        
return
licenseUrl
def
make_license_title
(
license
deps
=
None
)
:
    
"
"
"
Make
a
nice
human
-
readable
title
for
a
license
and
the
deps
it
applies
to
.
"
"
"
    
if
license
=
=
"
EXT
-
OPENSSL
"
:
        
return
"
OpenSSL
License
"
    
if
license
=
=
"
EXT
-
SQLITE
"
:
        
return
"
Optional
Notice
:
SQLite
"
    
if
license
=
=
"
MPL
-
2
.
0
"
:
        
title
=
"
Mozilla
Public
License
2
.
0
"
    
elif
license
=
=
"
Apache
-
2
.
0
"
:
        
title
=
"
Apache
License
2
.
0
"
    
else
:
        
title
=
f
"
{
license
}
License
"
    
if
deps
:
        
names
=
sorted
(
set
(
d
[
"
name
"
]
for
d
in
deps
)
)
        
title
=
"
{
}
:
{
}
"
.
format
(
title
"
"
.
join
(
names
)
)
    
return
title
def
group_dependencies_for_printing
(
deps
)
:
    
"
"
"
Iterate
over
groups
of
dependencies
and
their
license
info
in
print
order
.
    
This
is
a
helper
function
to
group
and
sort
our
various
dependencies
    
so
that
they
'
re
always
printed
in
sensible
consistent
order
and
we
    
don
'
t
unnecessarily
repeat
any
license
text
.
    
"
"
"
    
depsByLicenseTextHash
=
collections
.
defaultdict
(
list
)
    
for
info
in
deps
:
        
if
info
[
"
license
"
]
in
(
"
MPL
-
2
.
0
"
"
Apache
-
2
.
0
"
)
or
info
[
"
license
"
]
.
startswith
(
            
"
EXT
-
"
        
)
:
            
licenseTextHash
=
info
[
"
license
"
]
        
else
:
            
text
=
"
"
.
join
(
info
[
"
license_text
"
]
.
split
(
)
)
            
licenseTextHash
=
(
                
info
[
"
license
"
]
+
"
:
"
+
hashlib
.
sha256
(
text
.
encode
(
"
utf8
"
)
)
.
hexdigest
(
)
            
)
        
depsByLicenseTextHash
[
licenseTextHash
]
.
append
(
info
)
    
groups
=
[
]
    
for
licenseTextHash
unsorted_deps
in
depsByLicenseTextHash
.
items
(
)
:
        
deps
=
sorted
(
unsorted_deps
key
=
lambda
i
:
(
i
[
"
name
"
]
i
[
"
id
"
]
)
)
        
license
=
deps
[
0
]
[
"
license
"
]
        
if
licenseTextHash
!
=
"
Apache
-
2
.
0
"
:
            
licenseText
=
deps
[
0
]
[
"
license_text
"
]
        
else
:
            
for
dep
in
deps
:
                
licenseText
=
dep
[
"
license_text
"
]
                
if
"
[
yyyy
]
"
in
licenseText
and
"
NSS
"
not
in
licenseText
:
                    
break
            
else
:
                
raise
RuntimeError
(
"
Could
not
find
appropriate
apache
license
text
"
)
        
if
license
in
(
"
MPL
-
2
.
0
"
"
Apache
-
2
.
0
"
)
:
            
title
=
make_license_title
(
license
)
        
else
:
            
title
=
make_license_title
(
license
deps
)
        
groups
.
append
(
            
{
                
"
title
"
:
title
                
"
dependencies
"
:
deps
                
"
license
"
:
license
                
"
license_text_hash
"
:
licenseTextHash
                
"
license_text
"
:
licenseText
                
"
license_url
"
:
deps
[
0
]
.
get
(
"
license_url
"
)
            
}
        
)
    
def
sort_key
(
group
)
:
        
for
i
license
in
enumerate
(
LICENSES_IN_PREFERENCE_ORDER
)
:
            
if
group
[
"
license
"
]
=
=
license
:
                
return
(
i
[
d
[
"
name
"
]
for
d
in
group
[
"
dependencies
"
]
]
)
        
return
(
i
+
1
[
d
[
"
name
"
]
for
d
in
group
[
"
dependencies
"
]
]
)
    
groups
.
sort
(
key
=
sort_key
)
    
return
groups
def
print_dependency_summary_markdown
(
deps
file
=
sys
.
stdout
)
:
    
"
"
"
Print
a
nicely
-
formatted
summary
of
dependencies
and
their
license
info
.
"
"
"
    
def
pf
(
string
*
args
)
:
        
if
args
:
            
string
=
string
.
format
(
*
args
)
        
print
(
string
file
=
file
)
    
pf
(
"
#
Licenses
for
Third
-
Party
Dependencies
"
)
    
pf
(
"
"
)
    
pf
(
        
"
Binary
distributions
of
this
software
incorporate
code
from
a
number
of
third
-
party
dependencies
.
"
    
)
    
pf
(
        
"
These
dependencies
are
available
under
a
variety
of
free
and
open
source
licenses
"
    
)
    
pf
(
"
the
details
of
which
are
reproduced
below
.
"
)
    
pf
(
"
"
)
    
sections
=
group_dependencies_for_printing
(
deps
)
    
for
section
in
sections
:
        
header
=
section
[
"
title
"
]
        
anchor
=
(
            
header
.
lower
(
)
            
.
replace
(
"
"
"
-
"
)
            
.
replace
(
"
.
"
"
"
)
            
.
replace
(
"
"
"
"
)
            
.
replace
(
"
:
"
"
"
)
        
)
        
pf
(
"
*
[
{
}
]
(
#
{
}
)
"
header
anchor
)
    
pf
(
"
-
-
-
-
-
-
-
-
-
-
-
-
-
"
)
    
for
section
in
sections
:
        
pf
(
"
#
#
{
}
"
section
[
"
title
"
]
)
        
pf
(
"
"
)
        
pkgs
=
[
            
"
[
{
}
]
(
{
}
)
"
.
format
(
info
[
"
name
"
]
info
[
"
repository
"
]
)
            
for
info
in
section
[
"
dependencies
"
]
        
]
        
pkgs
=
sorted
(
set
(
pkgs
)
)
        
pf
(
            
"
The
following
text
applies
to
code
linked
from
these
dependencies
:
\
n
{
}
"
            
"
\
n
"
.
join
(
pkgs
)
        
)
        
pf
(
"
"
)
        
pf
(
"
"
)
        
assert
"
"
not
in
section
[
"
license_text
"
]
        
pf
(
"
{
}
"
section
[
"
license_text
"
]
)
        
pf
(
"
"
)
        
pf
(
"
-
-
-
-
-
-
-
-
-
-
-
-
-
"
)
def
print_dependency_summary_pom
(
deps
file
=
sys
.
stdout
)
:
    
"
"
"
Print
a
summary
of
dependencies
and
their
license
info
in
.
pom
file
XML
format
.
"
"
"
    
def
pf
(
string
*
args
)
:
        
if
args
:
            
string
=
string
.
format
(
*
args
)
        
print
(
string
file
=
file
)
    
pf
(
"
<
licenses
>
"
)
    
pf
(
"
<
!
-
-
"
)
    
pf
(
        
"
Binary
distributions
of
this
software
incorporate
code
from
a
number
of
third
-
party
dependencies
.
"
    
)
    
pf
(
        
"
These
dependencies
are
available
under
a
variety
of
free
and
open
source
licenses
"
    
)
    
pf
(
"
the
details
of
which
are
reproduced
below
.
"
)
    
pf
(
"
-
-
>
"
)
    
sections
=
group_dependencies_for_printing
(
deps
)
    
for
section
in
sections
:
        
deps
=
sorted
(
            
set
(
                
map
(
                    
lambda
d
:
(
d
[
"
name
"
]
d
[
"
license
"
]
d
[
"
license_url
"
]
)
                    
section
[
"
dependencies
"
]
                
)
            
)
        
)
        
for
name
license
license_url
in
deps
:
            
dep
=
{
"
name
"
:
name
"
license
"
:
license
"
license_url
"
:
license_url
}
            
pf
(
"
<
license
>
"
)
            
pf
(
                
"
<
name
>
{
}
<
/
name
>
"
                
saxutils
.
escape
(
make_license_title
(
dep
[
"
license
"
]
[
dep
]
)
)
            
)
            
pf
(
"
<
url
>
{
}
<
/
url
>
"
saxutils
.
escape
(
dep
[
"
license_url
"
]
)
)
            
pf
(
"
<
/
license
>
"
)
    
pf
(
"
<
/
licenses
>
"
)
if
__name__
=
=
"
__main__
"
:
    
parser
=
argparse
.
ArgumentParser
(
        
description
=
"
summarize
dependencies
and
license
information
"
    
)
    
parser
.
add_argument
(
"
-
p
"
"
-
-
package
"
action
=
"
append
"
dest
=
"
packages
"
)
    
parser
.
add_argument
(
"
-
-
target
"
action
=
"
append
"
dest
=
"
targets
"
)
    
parser
.
add_argument
(
        
"
-
-
all
-
android
-
targets
"
        
action
=
"
append_const
"
        
dest
=
"
targets
"
        
const
=
ALL_ANDROID_TARGETS
    
)
    
parser
.
add_argument
(
        
"
-
-
all
-
ios
-
targets
"
        
action
=
"
append_const
"
        
dest
=
"
targets
"
        
const
=
ALL_IOS_TARGETS
    
)
    
parser
.
add_argument
(
        
"
-
-
format
"
        
choices
=
[
"
markdown
"
"
json
"
"
pom
"
]
        
default
=
"
markdown
"
        
help
=
"
output
format
to
generate
"
    
)
    
parser
.
add_argument
(
        
"
-
-
check
"
        
action
=
"
store
"
        
help
=
"
suppress
output
instead
checking
that
it
matches
the
given
file
"
    
)
    
args
=
parser
.
parse_args
(
)
    
if
not
args
.
packages
:
        
args
.
packages
=
[
"
megazord
"
"
megazord_ios
"
"
megazord_focus
"
]
    
if
args
.
targets
:
        
args
.
targets
=
list
(
            
itertools
.
chain
(
*
(
[
t
]
if
isinstance
(
t
str
)
else
t
for
t
in
args
.
targets
)
)
        
)
    
metadata
=
get_workspace_metadata
(
)
    
deps
=
metadata
.
get_dependency_summary
(
args
.
packages
args
.
targets
)
    
if
args
.
check
:
        
output
=
io
.
StringIO
(
)
    
else
:
        
output
=
sys
.
stdout
    
if
args
.
format
=
=
"
json
"
:
        
json
.
dump
(
[
info
for
info
in
deps
]
output
)
    
elif
args
.
format
=
=
"
pom
"
:
        
print_dependency_summary_pom
(
deps
file
=
output
)
    
else
:
        
print_dependency_summary_markdown
(
deps
file
=
output
)
    
if
args
.
check
:
        
output
.
seek
(
0
)
        
outlines
=
output
.
readlines
(
)
        
with
open
(
args
.
check
)
as
f
:
            
checklines
=
f
.
readlines
(
)
            
if
outlines
!
=
checklines
:
                
raise
RuntimeError
(
                    
"
Dependency
details
have
changed
from
those
in
{
}
:
\
n
{
}
"
.
format
(
                        
args
.
check
"
"
.
join
(
difflib
.
unified_diff
(
checklines
outlines
)
)
                    
)
                
)
