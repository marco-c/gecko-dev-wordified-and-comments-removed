import
argparse
import
datetime
import
io
import
json
import
logging
import
os
import
sys
import
fluent
.
syntax
.
ast
as
FTL
import
mozpack
.
path
as
mozpath
import
mozversioncontrol
import
requests
from
fluent
.
syntax
.
parser
import
FluentParser
from
mozpack
.
chrome
.
manifest
import
Manifest
ManifestLocale
parse_manifest
from
mozbuild
.
configure
.
util
import
Version
def
write_file
(
path
content
)
:
    
with
io
.
open
(
path
"
w
"
encoding
=
"
utf
-
8
"
)
as
out
:
        
out
.
write
(
content
+
"
\
n
"
)
pushlog_api_url
=
"
{
0
}
/
json
-
rev
/
{
1
}
"
def
get_dt_from_hg
(
path
)
:
    
with
mozversioncontrol
.
get_repository_object
(
path
=
path
)
as
repo
:
        
phase
=
repo
.
_run
(
"
log
"
"
-
r
"
"
.
"
"
-
T
"
"
{
phase
}
"
)
        
if
phase
.
strip
(
)
!
=
"
public
"
:
            
return
datetime
.
datetime
.
utcnow
(
)
        
repo_url
=
repo
.
_run
(
"
paths
"
"
default
"
)
        
repo_url
=
repo_url
.
strip
(
)
.
replace
(
"
ssh
:
/
/
"
"
https
:
/
/
"
)
        
repo_url
=
repo_url
.
replace
(
"
hg
:
/
/
"
"
https
:
/
/
"
)
        
cs
=
repo
.
_run
(
"
log
"
"
-
r
"
"
.
"
"
-
T
"
"
{
node
}
"
)
    
url
=
pushlog_api_url
.
format
(
repo_url
cs
)
    
session
=
requests
.
Session
(
)
    
try
:
        
response
=
session
.
get
(
url
)
    
except
Exception
as
e
:
        
msg
=
"
Failed
to
retrieve
push
timestamp
using
{
}
\
nError
:
{
}
"
.
format
(
url
e
)
        
raise
Exception
(
msg
)
    
data
=
response
.
json
(
)
    
try
:
        
date
=
data
[
"
pushdate
"
]
[
0
]
    
except
KeyError
as
exc
:
        
msg
=
"
{
}
\
ndata
is
:
{
}
"
.
format
(
            
str
(
exc
)
json
.
dumps
(
data
indent
=
2
sort_keys
=
True
)
        
)
        
raise
KeyError
(
msg
)
    
return
datetime
.
datetime
.
utcfromtimestamp
(
date
)
def
get_timestamp_for_locale
(
path
)
:
    
dt
=
None
    
if
os
.
path
.
isdir
(
os
.
path
.
join
(
path
"
.
hg
"
)
)
:
        
dt
=
get_dt_from_hg
(
path
)
    
if
dt
is
None
:
        
dt
=
datetime
.
datetime
.
utcnow
(
)
    
dt
=
dt
.
replace
(
microsecond
=
0
)
    
return
dt
.
strftime
(
"
%
Y
%
m
%
d
%
H
%
M
%
S
"
)
def
parse_flat_ftl
(
path
)
:
    
parser
=
FluentParser
(
with_spans
=
False
)
    
try
:
        
with
open
(
path
encoding
=
"
utf
-
8
"
)
as
file
:
            
res
=
parser
.
parse
(
file
.
read
(
)
)
    
except
FileNotFoundError
as
err
:
        
logging
.
warning
(
err
)
        
return
{
}
    
result
=
{
}
    
for
entry
in
res
.
body
:
        
if
isinstance
(
entry
FTL
.
Message
)
and
isinstance
(
entry
.
value
FTL
.
Pattern
)
:
            
flat
=
"
"
            
for
elem
in
entry
.
value
.
elements
:
                
if
isinstance
(
elem
FTL
.
TextElement
)
:
                    
flat
+
=
elem
.
value
                
elif
isinstance
(
elem
.
expression
FTL
.
Literal
)
:
                    
flat
+
=
elem
.
expression
.
parse
(
)
[
"
value
"
]
                
else
:
                    
name
=
type
(
elem
.
expression
)
.
__name__
                    
raise
Exception
(
f
"
Unsupported
{
name
}
for
{
entry
.
id
.
name
}
in
{
path
}
"
)
            
result
[
entry
.
id
.
name
]
=
flat
.
strip
(
)
    
return
result
def
get_title_and_description
(
app
locale
)
:
    
dir
=
os
.
path
.
dirname
(
__file__
)
    
with
open
(
os
.
path
.
join
(
dir
"
langpack_localeNames
.
json
"
)
encoding
=
"
utf
-
8
"
)
as
nf
:
        
