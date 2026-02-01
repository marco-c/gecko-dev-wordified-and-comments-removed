import
os
import
shutil
import
tempfile
import
mozfile
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
    
_cert_db_key
=
"
AAAAAAAAAAAAAAAUAAAAG0Wbze8lahTcE4RhwEqMtTpThrzjMBkxFzAVBgNVBAMMDiBIVFRQMiBUZXN0IENB
"
    
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
enforce_gecko_prefs
(
{
            
"
browser
.
backup
.
enabled
"
:
True
            
"
browser
.
backup
.
log
"
:
True
            
"
browser
.
backup
.
archive
.
enabled
"
:
True
            
"
browser
.
backup
.
restore
.
enabled
"
:
True
            
"
browser
.
backup
.
archive
.
overridePlatformCheck
"
:
True
            
"
browser
.
backup
.
restore
.
overridePlatformCheck
"
:
True
            
"
browser
.
sessionstore
.
resume_from_crash
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
quit
(
)
        
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
        
MarionetteTestCase
.
tearDown
(
self
)
    
def
test_backup
(
self
)
:
        
self
.
add_test_cookie
(
)
        
self
.
add_test_login
(
)
        
self
.
add_test_certificate
(
)
        
self
.
add_test_saved_address
(
)
        
self
.
add_test_identity_credential
(
)
        
self
.
add_test_form_history
(
)
        
self
.
add_test_asrouter_snippets_data
(
)
        
self
.
add_test_protections_data
(
)
        
self
.
add_test_bookmarks
(
)
        
self
.
add_test_history
(
)
        
self
.
add_test_preferences
(
)
        
self
.
add_test_permissions
(
)
        
backupOSKeyStoreLabel
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
{
OSKeyStore
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
gre
/
modules
/
OSKeyStore
.
sys
.
mjs
"
          
)
;
          
const
BACKUP_OSKEYSTORE_LABEL
=
"
test
-
"
+
Math
.
random
(
)
.
toString
(
36
)
.
substr
(
2
)
;
          
OSKeyStore
.
STORE_LABEL
=
BACKUP_OSKEYSTORE_LABEL
;
          
return
BACKUP_OSKEYSTORE_LABEL
;
        
"
"
"
        
)
        
self
.
add_test_payment_methods
(
)
        
self
.
marionette
.
restart
(
)
        
self
.
add_test_sessionstore
(
)
        
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
{
OSKeyStore
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
gre
/
modules
/
OSKeyStore
.
sys
.
mjs
"
          
)
;
          
const
BACKUP_OSKEYSTORE_LABEL
=
arguments
[
0
]
;
          
OSKeyStore
.
STORE_LABEL
=
BACKUP_OSKEYSTORE_LABEL
;
        
"
"
"
            
script_args
=
[
backupOSKeyStoreLabel
]
        
)
        
archiveDestPath
=
os
.
path
.
join
(
tempfile
.
gettempdir
(
)
"
backup
-
dest
"
)
        
recoveryCode
=
"
This
is
a
test
password
"
        
archivePath
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
archiveDestPath
recoveryCode
outerResolve
]
=
arguments
;
          
bs
.
setParentDirPath
(
archiveDestPath
)
;
          
