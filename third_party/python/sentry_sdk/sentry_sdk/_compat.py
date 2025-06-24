import
sys
from
typing
import
TYPE_CHECKING
if
TYPE_CHECKING
:
    
from
typing
import
Any
    
from
typing
import
TypeVar
    
T
=
TypeVar
(
"
T
"
)
PY37
=
sys
.
version_info
[
0
]
=
=
3
and
sys
.
version_info
[
1
]
>
=
7
PY38
=
sys
.
version_info
[
0
]
=
=
3
and
sys
.
version_info
[
1
]
>
=
8
PY310
=
sys
.
version_info
[
0
]
=
=
3
and
sys
.
version_info
[
1
]
>
=
10
PY311
=
sys
.
version_info
[
0
]
=
=
3
and
sys
.
version_info
[
1
]
>
=
11
def
with_metaclass
(
meta
*
bases
)
:
    
class
MetaClass
(
type
)
:
        
def
__new__
(
metacls
name
this_bases
d
)
:
            
return
meta
(
name
bases
d
)
    
return
type
.
__new__
(
MetaClass
"
temporary_class
"
(
)
{
}
)
def
check_uwsgi_thread_support
(
)
:
    
try
:
        
from
uwsgi
import
opt
    
except
ImportError
:
        
return
True
    
from
sentry_sdk
.
consts
import
FALSE_VALUES
    
def
enabled
(
option
)
:
        
value
=
opt
.
get
(
option
False
)
        
if
isinstance
(
value
bool
)
:
            
return
value
        
if
isinstance
(
value
bytes
)
:
            
try
:
                
value
=
value
.
decode
(
)
            
except
Exception
:
                
pass
        
return
value
and
str
(
value
)
.
lower
(
)
not
in
FALSE_VALUES
    
threads_enabled
=
"
threads
"
in
opt
or
enabled
(
"
enable
-
threads
"
)
    
fork_hooks_on
=
enabled
(
"
py
-
call
-
uwsgi
-
fork
-
hooks
"
)
    
lazy_mode
=
enabled
(
"
lazy
-
apps
"
)
or
enabled
(
"
lazy
"
)
    
if
lazy_mode
and
not
threads_enabled
:
        
from
warnings
import
warn
        
warn
(
            
Warning
(
                
"
IMPORTANT
:
"
                
"
We
detected
the
use
of
uWSGI
without
thread
support
.
"
                
"
This
might
lead
to
unexpected
issues
.
"
                
'
Please
run
uWSGI
with
"
-
-
enable
-
threads
"
for
full
support
.
'
            
)
        
)
        
return
False
    
elif
not
lazy_mode
and
(
not
threads_enabled
or
not
fork_hooks_on
)
:
        
from
warnings
import
warn
        
warn
(
            
Warning
(
                
"
IMPORTANT
:
"
                
"
We
detected
the
use
of
uWSGI
in
preforking
mode
without
"
                
"
thread
support
.
This
might
lead
to
crashing
workers
.
"
                
'
Please
run
uWSGI
with
both
"
-
-
enable
-
threads
"
and
'
                
'
"
-
-
py
-
call
-
uwsgi
-
fork
-
hooks
"
for
full
support
.
'
            
)
        
)
        
return
False
    
return
True
