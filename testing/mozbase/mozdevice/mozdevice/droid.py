from
__future__
import
absolute_import
import
StringIO
import
re
import
time
from
mozdevice
import
version_codes
from
.
devicemanagerADB
import
DeviceManagerADB
from
.
devicemanager
import
DMError
class
DroidMixin
(
object
)
:
    
"
"
"
Mixin
to
extend
DeviceManager
with
Android
-
specific
functionality
"
"
"
    
_stopApplicationNeedsRoot
=
True
    
def
_getExtraAmStartArgs
(
self
)
:
        
return
[
]
    
def
launchApplication
(
self
appName
activityName
intent
url
=
None
                          
extras
=
None
wait
=
True
failIfRunning
=
True
)
:
        
"
"
"
        
Launches
an
Android
application
        
:
param
appName
:
Name
of
application
(
e
.
g
.
com
.
android
.
chrome
)
        
:
param
activityName
:
Name
of
activity
to
launch
(
e
.
g
.
.
Main
)
        
:
param
intent
:
Intent
to
launch
application
with
        
:
param
url
:
URL
to
open
        
:
param
extras
:
Dictionary
of
extra
arguments
to
launch
application
with
        
:
param
wait
:
If
True
wait
for
application
to
start
before
returning
        
:
param
failIfRunning
:
Raise
an
exception
if
instance
of
application
is
already
running
        
"
"
"
        
if
failIfRunning
and
self
.
processExist
(
appName
)
:
            
raise
DMError
(
"
Only
one
instance
of
an
application
may
be
running
"
                          
"
at
once
"
)
        
acmd
=
[
"
am
"
"
start
"
]
+
self
.
_getExtraAmStartArgs
(
)
+
\
            
[
"
-
W
"
if
wait
else
'
'
"
-
n
"
"
%
s
/
%
s
"
%
(
appName
activityName
)
]
        
if
intent
:
            
acmd
.
extend
(
[
"
-
a
"
intent
]
)
        
if
extras
:
            
for
(
key
val
)
in
extras
.
iteritems
(
)
:
                
if
type
(
val
)
is
int
:
                    
extraTypeParam
=
"
-
-
ei
"
                
elif
type
(
val
)
is
bool
:
                    
extraTypeParam
=
"
-
-
ez
"
                
else
:
                    
extraTypeParam
=
"
-
-
es
"
                
acmd
.
extend
(
[
extraTypeParam
str
(
key
)
str
(
val
)
]
)
        
if
url
:
            
acmd
.
extend
(
[
"
-
d
"
url
]
)
        
shellOutput
=
StringIO
.
StringIO
(
)
        
if
self
.
shell
(
acmd
shellOutput
)
=
=
0
:
            
return
        
shellOutput
.
seek
(
0
)
        
raise
DMError
(
"
Unable
to
launch
application
(
shell
output
:
'
%
s
'
)
"
%
shellOutput
.
read
(
)
)
    
def
launchFennec
(
self
appName
intent
=
"
android
.
intent
.
action
.
VIEW
"
                     
mozEnv
=
None
extraArgs
=
None
url
=
None
wait
=
True
                     
failIfRunning
=
True
)
:
        
"
"
"
        
Convenience
method
to
launch
Fennec
on
Android
with
various
debugging
        
arguments
        
:
param
appName
:
Name
of
fennec
application
(
e
.
g
.
org
.
mozilla
.
fennec
)
        
:
param
intent
:
Intent
to
launch
application
with
        
:
param
mozEnv
:
Mozilla
specific
environment
to
pass
into
application
        
:
param
extraArgs
:
Extra
arguments
to
be
parsed
by
fennec
        
:
param
url
:
URL
to
open
        
:
param
wait
:
If
True
wait
for
application
to
start
before
returning
        
:
param
failIfRunning
:
Raise
an
exception
if
instance
of
application
is
already
running
        
