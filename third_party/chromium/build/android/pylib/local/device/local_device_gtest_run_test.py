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
unittest
import
sys
sys
.
path
.
append
(
os
.
path
.
abspath
(
os
.
path
.
join
(
os
.
path
.
dirname
(
__file__
)
    
'
.
.
/
.
.
/
.
.
'
)
)
)
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
pylib
.
local
.
device
import
local_device_test_run
import
mock
from
unittest
.
mock
import
MagicMock
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
        
set
(
[
            
'
m4e3
'
            
'
p51
'
            
'
b17
'
        
]
)
        
set
(
local_device_gtest_run
.
_ExtractTestsFromFilters
(
[
'
b17
:
m4e3
:
p51
'
]
)
)
)
    
self
.
assertIsNone
(
local_device_gtest_run
.
_ExtractTestsFromFilters
(
[
'
-
mk2
'
]
)
)
    
self
.
assertIsNone
(
        
local_device_gtest_run
.
_ExtractTestsFromFilters
(
[
'
.
mk2
*
:
.
M67
*
'
]
)
)
    
self
.
assertIsNone
(
local_device_gtest_run
.
_ExtractTestsFromFilters
(
[
'
M67
*
'
]
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
_ExtractTestsFromFilters
(
[
'
.
M67
*
'
]
)
)
    
self
.
assertEqual
(
[
'
m4e3
'
]
                     
local_device_gtest_run
.
_ExtractTestsFromFilters
(
                         
[
'
b17
:
m4e3
:
p51
'
'
b17
:
m4e3
'
'
m4e3
:
p51
'
]
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
%
c
.
profraw
'
)
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
        
'
TestClass1
.
testcase1
'
        
'
TestClass1
.
otherTestCase
'
        
'
TestClass1
.
PRE_testcase1
'
        
'
TestClass1
.
abc_testcase2
'
        
'
TestClass1
.
PRE_PRE_testcase1
'
        
'
TestClass1
.
PRE_abc_testcase2
'
        
'
TestClass1
.
PRE_PRE_abc_testcase2
'
    
]
    
expectedTestcase1
=
[
        
'
TestClass1
.
PRE_PRE_testcase1
'
        
'
TestClass1
.
PRE_testcase1
'
        
'
TestClass1
.
testcase1
'
    
]
    
expectedTestcase2
=
[
        
'
TestClass1
.
PRE_PRE_abc_testcase2
'
        
'
TestClass1
.
PRE_abc_testcase2
'
        
'
TestClass1
.
abc_testcase2
'
    
]
    
expectedOtherTestcase
=
[
        
'
TestClass1
.
otherTestCase
'
    
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
  
def
testAppendPreTests
(
self
)
:
    
failed_tests
=
[
        
'
TestClass1
.
PRE_PRE_testcase1
'
        
'
TestClass1
.
abc_testcase2
'
        
'
TestClass1
.
PRE_def_testcase3
'
        
'
TestClass1
.
otherTestCase
'
    
]
    
tests
=
[
        
'
TestClass1
.
testcase1
'
        
'
TestClass1
.
otherTestCase
'
        
'
TestClass1
.
def_testcase3
'
        
'
TestClass1
.
PRE_testcase1
'
        
'
TestClass1
.
abc_testcase2
'
        
'
TestClass1
.
PRE_PRE_testcase1
'
        
'
TestClass1
.
PRE_abc_testcase2
'
        
'
TestClass1
.
PRE_def_testcase3
'
        
'
TestClass1
.
PRE_PRE_abc_testcase2
'
    
]
    
expectedTestcase1
=
[
        
'
TestClass1
.
PRE_PRE_testcase1
'
        
'
TestClass1
.
PRE_testcase1
'
        
'
TestClass1
.
testcase1
'
    
]
    
expectedTestcase2
=
[
        
'
TestClass1
.
PRE_PRE_abc_testcase2
'
        
'
TestClass1
.
PRE_abc_testcase2
'
        
'
TestClass1
.
abc_testcase2
'
    
]
    
expectedTestcase3
=
[
        
'
TestClass1
.
PRE_def_testcase3
'
        
'
TestClass1
.
def_testcase3
'
    
]
    
expectedOtherTestcase
=
[
        
'
TestClass1
.
otherTestCase
'
    
]
    
actualTestCase
=
self
.
_obj
.
_AppendPreTestsForRetry
(
failed_tests
tests
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
expectedTestcase3
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
class
LocalDeviceGtestTestRunShardingTest
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
_env
=
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
    
self
.
_test_instance
=
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
    
self
.
_obj
=
local_device_gtest_run
.
LocalDeviceGtestRun
(
        
self
.
_env
self
.
_test_instance
)
    
self
.
test_list
=
[
        
'
TestClass1
.
testcase1
'
        
'
TestClass2
.
testcase1
'
        
'
TestClass1
.
def_testcase3
'
        
'
TestClass1
.
abc_testcase2
'
        
'
TestClass3
.
testcase1
'
    
]
    
self
.
_env
.
ResetCurrentTry
=
MagicMock
(
side_effect
=
self
.
reset_try
)
    
self
.
_env
.
IncrementCurrentTry
=
MagicMock
(
side_effect
=
self
.
increment_try
)
    
self
.
_obj
.
_GetTests
=
MagicMock
(
return_value
=
self
.
test_list
)
  
def
reset_try
(
self
)
:
    
self
.
_env
.
current_try
=
0
  
def
increment_try
(
self
)
:
    
self
.
_env
.
current_try
+
=
1
  
def
test_CreateShardsForDevices
(
self
)
:
    
self
.
_obj
.
_env
.
devices
=
[
1
]
    
self
.
_obj
.
_test_instance
.
test_launcher_batch_limit
=
2
    
expected_shards
=
[
        
[
'
TestClass1
.
testcase1
'
'
TestClass2
.
testcase1
'
]
        
[
'
TestClass1
.
def_testcase3
'
'
TestClass1
.
abc_testcase2
'
]
        
[
'
TestClass3
.
testcase1
'
]
    
]
    
actual_shards
=
self
.
_obj
.
_CreateShardsForDevices
(
self
.
test_list
)
    
self
.
assertEqual
(
expected_shards
actual_shards
)
  
def
test_ApplyExternalSharding_1_shard
(
self
)
:
    
tests
=
[
        
'
TestClass1
.
testcase1
'
'
TestClass1
.
testcase2
'
'
TestClass2
.
testcase1
'
        
'
TestClass3
.
testcase1
'
    
]
    
expected_tests
=
[
        
'
TestClass1
.
testcase2
'
'
TestClass1
.
testcase1
'
'
TestClass3
.
testcase1
'
        
'
TestClass2
.
testcase1
'
    
]
    
actual_tests
=
self
.
_obj
.
_ApplyExternalSharding
(
        
tests
0
1
)
    
self
.
assertEqual
(
expected_tests
actual_tests
)
  
def
test_ApplyExternalSharding_2_shards
(
self
)
:
    
tests
=
[
        
'
TestClass1
.
testcase1
'
'
TestClass1
.
testcase2
'
'
TestClass2
.
testcase1
'
        
'
TestClass3
.
testcase1
'
    
]
    
expected_shard0
=
[
'
TestClass1
.
testcase2
'
'
TestClass1
.
testcase1
'
]
    
expected_shard1
=
[
'
TestClass3
.
testcase1
'
'
TestClass2
.
testcase1
'
]
    
actual_shard0
=
self
.
_obj
.
_ApplyExternalSharding
(
        
tests
0
2
)
    
actual_shard1
=
self
.
_obj
.
_ApplyExternalSharding
(
        
tests
1
2
)
    
self
.
assertEqual
(
expected_shard0
expected_shard0
)
    
self
.
assertEqual
(
expected_shard1
expected_shard1
)
    
self
.
assertSetEqual
(
set
(
actual_shard0
+
actual_shard1
)
set
(
tests
)
)
  
def
test_deterministic_sharding_grouped_tests
(
self
)
:
    
self
.
_test_instance
.
external_shard_index
=
0
    
self
.
_test_instance
.
total_external_shards
=
1
    
self
.
_test_instance
.
test_launcher_batch_limit
=
2
    
self
.
_env
.
devices
=
[
1
]
    
self
.
_env
.
recover_devices
=
False
    
self
.
_env
.
max_tries
=
1
    
expected_shards
=
[
        
[
'
TestClass1
.
def_testcase3
'
'
TestClass1
.
abc_testcase2
'
]
        
[
'
TestClass1
.
testcase1
'
'
TestClass3
.
testcase1
'
]
        
[
'
TestClass2
.
testcase1
'
]
    
]
    
def
mock_pMap
(
func
*
args
)
:
      
for
_
in
self
.
_env
.
devices
:
        
func
(
*
args
)
      
return
MagicMock
(
)
    
def
get_actual_shards
(
)
:
      
actual_shards
=
[
]
      
mock_RunTestsOnDevice
.
assert_called
(
)
      
tc
=
mock_RunTestsOnDevice
.
call_args
.
args
[
0
]
      
for
group
in
tc
:
        
actual_shards
.
append
(
group
)
        
tc
.
test_completed
(
)
      
return
actual_shards
    
mock_RunTestsOnDevice
=
MagicMock
(
        
autospec
=
'
local_device_test_run
.
LocalDeviceTestRun
.
_RunTestsOnDevice
'
)
    
(
local_device_test_run
.
LocalDeviceTestRun
        
.
_RunTestsOnDevice
)
=
mock_RunTestsOnDevice
    
with
mock
.
patch
.
object
(
        
self
.
_env
.
parallel_devices
"
pMap
"
side_effect
=
mock_pMap
    
)
:
      
self
.
_obj
.
RunTests
(
results
=
[
]
)
      
actual_shards
=
get_actual_shards
(
)
      
self
.
assertEqual
(
actual_shards
expected_shards
)
      
self
.
_obj
.
RunTests
(
results
=
[
]
)
      
actual_shards
=
get_actual_shards
(
)
      
self
.
assertEqual
(
actual_shards
expected_shards
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
