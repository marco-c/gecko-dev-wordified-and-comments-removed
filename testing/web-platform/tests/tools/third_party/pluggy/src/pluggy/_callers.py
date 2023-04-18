"
"
"
Call
loop
machinery
"
"
"
import
sys
from
.
_result
import
HookCallError
_Result
_raise_wrapfail
def
_multicall
(
hook_name
hook_impls
caller_kwargs
firstresult
)
:
    
"
"
"
Execute
a
call
into
multiple
python
functions
/
methods
and
return
the
    
result
(
s
)
.
    
caller_kwargs
comes
from
_HookCaller
.
__call__
(
)
.
    
"
"
"
    
__tracebackhide__
=
True
    
results
=
[
]
    
excinfo
=
None
    
try
:
        
teardowns
=
[
]
        
try
:
            
for
hook_impl
in
reversed
(
hook_impls
)
:
                
try
:
                    
args
=
[
caller_kwargs
[
argname
]
for
argname
in
hook_impl
.
argnames
]
                
except
KeyError
:
                    
for
argname
in
hook_impl
.
argnames
:
                        
if
argname
not
in
caller_kwargs
:
                            
raise
HookCallError
(
                                
f
"
hook
call
must
provide
argument
{
argname
!
r
}
"
                            
)
                
if
hook_impl
.
hookwrapper
:
                    
try
:
                        
gen
=
hook_impl
.
function
(
*
args
)
                        
next
(
gen
)
                        
teardowns
.
append
(
gen
)
                    
except
StopIteration
:
                        
_raise_wrapfail
(
gen
"
did
not
yield
"
)
                
else
:
                    
res
=
hook_impl
.
function
(
*
args
)
                    
if
res
is
not
None
:
                        
results
.
append
(
res
)
                        
if
firstresult
:
                            
break
        
except
BaseException
:
            
excinfo
=
sys
.
exc_info
(
)
    
finally
:
        
if
firstresult
:
            
outcome
=
_Result
(
results
[
0
]
if
results
else
None
excinfo
)
        
else
:
            
outcome
=
_Result
(
results
excinfo
)
        
for
gen
in
reversed
(
teardowns
)
:
            
try
:
                
gen
.
send
(
outcome
)
                
_raise_wrapfail
(
gen
"
has
second
yield
"
)
            
except
StopIteration
:
                
pass
        
return
outcome
.
get_result
(
)
