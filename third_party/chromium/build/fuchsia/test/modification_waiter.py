"
"
"
An
AbstractContextManager
to
wait
the
modifications
to
finish
during
exit
.
"
"
"
import
os
import
time
from
contextlib
import
AbstractContextManager
class
ModificationWaiter
(
AbstractContextManager
)
:
    
"
"
"
Exits
if
there
is
no
modifications
for
a
certain
time
period
or
the
    
timeout
has
been
reached
.
"
"
"
    
def
__init__
(
self
path
:
str
)
-
>
None
:
        
self
.
_path
=
path
        
self
.
_timeout
=
60
        
self
.
_quiet_time
=
5
    
def
__enter__
(
self
)
-
>
None
:
        
return
    
def
__exit__
(
self
exc_type
exc_value
traceback
)
-
>
bool
:
        
last_mod_time
=
time
.
time
(
)
        
start_time
=
last_mod_time
        
while
True
:
            
cur_time
=
time
.
time
(
)
            
if
cur_time
-
start_time
>
=
self
.
_timeout
:
                
break
            
cur_mod_time
=
os
.
path
.
getmtime
(
self
.
_path
)
            
if
cur_mod_time
>
last_mod_time
:
                
last_mod_time
=
cur_mod_time
            
elif
cur_time
-
last_mod_time
>
=
self
.
_quiet_time
:
                
break
            
time
.
sleep
(
1
)
        
return
False
