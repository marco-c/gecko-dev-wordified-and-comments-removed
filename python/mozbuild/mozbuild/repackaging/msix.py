r
"
"
"
Repackage
ZIP
archives
(
or
directories
)
into
MSIX
App
Packages
.
#
Known
issues
-
The
icons
in
the
Start
Menu
have
a
solid
colour
tile
behind
them
.
I
think
  
this
is
an
issue
with
plating
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
logging
import
os
import
sys
import
subprocess
import
time
import
urllib
from
six
.
moves
import
shlex_quote
from
mozboot
.
util
import
get_state_dir
from
mozbuild
.
util
import
ensureParentDir
from
mozfile
import
which
from
mozpack
.
copier
import
FileCopier
from
mozpack
.
files
import
FileFinder
JarFinder
from
mozpack
.
manifests
import
InstallManifest
from
mozpack
.
mozjar
import
JarReader
from
mozpack
.
packager
.
unpack
import
UnpackFinder
from
mozbuild
.
repackaging
.
application_ini
import
get_application_ini_values
import
mozpack
.
path
as
mozpath
def
log_copy_result
(
log
elapsed
destdir
result
)
:
    
COMPLETE
=
(
        
"
Elapsed
:
{
elapsed
:
.
2f
}
s
;
From
{
dest
}
:
Kept
{
existing
}
existing
;
"
        
"
Added
/
updated
{
updated
}
;
"
        
"
Removed
{
rm_files
}
files
and
{
rm_dirs
}
directories
.
"
    
)
    
copy_result
=
COMPLETE
.
format
(
        
elapsed
=
elapsed
        
dest
=
destdir
        
existing
=
result
.
existing_files_count
        
updated
=
result
.
updated_files_count
        
rm_files
=
result
.
removed_files_count
        
rm_dirs
=
result
.
removed_directories_count
    
)
    
log
(
logging
.
INFO
"
msix
"
{
"
copy_result
"
:
copy_result
}
"
{
copy_result
}
"
)
_MSIX_ARCH
=
{
"
x86
"
:
"
x86
"
"
x86_64
"
:
"
x64
"
"
aarch64
"
:
"
arm64
"
}
def
find_sdk_tool
(
binary
log
=
None
)
:
    
if
binary
.
lower
(
)
.
endswith
(
"
.
exe
"
)
:
        
binary
=
binary
[
:
-
4
]
    
maybe
=
os
.
environ
.
get
(
binary
.
upper
(
)
)
    
if
maybe
:
        
log
(
            
logging
.
DEBUG
            
"
msix
"
            
{
"
binary
"
:
binary
"
path
"
:
maybe
}
            
"
Found
{
binary
}
in
environment
:
{
path
}
"
        
)
        
return
mozpath
.
normsep
(
maybe
)
    
maybe
=
which
(
        
binary
extra_search_dirs
=
[
"
c
:
/
Windows
/
System32
/
WindowsPowershell
/
v1
.
0
"
]
    
)
    
if
maybe
:
        
log
(
            
logging
.
DEBUG
            
"
msix
"
            
{
"
binary
"
:
binary
"
path
"
:
maybe
}
            
"
Found
{
binary
}
on
path
:
{
path
}
"
        
)
        
return
mozpath
.
normsep
(
maybe
)
    
sdk
=
os
.
environ
.
get
(
"
WINDOWSSDKDIR
"
)
or
"
C
:
/
Program
Files
(
x86
)
/
Windows
Kits
/
10
"
    
log
(
        
logging
.
DEBUG
        
"
msix
"
        
{
"
binary
"
:
binary
"
sdk
"
:
sdk
}
        
"
Looking
for
{
binary
}
in
Windows
SDK
:
{
sdk
}
"
    
)
    
if
sdk
:
        
finder
=
FileFinder
(
sdk
)
        
is_64bits
=
sys
.
maxsize
>
2
*
*
32
        
arch
=
"
x64
"
if
is_64bits
else
"
x86
"
        
for
p
f
in
finder
.
find
(
            
"
bin
/
*
*
/
{
arch
}
/
{
binary
}
.
exe
"
.
format
(
arch
=
arch
binary
=
binary
)
        
)
:
            
maybe
=
mozpath
.
normsep
(
mozpath
.
join
(
sdk
p
)
)
            
