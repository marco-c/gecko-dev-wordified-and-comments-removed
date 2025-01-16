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
    
"
"
"
Checks
common
to
both
upload
and
commit
.
"
"
"
    
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
RunPylint
(
            
input_api
            
output_api
            
files_to_skip
=
(
                
r
'
^
base
[
\
\
\
/
]
.
*
\
.
py
'
                
r
'
^
build
[
\
\
\
/
]
.
*
\
.
py
'
                
r
'
^
buildtools
[
\
\
\
/
]
.
*
\
.
py
'
                
r
'
^
ios
[
\
\
\
/
]
.
*
\
.
py
'
                
r
'
^
out
.
*
[
\
\
\
/
]
.
*
\
.
py
'
                
r
'
^
testing
[
\
\
\
/
]
.
*
\
.
py
'
                
r
'
^
third_party
[
\
\
\
/
]
.
*
\
.
py
'
                
r
'
^
tools
[
\
\
\
/
]
.
*
\
.
py
'
                
r
'
^
tools_libyuv
[
\
\
\
/
]
valgrind
[
\
\
\
/
]
.
*
\
.
py
'
                
r
'
^
xcodebuild
.
*
[
\
\
\
/
]
.
*
\
.
py
'
            
)
            
disabled_warnings
=
[
                
'
F0401
'
                
'
E0611
'
                
'
W0232
'
            
]
            
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
    
return
results
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
_CommonChecks
(
input_api
output_api
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
CheckGNFormatted
(
input_api
output_api
)
    
)
    
return
results
def
CheckChangeOnCommit
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
_CommonChecks
(
input_api
output_api
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
CheckOwners
(
input_api
output_api
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
CheckChangeWasUploaded
(
input_api
output_api
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
CheckChangeHasDescription
(
input_api
                                                          
output_api
)
    
)
    
return
results
