import
contextlib
import
errno
import
logging
import
logging
.
handlers
import
os
import
sys
from
logging
import
Filter
from
typing
import
IO
Any
Callable
Iterator
Optional
TextIO
Type
cast
from
pip
.
_internal
.
utils
.
_log
import
VERBOSE
getLogger
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
deprecation
import
DEPRECATION_MSG_PREFIX
from
pip
.
_internal
.
utils
.
misc
import
ensure_dir
try
:
    
import
threading
except
ImportError
:
    
import
dummy_threading
as
threading
try
:
    
from
pip
.
_vendor
import
colorama
except
Exception
:
    
colorama
=
None
_log_state
=
threading
.
local
(
)
subprocess_logger
=
getLogger
(
"
pip
.
subprocessor
"
)
class
BrokenStdoutLoggingError
(
Exception
)
:
    
"
"
"
    
Raised
if
BrokenPipeError
occurs
for
the
stdout
stream
while
logging
.
    
"
"
"
    
pass
if
WINDOWS
:
    
def
_is_broken_pipe_error
(
exc_class
exc
)
:
        
"
"
"
See
the
docstring
for
non
-
Windows
below
.
"
"
"
        
return
(
exc_class
is
BrokenPipeError
)
or
(
            
isinstance
(
exc
OSError
)
and
exc
.
errno
in
(
errno
.
EINVAL
errno
.
EPIPE
)
        
)
else
:
    
def
_is_broken_pipe_error
(
exc_class
exc
)
:
        
"
"
"
        
Return
whether
an
exception
is
a
broken
pipe
error
.
        
Args
:
          
exc_class
:
an
exception
class
.
          
exc
:
an
exception
instance
.
        
"
"
"
        
return
exc_class
is
BrokenPipeError
contextlib
.
contextmanager
def
indent_log
(
num
=
2
)
:
    
"
"
"
    
A
context
manager
which
will
cause
the
log
output
to
be
indented
for
any
    
log
messages
emitted
inside
it
.
    
"
"
"
    
_log_state
.
indentation
=
get_indentation
(
)
    
_log_state
.
indentation
+
=
num
    
try
:
        
yield
    
finally
:
        
_log_state
.
indentation
-
=
num
def
get_indentation
(
)
:
    
return
getattr
(
_log_state
"
indentation
"
0
)
class
IndentingFormatter
(
logging
.
Formatter
)
:
    
default_time_format
=
"
%
Y
-
%
m
-
%
dT
%
H
:
%
M
:
%
S
"
    
def
__init__
(
        
self
        
*
args
        
add_timestamp
=
False
        
*
*
kwargs
    
)
:
        
"
"
"
        
A
logging
.
Formatter
that
obeys
the
indent_log
(
)
context
manager
.
        
:
param
add_timestamp
:
A
bool
indicating
output
lines
should
be
prefixed
            
with
their
record
'
s
timestamp
.
        
"
"
"
        
self
.
add_timestamp
=
add_timestamp
        
super
(
)
.
__init__
(
*
args
*
*
kwargs
)
    
def
get_message_start
(
self
formatted
levelno
)
:
        
"
"
"
        
Return
the
start
of
the
formatted
log
message
(
not
counting
the
        
prefix
to
add
to
each
line
)
.
        
"
"
"
        
if
levelno
<
logging
.
WARNING
:
            
return
"
"
        
if
formatted
.
startswith
(
DEPRECATION_MSG_PREFIX
)
:
            
return
"
"
        
if
levelno
<
logging
.
ERROR
:
            
return
"
WARNING
:
"
        
return
"
ERROR
:
"
    
def
format
(
self
record
)
:
        
"
"
"
        
Calls
the
standard
formatter
but
will
indent
all
of
the
log
message
        
lines
by
our
current
indentation
level
.
        
"
"
"
        
formatted
=
super
(
)
.
format
(
record
)
        
message_start
=
self
.
get_message_start
(
formatted
record
.
levelno
)
        
formatted
=
message_start
+
formatted
        
prefix
=
"
"
        
if
self
.
add_timestamp
:
            
prefix
=
f
"
{
self
.
formatTime
(
record
)
}
"
        
prefix
+
=
"
"
*
get_indentation
(
)
        
formatted
=
"
"
.
join
(
[
prefix
+
line
for
line
in
formatted
.
splitlines
(
True
)
]
)
        
