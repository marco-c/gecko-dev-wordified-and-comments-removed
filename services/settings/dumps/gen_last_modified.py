import
json
import
buildconfig
import
mozpack
.
path
as
mozpath
def
get_last_modified
(
full_path_to_remote_settings_dump_file
)
:
    
"
"
"
    
Get
the
last_modified
for
the
given
file
name
.
    
-
File
must
exist
    
-
Must
be
a
JSON
dictionary
with
a
data
list
e
.
g
.
{
"
data
"
:
[
]
}
    
-
Every
element
in
data
should
contain
a
"
last_modified
"
key
.
    
-
The
first
element
must
have
the
highest
"
last_modified
"
value
.
    
"
"
"
    
with
open
(
full_path_to_remote_settings_dump_file
"
r
"
)
as
f
:
        
records
=
json
.
load
(
f
)
[
"
data
"
]
        
assert
isinstance
(
records
list
)
    
last_modified
=
0
    
if
records
:
        
last_modified
=
records
[
0
]
[
"
last_modified
"
]
    
assert
isinstance
(
last_modified
int
)
    
return
last_modified
def
main
(
output
)
:
    
"
"
"
    
Generates
a
JSON
file
that
maps
"
bucket
/
collection
"
to
the
last_modified
    
value
within
.
    
Returns
a
set
of
the
file
locations
of
the
recorded
RemoteSettings
dumps
    
so
that
the
build
backend
can
invoke
this
script
again
when
needed
.
    
The
validity
of
the
JSON
file
is
verified
through
unit
tests
at
    
services
/
settings
/
test
/
unit
/
test_remote_settings_dump_lastmodified
.
js
    
"
"
"
    
assert
buildconfig
.
substs
[
"
MOZ_BUILD_APP
"
]
in
(
        
"
browser
"
        
"
mobile
/
android
"
        
"
comm
/
mail
"
        
"
comm
/
suite
"
    
)
    
remotesettings_dumps
=
{
}
    
if
buildconfig
.
substs
[
"
MOZ_BUILD_APP
"
]
!
=
"
mobile
/
android
"
:
        
remotesettings_dumps
[
"
blocklists
/
addons
-
bloomfilters
"
]
=
mozpath
.
join
(
            
buildconfig
.
topsrcdir
            
"
services
/
settings
/
dumps
/
blocklists
/
addons
-
bloomfilters
.
json
"
        
)
    
if
buildconfig
.
substs
[
"
MOZ_BUILD_APP
"
]
=
=
"
browser
"
:
        
remotesettings_dumps
[
"
main
/
search
-
config
"
]
=
mozpath
.
join
(
            
buildconfig
.
topsrcdir
            
"
services
/
settings
/
dumps
/
main
/
search
-
config
.
json
"
        
)
    
if
buildconfig
.
substs
[
"
MOZ_BUILD_APP
"
]
=
=
"
comm
/
mail
"
:
        
remotesettings_dumps
[
"
main
/
search
-
config
"
]
=
mozpath
.
join
(
            
buildconfig
.
topsrcdir
            
"
comm
/
mail
/
app
/
settings
/
dumps
/
thunderbird
/
search
-
config
.
json
"
        
)
    
output_dict
=
{
}
    
input_files
=
set
(
)
    
for
key
input_file
in
remotesettings_dumps
.
items
(
)
:
        
input_files
.
add
(
input_file
)
        
output_dict
[
key
]
=
get_last_modified
(
input_file
)
    
json
.
dump
(
output_dict
output
sort_keys
=
True
)
    
return
input_files
