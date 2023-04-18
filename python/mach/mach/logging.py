from
__future__
import
absolute_import
unicode_literals
try
:
    
import
blessings
except
ImportError
:
    
blessings
=
None
import
codecs
import
json
import
logging
import
six
import
sys
import
time
def
_wrap_stdstream
(
fh
)
:
    
if
fh
in
(
sys
.
stderr
sys
.
stdout
)
:
        
encoding
=
sys
.
getdefaultencoding
(
)
        
encoding
=
"
utf
-
8
"
if
encoding
in
(
"
ascii
"
"
charmap
"
)
else
encoding
        
if
six
.
PY2
:
            
return
codecs
.
getwriter
(
encoding
)
(
fh
errors
=
"
replace
"
)
        
else
:
            
return
codecs
.
getwriter
(
encoding
)
(
fh
.
buffer
errors
=
"
replace
"
)
    
else
:
        
return
fh
def
format_seconds
(
total
)
:
    
"
"
"
Format
number
of
seconds
to
MM
:
SS
.
DD
form
.
"
"
"
    
minutes
seconds
=
divmod
(
total
60
)
    
return
"
%
2d
:
%
05
.
2f
"
%
(
minutes
seconds
)
class
ConvertToStructuredFilter
(
logging
.
Filter
)
:
    
"
"
"
Filter
that
converts
unstructured
records
into
structured
ones
.
"
"
"
    
def
filter
(
self
record
)
:
        
if
hasattr
(
record
"
action
"
)
and
hasattr
(
record
"
params
"
)
:
            
return
True
        
record
.
action
=
"
unstructured
"
        
record
.
params
=
{
"
msg
"
:
record
.
getMessage
(
)
}
        
record
.
msg
=
"
{
msg
}
"
        
return
True
class
StructuredJSONFormatter
(
logging
.
Formatter
)
:
    
"
"
"
Log
formatter
that
writes
a
structured
JSON
entry
.
"
"
"
    
def
format
(
self
record
)
:
        
action
=
getattr
(
record
"
action
"
"
UNKNOWN
"
)
        
params
=
getattr
(
record
"
params
"
{
}
)
        
return
json
.
dumps
(
[
record
.
created
action
params
]
)
class
StructuredHumanFormatter
(
logging
.
Formatter
)
:
    
"
"
"
Log
formatter
that
writes
structured
messages
for
humans
.
    
It
is
important
that
this
formatter
never
be
added
to
a
logger
that
    
produces
unstructured
/
classic
log
messages
.
If
it
is
the
call
to
format
(
)
    
could
fail
because
the
string
could
contain
things
(
like
JSON
)
that
look
    
like
formatting
character
sequences
.
    
Because
of
this
limitation
format
(
)
will
fail
with
a
KeyError
if
an
    
unstructured
record
is
passed
or
if
the
structured
message
is
malformed
.
    
"
"
"
    
def
__init__
(
self
start_time
write_interval
=
False
write_times
=
True
)
:
        
self
.
start_time
=
start_time
        
self
.
write_interval
=
write_interval
        
self
.
write_times
=
write_times
        
self
.
last_time
=
None
    
def
format
(
self
record
)
:
        
formatted_msg
=
record
.
msg
.
format
(
*
*
record
.
params
)
        
elapsed_time
=
(
            
format_seconds
(
self
.
_time
(
record
)
)
+
"
"
if
self
.
write_times
else
"
"
        
)
        
rv
=
elapsed_time
+
formatted_msg
        
stack_trace
=
"
\
n
"
+
elapsed_time
+
formatted_stack_trace
(
record
self
)
        
rv
+
=
stack_trace
.
replace
(
"
\
n
"
f
"
\
n
{
elapsed_time
}
"
)
        
return
rv
    
def
_time
(
self
record
)
:
        
t
=
record
.
created
-
self
.
start_time
        
if
self
.
write_interval
and
self
.
last_time
is
not
None
:
            
t
=
record
.
created
-
self
.
last_time
        
self
.
last_time
=
record
.
created
        
return
t
class
StructuredTerminalFormatter
(
StructuredHumanFormatter
)
:
    
"
"
"
Log
formatter
for
structured
messages
writing
to
a
terminal
.
"
"
"
    
def
set_terminal
(
self
terminal
)
:
        
self
.
terminal
=
terminal
        
self
.
_sgr0
=
terminal
.
normal
if
terminal
and
blessings
else
"
"
    
def
format
(
self
record
)
:
        
