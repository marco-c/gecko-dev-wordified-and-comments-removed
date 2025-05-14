import
asyncio
import
json
import
math
import
os
import
pprint
import
re
import
sys
from
collections
import
namedtuple
from
urllib
.
parse
import
urljoin
import
aiohttp
import
hglib
from
hglib
.
util
import
cmdbuilder
from
looseversion
import
LooseVersion
from
mozilla_version
.
gecko
import
GeckoVersion
from
mozilla_version
.
version
import
VersionType
sys
.
path
.
insert
(
1
os
.
path
.
dirname
(
os
.
path
.
dirname
(
sys
.
path
[
0
]
)
)
)
from
mozharness
.
base
.
log
import
DEBUG
FATAL
INFO
WARNING
from
mozharness
.
base
.
script
import
BaseScript
PostScriptRun
PreScriptRun
class
CompareVersion
(
LooseVersion
)
:
    
version
=
"
"
    
def
__init__
(
self
versionMap
)
:
        
parts
=
versionMap
.
split
(
"
.
"
)
        
if
len
(
parts
)
=
=
2
:
            
intre
=
re
.
compile
(
"
(
[
0
-
9
.
]
+
)
(
.
*
)
"
)
            
match
=
intre
.
match
(
parts
[
-
1
]
)
            
if
match
:
                
parts
[
-
1
]
=
match
.
group
(
1
)
                
parts
.
append
(
"
0
%
s
"
%
match
.
group
(
2
)
)
        
else
:
            
parts
.
append
(
"
0
"
)
        
self
.
version
=
"
.
"
.
join
(
parts
)
        
LooseVersion
(
versionMap
)
BuildInfo
=
namedtuple
(
"
BuildInfo
"
[
"
product
"
"
version
"
"
buildID
"
]
)
def
is_triangular
(
x
)
:
    
"
"
"
Check
if
a
number
is
triangular
(
0
1
3
6
10
15
.
.
.
)
    
see
:
https
:
/
/
en
.
wikipedia
.
org
/
wiki
/
Triangular_number
#
Triangular_roots_and_tests_for_triangular_numbers
#
noqa
    
>
>
>
is_triangular
(
0
)
    
True
    
>
>
>
is_triangular
(
1
)
    
True
    
>
>
>
is_triangular
(
2
)
    
False
    
>
>
>
is_triangular
(
3
)
    
True
    
>
>
>
is_triangular
(
4
)
    
False
    
>
>
>
all
(
is_triangular
(
x
)
for
x
in
[
0
1
3
6
10
15
21
28
36
45
55
66
78
91
105
]
)
    
True
    
>
>
>
all
(
not
is_triangular
(
x
)
for
x
in
[
4
5
8
9
11
17
25
29
39
44
59
61
72
98
112
]
)
    
True
    
"
"
"
    
n
=
(
math
.
sqrt
(
8
*
x
+
1
)
-
1
)
/
2
    
return
n
=
=
int
(
n
)
class
UpdateVerifyConfigCreator
(
BaseScript
)
:
    
