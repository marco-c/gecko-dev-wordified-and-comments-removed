"
"
"
Generic
ways
to
upload
+
download
files
.
"
"
"
import
pprint
try
:
    
from
urllib2
import
urlopen
except
ImportError
:
    
from
urllib
.
request
import
urlopen
import
json
from
mozharness
.
base
.
log
import
DEBUG
class
TransferMixin
:
    
"
"
"
    
Generic
transfer
methods
.
    
Dependent
on
BaseScript
.
    
"
"
"
    
def
load_json_from_url
(
self
url
timeout
=
30
log_level
=
DEBUG
)
:
        
self
.
log
(
            
"
Attempting
to
download
%
s
;
timeout
=
%
i
"
%
(
url
timeout
)
level
=
log_level
        
)
        
try
:
            
r
=
urlopen
(
url
timeout
=
timeout
)
            
j
=
json
.
load
(
r
)
            
self
.
log
(
pprint
.
pformat
(
j
)
level
=
log_level
)
        
except
BaseException
:
            
self
.
exception
(
message
=
"
Unable
to
download
%
s
!
"
%
url
)
            
raise
        
return
j
