from
__future__
import
annotations
import
atexit
import
copy
import
logging
import
os
import
re
import
signal
import
sys
import
time
from
concurrent
.
futures
import
ProcessPoolExecutor
from
concurrent
.
futures
import
wait
as
futures_wait
from
concurrent
.
futures
.
process
import
_python_exit
as
futures_atexit
from
itertools
import
chain
from
math
import
ceil
from
multiprocessing
import
get_context
from
multiprocessing
.
queues
import
Queue
from
subprocess
import
CalledProcessError
import
mozpack
.
path
as
mozpath
from
mozbuild
.
util
import
cpu_count
from
mozversioncontrol
import
(
    
InvalidRepoPath
    
MissingUpstreamRepo
    
get_repository_object
)
from
.
errors
import
LintersNotConfigured
NoValidLinter
from
.
parser
import
Parser
from
.
pathutils
import
filterpaths
findobject
from
.
result
import
ResultSummary
from
.
types
import
supported_types
SHUTDOWN
=
False
orig_sigint
=
signal
.
getsignal
(
signal
.
SIGINT
)
logger
=
logging
.
getLogger
(
"
lint
"
)
handler
=
logging
.
StreamHandler
(
)
formatter
=
logging
.
Formatter
(
"
%
(
levelname
)
s
:
%
(
message
)
s
"
)
handler
.
setFormatter
(
formatter
)
logger
.
addHandler
(
handler
)
log
=
logging
.
LoggerAdapter
(
logger
{
"
lintname
"
:
"
mozlint
"
"
pid
"
:
os
.
getpid
(
)
}
)
def
_setup_logger
(
log
show_verbose
)
:
    
if
show_verbose
:
        
formatter
=
logging
.
Formatter
(
            
"
%
(
asctime
)
s
.
%
(
msecs
)
03d
%
(
lintname
)
s
(
%
(
pid
)
s
)
|
%
(
message
)
s
"
"
%
H
:
%
M
:
%
S
"
        
)
        
logger
.
handlers
[
0
]
.
setFormatter
(
formatter
)
        
log
.
setLevel
(
logging
.
DEBUG
)
    
else
:
        
log
.
setLevel
(
logging
.
WARNING
)
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
    
log
=
logging
.
LoggerAdapter
(
        
logger
{
"
lintname
"
:
config
.
get
(
"
name
"
)
"
pid
"
:
os
.
getpid
(
)
}
    
)
    
_setup_logger
(
log
lintargs
.
get
(
"
show_verbose
"
)
)
    
lintargs
[
"
log
"
]
=
log
    
result
=
ResultSummary
(
lintargs
[
"
root
"
]
)
    
if
SHUTDOWN
:
        
return
result
    
if
os
.
environ
.
get
(
"
CODE_REVIEW
"
)
=
=
"
1
"
and
config
.
get
(
        
"
code_review_warnings
"
True
    
)
:
        
lintargs
[
"
show_warnings
"
]
=
True
    
func
=
supported_types
[
config
[
"
type
"
]
]
    
start_time
=
time
.
monotonic
(
)
    
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
        
if
isinstance
(
res
dict
)
:
            
result
.
fixed
+
=
res
[
"
fixed
"
]
            
res
=
res
[
"
results
"
]
or
[
]
        
elif
isinstance
(
res
list
)
:
            
res
=
res
or
[
]
        
else
:
            
log
.
error
(
f
"
Unexpected
result
type
received
:
{
type
(
res
)
}
"
)
            
assert
False
    
except
Exception
:
        
log
.
exception
(
f
"
{
config
[
'
name
'
]
}
failed
"
)
        
res
=
1
    
except
(
KeyboardInterrupt
SystemExit
)
:
        
return
result
    
finally
:
        
end_time
=
time
.
monotonic
(
)
        
log
.
debug
(
f
"
Finished
in
{
end_time
-
start_time
:
.
2f
}
seconds
"
)
        
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
            
result
.
failed_run
.
add
(
config
[
"
name
"
]
)
    