(
async
(
)
=
>
{
            
await
bs
.
enableEncryption
(
recoveryCode
)
;
            
let
{
archivePath
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
archivePath
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
archivePath
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
            
script_args
=
[
archiveDestPath
recoveryCode
]
        
)
        
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
OSKeyStore
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
gre
/
modules
/
OSKeyStore
.
sys
.
mjs
"
           
)
;
           
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
              
await
OSKeyStore
.
cleanup
(
)
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
        
recoveryPath
=
os
.
path
.
join
(
tempfile
.
gettempdir
(
)
"
recovery
"
)
        
shutil
.
rmtree
(
recoveryPath
ignore_errors
=
True
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
        
[
            
newProfileName
            
newProfilePath
            
intermediateClientID
            
osKeyStoreLabel
        
]
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
OSKeyStore
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
gre
/
modules
/
OSKeyStore
.
sys
.
mjs
"
)
;
          
const
{
ClientID
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
gre
/
modules
/
ClientID
.
sys
.
mjs
"
)
;
          
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
get
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
archivePath
recoveryCode
recoveryPath
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
newProfileRootPath
=
await
IOUtils
.
createUniqueDirectory
(
              
PathUtils
.
tempDir
              
"
recoverFromBackupArchiveTest
-
newProfileRoot
"
            
)
;
            
/
/
This
is
some
hackery
to
make
it
so
that
OSKeyStore
doesn
'
t
kick
            
/
/
off
an
OS
authentication
dialog
in
our
test
and
also
to
make
            
/
/
sure
we
don
'
t
blow
away
the
_real_
OSKeyStore
key
for
the
browser
            
/
/
on
the
system
that
this
test
is
running
on
.
Normally
I
'
d
use
            
/
/
OSKeyStoreTestUtils
.
setup
to
do
this
but
apparently
the
            
/
/
testing
-
common
modules
aren
'
t
available
in
Marionette
tests
.
            
const
ORIGINAL_STORE_LABEL
=
OSKeyStore
.
STORE_LABEL
;
            
OSKeyStore
.
STORE_LABEL
=
"
test
-
"
+
Math
.
random
(
)
.
toString
(
36
)
.
substr
(
2
)
;
            
let
newProfile
=
await
bs
.
recoverFromBackupArchive
(
archivePath
recoveryCode
false
recoveryPath
newProfileRootPath
)
;
            
if
(
!
newProfile
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
recovery
profile
.
"
)
;
            
}
            
let
intermediateClientID
=
await
ClientID
.
getClientID
(
)
;
            
return
[
newProfile
.
name
newProfile
.
rootDir
.
path
intermediateClientID
OSKeyStore
.
STORE_LABEL
]
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
            
script_args
=
[
archivePath
recoveryCode
recoveryPath
]
        
)
        
print
(
f
"
Recovery
name
:
{
newProfileName
}
"
)
        
print
(
f
"
Recovery
path
:
{
newProfilePath
}
"
)
        
print
(
f
"
Intermediate
clientID
:
{
intermediateClientID
}
"
)
        
print
(
f
"
Persisting
fake
OSKeyStore
label
:
{
osKeyStoreLabel
}
"
)
        
self
.
marionette
.
quit
(
)
        
originalProfile
=
self
.
marionette
.
instance
.
profile
        
self
.
marionette
.
instance
.
profile
=
newProfilePath
        
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
        
encryptionEnabled
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
get
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
            
await
bs
.
postRecoveryComplete
;
            
await
bs
.
loadEncryptionState
(
)
;
            
return
bs
.
state
.
encryptionEnabled
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
encryptionEnabled
)
        
self
.
verify_recovered_test_cookie
(
)
        
self
.
verify_recovered_test_login
(
)
        
self
.
verify_recovered_test_certificate
(
)
        
self
.
verify_recovered_saved_address
(
)
        
self
.
verify_recovered_identity_credential
(
)
        
self
.
verify_recovered_form_history
(
)
        
self
.
verify_recovered_asrouter_snippets_data
(
)
        
self
.
verify_recovered_protections_data
(
)
        
self
.
verify_recovered_bookmarks
(
)
        
self
.
verify_recovered_history
(
)
        
self
.
verify_recovered_preferences
(
)
        
self
.
verify_recovered_permissions
(
)
        
self
.
verify_recovered_payment_methods
(
osKeyStoreLabel
)
        
self
.
verify_recovered_sessionstore
(
)
        
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
OSKeyStore
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
gre
/
modules
/
OSKeyStore
.
sys
.
mjs
"
)
;
          
let
[
osKeyStoreLabel
outerResolve
]
=
arguments
;
          
OSKeyStore
.
STORE_LABEL
=
osKeyStoreLabel
;
          
(
async
(
)
=
>
{
            
await
OSKeyStore
.
cleanup
(
)
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
            
script_args
=
[
osKeyStoreLabel
]
        
)
        
recoveredClientID
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
ClientID
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
gre
/
modules
/
ClientID
.
sys
.
mjs
"
)
;
          
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
            
