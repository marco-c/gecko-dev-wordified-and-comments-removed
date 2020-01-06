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
    
ManifestOverride
    
ManifestResource
    
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
        
elif
isinstance
(
entry
ManifestOverride
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
override
'
                
'
real
-
path
'
:
entry
.
overloaded
                
'
overlay
-
path
'
:
entry
.
overload
            
}
)
        
elif
isinstance
(
entry
ManifestResource
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
resource
'
                
'
alias
'
:
entry
.
name
                
'
path
'
:
entry
.
target
            
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
%
s
'
%
entry
[
0
]
)
def
create_webmanifest
(
locstr
appver
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
    
contributors
=
convert_contributors
(
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
langpack
-
id
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
"
langpack
-
"
+
main_locale
+
"
mozilla
.
org
"
                
'
strict_min_version
'
:
appver
            
}
        
}
        
'
name
'
:
defines
[
'
MOZ_LANG_TITLE
'
]
+
'
Language
Pack
'
        
'
description
'
:
'
Language
pack
for
Firefox
for
'
+
main_locale
        
'
version
'
:
appver
        
'
languages
'
:
locales
        
'
author
'
:
'
%
s
(
contributors
:
%
s
)
'
%
(
defines
[
'
MOZ_LANGPACK_CREATOR
'
]
contributors
)
        
'
chrome_entries
'
:
[
        
]
    
}
    
for
entry
in
chrome_entries
:
        
line
=
'
'
        
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
            
line
=
'
%
s
%
s
%
s
%
s
'
%
(
                
entry
[
'
type
'
]
                
entry
[
'
alias
'
]
                
entry
[
'
locale
'
]
                
entry
[
'
path
'
]
            
)
        
elif
entry
[
'
type
'
]
=
=
'
override
'
:
            
line
=
'
%
s
%
s
%
s
'
%
(
                
entry
[
'
type
'
]
                
entry
[
'
real
-
path
'
]
                
entry
[
'
overlay
-
path
'
]
            
)
        
elif
entry
[
'
type
'
]
=
=
'
resource
'
:
            
line
=
'
%
s
%
s
%
s
'
%
(
                
entry
[
'
type
'
]
                
entry
[
'
alias
'
]
                
entry
[
'
path
'
]
            
)
        
else
:
            
raise
Exception
(
'
Unknown
type
%
s
'
%
entry
[
'
type
'
]
)
        
manifest
[
'
chrome_entries
'
]
.
append
(
line
)
    
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
appver
'
                        
help
=
'
Version
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
appver
        
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
