def
lint
(
files
*
*
lintargs
)
:
    
return
1
LINTER
=
{
    
'
name
'
:
"
BadReturnCodeLinter
"
    
'
description
'
:
"
Returns
an
error
code
no
matter
what
"
    
'
include
'
:
[
        
'
files
'
    
]
    
'
type
'
:
'
external
'
    
'
extensions
'
:
[
'
.
js
'
'
.
jsm
'
]
    
'
payload
'
:
lint
}