else
:
        
for
r
in
res
:
            
if
not
lintargs
.
get
(
"
show_warnings
"
)
and
r
.
level
=
=
"
warning
"
:
                
result
.
suppressed_warnings
[
r
.
path
]
+
=
1
                
continue
            
result
.
issues
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
result
def
_split_dirs
(
paths
find_dotfiles
depth
)
:
    
split
=
[
]
    
for
path
in
sorted
(
paths
)
:
        
if
os
.
path
.
basename
(
path
)
.
startswith
(
"
.
"
)
or
not
os
.
path
.
isdir
(
path
)
:
            
split
.
append
(
path
)
            
continue
        
for
name
in
sorted
(
os
.
listdir
(
path
)
)
:
            
if
name
.
startswith
(
"
.
"
)
and
not
find_dotfiles
:
                
continue
            
split
.
append
(
os
.
path
.
join
(
path
name
)
)
    
if
depth
>
1
:
        
return
_split_dirs
(
split
find_dotfiles
depth
-
1
)
    
return
split
ENTRY_WEIGHT
=
0
.
2
def
_read_ignore_patterns
(
path
)
:
    
"
"
"
The
patterns
of
an
ignore
list
as
mozpath
patterns
.
A
.
txt
list
    
holds
one
path
per
line
and
any
other
list
is
a
JavaScript
list
of
quoted
    
glob
patterns
.
    
Negated
patterns
are
skipped
so
the
result
can
only
ignore
more
than
the
    
list
does
.
    
"
"
"
    
with
open
(
path
encoding
=
"
utf
-
8
"
)
as
fh
:
        
if
path
.
endswith
(
"
.
txt
"
)
:
            
return
[
p
for
line
in
fh
if
(
p
:
=
line
.
strip
(
)
.
strip
(
"
/
"
)
)
]
        
patterns
=
[
]
        
for
line
in
fh
:
            
if
not
(
m
:
=
re
.
match
(
r
'
\
s
*
"
(
[
^
"
!
]
[
^
"
]
*
)
"
?
\
s
*
(
/
/
.
*
)
?
'
line
)
)
:
                
continue
            
pattern
=
m
.
group
(
1
)
.
strip
(
"
/
"
)
            
patterns
.
append
(
pattern
if
"
/
"
in
pattern
else
f
"
*
*
/
{
pattern
}
"
)
    
return
patterns
def
_weigh
(
path
is_dir
root
checks
excluded
ignored
find_dotfiles
)
:
    
"
"
"
Return
a
[
path
weight
children
]
tree
for
path
or
None
if
    
it
is
excluded
.
A
file
checks
accepts
weighs
1
and
every
entry
    
also
weighs
ENTRY_WEIGHT
for
the
time
spent
walking
it
.
An
ignored
path
    
weighs
nothing
.
    
"
"
"
    
rel
=
mozpath
.
normsep
(
path
[
len
(
root
)
:
]
.
lstrip
(
os
.
sep
+
"
/
"
)
)
    
if
excluded
(
rel
)
:
        
return
None
    
if
ignored
(
rel
)
:
        
return
[
path
0
None
]
    
if
not
is_dir
:
        
return
[
path
int
(
checks
(
path
)
)
+
ENTRY_WEIGHT
None
]
    
children
=
[
]
    
try
:
        
with
os
.
scandir
(
path
)
as
it
:
            
entries
=
sorted
(
it
key
=
lambda
e
:
e
.
name
)
    
except
OSError
:
        
return
[
path
ENTRY_WEIGHT
None
]
    
for
entry
in
entries
:
        
if
entry
.
name
.
startswith
(
"
.
"
)
and
not
find_dotfiles
:
            
continue
        
if
child
:
=
_weigh
(
            
entry
.
path
            
entry
.
is_dir
(
follow_symlinks
=
False
)
            
root
            
checks
            
excluded
            
ignored
            
find_dotfiles
        
)
:
            
children
.
append
(
child
)
    