log
(
                
logging
.
DEBUG
                
"
msix
"
                
{
"
binary
"
:
binary
"
path
"
:
maybe
}
                
"
Found
{
binary
}
in
Windows
SDK
:
{
path
}
"
            
)
            
return
maybe
    
return
None
def
get_embedded_version
(
version
buildid
)
:
    
r
"
"
"
Turn
a
display
version
into
"
dotted
quad
"
notation
.
    
N
.
b
.
:
some
parts
of
the
MSIX
packaging
ecosystem
require
the
final
part
of
    
the
dotted
quad
to
be
identically
0
so
we
enforce
that
here
.
    
"
"
"
    
version
=
version
.
rsplit
(
"
esr
"
1
)
[
0
]
    
alpha
=
"
a
"
in
version
    
tail
=
None
    
if
"
a
"
in
version
:
        
head
tail
=
version
.
rsplit
(
"
a
"
1
)
        
if
tail
!
=
"
1
"
:
            
raise
ValueError
(
                
f
"
Alpha
version
not
of
the
form
X
.
0a1
is
not
supported
:
{
version
}
"
            
)
        
tail
=
buildid
    
elif
"
b
"
in
version
:
        
head
tail
=
version
.
rsplit
(
"
b
"
1
)
        
if
len
(
head
.
split
(
"
.
"
)
)
>
2
:
            
raise
ValueError
(
                
f
"
Beta
version
not
of
the
form
X
.
YbZ
is
not
supported
:
{
version
}
"
            
)
    
elif
"
rc
"
in
version
:
        
head
tail
=
version
.
rsplit
(
"
rc
"
1
)
        
if
len
(
head
.
split
(
"
.
"
)
)
>
2
:
            
raise
ValueError
(
                
f
"
Release
candidate
version
not
of
the
form
X
.
YrcZ
is
not
supported
:
{
version
}
"
            
)
    
else
:
        
head
=
version
    
components
=
(
head
.
split
(
"
.
"
)
+
[
"
0
"
"
0
"
"
0
"
]
)
[
:
3
]
    
if
tail
:
        
components
[
2
]
=
tail
    
if
alpha
:
        
if
components
[
1
]
!
=
"
0
"
:
            
raise
ValueError
(
                
f
"
Alpha
version
not
of
the
form
X
.
0a1
is
not
supported
:
{
version
}
"
            
)
        
year
=
buildid
[
2
:
4
]
        
if
year
[
0
]
=
=
"
0
"
:
            
year
=
year
[
1
:
]
        
month
=
buildid
[
4
:
6
]
        
day
=
buildid
[
6
:
8
]
        
if
day
[
0
]
=
=
"
0
"
:
            
day
=
day
[
1
:
]
        
hour
=
buildid
[
8
:
10
]
        
components
[
1
]
=
"
"
.
join
(
(
year
month
)
)
        
components
[
2
]
=
"
"
.
join
(
(
day
hour
)
)
    
version
=
"
{
}
.
{
}
.
{
}
.
0
"
.
format
(
*
components
)
    
return
version
def
repackage_msix
(
    
dir_or_package
    
channel
=
None
    
branding
=
None
    
template
=
None
    
distribution_dirs
=
[
]
    
locale_allowlist
=
set
(
)
    
version
=
None
    
vendor
=
None
    
displayname
=
None
    
app_name
=
"
firefox
"
    
identity
=
None
    
publisher
=
None
    
publisher_display_name
=
"
Mozilla
Corporation
"
    
arch
=
None
    
output
=
None
    
force
=
False
    
log
=
None
    
verbose
=
False
    
makeappx
=
None
)
:
    
if
not
channel
:
        
raise
Exception
(
"
channel
is
required
"
)
    
if
channel
not
in
[
"
official
"
"
beta
"
"
aurora
"
"
nightly
"
"
unofficial
"
]
:
        
raise
Exception
(
"
channel
is
unrecognized
:
{
}
"
.
format
(
channel
)
)
    
if
not
branding
:
        
raise
Exception
(
"
branding
dir
is
required
"
)
    
if
not
os
.
path
.
isdir
(
branding
)
:
        
raise
Exception
(
"
branding
dir
{
}
does
not
exist
"
.
format
(
branding
)
)
        
