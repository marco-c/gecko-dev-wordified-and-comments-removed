#
-
*
-
coding
:
utf
-
8
-
*
-
"
from
failedplatform
import
FailedPlatform
from
mozunit
import
main
def
test_get_possible_build_types
(
)
:
    
"
"
"
Test
get_possible_build_types
"
"
"
    
fp
=
FailedPlatform
(
{
}
)
    
assert
fp
.
get_possible_build_types
(
)
=
=
[
]
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
}
}
)
    
assert
fp
.
get_possible_build_types
(
)
=
=
[
"
build_type1
"
]
    
fp
=
FailedPlatform
(
        
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
}
"
build_type2
"
:
{
"
test_variant1
"
:
{
}
}
}
    
)
    
assert
fp
.
get_possible_build_types
(
)
=
=
[
"
build_type1
"
"
build_type2
"
]
def
test_get_possible_test_variants
(
)
:
    
"
"
"
Test
get_possible_test_variants
"
"
"
    
fp
=
FailedPlatform
(
{
}
)
    
assert
fp
.
get_possible_test_variants
(
"
"
)
=
=
[
]
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
}
}
)
    
assert
fp
.
get_possible_test_variants
(
"
unknown
"
)
=
=
[
]
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
}
}
)
    
assert
fp
.
get_possible_test_variants
(
"
build_type1
"
)
=
=
[
"
test_variant1
"
]
    
fp
=
FailedPlatform
(
        
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
}
"
build_type2
"
:
{
"
test_variant2
"
:
{
}
}
}
    
)
    
assert
fp
.
get_possible_test_variants
(
"
build_type2
"
)
=
=
[
"
test_variant2
"
]
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
"
test_variant2
"
:
{
}
}
}
)
    
assert
fp
.
get_possible_test_variants
(
"
build_type1
"
)
=
=
[
        
"
test_variant1
"
        
"
test_variant2
"
    
]
def
test_is_full_test_variants_fail
(
)
:
    
"
"
"
Test
is_full_test_variants_fail
"
"
"
    
fp
=
FailedPlatform
(
{
}
)
    
assert
fp
.
is_full_test_variants_fail
(
"
"
)
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
}
}
)
    
assert
fp
.
is_full_test_variants_fail
(
"
build_type1
"
)
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
}
}
)
    
assert
not
fp
.
is_full_test_variants_fail
(
"
build_type1
"
)
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
}
}
)
    
fp
.
failures
[
"
build_type1
"
]
=
{
"
test_variant2
"
}
    
assert
not
fp
.
is_full_test_variants_fail
(
"
build_type1
"
)
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
}
}
)
    
fp
.
failures
[
"
build_type1
"
]
=
{
"
test_variant1
"
}
    
assert
fp
.
is_full_test_variants_fail
(
"
build_type1
"
)
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
"
test_variant2
"
:
{
}
}
}
)
    
fp
.
failures
[
"
build_type1
"
]
=
{
"
test_variant1
"
}
    
assert
not
fp
.
is_full_test_variants_fail
(
"
build_type1
"
)
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
"
test_variant2
"
:
{
}
}
}
)
    
fp
.
failures
[
"
build_type1
"
]
=
{
"
test_variant1
"
"
test_variant2
"
}
    
assert
fp
.
is_full_test_variants_fail
(
"
build_type1
"
)
def
test_is_full_fail
(
)
:
    
"
"
"
Test
is_full_fail
"
"
"
    
fp
=
FailedPlatform
(
{
}
)
    
assert
fp
.
is_full_fail
(
)
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
}
}
)
    
assert
not
fp
.
is_full_fail
(
)
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
}
}
)
    
assert
not
fp
.
is_full_fail
(
)
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
}
}
)
    
fp
.
failures
[
"
build_type1
"
]
=
set
(
)
    
assert
fp
.
is_full_fail
(
)
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
}
}
)
    
fp
.
failures
[
"
build_type2
"
]
=
set
(
)
    
assert
not
fp
.
is_full_fail
(
)
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
}
}
)
    
fp
.
failures
[
"
build_type1
"
]
=
set
(
)
    
assert
not
fp
.
is_full_fail
(
)
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
}
}
)
    
fp
.
failures
[
"
build_type1
"
]
=
{
"
test_variant1
"
}
    
assert
fp
.
is_full_fail
(
)
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
"
test_variant2
"
:
{
}
}
}
)
    
fp
.
failures
[
"
build_type1
"
]
=
{
"
test_variant1
"
}
    
