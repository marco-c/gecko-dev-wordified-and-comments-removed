"
"
"
Tests
Google
Test
'
s
exception
catching
behavior
.
This
script
invokes
googletest
-
catch
-
exceptions
-
test_
and
googletest
-
catch
-
exceptions
-
ex
-
test_
(
programs
written
with
Google
Test
)
and
verifies
their
output
.
"
"
"
import
gtest_test_utils
FLAG_PREFIX
=
'
-
-
gtest_
'
LIST_TESTS_FLAG
=
FLAG_PREFIX
+
'
list_tests
'
NO_CATCH_EXCEPTIONS_FLAG
=
FLAG_PREFIX
+
'
catch_exceptions
=
0
'
FILTER_FLAG
=
FLAG_PREFIX
+
'
filter
'
EX_EXE_PATH
=
gtest_test_utils
.
GetTestExecutablePath
(
    
'
googletest
-
catch
-
exceptions
-
ex
-
test_
'
)
EXE_PATH
=
gtest_test_utils
.
GetTestExecutablePath
(
    
'
googletest
-
catch
-
exceptions
-
no
-
ex
-
test_
'
)
environ
=
gtest_test_utils
.
environ
SetEnvVar
=
gtest_test_utils
.
SetEnvVar
SetEnvVar
(
gtest_test_utils
.
PREMATURE_EXIT_FILE_ENV_VAR
None
)
TEST_LIST
=
gtest_test_utils
.
Subprocess
(
    
[
EXE_PATH
LIST_TESTS_FLAG
]
env
=
environ
)
.
output
SUPPORTS_SEH_EXCEPTIONS
=
'
ThrowsSehException
'
in
TEST_LIST
if
SUPPORTS_SEH_EXCEPTIONS
:
  
BINARY_OUTPUT
=
gtest_test_utils
.
Subprocess
(
[
EXE_PATH
]
env
=
environ
)
.
output
EX_BINARY_OUTPUT
=
gtest_test_utils
.
Subprocess
(
    
[
EX_EXE_PATH
]
env
=
environ
)
.
output
if
SUPPORTS_SEH_EXCEPTIONS
:
  
class
CatchSehExceptionsTest
(
gtest_test_utils
.
TestCase
)
:
    
"
"
"
Tests
exception
-
catching
behavior
.
"
"
"
    
def
TestSehExceptions
(
self
test_output
)
:
      
self
.
assert_
(
'
SEH
exception
with
code
0x2a
thrown
'
                   
'
in
the
test
fixture
\
'
s
constructor
'
                   
in
test_output
)
      
self
.
assert_
(
'
SEH
exception
with
code
0x2a
thrown
'
                   
'
in
the
test
fixture
\
'
s
destructor
'
                   
in
test_output
)
      
self
.
assert_
(
'
SEH
exception
with
code
0x2a
thrown
in
SetUpTestSuite
(
)
'
                   
in
test_output
)
      
self
.
assert_
(
'
SEH
exception
with
code
0x2a
thrown
in
TearDownTestSuite
(
)
'
                   
in
test_output
)
      
self
.
assert_
(
'
SEH
exception
with
code
0x2a
thrown
in
SetUp
(
)
'
                   
in
test_output
)
      
self
.
assert_
(
'
SEH
exception
with
code
0x2a
thrown
in
TearDown
(
)
'
                   
in
test_output
)
      
self
.
assert_
(
'
SEH
exception
with
code
0x2a
thrown
in
the
test
body
'
                   
in
test_output
)
    
def
testCatchesSehExceptionsWithCxxExceptionsEnabled
(
self
)
:
      
self
.
TestSehExceptions
(
EX_BINARY_OUTPUT
)
    
def
testCatchesSehExceptionsWithCxxExceptionsDisabled
(
self
)
:
      
self
.
TestSehExceptions
(
BINARY_OUTPUT
)
class
CatchCxxExceptionsTest
(
gtest_test_utils
.
TestCase
)
:
  
"
"
"
Tests
C
+
+
exception
-
catching
behavior
.
     
Tests
in
this
test
case
verify
that
:
     
*
C
+
+
exceptions
are
caught
and
logged
as
C
+
+
(
not
SEH
)
exceptions
     
