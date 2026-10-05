"
"
"
Fetch
and
cache
artifacts
from
URLs
.
This
module
manages
fetching
artifacts
from
URLS
and
purging
old
artifacts
using
a
simple
Least
Recently
Used
cache
.
This
module
requires
certain
modules
be
importable
from
the
ambient
Python
environment
.
Consumers
will
need
to
arrange
this
themselves
.
The
bulk
of
the
complexity
is
in
managing
and
persisting
several
caches
.
If
we
found
a
Python
LRU
cache
that
pickled
cleanly
we
could
remove
a
lot
of
this
code
!
Sadly
I
found
no
such
candidate
implementations
so
we
pickle
pylru
caches
manually
.
ArtifactCache
.
fetch
may
be
called
concurrently
from
multiple
threads
.
"
"
"
import
binascii
import
hashlib
import
logging
import
os
import
threading
import
urllib
.
parse
as
urlparse
import
dlmanager
import
mozpack
.
path
as
mozpath
import
requests
from
mozbuild
.
build_markers
import
build_marker
from
mozbuild
.
dirutils
import
mkdir
CHUNK_SIZE
=
16
*
1024
*
1024
dl_init
=
dlmanager
.
Download
.
__init__
dl_init
.
__defaults__
=
(
    
dl_init
.
__defaults__
[
:
1
]
+
(
CHUNK_SIZE
)
+
dl_init
.
__defaults__
[
2
:
]
)
MIN_CACHED_ARTIFACTS
=
12
MAX_CACHED_ARTIFACTS_SIZE
=
4
*
1024
*
1024
*
1024
class
ArtifactPersistLimit
(
dlmanager
.
PersistLimit
)
:
    
"
"
"
Handle
persistence
for
a
cache
of
artifacts
.
    
When
instantiating
a
DownloadManager
it
starts
by
filling
the
    
PersistLimit
instance
it
'
s
given
with
register_dir_content
.
    
In
practice
this
registers
all
the
files
already
in
the
cache
directory
.
    
After
a
download
finishes
the
newly
downloaded
file
is
registered
and
the
    
oldest
files
registered
to
the
PersistLimit
instance
are
removed
depending
    
on
the
size
and
file
limits
it
'
s
configured
for
.
    
This
is
all
good
but
there
are
a
few
tweaks
we
want
here
:
      
-
We
have
pickle
files
in
the
cache
directory
that
we
don
'
t
want
purged
.
      
-
Files
that
were
just
downloaded
in
the
same
session
shouldn
'
t
be
        
purged
.
(
if
for
some
reason
we
end
up
downloading
more
than
the
default
        
max
size
we
don
'
t
want
the
files
to
be
purged
)
    
To
achieve
this
this
subclass
of
PersistLimit
inhibits
the
register_file
    
method
for
pickle
files
and
tracks
what
files
were
downloaded
in
the
same
    
session
to
avoid
removing
them
.
    
The
register_file
method
may
be
used
to
register
cache
matches
too
so
that
    
later
sessions
know
they
were
freshly
used
.
    
"
"
"
    
def
__init__
(
self
log
=
None
)
:
        
super
(
)
.
__init__
(
            
size_limit
=
MAX_CACHED_ARTIFACTS_SIZE
file_limit
=
MIN_CACHED_ARTIFACTS
        
)
        
self
.
_log
=
log
        
self
.
_registering_dir
=
False
        
self
.
_downloaded_now
=
set
(
)
        
self
.
_lock
=
threading
.
RLock
(
)
    
def
log
(
self
*
args
*
*
kwargs
)
:
        
if
self
.
_log
:
            
self
.
_log
(
*
args
*
*
kwargs
)
    
def
register_file
(
self
path
)
:
        
if
(
            
path
.
endswith
(
"
.
pickle
"
)
            
or
path
.
endswith
(
"
.
checksum
"
)
            
or
os
.
path
.
basename
(
path
)
=
=
"
.
metadata_never_index
"
        
)
:
            
return
        
with
self
.
_lock
:
            
self
.
_register_file
(
path
)
    
def
_register_file
(
self
path
)
:
        
if
not
self
.
_registering_dir
:
            
try
:
                
os
.
utime
(
path
None
)
            
except
OSError
:
                
pass
            
self
.
_downloaded_now
.
add
(
path
)
        
super
(
)
.
register_file
(
path
)
    
def
register_dir_content
(
self
directory
pattern
=
"
*
"
)
:
        
self
.
_registering_dir
=
True
        
super
(
)
.
register_dir_content
(
directory
pattern
)
        
self
.
_registering_dir
=
False
    
def
remove_old_files
(
self
)
:
        
with
self
.
_lock
:
            
self
.
_remove_old_files
(
)
    
def
_remove_old_files
(
self
)
:
        
from
dlmanager
import
fs
        
files
=
sorted
(
self
.
files
key
=
lambda
f
:
f
.
stat
.
st_atime
)
        
kept
=
[
]
        
while
len
(
files
)
>
self
.
file_limit
and
self
.
_files_size
>
=
self
.
size_limit
:
            
f
=
files
.
pop
(
0
)
            
if
f
.
path
in
self
.
_downloaded_now
:
                
kept
.
append
(
f
)
                
continue
            
try
:
                
fs
.
remove
(
f
.
path
)
            
except
OSError
:
                
kept
.
append
(
f
)
                
continue
            
