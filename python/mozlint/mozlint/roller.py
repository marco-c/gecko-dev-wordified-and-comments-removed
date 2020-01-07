from
__future__
import
absolute_import
print_function
unicode_literals
import
os
import
signal
import
sys
import
traceback
from
collections
import
defaultdict
from
concurrent
.
futures
import
ProcessPoolExecutor
from
math
import
ceil
from
multiprocessing
import
cpu_count
from
subprocess
import
CalledProcessError
from
mozversioncontrol
import
get_repository_object
MissingUpstreamRepo
InvalidRepoPath
from
.
errors
import
LintersNotConfigured
from
.
parser
import
Parser
from
.
pathutils
import
findobject
from
.
types
import
supported_types
def
_run_worker
(
config
paths
*
*
lintargs
)
:
    
results
=
defaultdict
(
list
)
    
failed
=
[
]
    
func
=
supported_types
[
config
[
'
type
'
]
]
    
try
:
        
res
=
func
(
paths
config
*
*
lintargs
)
or
[
]
    
except
Exception
:
        
traceback
.
print_exc
(
)
        
res
=
1
    
finally
:
        
sys
.
stdout
.
flush
(
)
    
if
not
isinstance
(
res
(
list
tuple
)
)
:
        
if
res
:
            
failed
.
append
(
config
[
'
name
'
]
)
    
else
:
        
for
r
in
res
:
            
results
[
r
.
path
]
.
append
(
r
)
    
return
results
failed
class
LintRoller
(
object
)
:
    
"
"
"
Registers
and
runs
linters
.
    
:
param
root
:
Path
to
which
relative
paths
will
be
joined
.
If
                 
unspecified
root
will
either
be
determined
from
                 
version
control
or
cwd
.
    
:
param
lintargs
:
Arguments
to
pass
to
the
underlying
linter
(
s
)
.
    
"
"
"
    
MAX_PATHS_PER_JOB
=
50
    
def
__init__
(
self
root
*
*
lintargs
)
:
        
self
.
parse
=
Parser
(
)
        
try
:
            
self
.
vcs
=
get_repository_object
(
root
)
        
except
InvalidRepoPath
:
            
self
.
vcs
=
None
        
self
.
linters
=
[
]
        
self
.
lintargs
=
lintargs
        
self
.
lintargs
[
'
root
'
]
=
root
        
self
.
failed
=
None
        
self
.
failed_setup
=
None
        
self
.
results
=
None
        
self
.
root
=
root
    
def
read
(
self
paths
)
:
        
"
"
"
Parse
one
or
more
linters
and
add
them
to
the
registry
.
        
:
param
paths
:
A
path
or
iterable
of
paths
to
linter
definitions
.
        
"
"
"
        
if
isinstance
(
paths
basestring
)
:
            
paths
=
(
paths
)
        
for
path
in
paths
:
            
self
.
linters
.
extend
(
self
.
parse
(
path
)
)
    
def
setup
(
self
)
:
        
"
"
"
Run
setup
for
applicable
linters
"
"
"
        
if
not
self
.
linters
:
            
raise
LintersNotConfigured
        
self
.
failed_setup
=
set
(
)
        
for
linter
in
self
.
linters
:
            
if
'
setup
'
not
in
linter
:
                
continue
            
try
:
                
res
=
findobject
(
linter
[
'
setup
'
]
)
(
self
.
root
)
            
except
Exception
:
                
traceback
.
print_exc
(
)
                
res
=
1
            
if
res
:
                
self
.
failed_setup
.
add
(
linter
[
'
name
'
]
)
        
if
self
.
failed_setup
:
            
print
(
"
error
:
problem
with
lint
setup
skipping
{
}
"
.
format
(
                    
'
'
.
join
(
sorted
(
self
.
failed_setup
)
)
)
)
            
self
.
linters
=
[
l
for
l
in
self
.
linters
if
l
[
'
name
'
]
not
in
self
.
failed_setup
]
            
return
1
        
return
0
    
def
_generate_jobs
(
self
paths
num_procs
)
:
        
"
"
"
A
job
is
of
the
form
(
<
linter
:
dict
>
<
paths
:
list
>
)
.
"
"
"
        