assert
not
fp
.
is_full_fail
(
)
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
"
test_variant2
"
:
{
}
}
}
)
    
fp
.
failures
[
"
build_type1
"
]
=
{
"
test_variant1
"
"
test_variant2
"
}
    
assert
fp
.
is_full_fail
(
)
    
fp
=
FailedPlatform
(
        
{
            
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
"
test_variant2
"
:
{
}
}
            
"
build_type2
"
:
{
"
test_variant1
"
:
{
}
"
test_variant2
"
:
{
}
}
        
}
    
)
    
fp
.
failures
[
"
build_type1
"
]
=
{
"
test_variant1
"
"
test_variant2
"
}
    
assert
not
fp
.
is_full_fail
(
)
    
fp
=
FailedPlatform
(
        
{
            
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
"
test_variant2
"
:
{
}
}
            
"
build_type2
"
:
{
"
test_variant1
"
:
{
}
"
test_variant2
"
:
{
}
}
        
}
    
)
    
fp
.
failures
[
"
build_type1
"
]
=
{
"
test_variant1
"
"
test_variant2
"
}
    
fp
.
failures
[
"
build_type2
"
]
=
{
"
test_variant1
"
"
test_variant2
"
}
    
assert
fp
.
is_full_fail
(
)
def
test_get_no_variant_conditions
(
)
:
    
"
"
"
Test
get_no_variant_conditions
"
"
"
    
fp
=
FailedPlatform
(
{
}
)
    
assert
fp
.
get_no_variant_conditions
(
"
&
&
"
"
build_type1
"
)
=
=
"
"
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
}
}
)
    
assert
fp
.
get_no_variant_conditions
(
"
&
&
"
"
build_type1
"
)
=
=
"
"
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
}
}
)
    
assert
fp
.
get_no_variant_conditions
(
"
&
&
"
"
build_type1
"
)
=
=
"
&
&
!
test_variant1
"
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
"
!
fission
"
:
{
}
}
}
)
    
assert
(
        
fp
.
get_no_variant_conditions
(
"
&
&
"
"
build_type1
"
)
        
=
=
"
&
&
!
test_variant1
&
&
fission
"
    
)
def
test_get_test_variant_condition
(
)
:
    
"
"
"
Test
get_no_variant_conditions
"
"
"
    
fp
=
FailedPlatform
(
{
}
)
    
assert
(
        
fp
.
get_test_variant_condition
(
"
&
&
"
"
build_type1
"
"
test_variant1
"
)
        
=
=
"
&
&
test_variant1
"
    
)
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
}
}
)
    
assert
(
        
fp
.
get_test_variant_condition
(
"
&
&
"
"
build_type1
"
"
test_variant1
"
)
        
=
=
"
&
&
test_variant1
"
    
)
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
}
}
)
    
assert
(
        
fp
.
get_test_variant_condition
(
"
&
&
"
"
build_type1
"
"
test_variant1
"
)
        
=
=
"
&
&
test_variant1
"
    
)
    
fp
=
FailedPlatform
(
        
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
"
test_variant1
+
test_variant2
"
:
{
}
}
}
    
)
    
assert
(
        
fp
.
get_test_variant_condition
(
"
&
&
"
"
build_type1
"
"
test_variant1
"
)
        
=
=
"
&
&
test_variant1
&
&
!
test_variant2
"
    
)
    
fp
=
FailedPlatform
(
        
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
"
test_variant2
+
test_variant3
"
:
{
}
}
}
    
)
    
assert
(
        
fp
.
get_test_variant_condition
(
"
&
&
"
"
build_type1
"
"
test_variant1
"
)
        
=
=
"
&
&
test_variant1
"
    
)
    
fp
=
FailedPlatform
(
        
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
"
test_variant1
+
test_variant2
"
:
{
}
}
}
    
)
    
assert
(
        
fp
.
get_test_variant_condition
(
            
"
&
&
"
"
build_type1
"
"
test_variant1
+
test_variant2
"
        
)
        
=
=
"
&
&
test_variant1
&
&
test_variant2
"
    
)
    
fp
=
FailedPlatform
(
        
{
            
"
build_type1
"
:
{
                
"
test_variant1
+
test_variant2
"
:
{
}
                
"
test_variant1
+
test_variant2
+
test_variant3
"
:
{
}
            
}
        
}
    
)
    
assert
(
        
fp
.
get_test_variant_condition
(
            
"
&
&
"
"
build_type1
"
"
test_variant1
+
test_variant2
"
        
)
        
=
=
"
&
&
test_variant1
&
&
test_variant2
&
&
!
test_variant3
"
    
)
    
