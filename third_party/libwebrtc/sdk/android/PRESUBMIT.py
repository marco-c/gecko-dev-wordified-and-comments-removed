def
CheckChangeOnUpload
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
CheckPatchFormatted
(
input_api
output_api
)
)
    
return
results
def
CheckPatchFormatted
(
input_api
output_api
)
:
    
import
git_cl
    
cmd
=
[
'
cl
'
'
format
'
'
-
-
dry
-
run
'
input_api
.
PresubmitLocalPath
(
)
]
    
code
_
=
git_cl
.
RunGitWithCode
(
cmd
suppress_stderr
=
True
)
    
if
code
=
=
2
:
        
short_path
=
input_api
.
basename
(
input_api
.
PresubmitLocalPath
(
)
)
        
full_path
=
input_api
.
os_path
.
relpath
(
            
input_api
.
PresubmitLocalPath
(
)
input_api
.
change
.
RepositoryRoot
(
)
)
        
return
[
            
output_api
.
PresubmitPromptWarning
(
                
'
The
%
s
directory
requires
source
formatting
.
'
                
'
Please
run
git
cl
format
%
s
'
%
(
short_path
full_path
)
)
        
]
    
return
[
]
