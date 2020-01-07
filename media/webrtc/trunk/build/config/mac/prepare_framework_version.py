import
os
import
shutil
import
sys
def
PrepareFrameworkVersion
(
version_file
framework_root_dir
version
)
:
  
try
:
    
with
open
(
version_file
'
r
'
)
as
f
:
      
current_version
=
f
.
read
(
)
      
if
current_version
=
=
version
:
        
return
  
except
IOError
:
    
pass
  
if
os
.
path
.
exists
(
framework_root_dir
)
:
    
shutil
.
rmtree
(
framework_root_dir
)
  
dirname
=
os
.
path
.
dirname
(
version_file
)
  
if
not
os
.
path
.
isdir
(
dirname
)
:
    
os
.
makedirs
(
dirname
0700
)
  
with
open
(
version_file
'
w
+
'
)
as
f
:
    
f
.
write
(
version
)
if
__name__
=
=
'
__main__
'
:
  
PrepareFrameworkVersion
(
sys
.
argv
[
1
]
sys
.
argv
[
2
]
sys
.
argv
[
3
]
)
  
sys
.
exit
(
0
)
