import
buildconfig
def
main
(
output
input
)
:
    
if
buildconfig
.
substs
[
'
OS_ARCH
'
]
not
in
(
'
Linux
'
'
Darwin
'
)
:
        
print
"
Error
:
unhandled
OS_ARCH
%
s
"
%
buildconfig
.
substs
[
'
OS_ARCH
'
]
        
return
1
    
is_linux
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
Linux
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
not
is_linux
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
is_linux
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
                
else
:
                    
line
=
line
[
:
i
]
            
if
line
and
not
is_linux
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