names
=
json
.
load
(
nf
)
    
nameCharLimit
=
45
    
descCharLimit
=
132
    
nameTemplate
=
"
Language
:
{
}
"
    
descTemplate
=
"
{
}
Language
Pack
for
{
}
"
    
if
locale
in
names
:
        
data
=
names
[
locale
]
        
native
=
data
[
"
native
"
]
        
english
=
data
[
"
english
"
]
if
"
english
"
in
data
else
native
        
if
english
!
=
native
:
            
title
=
nameTemplate
.
format
(
f
"
{
native
}
(
{
english
}
)
"
)
            
if
len
(
title
)
>
nameCharLimit
:
                
title
=
nameTemplate
.
format
(
native
)
            
description
=
descTemplate
.
format
(
app
f
"
{
native
}
(
{
locale
}
)
{
english
}
"
)
        
else
:
            
title
=
nameTemplate
.
format
(
native
)
            
description
=
descTemplate
.
format
(
app
f
"
{
native
}
(
{
locale
}
)
"
)
    
else
:
        
title
=
nameTemplate
.
format
(
locale
)
        
description
=
descTemplate
.
format
(
app
locale
)
    
return
title
[
:
nameCharLimit
]
description
[
:
descCharLimit
]
def
get_author
(
ftl
)
:
    
author
=
ftl
[
"
langpack
-
creator
"
]
if
"
langpack
-
creator
"
in
ftl
else
"
mozilla
.
org
"
    
contrib
=
ftl
[
"
langpack
-
contributors
"
]
if
"
langpack
-
contributors
"
in
ftl
else
"
"
    
if
contrib
:
        
return
f
"
{
author
}
(
contributors
:
{
contrib
}
)
"
    
else
:
        
return
author
def
convert_entry_flags_to_platform_codes
(
flags
)
:
    
if
not
flags
:
        
return
None
    
ret
=
[
]
    
for
key
in
flags
:
        
if
key
!
=
"
os
"
:
            
raise
Exception
(
"
Unknown
flag
name
"
)
        
for
value
in
flags
[
key
]
.
values
:
            
if
value
[
0
]
!
=
"
=
=
"
:
                
raise
Exception
(
"
Inequality
flag
cannot
be
converted
"
)
            
if
value
[
1
]
=
=
"
Android
"
:
                
ret
.
append
(
"
android
"
)
            
elif
value
[
1
]
=
=
"
LikeUnix
"
:
                
ret
.
append
(
"
linux
"
)
            
elif
value
[
1
]
=
=
"
Darwin
"
:
                
ret
.
append
(
"
macosx
"
)
            
elif
value
[
1
]
=
=
"
WINNT
"
:
                
ret
.
append
(
"
win
"
)
            
else
:
                
raise
Exception
(
"
Unknown
flag
value
{
0
}
"
.
format
(
value
[
1
]
)
)
    
return
ret
def
parse_chrome_manifest
(
path
base_path
chrome_entries
)
:
    
for
entry
in
parse_manifest
(
None
path
)
:
        
if
isinstance
(
entry
Manifest
)
:
            
parse_chrome_manifest
(
                
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
path
)
entry
.
relpath
)
                
base_path
                
chrome_entries
            
)
        
elif
isinstance
(
entry
ManifestLocale
)
:
            
entry_path
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
relpath
(
os
.
path
.
dirname
(
path
)
base_path
)
entry
.
relpath
            
)
            
chrome_entries
.
append
(
                
{
                    
"
type
"
:
"
locale
"
                    
"
alias
"
:
entry
.
name
                    
"
locale
"
:
entry
.
id
                    
"
platforms
"
:
convert_entry_flags_to_platform_codes
(
entry
.
flags
)
                    
"
path
"
:
mozpath
.
normsep
(
entry_path
)
                
}
            
)
        
else
:
            
raise
Exception
(
"
Unknown
type
{
0
}
"
.
format
(
entry
.
name
)
)
def
get_version_maybe_buildid
(
version
)
:
    
buildid
=
os
.
environ
.
get
(
"
MOZ_BUILD_DATE
"
)
    
if
buildid
and
len
(
buildid
)
!
=
14
:
        
print
(
"
Ignoring
invalid
MOZ_BUILD_DATE
:
%
s
"
%
buildid
file
=
sys
.
stderr
)
        
buildid
=
None
    
if
buildid
:
        
date
time
=
buildid
[
:
8
]
buildid
[
8
:
]
        
version
=
f
"
{
version
}
buildid
{
date
}
.
{
time
}
"
    
return
version
def
create_webmanifest
(
    
locstr
    
version
    
min_app_ver
    
max_app_ver
    
app_name
    
l10n_basedir
    
langpack_eid
    
ftl
    
chrome_entries
)
:
    
