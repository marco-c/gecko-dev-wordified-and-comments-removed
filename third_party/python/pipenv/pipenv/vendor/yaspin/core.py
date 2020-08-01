#
-
*
-
coding
:
utf
-
8
-
*
-
"
"
"
yaspin
.
yaspin
~
~
~
~
~
~
~
~
~
~
~
~
~
A
lightweight
terminal
spinner
.
"
"
"
from
__future__
import
absolute_import
import
functools
import
itertools
import
signal
import
sys
import
threading
import
time
import
colorama
from
pipenv
.
vendor
.
vistir
import
cursor
from
.
base_spinner
import
default_spinner
from
.
compat
import
PY2
basestring
builtin_str
bytes
iteritems
str
from
.
constants
import
COLOR_ATTRS
COLOR_MAP
ENCODING
SPINNER_ATTRS
from
.
helpers
import
to_unicode
from
.
termcolor
import
colored
colorama
.
init
(
)
class
Yaspin
(
object
)
:
    
"
"
"
Implements
a
context
manager
that
spawns
a
thread
    
to
write
spinner
frames
into
a
tty
(
stdout
)
during
    
context
execution
.
    
"
"
"
    
def
__init__
(
        
self
        
spinner
=
None
        
text
=
"
"
        
color
=
None
        
on_color
=
None
        
attrs
=
None
        
reversal
=
False
        
side
=
"
left
"
        
sigmap
=
None
    
)
:
        
self
.
_spinner
=
self
.
_set_spinner
(
spinner
)
        
self
.
_frames
=
self
.
_set_frames
(
self
.
_spinner
reversal
)
        
self
.
_interval
=
self
.
_set_interval
(
self
.
_spinner
)
        
self
.
_cycle
=
self
.
_set_cycle
(
self
.
_frames
)
        
self
.
_color
=
self
.
_set_color
(
color
)
if
color
else
color
        
self
.
_on_color
=
self
.
_set_on_color
(
on_color
)
if
on_color
else
on_color
        
self
.
_attrs
=
self
.
_set_attrs
(
attrs
)
if
attrs
else
set
(
)
        
self
.
_color_func
=
self
.
_compose_color_func
(
)
        
self
.
_text
=
self
.
_set_text
(
text
)
        
self
.
_side
=
self
.
_set_side
(
side
)
        
self
.
_reversal
=
reversal
        
self
.
_stop_spin
=
None
        
self
.
_hide_spin
=
None
        
self
.
_spin_thread
=
None
        
self
.
_last_frame
=
None
        
self
.
_stdout_lock
=
threading
.
Lock
(
)
        
self
.
_sigmap
=
sigmap
if
sigmap
else
{
}
        
self
.
_dfl_sigmap
=
{
}
    
def
__repr__
(
self
)
:
        
repr_
=
u
"
<
Yaspin
frames
=
{
0
!
s
}
>
"
.
format
(
self
.
_frames
)
        
if
PY2
:
            
return
repr_
.
encode
(
ENCODING
)
        
return
repr_
    
def
__enter__
(
self
)
:
        
self
.
start
(
)
        
return
self
    
def
__exit__
(
self
exc_type
exc_val
traceback
)
:
        
if
self
.
_spin_thread
.
is_alive
(
)
:
            
self
.
stop
(
)
        
return
False
    
def
__call__
(
self
fn
)
:
        
functools
.
wraps
(
fn
)
        
def
inner
(
*
args
*
*
kwargs
)
:
            
with
self
:
                
return
fn
(
*
args
*
*
kwargs
)
        
return
inner
    
def
__getattr__
(
self
name
)
:
        
if
name
in
SPINNER_ATTRS
:
            
from
.
spinners
import
Spinners
            
sp
=
getattr
(
Spinners
name
)
            
self
.
spinner
=
sp
        
elif
name
in
COLOR_ATTRS
:
            
attr_type
=
COLOR_MAP
[
name
]
            
if
attr_type
=
=
"
attrs
"
:
                
self
.
attrs
=
[
name
]
            
if
attr_type
in
(
"
color
"
"
on_color
"
)
:
                
setattr
(
self
attr_type
name
)
        
elif
name
in
(
"
left
"
"
right
"
)
:
            
self
.
side
=
name
        
else
:
            
raise
AttributeError
(
                
"
'
{
0
}
'
object
has
no
attribute
:
'
{
1
}
'
"
.
format
(
                    
self
.
__class__
.
__name__
name
                
)
            
)
        
