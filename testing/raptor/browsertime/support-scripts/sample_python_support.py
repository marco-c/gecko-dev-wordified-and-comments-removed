class
SamplePythonSupport
:
    
def
__init__
(
self
*
*
kwargs
)
:
        
pass
    
def
modify_command
(
self
cmd
)
:
        
for
i
entry
in
enumerate
(
cmd
)
:
            
if
"
{
replace
-
with
-
constant
-
value
}
"
in
entry
:
                
cmd
[
i
]
=
"
25
"