return
ClientID
.
getClientID
(
)
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
assertNotEqual
(
recoveredClientID
intermediateClientID
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
profile
=
originalProfile
        
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
execute_async_script
(
            
"
"
"
          
let
[
newProfileName
outerResolve
]
=
arguments
;
          
let
profileSvc
=
Cc
[
"
mozilla
.
org
/
toolkit
/
profile
-
service
;
1
"
]
.
getService
(
            
Ci
.
nsIToolkitProfileService
          
)
;
          
let
profile
=
profileSvc
.
getProfileByName
(
newProfileName
)
;
          
profile
.
remove
(
true
)
;
          
profileSvc
.
asyncFlush
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
            
script_args
=
[
newProfileName
]
        
)
        
mozfile
.
remove
(
archivePath
)
        
mozfile
.
remove
(
recoveryPath
)
    
def
test_backup_disablement_in_new_session
(
self
)
:
        
archiveDestPath
=
os
.
path
.
join
(
            
tempfile
.
gettempdir
(
)
"
backup
-
dest
-
disable
-
test
"
        
)
        
[
archivePath
lastBackupFileName
]
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
archiveDestPath
outerResolve
]
=
arguments
;
          
bs
.
setParentDirPath
(
archiveDestPath
)
;
          
(
async
(
)
=
>
{
            
bs
.
setScheduledBackups
(
true
)
;
            
let
{
archivePath
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
archivePath
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
            
let
lastBackupFileName
=
Services
.
prefs
.
getStringPref
(
"
browser
.
backup
.
scheduled
.
last
-
backup
-
file
"
"
"
)
;
            
return
[
archivePath
lastBackupFileName
]
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
            
script_args
=
[
archiveDestPath
]
        
)
        
print
(
f
"
Created
backup
at
:
{
archivePath
}
"
)
        
print
(
f
"
Last
backup
filename
:
{
lastBackupFileName
}
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
        
if
os
.
path
.
exists
(
archivePath
)
:
            
print
(
f
"
File
size
:
{
os
.
path
.
getsize
(
archivePath
)
}
bytes
"
)
        
self
.
marionette
.
execute_async_script
(
            
"
"
"
          
ChromeUtils
.
defineESModuleGetters
(
this
{
            
BackupService
:
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
            
ASRouterTargeting
:
"
resource
:
/
/
/
modules
/
asrouter
/
ASRouterTargeting
.
sys
.
mjs
"
          
}
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
            
await
ASRouterTargeting
.
Environment
.
backupsInfo
;
            
await
bs
.
cleanupBackupFiles
(
)
;
            
bs
.
setScheduledBackups
(
false
)
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
            
script_args
=
[
]
        
)
        
archiveDeletedAfterDisable
=
not
os
.
path
.
exists
(
archivePath
)
        
self
.
assertTrue
(
            
archiveDeletedAfterDisable
            
f
"
Backup
file
should
be
deleted
after
disabling
backups
.
Path
:
{
archivePath
}
exists
:
{
os
.
path
.
exists
(
archivePath
)
}
"
        
)
    
def
add_test_cookie
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
            
/
/
We
'
ll
just
add
a
single
cookie
and
then
make
sure
that
it
shows
            
/
/
up
on
the
other
side
.
            
Services
.
cookies
.
removeAll
(
)
;
            
Services
.
cookies
.
add
(
              
"
.
example
.
com
"
              
"
/
"
              
"
first
"
              
"
one
"
              
false
              
false
              
false
              
Date
.
now
(
)
+
1000
              
{
}
              
Ci
.
nsICookie
.
SAMESITE_UNSET
              
Ci
.
nsICookie
.
SCHEME_HTTP
            
)
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
    
def
verify_recovered_test_cookie
(
self
)
:
        
cookiesLength
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
cookies
=
Services
.
cookies
.
getCookiesFromHost
(
"
example
.
com
"
{
}
)
;
            
return
cookies
.
length
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
assertEqual
(
cookiesLength
0
)
    
def
add_test_login
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
            
/
/
Let
'
s
start
with
adding
a
single
password
            
Services
.
logins
.
removeAllLogins
(
)
;
            
const
nsLoginInfo
=
new
Components
.
Constructor
(
              
"
mozilla
.
org
/
login
-
manager
/
loginInfo
;
1
"
              
Ci
.
nsILoginInfo
              
"
init
"
            
)
;
            
const
login1
=
new
nsLoginInfo
(
              
"
https
:
/
/
example
.
com
"
              
"
https
:
/
/
example
.
com
"
              
null
              
"
notifyu1
"
              
"
notifyp1
"
              
"
user
"
              
"
pass
"
            
)
;
            
await
Services
.
logins
.
addLoginAsync
(
login1
)
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
    
def
verify_recovered_test_login
(
self
)
:
        
loginsLength
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
logins
=
await
Services
.
logins
.
searchLoginsAsync
(
{
              
origin
:
"
https
:
/
/
example
.
com
"
            
}
)
;
            
return
logins
.
length
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
assertEqual
(
loginsLength
1
)
    
def
add_test_certificate
(
self
)
:
        
certPath
=
os
.
path
.
join
(
os
.
path
.
dirname
(
__file__
)
"
http2
-
ca
.
pem
"
)
        
self
.
marionette
.
execute_async_script
(
            
"
"
"
          
let
[
certPath
certDbKey
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
            
const
{
NetUtil
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
gre
/
modules
/
NetUtil
.
sys
.
mjs
"
            
)
;
            
let
certDb
=
Cc
[
"
mozilla
.
org
/
security
/
x509certdb
;
1
"
]
.
getService
(
              
Ci
.
nsIX509CertDB
            
)
;
            
if
(
certDb
.
findCertByDBKey
(
certDbKey
)
)
{
              
throw
new
Error
(
"
Should
not
have
this
certificate
yet
!
"
)
;
            
}
            
let
certFile
=
await
IOUtils
.
getFile
(
certPath
)
;
            
let
fstream
=
Cc
[
"
mozilla
.
org
/
network
/
file
-
input
-
stream
;
1
"
]
.
createInstance
(
              
Ci
.
nsIFileInputStream
            
)
;
            
fstream
.
init
(
certFile
-
1
0
0
)
;
            
let
data
=
NetUtil
.
readInputStreamToString
(
fstream
fstream
.
available
(
)
)
;
            
fstream
.
close
(
)
;
            
let
pem
=
data
.
replace
(
/
-
-
-
-
-
BEGIN
CERTIFICATE
-
-
-
-
-
/
"
"
)
                          
.
replace
(
/
-
-
-
-
-
END
CERTIFICATE
-
-
-
-
-
/
"
"
)
                          
.
replace
(
/
[
\
\
r
\
\
n
]
/
g
"
"
)
;
            
let
cert
=
certDb
.
addCertFromBase64
(
pem
"
CTu
u
u
"
)
;
            
if
(
cert
.
dbKey
!
=
certDbKey
)
{
              
throw
new
Error
(
"
The
inserted
certificate
DB
key
is
unexpected
.
"
)
;
            
}
          
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
            
script_args
=
[
certPath
self
.
_cert_db_key
]
        
)
    
def
verify_recovered_test_certificate
(
self
)
:
        
certExists
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
          
let
[
certDbKey
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
certDb
=
Cc
[
"
mozilla
.
org
/
security
/
x509certdb
;
1
"
]
.
getService
(
              
Ci
.
nsIX509CertDB
            
)
;
            
return
certDb
.
findCertByDBKey
(
certDbKey
)
!
=
null
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
            
script_args
=
[
self
.
_cert_db_key
]
        
)
        
self
.
assertTrue
(
certExists
)
    
def
add_test_saved_address
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
{
formAutofillStorage
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
autofill
/
FormAutofillStorage
.
sys
.
mjs
"
          
)
;
          
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
            
const
TEST_ADDRESS_1
=
{
              
"
given
-
name
"
:
"
John
"
              
"
additional
-
name
"
:
"
R
.
"
              
"
family
-
name
"
:
"
Smith
"
              
organization
:
"
World
Wide
Web
Consortium
"
              
"
street
-
address
"
:
"
32
Vassar
Street
\
\
\
nMIT
Room
32
-
G524
"
              
"
address
-
level2
"
:
"
Cambridge
"
              
"
address
-
level1
"
:
"
MA
"
              
"
postal
-
code
"
:
"
02139
"
              
country
:
"
US
"
              
tel
:
"
+
15195555555
"
              
email
:
"
user
example
.
com
"
            
}
;
            
await
formAutofillStorage
.
initialize
(
)
;
            
formAutofillStorage
.
addresses
.
removeAll
(
)
;
            
await
formAutofillStorage
.
addresses
.
add
(
TEST_ADDRESS_1
)
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
    
def
verify_recovered_saved_address
(
self
)
:
        
addressesLength
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
formAutofillStorage
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
autofill
/
FormAutofillStorage
.
sys
.
mjs
"
          
)
;
          
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
            
await
formAutofillStorage
.
initialize
(
)
;
            
let
addresses
=
await
formAutofillStorage
.
addresses
.
getAll
(
)
;
            
return
addresses
.
length
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
assertEqual
(
addressesLength
1
)
    
def
add_test_identity_credential
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
service
=
Cc
[
"
mozilla
.
org
/
browser
/
identity
-
credential
-
storage
-
service
;
1
"
]
                            
.
getService
(
Ci
.
nsIIdentityCredentialStorageService
)
;
            
service
.
clear
(
)
;
            
let
testPrincipal
=
Services
.
scriptSecurityManager
.
createContentPrincipal
(
              
Services
.
io
.
newURI
(
"
https
:
/
/
test
.
com
/
"
)
              
{
}
            
)
;
            
let
idpPrincipal
=
Services
.
scriptSecurityManager
.
createContentPrincipal
(
              
Services
.
io
.
newURI
(
"
https
:
/
/
idp
-
test
.
com
/
"
)
              
{
}
            
)
;
            
service
.
setState
(
              
testPrincipal
              
idpPrincipal
              
"
ID
"
              
true
              
true
            
)
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
    
def
verify_recovered_identity_credential
(
self
)
:
        
[
registered
allowLogout
]
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
service
=
Cc
[
"
mozilla
.
org
/
browser
/
identity
-
credential
-
storage
-
service
;
1
"
]
                            
.
getService
(
Ci
.
nsIIdentityCredentialStorageService
)
;
            
let
testPrincipal
=
Services
.
scriptSecurityManager
.
createContentPrincipal
(
              
Services
.
io
.
newURI
(
"
https
:
/
/
test
.
com
/
"
)
              
{
}
            
)
;
            
let
idpPrincipal
=
Services
.
scriptSecurityManager
.
createContentPrincipal
(
              
Services
.
io
.
newURI
(
"
https
:
/
/
idp
-
test
.
com
/
"
)
              
{
}
            
)
;
            
let
registered
=
{
}
;
            
let
allowLogout
=
{
}
;
            
service
.
getState
(
              
testPrincipal
              
idpPrincipal
              
"
ID
"
              
registered
              
allowLogout
            
)
;
            
return
[
registered
.
value
allowLogout
.
value
]
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
registered
)
        
self
.
assertTrue
(
allowLogout
)
    
def
add_test_form_history
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
{
FormHistory
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
gre
/
modules
/
FormHistory
.
sys
.
mjs
"
          
)
;
          
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
            
await
FormHistory
.
update
(
{
              
op
:
"
add
"
              
fieldname
:
"
some
-
test
-
field
"
              
value
:
"
I
was
recovered
!
"
              
timesUsed
:
1
              
firstUsed
:
0
              
lastUsed
:
0
            
}
)
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
    
def
verify_recovered_form_history
(
self
)
:
        
formHistoryResultsLength
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
FormHistory
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
gre
/
modules
/
FormHistory
.
sys
.
mjs
"
          
)
;
          
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
results
=
await
FormHistory
.
search
(
              
[
"
guid
"
]
              
{
fieldname
:
"
some
-
test
-
field
"
}
            
)
;
            
return
results
.
length
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
assertEqual
(
formHistoryResultsLength
1
)
    
def
add_test_asrouter_snippets_data
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
{
ASRouterStorage
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
asrouter
/
ASRouterStorage
.
sys
.
mjs
"
          
)
;
          
const
SNIPPETS_TABLE_NAME
=
"
snippets
"
;
          
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
storage
=
new
ASRouterStorage
(
{
              
storeNames
:
[
SNIPPETS_TABLE_NAME
]
            
}
)
;
            
let
snippetsTable
=
await
storage
.
getDbTable
(
SNIPPETS_TABLE_NAME
)
;
            
await
snippetsTable
.
set
(
"
backup
-
test
"
"
some
-
test
-
value
"
)
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
    
def
verify_recovered_asrouter_snippets_data
(
self
)
:
        
snippetsResult
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
ASRouterStorage
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
asrouter
/
ASRouterStorage
.
sys
.
mjs
"
          
)
;
          
const
SNIPPETS_TABLE_NAME
=
"
snippets
"
;
          
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
storage
=
new
ASRouterStorage
(
{
              
storeNames
:
[
SNIPPETS_TABLE_NAME
]
            
}
)
;
            
let
snippetsTable
=
await
storage
.
getDbTable
(
SNIPPETS_TABLE_NAME
)
;
            
return
await
snippetsTable
.
get
(
"
backup
-
test
"
)
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
assertEqual
(
snippetsResult
"
some
-
test
-
value
"
)
    
def
add_test_protections_data
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
TrackingDBService
=
Cc
[
"
mozilla
.
org
/
tracking
-
db
-
service
;
1
"
]
                                      
.
getService
(
Ci
.
nsITrackingDBService
)
;
          
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
entry
=
{
              
"
https
:
/
/
test
.
com
"
:
[
                
[
Ci
.
nsIWebProgressListener
.
STATE_BLOCKED_TRACKING_CONTENT
true
1
]
              
]
            
}
;
            
await
TrackingDBService
.
clearAll
(
)
;
            
await
TrackingDBService
.
saveEvents
(
JSON
.
stringify
(
entry
)
)
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
    
def
verify_recovered_protections_data
(
self
)
:
        
eventsSum
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
TrackingDBService
=
Cc
[
"
mozilla
.
org
/
tracking
-
db
-
service
;
1
"
]
                                      
.
getService
(
Ci
.
nsITrackingDBService
)
;
          
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
            
return
TrackingDBService
.
sumAllEvents
(
)
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
assertEqual
(
eventsSum
1
)
    
def
add_test_bookmarks
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
{
PlacesUtils
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
gre
/
modules
/
PlacesUtils
.
sys
.
mjs
"
          
)
;
          
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
            
await
PlacesUtils
.
bookmarks
.
eraseEverything
(
)
;
            
await
PlacesUtils
.
bookmarks
.
insert
(
{
              
parentGuid
:
PlacesUtils
.
bookmarks
.
toolbarGuid
              
title
:
"
Some
test
page
"
              
url
:
Services
.
io
.
newURI
(
"
https
:
/
/
www
.
backup
.
test
/
"
)
            
}
)
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
    
def
verify_recovered_bookmarks
(
self
)
:
        
bookmarkExists
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
PlacesUtils
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
gre
/
modules
/
PlacesUtils
.
sys
.
mjs
"
          
)
;
          
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
url
=
Services
.
io
.
newURI
(
"
https
:
/
/
www
.
backup
.
test
/
"
)
;
            