return
[
path
sum
(
(
c
[
1
]
for
c
in
children
)
start
=
ENTRY_WEIGHT
)
children
]
def
_balanced_jobs
(
    
paths
num_jobs
root
checks
excluded
ignored
find_dotfiles
max_chars
)
:
    
"
"
"
Divide
paths
into
about
num_jobs
lists
of
equal
weight
.
    
A
directory
heavier
than
an
equal
share
is
replaced
by
its
entries
so
no
    
single
path
holds
up
a
job
.
Paths
are
then
handed
out
heaviest
first
to
the
    
lightest
job
opening
a
new
job
only
when
a
command
line
would
grow
past
    
max_chars
.
    
"
"
"
    
nodes
=
[
        
node
        
for
p
in
paths
        
if
(
            
node
:
=
_weigh
(
                
p
os
.
path
.
isdir
(
p
)
root
checks
excluded
ignored
find_dotfiles
            
)
        
)
    
]
    
target
=
sum
(
n
[
1
]
for
n
in
nodes
)
/
num_jobs
    
items
=
[
]
    
while
nodes
:
        
path
weight
children
=
nodes
.
pop
(
)
        
if
not
(
            
children
and
weight
>
target
and
not
os
.
path
.
basename
(
path
)
.
startswith
(
"
.
"
)
        
)
:
            
items
.
append
(
(
weight
[
path
]
)
)
            
continue
        
chunk
chunk_weight
chunk_size
=
[
]
0
0
        
for
child
in
children
:
            
if
child
[
2
]
is
not
None
:
                
nodes
.
append
(
child
)
                
continue
            
size
=
len
(
child
[
0
]
)
+
1
            
if
chunk
and
(
                
chunk_weight
+
child
[
1
]
>
target
or
chunk_size
+
size
>
max_chars
            
)
:
                
items
.
append
(
(
chunk_weight
chunk
)
)
                
chunk
chunk_weight
chunk_size
=
[
]
0
0
            
chunk
.
append
(
child
[
0
]
)
            
chunk_weight
+
=
child
[
1
]
            
chunk_size
+
=
size
        
if
chunk
:
            
items
.
append
(
(
chunk_weight
chunk
)
)
    
jobs
=
[
[
0
0
[
]
]
for
_
in
range
(
num_jobs
)
]
    
for
weight
item_paths
in
sorted
(
items
key
=
lambda
i
:
(
-
i
[
0
]
i
[
1
]
[
0
]
)
)
:
        
size
=
sum
(
len
(
p
)
+
1
for
p
in
item_paths
)
        
job
=
min
(
            
(
j
for
j
in
jobs
if
j
[
1
]
+
size
<
=
max_chars
)
            
key
=
lambda
j
:
(
j
[
0
]
len
(
j
[
2
]
)
)
            
default
=
None
        
)
        
if
job
is
None
:
            
job
=
[
0
0
[
]
]
            
jobs
.
append
(
job
)
        
job
[
0
]
+
=
weight
        
job
[
1
]
+
=
size
        
job
[
2
]
.
extend
(
item_paths
)
    
return
[
j
[
2
]
for
j
in
sorted
(
jobs
key
=
lambda
j
:
-
j
[
0
]
)
if
j
[
2
]
]
def
_ancestors
(
path
)
:
    
parent
=
os
.
path
.
dirname
(
path
)
    
while
parent
!
=
path
:
        
yield
parent
        
path
parent
=
parent
os
.
path
.
dirname
(
parent
)
def
_group_jobs
(
jobs
)
:
    
groups
=
[
]
    
for
job
in
jobs
:
        
paths
=
set
(
job
[
1
]
)
        
ancestors
=
{
a
for
p
in
paths
for
a
in
_ancestors
(
p
)
}
        
for
group_jobs
group_paths
group_ancestors
in
groups
:
            
if
(
                
paths
.
isdisjoint
(
group_paths
)
                
and
paths
.
isdisjoint
(
group_ancestors
)
                
and
ancestors
.
isdisjoint
(
group_paths
)
            
)
:
                
