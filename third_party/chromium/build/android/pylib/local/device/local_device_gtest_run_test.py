"
"
"
Tests
for
local_device_gtest_test_run
.
"
"
"
import
os
import
tempfile
import
unittest
from
pylib
.
gtest
import
gtest_test_instance
from
pylib
.
local
.
device
import
local_device_environment
from
pylib
.
local
.
device
import
local_device_gtest_run
from
py_utils
import
tempfile_ext
import
mock
def
isSliceInList
(
s
l
)
:
  
lenOfSlice
=
len
(
s
)
  
return
any
(
s
=
=
l
[
i
:
lenOfSlice
+
i
]
for
i
in
range
(
len
(
l
)
-
lenOfSlice
+
1
)
)
class
LocalDeviceGtestRunTest
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
_obj
=
local_device_gtest_run
.
LocalDeviceGtestRun
(
        
mock
.
MagicMock
(
spec
=
local_device_environment
.
LocalDeviceEnvironment
)
        
mock
.
MagicMock
(
spec
=
gtest_test_instance
.
GtestTestInstance
)
)
  
def
testExtractTestsFromFilter
(
self
)
:
    
self
.
assertEqual
(
[
        
'
b17
'
        
'
m4e3
'
        
'
p51
'
    
]
local_device_gtest_run
.
_ExtractTestsFromFilter
(
'
b17
:
m4e3
:
p51
'
)
)
    
self
.
assertIsNone
(
local_device_gtest_run
.
_ExtractTestsFromFilter
(
'
-
mk2
'
)
)
    
self
.
assertIsNone
(
        
local_device_gtest_run
.
_ExtractTestsFromFilter
(
'
.
mk2
*
:
.
M67
*
'
)
)
    
self
.
assertIsNone
(
local_device_gtest_run
.
_ExtractTestsFromFilter
(
'
M67
*
'
)
)
    
self
.
assertEqual
(
[
'
.
M67
*
'
]
                     
local_device_gtest_run
.
_ExtractTestsFromFilter
(
'
.
M67
*
'
)
)
  
def
testGetLLVMProfilePath
(
self
)
:
    
path
=
local_device_gtest_run
.
_GetLLVMProfilePath
(
'
test_dir
'
'
sr71
'
'
5
'
)
    
self
.
assertEqual
(
path
os
.
path
.
join
(
'
test_dir
'
'
sr71_5_
%
2m
.
profraw
'
)
)
  
mock
.
patch
(
'
subprocess
.
check_output
'
)
  
def
testMergeCoverageFiles
(
self
mock_sub
)
:
    
with
tempfile_ext
.
NamedTemporaryDirectory
(
)
as
cov_tempd
:
      
pro_tempd
=
os
.
path
.
join
(
cov_tempd
'
profraw
'
)
      
os
.
mkdir
(
pro_tempd
)
      
profdata
=
tempfile
.
NamedTemporaryFile
(
          
dir
=
pro_tempd
          
delete
=
False
          
suffix
=
local_device_gtest_run
.
_PROFRAW_FILE_EXTENSION
)
      
local_device_gtest_run
.
_MergeCoverageFiles
(
cov_tempd
pro_tempd
)
      
self
.
assertFalse
(
os
.
path
.
exists
(
profdata
.
name
)
)
      
self
.
assertTrue
(
mock_sub
.
called
)
  
mock
.
patch
(
'
pylib
.
utils
.
google_storage_helper
.
upload
'
)
  
def
testUploadTestArtifacts
(
self
mock_gsh
)
:
    
link
=
self
.
_obj
.
_UploadTestArtifacts
(
mock
.
MagicMock
(
)
None
)
    
self
.
assertFalse
(
mock_gsh
.
called
)
    
self
.
assertIsNone
(
link
)
    
result
=
'
A
/
10
/
warthog
/
path
'
    
mock_gsh
.
return_value
=
result
    
with
tempfile_ext
.
NamedTemporaryFile
(
)
as
temp_f
:
      
link
=
self
.
_obj
.
_UploadTestArtifacts
(
mock
.
MagicMock
(
)
temp_f
)
    
self
.
assertTrue
(
mock_gsh
.
called
)
    
self
.
assertEqual
(
result
link
)
  
def
testGroupTests
(
self
)
:
    
test
=
[
        
"
TestClass1
.
testcase1
"
        
"
TestClass1
.
otherTestCase
"
        
"
TestClass1
.
PRE_testcase1
"
        
"
TestClass1
.
abc_testcase2
"
        
"
TestClass1
.
PRE_PRE_testcase1
"
        
"
TestClass1
.
PRE_abc_testcase2
"
        
"
TestClass1
.
PRE_PRE_abc_testcase2
"
    
]
    
expectedTestcase1
=
[
        
"
TestClass1
.
PRE_PRE_testcase1
"
        
"
TestClass1
.
PRE_testcase1
"
        
"
TestClass1
.
testcase1
"
    
]
    
expectedTestcase2
=
[
        
"
TestClass1
.
PRE_PRE_abc_testcase2
"
        
"
TestClass1
.
PRE_abc_testcase2
"
        
"
TestClass1
.
abc_testcase2
"
    
]
    
expectedOtherTestcase
=
[
        
"
TestClass1
.
otherTestCase
"
    
]
    
actualTestCase
=
self
.
_obj
.
_GroupTests
(
test
)
    
self
.
assertTrue
(
isSliceInList
(
expectedTestcase1
actualTestCase
)
)
    
self
.
assertTrue
(
isSliceInList
(
expectedTestcase2
actualTestCase
)
)
    
self
.
assertTrue
(
isSliceInList
(
expectedOtherTestcase
actualTestCase
)
)
if
__name__
=
=
'
__main__
'
:
  
unittest
.
main
(
verbosity
=
2
)