chunk_size
=
min
(
self
.
MAX_PATHS_PER_JOB
int
(
ceil
(
float
(
len
(
paths
)
)
/
num_procs
)
)
)
        
while
paths
:
            
for
linter
in
self
.
linters
:
                
yield
linter
paths
[
:
chunk_size
]
            
paths
=
paths
[
chunk_size
:
]
    
def
_collect_results
(
self
future
)
:
        
if
future
.
cancelled
(
)
:
            
return
        
results
failed
=
future
.
result
(
)
        
if
failed
:
            
self
.
failed
.
update
(
set
(
failed
)
)
        
for
k
v
in
results
.
iteritems
(
)
:
            
self
.
results
[
k
]
.
extend
(
v
)
    
def
roll
(
self
paths
=
None
outgoing
=
None
workdir
=
None
num_procs
=
None
)
:
        
"
"
"
Run
all
of
the
registered
linters
against
the
specified
file
paths
.
        
:
param
paths
:
An
iterable
of
files
and
/
or
directories
to
lint
.
        
:
param
outgoing
:
Lint
files
touched
by
commits
that
are
not
on
the
remote
repository
.
        
:
param
workdir
:
Lint
all
files
touched
in
the
working
directory
.
        
:
param
num_procs
:
The
number
of
processes
to
use
.
Default
:
cpu
count
        
:
return
:
A
dictionary
with
file
names
as
the
key
and
a
list
of
                 
:
class
:
~
result
.
ResultContainer
s
as
the
value
.
        
"
"
"
        
if
not
self
.
linters
:
            
raise
LintersNotConfigured
        
self
.
results
=
defaultdict
(
list
)
        
self
.
failed
=
set
(
)
        
paths
=
paths
or
set
(
)
        
if
isinstance
(
paths
basestring
)
:
            
paths
=
set
(
[
paths
]
)
        
elif
isinstance
(
paths
(
list
tuple
)
)
:
            
paths
=
set
(
paths
)
        
if
not
self
.
vcs
and
(
workdir
or
outgoing
)
:
            
print
(
"
error
:
'
{
}
'
is
not
a
known
repository
can
'
t
use
"
                  
"
-
-
workdir
or
-
-
outgoing
"
.
format
(
self
.
lintargs
[
'
root
'
]
)
)
        
try
:
            
if
workdir
:
                
paths
.
update
(
self
.
vcs
.
get_changed_files
(
'
AM
'
mode
=
workdir
)
)
            
if
outgoing
:
                
try
:
                    
paths
.
update
(
self
.
vcs
.
get_outgoing_files
(
'
AM
'
upstream
=
outgoing
)
)
                
except
MissingUpstreamRepo
:
                    
print
(
"
warning
:
could
not
find
default
push
specify
a
remote
for
-
-
outgoing
"
)
        
except
CalledProcessError
as
e
:
            
print
(
"
error
running
:
{
}
"
.
format
(
'
'
.
join
(
e
.
cmd
)
)
)
            
if
e
.
output
:
                
print
(
e
.
output
)
        
if
not
paths
and
(
workdir
or
outgoing
)
:
            
print
(
"
warning
:
no
files
linted
"
)
            
return
{
}
        
paths
=
paths
or
[
'
.
'
]
        
paths
=
map
(
os
.
path
.
abspath
paths
)
        
num_procs
=
num_procs
or
cpu_count
(
)
        
jobs
=
list
(
self
.
_generate_jobs
(
paths
num_procs
)
)
        
num_procs
=
min
(
len
(
jobs
)
num_procs
)
        
executor
=
ProcessPoolExecutor
(
num_procs
)
        
for
job
in
jobs
:
            
future
=
executor
.
submit
(
_run_worker
*
job
*
*
self
.
lintargs
)
            
future
.
add_done_callback
(
self
.
_collect_results
)
        
orig_sigint
=
signal
.
signal
(
signal
.
SIGINT
signal
.
SIG_IGN
)
        
executor
.
shutdown
(
)
        
signal
.
signal
(
signal
.
SIGINT
orig_sigint
)
        
return
self
.
results
