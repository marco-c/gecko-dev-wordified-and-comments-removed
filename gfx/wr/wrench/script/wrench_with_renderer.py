import
os
import
subprocess
import
sys
def
is_linux
(
)
:
    
return
sys
.
platform
.
startswith
(
'
linux
'
)
if
is_linux
(
)
:
    
requested_renderer
=
sys
.
argv
[
1
]
    
renderer
=
"
default
"
    
if
requested_renderer
=
=
'
hardware
'
:
        
pass
    
elif
requested_renderer
=
=
'
llvmpipe
'
:
        
os
.
environ
[
"
LIBGL_ALWAYS_SOFTWARE
"
]
=
"
1
"
        
os
.
environ
[
"
GALLIUM_DRIVER
"
]
=
"
llvmpipe
"
    
elif
requested_renderer
=
=
'
softpipe
'
:
        
os
.
environ
[
"
LIBGL_ALWAYS_SOFTWARE
"
]
=
"
1
"
        
os
.
environ
[
"
GALLIUM_DRIVER
"
]
=
"
softpipe
"
    
elif
requested_renderer
=
=
'
swiftshader
'
:
        
renderer
=
'
es3
'
    
else
:
        
print
(
'
Unknown
renderer
'
+
requested_renderer
)
        
sys
.
exit
(
1
)
    
cmd
=
[
        
'
cargo
'
        
'
run
'
        
'
-
-
release
'
        
'
-
-
'
        
'
-
-
no
-
block
'
        
'
-
-
no
-
picture
-
caching
'
        
'
-
-
no
-
subpixel
-
aa
'
        
'
-
-
renderer
'
        
renderer
        
'
load
'
    
]
    
cmd
+
=
sys
.
argv
[
2
:
]
    
print
(
'
Running
:
'
+
'
'
.
join
(
cmd
)
)
    
subprocess
.
check_call
(
cmd
)
else
:
    
print
(
'
This
script
is
only
supported
on
Linux
'
)
