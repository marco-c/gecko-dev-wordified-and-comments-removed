"
"
"
Run
testsuites
written
for
nose
.
"
"
"
from
_pytest
.
config
import
hookimpl
from
_pytest
.
fixtures
import
getfixturemarker
from
_pytest
.
nodes
import
Item
from
_pytest
.
python
import
Function
from
_pytest
.
unittest
import
TestCaseFunction
hookimpl
(
trylast
=
True
)
def
pytest_runtest_setup
(
item
:
Item
)
-
>
None
:
    
if
not
isinstance
(
item
Function
)
:
        
return
    
if
isinstance
(
item
TestCaseFunction
)
:
        
return
    
func
=
item
    
call_optional
(
func
.
obj
"
setup
"
)
    
func
.
addfinalizer
(
lambda
:
call_optional
(
func
.
obj
"
teardown
"
)
)
def
call_optional
(
obj
:
object
name
:
str
)
-
>
bool
:
    
method
=
getattr
(
obj
name
None
)
    
if
method
is
None
:
        
return
False
    
is_fixture
=
getfixturemarker
(
method
)
is
not
None
    
if
is_fixture
:
        
return
False
    
if
not
callable
(
method
)
:
        
return
False
    
method
(
)
    
return
True