formatted_msg
=
record
.
msg
.
format
(
*
*
record
.
params
)
        
elapsed_time
=
(
            
self
.
terminal
.
blue
(
format_seconds
(
self
.
_time
(
record
)
)
)
+
"
"
            
if
self
.
write_times
            
else
"
"
        
)
        
rv
=
elapsed_time
+
self
.
_colorize
(
formatted_msg
)
+
self
.
sgr0
        
stack_trace
=
"
\
n
"
+
elapsed_time
+
formatted_stack_trace
(
record
self
)
        
rv
+
=
stack_trace
.
replace
(
"
\
n
"
f
"
\
n
{
elapsed_time
}
"
)
        
return
rv
+
self
.
sgr0
    
def
_colorize
(
self
s
)
:
        
if
not
self
.
terminal
:
            
return
s
        
result
=
s
        
reftest
=
s
.
startswith
(
"
REFTEST
"
)
        
if
reftest
:
            
s
=
s
[
8
:
]
        
if
s
.
startswith
(
"
TEST
-
PASS
"
)
:
            
result
=
self
.
terminal
.
green
(
s
[
0
:
9
]
)
+
s
[
9
:
]
        
elif
s
.
startswith
(
"
TEST
-
UNEXPECTED
"
)
:
            
result
=
self
.
terminal
.
red
(
s
[
0
:
20
]
)
+
s
[
20
:
]
        
elif
s
.
startswith
(
"
TEST
-
START
"
)
:
            
result
=
self
.
terminal
.
yellow
(
s
[
0
:
10
]
)
+
s
[
10
:
]
        
elif
s
.
startswith
(
"
TEST
-
INFO
"
)
:
            
result
=
self
.
terminal
.
yellow
(
s
[
0
:
9
]
)
+
s
[
9
:
]
        
if
reftest
:
            
result
=
"
REFTEST
"
+
result
        
return
result
def
formatted_stack_trace
(
record
formatter
)
:
    
"
"
"
    
Formatting
behavior
here
intended
to
mimic
a
portion
of
the
    
standard
library
'
s
logging
.
Formatter
:
:
format
function
    
"
"
"
    
rv
=
"
"
    
if
record
.
exc_info
:
        
if
not
record
.
exc_text
:
            
record
.
exc_text
=
formatter
.
formatException
(
record
.
exc_info
)
    
if
record
.
exc_text
:
        
rv
=
record
.
exc_text
    
if
record
.
stack_info
:
        
if
rv
[
-
1
:
]
!
=
"
\
n
"
:
            
rv
=
rv
+
"
\
n
"
        
rv
=
rv
+
formatter
.
formatStack
(
record
.
stack_info
)
    
return
rv
class
LoggingManager
(
object
)
:
    
"
"
"
Holds
and
controls
global
logging
state
.
    
An
application
should
instantiate
one
of
these
and
configure
it
as
needed
.
    
This
class
provides
a
mechanism
to
configure
the
output
of
logging
data
    
both
from
mach
and
from
the
overall
logging
system
(
e
.
g
.
from
other
    
modules
)
.
    
"
"
"
    
def
__init__
(
self
)
:
        
self
.
start_time
=
time
.
time
(
)
        
self
.
json_handlers
=
[
]
        
self
.
terminal_handler
=
None
        
self
.
terminal_formatter
=
None
        
self
.
root_logger
=
logging
.
getLogger
(
)
        
self
.
root_logger
.
setLevel
(
logging
.
DEBUG
)
        
self
.
root_logger
.
addHandler
(
logging
.
NullHandler
(
)
)
        
mach_logger
=
logging
.
getLogger
(
"
mach
"
)
        
mach_logger
.
setLevel
(
logging
.
DEBUG
)
        
self
.
structured_filter
=
ConvertToStructuredFilter
(
)
        
self
.
structured_loggers
=
[
mach_logger
]
        
self
.
_terminal
=
None
    
property
    
def
terminal
(
self
)
:
        
if
not
self
.
_terminal
and
blessings
:
            
try
:
                
terminal
=
blessings
.
Terminal
(
stream
=
_wrap_stdstream
(
sys
.
stdout
)
)
                
if
terminal
.
is_a_tty
:
                    
self
.
_terminal
=
terminal
            
except
Exception
:
                
pass
        
return
self
.
_terminal
    
def
add_json_handler
(
self
fh
)
:
        
"
"
"
Enable
JSON
logging
on
the
specified
file
object
.
"
"
"
        
