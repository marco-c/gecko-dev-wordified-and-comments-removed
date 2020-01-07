from
__future__
import
absolute_import
import
os
import
mozunit
import
pytest
from
mozprofile
import
(
    
BaseProfile
    
Profile
    
ChromeProfile
    
FirefoxProfile
    
ThunderbirdProfile
    
create_profile
)
def
test_with_profile_should_cleanup
(
)
:
    
with
Profile
(
)
as
profile
:
        
assert
os
.
path
.
exists
(
profile
.
profile
)
    
assert
not
os
.
path
.
exists
(
profile
.
profile
)
def
test_with_profile_should_cleanup_even_on_exception
(
)
:
    
with
pytest
.
raises
(
ZeroDivisionError
)
:
        
with
Profile
(
)
as
profile
:
            
assert
os
.
path
.
exists
(
profile
.
profile
)
            
1
/
0
    
assert
not
os
.
path
.
exists
(
profile
.
profile
)
pytest
.
mark
.
parametrize
(
'
app
cls
'
[
    
(
'
chrome
'
ChromeProfile
)
    
(
'
firefox
'
FirefoxProfile
)
    
(
'
thunderbird
'
ThunderbirdProfile
)
    
(
'
unknown
'
None
)
]
)
def
test_create_profile
(
tmpdir
app
cls
)
:
    
path
=
tmpdir
.
strpath
    
if
cls
is
None
:
        
with
pytest
.
raises
(
NotImplementedError
)
:
            
create_profile
(
app
)
        
return
    
profile
=
create_profile
(
app
profile
=
path
)
    
assert
isinstance
(
profile
BaseProfile
)
    
assert
profile
.
__class__
=
=
cls
    
assert
profile
.
profile
=
=
path
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