return
formatted
def
_color_wrap
(
*
colors
)
:
    
def
wrapped
(
inp
)
:
        
return
"
"
.
join
(
list
(
colors
)
+
[
inp
colorama
.
Style
.
RESET_ALL
]
)
    
return
wrapped
class
ColorizedStreamHandler
(
logging
.
StreamHandler
)
:
    
if
colorama
:
        
COLORS
=
[
            
(
logging
.
ERROR
_color_wrap
(
colorama
.
Fore
.
RED
)
)
            
(
logging
.
WARNING
_color_wrap
(
colorama
.
Fore
.
YELLOW
)
)
        
]
    
else
:
        
COLORS
=
[
]
    
def
__init__
(
self
stream
=
None
no_color
=
None
)
:
        
super
(
)
.
__init__
(
stream
)
        
self
.
_no_color
=
no_color
        
if
WINDOWS
and
colorama
:
            
self
.
stream
=
colorama
.
AnsiToWin32
(
self
.
stream
)
    
def
_using_stdout
(
self
)
:
        
"
"
"
        
Return
whether
the
handler
is
using
sys
.
stdout
.
        
"
"
"
        
if
WINDOWS
and
colorama
:
            
stream
=
cast
(
colorama
.
AnsiToWin32
self
.
stream
)
            
return
stream
.
wrapped
is
sys
.
stdout
        
return
self
.
stream
is
sys
.
stdout
    
def
should_color
(
self
)
:
        
if
not
colorama
or
self
.
_no_color
:
            
return
False
        
real_stream
=
(
            
self
.
stream
            
if
not
isinstance
(
self
.
stream
colorama
.
AnsiToWin32
)
            
else
self
.
stream
.
wrapped
        
)
        
if
hasattr
(
real_stream
"
isatty
"
)
and
real_stream
.
isatty
(
)
:
            
return
True
        
if
os
.
environ
.
get
(
"
TERM
"
)
=
=
"
ANSI
"
:
            
return
True
        
return
False
    
def
format
(
self
record
)
:
        
msg
=
super
(
)
.
format
(
record
)
        
if
self
.
should_color
(
)
:
            
for
level
color
in
self
.
COLORS
:
                
if
record
.
levelno
>
=
level
:
                    
msg
=
color
(
msg
)
                    
break
        
return
msg
    
def
handleError
(
self
record
)
:
        
exc_class
exc
=
sys
.
exc_info
(
)
[
:
2
]
        
if
(
            
exc_class
            
and
exc
            
and
self
.
_using_stdout
(
)
            
and
_is_broken_pipe_error
(
exc_class
exc
)
        
)
:
            
raise
BrokenStdoutLoggingError
(
)
        
return
super
(
)
.
handleError
(
record
)
class
BetterRotatingFileHandler
(
logging
.
handlers
.
RotatingFileHandler
)
:
    
def
_open
(
self
)
:
        
ensure_dir
(
os
.
path
.
dirname
(
self
.
baseFilename
)
)
        
return
super
(
)
.
_open
(
)
class
MaxLevelFilter
(
Filter
)
:
    
def
__init__
(
self
level
)
:
        
self
.
level
=
level
    
def
filter
(
self
record
)
:
        
return
record
.
levelno
<
self
.
level
class
ExcludeLoggerFilter
(
Filter
)
:
    
"
"
"
    
A
logging
Filter
that
excludes
records
from
a
logger
(
or
its
children
)
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
        
return
not
super
(
)
.
filter
(
record
)
def
setup_logging
(
verbosity
no_color
user_log_file
)
:
    
"
"
"
Configures
and
sets
up
all
of
the
logging
    
Returns
the
requested
logging
level
as
its
integer
value
.
    
"
"
"
    
if
verbosity
>
=
2
:
        
level_number
=
logging
.
DEBUG
    
elif
verbosity
=
=
1
:
        
level_number
=
VERBOSE
    
elif
verbosity
=
=
-
1
:
        
level_number
=
logging
.
WARNING
    
elif
verbosity
=
=
-
2
:
        
level_number
=
logging
.
ERROR
    
elif
verbosity
<
=
-
3
:
        
level_number
=
logging
.
CRITICAL
    
else
:
        
level_number
=
logging
.
INFO
    
level
=
logging
.
getLevelName
(
level_number
)
    