let
bookmark
=
await
PlacesUtils
.
bookmarks
.
fetch
(
{
url
}
)
;
            
return
bookmark
!
=
null
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
bookmarkExists
)
    
def
add_test_history
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
{
PlacesUtils
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
gre
/
modules
/
PlacesUtils
.
sys
.
mjs
"
          
)
;
          
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
            
await
PlacesUtils
.
history
.
clear
(
)
;
            
let
entry
=
{
              
url
:
"
http
:
/
/
my
-
restored
-
history
.
com
"
              
visits
:
[
{
transition
:
PlacesUtils
.
history
.
TRANSITION_LINK
}
]
            
}
;
            
await
PlacesUtils
.
history
.
insertMany
(
[
entry
]
)
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
    
def
verify_recovered_history
(
self
)
:
        
historyExists
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
PlacesUtils
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
gre
/
modules
/
PlacesUtils
.
sys
.
mjs
"
          
)
;
          
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
entry
=
await
PlacesUtils
.
history
.
fetch
(
"
http
:
/
/
my
-
restored
-
history
.
com
"
)
;
            
return
entry
!
=
null
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
historyExists
)
    
def
add_test_preferences
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
          
Services
.
prefs
.
setBoolPref
(
"
test
-
pref
-
for
-
backup
"
true
)
        
