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
def
average_summary
(
values
)
:
    
"
"
"
Averages
all
given
values
.
    
:
param
list
values
:
list
of
values
to
average
.
    
:
returns
:
float
    
"
"
"
    
return
sum
(
[
float
(
v
)
for
v
in
values
]
)
/
len
(
values
)
def
sum_summary
(
values
)
:
    
"
"
"
Adds
all
values
together
.
    
:
param
list
values
:
list
of
values
to
sum
.
    
:
returns
:
float
    
"
"
"
    
return
sum
(
[
float
(
v
)
for
v
in
values
]
)