include_user_log
=
user_log_file
is
not
None
    
if
include_user_log
:
        
additional_log_file
=
user_log_file
        
root_level
=
"
DEBUG
"
    
else
:
        
additional_log_file
=
"
/
dev
/
null
"
        
root_level
=
level
    
vendored_log_level
=
"
WARNING
"
if
level
in
[
"
INFO
"
"
ERROR
"
]
else
"
DEBUG
"
    
log_streams
=
{
        
"
stdout
"
:
"
ext
:
/
/
sys
.
stdout
"
        
"
stderr
"
:
"
ext
:
/
/
sys
.
stderr
"
    
}
    
handler_classes
=
{
        
"
stream
"
:
"
pip
.
_internal
.
utils
.
logging
.
ColorizedStreamHandler
"
        
"
file
"
:
"
pip
.
_internal
.
utils
.
logging
.
BetterRotatingFileHandler
"
    
}
    
handlers
=
[
"
console
"
"
console_errors
"
"
console_subprocess
"
]
+
(
        
[
"
user_log
"
]
if
include_user_log
else
[
]
    
)
    
logging
.
config
.
dictConfig
(
        
{
            
"
version
"
:
1
            
"
disable_existing_loggers
"
:
False
            
"
filters
"
:
{
                
"
exclude_warnings
"
:
{
                    
"
(
)
"
:
"
pip
.
_internal
.
utils
.
logging
.
MaxLevelFilter
"
                    
"
level
"
:
logging
.
WARNING
                
}
                
"
restrict_to_subprocess
"
:
{
                    
"
(
)
"
:
"
logging
.
Filter
"
                    
"
name
"
:
subprocess_logger
.
name
                
}
                
"
exclude_subprocess
"
:
{
                    
"
(
)
"
:
"
pip
.
_internal
.
utils
.
logging
.
ExcludeLoggerFilter
"
                    
"
name
"
:
subprocess_logger
.
name
                
}
            
}
            
"
formatters
"
:
{
                
"
indent
"
:
{
                    
"
(
)
"
:
IndentingFormatter
                    
"
format
"
:
"
%
(
message
)
s
"
                
}
                
"
indent_with_timestamp
"
:
{
                    
"
(
)
"
:
IndentingFormatter
                    
"
format
"
:
"
%
(
message
)
s
"
                    
"
add_timestamp
"
:
True
                
}
            
}
            
"
handlers
"
:
{
                
"
console
"
:
{
                    
"
level
"
:
level
                    
"
class
"
:
handler_classes
[
"
stream
"
]
                    
"
no_color
"
:
no_color
                    
"
stream
"
:
log_streams
[
"
stdout
"
]
                    
"
filters
"
:
[
"
exclude_subprocess
"
"
exclude_warnings
"
]
                    
"
formatter
"
:
"
indent
"
                
}
                
"
console_errors
"
:
{
                    
"
level
"
:
"
WARNING
"
                    
"
class
"
:
handler_classes
[
"
stream
"
]
                    
"
no_color
"
:
no_color
                    
"
stream
"
:
log_streams
[
"
stderr
"
]
                    
"
filters
"
:
[
"
exclude_subprocess
"
]
                    
"
formatter
"
:
"
indent
"
                
}
                
"
console_subprocess
"
:
{
                    
"
level
"
:
level
                    
"
class
"
:
handler_classes
[
"
stream
"
]
                    
"
no_color
"
:
no_color
                    
"
stream
"
:
log_streams
[
"
stderr
"
]
                    
"
filters
"
:
[
"
restrict_to_subprocess
"
]
                    
"
formatter
"
:
"
indent
"
                
}
                
"
user_log
"
:
{
                    
"
level
"
:
"
DEBUG
"
                    
"
class
"
:
handler_classes
[
"
file
"
]
                    
"
filename
"
:
additional_log_file
                    
"
encoding
"
:
"
utf
-
8
"
                    
"
delay
"
:
True
                    
"
formatter
"
:
"
indent_with_timestamp
"
                
}
            
}
            
"
root
"
:
{
                
"
level
"
:
root_level
                
"
handlers
"
:
handlers
            
}
            
"
loggers
"
:
{
"
pip
.
_vendor
"
:
{
"
level
"
:
vendored_log_level
}
}
        
}
    
)
    
return
level_number
