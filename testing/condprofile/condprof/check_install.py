"
"
"
Installs
dependencies
at
runtime
to
simplify
deployment
.
"
"
"
import
sys
PY3
=
sys
.
version_info
.
major
=
=
3
def
install_reqs
(
)
:
    
try
:
        
import
yaml
    
except
Exception
:
        
import
subprocess
        
import
sys
        
import
os
        
root
=
os
.
path
.
join
(
os
.
path
.
dirname
(
__file__
)
"
.
.
"
)
        
if
not
os
.
path
.
exists
(
os
.
path
.
join
(
root
"
mozfile
"
)
)
:
            
req_file
=
PY3
and
"
local
-
requirements
.
txt
"
or
"
local
-
py2
-
requirements
.
txt
"
        
else
:
            
req_file
=
PY3
and
"
requirements
.
txt
"
or
"
py2
-
requirements
.
txt
"
        
subprocess
.
check_call
(
            
[
                
sys
.
executable
                
"
-
m
"
                
"
pip
"
                
"
-
-
isolated
"
                
"
install
"
                
"
-
-
index
-
url
"
                
"
https
:
/
/
pypi
.
python
.
org
/
simple
"
                
"
-
r
"
                
req_file
            
]
            
cwd
=
root
        
)
        
os
.
execl
(
sys
.
executable
sys
.
executable
*
sys
.
argv
)
        
sys
.
exit
(
)
install_reqs
(
)
import
yaml
