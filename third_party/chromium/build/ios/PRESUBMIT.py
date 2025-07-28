PRESUBMIT_VERSION
=
'
2
.
0
.
0
'
USE_PYTHON3
=
True
TEST_PATTERNS
=
[
r
'
.
+
_test
.
py
'
]
def
CheckUnitTests
(
input_api
output_api
)
:
  
return
input_api
.
canned_checks
.
RunUnitTestsInDirectory
(
      
input_api
      
output_api
      
'
.
'
      
files_to_check
=
TEST_PATTERNS
      
run_on_python2
=
False
      
skip_shebang_check
=
True
)
