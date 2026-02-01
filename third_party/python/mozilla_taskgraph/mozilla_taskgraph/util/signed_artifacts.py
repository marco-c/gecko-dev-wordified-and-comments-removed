def
get_signed_artifacts
(
input
formats
behavior
=
None
)
:
    
"
"
"
    
Get
the
list
of
signed
artifacts
for
the
given
input
and
formats
.
    
"
"
"
    
artifacts
=
set
(
)
    
if
input
.
endswith
(
"
.
dmg
"
)
:
        
artifacts
.
add
(
input
.
replace
(
"
.
dmg
"
"
.
tar
.
gz
"
)
)
        
if
behavior
and
behavior
!
=
"
mac_sign
"
:
            
artifacts
.
add
(
input
.
replace
(
"
.
dmg
"
"
.
pkg
"
)
)
    
else
:
        
artifacts
.
add
(
input
)
    
if
"
gcp_prod_autograph_gpg
"
in
formats
:
        
artifacts
.
add
(
f
"
{
input
}
.
asc
"
)
    
return
artifacts
