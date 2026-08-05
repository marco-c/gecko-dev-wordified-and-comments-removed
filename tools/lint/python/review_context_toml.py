import
os
from
mozlint
import
result
try
:
    
import
tomllib
except
ImportError
:
    
import
tomli
as
tomllib
from
python
.
review_context_schema
import
(
    
LoadFileAction
    
ReviewContextValidationError
    
validate_review_context_file
)
def
lint
(
paths
config
*
*
lintargs
)
:
    
root
=
lintargs
[
"
root
"
]
    
results
=
[
]
    
for
path
in
paths
:
        
if
os
.
path
.
isdir
(
path
)
:
            
continue
        
try
:
            
review_context
=
validate_review_context_file
(
path
)
        
except
(
tomllib
.
TOMLDecodeError
ReviewContextValidationError
)
as
exc
:
            
results
.
append
(
                
result
.
from_config
(
                    
config
                    
path
=
path
                    
message
=
str
(
exc
)
                
)
            
)
            
continue
        
for
rule
in
review_context
.
rules
:
            
for
action
in
rule
.
load
:
                
if
not
isinstance
(
action
LoadFileAction
)
or
action
.
repo
is
not
None
:
                    
continue
                
if
not
os
.
path
.
isfile
(
os
.
path
.
join
(
root
action
.
path
)
)
:
                    
results
.
append
(
                        
result
.
from_config
(
                            
config
                            
path
=
path
                            
message
=
(
                                
f
"
rule
{
rule
.
name
!
r
}
loads
missing
file
{
action
.
path
!
r
}
"
                            
)
                        
)
                    
)
    
return
results
