USE_PYTHON3
=
True
def
_CommonChecks
(
input_api
output_api
)
:
  
results
=
[
]
  
results
.
extend
(
      
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
                                                      
[
r
'
^
.
+
_unittest
\
.
py
'
]
                                                      
skip_shebang_check
=
False
                                                      
run_on_python2
=
False
)
)
  
cmd
=
[
input_api
.
python3_executable
'
mb
.
py
'
'
validate
'
]
  
kwargs
=
{
'
cwd
'
:
input_api
.
PresubmitLocalPath
(
)
}
  
results
.
extend
(
input_api
.
RunTests
(
[
      
input_api
.
Command
(
name
=
'
mb_validate
'
                        
cmd
=
cmd
kwargs
=
kwargs
                        
message
=
output_api
.
PresubmitError
)
]
)
)
  
results
.
extend
(
      
input_api
.
canned_checks
.
CheckLongLines
(
          
input_api
          
output_api
          
maxlen
=
80
          
source_file_filter
=
lambda
x
:
'
mb_config
.
pyl
'
in
x
.
LocalPath
(
)
)
)
  
return
results
def
CheckChangeOnUpload
(
input_api
output_api
)
:
  
return
_CommonChecks
(
input_api
output_api
)
def
CheckChangeOnCommit
(
input_api
output_api
)
:
  
return
_CommonChecks
(
input_api
output_api
)