config_options
=
[
        
[
            
[
"
-
-
product
"
]
            
{
                
"
dest
"
:
"
product
"
                
"
help
"
:
"
Product
being
tested
as
used
in
the
update
URL
and
filenames
.
Eg
:
firefox
"
            
}
        
]
        
[
            
[
"
-
-
stage
-
product
"
]
            
{
                
"
dest
"
:
"
stage_product
"
                
"
help
"
:
"
Product
being
tested
as
used
in
stage
directories
and
ship
it
"
                
"
If
not
passed
this
is
assumed
to
be
the
same
as
product
.
"
            
}
        
]
        
[
            
[
"
-
-
app
-
name
"
]
            
{
                
"
dest
"
:
"
app_name
"
                
"
help
"
:
"
App
name
being
tested
.
Eg
:
browser
"
            
}
        
]
        
[
            
[
"
-
-
branch
-
prefix
"
]
            
{
                
"
dest
"
:
"
branch_prefix
"
                
"
help
"
:
"
Prefix
of
release
branch
names
.
Eg
:
mozilla
comm
"
            
}
        
]
        
[
            
[
"
-
-
channel
"
]
            
{
                
"
dest
"
:
"
channel
"
                
"
help
"
:
"
Channel
to
run
update
verify
against
"
            
}
        
]
        
[
            
[
"
-
-
aus
-
server
"
]
            
{
                
"
dest
"
:
"
aus_server
"
                
"
default
"
:
"
https
:
/
/
aus5
.
mozilla
.
org
"
                
"
help
"
:
"
AUS
server
to
run
update
verify
against
"
            
}
        
]
        
[
            
[
"
-
-
to
-
version
"
]
            
{
                
"
dest
"
:
"
to_version
"
                
"
help
"
:
"
The
version
of
the
release
being
updated
to
.
Eg
:
59
.
0b5
"
            
}
        
]
        
[
            
[
"
-
-
to
-
app
-
version
"
]
            
{
                
"
dest
"
:
"
to_app_version
"
                
"
help
"
:
"
The
in
-
app
version
of
the
release
being
updated
to
.
Eg
:
59
.
0
"
            
}
        
]
        
[
            
[
"
-
-
to
-
display
-
version
"
]
            
{
                
"
dest
"
:
"
to_display_version
"
                
"
help
"
:
"
The
human
-
readable
version
of
the
release
being
updated
to
.
Eg
:
59
.
0
Beta
9
"
            
}
        
]
        
[
            
[
"
-
-
to
-
build
-
number
"
]
            
{
                
"
dest
"
:
"
to_build_number
"
                
"
help
"
:
"
The
build
number
of
the
release
being
updated
to
"
            
}
        
]
        
[
            
[
"
-
-
to
-
buildid
"
]
            
{
                
"
dest
"
:
"
to_buildid
"
                
"
help
"
:
"
The
buildid
of
the
release
being
updated
to
"
            
}
        
]
        
[
            
[
"
-
-
to
-
revision
"
]
            
{
                
"
dest
"
:
"
to_revision
"
                
"
help
"
:
"
The
revision
that
the
release
being
updated
to
was
built
against
"
            
}
        
]
        
[
            
[
"
-
-
partial
-
version
"
]
            
{
                
"
dest
"
:
"
partial_versions
"
                
"
default
"
:
[
]
                
"
action
"
:
"
append
"
                
"
help
"
:
"
A
previous
release
version
that
is
expected
to
receive
a
partial
update
.
"
                
"
Eg
:
59
.
0b4
.
May
be
specified
multiple
times
.
"
            
}
        
]
        
[
            
[
"
-
-
last
-
watershed
"
]
            
{
                
"
dest
"
:
"
last_watershed
"
                
"
help
"
:
"
The
earliest
version
to
include
in
the
update
verify
config
.
Eg
:
57
.
0b10
"
            
}
        
]
        
[
            
[
"
-
-
include
-
version
"
]
            
{
                
"
dest
"
:
"
include_versions
"
                
"
default
"
:
[
]
                
"
action
"
:
"
append
"
                
"
help
"
:
"
Only
include
versions
that
match
one
of
these
regexes
.
"
                
"
May
be
passed
multiple
times
"
            
}
        
]
        
[
            
[
"
-
-
mar
-
channel
-
id
-
override
"
]
            
{
                
"
dest
"
:
"
mar_channel_id_options
"
                
"
default
"
:
[
]
                
"
action
"
:
"
append
"
                
"
help
"
:
"
A
version
regex
and
channel
id
string
to
override
those
versions
with
.
"
                
"
Eg
:
^
\
\
d
+
\
\
.
\
\
d
+
(
\
\
.
\
\
d
+
)
?
firefox
-
mozilla
-
beta
firefox
-
mozilla
-
release
"
                
"
will
set
accepted
mar
channel
ids
to
'
firefox
-
mozilla
-
beta
'
and
"
                
"
'
firefox
-
mozilla
-
release
for
x
.
y
and
x
.
y
.
z
versions
.
"
                
"
May
be
passed
multiple
times
"
            
}
        
]
        
[
            
[
"
-
-
override
-
certs
"
]
            
{
                
"
dest
"
:
"
override_certs
"
                
"
default
"
:
None
                
"
help
"
:
"
Certs
to
override
the
updater
with
prior
to
running
update
verify
.
"
                
"
If
passed
should
be
one
of
:
dep
nightly
release
"
                
"
If
not
passed
no
certificate
overriding
will
be
configured
"
            
}
        
]
        
[
            
[
"
-
-
platform
"
]
            
{
                
"
dest
"
:
"
platform
"
                
"
help
"
:
"
The
platform
to
generate
the
update
verify
config
for
in
FTP
-
style
"
            
}
        
]
        
[
            
[
"
-
-
updater
-
platform
"
]
            
{
                
"
dest
"
:
"
updater_platform
"
                
"
help
"
:
"
The
platform
to
run
the
updater
on
in
FTP
-
style
.
"
                
"
If
not
specified
this
is
assumed
to
be
the
same
as
platform
"
            
}
        
]
        
[
            
[
"
-
-
archive
-
prefix
"
]
            
{
                
"
dest
"
:
"
archive_prefix
"
                
"
help
"
:
"
The
server
/
path
to
pull
the
current
release
from
.
"
                
"
Eg
:
https
:
/
/
archive
.
mozilla
.
org
/
pub
"
            
}
        
]
        
[
            
[
"
-
-
previous
-
archive
-
prefix
"
]
            
{
                
"
dest
"
:
"
previous_archive_prefix
"
                
"
help
"
:
"
The
server
/
path
to
pull
the
previous
releases
from
"
                
"
If
not
specified
this
is
assumed
to
be
the
same
as
-
-
archive
-
prefix
"
            
}
        
]
        
[
            
[
"
-
-
repo
-
path
"
]
            
{
                
"
dest
"
:
"
repo_path
"
                
"
help
"
:
(
                    
"
The
repository
(
relative
to
the
hg
server
root
)
that
the
current
"
                    
"
release
was
built
from
Eg
:
releases
/
mozilla
-
beta
"
                
)
            
}
        
]
        
[
            
[
"
-
-
output
-
file
"
]
            
{
                
"
dest
"
:
"
output_file
"
                
"
help
"
:
"
Where
to
write
the
update
verify
config
to
"
            
}
        
]
        
[
            
[
"
-
-
product
-
details
-
server
"
]
            
{
                
"
dest
"
:
"
product_details_server
"
                
"
default
"
:
"
https
:
/
/
product
-
details
.
mozilla
.
org
"
                
"
help
"
:
"
Product
Details
server
to
pull
previous
release
info
from
.
"
                
"
Using
anything
other
than
the
production
server
is
likely
to
"
                
"
cause
issues
with
update
verify
.
"
            
}
        
]
        
[
            
[
"
-
-
last
-
linux
-
bz2
-
version
"
]
            
{
                
"
dest
"
:
"
last_linux_bz2_version
"
                
"
help
"
:
"
Last
linux
build
version
with
bz2
compression
.
"
            
}
        
]
        
[
            
[
"
-
-
hg
-
server
"
]
            
{
                
"
dest
"
:
"
hg_server
"
                
"
default
"
:
"
https
:
/
/
hg
.
mozilla
.
org
"
                
"
help
"
:
"
Mercurial
server
to
pull
various
previous
and
current
version
info
from
"
            
}
        
]
        
[
            
[
"
-
-
full
-
check
-
locale
"
]
            
{
                
"
dest
"
:
"
full_check_locales
"
                
"
default
"
:
[
"
de
"
"
en
-
US
"
"
ru
"
]
                
"
action
"
:
"
append
"
                
"
help
"
:
"
A
list
of
locales
to
generate
full
update
verify
checks
for
"
            
}
        
]
        
[
            
[
"
-
-
local
-
repo
"
]
            
{
                
"
dest
"
:
"
local_repo
"
                
"
help
"
:
"
Path
to
local
clone
of
the
repository
"
            
}
        
]
    
]
    