return
self
    
property
    
def
spinner
(
self
)
:
        
return
self
.
_spinner
    
spinner
.
setter
    
def
spinner
(
self
sp
)
:
        
self
.
_spinner
=
self
.
_set_spinner
(
sp
)
        
self
.
_frames
=
self
.
_set_frames
(
self
.
_spinner
self
.
_reversal
)
        
self
.
_interval
=
self
.
_set_interval
(
self
.
_spinner
)
        
self
.
_cycle
=
self
.
_set_cycle
(
self
.
_frames
)
    
property
    
def
text
(
self
)
:
        
return
self
.
_text
    
text
.
setter
    
def
text
(
self
txt
)
:
        
self
.
_text
=
self
.
_set_text
(
txt
)
    
property
    
def
color
(
self
)
:
        
return
self
.
_color
    
color
.
setter
    
def
color
(
self
value
)
:
        
self
.
_color
=
self
.
_set_color
(
value
)
if
value
else
value
        
self
.
_color_func
=
self
.
_compose_color_func
(
)
    
property
    
def
on_color
(
self
)
:
        
return
self
.
_on_color
    
on_color
.
setter
    
def
on_color
(
self
value
)
:
        
self
.
_on_color
=
self
.
_set_on_color
(
value
)
if
value
else
value
        
self
.
_color_func
=
self
.
_compose_color_func
(
)
    
property
    
def
attrs
(
self
)
:
        
return
list
(
self
.
_attrs
)
    
attrs
.
setter
    
def
attrs
(
self
value
)
:
        
new_attrs
=
self
.
_set_attrs
(
value
)
if
value
else
set
(
)
        
self
.
_attrs
=
self
.
_attrs
.
union
(
new_attrs
)
        
self
.
_color_func
=
self
.
_compose_color_func
(
)
    
property
    
def
side
(
self
)
:
        
return
self
.
_side
    
side
.
setter
    
def
side
(
self
value
)
:
        
self
.
_side
=
self
.
_set_side
(
value
)
    
property
    
def
reversal
(
self
)
:
        
return
self
.
_reversal
    
reversal
.
setter
    
def
reversal
(
self
value
)
:
        
self
.
_reversal
=
value
        
self
.
_frames
=
self
.
_set_frames
(
self
.
_spinner
self
.
_reversal
)
        
self
.
_cycle
=
self
.
_set_cycle
(
self
.
_frames
)
    
def
start
(
self
)
:
        
if
self
.
_sigmap
:
            
self
.
_register_signal_handlers
(
)
        
if
sys
.
stdout
.
isatty
(
)
:
            
self
.
_hide_cursor
(
)
        
self
.
_stop_spin
=
threading
.
Event
(
)
        
self
.
_hide_spin
=
threading
.
Event
(
)
        
self
.
_spin_thread
=
threading
.
Thread
(
target
=
self
.
_spin
)
        
self
.
_spin_thread
.
start
(
)
    
def
stop
(
self
)
:
        
if
self
.
_dfl_sigmap
:
            
self
.
_reset_signal_handlers
(
)
        
if
self
.
_spin_thread
:
            
self
.
_stop_spin
.
set
(
)
            
self
.
_spin_thread
.
join
(
)
        
sys
.
stdout
.
write
(
"
\
r
"
)
        
self
.
_clear_line
(
)
        
if
sys
.
stdout
.
isatty
(
)
:
            
self
.
_show_cursor
(
)
    
def
hide
(
self
)
:
        
"
"
"
Hide
the
spinner
to
allow
for
custom
writing
to
the
terminal
.
"
"
"
        
thr_is_alive
=
self
.
_spin_thread
and
self
.
_spin_thread
.
is_alive
(
)
        
if
thr_is_alive
and
not
self
.
_hide_spin
.
is_set
(
)
:
            
with
self
.
_stdout_lock
:
                
self
.
_hide_spin
.
set
(
)
                
sys
.
stdout
.
write
(
"
\
r
"
)
                
self
.
_clear_line
(
)
                
sys
.
stdout
.
flush
(
)
    
def
show
(
self
)
:
        
"
"
"
Show
the
hidden
spinner
.
"
"
"
        
thr_is_alive
=
self
.
_spin_thread
and
self
.
_spin_thread
.
is_alive
(
)
        
if
thr_is_alive
and
self
.
_hide_spin
.
is_set
(
)
:
            
with
self
.
_stdout_lock
:
                
