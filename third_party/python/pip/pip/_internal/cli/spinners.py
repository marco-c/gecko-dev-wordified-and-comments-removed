import
contextlib
import
itertools
import
logging
import
sys
import
time
from
typing
import
IO
Iterator
from
pip
.
_vendor
.
progress
import
HIDE_CURSOR
SHOW_CURSOR
from
pip
.
_internal
.
utils
.
compat
import
WINDOWS
from
pip
.
_internal
.
utils
.
logging
import
get_indentation
logger
=
logging
.
getLogger
(
__name__
)
class
SpinnerInterface
:
    
def
spin
(
self
)
-
>
None
:
        
raise
NotImplementedError
(
)
    
def
finish
(
self
final_status
:
str
)
-
>
None
:
        
raise
NotImplementedError
(
)
class
InteractiveSpinner
(
SpinnerInterface
)
:
    
def
__init__
(
        
self
        
message
:
str
        
file
:
IO
[
str
]
=
None
        
spin_chars
:
str
=
"
-
\
\
|
/
"
        
min_update_interval_seconds
:
float
=
0
.
125
    
)
:
        
self
.
_message
=
message
        
if
file
is
None
:
            
file
=
sys
.
stdout
        
self
.
_file
=
file
        
self
.
_rate_limiter
=
RateLimiter
(
min_update_interval_seconds
)
        
self
.
_finished
=
False
        
self
.
_spin_cycle
=
itertools
.
cycle
(
spin_chars
)
        
self
.
_file
.
write
(
"
"
*
get_indentation
(
)
+
self
.
_message
+
"
.
.
.
"
)
        
self
.
_width
=
0
    
def
_write
(
self
status
:
str
)
-
>
None
:
        
assert
not
self
.
_finished
        
backup
=
"
\
b
"
*
self
.
_width
        
self
.
_file
.
write
(
backup
+
"
"
*
self
.
_width
+
backup
)
        
self
.
_file
.
write
(
status
)
        
self
.
_width
=
len
(
status
)
        
self
.
_file
.
flush
(
)
        
self
.
_rate_limiter
.
reset
(
)
    
def
spin
(
self
)
-
>
None
:
        
if
self
.
_finished
:
            
return
        
if
not
self
.
_rate_limiter
.
ready
(
)
:
            
return
        
self
.
_write
(
next
(
self
.
_spin_cycle
)
)
    
def
finish
(
self
final_status
:
str
)
-
>
None
:
        
if
self
.
_finished
:
            
return
        
self
.
_write
(
final_status
)
        
self
.
_file
.
write
(
"
\
n
"
)
        
self
.
_file
.
flush
(
)
        
self
.
_finished
=
True
class
NonInteractiveSpinner
(
SpinnerInterface
)
:
    
def
__init__
(
self
message
:
str
min_update_interval_seconds
:
float
=
60
.
0
)
-
>
None
:
        
self
.
_message
=
message
        
self
.
_finished
=
False
        
self
.
_rate_limiter
=
RateLimiter
(
min_update_interval_seconds
)
        
self
.
_update
(
"
started
"
)
    
def
_update
(
self
status
:
str
)
-
>
None
:
        
assert
not
self
.
_finished
        
self
.
_rate_limiter
.
reset
(
)
        
logger
.
info
(
"
%
s
:
%
s
"
self
.
_message
status
)
    
def
spin
(
self
)
-
>
None
:
        
if
self
.
_finished
:
            
return
        
if
not
self
.
_rate_limiter
.
ready
(
)
:
            
return
        
self
.
_update
(
"
still
running
.
.
.
"
)
    
def
finish
(
self
final_status
:
str
)
-
>
None
:
        
if
self
.
_finished
:
            
return
        
self
.
_update
(
f
"
finished
with
status
'
{
final_status
}
'
"
)
        
self
.
_finished
=
True
class
RateLimiter
:
    
def
__init__
(
self
min_update_interval_seconds
:
float
)
-
>
None
:
        
self
.
_min_update_interval_seconds
=
min_update_interval_seconds
        
self
.
_last_update
:
float
=
0
    
def
ready
(
self
)
-
>
bool
:
        
now
=
time
.
time
(
)
        
delta
=
now
-
self
.
_last_update
        
return
delta
>
=
self
.
_min_update_interval_seconds
    
def
reset
(
self
)
-
>
None
:
        
self
.
_last_update
=
time
.
time
(
)
contextlib
.
contextmanager
def
open_spinner
(
message
:
str
)
-
>
Iterator
[
SpinnerInterface
]
:
    
if
sys
.
stdout
.
isatty
(
)
and
logger
.
getEffectiveLevel
(
)
<
=
logging
.
INFO
:
        
spinner
:
SpinnerInterface
=
InteractiveSpinner
(
message
)
    
else
:
        
spinner
=
NonInteractiveSpinner
(
message
)
    
try
:
        
with
hidden_cursor
(
sys
.
stdout
)
:
            
yield
spinner
    
except
KeyboardInterrupt
:
        
spinner
.
finish
(
"
canceled
"
)
        
raise
    
except
Exception
:
        
spinner
.
finish
(
"
error
"
)
        
raise
    
else
:
        
spinner
.
finish
(
"
done
"
)
contextlib
.
contextmanager
def
hidden_cursor
(
file
:
IO
[
str
]
)
-
>
Iterator
[
None
]
:
    
if
WINDOWS
:
        
yield
    
elif
not
file
.
isatty
(
)
or
logger
.
getEffectiveLevel
(
)
>
logging
.
INFO
:
        
yield
    
else
:
        
file
.
write
(
HIDE_CURSOR
)
        
try
:
            
yield
        
finally
:
            
file
.
write
(
SHOW_CURSOR
)