fp
=
FailedPlatform
(
        
{
            
"
build_type1
"
:
{
                
"
test_variant2
+
test_variant1
"
:
{
}
                
"
test_variant1
+
test_variant3
+
test_variant2
"
:
{
}
            
}
        
}
    
)
    
assert
(
        
fp
.
get_test_variant_condition
(
            
"
&
&
"
"
build_type1
"
"
test_variant2
+
test_variant1
"
        
)
        
=
=
"
&
&
test_variant2
&
&
test_variant1
&
&
!
test_variant3
"
    
)
    
fp
=
FailedPlatform
(
        
{
            
"
build_type1
"
:
{
                
"
test_variant1
+
test_variant2
"
:
{
}
                
"
test_variant1
+
test_variant2
+
test_variant3
"
:
{
}
                
"
test_variant1
+
test_variant4
+
test_variant2
"
:
{
}
            
}
        
}
    
)
    
assert
(
        
fp
.
get_test_variant_condition
(
            
"
&
&
"
"
build_type1
"
"
test_variant2
+
test_variant1
"
        
)
        
=
=
"
&
&
test_variant2
&
&
test_variant1
&
&
!
test_variant3
&
&
!
test_variant4
"
    
)
    
fp
=
FailedPlatform
(
        
{
            
"
build_type1
"
:
{
                
"
test_variant1
+
test_variant2
"
:
{
}
                
"
test_variant1
+
test_variant3
"
:
{
}
            
}
        
}
    
)
    
assert
(
        
fp
.
get_test_variant_condition
(
            
"
&
&
"
"
build_type1
"
"
test_variant1
+
test_variant2
"
        
)
        
=
=
"
&
&
test_variant1
&
&
test_variant2
"
    
)
    
fp
=
FailedPlatform
(
        
{
            
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
}
            
"
build_type2
"
:
{
"
test_variant1
+
test_variant2
"
:
{
}
}
        
}
    
)
    
assert
(
        
fp
.
get_test_variant_condition
(
"
&
&
"
"
build_type1
"
"
test_variant1
"
)
        
=
=
"
&
&
test_variant1
"
    
)
def
test_get_skip_string
(
)
:
    
"
"
"
Test
get_skip_string
"
"
"
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
no_variant
"
:
{
}
}
}
)
    
assert
fp
.
get_skip_string
(
"
&
&
"
"
build_type1
"
"
no_variant
"
)
=
=
"
"
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
}
}
)
    
assert
fp
.
get_skip_string
(
"
&
&
"
"
build_type1
"
"
test_variant1
"
)
=
=
"
"
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
test_variant1
+
test_variant2
"
:
{
}
}
}
)
    
assert
(
        
fp
.
get_skip_string
(
"
&
&
"
"
build_type1
"
"
test_variant1
+
test_variant2
"
)
=
=
"
"
    
)
    
fp
=
FailedPlatform
(
        
{
"
build_type1
"
:
{
"
no_variant
"
:
{
}
}
"
build_type2
"
:
{
"
no_variant
"
:
{
}
}
}
    
)
    
assert
fp
.
get_skip_string
(
"
&
&
"
"
build_type1
"
"
no_variant
"
)
=
=
"
&
&
build_type1
"
    
fp
=
FailedPlatform
(
        
{
            
"
build_type1
"
:
{
"
no_variant
"
:
{
}
"
test_variant1
"
:
{
}
}
            
"
build_type2
"
:
{
"
no_variant
"
:
{
}
}
        
}
    
)
    
assert
(
        
fp
.
get_skip_string
(
"
&
&
"
"
build_type1
"
"
no_variant
"
)
        
=
=
"
&
&
build_type1
&
&
!
test_variant1
"
    
)
    
fp
=
FailedPlatform
(
        
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
}
"
build_type2
"
:
{
"
no_variant
"
:
{
}
}
}
    
)
    
assert
(
        
fp
.
get_skip_string
(
"
&
&
"
"
build_type1
"
"
test_variant1
"
)
=
=
"
&
&
build_type1
"
    
)
    
fp
=
FailedPlatform
(
        
{
            
"
build_type1
"
:
{
"
test_variant1
+
test_variant2
"
:
{
}
}
            
"
build_type2
"
:
{
"
no_variant
"
:
{
}
}
        
}
    
)
    
assert
(
        
fp
.
get_skip_string
(
"
&
&
"
"
build_type1
"
"
test_variant1
+
test_variant2
"
)
        
=
=
"
&
&
build_type1
"
    
)
    
