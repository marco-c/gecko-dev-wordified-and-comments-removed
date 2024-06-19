"
"
"
Discover
and
run
std
-
library
"
unittest
"
style
tests
.
"
"
"
import
sys
import
traceback
import
types
from
typing
import
Any
from
typing
import
Callable
from
typing
import
Generator
from
typing
import
Iterable
from
typing
import
List
from
typing
import
Optional
from
typing
import
Tuple
from
typing
import
Type
from
typing
import
TYPE_CHECKING
from
typing
import
Union
import
_pytest
.
_code
from
_pytest
.
compat
import
is_async_function
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
FixtureRequest
from
_pytest
.
nodes
import
Collector
from
_pytest
.
nodes
import
Item
from
_pytest
.
outcomes
import
exit
from
_pytest
.
outcomes
import
fail
from
_pytest
.
outcomes
import
skip
from
_pytest
.
outcomes
import
xfail
from
_pytest
.
python
import
Class
from
_pytest
.
python
import
Function
from
_pytest
.
python
import
Module
from
_pytest
.
runner
import
CallInfo
import
pytest
if
sys
.
version_info
[
:
2
]
<
(
3
11
)
:
    
from
exceptiongroup
import
ExceptionGroup
if
TYPE_CHECKING
:
    
import
unittest
    
import
twisted
.
trial
.
unittest
    
_SysExcInfoType
=
Union
[
        
Tuple
[
Type
[
BaseException
]
BaseException
types
.
TracebackType
]
        
Tuple
[
None
None
None
]
    
]
def
pytest_pycollect_makeitem
(
    
collector
:
Union
[
Module
Class
]
name
:
str
obj
:
object
)
-
>
Optional
[
"
UnitTestCase
"
]
:
    
try
:
        
ut
=
sys
.
modules
[
"
unittest
"
]
        
if
not
issubclass
(
obj
ut
.
TestCase
)
:
            
return
None
    
except
Exception
:
        
return
None
    
return
UnitTestCase
.
from_parent
(
collector
name
=
name
obj
=
obj
)
class
UnitTestCase
(
Class
)
:
    
nofuncargs
=
True
    
def
newinstance
(
self
)
:
        
return
self
.
obj
(
"
runTest
"
)
    
def
collect
(
self
)
-
>
Iterable
[
Union
[
Item
Collector
]
]
:
        
from
unittest
import
TestLoader
        
cls
=
self
.
obj
        
if
not
getattr
(
cls
"
__test__
"
True
)
:
            
return
        
skipped
=
_is_skipped
(
cls
)
        
if
not
skipped
:
            
self
.
_register_unittest_setup_method_fixture
(
cls
)
            
self
.
_register_unittest_setup_class_fixture
(
cls
)
            
self
.
_register_setup_class_fixture
(
)
        
self
.
session
.
_fixturemanager
.
parsefactories
(
self
.
newinstance
(
)
self
.
nodeid
)
        
loader
=
TestLoader
(
)
        
foundsomething
=
False
        
for
name
in
loader
.
getTestCaseNames
(
self
.
obj
)
:
            
x
=
getattr
(
self
.
obj
name
)
            
if
not
getattr
(
x
"
__test__
"
True
)
:
                
continue
            
yield
TestCaseFunction
.
from_parent
(
self
name
=
name
)
            
foundsomething
=
True
        
if
not
foundsomething
:
            
runtest
=
getattr
(
self
.
obj
"
runTest
"
None
)
            
if
runtest
is
not
None
:
                
ut
=
sys
.
modules
.
get
(
"
twisted
.
trial
.
unittest
"
None
)
                
if
ut
is
None
or
runtest
!
=
ut
.
TestCase
.
runTest
:
                    
yield
TestCaseFunction
.
from_parent
(
self
name
=
"
runTest
"
)
    
def
_register_unittest_setup_class_fixture
(
self
cls
:
type
)
-
>
None
:
        
"
"
"
Register
an
auto
-
use
fixture
to
invoke
setUpClass
and
        
tearDownClass
(
#
517
)
.
"
"
"
        
setup
=
getattr
(
cls
"
setUpClass
"
None
)
        
teardown
=
getattr
(
cls
"
tearDownClass
"
None
)
        
if
setup
is
None
and
teardown
is
None
:
            
