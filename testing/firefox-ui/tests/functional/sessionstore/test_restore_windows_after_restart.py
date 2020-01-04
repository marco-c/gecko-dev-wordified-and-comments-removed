from
firefox_ui_harness
.
testcases
import
FirefoxTestCase
class
TestRestoreWindowsAfterRestart
(
FirefoxTestCase
)
:
    
def
setUp
(
self
)
:
        
FirefoxTestCase
.
setUp
(
self
)
        
self
.
test_windows
=
set
(
[
            
(
self
.
marionette
.
absolute_url
(
'
layout
/
mozilla
.
html
'
)
)
            
(
self
.
marionette
.
absolute_url
(
'
layout
/
mozilla_organizations
.
html
'
)
             
self
.
marionette
.
absolute_url
(
'
layout
/
mozilla_community
.
html
'
)
)
            
(
self
.
marionette
.
absolute_url
(
'
layout
/
mozilla_governance
.
html
'
)
             
self
.
marionette
.
absolute_url
(
'
layout
/
mozilla_grants
.
html
'
)
)
        
]
)
        
self
.
private_windows
=
set
(
[
            
(
self
.
marionette
.
absolute_url
(
'
layout
/
mozilla_mission
.
html
'
)
             
self
.
marionette
.
absolute_url
(
'
layout
/
mozilla_organizations
.
html
'
)
)
            
(
self
.
marionette
.
absolute_url
(
'
layout
/
mozilla_projects
.
html
'
)
             
self
.
marionette
.
absolute_url
(
'
layout
/
mozilla_mission
.
html
'
)
)
        
]
)
        
self
.
marionette
.
enforce_gecko_prefs
(
{
            
'
browser
.
startup
.
page
'
:
3
            
'
browser
.
sessionstore
.
restore_on_demand
'
:
False
            
'
browser
.
sessionstore
.
debug
.
no_auto_updates
'
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
restart
(
clean
=
True
)
        
finally
:
            
FirefoxTestCase
.
tearDown
(
self
)
    
def
test_with_variety
(
self
)
:
        
"
"
"
Opens
a
set
of
windows
both
standard
and
private
with
        
some
number
of
tabs
in
them
.
Once
the
tabs
have
loaded
restarts
        
the
browser
and
then
ensures
that
the
standard
tabs
have
been
        
restored
and
that
the
private
ones
have
not
.
        
"
"
"
        
self
.
open_windows
(
self
.
test_windows
)
        
self
.
open_windows
(
self
.
private_windows
is_private
=
True
)
        
self
.
restart
(
)
        
windows
=
self
.
windows
.
all
        
opened_windows
=
set
(
)
        
for
win
in
windows
:
            
urls
=
tuple
(
)
            
for
tab
in
win
.
tabbar
.
tabs
:
                
urls
=
urls
+
tuple
(
[
tab
.
location
]
)
            
opened_windows
.
add
(
urls
)
        
self
.
assertEqual
(
opened_windows
self
.
test_windows
)
    
def
open_windows
(
self
window_sets
is_private
=
False
)
:
        
"
"
"
Opens
a
set
of
windows
with
tabs
pointing
at
some
        
URLs
.
        
param
window_sets
(
list
)
               
A
set
of
URL
tuples
.
Each
tuple
within
window_sets
               
represents
a
window
and
each
URL
in
the
URL
               
tuples
represents
what
will
be
loaded
in
a
tab
.
               
Note
that
if
is_private
is
False
then
the
first
               
URL
tuple
will
be
opened
in
the
current
window
and
               
subequent
tuples
will
be
opened
in
new
windows
.
               
Example
:
               
set
(
                   
(
self
.
marionette
.
absolute_url
(
'
layout
/
mozilla_1
.
html
'
)
                    
self
.
marionette
.
absolute_url
(
'
layout
/
mozilla_2
.
html
'
)
)
                   
(
self
.
marionette
.
absolute_url
(
'
layout
/
mozilla_3
.
html
'
)
                    
self
.
marionette
.
absolute_url
(
'
layout
/
mozilla_4
.
html
'
)
)
               
)
               
This
would
take
the
currently
open
window
and
load
               
mozilla_1
.
html
and
mozilla_2
.
html
in
new
tabs
.
It
would
               
then
open
a
new
second
window
and
load
tabs
at
               
mozilla_3
.
html
and
mozilla_4
.
html
.
        
param
is_private
(
boolean
optional
)
               
Whether
or
not
any
new
windows
should
be
a
private
browsing
               
windows
.
        
"
"
"
        
if
(
is_private
)
:
            
win
=
self
.
browser
.
open_browser
(
is_private
=
True
)
            
win
.
switch_to
(
)
        
else
:
            
win
=
self
.
browser
        
for
index
urls
in
enumerate
(
window_sets
)
:
            
if
index
>
0
:
                
win
=
self
.
browser
.
open_browser
(
is_private
=
is_private
)
            
win
.
switch_to
(
)
            
self
.
open_tabs
(
win
urls
)
    
def
open_tabs
(
self
win
urls
)
:
        
"
"
"
Opens
a
set
of
URLs
inside
a
window
in
new
tabs
.
        
param
win
(
browser
window
)
               
The
browser
window
to
load
the
tabs
in
.
        
param
urls
(
tuple
)
               
A
tuple
of
URLs
to
load
in
this
window
.
The
               
first
URL
will
be
loaded
in
the
currently
selected
               
browser
tab
.
Subsequent
URLs
will
be
loaded
in
               
new
tabs
.
        
"
"
"
        
with
self
.
marionette
.
using_context
(
'
content
'
)
:
            
if
isinstance
(
urls
str
)
:
                
self
.
marionette
.
navigate
(
urls
)
            
else
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
                        
with
self
.
marionette
.
using_context
(
'
chrome
'
)
:
                            
win
.
tabbar
.
open_tab
(
)
                    
self
.
marionette
.
navigate
(
url
)
