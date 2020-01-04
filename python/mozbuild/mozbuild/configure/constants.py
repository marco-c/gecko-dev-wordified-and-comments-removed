from
__future__
import
absolute_import
print_function
unicode_literals
from
mozbuild
.
util
import
EnumString
CompilerType
=
EnumString
.
subclass
(
    
'
clang
'
    
'
clang
-
cl
'
    
'
gcc
'
    
'
msvc
'
)
OS
=
EnumString
.
subclass
(
    
'
Android
'
    
'
DragonFly
'
    
'
FreeBSD
'
    
'
GNU
'
    
'
iOS
'
    
'
NetBSD
'
    
'
OpenBSD
'
    
'
OSX
'
    
'
WINNT
'
)
Kernel
=
EnumString
.
subclass
(
    
'
Darwin
'
    
'
DragonFly
'
    
'
FreeBSD
'
    
'
kFreeBSD
'
    
'
Linux
'
    
'
NetBSD
'
    
'
OpenBSD
'
    
'
WINNT
'
)
CPU
=
EnumString
.
subclass
(
    
'
aarch64
'
    
'
Alpha
'
    
'
arm
'
    
'
hppa
'
    
'
ia64
'
    
'
mips32
'
    
'
mips64
'
    
'
ppc
'
    
'
ppc64
'
    
'
s390
'
    
'
s390x
'
    
'
sparc
'
    
'
sparc64
'
    
'
x86
'
    
'
x86_64
'
)
Endianness
=
EnumString
.
subclass
(
    
'
big
'
    
'
little
'
)