break
        
else
:
            
group_jobs
group_paths
group_ancestors
=
[
]
set
(
)
set
(
)
            
groups
.
append
(
(
group_jobs
group_paths
group_ancestors
)
)
        
group_jobs
.
append
(
job
)
        
group_paths
|
=
paths
        
group_ancestors
|
=
ancestors
    
return
[
group_jobs
for
group_jobs
_
_
in
groups
]
class
InterruptableQueue
(
Queue
)
:
    
"
"
"
A
multiprocessing
.
Queue
that
catches
KeyboardInterrupt
when
a
worker
is
    
blocking
on
it
and
returns
None
.
    
This
is
needed
to
gracefully
handle
KeyboardInterrupts
when
a
worker
is
    
blocking
on
ProcessPoolExecutor
'
s
call
queue
.
    
"
"
"
    
def
__init__
(
self
*
args
*
*
kwargs
)
:
        
kwargs
[
"
ctx
"
]
=
get_context
(
)
        
super
(
)
.
__init__
(
*
args
*
*
kwargs
)
    
def
get
(
self
*
args
*
*
kwargs
)
:
        
try
:
            
return
Queue
.
get
(
self
*
args
*
*
kwargs
)
        
except
KeyboardInterrupt
:
            
return
None
def
_worker_sigint_handler
(
signum
frame
)
:
    
"
"
"
Sigint
handler
for
the
worker
subprocesses
.
    
Tells
workers
not
to
process
the
extra
jobs
on
the
call
queue
that
couldn
'
t
    
be
canceled
by
the
parent
process
.
    
"
"
"
    
global
SHUTDOWN
    
SHUTDOWN
=
True
    
orig_sigint
(
signum
frame
)
def
wrap_futures_atexit
(
)
:
    
"
"
"
Sometimes
futures
'
atexit
handler
can
spew
tracebacks
.
This
wrapper
    
suppresses
them
.
"
"
"
    
try
:
        
futures_atexit
(
)
    
except
Exception
:
        
pass
atexit
.
unregister
(
futures_atexit
)
atexit
.
register
(
wrap_futures_atexit
)
class
LintRoller
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
(
        
50
    
)
    
MAX_CHARS_PER_JOB
=
20000
if
sys
.
platform
=
=
"
win32
"
else
200000
    
def
__init__
(
        
self
        
root
        
exclude
=
None
        
third_party_exclude
=
None
        
include_thiry_party
=
False
        
setupargs
=
None
        
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
root
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
_setup_done
=
set
(
)
        
self
.
lintargs
=
lintargs
        
self
.
lintargs
[
"
root
"
]
=
root
        
self
.
_setupargs
=
setupargs
or
{
}
        
self
.
result
=
ResultSummary
(
            
root
            
fail_on_warnings
=
lintargs
.
get
(
"
show_warnings
"
)
!
=
"
soft
"
        
)
        
self
.
root
=
root
        
self
.
exclude
=
exclude
or
[
]
        
self
.
third_party_exclude
=
third_party_exclude
or
[
]
        
self
.
include_third_party
=
include_thiry_party
        
_setup_logger
(
log
lintargs
.
get
(
"
show_verbose
"
)
)
    
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
str
)
:
            
paths
=
(
paths
)
        
for
linter
in
chain
(
*
[
self
.
parse
(
p
)
for
p
in
paths
]
)
:
            
linter
[
"
local_exclude
"
]
=
linter
.
get
(
"
exclude
"
[
]
)
[
:
]
            
linter
[
"
global_exclude
"
]
=
self
.
exclude
[
:
]
            
exclude
=
linter
.
setdefault
(
"
exclude
"
[
]
)
            
exclude
.
extend
(
self
.
exclude
)
            
if
not
self
.
include_third_party
and
not
linter
.
get
(
                
"
include_third_party
"
False
            
)
:
                
exclude
.
extend
(
self
.
third_party_exclude
)
            
self
.
linters
.
append
(
linter
)
    
