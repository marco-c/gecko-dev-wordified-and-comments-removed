import
json
import
os
import
pathlib
from
collections
import
OrderedDict
from
.
constant
import
Constant
from
.
transformer
import
SimplePerfherderTransformer
Transformer
get_transformer
class
PerftestETL
(
object
)
:
    
"
"
"
Controller
class
for
the
PerftestETL
.
"
"
"
    
def
__init__
(
        
self
        
file_groups
        
config
        
prefix
        
logger
        
custom_transform
=
None
        
sort_files
=
False
    
)
:
        
"
"
"
Initializes
PerftestETL
.
        
:
param
dict
file_groups
:
A
dict
of
file
groupings
.
The
value
            
of
each
of
the
dict
entries
is
the
name
of
the
data
that
            
will
be
produced
.
        
:
param
str
custom_transform
:
The
class
name
of
a
custom
transformer
.
        
"
"
"
        
self
.
fmt_data
=
{
}
        
self
.
file_groups
=
file_groups
        
self
.
config
=
config
        
self
.
sort_files
=
sort_files
        
self
.
const
=
Constant
(
)
        
self
.
prefix
=
prefix
        
self
.
logger
=
logger
        
tfms_dict
=
self
.
const
.
predefined_transformers
        
plugin_path
=
os
.
getenv
(
"
NOTEBOOK_PLUGIN
"
)
        
if
plugin_path
:
            
raise
Exception
(
"
NOTEBOOK_PLUGIN
is
currently
broken
.
"
)
        
if
custom_transform
:
            
try
:
                
tfm_cls
=
get_transformer
(
custom_transform
)
            
except
ImportError
:
                
tfm_cls
=
tfms_dict
.
get
(
custom_transform
)
            
if
tfm_cls
:
                
self
.
transformer
=
Transformer
(
                    
files
=
[
]
                    
custom_transformer
=
tfm_cls
(
)
                    
logger
=
self
.
logger
                    
prefix
=
self
.
prefix
                
)
                
self
.
logger
.
info
(
f
"
Found
{
custom_transform
}
transformer
"
self
.
prefix
)
            
else
:
                
raise
Exception
(
f
"
Could
not
get
a
{
custom_transform
}
transformer
.
"
)
        
else
:
            
self
.
transformer
=
Transformer
(
                
files
=
[
]
                
custom_transformer
=
SimplePerfherderTransformer
(
)
                
logger
=
self
.
logger
                
prefix
=
self
.
prefix
            
)
    
def
parse_file_grouping
(
self
file_grouping
)
:
        
"
"
"
Handles
differences
in
the
file_grouping
definitions
.
        
It
can
either
be
a
path
to
a
folder
containing
the
files
a
list
of
files
        
or
it
can
contain
settings
from
an
artifact_downloader
instance
.
        
:
param
file_grouping
:
A
file
grouping
entry
.
        
:
return
:
A
list
of
files
to
process
.
        
"
"
"
        
files
=
[
]
        
if
isinstance
(
file_grouping
list
)
:
            
files
=
file_grouping
        
elif
isinstance
(
file_grouping
dict
)
:
            
raise
Exception
(
                
"
Artifact
downloader
tooling
is
disabled
for
the
time
being
.
"
            
)
        
elif
isinstance
(
file_grouping
str
)
:
            
filepath
=
file_grouping
            
newf
=
[
f
.
resolve
(
)
.
as_posix
(
)
for
f
in
pathlib
.
Path
(
filepath
)
.
rglob
(
"
*
"
)
]
            
files
=
newf
        
else
:
            
raise
Exception
(
                
"
Unknown
file
grouping
type
provided
here
:
%
s
"
%
file_grouping
            
)
        
if
self
.
sort_files
:
            
if
isinstance
(
files
list
)
:
                
files
.
sort
(
)
            
else
:
                
for
_
file_list
in
files
.
items
(
)
:
                    
file_list
.
sort
(
)
                
files
=
OrderedDict
(
sorted
(
files
.
items
(
)
key
=
lambda
entry
:
entry
[
0
]
)
)
        
if
not
files
:
            
raise
Exception
(
                
"
Could
not
find
any
files
in
this
configuration
:
%
s
"
%
file_grouping
            
)
        
return
files
    
def
parse_output
(
self
)
:
        
prefix
=
"
"
if
"
prefix
"
not
in
self
.
config
else
self
.
config
[
"
prefix
"
]
        
filepath
=
f
"
{
prefix
}
std
-
output
.
json
"
        
if
"
output
"
in
self
.
config
:
            
filepath
=
self
.
config
[
"
output
"
]
        
if
os
.
path
.
isdir
(
filepath
)
:
            
filepath
=
os
.
path
.
join
(
filepath
f
"
{
prefix
}
std
-
output
.
json
"
)
        
return
filepath
    
def
process
(
self
*
*
kwargs
)
:
        
"
"
"
Process
the
file
groups
and
return
the
results
of
the
requested
analyses
.
        
:
return
:
All
the
results
in
a
dictionary
.
The
field
names
are
the
Analyzer
            
funtions
that
were
called
.
        
"
"
"
        
fmt_data
=
[
]
        
for
name
files
in
self
.
file_groups
.
items
(
)
:
            
files
=
self
.
parse_file_grouping
(
files
)
            
if
isinstance
(
files
dict
)
:
                
raise
Exception
(
                    
"
Artifact
downloader
tooling
is
disabled
for
the
time
being
.
"
                
)
            
else
:
                
self
.
transformer
.
files
=
files
                
trfm_data
=
self
.
transformer
.
process
(
name
*
*
kwargs
)
                
if
isinstance
(
trfm_data
list
)
:
                    
fmt_data
.
extend
(
trfm_data
)
                
else
:
                    
fmt_data
.
append
(
trfm_data
)
        
self
.
fmt_data
=
fmt_data
        
output_data_filepath
=
self
.
parse_output
(
)
        
print
(
"
Writing
results
to
%
s
"
%
output_data_filepath
)
        
with
open
(
output_data_filepath
"
w
"
)
as
f
:
            
json
.
dump
(
self
.
fmt_data
f
indent
=
4
sort_keys
=
True
)
        
return
{
"
data
"
:
self
.
fmt_data
"
file
-
output
"
:
output_data_filepath
}