return
None
        
cleanup
=
getattr
(
cls
"
doClassCleanups
"
lambda
:
None
)
        
def
process_teardown_exceptions
(
)
-
>
None
:
            
exc_infos
=
getattr
(
cls
"
tearDown_exceptions
"
None
)
            
if
not
exc_infos
:
                
return
            
exceptions
=
[
exc
for
(
_
exc
_
)
in
exc_infos
]
            
if
len
(
exceptions
)
=
=
1
:
                
raise
exceptions
[
0
]
            
else
:
                
raise
ExceptionGroup
(
"
Unittest
class
cleanup
errors
"
exceptions
)
        
def
unittest_setup_class_fixture
(
            
request
:
FixtureRequest
        
)
-
>
Generator
[
None
None
None
]
:
            
cls
=
request
.
cls
            
if
_is_skipped
(
cls
)
:
                
reason
=
cls
.
__unittest_skip_why__
                
raise
pytest
.
skip
.
Exception
(
reason
_use_item_location
=
True
)
            
if
setup
is
not
None
:
                
try
:
                    
setup
(
)
                
except
Exception
:
                    
cleanup
(
)
                    
process_teardown_exceptions
(
)
                    
raise
            
yield
            
try
:
                
if
teardown
is
not
None
:
                    
teardown
(
)
            
finally
:
                
cleanup
(
)
                
process_teardown_exceptions
(
)
        
self
.
session
.
_fixturemanager
.
_register_fixture
(
            
name
=
f
"
_unittest_setUpClass_fixture_
{
cls
.
__qualname__
}
"
            
func
=
unittest_setup_class_fixture
            
nodeid
=
self
.
nodeid
            
scope
=
"
class
"
            
autouse
=
True
        
)
    
def
_register_unittest_setup_method_fixture
(
self
cls
:
type
)
-
>
None
:
        
"
"
"
Register
an
auto
-
use
fixture
to
invoke
setup_method
and
        
teardown_method
(
#
517
)
.
"
"
"
        
setup
=
getattr
(
cls
"
setup_method
"
None
)
        
teardown
=
getattr
(
cls
"
teardown_method
"
None
)
        
if
setup
is
None
and
teardown
is
None
:
            
return
None
        
def
unittest_setup_method_fixture
(
            
request
:
FixtureRequest
        
)
-
>
Generator
[
None
None
None
]
:
            
self
=
request
.
instance
            
if
_is_skipped
(
self
)
:
                
reason
=
self
.
__unittest_skip_why__
                
raise
pytest
.
skip
.
Exception
(
reason
_use_item_location
=
True
)
            
if
setup
is
not
None
:
                
setup
(
self
request
.
function
)
            
yield
            
if
teardown
is
not
None
:
                
teardown
(
self
request
.
function
)
        
self
.
session
.
_fixturemanager
.
_register_fixture
(
            
name
=
f
"
_unittest_setup_method_fixture_
{
cls
.
__qualname__
}
"
            
func
=
unittest_setup_method_fixture
            
nodeid
=
self
.
nodeid
            
scope
=
"
function
"
            
autouse
=
True
        
)
class
TestCaseFunction
(
Function
)
:
    
nofuncargs
=
True
    
_excinfo
:
Optional
[
List
[
_pytest
.
_code
.
ExceptionInfo
[
BaseException
]
]
]
=
None
    
def
_getinstance
(
self
)
:
        
assert
isinstance
(
self
.
parent
UnitTestCase
)
        
return
self
.
parent
.
obj
(
self
.
name
)
    
property
    
def
_testcase
(
self
)
:
        
return
self
.
instance
    
def
setup
(
self
)
-
>
None
:
        
self
.
_explicit_tearDown
:
Optional
[
Callable
[
[
]
None
]
]
=
None
        
super
(
)
.
setup
(
)
    
def
teardown
(
self
)
-
>
None
:
        
super
(
)
.
teardown
(
)
        
if
self
.
_explicit_tearDown
is
not
None
:
            
self
.
_explicit_tearDown
(
)
            
self
.
_explicit_tearDown
=
None
        
self
.
_obj
=
None
    
def
startTest
(
self
testcase
:
"
unittest
.
TestCase
"
)
-
>
None
:
        
pass
    