self
.
log
(
                
logging
.
INFO
                
"
artifact
"
                
{
"
filename
"
:
f
.
path
}
                
"
Purged
artifact
{
filename
}
"
            
)
            
self
.
_files_size
-
=
f
.
stat
.
st_size
        
self
.
files
=
files
+
kept
    
def
remove_all
(
self
)
:
        
from
dlmanager
import
fs
        
for
f
in
self
.
files
:
            
fs
.
remove
(
f
.
path
)
        
self
.
_files_size
=
0
        
self
.
files
=
[
]
class
ArtifactCache
:
    
"
"
"
Fetch
artifacts
from
URLS
and
purge
least
recently
used
artifacts
from
disk
.
"
"
"
    
def
__init__
(
self
cache_dir
log
=
None
skip_cache
=
False
)
:
        
mkdir
(
cache_dir
not_indexed
=
True
)
        
self
.
_cache_dir
=
cache_dir
        
self
.
_log
=
log
        
self
.
_skip_cache
=
skip_cache
        
self
.
_persist_limit
=
ArtifactPersistLimit
(
log
)
        
session
=
requests
.
Session
(
)
        
session
.
hooks
[
"
response
"
]
.
append
(
self
.
_track_response
)
        
self
.
_download_manager
=
dlmanager
.
DownloadManager
(
            
self
.
_cache_dir
session
=
session
persist_limit
=
self
.
_persist_limit
        
)
        
self
.
_response
=
threading
.
local
(
)
    
def
log
(
self
*
args
*
*
kwargs
)
:
        
if
self
.
_log
:
            
self
.
_log
(
*
args
*
*
kwargs
)
    
def
_track_response
(
self
response
*
args
*
*
kwargs
)
:
        
self
.
_response
.
current
=
response
    
def
fetch
(
self
url
force
=
False
)
:
        
fname
=
os
.
path
.
basename
(
url
)
        
try
:
            
if
len
(
fname
)
not
in
(
32
40
56
64
96
128
)
:
                
raise
TypeError
(
)
            
binascii
.
unhexlify
(
fname
)
        
except
(
TypeError
binascii
.
Error
)
:
            
hash
=
hashlib
.
sha256
(
url
.
encode
(
)
)
.
hexdigest
(
)
[
:
16
]
            
basename
=
os
.
path
.
basename
(
urlparse
.
urlparse
(
url
)
.
path
)
            
fname
=
hash
+
"
-
"
+
basename
        
path
=
os
.
path
.
abspath
(
mozpath
.
join
(
self
.
_cache_dir
fname
)
)
        
if
self
.
_skip_cache
and
os
.
path
.
exists
(
path
)
:
            
self
.
log
(
                
logging
.
INFO
                
"
artifact
"
                
{
"
path
"
:
path
}
                
"
Skipping
cache
:
removing
cached
downloaded
artifact
{
path
}
"
            
)
            
os
.
remove
(
path
)
        
dl
=
None
        
try
:
            
dl
=
self
.
_download_manager
.
download
(
url
fname
)
            
last_dl_update
=
-
1
            
def
download_progress
(
dl
_decoded_bytes
total_size
)
:
                
nonlocal
last_dl_update
                
if
not
total_size
:
                    
return
                
bytes_so_far
=
self
.
_response
.
current
.
raw
.
tell
(
)
                
percent
=
(
float
(
bytes_so_far
)
/
total_size
)
*
100
                
now
=
int
(
percent
/
5
)
                
if
now
=
=
last_dl_update
:
                    
return
                
last_dl_update
=
now
                
self
.
log
(
                    
logging
.
INFO
                    
"
artifact
"
                    
{
                        
"
fname
"
:
fname
                        
"
bytes_so_far
"
:
bytes_so_far
                        
"
total_size
"
:
total_size
                        
"
percent
"
:
percent
                    
}
                    
"
Downloading
{
fname
}
.
.
.
{
percent
:
02
.
1f
}
%
"
                
)
            
if
dl
:
                
self
.
log
(
                    
logging
.
INFO
                    
"
artifact
"
                    
{
"
path
"
:
path
}
                    
"
Downloading
artifact
to
local
cache
:
{
path
}
"
                
)
                
dl
.
set_progress
(
download_progress
)
                
with
build_marker
(
"
ArtifactDownload
"
url
log
=
self
.
log
)
:
                    
dl
.
wait
(
)
            
else
:
                
self
.
log
(
                    
logging
.
INFO
                    
"
artifact
"
                    
{
"
path
"
:
path
}
                    
"
Using
artifact
from
local
cache
:
{
path
}
"
                
)
                
path
=
os
.
path
.
join
(
self
.
_cache_dir
fname
)
                
self
.
_persist_limit
.
register_file
(
path
)
            
return
os
.
path
.
abspath
(
mozpath
.
join
(
self
.
_cache_dir
fname
)
)
        
finally
:
            
if
dl
:
                
dl
.
cancel
(
)
    
def
cancel
(
self
)
:
        
"
"
"
Cancel
all
background
downloads
in
progress
.
"
"
"
        
self
.
_download_manager
.
cancel
(
)
    
def
clear_cache
(
self
)
:
        
if
self
.
_skip_cache
:
            
self
.
log
(
                
logging
.
INFO
"
artifact
"
{
}
"
Skipping
cache
:
ignoring
clear_cache
!
"
            
)
            
return
        
self
.
_persist_limit
.
remove_all
(
)
