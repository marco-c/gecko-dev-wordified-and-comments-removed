import
logging
class
MachEnvironment
:
    
def
__init__
(
self
mach_command
)
:
        
self
.
return_code
=
0
        
self
.
mach_cmd
=
mach_command
        
self
.
log
=
mach_command
.
log
        
self
.
run_process
=
mach_command
.
run_process
    
def
info
(
self
msg
name
=
"
mozperftest
"
*
*
kwargs
)
:
        
self
.
log
(
logging
.
INFO
name
kwargs
msg
)
    
def
debug
(
self
msg
name
=
"
mozperftest
"
*
*
kwargs
)
:
        
self
.
log
(
logging
.
DEBUG
name
kwargs
msg
)
    
def
warning
(
self
msg
name
=
"
mozperftest
"
*
*
kwargs
)
:
        
self
.
log
(
logging
.
WARNING
name
kwargs
msg
)
    
def
__enter__
(
self
)
:
        
self
.
setup
(
)
        
return
self
    
def
__exit__
(
self
type
value
traceback
)
:
        
self
.
teardown
(
)
    
def
__call__
(
self
metadata
)
:
        
pass
    
def
setup
(
self
)
:
        
pass
    
def
teardown
(
self
)
:
        
pass
class
MultipleMachEnvironment
(
MachEnvironment
)
:
    
def
__init__
(
self
mach_command
factories
)
:
        
super
(
MultipleMachEnvironment
self
)
.
__init__
(
mach_command
)
        
self
.
envs
=
[
factory
(
mach_command
)
for
factory
in
factories
]
    
def
__enter__
(
self
)
:
        
for
env
in
self
.
envs
:
            
env
.
setup
(
)
        
return
self
    
def
__exit__
(
self
type
value
traceback
)
:
        
for
env
in
self
.
envs
:
            
env
.
teardown
(
)
    
def
__call__
(
self
metadata
)
:
        
for
env
in
self
.
envs
:
            
metadata
=
env
(
metadata
)
        
return
metadata
    
def
_call_env
(
self
name
)
:
        
def
_call
(
*
args
*
*
kw
)
:
            
return
[
getattr
(
env
name
)
(
*
args
*
*
kw
)
for
env
in
self
.
envs
]
        
return
_call
    
def
__getattr__
(
self
name
)
:
        
return
self
.
_call_env
(
name
)
