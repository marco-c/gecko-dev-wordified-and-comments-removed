import
os
import
stat
def
raise_on_exist_ro_file
(
filename
:
str
)
-
>
None
:
    
try
:
        
file_stat
=
os
.
stat
(
filename
)
    
except
OSError
:
        
return
None
    
if
file_stat
.
st_mtime
!
=
0
:
        
if
not
(
file_stat
.
st_mode
&
stat
.
S_IWUSR
)
:
            
raise
PermissionError
(
f
"
Permission
denied
:
{
filename
!
r
}
"
)
__all__
=
[
    
"
raise_on_exist_ro_file
"
]
