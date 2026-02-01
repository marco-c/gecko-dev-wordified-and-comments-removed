import
os
from
urllib
.
parse
import
quote
from
marionette_driver
import
Wait
errors
from
marionette_harness
import
MarionetteTestCase
WindowManagerMixin
def
inline
(
doc
)
:
    
return
f
"
data
:
text
/
html
;
charset
=
utf
-
8
{
quote
(
doc
)
}
"
class
TestSessionRestoreLogging
(
WindowManagerMixin
MarionetteTestCase
)
:
    
def
setUp
(
self
)
:
        
super
(
)
.
setUp
(
)
        
self
.
marionette
.
enforce_gecko_prefs
(
{
            
"
browser
.
sessionstore
.
loglevel
"
:
"
Debug
"
            
"
browser
.
sessionstore
.
log
.
appender
.
file
.
logOnSuccess
"
:
True
        
}
)
    
def
tearDown
(
self
)
:
        
try
:
            
self
.
marionette
.
restart
(
in_app
=
False
clean
=
True
)
        
finally
:
            
super
(
)
.
tearDown
(
)
    
def
getSessionFilePath
(
self
)
:
        
profilePath
=
self
.
marionette
.
instance
.
profile
.
profile
        
assert
profilePath
is
not
None
        
return
os
.
path
.
join
(
profilePath
"
sessionstore
.
jsonlz4
"
)
    
def
getLogDirectoryPath
(
self
)
:
        
profilePath
=
self
.
marionette
.
instance
.
profile
.
profile
        
assert
profilePath
is
not
None
        
return
os
.
path
.
join
(
profilePath
"
sessionstore
-
logs
"
)
    
def
cleanupLogDirectory
(
self
)
:
        
dirPath
=
self
.
getLogDirectoryPath
(
)
        
for
fname
in
self
.
getLogFiles
(
)
:
            
fpath
=
os
.
path
.
join
(
dirPath
fname
)
            
os
.
remove
(
fpath
)
    
def
getLogFiles
(
self
matchstr
=
"
"
)
:
        
dirPath
=
self
.
getLogDirectoryPath
(
)
        
fileNames
=
[
]
        
if
os
.
path
.
isdir
(
dirPath
)
:
            
fileNames
=
[
entry
.
name
for
entry
in
os
.
scandir
(
dirPath
)
if
entry
.
is_file
(
)
]
        
if
len
(
matchstr
)
>
0
and
len
(
fileNames
)
>
0
:
            
fileNames
=
filter
(
lambda
name
:
matchstr
in
name
fileNames
)
        
return
fileNames
    
def
getMostRecentLogFile
(
self
matchstr
=
"
"
)
:
        
dirPath
=
self
.
getLogDirectoryPath
(
)
        
files
=
[
os
.
path
.
join
(
dirPath
f
)
for
f
in
self
.
getLogFiles
(
matchstr
)
]
        
return
max
(
files
key
=
os
.
path
.
getctime
)
if
len
(
files
)
>
0
else
None
    
def
openAndCloseSaveworthyWindow
(
self
)
:
        
urls
=
(
            
inline
(
"
"
"
<
div
"
>
ipsum
<
/
div
>
"
"
"
)
            
inline
(
"
"
"
<
div
"
>
dolor
<
/
div
>
"
"
"
)
        
)
        
self
.
marionette
.
set_context
(
"
chrome
"
)
        
origWindow
=
self
.
marionette
.
current_window_handle
        
win
=
self
.
open_window
(
private
=
False
)
        
self
.
marionette
.
switch_to_window
(
win
)
        
with
self
.
marionette
.
using_context
(
"
content
"
)
:
            
for
index
url
in
enumerate
(
urls
)
:
                
if
index
>
0
:
                    
tab
=
self
.
open_tab
(
)
                    
self
.
marionette
.
switch_to_window
(
tab
)
                
self
.
marionette
.
navigate
(
url
)
        
self
.
marionette
.
execute_script
(
"
window
.
close
(
)
"
)
        
self
.
marionette
.
switch_to_window
(
origWindow
)
    
def
getLineCount
(
self
logFile
)
:
        
with
open
(
logFile
)
as
f
:
            
return
sum
(
1
for
_
in
f
)
    
def
test_per_startup_logfile_creation
(
self
)
:
        