def
_addexcinfo
(
self
rawexcinfo
:
"
_SysExcInfoType
"
)
-
>
None
:
        
rawexcinfo
=
getattr
(
rawexcinfo
"
_rawexcinfo
"
rawexcinfo
)
        
try
:
            
excinfo
=
_pytest
.
_code
.
ExceptionInfo
[
BaseException
]
.
from_exc_info
(
                
rawexcinfo
            
)
            
_
=
excinfo
.
value
            
_
=
excinfo
.
traceback
        
except
TypeError
:
            
try
:
                
try
:
                    
values
=
traceback
.
format_exception
(
*
rawexcinfo
)
                    
values
.
insert
(
                        
0
                        
"
NOTE
:
Incompatible
Exception
Representation
"
                        
"
displaying
natively
:
\
n
\
n
"
                    
)
                    
fail
(
"
"
.
join
(
values
)
pytrace
=
False
)
                
except
(
fail
.
Exception
KeyboardInterrupt
)
:
                    
raise
                
except
BaseException
:
                    
fail
(
                        
"
ERROR
:
Unknown
Incompatible
Exception
"
                        
f
"
representation
:
\
n
{
rawexcinfo
!
r
}
"
                        
pytrace
=
False
                    
)
            
except
KeyboardInterrupt
:
                
raise
            
except
fail
.
Exception
:
                
excinfo
=
_pytest
.
_code
.
ExceptionInfo
.
from_current
(
)
        
self
.
__dict__
.
setdefault
(
"
_excinfo
"
[
]
)
.
append
(
excinfo
)
    
def
addError
(
        
self
testcase
:
"
unittest
.
TestCase
"
rawexcinfo
:
"
_SysExcInfoType
"
    
)
-
>
None
:
        
try
:
            
if
isinstance
(
rawexcinfo
[
1
]
exit
.
Exception
)
:
                
exit
(
rawexcinfo
[
1
]
.
msg
)
        
except
TypeError
:
            
pass
        
self
.
_addexcinfo
(
rawexcinfo
)
    
def
addFailure
(
        
self
testcase
:
"
unittest
.
TestCase
"
rawexcinfo
:
"
_SysExcInfoType
"
    
)
-
>
None
:
        
self
.
_addexcinfo
(
rawexcinfo
)
    
def
addSkip
(
self
testcase
:
"
unittest
.
TestCase
"
reason
:
str
)
-
>
None
:
        
try
:
            
raise
pytest
.
skip
.
Exception
(
reason
_use_item_location
=
True
)
        
except
skip
.
Exception
:
            
self
.
_addexcinfo
(
sys
.
exc_info
(
)
)
    
def
addExpectedFailure
(
        
self
        
testcase
:
"
unittest
.
TestCase
"
        
rawexcinfo
:
"
_SysExcInfoType
"
        
reason
:
str
=
"
"
    
)
-
>
None
:
        
try
:
            
xfail
(
str
(
reason
)
)
        
except
xfail
.
Exception
:
            
self
.
_addexcinfo
(
sys
.
exc_info
(
)
)
    
def
addUnexpectedSuccess
(
        
self
        
testcase
:
"
unittest
.
TestCase
"
        
reason
:
Optional
[
"
twisted
.
trial
.
unittest
.
Todo
"
]
=
None
    
)
-
>
None
:
        
msg
=
"
Unexpected
success
"
        
if
reason
:
            
msg
+
=
f
"
:
{
reason
.
reason
}
"
        
try
:
            
fail
(
msg
pytrace
=
False
)
        
except
fail
.
Exception
:
            
self
.
_addexcinfo
(
sys
.
exc_info
(
)
)
    
def
addSuccess
(
self
testcase
:
"
unittest
.
TestCase
"
)
-
>
None
:
        
pass
    
def
stopTest
(
self
testcase
:
"
unittest
.
TestCase
"
)
-
>
None
:
        
pass
    
def
addDuration
(
self
testcase
:
"
unittest
.
TestCase
"
elapsed
:
float
)
-
>
None
:
        
pass
    
def
runtest
(
self
)
-
>
None
:
        
from
_pytest
.
debugging
import
maybe_wrap_pytest_function_for_tracing
        
testcase
=
self
.
instance
        
assert
testcase
is
not
None
        
maybe_wrap_pytest_function_for_tracing
(
self
)
        