def
__init__
(
self
)
:
        
BaseScript
.
__init__
(
            
self
            
config_options
=
self
.
config_options
            
config
=
{
}
            
all_actions
=
[
                
"
gather
-
info
"
                
"
create
-
config
"
                
"
write
-
config
"
            
]
            
default_actions
=
[
                
"
gather
-
info
"
                
"
create
-
config
"
                
"
write
-
config
"
            
]
        
)
        
self
.
hgclient
=
None
    
PreScriptRun
    
def
_setup_hgclient
(
self
)
:
        
if
not
self
.
config
.
get
(
"
local_repo
"
)
:
            
return
        
self
.
hgclient
=
hglib
.
open
(
self
.
config
[
"
local_repo
"
]
)
        
try
:
            
self
.
hg_tags
=
set
(
t
[
0
]
.
decode
(
"
utf
-
8
"
)
for
t
in
self
.
hgclient
.
tags
(
)
)
            
self
.
log
(
f
"
Loaded
tags
from
local
hg
repo
.
{
len
(
self
.
hg_tags
)
}
tags
found
.
"
)
        
except
Exception
as
e
:
            
self
.
log
(
f
"
Error
loading
tags
from
local
hg
repo
:
{
e
}
"
)
            
self
.
hg_tags
=
set
(
)
    
