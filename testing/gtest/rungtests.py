from
__future__
import
with_statement
from
optparse
import
OptionParser
import
os
import
sys
import
mozcrash
import
mozinfo
import
mozlog
import
mozprocess
from
mozrunner
.
utils
import
get_stack_fixer_function
log
=
mozlog
.
unstructured
.
getLogger
(
'
gtest
'
)
class
GTests
(
object
)
:
    
TEST_PROC_TIMEOUT
=
1200
    
TEST_PROC_NO_OUTPUT_TIMEOUT
=
300
    
def
run_gtest
(
self
prog
xre_path
cwd
symbols_path
=
None
                  
utility_path
=
None
)
:
        
"
"
"
        
Run
a
single
C
+
+
unit
test
program
.
        
Arguments
:
        
*
prog
:
The
path
to
the
test
program
to
run
.
        
*
env
:
The
environment
to
use
for
running
the
program
.
        
*
cwd
:
The
directory
to
run
tests
from
(
support
files
will
be
found
               
in
this
direcotry
)
.
        
*
symbols_path
:
A
path
to
a
directory
containing
Breakpad
-
formatted
                        
symbol
files
for
producing
stack
traces
on
crash
.
        
*
utility_path
:
A
path
to
a
directory
containing
utility
programs
.
                        
currently
used
to
locate
a
stack
fixer
to
provide
                        
symbols
symbols
for
assertion
stacks
.
        
Return
True
if
the
program
exits
with
a
zero
status
False
otherwise
.
        
"
"
"
        
self
.
xre_path
=
xre_path
        
env
=
self
.
build_environment
(
)
        
log
.
info
(
"
Running
gtest
"
)
        
if
cwd
and
not
os
.
path
.
isdir
(
cwd
)
:
            
os
.
makedirs
(
cwd
)
        
stream_output
=
mozprocess
.
StreamOutput
(
sys
.
stdout
)
        
process_output
=
stream_output
        
if
utility_path
:
            
stack_fixer
=
get_stack_fixer_function
(
utility_path
symbols_path
)
            
if
stack_fixer
:
                
process_output
=
lambda
line
:
stream_output
(
stack_fixer
(
line
)
)
        
proc
=
mozprocess
.
ProcessHandler
(
[
prog
"
-
unittest
"
                                         
"
-
-
gtest_death_test_style
=
threadsafe
"
]
                                         
cwd
=
cwd
                                         
env
=
env
                                         
processOutputLine
=
process_output
)
        
proc
.
run
(
timeout
=
GTests
.
TEST_PROC_TIMEOUT
                 
outputTimeout
=
GTests
.
TEST_PROC_NO_OUTPUT_TIMEOUT
)
        
proc
.
wait
(
)
        
if
proc
.
timedOut
:
            
log
.
testFail
(
"
gtest
|
timed
out
after
%
d
seconds
"
GTests
.
TEST_PROC_TIMEOUT
)
            
return
False
        
if
mozcrash
.
check_for_crashes
(
cwd
symbols_path
test_name
=
"
gtest
"
)
:
            
return
False
        
result
=
proc
.
proc
.
returncode
=
=
0
        
if
not
result
:
            
log
.
testFail
(
"
gtest
|
test
failed
with
return
code
%
d
"
proc
.
proc
.
returncode
)
        
return
result
    
def
build_core_environment
(
self
env
=
{
}
)
:
        
"
"
"
        
Add
environment
variables
likely
to
be
used
across
all
platforms
including
remote
systems
.
        
"
"
"
        
env
[
"
MOZ_XRE_DIR
"
]
=
self
.
xre_path
        
env
[
"
MOZ_GMP_PATH
"
]
=
os
.
pathsep
.
join
(
            
os
.
path
.
join
(
self
.
xre_path
p
"
1
.
0
"
)
            
for
p
in
(
'
gmp
-
fake
'
'
gmp
-
fakeopenh264
'
)
        
)
        
env
[
"
XPCOM_DEBUG_BREAK
"
]
=
"
stack
-
and
-
abort
"
        
env
[
"
MOZ_CRASHREPORTER_NO_REPORT
"
]
=
"
1
"
        
env
[
"
MOZ_CRASHREPORTER
"
]
=
"
1
"
        
env
[
"
MOZ_RUN_GTEST
"
]
=
"
1
"
        
env
[
"
MOZ_TBPL_PARSER
"
]
=
"
1
"
        
if
not
mozinfo
.
has_sandbox
:
          
env
[
"
MOZ_DISABLE_GMP_SANDBOX
"
]
=
"
1
"
        
return
env
    
def
build_environment
(
self
)
:
        
"
"
"
        
Create
and
return
a
dictionary
of
all
the
appropriate
env
variables
and
values
.
        
On
a
remote
system
we
overload
this
to
set
different
values
and
are
missing
things
like
os
.
environ
and
PATH
.
        
"
"
"
        
if
not
os
.
path
.
isdir
(
self
.
xre_path
)
:
            
raise
Exception
(
"
xre_path
does
not
exist
:
%
s
"
self
.
xre_path
)
        