version
=
"
1
.
2
.
3
"
    
if
arch
is
None
or
arch
not
in
_MSIX_ARCH
.
keys
(
)
:
        
raise
Exception
(
            
"
arch
name
must
be
provided
and
one
of
{
}
.
"
.
format
(
_MSIX_ARCH
.
keys
(
)
)
        
)
    
if
not
os
.
path
.
exists
(
dir_or_package
)
:
        
raise
Exception
(
"
{
}
does
not
exist
"
.
format
(
dir_or_package
)
)
    
if
os
.
path
.
isdir
(
dir_or_package
)
:
        
finder
=
FileFinder
(
dir_or_package
)
    
else
:
        
finder
=
JarFinder
(
dir_or_package
JarReader
(
dir_or_package
)
)
    
values
=
get_application_ini_values
(
        
finder
        
dict
(
section
=
"
App
"
value
=
"
CodeName
"
fallback
=
"
Name
"
)
        
dict
(
section
=
"
App
"
value
=
"
Vendor
"
)
        
dict
(
section
=
"
App
"
value
=
"
Version
"
)
        
dict
(
section
=
"
App
"
value
=
"
BuildID
"
)
    
)
    
first
=
next
(
values
)
    
displayname
=
displayname
or
"
Mozilla
{
}
"
.
format
(
first
)
    
second
=
next
(
values
)
    
vendor
=
vendor
or
second
    
if
not
version
:
        
version
=
next
(
values
)
        
buildid
=
next
(
values
)
        
version
=
get_embedded_version
(
version
buildid
)
    
lines
=
[
        
line
        
for
line
in
open
(
mozpath
.
join
(
branding
"
configure
.
sh
"
)
)
.
readlines
(
)
        
if
"
MOZ_IGECKOBACKCHANNEL_IID
"
in
line
    
]
    
MOZ_IGECKOBACKCHANNEL_IID
=
lines
[
-
1
]
    
_
_
MOZ_IGECKOBACKCHANNEL_IID
=
MOZ_IGECKOBACKCHANNEL_IID
.
partition
(
"
=
"
)
    
MOZ_IGECKOBACKCHANNEL_IID
=
MOZ_IGECKOBACKCHANNEL_IID
.
strip
(
)
    
if
MOZ_IGECKOBACKCHANNEL_IID
.
startswith
(
(
'
"
'
"
'
"
)
)
:
        
MOZ_IGECKOBACKCHANNEL_IID
=
MOZ_IGECKOBACKCHANNEL_IID
[
1
:
-
1
]
    
unpack_finder
=
UnpackFinder
(
finder
)
    
lines
=
[
]
    
for
_
f
in
unpack_finder
.
find
(
"
*
*
/
chrome
/
en
-
US
/
locale
/
branding
/
brand
.
properties
"
)
:
        
lines
.
extend
(
            
line
            
for
line
in
f
.
open
(
)
.
read
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
.
splitlines
(
)
            
if
"
brandFullName
"
in
line
        
)
    
(
brandFullName
)
=
lines
    
_
_
brandFullName
=
brandFullName
.
partition
(
"
=
"
)
    
brandFullName
=
brandFullName
.
strip
(
)
    
output_dir
=
mozpath
.
normsep
(
        
mozpath
.
join
(
            
get_state_dir
(
)
"
cache
"
"
mach
-
msix
"
"
msix
-
temp
-
{
}
"
.
format
(
channel
)
        
)
    
)
    
if
channel
=
=
"
beta
"
:
        
displayname
+
=
"
Beta
"
        
brandFullName
+
=
"
Beta
"
    
instdir
=
"
{
}
Package
Root
"
.
format
(
displayname
)
    
identity
=
identity
or
"
{
}
.
{
}
"
.
format
(
vendor
displayname
)
.
replace
(
"
"
"
"
)
    
package_output_name
=
"
{
identity
}
_
{
version
}
_
{
arch
}
"
.
format
(
        
identity
=
identity
version
=
version
arch
=
_MSIX_ARCH
[
arch
]
    
)
    
default_output
=
mozpath
.
normsep
(
        
mozpath
.
join
(
            
get_state_dir
(
)
"
cache
"
"
mach
-
msix
"
"
{
}
.
msix
"
.
format
(
package_output_name
)
        
)
    
)
    