self
.
marionette
.
quit
(
)
        
self
.
cleanupLogDirectory
(
)
        
self
.
marionette
.
start_session
(
)
        
self
.
marionette
.
set_context
(
"
chrome
"
)
        
self
.
marionette
.
quit
(
)
        
self
.
assertEqual
(
            
len
(
self
.
getLogFiles
(
)
)
            
1
            
"
Exactly
one
log
file
was
created
after
a
restart
and
quit
"
        
)
        
self
.
marionette
.
start_session
(
)
    
def
test_errors_flush_to_disk
(
self
)
:
        
self
.
marionette
.
enforce_gecko_prefs
(
{
            
"
browser
.
sessionstore
.
log
.
appender
.
file
.
logOnSuccess
"
:
False
        
}
)
        
self
.
marionette
.
quit
(
)
        
sessionFile
=
self
.
getSessionFilePath
(
)
        
self
.
assertTrue
(
            
os
.
path
.
isfile
(
sessionFile
)
            
"
The
sessionstore
.
jsonlz4
file
exists
in
the
profile
directory
"
        
)
        
with
open
(
sessionFile
"
wb
"
)
as
f
:
            
f
.
write
(
b
"
\
x00
\
xff
\
xabgarbageDATA
"
)
        
self
.
marionette
.
start_session
(
)
        
self
.
marionette
.
set_context
(
"
chrome
"
)
        
errorLogFile
=
self
.
getMostRecentLogFile
(
"
error
-
"
)
        
self
.
assertTrue
(
errorLogFile
"
We
logged
errors
immediately
"
)
        
if
os
.
path
.
isfile
(
sessionFile
)
:
            
os
.
remove
(
sessionFile
)
    
def
test_periodic_flush_to_disk
(
self
)
:
        
logFile
=
self
.
getMostRecentLogFile
(
)
        
logFileCount
=
len
(
self
.
getLogFiles
(
)
)
        
self
.
assertTrue
(
logFile
"
A
log
file
already
exists
"
)
        
self
.
assertEqual
(
logFileCount
1
"
A
single
'
success
'
log
file
exists
"
)
        
startLineCount
=
self
.
getLineCount
(
logFile
)
        
self
.
openAndCloseSaveworthyWindow
(
)
        
self
.
assertEqual
(
            
self
.
getLineCount
(
logFile
)
            
startLineCount
            
"
Log
file
line
count
unchanged
;
debug
messages
should
be
buffered
and
not
yet
flushed
to
disk
"
        
)
        
self
.
marionette
.
set_pref
(
"
browser
.
sessionstore
.
logFlushIntervalSeconds
"
1
)
        
origWindow
=
self
.
marionette
.
current_window_handle
        
self
.
openAndCloseSaveworthyWindow
(
)
        
try
:
            
wait
=
Wait
(
self
.
marionette
timeout
=
5
interval
=
0
.
1
)
            
wait
.
until
(
                
lambda
_
:
self
.
getLineCount
(
logFile
)
>
startLineCount
                
message
=
"
Waiting
for
line
count
in
the
log
file
to
grow
"
            
)
            
newLineCount
=
self
.
getLineCount
(
logFile
)
            
self
.
assertTrue
(
                
newLineCount
>
startLineCount
                
f
"
{
newLineCount
-
startLineCount
}
lines
got
flushed
to
the
log
file
"
            
)
        
except
errors
.
TimeoutException
as
e
:
            
message
=
(
                
f
"
{
e
.
message
}
.
Line
count
didn
'
t
grow
as
expected
in
log
file
{
logFile
}
"
            
)
            
raise
errors
.
TimeoutException
(
message
)
        
finally
:
            
self
.
marionette
.
switch_to_window
(
origWindow
)
            
self
.
marionette
.
clear_pref
(
"
browser
.
sessionstore
.
logFlushIntervalSeconds
"
)
        
self
.
assertTrue
(
            
self
.
getLineCount
(
logFile
)
>
startLineCount
            
"
Debug
log
messages
got
flushed
to
disk
"
        
)
        
self
.
assertEqual
(
            
len
(
self
.
getLogFiles
(
)
)
            
logFileCount
            
"
We
just
appended
to
the
one
log
file
and
didn
'
t
create
any
others
"
        
)
