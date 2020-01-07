import
os
import
os
.
path
from
pip9
.
compat
import
get_path_uid
def
check_path_owner
(
path
)
:
    
if
not
hasattr
(
os
"
geteuid
"
)
:
        
return
True
    
previous
=
None
    
while
path
!
=
previous
:
        
if
os
.
path
.
lexists
(
path
)
:
            
if
os
.
geteuid
(
)
=
=
0
:
                
try
:
                    
path_uid
=
get_path_uid
(
path
)
                
except
OSError
:
                    
return
False
                
return
path_uid
=
=
0
            
else
:
                
return
os
.
access
(
path
os
.
W_OK
)
        
else
:
            
previous
path
=
path
os
.
path
.
dirname
(
path
)