def
setup
(
self
virtualenv_manager
=
None
names
=
None
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
        
:
param
names
:
Only
set
up
the
linters
with
these
names
(
optional
)
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
NoValidLinter
        
for
linter
in
self
.
linters
:
            
if
"
setup
"
not
in
linter
or
linter
[
"
name
"
]
in
self
.
_setup_done
:
                
continue
            
if
names
is
not
None
and
linter
[
"
name
"
]
not
in
names
:
                
continue
            
self
.
_setup_done
.
add
(
linter
[
"
name
"
]
)
            
try
:
                
setupargs
=
copy
.
deepcopy
(
self
.
lintargs
)
                
setupargs
.
update
(
self
.
_setupargs
)
                
setupargs
[
"
name
"
]
=
linter
[
"
name
"
]
                
setupargs
[
"
log
"
]
=
logging
.
LoggerAdapter
(
                    
logger
{
"
lintname
"
:
linter
[
"
name
"
]
"
pid
"
:
os
.
getpid
(
)
}
                
)
                
if
virtualenv_manager
is
not
None
:
                    
setupargs
[
"
virtualenv_manager
"
]
=
virtualenv_manager
                
start_time
=
time
.
monotonic
(
)
                
res
=
(
                    
findobject
(
                        
linter
[
"
setup
"
]
                        
linter
[
"
path
"
]
                        
self
.
lintargs
.
get
(
"
linter_paths
"
)
                    
)
(
                        
*
*
setupargs
                    
)
                    
or
0
                
)
                
log
.
debug
(
                    
f
"
setup
for
{
linter
[
'
name
'
]
}
finished
in
"
                    
f
"
{
round
(
time
.
monotonic
(
)
-
start_time
2
)
}
seconds
"
                
)
            
except
Exception
:
                
log
.
exception
(
f
"
{
linter
[
'
name
'
]
}
setup
failed
"
)
                
res
=
1
            
if
res
>
0
:
                
self
.
result
.
failed_setup
.
add
(
linter
[
"
name
"
]
)
                
self
.
result
.
skipped
.
add
(
linter
[
"
name
"
]
)
            
elif
res
<
0
:
                
self
.
result
.
skipped
.
add
(
linter
[
"
name
"
]
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
"
name
"
]
not
in
self
.
result
.
skipped
]
        
if
self
.
result
.
failed_setup
:
            
log
.
error
(
                
"
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
                    
"
"
.
join
(
sorted
(
self
.
result
.
failed_setup
)
)
                
)
            
)
            
return
1
        
if
not
self
.
linters
:
            
log
.
error
(
"
all
linters
were
skipped
due
to
setup
nothing
to
do
!
"
)
            
return
1
        
return
0
    
def
should_lint_entire_tree
(
self
vcs_paths
:
set
[
str
]
linter
:
dict
)
-
>
bool
:
        
"
"
"
Return
True
if
the
linter
should
be
run
on
the
entire
tree
.
"
"
"
        
if
"
fix
"
in
self
.
lintargs
and
self
.
lintargs
[
"
fix
"
]
:
            
return
False
        
if
self
.
lintargs
.
get
(
"
stdin_filename
"
)
:
            
return
False
        
return
any
(
            
os
.
path
.
isfile
(
p
)
            
and
(
                
mozpath
.
match
(
p
pattern
)
                
or
mozpath
.
match
(
mozpath
.
relpath
(
p
self
.
root
)
pattern
)
            
)
            
for
pattern
in
linter
.
get
(
"
support
-
files
"
[
]
)
            
for
p
in
vcs_paths
        
)
    
def
_generate_jobs
(
self
paths
vcs_paths
num_procs
)
:
        
def
__get_current_paths
(
path
=
self
.
root
)
:
            
return
[
os
.
path
.
join
(
path
p
)
for
p
in
os
.
listdir
(
path
)
]
        
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
        
for
linter
in
self
.
linters
:
            
if
self
.
should_lint_entire_tree
(
vcs_paths
linter
)
:
                
