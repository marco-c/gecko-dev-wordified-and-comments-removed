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