output
=
output
or
default_output
    
log
(
logging
.
INFO
"
msix
"
{
"
output
"
:
output
}
"
Repackaging
to
:
{
output
}
"
)
    
m
=
InstallManifest
(
)
    
m
.
add_copy
(
mozpath
.
join
(
template
"
Resources
.
pri
"
)
"
Resources
.
pri
"
)
    
m
.
add_pattern_copy
(
mozpath
.
join
(
branding
"
msix
"
"
Assets
"
)
"
*
*
"
"
Assets
"
)
    
m
.
add_pattern_copy
(
mozpath
.
join
(
template
"
VFS
"
)
"
*
*
"
"
VFS
"
)
    
copier
=
FileCopier
(
)
    
for
p
f
in
finder
:
        
pp
=
os
.
path
.
relpath
(
p
"
firefox
"
)
        
copier
.
add
(
mozpath
.
normsep
(
mozpath
.
join
(
"
VFS
"
"
ProgramFiles
"
instdir
pp
)
)
f
)
    
locales
=
set
(
[
"
en
-
US
"
]
)
    
for
distribution_dir
in
[
        
mozpath
.
join
(
template
"
distribution
"
)
    
]
+
distribution_dirs
:
        
log
(
            
logging
.
INFO
            
"
msix
"
            
{
"
dir
"
:
distribution_dir
}
            
"
Adding
distribution
files
from
{
dir
}
"
        
)
        
finder
=
FileFinder
(
distribution_dir
)
        
for
p
f
in
finder
:
            
locale
=
None
            
if
os
.
path
.
basename
(
p
)
=
=
"
target
.
langpack
.
xpi
"
:
                
base
locale
=
os
.
path
.
split
(
os
.
path
.
dirname
(
p
)
)
                
dest
=
mozpath
.
normsep
(
                    
mozpath
.
join
(
                        
base
                        
f
"
locale
-
{
locale
}
"
                        
f
"
langpack
-
{
locale
}
firefox
.
mozilla
.
org
.
xpi
"
                    
)
                
)
                
log
(
                    
logging
.
DEBUG
                    
"
msix
"
                    
{
"
path
"
:
p
"
dest
"
:
dest
}
                    
"
Renaming
langpack
{
path
}
to
{
dest
}
"
                
)
            
else
:
                
dest
=
p
            
if
locale
:
                
locale
=
locale
.
strip
(
)
.
lower
(
)
                
locales
.
add
(
locale
)
                
log
(
                    
logging
.
DEBUG
                    
"
msix
"
                    
{
"
locale
"
:
locale
"
dest
"
:
dest
}
                    
"
Distributing
locale
'
{
locale
}
'
from
{
dest
}
"
                
)
            
copier
.
add
(
                
mozpath
.
normsep
(
                    
mozpath
.
join
(
"
VFS
"
"
ProgramFiles
"
instdir
"
distribution
"
dest
)
                
)
                
f
            
)
    
locales
.
remove
(
"
en
-
US
"
)
    
unadvertised
=
set
(
)
    
if
locale_allowlist
:
        
unadvertised
=
locales
-
locale_allowlist
        
locales
=
locales
&
locale_allowlist
    
for
locale
in
sorted
(
unadvertised
)
:
        
log
(
            
logging
.
INFO
            
"
msix
"
            
{
"
locale
"
:
locale
}
            
"
Not
advertising
distributed
locale
'
{
locale
}
'
that
is
not
recognized
by
Windows
"
        
)
    
locales
=
[
"
en
-
US
"
]
+
list
(
sorted
(
locales
)
)
    
resource_language_list
=
"
\
n
"
.
join
(
        
f
'
<
Resource
Language
=
"
{
locale
}
"
/
>
'
for
locale
in
sorted
(
locales
)
    
)
    
