class
SkipTest
(
Exception
)
:
    
"
"
"
    
Raise
this
exception
in
a
test
to
skip
it
.
    
Usually
you
can
use
TestResult
.
skip
(
)
or
one
of
the
skipping
decorators
    
instead
of
raising
this
directly
.
    
"
"
"
    
pass
class
_ExpectedFailure
(
Exception
)
:
    
"
"
"
    
Raise
this
when
a
test
is
expected
to
fail
.
    
This
is
an
implementation
detail
.
    
"
"
"
    
def
__init__
(
self
exc_info
)
:
        
super
(
_ExpectedFailure
self
)
.
__init__
(
)
        
self
.
exc_info
=
exc_info
class
_UnexpectedSuccess
(
Exception
)
:
    
"
"
"
The
test
was
supposed
to
fail
but
it
didn
'
t
.
"
"
"
    
pass
