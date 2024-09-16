from
marionette_harness
import
MarionetteTestCase
class
BounceTrackingStoragePersistenceTestCase
(
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
BounceTrackingStoragePersistenceTestCase
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
privacy
.
bounceTrackingProtection
.
enabled
"
:
True
                
"
privacy
.
bounceTrackingProtection
.
enableTestMode
"
:
True
            
}
        
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
populate_state
(
)
    
def
tearDown
(
self
)
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
        
super
(
BounceTrackingStoragePersistenceTestCase
self
)
.
tearDown
(
)
    
def
populate_state
(
self
)
:
        
self
.
marionette
.
execute_script
(
            
"
"
"
            
let
bounceTrackingProtection
=
Cc
[
"
mozilla
.
org
/
bounce
-
tracking
-
protection
;
1
"
]
.
getService
(
            
Ci
.
nsIBounceTrackingProtection
            
)
;
            
bounceTrackingProtection
.
testAddBounceTrackerCandidate
(
{
}
"
bouncetracker
.
net
"
Date
.
now
(
)
*
10000
)
;
            
bounceTrackingProtection
.
testAddBounceTrackerCandidate
(
{
}
"
bouncetracker
.
org
"
Date
.
now
(
)
*
10000
)
;
            
bounceTrackingProtection
.
testAddBounceTrackerCandidate
(
{
userContextId
:
3
}
"
tracker
.
com
"
Date
.
now
(
)
*
10000
)
;
            
/
/
A
private
browsing
entry
which
must
not
be
persisted
across
restarts
.
            
bounceTrackingProtection
.
testAddBounceTrackerCandidate
(
{
privateBrowsingId
:
1
}
"
tracker
.
net
"
Date
.
now
(
)
*
10000
)
;
            
bounceTrackingProtection
.
testAddUserActivation
(
{
}
"
example
.
com
"
(
Date
.
now
(
)
+
5000
)
*
10000
)
;
            
/
/
A
private
browsing
entry
which
must
not
be
persisted
across
restarts
.
            
bounceTrackingProtection
.
testAddUserActivation
(
{
privateBrowsingId
:
1
}
"
example
.
org
"
(
Date
.
now
(
)
+
2000
)
*
10000
)
;
            
"
"
"
        
)
    
def
test_state_after_restart
(
self
)
:
        
self
.
marionette
.
restart
(
clean
=
False
in_app
=
True
)
        
bounceTrackerCandidates
=
self
.
marionette
.
execute_script
(
            
"
"
"
                
let
bounceTrackingProtection
=
Cc
[
"
mozilla
.
org
/
bounce
-
tracking
-
protection
;
1
"
]
.
getService
(
                
Ci
.
nsIBounceTrackingProtection
                
)
;
                
return
bounceTrackingProtection
.
testGetBounceTrackerCandidateHosts
(
{
}
)
.
map
(
entry
=
>
entry
.
siteHost
)
.
sort
(
)
;
            
"
"
"
        
)
        
self
.
assertEqual
(
            
len
(
bounceTrackerCandidates
)
            
2
            
msg
=
"
There
should
be
two
entries
for
default
OA
"
        
)
        
self
.
assertEqual
(
bounceTrackerCandidates
[
0
]
"
bouncetracker
.
net
"
)
        
self
.
assertEqual
(
bounceTrackerCandidates
[
1
]
"
bouncetracker
.
org
"
)
        
bounceTrackerCandidates
=
self
.
marionette
.
execute_script
(
            
"
"
"
                
let
bounceTrackingProtection
=
Cc
[
"
mozilla
.
org
/
bounce
-
tracking
-
protection
;
1
"
]
.
getService
(
                
Ci
.
nsIBounceTrackingProtection
                
)
;
                
return
bounceTrackingProtection
.
testGetBounceTrackerCandidateHosts
(
{
userContextId
:
3
}
)
.
map
(
entry
=
>
entry
.
siteHost
)
.
sort
(
)
;
            
"
"
"
        
)
        
self
.
assertEqual
(
            
len
(
bounceTrackerCandidates
)
            
1
            
msg
=
"
There
should
be
only
one
entry
for
user
context
3
"
        
)
        
self
.
assertEqual
(
bounceTrackerCandidates
[
0
]
"
tracker
.
com
"
)
        
bounceTrackerCandidates
=
self
.
marionette
.
execute_script
(
            
"
"
"
                
let
bounceTrackingProtection
=
Cc
[
"
mozilla
.
org
/
bounce
-
tracking
-
protection
;
1
"
]
.
getService
(
                
Ci
.
nsIBounceTrackingProtection
                
)
;
                
return
bounceTrackingProtection
.
testGetBounceTrackerCandidateHosts
(
{
userContextId
:
4
}
)
.
length
;
            
"
"
"
        
)
        
self
.
assertEqual
(
            
bounceTrackerCandidates
            
0
            
msg
=
"
There
should
be
no
entries
for
user
context
4
"
        
)
        
bounceTrackerCandidates
=
self
.
marionette
.
execute_script
(
            
"
"
"
                
let
bounceTrackingProtection
=
Cc
[
"
mozilla
.
org
/
bounce
-
tracking
-
protection
;
1
"
]
.
getService
(
                
Ci
.
nsIBounceTrackingProtection
                
)
;
                
return
bounceTrackingProtection
.
testGetBounceTrackerCandidateHosts
(
{
privateBrowsingId
:
1
}
)
.
length
;
            
"
"
"
        
)
        
self
.
assertEqual
(
            
bounceTrackerCandidates
            
0
            
msg
=
"
There
should
be
no
entries
for
private
browsing
"
        
)
        
userActivations
=
self
.
marionette
.
execute_script
(
            
"
"
"
                
let
bounceTrackingProtection
=
Cc
[
"
mozilla
.
org
/
bounce
-
tracking
-
protection
;
1
"
]
.
getService
(
                
Ci
.
nsIBounceTrackingProtection
                
)
;
                
return
bounceTrackingProtection
.
testGetUserActivationHosts
(
{
}
)
.
map
(
entry
=
>
entry
.
siteHost
)
.
sort
(
)
;
            
"
"
"
        
)
        
self
.
assertEqual
(
            
len
(
userActivations
)
            
1
            
msg
=
"
There
should
be
only
one
entry
for
user
activation
"
        
)
        
self
.
assertEqual
(
userActivations
[
0
]
"
example
.
com
"
)
        
userActivations
=
self
.
marionette
.
execute_script
(
            
"
"
"
                
let
bounceTrackingProtection
=
Cc
[
"
mozilla
.
org
/
bounce
-
tracking
-
protection
;
1
"
]
.
getService
(
                
Ci
.
nsIBounceTrackingProtection
                
)
;
                
return
bounceTrackingProtection
.
testGetUserActivationHosts
(
{
privateBrowsingId
:
1
}
)
.
length
;
            
"
"
"
        
)
        
self
.
assertEqual
(
            
userActivations
0
msg
=
"
There
should
be
no
entries
for
private
browsing
"
        
)