PostScriptRun
    
def
_close_hg_client
(
self
)
:
        
if
hasattr
(
self
"
hgclient
"
)
:
            
self
.
hgclient
.
close
(
)
            
self
.
log
(
"
Closed
HG
client
.
"
)
    
def
_pre_config_lock
(
self
rw_config
)
:
        
super
(
UpdateVerifyConfigCreator
self
)
.
_pre_config_lock
(
rw_config
)
        
if
"
updater_platform
"
not
in
self
.
config
:
            
self
.
config
[
"
updater_platform
"
]
=
self
.
config
[
"
platform
"
]
        
if
"
stage_product
"
not
in
self
.
config
:
            
self
.
config
[
"
stage_product
"
]
=
self
.
config
[
"
product
"
]
        
if
"
previous_archive_prefix
"
not
in
self
.
config
:
            
self
.
config
[
"
previous_archive_prefix
"
]
=
self
.
config
[
"
archive_prefix
"
]
        
self
.
config
[
"
archive_prefix
"
]
.
rstrip
(
"
/
"
)
        
self
.
config
[
"
previous_archive_prefix
"
]
.
rstrip
(
"
/
"
)
        
self
.
config
[
"
mar_channel_id_overrides
"
]
=
{
}
        
for
override
in
self
.
config
[
"
mar_channel_id_options
"
]
:
            
pattern
override_str
=
override
.
split
(
"
"
1
)
            
self
.
config
[
"
mar_channel_id_overrides
"
]
[
pattern
]
=
override_str
    
def
_get_branch_url
(
self
branch_prefix
version
)
:
        
version
=
GeckoVersion
.
parse
(
version
)
        
branch
=
None
        
if
version
.
version_type
=
=
VersionType
.
BETA
:
            
branch
=
f
"
releases
/
{
branch_prefix
}
-
beta
"
        
elif
version
.
version_type
=
=
VersionType
.
ESR
:
            
branch
=
f
"
releases
/
{
branch_prefix
}
-
esr
{
version
.
major_number
}
"
        
elif
version
.
version_type
=
=
VersionType
.
RELEASE
:
            
branch
=
f
"
releases
/
{
branch_prefix
}
-
release
"
        
if
not
branch
:
            
raise
Exception
(
"
Cannot
determine
branch
cannot
continue
!
"
)
        
return
branch
    
async
def
_download_build_info
(
        
self
semaphore
session
product
version
info_file_url
    
)
:
        
"
"
"
Async
download
and
parse
build
info
file
for
given
url
        
Args
:
            
semaphore
:
Semaphore
object
to
control
max
async
parallel
channels
            
session
:
Http
session
handler
            
product
:
Product
string
            
version
:
Version
string
            
info_file_url
:
URL
to
desired
buildid
file
        
Returns
:
            
BuildInfo
Tuple
(
product
version
buildID
)
        
"
"
"
        
async
def
_get
(
)
:
            
async
with
session
.
get
(
info_file_url
)
as
response
:
                
if
response
.
status
<
400
:
                    
return
response
.
status
await
response
.
text
(
)
                
return
response
.
status
response
.
reason
        
RETRIES
=
3
        
RETRY_DELAY_STEP
=
5
        
async
with
semaphore
:
            
attempt
=
1
            
while
attempt
<
=
RETRIES
:
                
self
.
log
(
                    
f
"
Retrieving
buildid
from
info
file
:
{
info_file_url
}
-
attempt
:
#
{
attempt
}
"
                    
level
=
INFO
                
)
                
status
text
=
await
_get
(
)
                
if
status
<
400
:
                    
return
BuildInfo
(
product
version
text
.
split
(
"
=
"
)
[
1
]
.
strip
(
)
)
                
self
.
log
(
                    
f
"
Error
retrieving
buildid
{
info_file_url
}
-
Status
:
{
status
}
-
Reason
:
{
text
}
"
                
)
                
if
status
=
=
404
:
                    
raise
Exception
(
f
"
File
not
found
on
remote
server
:
{
info_file_url
}
"
)
                
attempt
+
=
1
                
await
asyncio
.
sleep
(
RETRY_DELAY_STEP
*
attempt
)
            
raise
Exception
(
f
"
Max
number
of
retries
reached
for
{
info_file_url
}
"
)
    
def
_async_download_build_ids
(
self
filelist
)
:
        
"
"
"
Download
all
build_info
asynchronously
then
process
once
everything
is
downloaded
        
