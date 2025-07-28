import
signal
import
sys
class
ExitOnSigTerm
(
)
:
  
"
"
"
A
context
manager
that
calls
sys
.
exit
(
0
)
upon
receipt
of
SIGTERM
.
This
  
results
in
a
SystemExit
exception
being
raised
which
causes
any
finally
  
clauses
to
be
run
and
other
contexts
to
be
cleaned
up
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
_previous_handler
=
None
  
def
__enter__
(
self
)
:
    
self
.
_previous_handler
=
signal
.
signal
(
        
signal
.
SIGTERM
lambda
sig_num
frame
:
sys
.
exit
(
0
)
)
    
return
self
  
def
__exit__
(
self
exc_type
exc_val
exc_tb
)
:
    
signal
.
signal
(
signal
.
SIGTERM
self
.
_previous_handler
)
    
return
False