defines
=
{
        
"
APPX_ARCH
"
:
_MSIX_ARCH
[
arch
]
        
"
APPX_DISPLAYNAME
"
:
brandFullName
        
"
APPX_DESCRIPTION
"
:
brandFullName
        
"
APPX_IDENTITY
"
:
identity
        
"
APPX_INSTDIR
"
:
instdir
        
"
APPX_INSTDIR_QUOTED
"
:
urllib
.
parse
.
quote
(
instdir
)
        
"
APPX_PUBLISHER
"
:
publisher
        
"
APPX_PUBLISHER_DISPLAY_NAME
"
:
publisher_display_name
        
"
APPX_RESOURCE_LANGUAGE_LIST
"
:
resource_language_list
        
"
APPX_VERSION
"
:
version
        
"
MOZ_APP_DISPLAYNAME
"
:
displayname
        
"
MOZ_APP_NAME
"
:
app_name
        
"
MOZ_IGECKOBACKCHANNEL_IID
"
:
MOZ_IGECKOBACKCHANNEL_IID
    
}
    
m
.
add_preprocess
(
        
mozpath
.
join
(
template
"
AppxManifest
.
xml
.
in
"
)
        
"
AppxManifest
.
xml
"
        
[
]
        
defines
=
defines
        
marker
=
"
<
!
-
-
#
"
    
)
    
m
.
populate_registry
(
copier
)
    
output_dir
=
mozpath
.
abspath
(
output_dir
)
    
ensureParentDir
(
output_dir
)
    
start
=
time
.
time
(
)
    
result
=
copier
.
copy
(
        
output_dir
remove_empty_directories
=
True
skip_if_older
=
not
force
    
)
    
if
log
:
        
log_copy_result
(
log
time
.
time
(
)
-
start
output_dir
result
)
    
if
not
makeappx
:
        
makeappx
=
find_sdk_tool
(
"
makeappx
.
exe
"
log
=
log
)
    
if
not
makeappx
:
        
raise
ValueError
(
            
"
makeappx
is
required
;
"
"
set
SIGNTOOL
or
WINDOWSSDKDIR
or
PATH
"
        
)
    
stdout
=
subprocess
.
run
(
        
[
makeappx
]
check
=
False
capture_output
=
True
universal_newlines
=
True
    
)
.
stdout
    
is_makeappx
=
"
MakeAppx
Tool
"
in
stdout
    
if
is_makeappx
:
        
args
=
[
makeappx
"
pack
"
"
/
d
"
output_dir
"
/
p
"
output
"
/
overwrite
"
]
    
else
:
        
args
=
[
makeappx
"
pack
"
"
-
d
"
output_dir
"
-
p
"
output
]
    
if
verbose
and
is_makeappx
:
        
args
.
append
(
"
/
verbose
"
)
    
joined
=
"
"
.
join
(
shlex_quote
(
arg
)
for
arg
in
args
)
    
log
(
logging
.
INFO
"
msix
"
{
"
args
"
:
args
"
joined
"
:
joined
}
"
Invoking
:
{
joined
}
"
)
    
sys
.
stdout
.
flush
(
)
    
if
verbose
:
        
subprocess
.
check_call
(
args
universal_newlines
=
True
)
    
else
:
        
try
:
            
subprocess
.
check_output
(
args
universal_newlines
=
True
)
        
except
subprocess
.
CalledProcessError
as
e
:
            
sys
.
stderr
.
write
(
e
.
output
)
            
raise
    
return
output
def
sign_msix
(
output
force
=
False
log
=
None
verbose
=
False
)
:
    
"
"
"
Sign
an
MSIX
with
a
locally
generated
self
-
signed
certificate
.
"
"
"
    
if
sys
.
platform
!
=
"
win32
"
:
        
raise
Exception
(
"
sign
msix
only
works
on
Windows
"
)
    
powershell_exe
=
find_sdk_tool
(
"
powershell
.
exe
"
log
=
log
)
    
if
not
powershell_exe
:
        
raise
ValueError
(
"
powershell
is
required
;
"
"
set
POWERSHELL
or
PATH
"
)
    
def
powershell
(
argstring
check
=
True
)
:
        
"
Invoke
powershell
.
exe
.
Arguments
are
given
as
a
string
to
allow
consumer
to
quote
.
"
        
args
=
[
powershell_exe
"
-
c
"
argstring
]
        
joined
=
"
"
.
join
(
shlex_quote
(
arg
)
for
arg
in
args
)
        
log
(
            
logging
.
INFO
"
msix
"
{
"
args
"
:
args
"
joined
"
:
joined
}
"
Invoking
:
{
joined
}
"
        
)
        
