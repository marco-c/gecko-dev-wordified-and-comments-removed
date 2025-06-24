import
os
from
collections
import
deque
from
sentry_sdk
.
_compat
import
PY311
from
sentry_sdk
.
utils
import
filename_for_module
from
typing
import
TYPE_CHECKING
if
TYPE_CHECKING
:
    
from
sentry_sdk
.
_lru_cache
import
LRUCache
    
from
types
import
FrameType
    
from
typing
import
Deque
    
from
typing
import
List
    
from
typing
import
Optional
    
from
typing
import
Sequence
    
from
typing
import
Tuple
    
from
typing_extensions
import
TypedDict
    
ThreadId
=
str
    
ProcessedStack
=
List
[
int
]
    
ProcessedFrame
=
TypedDict
(
        
"
ProcessedFrame
"
        
{
            
"
abs_path
"
:
str
            
"
filename
"
:
Optional
[
str
]
            
"
function
"
:
str
            
"
lineno
"
:
int
            
"
module
"
:
Optional
[
str
]
        
}
    
)
    
ProcessedThreadMetadata
=
TypedDict
(
        
"
ProcessedThreadMetadata
"
        
{
"
name
"
:
str
}
    
)
    
FrameId
=
Tuple
[
        
str
        
int
        
str
    
]
    
FrameIds
=
Tuple
[
FrameId
.
.
.
]
    
StackId
=
Tuple
[
int
int
]
    
ExtractedStack
=
Tuple
[
StackId
FrameIds
List
[
ProcessedFrame
]
]
    
ExtractedSample
=
Sequence
[
Tuple
[
ThreadId
ExtractedStack
]
]
DEFAULT_SAMPLING_FREQUENCY
=
101
MAX_STACK_DEPTH
=
128
if
PY311
:
    
def
get_frame_name
(
frame
)
:
        
return
frame
.
f_code
.
co_qualname
else
:
    
def
get_frame_name
(
frame
)
:
        
f_code
=
frame
.
f_code
        
co_varnames
=
f_code
.
co_varnames
        
name
=
f_code
.
co_name
        
try
:
            
if
(
                
co_varnames
                
and
co_varnames
[
0
]
=
=
"
self
"
                
and
"
self
"
in
frame
.
f_locals
            
)
:
                
for
cls
in
type
(
frame
.
f_locals
[
"
self
"
]
)
.
__mro__
:
                    
if
name
in
cls
.
__dict__
:
                        
return
"
{
}
.
{
}
"
.
format
(
cls
.
__name__
name
)
        
except
(
AttributeError
ValueError
)
:
            
pass
        
try
:
            
if
(
                
co_varnames
                
and
co_varnames
[
0
]
=
=
"
cls
"
                
and
"
cls
"
in
frame
.
f_locals
            
)
:
                
for
cls
in
frame
.
f_locals
[
"
cls
"
]
.
__mro__
:
                    
if
name
in
cls
.
__dict__
:
                        
return
"
{
}
.
{
}
"
.
format
(
cls
.
__name__
name
)
        
except
(
AttributeError
ValueError
)
:
            
pass
        
return
name
def
frame_id
(
raw_frame
)
:
    
return
(
raw_frame
.
f_code
.
co_filename
raw_frame
.
f_lineno
get_frame_name
(
raw_frame
)
)
def
extract_frame
(
fid
raw_frame
cwd
)
:
    
abs_path
=
raw_frame
.
f_code
.
co_filename
    
try
:
        
module
=
raw_frame
.
f_globals
[
"
__name__
"
]
    
except
Exception
:
        
module
=
None
    
return
{
        
"
abs_path
"
:
os
.
path
.
join
(
cwd
abs_path
)
        
"
module
"
:
module
        
"
filename
"
:
filename_for_module
(
module
abs_path
)
or
None
        
"
function
"
:
fid
[
2
]
        
"
lineno
"
:
raw_frame
.
f_lineno
    
}
def
extract_stack
(
    
raw_frame
    
cache
    
cwd
    
max_stack_depth
=
MAX_STACK_DEPTH
)
:
    
"
"
"
    
Extracts
the
stack
starting
the
specified
frame
.
The
extracted
stack
    
assumes
the
specified
frame
is
the
top
of
the
stack
and
works
back
    
to
the
bottom
of
the
stack
.
    
In
the
event
that
the
stack
is
more
than
MAX_STACK_DEPTH
frames
deep
    
only
the
first
MAX_STACK_DEPTH
frames
will
be
returned
.
    
"
"
"
    
raw_frames
=
deque
(
maxlen
=
max_stack_depth
)
    
while
raw_frame
is
not
None
:
        
f_back
=
raw_frame
.
f_back
        
raw_frames
.
append
(
raw_frame
)
        
raw_frame
=
f_back
    
frame_ids
=
tuple
(
frame_id
(
raw_frame
)
for
raw_frame
in
raw_frames
)
    
frames
=
[
]
    
for
i
fid
in
enumerate
(
frame_ids
)
:
        
frame
=
cache
.
get
(
fid
)
        
if
frame
is
None
:
            
frame
=
extract_frame
(
fid
raw_frames
[
i
]
cwd
)
            
cache
.
set
(
fid
frame
)
        
frames
.
append
(
frame
)
    
stack_id
=
len
(
raw_frames
)
hash
(
frame_ids
)
    
return
stack_id
frame_ids
frames