"
"
"
        
)
    
def
verify_recovered_preferences
(
self
)
:
        
prefExists
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
          
return
Services
.
prefs
.
getBoolPref
(
"
test
-
pref
-
for
-
backup
"
false
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
prefExists
)
    
def
add_test_permissions
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
principal
=
Services
.
scriptSecurityManager
.
createContentPrincipalFromOrigin
(
            
"
https
:
/
/
test
-
permission
-
site
.
com
"
          
)
;
          
Services
.
perms
.
addFromPrincipal
(
            
principal
            
"
desktop
-
notification
"
            
Services
.
perms
.
ALLOW_ACTION
          
)
;
        
"
"
"
        
)
    
def
verify_recovered_permissions
(
self
)
:
        
permissionExists
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
principal
=
Services
.
scriptSecurityManager
.
createContentPrincipalFromOrigin
(
            
"
https
:
/
/
test
-
permission
-
site
.
com
"
          
)
;
          
let
perms
=
Services
.
perms
.
getAllForPrincipal
(
principal
)
;
          
if
(
perms
.
length
!
=
1
)
{
            
throw
new
Error
(
"
Got
an
unexpected
number
of
permissions
"
)
;
          
}
          
return
perms
[
0
]
.
type
=
=
"
desktop
-
notification
"
        