return
subprocess
.
run
(
            
args
check
=
check
universal_newlines
=
True
capture_output
=
True
        
)
.
stdout
    
signtool
=
find_sdk_tool
(
"
signtool
.
exe
"
log
=
log
)
    
if
not
signtool
:
        
raise
ValueError
(
            
"
signtool
is
required
;
"
"
set
SIGNTOOL
or
WINDOWSSDKDIR
or
PATH
"
        
)
    
vendor
=
"
Mozilla
"
    
publisher
=
"
CN
=
Mozilla
Corporation
OU
=
MSIX
Packaging
"
    
friendly_name
=
"
Mozilla
Corporation
MSIX
Packaging
Test
Certificate
"
    
crt_path
=
mozpath
.
join
(
        
get_state_dir
(
)
        
"
cache
"
        
"
mach
-
msix
"
        
"
{
}
.
crt
"
.
format
(
friendly_name
)
.
replace
(
"
"
"
_
"
)
.
lower
(
)
    
)
    
crt_path
=
mozpath
.
abspath
(
crt_path
)
    
ensureParentDir
(
crt_path
)
    
pfx_path
=
crt_path
.
replace
(
"
.
crt
"
"
.
pfx
"
)
    
password
=
"
193dbfc6
-
8ff7
-
4a95
-
8f32
-
6b4468626bd0
"
    
if
force
or
not
os
.
path
.
isfile
(
crt_path
)
:
        
log
(
            
logging
.
INFO
            
"
msix
"
            
{
"
crt_path
"
:
crt_path
}
            
"
Creating
new
self
signed
certificate
at
:
{
}
"
.
format
(
crt_path
)
        
)
        
thumbprints
=
[
            
thumbprint
.
strip
(
)
            
for
thumbprint
in
powershell
(
                
(
                    
"
Get
-
ChildItem
-
Path
Cert
:
\
CurrentUser
\
My
"
                    
'
|
Where
-
Object
{
{
_
.
Subject
-
Match
"
{
}
"
}
}
'
                    
'
|
Where
-
Object
{
{
_
.
FriendlyName
-
Match
"
{
}
"
}
}
'
                    
"
|
Select
-
Object
-
ExpandProperty
Thumbprint
"
                
)
.
format
(
vendor
friendly_name
)
            
)
.
splitlines
(
)
        
]
        
if
len
(
thumbprints
)
>
1
:
            
raise
Exception
(
                
"
Multiple
certificates
with
friendly
name
found
:
{
}
"
.
format
(
                    
friendly_name
                
)
            
)
        
if
len
(
thumbprints
)
=
=
1
:
            
thumbprint
=
thumbprints
[
0
]
        
else
:
            
thumbprint
=
None
        
if
not
thumbprint
:
            
thumbprint
=
(
                
powershell
(
                    
(
                        
'
New
-
SelfSignedCertificate
-
Type
Custom
-
Subject
"
{
}
"
'
                        
'
-
KeyUsage
DigitalSignature
-
FriendlyName
"
{
}
"
'
                        
"
-
CertStoreLocation
Cert
:
\
CurrentUser
\
My
"
                        
'
-
TextExtension
(
"
2
.
5
.
29
.
37
=
{
{
text
}
}
1
.
3
.
6
.
1
.
5
.
5
.
7
.
3
.
3
"
'
                        
'
"
2
.
5
.
29
.
19
=
{
{
text
}
}
"
)
'
                        
"
|
Select
-
Object
-
ExpandProperty
Thumbprint
"
                    
)
.
format
(
publisher
friendly_name
)
                
)
                
.
strip
(
)
                
.
upper
(
)
            
)
        
if
not
thumbprint
:
            
raise
Exception
(
                
"
Failed
to
find
or
create
certificate
with
friendly
name
:
{
}
"
.
format
(
                    
friendly_name
                
)
            
)
        
powershell
(
            
'
Export
-
Certificate
-
Cert
Cert
:
\
CurrentUser
\
My
\
{
}
-
FilePath
"
{
}
"
'
.
format
(
                
thumbprint
crt_path
            
)
        
)
        
log
(
            
logging
.
INFO
            
"
msix
"
            
{
"
crt_path
"
:
crt_path
}
            
"
Exported
public
certificate
:
{
crt_path
}
"
        
)
        
