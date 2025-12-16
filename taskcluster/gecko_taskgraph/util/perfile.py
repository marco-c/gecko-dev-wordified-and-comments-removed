import
itertools
import
logging
import
math
import
taskgraph
from
mozbuild
.
util
import
memoize
from
mozpack
.
path
import
match
as
mozpackmatch
from
taskgraph
.
util
import
json
logger
=
logging
.
getLogger
(
__name__
)
memoize
def
perfile_number_of_chunks
(
is_try
try_task_config
files_changed
type
)
:
    
changed_files
=
set
(
files_changed
)
    
if
taskgraph
.
fast
and
not
is_try
:
        
return
3
    
tests_per_chunk
=
10
.
0
    
if
type
.
startswith
(
"
test
-
coverage
"
)
:
        
tests_per_chunk
=
30
.
0
    
if
type
.
startswith
(
"
test
-
verify
-
wpt
"
)
or
type
.
startswith
(
"
test
-
coverage
-
wpt
"
)
:
        
file_patterns
=
[
            
"
testing
/
web
-
platform
/
tests
/
*
*
"
            
"
testing
/
web
-
platform
/
mozilla
/
tests
/
*
*
"
        
]
    
elif
type
.
startswith
(
"
test
-
verify
-
gpu
"
)
or
type
.
startswith
(
"
test
-
coverage
-
gpu
"
)
:
        
file_patterns
=
[
            
"
*
*
/
*
webgl
*
/
*
*
/
test_
*
"
            
"
*
*
/
dom
/
canvas
/
*
*
/
test_
*
"
            
"
*
*
/
gfx
/
tests
/
*
*
/
test_
*
"
            
"
*
*
/
devtools
/
canvasdebugger
/
*
*
/
browser_
*
"
            
"
*
*
/
reftest
*
/
*
*
"
        
]
    
elif
type
.
startswith
(
"
test
-
verify
"
)
or
type
.
startswith
(
"
test
-
coverage
"
)
:
        
file_patterns
=
[
            
"
*
*
/
test_
*
"
            
"
*
*
/
browser_
*
"
            
"
*
*
/
crashtest
*
/
*
*
"
            
"
js
/
src
/
tests
/
test
/
*
*
"
            
"
js
/
src
/
tests
/
non262
/
*
*
"
            
"
js
/
src
/
tests
/
test262
/
*
*
"
        
]
    
else
:
        
return
1
    
if
try_task_config
:
        
suite_to_paths
=
json
.
loads
(
try_task_config
)
        
specified_files
=
itertools
.
chain
.
from_iterable
(
suite_to_paths
.
values
(
)
)
        
changed_files
.
update
(
specified_files
)
    
test_count
=
0
    
for
pattern
in
file_patterns
:
        
for
path
in
changed_files
:
            
if
path
.
endswith
(
"
.
list
"
)
or
path
.
endswith
(
"
.
ini
"
)
:
                
continue
            
if
path
.
endswith
(
"
^
headers
^
"
)
:
                
continue
            
if
mozpackmatch
(
path
pattern
)
:
                
gpu
=
False
                
if
type
in
{
"
test
-
verify
-
e10s
"
"
test
-
coverage
-
e10s
"
}
:
                    
gpu_dirs
=
[
                        
"
dom
/
canvas
"
                        
"
gfx
/
tests
"
                        
"
devtools
/
canvasdebugger
"
                        
"
webgl
"
                    
]
                    
for
gdir
in
gpu_dirs
:
                        
if
len
(
path
.
split
(
gdir
)
)
>
1
:
                            
gpu
=
True
                
if
not
gpu
:
                    
test_count
+
=
1
    
chunks
=
test_count
/
tests_per_chunk
    
chunks
=
int
(
math
.
ceil
(
chunks
)
)
    
if
is_try
and
chunks
=
=
0
:
        
chunks
=
1
    
return
chunks
