import
os
import
stat
from
urllib
.
parse
import
quote
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
TestSessionRestoreLogging
self
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
TestSessionRestoreLogging
self
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
        
os
.
chmod
(
sessionFile
stat
.
S_IWUSR
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
