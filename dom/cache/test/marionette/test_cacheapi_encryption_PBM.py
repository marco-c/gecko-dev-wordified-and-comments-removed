import
os
import
re
import
sys
from
pathlib
import
Path
sys
.
path
.
append
(
os
.
fspath
(
Path
(
__file__
)
.
parents
[
3
]
/
"
quota
/
test
/
marionette
"
)
)
from
quota_test_case
import
QuotaTestCase
CACHEAPI_PBM_PREF
=
"
dom
.
cache
.
privateBrowsing
.
enabled
"
QM_TESTING_PREF
=
"
dom
.
quotaManager
.
testing
"
class
CacheAPIEncryptionPBM
(
QuotaTestCase
)
:
    
"
"
"
    
Bug1856953
:
Ensure
CacheAPI
data
gets
encrypted
in
Private
Browsing
Mode
.
    
We
need
to
ensure
data
inside
both
sqlite
fields
and
request
/
response
files
    
gets
encrypted
    
"
"
"
    
def
setUp
(
self
)
:
        
super
(
CacheAPIEncryptionPBM
self
)
.
setUp
(
)
        
self
.
cacheName
=
"
CachePBMTest
"
        
self
.
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
        
self
.
cacheAPIStoragePath
=
None
        
self
.
defaultCacheAPIPBMPref
=
self
.
marionette
.
get_pref
(
CACHEAPI_PBM_PREF
)
        
self
.
marionette
.
set_pref
(
CACHEAPI_PBM_PREF
True
)
        
self
.
defaultQMPrefValue
=
self
.
marionette
.
get_pref
(
QM_TESTING_PREF
)
        
self
.
marionette
.
set_pref
(
QM_TESTING_PREF
True
)
        
self
.
cacheRequestStr
=
"
https
:
/
/
example
.
com
/
"
        
self
.
cacheResponseStr
=
"
CacheAPIEncryptionPBM
"
        
self
.
cacheDBFileName
=
"
caches
.
sqlite
"
        
self
.
cacheDBJournalFileName
=
"
caches
.
sqlite
-
wal
"
        
self
.
dbCheckpointThresholdBytes
=
512
*
1024
        
pbmWindowHandle
=
self
.
marionette
.
open
(
type
=
"
window
"
private
=
True
)
[
"
handle
"
]
        
self
.
marionette
.
switch_to_window
(
pbmWindowHandle
)
        
self
.
marionette
.
navigate
(
            
self
.
marionette
.
absolute_url
(
"
dom
/
cache
/
basicCacheAPI_PBM
.
html
"
)
        
)
        
self
.
origin
=
self
.
marionette
.
absolute_url
(
"
"
)
[
:
-
1
]
+
"
^
privateBrowsingId
=
1
"
    
def
tearDown
(
self
)
:
        
super
(
CacheAPIEncryptionPBM
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
set_pref
(
CACHEAPI_PBM_PREF
self
.
defaultCacheAPIPBMPref
)
        
self
.
marionette
.
set_pref
(
QM_TESTING_PREF
self
.
defaultQMPrefValue
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
wrappedJSObject
.
releaseCache
(
)
"
)
        
self
.
marionette
.
close
(
)
    
def
test_ensure_encrypted_request_response
(
self
)
:
        
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
[
name
requestStr
responseStr
resolve
]
=
arguments
;
                
const
request
=
new
Request
(
requestStr
)
;
                
const
response
=
new
Response
(
responseStr
)
;
                
window
.
wrappedJSObject
.
addDataIntoCache
(
name
request
response
)
                                      
.
then
(
(
)
=
>
{
resolve
(
)
;
}
)
;
            
"
"
"
            
script_args
=
(
self
.
cacheName
self
.
cacheRequestStr
self
.
cacheResponseStr
)
        
)
        
self
.
ensureInvariantHolds
(
            
lambda
_
:
os
.
path
.
exists
(
self
.
getCacheAPIStoragePath
(
)
)
        
)
        
