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
'
OS_ARCH
'
]
=
=
'
Darwin
'
    
with
open
(
input
'
rb
'
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
'
;
-
'
in
line
:
                
continue
            
if
is_darwin
and
'
;
+
'
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
'
DATA
'
'
'
)
            
line
=
line
.
replace
(
'
;
+
'
'
'
)
            
line
=
line
.
replace
(
'
;
;
'
'
'
)
            
i
=
line
.
find
(
'
;
'
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
'
_
'
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
'
\
n
'
)
