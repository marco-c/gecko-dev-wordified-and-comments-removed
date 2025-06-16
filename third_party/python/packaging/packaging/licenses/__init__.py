from
__future__
import
annotations
import
re
from
typing
import
NewType
cast
from
packaging
.
licenses
.
_spdx
import
EXCEPTIONS
LICENSES
__all__
=
[
    
"
InvalidLicenseExpression
"
    
"
NormalizedLicenseExpression
"
    
"
canonicalize_license_expression
"
]
license_ref_allowed
=
re
.
compile
(
"
^
[
A
-
Za
-
z0
-
9
.
-
]
*
"
)
NormalizedLicenseExpression
=
NewType
(
"
NormalizedLicenseExpression
"
str
)
class
InvalidLicenseExpression
(
ValueError
)
:
    
"
"
"
Raised
when
a
license
-
expression
string
is
invalid
    
>
>
>
canonicalize_license_expression
(
"
invalid
"
)
    
Traceback
(
most
recent
call
last
)
:
        
.
.
.
    
packaging
.
licenses
.
InvalidLicenseExpression
:
Invalid
license
expression
:
'
invalid
'
    
"
"
"
def
canonicalize_license_expression
(
    
raw_license_expression
:
str
)
-
>
NormalizedLicenseExpression
:
    
if
not
raw_license_expression
:
        
message
=
f
"
Invalid
license
expression
:
{
raw_license_expression
!
r
}
"
        
raise
InvalidLicenseExpression
(
message
)
    
license_expression
=
raw_license_expression
.
replace
(
"
(
"
"
(
"
)
.
replace
(
"
)
"
"
)
"
)
    
licenseref_prefix
=
"
LicenseRef
-
"
    
license_refs
=
{
        
ref
.
lower
(
)
:
"
LicenseRef
-
"
+
ref
[
len
(
licenseref_prefix
)
:
]
        
for
ref
in
license_expression
.
split
(
)
        
if
ref
.
lower
(
)
.
startswith
(
licenseref_prefix
.
lower
(
)
)
    
}
    
license_expression
=
license_expression
.
lower
(
)
    
tokens
=
license_expression
.
split
(
)
    
python_tokens
=
[
]
    
for
token
in
tokens
:
        
if
token
not
in
{
"
or
"
"
and
"
"
with
"
"
(
"
"
)
"
}
:
            
python_tokens
.
append
(
"
False
"
)
        
elif
token
=
=
"
with
"
:
            
python_tokens
.
append
(
"
or
"
)
        
elif
token
=
=
"
(
"
and
python_tokens
and
python_tokens
[
-
1
]
not
in
{
"
or
"
"
and
"
}
:
            
message
=
f
"
Invalid
license
expression
:
{
raw_license_expression
!
r
}
"
            
raise
InvalidLicenseExpression
(
message
)
        
else
:
            
python_tokens
.
append
(
token
)
    
python_expression
=
"
"
.
join
(
python_tokens
)
    
try
:
        
invalid
=
eval
(
python_expression
globals
(
)
locals
(
)
)
    
except
Exception
:
        
invalid
=
True
    
if
invalid
is
not
False
:
        
message
=
f
"
Invalid
license
expression
:
{
raw_license_expression
!
r
}
"
        
raise
InvalidLicenseExpression
(
message
)
from
None
    
normalized_tokens
=
[
]
    
for
token
in
tokens
:
        
if
token
in
{
"
or
"
"
and
"
"
with
"
"
(
"
"
)
"
}
:
            
normalized_tokens
.
append
(
token
.
upper
(
)
)
            
continue
        
if
normalized_tokens
and
normalized_tokens
[
-
1
]
=
=
"
WITH
"
:
            
if
token
not
in
EXCEPTIONS
:
                
message
=
f
"
Unknown
license
exception
:
{
token
!
r
}
"
                
raise
InvalidLicenseExpression
(
message
)
            
normalized_tokens
.
append
(
EXCEPTIONS
[
token
]
[
"
id
"
]
)
        
else
:
            
if
token
.
endswith
(
"
+
"
)
:
                
final_token
=
token
[
:
-
1
]
                
suffix
=
"
+
"
            
else
:
                
final_token
=
token
                
suffix
=
"
"
            
if
final_token
.
startswith
(
"
licenseref
-
"
)
:
                
if
not
license_ref_allowed
.
match
(
final_token
)
:
                    
message
=
f
"
Invalid
licenseref
:
{
final_token
!
r
}
"
                    
raise
InvalidLicenseExpression
(
message
)
                
normalized_tokens
.
append
(
license_refs
[
final_token
]
+
suffix
)
            
else
:
                
if
final_token
not
in
LICENSES
:
                    
message
=
f
"
Unknown
license
:
{
final_token
!
r
}
"
                    
raise
InvalidLicenseExpression
(
message
)
                
normalized_tokens
.
append
(
LICENSES
[
final_token
]
[
"
id
"
]
+
suffix
)
    
normalized_expression
=
"
"
.
join
(
normalized_tokens
)
    
return
cast
(
        
NormalizedLicenseExpression
        
normalized_expression
.
replace
(
"
(
"
"
(
"
)
.
replace
(
"
)
"
"
)
"
)
    
)