Args
:
            
filelist
:
List
of
tuples
(
product
version
info_file_url
)
        
Returns
:
            
List
of
BuildInfo
tuples
(
product
version
buildID
)
        
"
"
"
        
CONCURRENCY
=
15
        
loop
=
asyncio
.
get_event_loop
(
)
        
async
def
_run_semaphore
(
)
:
            
async
with
aiohttp
.
ClientSession
(
)
as
session
:
                
self
.
log
(
                    
f
"
Starting
async
download
.
Semaphore
with
{
CONCURRENCY
}
concurrencies
.
"
                
)
                
semaphore
=
asyncio
.
Semaphore
(
CONCURRENCY
)
                
tasks
=
[
                    
self
.
_download_build_info
(
semaphore
session
*
info
)
                    
for
info
in
filelist
                
]
                
return
await
asyncio
.
gather
(
*
tasks
)
        
return
loop
.
run_until_complete
(
_run_semaphore
(
)
)
    
def
_get_update_paths
(
self
)
:
        
from
mozrelease
.
l10n
import
getPlatformLocales
        
from
mozrelease
.
paths
import
getCandidatesDir
        
from
mozrelease
.
platforms
import
ftp2infoFile
        
from
mozrelease
.
versions
import
MozillaVersion
        
self
.
update_paths
=
{
}
        
ret
=
self
.
_retry_download
(
            
"
{
}
/
1
.
0
/
{
}
.
json
"
.
format
(
                
self
.
config
[
"
product_details_server
"
]
                
self
.
config
[
"
stage_product
"
]
            
)
            
"
WARNING
"
        
)
        
releases
=
json
.
load
(
ret
)
[
"
releases
"
]
        
info_file_urls
=
[
]
        
for
release_name
release_info
in
reversed
(
            
sorted
(
releases
.
items
(
)
key
=
lambda
x
:
MozillaVersion
(
x
[
1
]
[
"
version
"
]
)
)
        
)
:
            
product
version
=
release_name
.
split
(
"
-
"
1
)
            
for
v
in
self
.
config
[
"
include_versions
"
]
:
                
if
re
.
match
(
v
version
)
:
                    
break
            
else
:
                
self
.
log
(
                    
"
Skipping
release
whose
version
doesn
'
t
match
any
"
                    
"
include_version
pattern
:
%
s
"
%
release_name
                    
level
=
INFO
                
)
                
continue
            
if
self
.
config
[
"
stage_product
"
]
!
=
product
:
                
self
.
log
(
                    
"
Skipping
release
that
doesn
'
t
match
product
name
:
%
s
"
                    
%
release_name
                    
level
=
INFO
                
)
                
continue
            
if
MozillaVersion
(
version
)
<
MozillaVersion
(
self
.
config
[
"
last_watershed
"
]
)
:
                
self
.
log
(
                    
"
Skipping
release
that
'
s
behind
the
last
watershed
:
%
s
"
                    
%
release_name
                    
level
=
INFO
                
)
                
continue
            
if
version
=
=
self
.
config
[
"
to_version
"
]
:
                
self
.
log
(
                    
"
Skipping
release
that
is
the
same
as
to
version
:
%
s
"
                    
%
release_name
                    
level
=
INFO
                
)
                
continue
            
if
MozillaVersion
(
version
)
>
MozillaVersion
(
self
.
config
[
"
to_version
"
]
)
:
                
self
.
log
(
                    
"
Skipping
release
that
'
s
newer
than
to
version
:
%
s
"
%
release_name
                    
level
=
INFO
                
)
                
continue
            
info_file_source
=
"
{
}
{
}
/
{
}
_info
.
txt
"
.
format
(
                
self
.
config
[
"
previous_archive_prefix
"
]
                
getCandidatesDir
(
                    
self
.
config
[
"
stage_product
"
]
                    
version
                    
release_info
[
"
build_number
"
]
                
)
                
ftp2infoFile
(
self
.
config
[
"
platform
"
]
)
            
)
            
info_file_urls
.
append
(
(
product
version
info_file_source
)
)
        
build_info_list
=
self
.
_async_download_build_ids
(
info_file_urls
)
        
for
build
in
build_info_list
:
            
if
build
.
version
in
self
.
update_paths
:
                
raise
Exception
(
                    
"
Found
duplicate
release
for
version
:
%
s
"
build
.
version
                
)
            
