import
mozunit
import
pytest
from
jsonschema
.
exceptions
import
ValidationError
from
mozperftest
.
metrics
.
utils
import
validate_intermediate_results
def
test_results_with_directory
(
)
:
    
test_result
=
{
        
"
results
"
:
"
path
-
to
-
results
"
        
"
name
"
:
"
the
-
name
"
    
}
    
validate_intermediate_results
(
test_result
)
def
test_results_with_measurements
(
)
:
    
test_result
=
{
        
"
results
"
:
[
            
{
"
name
"
:
"
metric
-
1
"
"
values
"
:
[
0
1
1
0
]
}
            
{
"
name
"
:
"
metric
-
2
"
"
values
"
:
[
0
1
1
0
]
}
        
]
        
"
name
"
:
"
the
-
name
"
    
}
    
validate_intermediate_results
(
test_result
)
def
test_results_with_suite_perfherder_options
(
)
:
    
test_result
=
{
        
"
results
"
:
[
            
{
"
name
"
:
"
metric
-
1
"
"
values
"
:
[
0
1
1
0
]
}
            
{
"
name
"
:
"
metric
-
2
"
"
values
"
:
[
0
1
1
0
]
}
        
]
        
"
name
"
:
"
the
-
name
"
        
"
extraOptions
"
:
[
"
an
-
extra
-
option
"
]
        
"
value
"
:
9000
    
}
    
validate_intermediate_results
(
test_result
)
def
test_results_with_subtest_perfherder_options
(
)
:
    
test_result
=
{
        
"
results
"
:
[
            
{
"
name
"
:
"
metric
-
1
"
"
shouldAlert
"
:
True
"
values
"
:
[
0
1
1
0
]
}
            
{
"
name
"
:
"
metric
-
2
"
"
alertThreshold
"
:
1
.
0
"
values
"
:
[
0
1
1
0
]
}
        
]
        
"
name
"
:
"
the
-
name
"
        
"
extraOptions
"
:
[
"
an
-
extra
-
option
"
]
        
"
value
"
:
9000
    
}
    
validate_intermediate_results
(
test_result
)
def
test_results_with_bad_suite_property
(
)
:
    
test_result
=
{
        
"
results
"
:
"
path
-
to
-
results
"
        
"
name
"
:
"
the
-
name
"
        
"
I
'
ll
cause
a
failure
"
:
"
an
expected
failure
"
    
}
    
with
pytest
.
raises
(
ValidationError
)
:
        
validate_intermediate_results
(
test_result
)
def
test_results_with_bad_subtest_property
(
)
:
    
test_result
=
{
        
"
results
"
:
[
            
{
"
name
"
:
"
metric
-
1
"
"
shouldalert
"
:
True
"
values
"
:
[
0
1
1
0
]
}
            
{
"
name
"
:
"
metric
-
2
"
"
alertThreshold
"
:
1
.
0
"
values
"
:
[
0
1
1
0
]
}
        
]
        
"
name
"
:
"
the
-
name
"
        
"
extraOptions
"
:
[
"
an
-
extra
-
option
"
]
        
"
value
"
:
9000
    
}
    
with
pytest
.
raises
(
ValidationError
)
:
        
validate_intermediate_results
(
test_result
)
def
test_results_with_missing_suite_property
(
)
:
    
test_result
=
{
        
"
name
"
:
"
the
-
name
"
    
}
    
with
pytest
.
raises
(
ValidationError
)
:
        
validate_intermediate_results
(
test_result
)
def
test_results_with_missing_subtest_property
(
)
:
    
test_result
=
{
        
"
results
"
:
[
            
{
"
name
"
:
"
metric
-
2
"
"
alertThreshold
"
:
1
.
0
}
        
]
        
"
name
"
:
"
the
-
name
"
        
"
extraOptions
"
:
[
"
an
-
extra
-
option
"
]
        
"
value
"
:
9000
    
}
    
with
pytest
.
raises
(
ValidationError
)
:
        
validate_intermediate_results
(
test_result
)
if
__name__
=
=
"
__main__
"
:
    
mozunit
.
main
(
)