*
Exception
thrown
affect
the
remainder
of
the
test
work
flow
in
the
       
expected
manner
.
  
"
"
"
  
def
testCatchesCxxExceptionsInFixtureConstructor
(
self
)
:
    
self
.
assertTrue
(
        
'
C
+
+
exception
with
description
'
        
'
"
Standard
C
+
+
exception
"
thrown
'
        
'
in
the
test
fixture
\
'
s
constructor
'
in
EX_BINARY_OUTPUT
        
EX_BINARY_OUTPUT
)
    
self
.
assert_
(
'
unexpected
'
not
in
EX_BINARY_OUTPUT
                 
'
This
failure
belongs
in
this
test
only
if
'
                 
'
"
CxxExceptionInConstructorTest
"
(
no
quotes
)
'
                 
'
appears
on
the
same
line
as
words
"
called
unexpectedly
"
'
)
  
if
(
'
CxxExceptionInDestructorTest
.
ThrowsExceptionInDestructor
'
in
      
EX_BINARY_OUTPUT
)
:
    
def
testCatchesCxxExceptionsInFixtureDestructor
(
self
)
:
      
self
.
assertTrue
(
          
'
C
+
+
exception
with
description
'
          
'
"
Standard
C
+
+
exception
"
thrown
'
          
'
in
the
test
fixture
\
'
s
destructor
'
in
EX_BINARY_OUTPUT
          
EX_BINARY_OUTPUT
)
      
self
.
assertTrue
(
          
'
CxxExceptionInDestructorTest
:
:
TearDownTestSuite
(
)
'
          
'
called
as
expected
.
'
in
EX_BINARY_OUTPUT
EX_BINARY_OUTPUT
)
  
def
testCatchesCxxExceptionsInSetUpTestCase
(
self
)
:
    
self
.
assertTrue
(
        
'
C
+
+
exception
with
description
"
Standard
C
+
+
exception
"
'
        
'
thrown
in
SetUpTestSuite
(
)
'
in
EX_BINARY_OUTPUT
EX_BINARY_OUTPUT
)
    
self
.
assertTrue
(
        
'
CxxExceptionInConstructorTest
:
:
TearDownTestSuite
(
)
'
        
'
called
as
expected
.
'
in
EX_BINARY_OUTPUT
EX_BINARY_OUTPUT
)
    
self
.
assertTrue
(
        
'
CxxExceptionInSetUpTestSuiteTest
constructor
'
        
'
called
as
expected
.
'
in
EX_BINARY_OUTPUT
EX_BINARY_OUTPUT
)
    
self
.
assertTrue
(
        
'
CxxExceptionInSetUpTestSuiteTest
destructor
'
        
'
called
as
expected
.
'
in
EX_BINARY_OUTPUT
EX_BINARY_OUTPUT
)
    
self
.
assertTrue
(
        
'
CxxExceptionInSetUpTestSuiteTest
:
:
SetUp
(
)
'
        
'
called
as
expected
.
'
in
EX_BINARY_OUTPUT
EX_BINARY_OUTPUT
)
    
self
.
assertTrue
(
        
'
CxxExceptionInSetUpTestSuiteTest
:
:
TearDown
(
)
'
        
'
called
as
expected
.
'
in
EX_BINARY_OUTPUT
EX_BINARY_OUTPUT
)
    
self
.
assertTrue
(
        
'
CxxExceptionInSetUpTestSuiteTest
test
body
'
        
'
called
as
expected
.
'
in
EX_BINARY_OUTPUT
EX_BINARY_OUTPUT
)
  
def
testCatchesCxxExceptionsInTearDownTestCase
(
self
)
:
    
self
.
assertTrue
(
        
'
C
+
+
exception
with
description
"
Standard
C
+
+
exception
"
'
        
'
thrown
in
TearDownTestSuite
(
)
'
in
EX_BINARY_OUTPUT
EX_BINARY_OUTPUT
)
  
def
testCatchesCxxExceptionsInSetUp
(
self
)
:
    
self
.
assertTrue
(
        
'
C
+
+
exception
with
description
"
Standard
C
+
+
exception
"
'
        
'
thrown
in
SetUp
(
)
'
in
EX_BINARY_OUTPUT
EX_BINARY_OUTPUT
)
    