shipped_locales
app_version
=
self
.
_get_files_from_repo_tag
(
                
build
.
product
                
build
.
version
                
f
"
{
self
.
config
[
'
app_name
'
]
}
/
locales
/
shipped
-
locales
"
                
f
"
{
self
.
config
[
'
app_name
'
]
}
/
config
/
version
.
txt
"
            
)
            
self
.
log
(
f
"
Adding
{
build
.
version
}
to
update
paths
"
level
=
INFO
)
            
self
.
update_paths
[
build
.
version
]
=
{
                
"
appVersion
"
:
app_version
                
"
locales
"
:
getPlatformLocales
(
shipped_locales
self
.
config
[
"
platform
"
]
)
                
"
buildID
"
:
build
.
buildID
            
}
            
for
pattern
mar_channel_ids
in
self
.
config
[
                
"
mar_channel_id_overrides
"
            
]
.
items
(
)
:
                
if
re
.
match
(
pattern
build
.
version
)
:
                    
self
.
update_paths
[
build
.
version
]
[
"
marChannelIds
"
]
=
mar_channel_ids
    
def
_get_file_from_repo
(
self
rev
branch
path
)
:
        
if
self
.
config
.
get
(
"
local_repo
"
)
:
            
try
:
                
return
self
.
_get_files_from_local_repo
(
rev
path
)
[
0
]
            
except
Exception
:
                
self
.
log
(
                    
"
Unable
to
get
file
from
local
repo
trying
from
remote
instead
.
"
                
)
        
return
self
.
_get_files_from_remote_repo
(
rev
branch
path
)
[
0
]
    
def
_get_files_from_repo_tag
(
self
product
version
*
paths
)
:
        
tag
=
"
{
}
_
{
}
_RELEASE
"
.
format
(
product
.
upper
(
)
version
.
replace
(
"
.
"
"
_
"
)
)
        
if
self
.
config
.
get
(
"
local_repo
"
)
and
tag
in
self
.
hg_tags
:
            
return
self
.
_get_files_from_local_repo
(
tag
*
paths
)
        
branch
=
self
.
_get_branch_url
(
self
.
config
[
"
branch_prefix
"
]
version
)
        
return
self
.
_get_files_from_remote_repo
(
tag
branch
*
paths
)
    
def
_get_files_from_local_repo
(
self
rev
*
paths
)
:
        
"
"
"
Retrieve
multiple
files
from
the
local
repo
at
a
given
revision
"
"
"
        
args
=
cmdbuilder
(
            
b
"
cat
"
            
b
"
-
-
cwd
"
            
bytes
(
self
.
config
[
"
local_repo
"
]
"
utf
-
8
"
)
            
*
[
bytes
(
p
"
utf
-
8
"
)
for
p
in
paths
]
            
r
=
bytes
(
rev
"
utf
-
8
"
)
            
T
=
b
"
{
path
}
\
\
0
{
data
}
\
\
0
"
        
)
        
try
:
            
raw
=
self
.
hgclient
.
rawcommand
(
args
)
.
strip
(
)
.
decode
(
"
utf
-
8
"
)
        
except
Exception
as
e
:
            
self
.
log
(
"
Error
retrieving
file
from
local
repository
.
"
)
            
raise
e
        
chunks
=
raw
.
split
(
"
\
x00
"
)
[
:
-
1
]
        
path_contents
=
{
}
        
while
chunks
:
            
filename
=
chunks
.
pop
(
0
)
            
data
=
chunks
.
pop
(
0
)
.
strip
(
)
            
path_contents
[
filename
]
=
data
        
result
=
[
]
        
for
path
in
paths
:
            
if
path
not
in
path_contents
:
                
raise
Exception
(
                    
f
"
_get_files_from_local_repo
:
Could
not
find
{
path
}
in
revision
{
rev
}
"
                
)
            
result
.
append
(
path_contents
[
path
]
)
        
return
result
    
def
_get_files_from_remote_repo
(
self
rev
branch
*
paths
)
:
        
files
=
[
]
        
for
path
in
paths
:
            
hg_url
=
urljoin
(
                
self
.
config
[
"
hg_server
"
]
f
"
{
branch
}
/
raw
-
file
/
{
rev
}
/
{
path
}
"
            
)
            
ret
=
self
.
_retry_download
(
                
hg_url
"
WARNING
"
retry_config
=
{
"
sleeptime
"
:
5
"
max_sleeptime
"
:
5
}
            
)
            
if
ret
is
None
:
                
self
.
log
(
"
couldn
'
t
fetch
file
from
hg
;
trying
github
"
)
                
