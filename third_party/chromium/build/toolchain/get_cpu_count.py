import
multiprocessing
import
sys
def
main
(
)
:
  
try
:
    
cpu_count
=
multiprocessing
.
cpu_count
(
)
  
except
:
    
cpu_count
=
1
  
print
(
cpu_count
)
  
return
0
if
__name__
=
=
'
__main__
'
:
  
sys
.
exit
(
main
(
)
)
