import
sys
from
.
errors
import
AutocommandError
class
AutomainRequiresModuleError
(
AutocommandError
TypeError
)
:
    
pass
def
automain
(
module
*
args
=
(
)
kwargs
=
None
)
:
    
'
'
'
    
This
decorator
automatically
invokes
a
function
if
the
module
is
being
run
    
as
the
"
__main__
"
module
.
Optionally
provide
args
or
kwargs
with
which
to
    
call
the
function
.
If
module
is
"
__main__
"
the
function
is
called
and
    
the
program
is
sys
.
exit
ed
with
the
return
value
.
You
can
also
pass
True
    
to
cause
the
function
to
be
called
unconditionally
.
If
the
function
is
not
    
called
it
is
returned
unchanged
by
the
decorator
.
    
Usage
:
    
automain
(
__name__
)
#
Pass
__name__
to
check
__name__
=
=
"
__main__
"
    
def
main
(
)
:
        
.
.
.
    
If
__name__
is
"
__main__
"
here
the
main
function
is
called
and
then
    
sys
.
exit
called
with
the
return
value
.
    
'
'
'
    
if
callable
(
module
)
:
        
raise
AutomainRequiresModuleError
(
module
)
    
if
module
=
=
'
__main__
'
or
module
is
True
:
        
if
kwargs
is
None
:
            
kwargs
=
{
}
        
def
automain_decorator
(
main
)
:
            
sys
.
exit
(
main
(
*
args
*
*
kwargs
)
)
        
return
automain_decorator
    
else
:
        
return
lambda
main
:
main