git_url
=
f
"
https
:
/
/
raw
.
githubusercontent
.
com
/
mozilla
-
firefox
/
firefox
/
refs
/
tags
/
{
rev
}
/
{
path
}
"
                
ret
=
self
.
_retry_download
(
git_url
"
WARNING
"
)
            
files
.
append
(
ret
.
read
(
)
.
strip
(
)
.
decode
(
"
utf
-
8
"
)
)
        
return
files
    
def
gather_info
(
self
)
:
        
from
mozilla_version
.
gecko
import
GeckoVersion
        
self
.
_get_update_paths
(
)
        
if
self
.
update_paths
:
            
self
.
log
(
"
Found
update
paths
:
"
level
=
DEBUG
)
            
self
.
log
(
pprint
.
pformat
(
self
.
update_paths
)
level
=
DEBUG
)
        
elif
GeckoVersion
.
parse
(
self
.
config
[
"
to_version
"
]
)
<
=
GeckoVersion
.
parse
(
            
self
.
config
[
"
last_watershed
"
]
        
)
:
            
self
.
log
(
                
"
Didn
'
t
find
any
update
paths
but
to_version
{
}
is
before
the
last_
"
                
"
watershed
{
}
generating
empty
config
"
.
format
(
                    
self
.
config
[
"
to_version
"
]
                    
self
.
config
[
"
last_watershed
"
]
                
)
                
level
=
WARNING
            
)
        
else
:
            
self
.
log
(
"
Didn
'
t
find
any
update
paths
cannot
continue
"
level
=
FATAL
)
    
def
create_config
(
self
)
:
        
from
mozrelease
.
l10n
import
getPlatformLocales
        
from
mozrelease
.
paths
import
(
            
getCandidatesDir
            
getReleaseInstallerPath
            
getReleasesDir
        
)
        
from
mozrelease
.
platforms
import
ftp2updatePlatforms
        
from
mozrelease
.
update_verify
import
UpdateVerifyConfig
        
from
mozrelease
.
versions
import
getPrettyVersion
        
candidates_dir
=
getCandidatesDir
(
            
self
.
config
[
"
stage_product
"
]
            
self
.
config
[
"
to_version
"
]
            
self
.
config
[
"
to_build_number
"
]
        
)
        
to_
=
getReleaseInstallerPath
(
            
self
.
config
[
"
product
"
]
            
self
.
config
[
"
product
"
]
.
title
(
)
            
self
.
config
[
"
to_version
"
]
            
self
.
config
[
"
platform
"
]
            
locale
=
"
%
locale
%
"
            
last_linux_bz2_version
=
self
.
config
.
get
(
"
last_linux_bz2_version
"
)
        
)
        
to_path
=
f
"
{
candidates_dir
}
/
{
to_
}
"
        
to_display_version
=
self
.
config
.
get
(
"
to_display_version
"
)
        
if
not
to_display_version
:
            
to_display_version
=
getPrettyVersion
(
self
.
config
[
"
to_version
"
]
)
        
self
.
update_verify_config
=
UpdateVerifyConfig
(
            
product
=
self
.
config
[
"
product
"
]
.
title
(
)
            
channel
=
self
.
config
[
"
channel
"
]
            
aus_server
=
self
.
config
[
"
aus_server
"
]
            
to
=
to_path
            
to_build_id
=
self
.
config
[
"
to_buildid
"
]
            
to_app_version
=
self
.
config
[
"
to_app_version
"
]
            
to_display_version
=
to_display_version
            
override_certs
=
self
.
config
.
get
(
"
override_certs
"
)
        
)
        
to_shipped_locales
=
self
.
_get_file_from_repo
(
            
self
.
config
[
"
to_revision
"
]
            
self
.
config
[
"
repo_path
"
]
            
"
{
}
/
locales
/
shipped
-
locales
"
.
format
(
self
.
config
[
"
app_name
"
]
)
        
)
        
to_locales
=
set
(
            
getPlatformLocales
(
to_shipped_locales
self
.
config
[
"
platform
"
]
)
        
)
        
completes_only_index
=
0
        
for
fromVersion
in
reversed
(
sorted
(
self
.
update_paths
key
=
CompareVersion
)
)
:
            
from_
=
self
.
update_paths
[
fromVersion
]
            
locales
=
sorted
(
list
(
set
(
from_
[
"
locales
"
]
)
.
intersection
(
to_locales
)
)
)
            
appVersion
=
from_
[
"
appVersion
"
]
            
