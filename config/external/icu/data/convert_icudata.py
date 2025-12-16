import
os
import
subprocess
import
buildconfig
def
main
(
output
data_file
)
:
    
output
.
close
(
)
    
subprocess
.
run
(
        
[
            
os
.
path
.
join
(
buildconfig
.
topobjdir
"
dist
"
"
host
"
"
bin
"
"
icupkg
"
)
            
"
-
tb
"
            
data_file
            
output
.
name
        
]
        
check
=
True
    
)
