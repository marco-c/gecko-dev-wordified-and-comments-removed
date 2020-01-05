def
lint
(
files
logger
*
*
kwargs
)
:
    
for
path
in
files
:
        
with
open
(
path
'
r
'
)
as
fh
:
            
for
i
line
in
enumerate
(
fh
.
readlines
(
)
)
:
                
if
'
foobar
'
in
line
:
                    
logger
.
lint_error
(
path
=
path
                                      
lineno
=
i
+
1
                                      
column
=
1
                                      
rule
=
"
no
-
foobar
"
)
LINTER
=
{
    
'
name
'
:
"
StructuredLinter
"
    
'
description
'
:
"
It
'
s
bad
to
have
the
string
foobar
in
js
files
.
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
structured_log
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