handler
=
logging
.
StreamHandler
(
stream
=
fh
)
        
handler
.
setFormatter
(
StructuredJSONFormatter
(
)
)
        
handler
.
setLevel
(
logging
.
DEBUG
)
        
for
logger
in
self
.
structured_loggers
:
            
logger
.
addHandler
(
handler
)
        
self
.
json_handlers
.
append
(
handler
)
    
def
add_terminal_logging
(
        
self
fh
=
sys
.
stdout
level
=
logging
.
INFO
write_interval
=
False
write_times
=
True
    
)
:
        
"
"
"
Enable
logging
to
the
terminal
.
"
"
"
        
fh
=
_wrap_stdstream
(
fh
)
        
formatter
=
StructuredHumanFormatter
(
            
self
.
start_time
write_interval
=
write_interval
write_times
=
write_times
        
)
        
if
self
.
terminal
:
            
formatter
=
StructuredTerminalFormatter
(
                
self
.
start_time
write_interval
=
write_interval
write_times
=
write_times
            
)
            
formatter
.
set_terminal
(
self
.
terminal
)
        
handler
=
logging
.
StreamHandler
(
stream
=
fh
)
        
handler
.
setFormatter
(
formatter
)
        
handler
.
setLevel
(
level
)
        
for
logger
in
self
.
structured_loggers
:
            
logger
.
addHandler
(
handler
)
        
self
.
terminal_handler
=
handler
        
self
.
terminal_formatter
=
formatter
    
def
replace_terminal_handler
(
self
handler
)
:
        
"
"
"
Replace
the
installed
terminal
handler
.
        
Returns
the
old
handler
or
None
if
none
was
configured
.
        
If
the
new
handler
is
None
removes
any
existing
handler
and
disables
        
logging
to
the
terminal
.
        
"
"
"
        
old
=
self
.
terminal_handler
        
if
old
:
            
for
logger
in
self
.
structured_loggers
:
                
logger
.
removeHandler
(
old
)
        
if
handler
:
            
for
logger
in
self
.
structured_loggers
:
                
logger
.
addHandler
(
handler
)
        
self
.
terminal_handler
=
handler
        
return
old
    
def
enable_unstructured
(
self
)
:
        
"
"
"
Enable
logging
of
unstructured
messages
.
"
"
"
        
if
self
.
terminal_handler
:
            
self
.
terminal_handler
.
addFilter
(
self
.
structured_filter
)
            
self
.
root_logger
.
addHandler
(
self
.
terminal_handler
)
    
def
disable_unstructured
(
self
)
:
        
"
"
"
Disable
logging
of
unstructured
messages
.
"
"
"
        
if
self
.
terminal_handler
:
            
self
.
terminal_handler
.
removeFilter
(
self
.
structured_filter
)
            
self
.
root_logger
.
removeHandler
(
self
.
terminal_handler
)
    
def
register_structured_logger
(
self
logger
terminal
=
True
json
=
True
)
:
        
"
"
"
Register
a
structured
logger
.
        
This
needs
to
be
called
for
all
structured
loggers
that
don
'
t
chain
up
        
to
the
mach
logger
in
order
for
their
output
to
be
captured
.
        
"
"
"
        
self
.
structured_loggers
.
append
(
logger
)
        
if
terminal
and
self
.
terminal_handler
:
            
logger
.
addHandler
(
self
.
terminal_handler
)
        
if
json
:
            
for
handler
in
self
.
json_handlers
:
                
logger
.
addHandler
(
handler
)
    
def
enable_all_structured_loggers
(
self
terminal
=
True
json
=
True
)
:
        
"
"
"
Enable
logging
of
all
structured
messages
from
all
loggers
.
        
terminal
and
json
determine
which
log
handlers
to
operate
        
on
.
By
default
all
known
handlers
are
operated
on
.
        
"
"
"
        
logging
.
getLogger
(
"
glean
"
)
.
setLevel
(
logging
.
CRITICAL
)
        
for
logger
in
self
.
root_logger
.
manager
.
loggerDict
.
values
(
)
:
            
if
not
isinstance
(
logger
logging
.
Logger
)
:
                
continue
            
if
terminal
:
                
logger
.
removeHandler
(
self
.
terminal_handler
)
            
if
json
:
                
for
handler
in
self
.
json_handlers
:
                    
logger
.
removeHandler
(
handler
)
        
self
.
structured_loggers
=
[
]
        
self
.
register_structured_logger
(
self
.
root_logger
terminal
=
terminal
json
=
json
)
