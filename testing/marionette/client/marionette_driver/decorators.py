from
functools
import
wraps
import
socket
import
sys
import
traceback
def
_find_marionette_in_args
(
*
args
*
*
kwargs
)
:
    
try
:
        
m
=
[
a
for
a
in
args
+
tuple
(
kwargs
.
values
(
)
)
if
hasattr
(
a
'
session
'
)
]
[
0
]
    
except
IndexError
:
        
print
(
"
Can
only
apply
decorator
to
function
using
a
marionette
object
"
)
        
raise
    
return
m
def
do_process_check
(
func
)
:
    
"
"
"
Decorator
which
checks
the
process
status
after
the
function
has
run
.
"
"
"
    
wraps
(
func
)
    
def
_
(
*
args
*
*
kwargs
)
:
        
m
=
_find_marionette_in_args
(
*
args
*
*
kwargs
)
        
try
:
            
return
func
(
*
args
*
*
kwargs
)
        
except
IOError
as
e
:
            
exc
val
tb
=
sys
.
exc_info
(
)
            
crashed
=
False
            
try
:
                
crashed
=
m
.
check_for_crash
(
)
            
except
Exception
:
                
traceback
.
print_exc
(
)
            
if
type
(
e
)
in
(
socket
.
error
socket
.
timeout
)
or
crashed
:
                
m
.
handle_socket_failure
(
crashed
)
            
raise
exc
val
tb
    
return
_
def
uses_marionette
(
func
)
:
    
"
"
"
Decorator
which
creates
a
marionette
session
and
deletes
it
    
afterwards
if
one
doesn
'
t
already
exist
.
    
"
"
"
    
wraps
(
func
)
    
def
_
(
*
args
*
*
kwargs
)
:
        
m
=
_find_marionette_in_args
(
*
args
*
*
kwargs
)
        
delete_session
=
False
        
if
not
m
.
session
:
            
delete_session
=
True
            
m
.
start_session
(
)
        
m
.
set_context
(
m
.
CONTEXT_CHROME
)
        
ret
=
func
(
*
args
*
*
kwargs
)
        
if
delete_session
:
            
m
.
delete_session
(
)
        
return
ret
    
return
_
def
using_context
(
context
)
:
    
"
"
"
Decorator
which
allows
a
function
to
execute
in
certain
scope
    
using
marionette
.
using_context
functionality
and
returns
to
old
    
scope
once
the
function
exits
.
    
:
param
context
:
Either
'
chrome
'
or
'
content
'
.
    
"
"
"
    
def
wrap
(
func
)
:
        
wraps
(
func
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
            
m
=
_find_marionette_in_args
(
*
args
*
*
kwargs
)
            
with
m
.
using_context
(
context
)
:
                
return
func
(
*
args
*
*
kwargs
)
        
return
inner
    
return
wrap
