from
sys
import
version_info
if
version_info
[
:
2
]
<
=
(
2
5
)
:
    
def
partition
(
string
sep
)
:
        
try
:
            
a
c
=
string
.
split
(
sep
1
)
        
except
ValueError
:
            
a
b
c
=
string
'
'
'
'
        
else
:
            
b
=
sep
        
return
a
b
c
else
:
    
def
partition
(
string
sep
)
:
        
return
string
.
partition
(
sep
)