self
.
ensureSqliteIsEncrypted
(
)
        
self
.
ensureInvariantHolds
(
            
lambda
_
:
self
.
findDirObj
(
self
.
cacheAPIStoragePath
"
morgue
"
False
)
            
is
not
None
        
)
        
cacheResponseDir
=
self
.
findDirObj
(
self
.
cacheAPIStoragePath
"
morgue
"
False
)
        
self
.
ensureInvariantHolds
(
lambda
_
:
any
(
os
.
listdir
(
cacheResponseDir
)
)
)
        
cacheResponseBodiesPath
=
[
            
d
for
d
in
Path
(
cacheResponseDir
)
.
iterdir
(
)
if
d
.
is_dir
(
)
        
]
[
0
]
        
self
.
ensureInvariantHolds
(
            
lambda
_
:
self
.
findDirObj
(
cacheResponseBodiesPath
"
.
final
"
True
)
            
is
not
None
        
)
        
cacheResponseBodyPath
=
self
.
findDirObj
(
cacheResponseBodiesPath
"
.
final
"
True
)
        
foundRawValue
=
False
        
with
open
(
cacheResponseBodyPath
"
rb
"
)
as
f_binary
:
            
foundRawValue
=
re
.
search
(
b
"
sNaPpY
"
f_binary
.
read
(
)
)
is
not
None
        
self
.
assertFalse
(
foundRawValue
"
Response
body
did
not
get
encrypted
"
)
    
def
ensureSqliteIsEncrypted
(
self
)
:
        
self
.
ensureInvariantHolds
(
            
lambda
_
:
self
.
findDirObj
(
                
self
.
cacheAPIStoragePath
self
.
cacheDBJournalFileName
True
            
)
            
is
not
None
        
)
        
dbJournalFile
=
self
.
findDirObj
(
            
self
.
cacheAPIStoragePath
self
.
cacheDBJournalFileName
True
        
)
        
self
.
ensureInvariantHolds
(
            
lambda
_
:
self
.
findDirObj
(
                
self
.
cacheAPIStoragePath
self
.
cacheDBFileName
True
            
)
            
is
not
None
        
)
        
dbFile
=
self
.
findDirObj
(
self
.
cacheAPIStoragePath
self
.
cacheDBFileName
True
)
        
self
.
assertTrue
(
            
os
.
path
.
getsize
(
dbJournalFile
)
<
self
.
dbCheckpointThresholdBytes
        
)
        
self
.
assertTrue
(
os
.
path
.
getsize
(
dbJournalFile
)
>
os
.
path
.
getsize
(
dbFile
)
)
        
self
.
assertFalse
(
            
self
.
cacheRequestStr
.
encode
(
"
ascii
"
)
in
open
(
dbJournalFile
"
rb
"
)
.
read
(
)
            
"
Sqlite
journal
file
did
not
get
encrypted
"
        
)
        
self
.
assertTrue
(
self
.
resetStoragesForPrincipal
(
self
.
origin
"
private
"
"
cache
"
)
)
        
self
.
assertFalse
(
os
.
path
.
getsize
(
dbJournalFile
)
>
os
.
path
.
getsize
(
dbFile
)
)
        
self
.
assertFalse
(
            
self
.
cacheRequestStr
.
encode
(
"
ascii
"
)
in
open
(
dbFile
"
rb
"
)
.
read
(
)
            
"
Sqlite
main
db
file
did
not
get
encrypted
"
        
)
    
def
getCacheAPIStoragePath
(
self
)
:
        
if
self
.
cacheAPIStoragePath
is
not
None
:
            
return
self
.
cacheAPIStoragePath
        
self
.
cacheAPIStoragePath
=
self
.
getStoragePath
(
            
self
.
profilePath
self
.
origin
"
private
"
"
cache
"
        
)
        
print
(
"
cacheAPI
origin
directory
=
"
+
self
.
cacheAPIStoragePath
)
        
return
self
.
cacheAPIStoragePath
