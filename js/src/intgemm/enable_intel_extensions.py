def
main
(
output
intgemm_config
)
:
    
with
open
(
intgemm_config
"
r
"
)
as
f
:
        
config
=
f
.
read
(
)
    
config
=
config
.
replace
(
        
"
#
cmakedefine
INTGEMM_COMPILER_SUPPORTS_AVX2
"
        
"
#
define
INTGEMM_COMPILER_SUPPORTS_AVX2
"
    
)
    
config
=
config
.
replace
(
"
#
cmakedefine
"
"
#
undef
"
)
    
output
.
write
(
config
)
    
output
.
close
(
)
    
return
0
