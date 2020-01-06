"
"
"
Execute
computations
asynchronously
using
threads
or
processes
.
"
"
"
__author__
=
'
Brian
Quinlan
(
brian
sweetapp
.
com
)
'
from
concurrent
.
futures
.
_base
import
(
FIRST_COMPLETED
                                      
FIRST_EXCEPTION
                                      
ALL_COMPLETED
                                      
CancelledError
                                      
TimeoutError
                                      
Future
                                      
Executor
                                      
wait
                                      
as_completed
)
from
concurrent
.
futures
.
thread
import
ThreadPoolExecutor
try
:
    
from
concurrent
.
futures
.
process
import
ProcessPoolExecutor
except
ImportError
:
    
pass