self
.
_hide_spin
.
clear
(
)
                
sys
.
stdout
.
write
(
"
\
r
"
)
                
self
.
_clear_line
(
)
    
def
write
(
self
text
)
:
        
"
"
"
Write
text
in
the
terminal
without
breaking
the
spinner
.
"
"
"
        
with
self
.
_stdout_lock
:
            
sys
.
stdout
.
write
(
"
\
r
"
)
            
self
.
_clear_line
(
)
            
_text
=
to_unicode
(
text
)
            
if
PY2
:
                
_text
=
_text
.
encode
(
ENCODING
)
            
assert
isinstance
(
_text
builtin_str
)
            
sys
.
stdout
.
write
(
"
{
0
}
\
n
"
.
format
(
_text
)
)
    
def
ok
(
self
text
=
"
OK
"
)
:
        
"
"
"
Set
Ok
(
success
)
finalizer
to
a
spinner
.
"
"
"
        
_text
=
text
if
text
else
"
OK
"
        
self
.
_freeze
(
_text
)
    
def
fail
(
self
text
=
"
FAIL
"
)
:
        
"
"
"
Set
fail
finalizer
to
a
spinner
.
"
"
"
        
_text
=
text
if
text
else
"
FAIL
"
        
self
.
_freeze
(
_text
)
    
def
_freeze
(
self
final_text
)
:
        
"
"
"
Stop
spinner
compose
last
frame
and
'
freeze
'
it
.
"
"
"
        
text
=
to_unicode
(
final_text
)
        
self
.
_last_frame
=
self
.
_compose_out
(
text
mode
=
"
last
"
)
        
self
.
stop
(
)
        
with
self
.
_stdout_lock
:
            
sys
.
stdout
.
write
(
self
.
_last_frame
)
    
def
_spin
(
self
)
:
        
while
not
self
.
_stop_spin
.
is_set
(
)
:
            
if
self
.
_hide_spin
.
is_set
(
)
:
                
time
.
sleep
(
self
.
_interval
)
                
continue
            
spin_phase
=
next
(
self
.
_cycle
)
            
out
=
self
.
_compose_out
(
spin_phase
)
            
with
self
.
_stdout_lock
:
                
sys
.
stdout
.
write
(
out
)
                
self
.
_clear_line
(
)
                
sys
.
stdout
.
flush
(
)
            
time
.
sleep
(
self
.
_interval
)
    
def
_compose_color_func
(
self
)
:
        
fn
=
functools
.
partial
(
            
colored
            
color
=
self
.
_color
            
on_color
=
self
.
_on_color
            
attrs
=
list
(
self
.
_attrs
)
        
)
        
return
fn
    
def
_compose_out
(
self
frame
mode
=
None
)
:
        
assert
isinstance
(
frame
str
)
        
assert
isinstance
(
self
.
_text
str
)
        
frame
=
frame
.
encode
(
ENCODING
)
if
PY2
else
frame
        
text
=
self
.
_text
.
encode
(
ENCODING
)
if
PY2
else
self
.
_text
        
if
self
.
_color_func
is
not
None
:
            
frame
=
self
.
_color_func
(
frame
)
        
if
self
.
_side
=
=
"
right
"
:
            
frame
text
=
text
frame
        
if
not
mode
:
            
out
=
"
\
r
{
0
}
{
1
}
"
.
format
(
frame
text
)
        
else
:
            
out
=
"
{
0
}
{
1
}
\
n
"
.
format
(
frame
text
)
        
assert
isinstance
(
out
builtin_str
)
        
return
out
    
def
_register_signal_handlers
(
self
)
:
        
try
:
            
if
signal
.
SIGKILL
in
self
.
_sigmap
.
keys
(
)
:
                
raise
ValueError
(
                    
"
Trying
to
set
handler
for
SIGKILL
signal
.
"
                    
"
SIGKILL
cannot
be
cought
or
ignored
in
POSIX
systems
.
"
                
)
        
except
AttributeError
:
            
pass
        
for
sig
sig_handler
in
iteritems
(
self
.
_sigmap
)
:
            
dfl_handler
=
signal
.
getsignal
(
sig
)
            
self
.
_dfl_sigmap
[
sig
]
=
dfl_handler
            
if
callable
(
sig_handler
)
:
                
sig_handler
=
functools
.
partial
(
sig_handler
spinner
=
self
)
            
signal
.
signal
(
sig
sig_handler
)
    
