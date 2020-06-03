"
"
"
Monkey
-
patching
to
add
multiprocessing
support
for
coverage
.
py
"
"
"
import
multiprocessing
import
multiprocessing
.
process
import
os
import
os
.
path
import
sys
import
traceback
from
coverage
import
env
from
coverage
.
misc
import
contract
PATCHED_MARKER
=
"
_coverage
patched
"
if
env
.
PYVERSION
>
=
(
3
4
)
:
    
OriginalProcess
=
multiprocessing
.
process
.
BaseProcess
else
:
    
OriginalProcess
=
multiprocessing
.
Process
original_bootstrap
=
OriginalProcess
.
_bootstrap
class
ProcessWithCoverage
(
OriginalProcess
)
:
    
"
"
"
A
replacement
for
multiprocess
.
Process
that
starts
coverage
.
"
"
"
    
def
_bootstrap
(
self
*
args
*
*
kwargs
)
:
        
"
"
"
Wrapper
around
_bootstrap
to
start
coverage
.
"
"
"
        
try
:
            
from
coverage
import
Coverage
            
cov
=
Coverage
(
data_suffix
=
True
)
            
cov
.
_warn_preimported_source
=
False
            
cov
.
start
(
)
            
debug
=
cov
.
_debug
            
if
debug
.
should
(
"
multiproc
"
)
:
                
debug
.
write
(
"
Calling
multiprocessing
bootstrap
"
)
        
except
Exception
:
            
print
(
"
Exception
during
multiprocessing
bootstrap
init
:
"
)
            
traceback
.
print_exc
(
file
=
sys
.
stdout
)
            
sys
.
stdout
.
flush
(
)
            
raise
        
try
:
            
return
original_bootstrap
(
self
*
args
*
*
kwargs
)
        
finally
:
            
if
debug
.
should
(
"
multiproc
"
)
:
                
debug
.
write
(
"
Finished
multiprocessing
bootstrap
"
)
            
cov
.
stop
(
)
            
cov
.
save
(
)
            
if
debug
.
should
(
"
multiproc
"
)
:
                
debug
.
write
(
"
Saved
multiprocessing
data
"
)
class
Stowaway
(
object
)
:
    
"
"
"
An
object
to
pickle
so
when
it
is
unpickled
it
can
apply
the
monkey
-
patch
.
"
"
"
    
def
__init__
(
self
rcfile
)
:
        
self
.
rcfile
=
rcfile
    
def
__getstate__
(
self
)
:
        
return
{
'
rcfile
'
:
self
.
rcfile
}
    
def
__setstate__
(
self
state
)
:
        
patch_multiprocessing
(
state
[
'
rcfile
'
]
)
contract
(
rcfile
=
str
)
def
patch_multiprocessing
(
rcfile
)
:
    
"
"
"
Monkey
-
patch
the
multiprocessing
module
.
    
This
enables
coverage
measurement
of
processes
started
by
multiprocessing
.
    
This
involves
aggressive
monkey
-
patching
.
    
rcfile
is
the
path
to
the
rcfile
being
used
.
    
"
"
"
    
if
hasattr
(
multiprocessing
PATCHED_MARKER
)
:
        
return
    
if
env
.
PYVERSION
>
=
(
3
4
)
:
        
OriginalProcess
.
_bootstrap
=
ProcessWithCoverage
.
_bootstrap
    
else
:
        
multiprocessing
.
Process
=
ProcessWithCoverage
    
os
.
environ
[
"
COVERAGE_RCFILE
"
]
=
os
.
path
.
abspath
(
rcfile
)
    
try
:
        
from
multiprocessing
import
spawn
        
original_get_preparation_data
=
spawn
.
get_preparation_data
    
except
(
ImportError
AttributeError
)
:
        
pass
    
else
:
        
def
get_preparation_data_with_stowaway
(
name
)
:
            
"
"
"
Get
the
original
preparation
data
and
also
insert
our
stowaway
.
"
"
"
            
d
=
original_get_preparation_data
(
name
)
            
d
[
'
stowaway
'
]
=
Stowaway
(
rcfile
)
            
return
d
        
spawn
.
get_preparation_data
=
get_preparation_data_with_stowaway
    
setattr
(
multiprocessing
PATCHED_MARKER
True
)
