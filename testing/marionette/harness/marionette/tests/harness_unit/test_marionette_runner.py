import
pytest
from
marionette
import
runtests
pytest
.
fixture
def
harness_class
(
request
)
:
    
failures
=
request
.
getfuncargvalue
(
'
num_failures
'
)
    
class
Harness
(
object
)
:
        
def
__init__
(
*
args
*
*
kwargs
)
:
            
pass
        
def
run
(
*
args
*
*
kwargs
)
:
            
if
failures
is
None
:
                
raise
Exception
            
else
:
                
return
failures
    
return
Harness
pytest
.
mark
.
parametrize
(
    
"
num_failures
exit_code
"
    
[
(
0
0
)
(
1
10
)
(
None
1
)
]
)
def
test_cli_exit_code
(
num_failures
exit_code
harness_class
)
:
    
with
pytest
.
raises
(
SystemExit
)
as
err
:
        
runtests
.
cli
(
harness_class
=
harness_class
)
    
assert
err
.
value
.
code
=
=
exit_code