fp
=
FailedPlatform
(
        
{
            
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
"
test_variant2
"
:
{
}
}
            
"
build_type2
"
:
{
"
no_variant
"
:
{
}
}
        
}
    
)
    
assert
(
        
fp
.
get_skip_string
(
"
&
&
"
"
build_type1
"
"
test_variant1
"
)
        
=
=
"
&
&
build_type1
&
&
test_variant1
"
    
)
    
fp
=
FailedPlatform
(
        
{
"
build_type1
"
:
{
"
no_variant
"
:
{
}
}
"
build_type2
"
:
{
"
no_variant
"
:
{
}
}
}
    
)
    
assert
fp
.
get_skip_string
(
"
&
&
"
"
build_type1
"
"
no_variant
"
)
=
=
"
&
&
build_type1
"
    
assert
fp
.
get_skip_string
(
"
&
&
"
"
build_type2
"
"
no_variant
"
)
=
=
"
"
    
fp
=
FailedPlatform
(
        
{
            
"
build_type1
"
:
{
"
test_variant1
+
test_variant2
"
:
{
}
}
            
"
build_type2
"
:
{
"
test_variant1
+
test_variant2
"
:
{
}
}
        
}
    
)
    
assert
(
        
fp
.
get_skip_string
(
"
&
&
"
"
build_type1
"
"
test_variant1
+
test_variant2
"
)
        
=
=
"
&
&
build_type1
"
    
)
    
assert
(
        
fp
.
get_skip_string
(
"
&
&
"
"
build_type2
"
"
test_variant1
+
test_variant2
"
)
=
=
"
"
    
)
    
fp
=
FailedPlatform
(
{
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
"
test_variant2
"
:
{
}
}
}
)
    
assert
(
        
fp
.
get_skip_string
(
"
&
&
"
"
build_type1
"
"
test_variant1
"
)
        
=
=
"
&
&
build_type1
&
&
test_variant1
"
    
)
    
assert
fp
.
get_skip_string
(
"
&
&
"
"
build_type1
"
"
test_variant2
"
)
=
=
"
"
    
fp
=
FailedPlatform
(
        
{
            
"
build_type1
"
:
{
"
test_variant1
"
:
{
}
"
no_variant
"
:
{
}
}
            
"
build_type2
"
:
{
"
no_variant
"
:
{
}
}
        
}
    
)
    
assert
(
        
fp
.
get_skip_string
(
"
&
&
"
"
build_type1
"
"
test_variant1
"
)
        
=
=
"
&
&
build_type1
&
&
test_variant1
"
    
)
    
assert
fp
.
get_skip_string
(
"
&
&
"
"
build_type1
"
"
no_variant
"
)
=
=
"
&
&
build_type1
"
    
fp
=
FailedPlatform
(
        
{
            
"
build_type1
"
:
{
                
"
test_variant1
"
:
{
}
                
"
test_variant2
"
:
{
}
                
"
test_variant1
+
test_variant2
"
:
{
}
            
}
            
"
build_type2
"
:
{
"
no_variant
"
:
{
}
"
test_variant1
"
:
{
}
"
test_variant2
"
:
{
}
}
        
}
    
)
    
assert
(
        
fp
.
get_skip_string
(
"
&
&
"
"
build_type1
"
"
test_variant1
"
)
        
=
=
"
&
&
build_type1
&
&
test_variant1
&
&
!
test_variant2
"
    
)
    
assert
(
        
fp
.
get_skip_string
(
"
&
&
"
"
build_type2
"
"
no_variant
"
)
        
=
=
"
&
&
build_type2
&
&
!
test_variant1
&
&
!
test_variant2
"
    
)
    
assert
(
        
fp
.
get_skip_string
(
"
&
&
"
"
build_type1
"
"
test_variant2
"
)
        
=
=
"
&
&
build_type1
&
&
test_variant2
&
&
!
test_variant1
"
    
)
    
assert
(
        
fp
.
get_skip_string
(
"
&
&
"
"
build_type1
"
"
test_variant1
+
test_variant2
"
)
        
=
=
"
&
&
build_type1
"
    
)
    
assert
(
        
fp
.
get_skip_string
(
"
&
&
"
"
build_type2
"
"
test_variant1
"
)
        
=
=
"
&
&
build_type2
&
&
test_variant1
"
    
)
    
assert
fp
.
get_skip_string
(
"
&
&
"
"
build_type2
"
"
test_variant2
"
)
=
=
"
"
if
__name__
=
=
"
__main__
"
:
    
main
(
)