def
_reset_signal_handlers
(
self
)
:
        
for
sig
sig_handler
in
iteritems
(
self
.
_dfl_sigmap
)
:
            
signal
.
signal
(
sig
sig_handler
)
    
staticmethod
    
def
_set_color
(
value
)
:
        
available_values
=
[
k
for
k
v
in
iteritems
(
COLOR_MAP
)
if
v
=
=
"
color
"
]
        
if
value
not
in
available_values
:
            
raise
ValueError
(
                
"
'
{
0
}
'
:
unsupported
color
value
.
Use
one
of
the
:
{
1
}
"
.
format
(
                    
value
"
"
.
join
(
available_values
)
                
)
            
)
        
return
value
    
staticmethod
    
def
_set_on_color
(
value
)
:
        
available_values
=
[
            
k
for
k
v
in
iteritems
(
COLOR_MAP
)
if
v
=
=
"
on_color
"
        
]
        
if
value
not
in
available_values
:
            
raise
ValueError
(
                
"
'
{
0
}
'
:
unsupported
on_color
value
.
"
                
"
Use
one
of
the
:
{
1
}
"
.
format
(
                    
value
"
"
.
join
(
available_values
)
                
)
            
)
        
return
value
    
staticmethod
    
def
_set_attrs
(
attrs
)
:
        
available_values
=
[
k
for
k
v
in
iteritems
(
COLOR_MAP
)
if
v
=
=
"
attrs
"
]
        
for
attr
in
attrs
:
            
if
attr
not
in
available_values
:
                
raise
ValueError
(
                    
"
'
{
0
}
'
:
unsupported
attribute
value
.
"
                    
"
Use
one
of
the
:
{
1
}
"
.
format
(
                        
attr
"
"
.
join
(
available_values
)
                    
)
                
)
        
return
set
(
attrs
)
    
staticmethod
    
def
_set_spinner
(
spinner
)
:
        
if
not
spinner
:
            
sp
=
default_spinner
        
if
hasattr
(
spinner
"
frames
"
)
and
hasattr
(
spinner
"
interval
"
)
:
            
if
not
spinner
.
frames
or
not
spinner
.
interval
:
                
sp
=
default_spinner
            
else
:
                
sp
=
spinner
        
else
:
            
sp
=
default_spinner
        
return
sp
    
staticmethod
    
def
_set_side
(
side
)
:
        
if
side
not
in
(
"
left
"
"
right
"
)
:
            
raise
ValueError
(
                
"
'
{
0
}
'
:
unsupported
side
value
.
"
                
"
Use
either
'
left
'
or
'
right
'
.
"
            
)
        
return
side
    
staticmethod
    
def
_set_frames
(
spinner
reversal
)
:
        
uframes
=
None
        
uframes_seq
=
None
        
if
isinstance
(
spinner
.
frames
basestring
)
:
            
uframes
=
to_unicode
(
spinner
.
frames
)
if
PY2
else
spinner
.
frames
        
if
isinstance
(
spinner
.
frames
(
list
tuple
)
)
:
            
if
spinner
.
frames
and
isinstance
(
spinner
.
frames
[
0
]
bytes
)
:
                
uframes_seq
=
[
to_unicode
(
frame
)
for
frame
in
spinner
.
frames
]
            
else
:
                
uframes_seq
=
spinner
.
frames
        
_frames
=
uframes
or
uframes_seq
        
if
not
_frames
:
            
raise
ValueError
(
                
"
{
0
!
r
}
:
no
frames
found
in
spinner
"
.
format
(
spinner
)
            
)
        
frames
=
_frames
[
:
:
-
1
]
if
reversal
else
_frames
        
return
frames
    
staticmethod
    
def
_set_interval
(
spinner
)
:
        
return
spinner
.
interval
*
0
.
001
    
staticmethod
    
def
_set_cycle
(
frames
)
:
        
return
itertools
.
cycle
(
frames
)
    
staticmethod
    
def
_set_text
(
text
)
:
        
if
PY2
:
            
return
to_unicode
(
text
)
        
return
text
    
staticmethod
    
def
_hide_cursor
(
)
:
        
cursor
.
hide_cursor
(
)
    
staticmethod
    
def
_show_cursor
(
)
:
        
cursor
.
show_cursor
(
)
    
staticmethod
    
def
_clear_line
(
)
:
        
sys
.
stdout
.
write
(
chr
(
27
)
+
"
[
K
"
)