self
.
assertTrue
(
        
'
CxxExceptionInSetUpTest
:
:
TearDownTestSuite
(
)
'
        
'
called
as
expected
.
'
in
EX_BINARY_OUTPUT
EX_BINARY_OUTPUT
)
    
self
.
assertTrue
(
        
'
CxxExceptionInSetUpTest
destructor
'
        
'
called
as
expected
.
'
in
EX_BINARY_OUTPUT
EX_BINARY_OUTPUT
)
    
self
.
assertTrue
(
        
'
CxxExceptionInSetUpTest
:
:
TearDown
(
)
'
        
'
called
as
expected
.
'
in
EX_BINARY_OUTPUT
EX_BINARY_OUTPUT
)
    
self
.
assert_
(
'
unexpected
'
not
in
EX_BINARY_OUTPUT
                 
'
This
failure
belongs
in
this
test
only
if
'
                 
'
"
CxxExceptionInSetUpTest
"
(
no
quotes
)
'
                 
'
appears
on
the
same
line
as
words
"
called
unexpectedly
"
'
)
  
def
testCatchesCxxExceptionsInTearDown
(
self
)
:
    
self
.
assertTrue
(
        
'
C
+
+
exception
with
description
"
Standard
C
+
+
exception
"
'
        
'
thrown
in
TearDown
(
)
'
in
EX_BINARY_OUTPUT
EX_BINARY_OUTPUT
)
    
self
.
assertTrue
(
        
'
CxxExceptionInTearDownTest
:
:
TearDownTestSuite
(
)
'
        
'
called
as
expected
.
'
in
EX_BINARY_OUTPUT
EX_BINARY_OUTPUT
)
    
self
.
assertTrue
(
        
'
CxxExceptionInTearDownTest
destructor
'
        
'
called
as
expected
.
'
in
EX_BINARY_OUTPUT
EX_BINARY_OUTPUT
)
  
def
testCatchesCxxExceptionsInTestBody
(
self
)
:
    
self
.
assertTrue
(
        
'
C
+
+
exception
with
description
"
Standard
C
+
+
exception
"
'
        
'
thrown
in
the
test
body
'
in
EX_BINARY_OUTPUT
EX_BINARY_OUTPUT
)
    
self
.
assertTrue
(
        
'
CxxExceptionInTestBodyTest
:
:
TearDownTestSuite
(
)
'
        
'
called
as
expected
.
'
in
EX_BINARY_OUTPUT
EX_BINARY_OUTPUT
)
    
self
.
assertTrue
(
        
'
CxxExceptionInTestBodyTest
destructor
'
        
'
called
as
expected
.
'
in
EX_BINARY_OUTPUT
EX_BINARY_OUTPUT
)
    
self
.
assertTrue
(
        
'
CxxExceptionInTestBodyTest
:
:
TearDown
(
)
'
        
'
called
as
expected
.
'
in
EX_BINARY_OUTPUT
EX_BINARY_OUTPUT
)
  
def
testCatchesNonStdCxxExceptions
(
self
)
:
    
self
.
assertTrue
(
        
'
Unknown
C
+
+
exception
thrown
in
the
test
body
'
in
EX_BINARY_OUTPUT
        
EX_BINARY_OUTPUT
)
  
def
testUnhandledCxxExceptionsAbortTheProgram
(
self
)
:
    
FITLER_OUT_SEH_TESTS_FLAG
=
FILTER_FLAG
+
'
=
-
*
Seh
*
'
    
uncaught_exceptions_ex_binary_output
=
gtest_test_utils
.
Subprocess
(
        
[
EX_EXE_PATH
         
NO_CATCH_EXCEPTIONS_FLAG
         
FITLER_OUT_SEH_TESTS_FLAG
]
        
env
=
environ
)
.
output
    
self
.
assert_
(
'
Unhandled
C
+
+
exception
terminating
the
program
'
                 
in
uncaught_exceptions_ex_binary_output
)
    
self
.
assert_
(
'
unexpected
'
not
in
uncaught_exceptions_ex_binary_output
)
if
__name__
=
=
'
__main__
'
:
  
gtest_test_utils
.
Main
(
)