lpaths
=
__get_current_paths
(
)
                
print
(
                    
"
warning
:
{
}
support
-
file
modified
linting
entire
tree
"
                    
"
(
press
ctrl
-
c
to
cancel
)
"
.
format
(
linter
[
"
name
"
]
)
                
)
            
elif
paths
=
=
{
os
.
path
.
abspath
(
self
.
root
)
}
:
                
lpaths
=
__get_current_paths
(
)
            
else
:
                
lpaths
=
paths
.
union
(
vcs_paths
)
            
lpaths
=
list
(
lpaths
)
or
__get_current_paths
(
os
.
getcwd
(
)
)
            
depth
=
linter
.
get
(
"
split
-
dirs
"
)
            
if
depth
and
depth
!
=
"
auto
"
:
                
lpaths
=
_split_dirs
(
lpaths
linter
.
get
(
"
find
-
dotfiles
"
False
)
depth
)
            
if
self
.
lintargs
.
get
(
"
use_filters
"
True
)
:
                
lpaths
_
=
filterpaths
(
                    
self
.
root
                    
lpaths
                    
include
=
linter
[
"
include
"
]
                    
exclude
=
linter
.
get
(
"
exclude
"
[
]
)
                    
extensions
=
linter
.
get
(
"
extensions
"
[
]
)
                    
exclude_extensions
=
linter
.
get
(
"
exclude_extensions
"
[
]
)
                    
expand_excludes
=
False
                
)
                
if
not
lpaths
:
                    
continue
            
if
linter
[
"
type
"
]
=
=
"
global
"
:
                
yield
linter
lpaths
                
continue
            
if
depth
=
=
"
auto
"
:
                
extensions
=
tuple
(
f
"
.
{
e
}
"
for
e
in
linter
.
get
(
"
extensions
"
[
]
)
)
                
skipped
=
tuple
(
f
"
.
{
e
}
"
for
e
in
linter
.
get
(
"
exclude_extensions
"
[
]
)
)
                
ignore
=
[
                    
pattern
                    
for
ignore_file
in
linter
.
get
(
"
split
-
ignore
-
files
"
[
]
)
                    
for
pattern
in
_read_ignore_patterns
(
                        
os
.
path
.
join
(
self
.
root
ignore_file
)
                    
)
                
]
                
for
job_paths
in
_balanced_jobs
(
                    
lpaths
                    
num_procs
                    
self
.
root
                    
lambda
p
:
(
                        
p
.
endswith
(
extensions
)
                        
if
extensions
                        
else
not
p
.
endswith
(
skipped
)
                    
)
                    
mozpath
.
matcher
(
                        
linter
.
get
(
"
exclude
"
[
]
)
                        
if
self
.
lintargs
.
get
(
"
use_filters
"
True
)
                        
else
[
]
                    
)
                    
mozpath
.
matcher
(
ignore
)
                    
linter
.
get
(
"
find
-
dotfiles
"
False
)
                    
self
.
MAX_CHARS_PER_JOB
                
)
:
                    
yield
linter
job_paths
                
continue
            
num_jobs
=
max
(
                
min
(
num_procs
len
(
lpaths
)
)
                
int
(
ceil
(
len
(
lpaths
)
/
self
.
MAX_PATHS_PER_JOB
)
)
            
)
            
for
i
in
range
(
num_jobs
)
:
                
yield
linter
lpaths
[
i
:
:
num_jobs
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
        
try
:
            
self
.
result
.
update
(
future
.
result
(
)
)
        
except
Exception
:
            
log
.
exception
(
"
Sub
-
process
raised
an
error
:
"
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
        
rev
=
None
        
num_procs
=
None
        
virtualenv_manager
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
        
Linters
that
have
files
to
lint
are
set
up
first
unless
setup
has
        
already
run
for
them
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
param
virtualenv_manager
:
Passed
to
the
linters
'
setup
functions
.
        
:
return
:
A
:
class
:
~
result
.
ResultSummary
instance
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
result
.
reset
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
str
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
            
log
.
error
(
                
"
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
"
root
"
]
                
)
            
)
        
