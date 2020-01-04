from
__future__
import
absolute_import
print_function
unicode_literals
import
unittest
from
.
.
kind
.
legacy
import
(
    
LegacyKind
    
validate_build_task
    
BuildTaskValidationException
)
from
mozunit
import
main
class
TestLegacyKind
(
unittest
.
TestCase
)
:
    
def
setUp
(
self
)
:
        
self
.
kind
=
LegacyKind
(
'
/
root
'
{
}
)
class
TestValidateBuildTask
(
unittest
.
TestCase
)
:
    
def
test_validate_missing_extra
(
self
)
:
        
with
self
.
assertRaises
(
BuildTaskValidationException
)
:
            
validate_build_task
(
{
}
)
    
def
test_validate_valid
(
self
)
:
        
with
self
.
assertRaises
(
BuildTaskValidationException
)
:
            
validate_build_task
(
{
                
'
extra
'
:
{
                    
'
locations
'
:
{
                        
'
build
'
:
'
'
                        
'
tests
'
:
'
'
                    
}
                
}
            
}
)
if
__name__
=
=
'
__main__
'
:
    
main
(
)