locales
=
list
(
map
(
lambda
loc
:
loc
.
strip
(
)
locstr
.
split
(
"
"
)
)
)
    
main_locale
=
locales
[
0
]
    
title
description
=
get_title_and_description
(
app_name
main_locale
)
    
author
=
get_author
(
ftl
)
    
manifest
=
{
        
"
langpack_id
"
:
main_locale
        
"
manifest_version
"
:
2
        
"
applications
"
:
{
            
"
gecko
"
:
{
                
"
id
"
:
langpack_eid
                
"
strict_min_version
"
:
min_app_ver
                
"
strict_max_version
"
:
max_app_ver
            
}
        
}
        
"
name
"
:
title
        
"
description
"
:
description
        
"
version
"
:
get_version_maybe_buildid
(
version
)
        
"
languages
"
:
{
}
        
"
sources
"
:
{
"
browser
"
:
{
"
base_path
"
:
"
browser
/
"
}
}
        
"
author
"
:
author
    
}
    
cr
=
{
}
    
for
entry
in
chrome_entries
:
        
if
entry
[
"
type
"
]
=
=
"
locale
"
:
            
platforms
=
entry
[
"
platforms
"
]
            
if
platforms
:
                
if
entry
[
"
alias
"
]
not
in
cr
:
                    
cr
[
entry
[
"
alias
"
]
]
=
{
}
                
for
platform
in
platforms
:
                    
cr
[
entry
[
"
alias
"
]
]
[
platform
]
=
entry
[
"
path
"
]
            
else
:
                
assert
entry
[
"
alias
"
]
not
in
cr
                
cr
[
entry
[
"
alias
"
]
]
=
entry
[
"
path
"
]
        
else
:
            
raise
Exception
(
"
Unknown
type
{
0
}
"
.
format
(
entry
[
"
type
"
]
)
)
    
for
loc
in
locales
:
        
manifest
[
"
languages
"
]
[
loc
]
=
{
            
"
version
"
:
get_timestamp_for_locale
(
os
.
path
.
join
(
l10n_basedir
loc
)
)
            
"
chrome_resources
"
:
cr
        
}
    
return
json
.
dumps
(
manifest
indent
=
2
ensure_ascii
=
False
)
def
main
(
args
)
:
    
parser
=
argparse
.
ArgumentParser
(
)
    
parser
.
add_argument
(
        
"
-
-
locales
"
help
=
"
List
of
language
codes
provided
by
the
langpack
"
    
)
    
parser
.
add_argument
(
"
-
-
app
-
version
"
help
=
"
Version
of
the
application
"
)
    
parser
.
add_argument
(
        
"
-
-
max
-
app
-
ver
"
help
=
"
Max
version
of
the
application
the
langpack
is
for
"
    
)
    
parser
.
add_argument
(
        
"
-
-
app
-
name
"
help
=
"
Name
of
the
application
the
langpack
is
for
"
    
)
    
parser
.
add_argument
(
        
"
-
-
l10n
-
basedir
"
help
=
"
Base
directory
for
locales
used
in
the
language
pack
"
    
)
    
parser
.
add_argument
(
        
"
-
-
langpack
-
eid
"
help
=
"
Language
pack
id
to
use
for
this
locale
"
    
)
    
parser
.
add_argument
(
        
"
-
-
metadata
"
        
help
=
"
FTL
file
defining
langpack
metadata
"
    
)
    
parser
.
add_argument
(
"
-
-
input
"
help
=
"
Langpack
directory
.
"
)
    
args
=
parser
.
parse_args
(
args
)
    
chrome_entries
=
[
]
    
parse_chrome_manifest
(
        
os
.
path
.
join
(
args
.
input
"
chrome
.
manifest
"
)
args
.
input
chrome_entries
    
)
    
ftl
=
parse_flat_ftl
(
args
.
metadata
)
    
min_app_version
=
args
.
app_version
    
if
"
a
"
not
in
min_app_version
:
        
v
=
Version
(
min_app_version
)
        
if
args
.
app_name
=
=
"
SeaMonkey
"
:
            
min_app_version
=
"
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
v
.
major
v
.
minor
)
        
else
:
            
min_app_version
=
"
{
}
.
0
"
.
format
(
v
.
major
)
    
res
=
create_webmanifest
(
        
args
.
locales
        
args
.
app_version
        
min_app_version
        
args
.
max_app_ver
        
args
.
app_name
        
args
.
l10n_basedir
        
args
.
langpack_eid
        
ftl
        
chrome_entries
    
)
    
write_file
(
os
.
path
.
join
(
args
.
input
"
manifest
.
json
"
)
res
)
if
__name__
=
=
"
__main__
"
:
    
main
(
sys
.
argv
[
1
:
]
)
