import
itertools
import
sys
from
signal
import
SIGINT
default_int_handler
signal
from
typing
import
Any
from
pip
.
_vendor
.
progress
.
bar
import
Bar
FillingCirclesBar
IncrementalBar
from
pip
.
_vendor
.
progress
.
spinner
import
Spinner
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
from
pip
.
_internal
.
utils
.
misc
import
format_size
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
def
_select_progress_class
(
preferred
:
Bar
fallback
:
Bar
)
-
>
Bar
:
    
encoding
=
getattr
(
preferred
.
file
"
encoding
"
None
)
    
if
not
encoding
:
        
return
fallback
    
characters
=
[
        
getattr
(
preferred
"
empty_fill
"
"
"
)
        
getattr
(
preferred
"
fill
"
"
"
)
    
]
    
characters
+
=
list
(
getattr
(
preferred
"
phases
"
[
]
)
)
    
try
:
        
"
"
.
join
(
characters
)
.
encode
(
encoding
)
    
except
UnicodeEncodeError
:
        
return
fallback
    
else
:
        
return
preferred
_BaseBar
:
Any
=
_select_progress_class
(
IncrementalBar
Bar
)
class
InterruptibleMixin
:
    
"
"
"
    
Helper
to
ensure
that
self
.
finish
(
)
gets
called
on
keyboard
interrupt
.
    
This
allows
downloads
to
be
interrupted
without
leaving
temporary
state
    
(
like
hidden
cursors
)
behind
.
    
This
class
is
similar
to
the
progress
library
'
s
existing
SigIntMixin
    
helper
but
as
of
version
1
.
2
that
helper
has
the
following
problems
:
    
1
.
It
calls
sys
.
exit
(
)
.
    
2
.
It
discards
the
existing
SIGINT
handler
completely
.
    
3
.
It
leaves
its
own
handler
in
place
even
after
an
uninterrupted
finish
       
which
will
have
unexpected
delayed
effects
if
the
user
triggers
an
       
unrelated
keyboard
interrupt
some
time
after
a
progress
-
displaying
       
download
has
already
completed
for
example
.
    
"
"
"
    
def
__init__
(
self
*
args
:
Any
*
*
kwargs
:
Any
)
-
>
None
:
        
"
"
"
        
Save
the
original
SIGINT
handler
for
later
.
        
"
"
"
        
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
        
self
.
original_handler
=
signal
(
SIGINT
self
.
handle_sigint
)
        
if
self
.
original_handler
is
None
:
            
self
.
original_handler
=
default_int_handler
    
def
finish
(
self
)
-
>
None
:
        
"
"
"
        
Restore
the
original
SIGINT
handler
after
finishing
.
        
This
should
happen
regardless
of
whether
the
progress
display
finishes
        
normally
or
gets
interrupted
.
        
"
"
"
        
super
(
)
.
finish
(
)
        
signal
(
SIGINT
self
.
original_handler
)
    
def
handle_sigint
(
self
signum
frame
)
:
        
"
"
"
        
Call
self
.
finish
(
)
before
delegating
to
the
original
SIGINT
handler
.
        
This
handler
should
only
be
in
place
while
the
progress
display
is
        
active
.
        
"
"
"
        
self
.
finish
(
)
        
self
.
original_handler
(
signum
frame
)
class
SilentBar
(
Bar
)
:
    
def
update
(
self
)
-
>
None
:
        
pass
class
BlueEmojiBar
(
IncrementalBar
)
:
    
suffix
=
"
%
(
percent
)
d
%
%
"
    
bar_prefix
=
"
"
    
bar_suffix
=
"
"
    
phases
=
(
"
\
U0001F539
"
"
\
U0001F537
"
"
\
U0001F535
"
)
class
DownloadProgressMixin
:
    
def
__init__
(
self
*
args
:
Any
*
*
kwargs
:
Any
)
-
>
None
:
        
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
        
self
.
message
:
str
=
(
"
"
*
(
get_indentation
(
)
+
2
)
)
+
self
.
message
    
property
    
def
downloaded
(
self
)
-
>
str
:
        
