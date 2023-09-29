import
multiprocessing
import
sys
def
max_parallelism
(
)
-
>
int
:
    
cpu_count
=
multiprocessing
.
cpu_count
(
)
    
if
sys
.
platform
=
=
'
win32
'
:
        
cpu_count
=
min
(
cpu_count
56
)
    
return
cpu_count