vcs_paths
=
set
(
)
        
try
:
            
if
workdir
:
                
vcs_paths
.
update
(
self
.
vcs
.
get_changed_files
(
"
AM
"
mode
=
workdir
)
)
            
if
rev
:
                
vcs_paths
.
update
(
self
.
vcs
.
get_changed_files
(
"
AM
"
rev
=
rev
)
)
            
if
outgoing
:
                
upstream
=
outgoing
if
isinstance
(
outgoing
str
)
else
None
                
try
:
                    
vcs_paths
.
update
(
                        
self
.
vcs
.
get_outgoing_files
(
"
AM
"
upstream
=
upstream
)
                    
)
                
except
MissingUpstreamRepo
:
                    
log
.
warning
(
                        
"
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
            
msg
=
f
"
command
failed
:
{
'
'
.
join
(
e
.
cmd
)
}
"
            
if
e
.
output
:
                
msg
=
f
"
{
msg
}
\
n
{
e
.
output
}
"
            
log
.
exception
(
msg
)
        
if
not
(
paths
or
vcs_paths
)
and
(
workdir
or
outgoing
)
:
            
if
os
.
environ
.
get
(
"
MOZ_AUTOMATION
"
)
and
not
os
.
environ
.
get
(
                
"
PYTEST_CURRENT_TEST
"
            
)
:
                
raise
Exception
(
                    
"
Despite
being
a
CI
lint
job
no
files
were
linted
.
Is
the
task
"
                    
"
missing
explicit
paths
?
"
                
)
            
log
.
warning
(
"
no
files
linted
"
)
            
return
self
.
result
        
paths
=
set
(
map
(
os
.
path
.
abspath
paths
)
)
        
vcs_paths
=
set
(
[
            
os
.
path
.
join
(
self
.
root
p
)
if
not
os
.
path
.
isabs
(
p
)
else
p
for
p
in
vcs_paths
        
]
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
vcs_paths
num_procs
)
)
        
if
jobs
:
            
self
.
setup
(
virtualenv_manager
names
=
{
linter
[
"
name
"
]
for
linter
_
in
jobs
}
)
            
jobs
=
[
job
for
job
in
jobs
if
job
[
0
]
[
"
name
"
]
not
in
self
.
result
.
skipped
]
        
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
or
1
        
if
sys
.
platform
=
=
"
win32
"
:
            
num_procs
=
min
(
num_procs
61
)
        
signal
.
signal
(
signal
.
SIGINT
_worker_sigint_handler
)
        
executor
=
ProcessPoolExecutor
(
num_procs
)
        
executor
.
_call_queue
=
InterruptableQueue
(
executor
.
_call_queue
.
_maxsize
)
        
futures
=
[
]
        
def
_parent_sigint_handler
(
signum
frame
)
:
            
"
"
"
Sigint
handler
for
the
parent
process
.
            
Cancels
all
jobs
that
have
not
yet
been
placed
on
the
call
queue
.
            
The
parent
process
won
'
t
exit
until
all
workers
have
terminated
.
            
Assuming
the
linters
are
implemented
properly
this
shouldn
'
t
take
            
more
than
a
couple
seconds
.
            
"
"
"
            
[
f
.
cancel
(
)
for
f
in
futures
]
            
executor
.
shutdown
(
wait
=
True
)
            
log
.
warning
(
"
\
nnot
all
files
were
linted
"
)
            
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
        
signal
.
signal
(
signal
.
SIGINT
_parent_sigint_handler
)
        
if
self
.
lintargs
.
get
(
"
fix
"
)
:
            
for
group_jobs
in
_group_jobs
(
jobs
)
:
                
group_futures
=
[
]
                
for
job
in
group_jobs
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
                    
futures
.
append
(
future
)
                    
group_futures
.
append
(
future
)
                
futures_wait
(
group_futures
)
        
else
:
            
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
                
futures
.
append
(
future
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
result
