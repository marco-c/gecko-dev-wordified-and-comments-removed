"
"
"
mac_desktop_image
.
py
Mac
-
specific
utility
to
get
/
set
the
desktop
background
image
or
check
that
the
current
background
image
path
matches
a
provided
path
.
Depends
on
Objective
-
C
python
binding
imports
which
are
in
the
python
import
paths
by
default
when
using
macOS
'
s
/
usr
/
bin
/
python
.
Includes
generous
amount
of
logging
to
aid
debugging
for
use
in
automated
tests
.
"
"
"
from
__future__
import
absolute_import
print_function
import
argparse
import
logging
import
os
import
sys
from
AppKit
import
NSScreen
NSWorkspace
from
Cocoa
import
NSURL
def
main
(
)
:
    
parser
=
argparse
.
ArgumentParser
(
        
description
=
"
Utility
to
print
set
or
"
        
+
"
check
the
path
to
image
being
used
as
"
        
+
"
the
desktop
background
image
.
By
"
        
+
"
default
prints
the
path
to
the
"
        
+
"
current
desktop
background
image
.
"
    
)
    
parser
.
add_argument
(
        
"
-
v
"
        
"
-
-
verbose
"
        
action
=
"
store_true
"
        
help
=
"
print
verbose
debugging
information
"
        
default
=
False
    
)
    
group
=
parser
.
add_mutually_exclusive_group
(
)
    
group
.
add_argument
(
        
"
-
s
"
        
"
-
-
set
-
background
-
image
"
        
dest
=
"
newBackgroundImagePath
"
        
required
=
False
        
help
=
"
path
to
the
new
background
image
to
set
.
A
zero
"
        
+
"
exit
code
indicates
no
errors
occurred
.
"
        
default
=
None
    
)
    
group
.
add_argument
(
        
"
-
c
"
        
"
-
-
check
-
background
-
image
"
        
dest
=
"
checkBackgroundImagePath
"
        
required
=
False
        
help
=
"
check
if
the
provided
background
image
path
"
        
+
"
matches
the
provided
path
.
A
zero
exit
code
"
        
+
"
indicates
the
paths
match
.
"
        
default
=
None
    
)
    
args
=
parser
.
parse_args
(
)
    
if
args
.
verbose
:
        
logging
.
basicConfig
(
level
=
logging
.
DEBUG
)
    
else
:
        
logging
.
basicConfig
(
level
=
logging
.
CRITICAL
)
    
logger
=
logging
.
getLogger
(
"
desktopImage
"
)
    
if
args
.
checkBackgroundImagePath
is
not
None
:
        
logger
.
debug
(
            
"
checking
provided
desktop
image
%
s
matches
current
"
            
"
image
"
%
args
.
checkBackgroundImagePath
        
)
    
elif
args
.
newBackgroundImagePath
is
not
None
:
        
logger
.
debug
(
"
setting
image
to
%
s
"
%
args
.
newBackgroundImagePath
)
    
else
:
        
logger
.
debug
(
"
retrieving
desktop
image
path
"
)
    
focussedScreen
=
NSScreen
.
mainScreen
(
)
    
if
not
focussedScreen
:
        
raise
RuntimeError
(
"
mainScreen
error
"
)
    
ws
=
NSWorkspace
.
sharedWorkspace
(
)
    
if
not
ws
:
        
raise
RuntimeError
(
"
sharedWorkspace
error
"
)
    
if
args
.
checkBackgroundImagePath
is
not
None
:
        
existingImageURL
=
getCurrentDesktopImageURL
(
focussedScreen
ws
logger
)
        
existingImagePath
=
existingImageURL
.
path
(
)
        
existingImagePathReal
=
os
.
path
.
realpath
(
existingImagePath
)
        
logger
.
debug
(
"
existing
desktop
image
:
%
s
"
%
existingImagePath
)
        
logger
.
debug
(
"
existing
desktop
image
realpath
:
%
s
"
%
existingImagePath
)
        
checkImagePathReal
=
os
.
path
.
realpath
(
args
.
checkBackgroundImagePath
)
        
logger
.
debug
(
"
check
desktop
image
:
%
s
"
%
args
.
checkBackgroundImagePath
)
        
logger
.
debug
(
"
check
desktop
image
realpath
:
%
s
"
%
checkImagePathReal
)
        
if
existingImagePathReal
=
=
checkImagePathReal
:
            
print
(
"
desktop
image
path
matches
provided
path
"
)
            
return
True
        
print
(
"
desktop
image
path
does
NOT
match
provided
path
"
)
        
return
False
    
if
args
.
verbose
:
        
existingImageURL
=
getCurrentDesktopImageURL
(
focussedScreen
ws
logger
)
        
logger
.
debug
(
"
existing
desktop
image
:
%
s
"
%
existingImageURL
.
path
(
)
)
    
if
args
.
newBackgroundImagePath
is
not
None
:
        
newImagePath
=
args
.
newBackgroundImagePath
        
if
not
os
.
path
.
exists
(
newImagePath
)
:
            
logger
.
critical
(
"
%
s
does
not
exist
"
%
newImagePath
)
            
return
False
        
if
not
os
.
access
(
newImagePath
os
.
R_OK
)
:
            
logger
.
critical
(
"
%
s
is
not
readable
"
%
newImagePath
)
            
return
False
        
logger
.
debug
(
"
new
desktop
image
to
set
:
%
s
"
%
newImagePath
)
        
newImageURL
=
NSURL
.
fileURLWithPath_
(
newImagePath
)
        
logger
.
debug
(
"
new
desktop
image
URL
to
set
:
%
s
"
%
newImageURL
)
        
status
=
False
        
(
status
error
)
=
ws
.
setDesktopImageURL_forScreen_options_error_
(
            
newImageURL
focussedScreen
None
None
        
)
        
if
not
status
:
            
raise
RuntimeError
(
"
setDesktopImageURL
error
"
)
    
imageURL
=
getCurrentDesktopImageURL
(
focussedScreen
ws
logger
)
    
imagePath
=
imageURL
.
path
(
)
    
imagePathReal
=
os
.
path
.
realpath
(
imagePath
)
    
logger
.
debug
(
"
updated
desktop
image
URL
:
%
s
"
%
imageURL
)
    
logger
.
debug
(
"
updated
desktop
image
path
:
%
s
"
%
imagePath
)
    
logger
.
debug
(
"
updated
desktop
image
path
(
resolved
)
:
%
s
"
%
imagePathReal
)
    
print
(
imagePathReal
)
    
return
True
def
getCurrentDesktopImageURL
(
focussedScreen
workspace
logger
)
:
    
imageURL
=
workspace
.
desktopImageURLForScreen_
(
focussedScreen
)
    
if
not
imageURL
:
        
raise
RuntimeError
(
"
desktopImageURLForScreen
returned
invalid
URL
"
)
    
if
not
imageURL
.
isFileURL
(
)
:
        
logger
.
warning
(
"
desktop
image
URL
is
not
a
file
URL
"
)
    
return
imageURL
if
__name__
=
=
"
__main__
"
:
    
if
not
main
(
)
:
        
sys
.
exit
(
1
)
    
else
:
        
sys
.
exit
(
0
)
