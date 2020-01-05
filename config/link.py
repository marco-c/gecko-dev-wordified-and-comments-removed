import
expandlibs_exec
import
sys
import
threading
import
time
def
periodically_print_status
(
proc
)
:
    
"
"
"
    
Print
something
to
the
console
every
20
minutes
to
prevent
the
build
job
    
from
getting
killed
when
linking
a
large
binary
.
    
Check
status
of
the
linker
every
0
.
5
seconds
.
    
"
"
"
    
idleTime
=
0
    
while
proc
.
returncode
is
None
:
        
time
.
sleep
(
0
.
5
)
        
idleTime
+
=
0
.
5
        
if
idleTime
>
20
*
60
:
          
print
"
Still
linking
20
minutes
passed
.
.
.
"
          
sys
.
stdout
.
flush
(
)
          
idleTime
=
0
def
wrap_linker
(
args
)
:
    
"
"
"
    
Execute
|
args
|
and
pass
resulting
|
proc
|
object
to
a
second
thread
that
    
will
track
the
status
of
the
started
|
proc
|
.
    
"
"
"
    
t
=
[
None
]
    
def
callback
(
proc
)
:
        
t
[
0
]
=
threading
.
Thread
(
target
=
periodically_print_status
                             
args
=
(
proc
)
)
        
t
[
0
]
.
start
(
)
    
exitcode
=
expandlibs_exec
.
main
(
args
proc_callback
=
callback
)
    
t
[
0
]
.
join
(
)
    
return
exitcode
if
__name__
=
=
"
__main__
"
:
    
if
len
(
sys
.
argv
)
<
2
:
        
print
>
>
sys
.
stderr
"
Usage
:
link
.
py
<
commandline
>
"
        
sys
.
exit
(
1
)
    
sys
.
exit
(
wrap_linker
(
sys
.
argv
[
1
:
]
)
)
