from
__future__
import
absolute_import
import
os
import
mock
import
mozunit
from
talos
.
ffsetup
import
FFSetup
class
TestFFSetup
(
object
)
:
    
def
setup_method
(
self
method
)
:
        
self
.
ffsetup
=
FFSetup
(
            
{
                
"
env
"
:
{
}
                
"
symbols_path
"
:
"
"
                
"
preferences
"
:
{
}
                
"
webserver
"
:
"
"
                
"
extensions
"
:
[
]
            
}
            
{
                
"
preferences
"
:
{
}
                
"
extensions
"
:
[
]
                
"
profile
"
:
None
            
}
        
)
    
def
test_clean
(
self
)
:
        
assert
self
.
ffsetup
.
_tmp_dir
is
not
None
        
assert
os
.
path
.
exists
(
self
.
ffsetup
.
_tmp_dir
)
is
True
        
self
.
ffsetup
.
clean
(
)
        
assert
self
.
ffsetup
.
_tmp_dir
is
not
None
        
assert
os
.
path
.
exists
(
self
.
ffsetup
.
_tmp_dir
)
is
False
        
gecko_profile
=
mock
.
Mock
(
)
        
self
.
ffsetup
.
gecko_profile
=
gecko_profile
        
self
.
ffsetup
.
clean
(
)
        
assert
gecko_profile
.
clean
.
called
is
True
if
__name__
=
=
'
__main__
'
:
    
mozunit
.
main
(
)
