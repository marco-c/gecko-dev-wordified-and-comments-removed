from
__future__
import
absolute_import
unicode_literals
def
get_logger
(
logger_name
)
:
    
"
"
"
Returns
the
logger
that
should
be
used
based
on
logger_name
.
    
Defaults
to
the
logging
logger
if
mozlog
cannot
be
imported
.
    
:
returns
:
mozlog
or
logging
logger
object
    
"
"
"
    
logger
=
None
    
try
:
        
import
mozlog
        
logger
=
mozlog
.
get_default_logger
(
logger_name
)
    
except
ImportError
:
        
pass
    
if
logger
is
None
:
        
import
logging
        
logging
.
basicConfig
(
)
        
logger
=
logging
.
getLogger
(
logger_name
)
    
return
logger
