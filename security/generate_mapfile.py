import
buildconfig
def
main
(
output
input
)
:
    
is_darwin
=
buildconfig
.
substs
[
"
OS_ARCH
"
]
=
=
"
Darwin
"
    
is_mingw
=
"
WINNT
"
=
=
buildconfig
.
substs
[
"
OS_ARCH
"
]
and
buildconfig
.
substs
.
get
(
        
"
GCC_USE_GNU_LD
"
    
)
    
with
open
(
input
encoding
=
"
utf
-
8
"
)
as
f
:
        
for
line
in
f
:
            
line
=
line
.
rstrip
(
)
            
if
not
is_mingw
and
"
;
-
"
in
line
:
                
continue
            
if
is_darwin
and
"
;
+
"
in
line
:
                
continue
            
line
=
line
.
replace
(
"
DATA
"
"
"
)
            
if
not
is_mingw
:
                
line
=
line
.
replace
(
"
;
+
"
"
"
)
            
line
=
line
.
replace
(
"
;
;
"
"
"
)
            
i
=
line
.
find
(
"
;
"
)
            
if
i
!
=
-
1
:
                
if
is_darwin
or
is_mingw
:
                    
line
=
line
[
:
i
]
                
else
:
                    
line
=
line
[
:
i
+
1
]
            
if
line
and
is_darwin
:
                
output
.
write
(
"
_
"
)
            
output
.
write
(
line
)
            
output
.
write
(
"
\
n
"
)