"
"
"
        
)
        
self
.
assertTrue
(
permissionExists
)
    
def
add_test_payment_methods
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
{
formAutofillStorage
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
autofill
/
FormAutofillStorage
.
sys
.
mjs
"
          
)
;
          
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
            
await
formAutofillStorage
.
initialize
(
)
;
            
await
formAutofillStorage
.
creditCards
.
add
(
{
              
"
cc
-
name
"
:
"
Foxy
the
Firefox
"
              
"
cc
-
number
"
:
"
5555555555554444
"
              
"
cc
-
exp
-
month
"
:
5
              
"
cc
-
exp
-
year
"
:
2099
            
}
)
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
    
def
verify_recovered_payment_methods
(
self
osKeyStoreLabel
)
:
        
cardExists
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
formAutofillStorage
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
autofill
/
FormAutofillStorage
.
sys
.
mjs
"
          
)
;
          
let
nativeOSKeyStore
=
Cc
[
"
mozilla
.
org
/
security
/
oskeystore
;
1
"
]
.
getService
(
            
Ci
.
nsIOSKeyStore
          
)
;
          
let
[
osKeyStoreLabel
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
            
await
formAutofillStorage
.
initialize
(
)
;
            
let
cards
=
await
formAutofillStorage
.
creditCards
.
getAll
(
)
;
            
if
(
cards
.
length
!
=
1
)
{
              
return
false
;
            
}
            
let
card
=
cards
[
0
]
;
            
if
(
card
[
"
cc
-
name
"
]
!
=
"
Foxy
the
Firefox
"
)
{
              
return
false
;
            
}
            
if
(
card
[
"
cc
-
exp
-
month
"
]
!
=
"
5
"
)
{
              
return
false
;
            
}
            
if
(
card
[
"
cc
-
exp
-
year
"
]
!
=
"
2099
"
)
{
              
return
false
;
            
}
            
if
(
!
card
[
"
cc
-
number
-
encrypted
"
]
)
{
              
return
false
;
            
}
            
/
/
Hack
around
OSKeyStore
'
s
insistence
on
asking
for
            
/
/
reauthentication
by
using
the
underlying
nativeOSKeyStore
            
/
/
to
decrypt
the
credit
card
number
to
check
it
.
            
let
plaintextCardBytes
=
              
await
nativeOSKeyStore
.
asyncDecryptBytes
(
                
osKeyStoreLabel
                
card
[
"
cc
-
number
-
encrypted
"
]
              
)
;
            
let
plaintextCard
=
String
.
fromCharCode
.
apply
(
              
String
              
plaintextCardBytes
            
)
;
            
if
(
plaintextCard
!
=
"
5555555555554444
"
)
{
              
return
false
;
            
}
            
return
true
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
            
script_args
=
[
osKeyStoreLabel
]
        
)
        
self
.
assertTrue
(
cardExists
)
    
def
add_test_sessionstore
(
self
)
:
        
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
            
self
.
marionette
.
navigate
(
"
about
:
mozilla
"
)
    
def
verify_recovered_sessionstore
(
self
)
:
        
[
tabCount
url
]
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
{
SessionStore
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
sessionstore
/
SessionStore
.
sys
.
mjs
"
          
)
;
          
const
session
=
SessionStore
.
getCurrentState
(
true
)
;
          
const
win
=
session
.
windows
[
0
]
;
          
const
tabLen
=
win
.
tabs
.
length
;
          
const
tab
=
win
.
tabs
[
0
]
;
          
const
entry
=
tab
.
entries
[
0
]
;
          
const
url
=
entry
.
url
;
          
return
[
tabLen
url
]
;
        
"
"
"
        
)
        
self
.
assertEqual
(
tabCount
1
)
        
self
.
assertEqual
(
url
"
about
:
mozilla
"
)
