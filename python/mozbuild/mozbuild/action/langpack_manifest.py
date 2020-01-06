from
__future__
import
absolute_import
import
argparse
import
sys
import
os
import
json
import
io
from
mozpack
.
chrome
.
manifest
import
(
    
Manifest
    
ManifestLocale
    
parse_manifest
)
from
mozbuild
.
preprocessor
import
Preprocessor
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
'
w
'
encoding
=
'
utf
-
8
'
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
'
\
n
'
)
def
parse_defines
(
paths
)
:
    
pp
=
Preprocessor
(
)
    
for
path
in
paths
:
        
pp
.
do_include
(
path
)
    
return
pp
.
context
def
convert_contributors
(
str
)
:
    
str
=
str
.
replace
(
'
<
em
:
contributor
>
'
'
'
)
    
tokens
=
str
.
split
(
'
<
/
em
:
contributor
>
'
)
    
tokens
=
map
(
lambda
t
:
t
.
strip
(
)
tokens
)
    
tokens
=
filter
(
lambda
t
:
t
!
=
'
'
tokens
)
    
return
'
'
.
join
(
tokens
)
def
build_author_string
(
author
contributors
)
:
    
contrib
=
convert_contributors
(
contributors
)
    
if
len
(
contrib
)
=
=
0
:
        
return
author
    
return
'
{
0
}
(
contributors
:
{
1
}
)
'
.
format
(
author
contrib
)
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
'
os
'
:
            
raise
Exception
(
'
Unknown
flag
name
'
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
'
=
=
'
:
                
raise
Exception
(
'
Inequality
flag
cannot
be
converted
'
)
            
if
value
[
1
]
=
=
'
Android
'
:
                
ret
.
append
(
'
android
'
)
            
elif
value
[
1
]
=
=
'
LikeUnix
'
:
                
ret
.
append
(
'
linux
'
)
            
elif
value
[
1
]
=
=
'
Darwin
'
:
                
ret
.
append
(
'
macosx
'
)
            
elif
value
[
1
]
=
=
'
WINNT
'
:
                
ret
.
append
(
'
win
'
)
            
else
:
                
raise
Exception
(
'
Unknown
flag
value
{
0
}
'
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
            
chrome_entries
.
append
(
{
                
'
type
'
:
'
locale
'
                
'
alias
'
:
entry
.
name
                
'
locale
'
:
entry
.
id
                
'
platforms
'
:
convert_entry_flags_to_platform_codes
(
entry
.
flags
)
                
'
path
'
:
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
            
}
)
        
else
:
            
raise
Exception
(
'
Unknown
type
{
0
}
'
.
format
(
entry
.
name
)
)
def
create_webmanifest
(
locstr
min_app_ver
max_app_ver
app_name
                       
defines
chrome_entries
)
:
    
locales
=
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
'
'
)
)
    
main_locale
=
locales
[
0
]
    
author
=
build_author_string
(
        
defines
[
'
MOZ_LANGPACK_CREATOR
'
]
        
defines
[
'
MOZ_LANGPACK_CONTRIBUTORS
'
]
    
)
    
manifest
=
{
        
'
langpack_id
'
:
main_locale
        
'
manifest_version
'
:
2
        
'
applications
'
:
{
            
'
gecko
'
:
{
                
'
id
'
:
'
langpack
-
{
0
}
firefox
.
mozilla
.
org
'
.
format
(
main_locale
)
                
'
strict_min_version
'
:
min_app_ver
                
'
strict_max_version
'
:
max_app_ver
            
}
        
}
        
'
name
'
:
'
{
0
}
Language
Pack
'
.
format
(
defines
[
'
MOZ_LANG_TITLE
'
]
)
        
'
description
'
:
'
Language
pack
for
{
0
}
for
{
1
}
'
.
format
(
app_name
main_locale
)
        
'
version
'
:
min_app_ver
        
'
languages
'
:
{
}
        
'
sources
'
:
{
            
'
browser
'
:
{
                
'
base_path
'
:
'
browser
/
'
            
}
        
}
        
'
author
'
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
'
type
'
]
=
=
'
locale
'
:
            
platforms
=
entry
[
'
platforms
'
]
            
if
platforms
:
                
if
entry
[
'
alias
'
]
not
in
cr
:
                    
cr
[
entry
[
'
alias
'
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
'
alias
'
]
]
[
platform
]
=
entry
[
'
path
'
]
            
else
:
                
assert
entry
[
'
alias
'
]
not
in
cr
                
cr
[
entry
[
'
alias
'
]
]
=
entry
[
'
path
'
]
        
else
:
            
raise
Exception
(
'
Unknown
type
{
0
}
'
.
format
(
entry
[
'
type
'
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
'
languages
'
]
[
loc
]
=
{
            
'
version
'
:
min_app_ver
            
'
chrome_resources
'
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
encoding
=
'
utf8
'
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
'
-
-
locales
'
                        
help
=
'
List
of
language
codes
provided
by
the
langpack
'
)
    
parser
.
add_argument
(
'
-
-
min
-
app
-
ver
'
                        
help
=
'
Min
version
of
the
application
the
langpack
is
for
'
)
    
parser
.
add_argument
(
'
-
-
max
-
app
-
ver
'
                        
help
=
'
Max
version
of
the
application
the
langpack
is
for
'
)
    
parser
.
add_argument
(
'
-
-
app
-
name
'
                        
help
=
'
Name
of
the
application
the
langpack
is
for
'
)
    
parser
.
add_argument
(
'
-
-
defines
'
default
=
[
]
nargs
=
'
+
'
                        
help
=
'
List
of
defines
files
to
load
data
from
'
)
    
parser
.
add_argument
(
'
-
-
input
'
                        
help
=
'
Langpack
directory
.
'
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
'
chrome
.
manifest
'
)
args
.
input
chrome_entries
)
    
defines
=
parse_defines
(
args
.
defines
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
min_app_ver
        
args
.
max_app_ver
        
args
.
app_name
        
defines
        
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
'
manifest
.
json
'
)
res
)
if
__name__
=
=
'
__main__
'
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