powershell
(
            
(
                
'
Export
-
PfxCertificate
-
Cert
Cert
:
\
CurrentUser
\
My
\
{
}
-
FilePath
"
{
}
"
'
                
'
-
Password
(
ConvertTo
-
SecureString
-
String
"
{
}
"
-
Force
-
AsPlainText
)
'
            
)
.
format
(
thumbprint
pfx_path
password
)
        
)
        
log
(
            
logging
.
INFO
            
"
msix
"
            
{
"
pfx_path
"
:
pfx_path
}
            
"
Exported
private
certificate
:
{
pfx_path
}
"
        
)
    
log
(
        
logging
.
INFO
        
"
msix
"
        
{
"
crt_path
"
:
crt_path
}
        
"
Signing
with
existing
self
signed
certificate
:
{
crt_path
}
"
    
)
    
thumbprints
=
[
        
thumbprint
.
strip
(
)
        
for
thumbprint
in
powershell
(
            
'
Get
-
PfxCertificate
-
FilePath
"
{
}
"
|
Select
-
Object
-
ExpandProperty
Thumbprint
'
.
format
(
                
crt_path
            
)
        
)
.
splitlines
(
)
    
]
    
if
len
(
thumbprints
)
>
1
:
        
raise
Exception
(
"
Multiple
thumbprints
found
for
PFX
:
{
}
"
.
format
(
pfx_path
)
)
    
if
len
(
thumbprints
)
=
=
0
:
        
raise
Exception
(
"
No
thumbprints
found
for
PFX
:
{
}
"
.
format
(
pfx_path
)
)
    
thumbprint
=
thumbprints
[
0
]
    
log
(
        
logging
.
INFO
        
"
msix
"
        
{
"
thumbprint
"
:
thumbprint
}
        
"
Signing
with
certificate
with
thumbprint
:
{
thumbprint
}
"
    
)
    
args
=
[
        
signtool
        
"
sign
"
        
"
/
a
"
        
"
/
fd
"
        
"
SHA256
"
        
"
/
f
"
        
pfx_path
        
"
/
p
"
        
password
        
output
    
]
    
if
not
verbose
:
        
subprocess
.
check_call
(
args
universal_newlines
=
True
)
    
else
:
        
try
:
            
subprocess
.
check_output
(
args
universal_newlines
=
True
)
        
except
subprocess
.
CalledProcessError
as
e
:
            
sys
.
stderr
.
write
(
e
.
output
)
            
raise
    
if
verbose
:
        
root_thumbprints
=
[
            
root_thumbprint
.
strip
(
)
            
for
root_thumbprint
in
powershell
(
                
"
Get
-
ChildItem
-
Path
Cert
:
\
LocalMachine
\
Root
\
{
}
"
                
"
|
Select
-
Object
-
ExpandProperty
Thumbprint
"
.
format
(
thumbprint
)
                
check
=
False
            
)
.
splitlines
(
)
        
]
        
if
thumbprint
not
in
root_thumbprints
:
            
log
(
                
logging
.
INFO
                
"
msix
"
                
{
"
thumbprint
"
:
thumbprint
}
                
"
Certificate
with
thumbprint
not
found
in
trusted
roots
:
{
thumbprint
}
"
            
)
            
log
(
                
logging
.
INFO
                
"
msix
"
                
{
"
crt_path
"
:
crt_path
"
output
"
:
output
}
                
r
"
"
"
\
#
Usage
To
trust
this
certificate
(
requires
an
elevated
shell
)
:
powershell
-
c
'
Import
-
Certificate
-
FilePath
"
{
crt_path
}
"
-
Cert
Cert
:
\
LocalMachine
\
Root
\
'
To
verify
this
MSIX
signature
exists
and
is
trusted
:
powershell
-
c
'
Get
-
AuthenticodeSignature
-
FilePath
"
{
output
}
"
|
Format
-
List
*
'
To
install
this
MSIX
:
powershell
-
c
'
Add
-
AppPackage
-
path
"
{
output
}
"
'
To
see
details
after
installing
:
powershell
-
c
'
Get
-
AppPackage
-
name
Mozilla
.
MozillaFirefox
(
Beta
.
.
.
)
'
                
"
"
"
.
strip
(
)
            
)
    
return
0
