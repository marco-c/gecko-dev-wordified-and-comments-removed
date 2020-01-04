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
task
.
legacy
import
(
    
validate_build_task
    
BuildTaskValidationException
)
from
mozunit
import
main
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
