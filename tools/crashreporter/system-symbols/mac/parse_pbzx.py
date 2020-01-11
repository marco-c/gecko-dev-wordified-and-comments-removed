import
struct
import
sys
def
seekread
(
f
offset
=
None
length
=
0
relative
=
True
)
:
    
if
offset
is
not
None
:
        
f
.
seek
(
offset
[
0
1
2
]
[
relative
]
)
    
if
length
!
=
0
:
        
return
f
.
read
(
length
)
def
parse_pbzx
(
pbzx_path
)
:
    
section
=
0
    
xar_out_path
=
"
%
s
.
part
%
02d
.
cpio
.
xz
"
%
(
pbzx_path
section
)
    
f
=
open
(
pbzx_path
"
rb
"
)
    
magic
=
seekread
(
f
length
=
4
)
    
if
magic
!
=
"
pbzx
"
:
        
raise
"
Error
:
Not
a
pbzx
file
"
    
flags
=
seekread
(
f
length
=
8
)
    
flags
=
struct
.
unpack
(
"
>
Q
"
flags
)
[
0
]
    
xar_f
=
open
(
xar_out_path
"
wb
"
)
    
while
flags
&
(
1
<
<
24
)
:
        
flags
=
seekread
(
f
length
=
8
)
        
flags
=
struct
.
unpack
(
"
>
Q
"
flags
)
[
0
]
        
f_length
=
seekread
(
f
length
=
8
)
        
f_length
=
struct
.
unpack
(
"
>
Q
"
f_length
)
[
0
]
        
xzmagic
=
seekread
(
f
length
=
6
)
        
if
xzmagic
!
=
"
\
xfd7zXZ
\
x00
"
:
            
seekread
(
f
offset
=
-
6
length
=
0
)
            
f_content
=
seekread
(
f
length
=
f_length
)
            
section
+
=
1
            
decomp_out
=
"
%
s
.
part
%
02d
.
cpio
"
%
(
pbzx_path
section
)
            
g
=
open
(
decomp_out
"
wb
"
)
            
g
.
write
(
f_content
)
            
g
.
close
(
)
            
xar_f
.
close
(
)
            
section
+
=
1
            
new_out
=
"
%
s
.
part
%
02d
.
cpio
.
xz
"
%
(
pbzx_path
section
)
            
xar_f
=
open
(
new_out
"
wb
"
)
        
else
:
            
f_length
-
=
6
            
f_content
=
seekread
(
f
length
=
f_length
)
            
tail
=
seekread
(
f
offset
=
-
2
length
=
2
)
            
xar_f
.
write
(
xzmagic
)
            
xar_f
.
write
(
f_content
)
            
if
tail
!
=
"
YZ
"
:
                
xar_f
.
close
(
)
                
raise
"
Error
:
Footer
is
not
xar
file
footer
"
    
try
:
        
f
.
close
(
)
        
xar_f
.
close
(
)
    
except
BaseException
:
        
pass
def
main
(
)
:
    
parse_pbzx
(
sys
.
argv
[
1
]
)
if
__name__
=
=
"
__main__
"
:
    
main
(
)
