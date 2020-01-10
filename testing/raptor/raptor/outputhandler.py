from
__future__
import
absolute_import
import
json
from
logger
.
logger
import
RaptorLogger
LOG
=
RaptorLogger
(
component
=
'
raptor
-
output
-
handler
'
)
class
OutputHandler
(
object
)
:
    
def
__init__
(
self
)
:
        
self
.
proc
=
None
    
def
__call__
(
self
line
)
:
        
if
not
line
.
strip
(
)
:
            
return
        
line
=
line
.
decode
(
'
utf
-
8
'
errors
=
'
replace
'
)
        
try
:
            
data
=
json
.
loads
(
line
)
        
except
ValueError
:
            
self
.
process_output
(
line
)
            
return
        
if
isinstance
(
data
dict
)
and
'
action
'
in
data
:
            
LOG
.
log_raw
(
data
)
        
else
:
            
self
.
process_output
(
json
.
dumps
(
data
)
)
    
def
process_output
(
self
line
)
:
        
if
"
raptor
"
in
line
:
            
LOG
.
process_output
(
self
.
proc
.
pid
line
)