build_id
=
from_
[
"
buildID
"
]
            
mar_channel_IDs
=
from_
.
get
(
"
marChannelIds
"
)
            
if
self
.
config
[
"
platform
"
]
not
in
(
"
win32
"
"
win64
"
)
or
LooseVersion
(
                
fromVersion
            
)
<
LooseVersion
(
"
42
.
0
"
)
:
                
update_platform
=
ftp2updatePlatforms
(
self
.
config
[
"
platform
"
]
)
[
0
]
            
else
:
                
update_platform
=
ftp2updatePlatforms
(
self
.
config
[
"
platform
"
]
)
[
1
]
            
release_dir
=
getReleasesDir
(
self
.
config
[
"
stage_product
"
]
fromVersion
)
            
path_
=
getReleaseInstallerPath
(
                
self
.
config
[
"
product
"
]
                
self
.
config
[
"
product
"
]
.
title
(
)
                
fromVersion
                
self
.
config
[
"
platform
"
]
                
locale
=
"
%
locale
%
"
                
last_linux_bz2_version
=
self
.
config
.
get
(
"
last_linux_bz2_version
"
)
            
)
            
from_path
=
f
"
{
release_dir
}
/
{
path_
}
"
            
updater_package
=
"
{
}
/
{
}
"
.
format
(
                
release_dir
                
getReleaseInstallerPath
(
                    
self
.
config
[
"
product
"
]
                    
self
.
config
[
"
product
"
]
.
title
(
)
                    
fromVersion
                    
self
.
config
[
"
updater_platform
"
]
                    
locale
=
"
%
locale
%
"
                    
last_linux_bz2_version
=
self
.
config
.
get
(
"
last_linux_bz2_version
"
)
                
)
            
)
            
quick_check_locales
=
[
                
l
for
l
in
locales
if
l
not
in
self
.
config
[
"
full_check_locales
"
]
            
]
            
this_full_check_locales
=
[
                
l
for
l
in
self
.
config
[
"
full_check_locales
"
]
if
l
in
locales
            
]
            
if
fromVersion
in
self
.
config
[
"
partial_versions
"
]
:
                
self
.
info
(
                    
"
Generating
configs
for
partial
update
checks
for
%
s
"
%
fromVersion
                
)
                
self
.
update_verify_config
.
addRelease
(
                    
release
=
appVersion
                    
build_id
=
build_id
                    
locales
=
locales
                    
patch_types
=
[
"
complete
"
"
partial
"
]
                    
from_path
=
from_path
                    
ftp_server_from
=
self
.
config
[
"
previous_archive_prefix
"
]
                    
ftp_server_to
=
self
.
config
[
"
archive_prefix
"
]
                    
mar_channel_IDs
=
mar_channel_IDs
                    
platform
=
update_platform
                    
updater_package
=
updater_package
                
)
            
else
:
                
if
this_full_check_locales
and
is_triangular
(
completes_only_index
)
:
                    
self
.
info
(
"
Generating
full
check
configs
for
%
s
"
%
fromVersion
)
                    
self
.
update_verify_config
.
addRelease
(
                        
release
=
appVersion
                        
build_id
=
build_id
                        
locales
=
this_full_check_locales
                        
from_path
=
from_path
                        
ftp_server_from
=
self
.
config
[
"
previous_archive_prefix
"
]
                        
ftp_server_to
=
self
.
config
[
"
archive_prefix
"
]
                        
mar_channel_IDs
=
mar_channel_IDs
                        
platform
=
update_platform
                        
updater_package
=
updater_package
                    
)
                
if
len
(
quick_check_locales
)
>
0
:
                    
self
.
info
(
"
Generating
quick
check
configs
for
%
s
"
%
fromVersion
)
                    
if
not
is_triangular
(
completes_only_index
)
:
                        
_locales
=
locales
                    
else
:
                        
_locales
=
quick_check_locales
                    
self
.
update_verify_config
.
addRelease
(
                        
release
=
appVersion
                        
build_id
=
build_id
                        
locales
=
_locales
                        
platform
=
update_platform
                    
)
                
completes_only_index
+
=
1
    
def
write_config
(
self
)
:
        
with
open
(
self
.
config
[
"
output_file
"
]
"
wb
+
"
)
as
fh
:
            
self
.
update_verify_config
.
write
(
fh
)
if
__name__
=
=
"
__main__
"
:
    
UpdateVerifyConfigCreator
(
)
.
run_and_exit
(
)
