"
"
"
Top
-
level
presubmit
script
for
build
/
fuchsia
/
test
.
See
http
:
/
/
dev
.
chromium
.
org
/
developers
/
how
-
tos
/
depottools
/
presubmit
-
scripts
for
more
details
about
the
presubmit
API
built
into
depot_tools
.
"
"
"
_EXTRA_PATHS_COMPONENTS
=
[
(
'
testing
'
)
]
def
CommonChecks
(
input_api
output_api
)
:
    
if
input_api
.
is_windows
:
        
return
[
]
    
tests
=
[
]
    
chromium_src_path
=
input_api
.
os_path
.
realpath
(
        
input_api
.
os_path
.
join
(
input_api
.
PresubmitLocalPath
(
)
'
.
.
'
'
.
.
'
                               
'
.
.
'
)
)
    
pylint_extra_paths
=
[
        
input_api
.
os_path
.
join
(
chromium_src_path
*
component
)
        
for
component
in
_EXTRA_PATHS_COMPONENTS
    
]
    
tests
.
extend
(
        
input_api
.
canned_checks
.
GetPylint
(
input_api
                                          
output_api
                                          
extra_paths_list
=
pylint_extra_paths
                                          
pylintrc
=
'
pylintrc
'
                                          
version
=
'
2
.
7
'
)
)
    
tests
.
append
(
        
input_api
.
Command
(
            
name
=
'
coveragetest
'
            
cmd
=
[
input_api
.
python3_executable
'
coveragetest
.
py
'
]
            
kwargs
=
{
}
            
message
=
output_api
.
PresubmitError
)
)
    
return
input_api
.
RunTests
(
tests
)
def
CheckChangeOnUpload
(
input_api
output_api
)
:
    
return
CommonChecks
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
CommonChecks
(
input_api
output_api
)
