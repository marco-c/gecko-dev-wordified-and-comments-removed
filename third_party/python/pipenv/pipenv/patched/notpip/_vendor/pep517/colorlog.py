"
"
"
Nicer
log
formatting
with
colours
.
Code
copied
from
Tornado
Apache
licensed
.
"
"
"
import
logging
import
sys
try
:
    
import
curses
except
ImportError
:
    
curses
=
None
def
_stderr_supports_color
(
)
:
    
color
=
False
    
if
curses
and
hasattr
(
sys
.
stderr
'
isatty
'
)
and
sys
.
stderr
.
isatty
(
)
:
        
try
:
            
curses
.
setupterm
(
)
            
if
curses
.
tigetnum
(
"
colors
"
)
>
0
:
                
color
=
True
        
except
Exception
:
            
pass
    
return
color
class
LogFormatter
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
with
colour
support
    
"
"
"
    
DEFAULT_COLORS
=
{
        
logging
.
INFO
:
2
        
logging
.
WARNING
:
3
        
logging
.
ERROR
:
1
        
logging
.
CRITICAL
:
1
    
}
    
def
__init__
(
self
color
=
True
datefmt
=
None
)
:
        
r
"
"
"
        
:
arg
bool
color
:
Enables
color
support
.
        
:
arg
string
fmt
:
Log
message
format
.
        
It
will
be
applied
to
the
attributes
dict
of
log
records
.
The
        
text
between
%
(
color
)
s
and
%
(
end_color
)
s
will
be
colored
        
depending
on
the
level
if
color
support
is
on
.
        
:
arg
dict
colors
:
color
mappings
from
logging
level
to
terminal
color
        
code
        
:
arg
string
datefmt
:
Datetime
format
.
        
Used
for
formatting
(
asctime
)
placeholder
in
prefix_fmt
.
        
.
.
versionchanged
:
:
3
.
2
        
Added
fmt
and
datefmt
arguments
.
        
"
"
"
        
logging
.
Formatter
.
__init__
(
self
datefmt
=
datefmt
)
        
self
.
_colors
=
{
}
        
if
color
and
_stderr_supports_color
(
)
:
            
fg_color
=
(
curses
.
tigetstr
(
"
setaf
"
)
or
                        
curses
.
tigetstr
(
"
setf
"
)
or
"
"
)
            
if
(
3
0
)
<
sys
.
version_info
<
(
3
2
3
)
:
                
fg_color
=
str
(
fg_color
"
ascii
"
)
            
for
levelno
code
in
self
.
DEFAULT_COLORS
.
items
(
)
:
                
self
.
_colors
[
levelno
]
=
str
(
                    
curses
.
tparm
(
fg_color
code
)
"
ascii
"
)
            
self
.
_normal
=
str
(
curses
.
tigetstr
(
"
sgr0
"
)
"
ascii
"
)
            
scr
=
curses
.
initscr
(
)
            
self
.
termwidth
=
scr
.
getmaxyx
(
)
[
1
]
            
curses
.
endwin
(
)
        
else
:
            
self
.
_normal
=
'
'
            
self
.
termwidth
=
70
    
def
formatMessage
(
self
record
)
:
        
mlen
=
len
(
record
.
message
)
        
right_text
=
'
{
initial
}
-
{
name
}
'
.
format
(
initial
=
record
.
levelname
[
0
]
                                               
name
=
record
.
name
)
        
if
mlen
+
len
(
right_text
)
<
self
.
termwidth
:
            
space
=
'
'
*
(
self
.
termwidth
-
(
mlen
+
len
(
right_text
)
)
)
        
else
:
            
space
=
'
'
        
if
record
.
levelno
in
self
.
_colors
:
            
start_color
=
self
.
_colors
[
record
.
levelno
]
            
end_color
=
self
.
_normal
        
else
:
            
start_color
=
end_color
=
'
'
        
return
record
.
message
+
space
+
start_color
+
right_text
+
end_color
def
enable_colourful_output
(
level
=
logging
.
INFO
)
:
    
handler
=
logging
.
StreamHandler
(
)
    
handler
.
setFormatter
(
LogFormatter
(
)
)
    
logging
.
root
.
addHandler
(
handler
)
    
logging
.
root
.
setLevel
(
level
)