return
format_size
(
self
.
index
)
    
property
    
def
download_speed
(
self
)
-
>
str
:
        
if
self
.
avg
=
=
0
.
0
:
            
return
"
.
.
.
"
        
return
format_size
(
1
/
self
.
avg
)
+
"
/
s
"
    
property
    
def
pretty_eta
(
self
)
-
>
str
:
        
if
self
.
eta
:
            
return
f
"
eta
{
self
.
eta_td
}
"
        
return
"
"
    
def
iter
(
self
it
)
:
        
for
x
in
it
:
            
yield
x
            
self
.
next
(
len
(
x
)
)
        
self
.
finish
(
)
class
WindowsMixin
:
    
def
__init__
(
self
*
args
:
Any
*
*
kwargs
:
Any
)
-
>
None
:
        
if
WINDOWS
and
self
.
hide_cursor
:
            
self
.
hide_cursor
=
False
        
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
        
if
WINDOWS
and
colorama
:
            
self
.
file
=
colorama
.
AnsiToWin32
(
self
.
file
)
            
self
.
file
.
isatty
=
lambda
:
self
.
file
.
wrapped
.
isatty
(
)
            
self
.
file
.
flush
=
lambda
:
self
.
file
.
wrapped
.
flush
(
)
class
BaseDownloadProgressBar
(
WindowsMixin
InterruptibleMixin
DownloadProgressMixin
)
:
    
file
=
sys
.
stdout
    
message
=
"
%
(
percent
)
d
%
%
"
    
suffix
=
"
%
(
downloaded
)
s
%
(
download_speed
)
s
%
(
pretty_eta
)
s
"
class
DefaultDownloadProgressBar
(
BaseDownloadProgressBar
_BaseBar
)
:
    
pass
class
DownloadSilentBar
(
BaseDownloadProgressBar
SilentBar
)
:
    
pass
class
DownloadBar
(
BaseDownloadProgressBar
Bar
)
:
    
pass
class
DownloadFillingCirclesBar
(
BaseDownloadProgressBar
FillingCirclesBar
)
:
    
pass
class
DownloadBlueEmojiProgressBar
(
BaseDownloadProgressBar
BlueEmojiBar
)
:
    
pass
class
DownloadProgressSpinner
(
    
WindowsMixin
InterruptibleMixin
DownloadProgressMixin
Spinner
)
:
    
file
=
sys
.
stdout
    
suffix
=
"
%
(
downloaded
)
s
%
(
download_speed
)
s
"
    
def
next_phase
(
self
)
-
>
str
:
        
if
not
hasattr
(
self
"
_phaser
"
)
:
            
self
.
_phaser
=
itertools
.
cycle
(
self
.
phases
)
        
return
next
(
self
.
_phaser
)
    
def
update
(
self
)
-
>
None
:
        
message
=
self
.
message
%
self
        
phase
=
self
.
next_phase
(
)
        
suffix
=
self
.
suffix
%
self
        
line
=
"
"
.
join
(
            
[
                
message
                
"
"
if
message
else
"
"
                
phase
                
"
"
if
suffix
else
"
"
                
suffix
            
]
        
)
        
self
.
writeln
(
line
)
BAR_TYPES
=
{
    
"
off
"
:
(
DownloadSilentBar
DownloadSilentBar
)
    
"
on
"
:
(
DefaultDownloadProgressBar
DownloadProgressSpinner
)
    
"
ascii
"
:
(
DownloadBar
DownloadProgressSpinner
)
    
"
pretty
"
:
(
DownloadFillingCirclesBar
DownloadProgressSpinner
)
    
"
emoji
"
:
(
DownloadBlueEmojiProgressBar
DownloadProgressSpinner
)
}
def
DownloadProgressProvider
(
progress_bar
max
=
None
)
:
    
if
max
is
None
or
max
=
=
0
:
        
return
BAR_TYPES
[
progress_bar
]
[
1
]
(
)
.
iter
    
else
:
        
return
BAR_TYPES
[
progress_bar
]
[
0
]
(
max
=
max
)
.
iter
