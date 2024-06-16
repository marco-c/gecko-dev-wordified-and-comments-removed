import
json
import
os
from
marionette_harness
import
MarionetteTestCase
class
BackupTest
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
        
MarionetteTestCase
.
setUp
(
self
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
marionette
.
instance
.
prefs
=
{
            
"
browser
.
backup
.
log
"
:
True
        
}
        
self
.
marionette
.
instance
.
switch_profile
(
)
        
self
.
marionette
.
start_session
(
)
    
def
test_backup
(
self
)
:
        
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
        
resourceKeys
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
          
const
DefaultBackupResources
=
ChromeUtils
.
importESModule
(
"
resource
:
/
/
/
modules
/
backup
/
BackupResources
.
sys
.
mjs
"
)
;
          
let
resourceKeys
=
[
]
;
          
for
(
const
resourceName
in
DefaultBackupResources
)
{
            
let
resource
=
DefaultBackupResources
[
resourceName
]
;
            
resourceKeys
.
push
(
resource
.
key
)
;
          
}
          
return
resourceKeys
;
        
"
"
"
        
)
        
stagingPath
=
self
.
marionette
.
execute_async_script
(
            
"
"
"
          
const
{
BackupService
}
=
ChromeUtils
.
importESModule
(
"
resource
:
/
/
/
modules
/
backup
/
BackupService
.
sys
.
mjs
"
)
;
          
let
bs
=
BackupService
.
init
(
)
;
          
if
(
!
bs
)
{
            
throw
new
Error
(
"
Could
not
get
initialized
BackupService
.
"
)
;
          
}
          
let
[
outerResolve
]
=
arguments
;
          
(
async
(
)
=
>
{
            
let
{
stagingPath
}
=
await
bs
.
createBackup
(
)
;
            
if
(
!
stagingPath
)
{
              
throw
new
Error
(
"
Could
not
create
backup
.
"
)
;
            
}
            
return
stagingPath
;
          
}
)
(
)
.
then
(
outerResolve
)
;
        
"
"
"
        
)
        
self
.
assertTrue
(
os
.
path
.
exists
(
stagingPath
)
)
        
manifestPath
=
os
.
path
.
join
(
stagingPath
"
backup
-
manifest
.
json
"
)
        
self
.
assertTrue
(
os
.
path
.
exists
(
manifestPath
)
)
        
with
open
(
manifestPath
"
r
"
)
as
f
:
            
manifest
=
json
.
load
(
f
)
        
self
.
assertIn
(
"
resources
"
manifest
)
        
resources
=
manifest
[
"
resources
"
]
        
self
.
assertTrue
(
isinstance
(
resources
dict
)
)
        
self
.
assertTrue
(
len
(
resources
)
>
0
)
        
self
.
assertEqual
(
len
(
resources
)
len
(
resourceKeys
)
)
        
for
resourceKey
in
resourceKeys
:
            
self
.
assertIn
(
resourceKey
resources
)
        
for
resourceKey
in
resources
:
            
print
(
"
Checking
resource
:
%
s
"
%
resourceKey
)
            
resourceStagingDir
=
os
.
path
.
join
(
stagingPath
resourceKey
)
            
self
.
assertTrue
(
os
.
path
.
exists
(
resourceStagingDir
)
)