env
=
dict
(
os
.
environ
)
        
env
=
self
.
build_core_environment
(
env
)
        
env
[
"
PERFHERDER_ALERTING_ENABLED
"
]
=
"
1
"
        
pathvar
=
"
"
        
if
mozinfo
.
os
=
=
"
linux
"
:
            
pathvar
=
"
LD_LIBRARY_PATH
"
            
del
env
[
"
PERFHERDER_ALERTING_ENABLED
"
]
        
elif
mozinfo
.
os
=
=
"
mac
"
:
            
pathvar
=
"
DYLD_LIBRARY_PATH
"
        
elif
mozinfo
.
os
=
=
"
win
"
:
            
pathvar
=
"
PATH
"
        
if
pathvar
:
            
if
pathvar
in
env
:
                
env
[
pathvar
]
=
"
%
s
%
s
%
s
"
%
(
self
.
xre_path
os
.
pathsep
env
[
pathvar
]
)
            
else
:
                
env
[
pathvar
]
=
self
.
xre_path
        
if
mozinfo
.
info
[
"
asan
"
]
:
            
llvmsym
=
os
.
path
.
join
(
                
self
.
xre_path
                
"
llvm
-
symbolizer
"
+
mozinfo
.
info
[
"
bin_suffix
"
]
.
encode
(
'
ascii
'
)
)
            
if
os
.
path
.
isfile
(
llvmsym
)
:
                
env
[
"
ASAN_SYMBOLIZER_PATH
"
]
=
llvmsym
                
log
.
info
(
"
gtest
|
ASan
using
symbolizer
at
%
s
"
llvmsym
)
            
else
:
                
log
.
info
(
"
gtest
|
Failed
to
find
ASan
symbolizer
at
%
s
"
llvmsym
)
        
return
env
class
gtestOptions
(
OptionParser
)
:
    
def
__init__
(
self
)
:
        
OptionParser
.
__init__
(
self
)
        
self
.
add_option
(
"
-
-
cwd
"
                        
dest
=
"
cwd
"
                        
default
=
os
.
getcwd
(
)
                        
help
=
"
absolute
path
to
directory
from
which
to
run
the
binary
"
)
        
self
.
add_option
(
"
-
-
xre
-
path
"
                        
dest
=
"
xre_path
"
                        
default
=
None
                        
help
=
"
absolute
path
to
directory
containing
XRE
(
probably
xulrunner
)
"
)
        
self
.
add_option
(
"
-
-
symbols
-
path
"
                        
dest
=
"
symbols_path
"
                        
default
=
None
                        
help
=
"
absolute
path
to
directory
containing
breakpad
symbols
or
the
URL
of
a
zip
file
containing
symbols
"
)
        
self
.
add_option
(
"
-
-
utility
-
path
"
                        
dest
=
"
utility_path
"
                        
default
=
None
                        
help
=
"
path
to
a
directory
containing
utility
program
binaries
"
)
def
update_mozinfo
(
)
:
    
"
"
"
walk
up
directories
to
find
mozinfo
.
json
update
the
info
"
"
"
    
path
=
os
.
path
.
abspath
(
os
.
path
.
realpath
(
os
.
path
.
dirname
(
__file__
)
)
)
    
dirs
=
set
(
)
    
while
path
!
=
os
.
path
.
expanduser
(
'
~
'
)
:
        
if
path
in
dirs
:
            
break
        
dirs
.
add
(
path
)
        
path
=
os
.
path
.
split
(
path
)
[
0
]
    
mozinfo
.
find_and_update_from_json
(
*
dirs
)
def
main
(
)
:
    
parser
=
gtestOptions
(
)
    
options
args
=
parser
.
parse_args
(
)
    
if
not
args
:
        
print
>
>
sys
.
stderr
"
"
"
Usage
:
%
s
<
binary
>
"
"
"
%
sys
.
argv
[
0
]
        
sys
.
exit
(
1
)
    
if
not
options
.
xre_path
:
        
print
>
>
sys
.
stderr
"
"
"
Error
:
-
-
xre
-
path
is
required
"
"
"
        
sys
.
exit
(
1
)
    
if
not
options
.
utility_path
:
        
print
>
>
sys
.
stderr
"
"
"
Warning
:
-
-
utility
-
path
is
required
to
process
assertion
stacks
"
"
"
    
update_mozinfo
(
)
    
prog
=
os
.
path
.
abspath
(
args
[
0
]
)
    
options
.
xre_path
=
os
.
path
.
abspath
(
options
.
xre_path
)
    
tester
=
GTests
(
)
    
try
:
        
result
=
tester
.
run_gtest
(
prog
options
.
xre_path
                                  
options
.
cwd
                                  
symbols_path
=
options
.
symbols_path
                                  
utility_path
=
options
.
utility_path
)
    
except
Exception
e
:
        
log
.
error
(
str
(
e
)
)
        
result
=
False
    
sys
.
exit
(
0
if
result
else
1
)
if
__name__
=
=
'
__main__
'
:
    
main
(
)
