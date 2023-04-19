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
  
pylint_checks
=
input_api
.
canned_checks
.
GetPylint
(
input_api
output_api
)
  
results
.
extend
(
input_api
.
RunTests
(
pylint_checks
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
)
)
  
cmd
=
[
input_api
.
python_executable
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