if
is_async_function
(
self
.
obj
)
:
            
testcase
(
result
=
self
)
        
else
:
            
assert
isinstance
(
self
.
parent
UnitTestCase
)
            
skipped
=
_is_skipped
(
self
.
obj
)
or
_is_skipped
(
self
.
parent
.
obj
)
            
if
self
.
config
.
getoption
(
"
usepdb
"
)
and
not
skipped
:
                
self
.
_explicit_tearDown
=
testcase
.
tearDown
                
setattr
(
testcase
"
tearDown
"
lambda
*
args
:
None
)
            
setattr
(
testcase
self
.
name
self
.
obj
)
            
try
:
                
testcase
(
result
=
self
)
            
finally
:
                
delattr
(
testcase
self
.
name
)
    
def
_traceback_filter
(
        
self
excinfo
:
_pytest
.
_code
.
ExceptionInfo
[
BaseException
]
    
)
-
>
_pytest
.
_code
.
Traceback
:
        
traceback
=
super
(
)
.
_traceback_filter
(
excinfo
)
        
ntraceback
=
traceback
.
filter
(
            
lambda
x
:
not
x
.
frame
.
f_globals
.
get
(
"
__unittest
"
)
        
)
        
if
not
ntraceback
:
            
ntraceback
=
traceback
        
return
ntraceback
hookimpl
(
tryfirst
=
True
)
def
pytest_runtest_makereport
(
item
:
Item
call
:
CallInfo
[
None
]
)
-
>
None
:
    
if
isinstance
(
item
TestCaseFunction
)
:
        
if
item
.
_excinfo
:
            
call
.
excinfo
=
item
.
_excinfo
.
pop
(
0
)
            
try
:
                
del
call
.
result
            
except
AttributeError
:
                
pass
    
unittest
=
sys
.
modules
.
get
(
"
unittest
"
)
    
if
unittest
and
call
.
excinfo
and
isinstance
(
call
.
excinfo
.
value
unittest
.
SkipTest
)
:
        
excinfo
=
call
.
excinfo
        
call2
=
CallInfo
[
None
]
.
from_call
(
            
lambda
:
pytest
.
skip
(
str
(
excinfo
.
value
)
)
call
.
when
        
)
        
call
.
excinfo
=
call2
.
excinfo
classImplements_has_run
=
False
hookimpl
(
wrapper
=
True
)
def
pytest_runtest_protocol
(
item
:
Item
)
-
>
Generator
[
None
object
object
]
:
    
if
isinstance
(
item
TestCaseFunction
)
and
"
twisted
.
trial
.
unittest
"
in
sys
.
modules
:
        
ut
:
Any
=
sys
.
modules
[
"
twisted
.
python
.
failure
"
]
        
global
classImplements_has_run
        
Failure__init__
=
ut
.
Failure
.
__init__
        
if
not
classImplements_has_run
:
            
from
twisted
.
trial
.
itrial
import
IReporter
            
from
zope
.
interface
import
classImplements
            
classImplements
(
TestCaseFunction
IReporter
)
            
classImplements_has_run
=
True
        
def
excstore
(
            
self
exc_value
=
None
exc_type
=
None
exc_tb
=
None
captureVars
=
None
        
)
:
            
if
exc_value
is
None
:
                
self
.
_rawexcinfo
=
sys
.
exc_info
(
)
            
else
:
                
if
exc_type
is
None
:
                    
exc_type
=
type
(
exc_value
)
                
self
.
_rawexcinfo
=
(
exc_type
exc_value
exc_tb
)
            
try
:
                
Failure__init__
(
                    
self
exc_value
exc_type
exc_tb
captureVars
=
captureVars
                
)
            
except
TypeError
:
                
Failure__init__
(
self
exc_value
exc_type
exc_tb
)
        
ut
.
Failure
.
__init__
=
excstore
        
try
:
            
res
=
yield
        
finally
:
            
ut
.
Failure
.
__init__
=
Failure__init__
    
else
:
        
res
=
yield
    
return
res
def
_is_skipped
(
obj
)
-
>
bool
:
    
"
"
"
Return
True
if
the
given
object
has
been
marked
with
unittest
.
skip
.
"
"
"
    
return
bool
(
getattr
(
obj
"
__unittest_skip__
"
False
)
)
