import
os
from
mozunit
import
main
def
test_set_isatty_environ
(
monkeypatch
get_mach
)
:
    
monkeypatch
.
delenv
(
"
MACH_STDOUT_ISATTY
"
raising
=
False
)
    
monkeypatch
.
setattr
(
os
"
isatty
"
lambda
fd
:
True
)
    
m
=
get_mach
(
)
    
orig_run
=
m
.
_run
    
env_is_set
=
[
]
    
def
wrap_run
(
*
args
*
*
kwargs
)
:
        
env_is_set
.
append
(
"
MACH_STDOUT_ISATTY
"
in
os
.
environ
)
        
return
orig_run
(
*
args
*
*
kwargs
)
    
monkeypatch
.
setattr
(
m
"
_run
"
wrap_run
)
    
ret
=
m
.
run
(
[
]
)
    
assert
ret
=
=
0
    
assert
env_is_set
[
0
]
if
__name__
=
=
"
__main__
"
:
    
main
(
)