"
"
"
        
extras
=
{
}
        
if
mozEnv
:
            
for
(
envCnt
(
envkey
envval
)
)
in
enumerate
(
mozEnv
.
iteritems
(
)
)
:
                
extras
[
"
env
"
+
str
(
envCnt
)
]
=
envkey
+
"
=
"
+
envval
        
if
extraArgs
:
            
extras
[
'
args
'
]
=
"
"
.
join
(
extraArgs
)
        
self
.
launchApplication
(
appName
"
.
App
"
intent
url
=
url
                               
extras
=
extras
                               
wait
=
wait
failIfRunning
=
failIfRunning
)
    
def
getInstalledApps
(
self
)
:
        
"
"
"
        
Lists
applications
installed
on
this
Android
device
        
Returns
a
list
of
application
names
in
the
form
[
'
org
.
mozilla
.
fennec
'
.
.
.
]
        
"
"
"
        
output
=
self
.
shellCheckOutput
(
[
"
pm
"
"
list
"
"
packages
"
"
-
f
"
]
)
        
apps
=
[
]
        
for
line
in
output
.
splitlines
(
)
:
            
apps
.
append
(
line
.
split
(
'
=
'
)
[
1
]
)
        
return
apps
    
def
stopApplication
(
self
appName
)
:
        
"
"
"
        
Stops
the
specified
application
        
For
Android
3
.
0
+
we
use
the
"
am
force
-
stop
"
to
do
this
which
is
        
reliable
and
does
not
require
root
.
For
earlier
versions
of
Android
        
we
simply
try
to
manually
kill
the
processes
started
by
the
app
        
repeatedly
until
none
is
around
any
more
.
This
is
less
reliable
and
        
does
require
root
.
        
:
param
appName
:
Name
of
application
(
e
.
g
.
com
.
android
.
chrome
)
        
"
"
"
        
version
=
self
.
shellCheckOutput
(
[
"
getprop
"
"
ro
.
build
.
version
.
sdk
"
]
)
        
if
int
(
version
)
>
=
version_codes
.
HONEYCOMB
:
            
self
.
shellCheckOutput
(
[
"
am
"
"
force
-
stop
"
appName
]
                                  
root
=
self
.
_stopApplicationNeedsRoot
)
        
else
:
            
num_tries
=
0
            
max_tries
=
5
            
while
self
.
processExist
(
appName
)
:
                
if
num_tries
>
max_tries
:
                    
raise
DMError
(
"
Couldn
'
t
successfully
kill
%
s
after
%
s
"
                                  
"
tries
"
%
(
appName
max_tries
)
)
                
self
.
killProcess
(
appName
)
                
num_tries
+
=
1
                
time
.
sleep
(
1
)
class
DroidADB
(
DeviceManagerADB
DroidMixin
)
:
    
_stopApplicationNeedsRoot
=
False
    
def
getTopActivity
(
self
)
:
        
package
=
None
        
data
=
None
        
try
:
            
data
=
self
.
shellCheckOutput
(
                
[
"
dumpsys
"
"
window
"
"
windows
"
]
timeout
=
60
)
        
except
Exception
:
            
return
"
"
        
m
=
re
.
search
(
'
mFocusedApp
(
.
+
)
/
'
data
)
        
if
not
m
:
            
m
=
re
.
search
(
'
FocusedApplication
(
.
+
)
/
'
data
)
        
if
m
:
            
line
=
m
.
group
(
0
)
            
m
=
re
.
search
(
'
(
\
S
+
)
/
'
line
)
            
if
m
:
                
package
=
m
.
group
(
1
)
        
if
not
package
:
            
package
=
"
"
        
return
package
    
def
getAppRoot
(
self
packageName
)
:
        
"
"
"
        
Returns
the
root
directory
for
the
specified
android
application
        
"
"
"
        
return
'
/
data
/
data
/
%
s
'
%
packageName
