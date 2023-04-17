from
__future__
import
absolute_import
print_function
unicode_literals
import
codecs
import
errno
import
io
import
itertools
import
logging
import
os
import
sys
import
textwrap
try
:
    
from
collections
.
abc
import
Iterable
except
ImportError
:
    
from
collections
import
Iterable
base_dir
=
os
.
path
.
abspath
(
os
.
path
.
dirname
(
__file__
)
)
sys
.
path
.
insert
(
0
os
.
path
.
join
(
base_dir
"
python
"
"
mach
"
)
)
sys
.
path
.
insert
(
0
os
.
path
.
join
(
base_dir
"
python
"
"
mozboot
"
)
)
sys
.
path
.
insert
(
0
os
.
path
.
join
(
base_dir
"
python
"
"
mozbuild
"
)
)
sys
.
path
.
insert
(
0
os
.
path
.
join
(
base_dir
"
third_party
"
"
python
"
"
six
"
)
)
from
mozbuild
.
configure
import
(
    
ConfigureSandbox
    
TRACE
)
from
mozbuild
.
pythonutil
import
iter_modules_in_path
from
mozbuild
.
backend
.
configenvironment
import
PartialConfigEnvironment
from
mozbuild
.
util
import
write_indented_repr
import
mozpack
.
path
as
mozpath
import
six
def
main
(
argv
)
:
    
config
=
{
}
    
if
"
OLD_CONFIGURE
"
not
in
os
.
environ
:
        
os
.
environ
[
"
OLD_CONFIGURE
"
]
=
os
.
path
.
join
(
base_dir
"
old
-
configure
"
)
    
sandbox
=
ConfigureSandbox
(
config
os
.
environ
argv
)
    
clobber_file
=
"
CLOBBER
"
    
if
not
os
.
path
.
exists
(
clobber_file
)
:
        
with
open
(
clobber_file
"
a
"
)
:
            
pass
    
if
os
.
environ
.
get
(
"
MOZ_CONFIGURE_TRACE
"
)
:
        
sandbox
.
_logger
.
setLevel
(
TRACE
)
    
sandbox
.
run
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
__file__
)
"
moz
.
configure
"
)
)
    
if
sandbox
.
_help
:
        
return
0
    
logging
.
getLogger
(
"
moz
.
configure
"
)
.
info
(
"
Creating
config
.
status
"
)
    
old_js_configure_substs
=
config
.
pop
(
"
OLD_JS_CONFIGURE_SUBSTS
"
None
)
    
old_js_configure_defines
=
config
.
pop
(
"
OLD_JS_CONFIGURE_DEFINES
"
None
)
    
if
old_js_configure_substs
or
old_js_configure_defines
:
        
js_config
=
config
.
copy
(
)
        
pwd
=
os
.
getcwd
(
)
        
try
:
            
try
:
                
os
.
makedirs
(
"
js
/
src
"
)
            
except
OSError
as
e
:
                
if
e
.
errno
!
=
errno
.
EEXIST
:
                    
raise
            
os
.
chdir
(
"
js
/
src
"
)
            
js_config
[
"
OLD_CONFIGURE_SUBSTS
"
]
=
old_js_configure_substs
            
js_config
[
"
OLD_CONFIGURE_DEFINES
"
]
=
old_js_configure_defines
            
js_config
[
"
TOPOBJDIR
"
]
+
=
"
/
js
/
src
"
            
config_status
(
js_config
execute
=
False
)
        
finally
:
            
os
.
chdir
(
pwd
)
    
return
config_status
(
config
)
def
check_unicode
(
obj
)
:
    
"
"
"
Recursively
check
that
all
strings
in
the
object
are
unicode
strings
.
"
"
"
    
if
isinstance
(
obj
dict
)
:
        
result
=
True
        
for
k
v
in
six
.
iteritems
(
obj
)
:
            
if
not
check_unicode
(
k
)
:
                
print
(
"
%
s
key
is
not
unicode
.
"
%
k
file
=
sys
.
stderr
)
                
result
=
False
            
elif
not
check_unicode
(
v
)
:
                
print
(
"
%
s
value
is
not
unicode
.
"
%
k
file
=
sys
.
stderr
)
                
result
=
False
        
return
result
    
if
isinstance
(
obj
bytes
)
:
        
return
False
    
if
isinstance
(
obj
six
.
text_type
)
:
        
return
True
    
if
isinstance
(
obj
Iterable
)
:
        
return
all
(
check_unicode
(
o
)
for
o
in
obj
)
    
return
True
def
config_status
(
config
execute
=
True
)
:
    
def
sanitize_config
(
v
)
:
        
if
v
is
True
:
            
return
"
1
"
        
if
v
is
False
:
            
return
"
"
        
if
not
isinstance
(
v
(
bytes
six
.
text_type
dict
)
)
and
isinstance
(
v
Iterable
)
:
            
return
list
(
v
)
        
return
v
    
sanitized_config
=
{
}
    
sanitized_config
[
"
substs
"
]
=
{
        
k
:
sanitize_config
(
v
)
        
for
k
v
in
six
.
iteritems
(
config
)
        
if
k
        
not
in
(
            
"
DEFINES
"
            
"
TOPSRCDIR
"
            
"
TOPOBJDIR
"
            
"
CONFIG_STATUS_DEPS
"
            
"
OLD_CONFIGURE_SUBSTS
"
            
"
OLD_CONFIGURE_DEFINES
"
        
)
    
}
    
for
k
v
in
config
[
"
OLD_CONFIGURE_SUBSTS
"
]
:
        
sanitized_config
[
"
substs
"
]
[
k
]
=
sanitize_config
(
v
)
    
sanitized_config
[
"
defines
"
]
=
{
        
k
:
sanitize_config
(
v
)
for
k
v
in
six
.
iteritems
(
config
[
"
DEFINES
"
]
)
    
}
    
for
k
v
in
config
[
"
OLD_CONFIGURE_DEFINES
"
]
:
        
sanitized_config
[
"
defines
"
]
[
k
]
=
sanitize_config
(
v
)
    
sanitized_config
[
"
topsrcdir
"
]
=
config
[
"
TOPSRCDIR
"
]
    
sanitized_config
[
"
topobjdir
"
]
=
config
[
"
TOPOBJDIR
"
]
    
sanitized_config
[
"
mozconfig
"
]
=
config
.
get
(
"
MOZCONFIG
"
)
    
if
not
check_unicode
(
sanitized_config
)
:
        
print
(
"
Configuration
should
be
all
unicode
.
"
file
=
sys
.
stderr
)
        
print
(
"
Please
file
a
bug
for
the
above
.
"
file
=
sys
.
stderr
)
        
sys
.
exit
(
1
)
    
def
normalize
(
obj
)
:
        
if
isinstance
(
obj
dict
)
:
            
return
{
k
:
normalize
(
v
)
for
k
v
in
six
.
iteritems
(
obj
)
}
        
if
isinstance
(
obj
six
.
text_type
)
:
            
return
six
.
text_type
(
obj
)
        
if
isinstance
(
obj
Iterable
)
:
            
return
[
normalize
(
o
)
for
o
in
obj
]
        
return
obj
    
sanitized_config
=
normalize
(
sanitized_config
)
    
with
codecs
.
open
(
"
config
.
status
"
"
w
"
"
utf
-
8
"
)
as
fh
:
        
fh
.
write
(
            
textwrap
.
dedent
(
                
"
"
"
\
            
#
!
%
(
python
)
s
            
#
coding
=
utf
-
8
            
from
__future__
import
unicode_literals
        
"
"
"
            
)
            
%
{
"
python
"
:
config
[
"
PYTHON3
"
]
}
        
)
        
for
k
v
in
sorted
(
six
.
iteritems
(
sanitized_config
)
)
:
            
fh
.
write
(
"
%
s
=
"
%
k
)
            
write_indented_repr
(
fh
v
)
        
fh
.
write
(
            
"
__all__
=
[
'
topobjdir
'
'
topsrcdir
'
'
defines
'
"
"
'
substs
'
'
mozconfig
'
]
"
        
)
        
if
execute
:
            
fh
.
write
(
                
textwrap
.
dedent
(
                    
"
"
"
                
if
__name__
=
=
'
__main__
'
:
                    
from
mozbuild
.
config_status
import
config_status
                    
args
=
dict
(
[
(
name
globals
(
)
[
name
]
)
for
name
in
__all__
]
)
                    
config_status
(
*
*
args
)
            
"
"
"
                
)
            
)
    
partial_config
=
PartialConfigEnvironment
(
config
[
"
TOPOBJDIR
"
]
)
    
partial_config
.
write_vars
(
sanitized_config
)
    
with
io
.
open
(
"
config_status_deps
.
in
"
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
newline
=
"
\
n
"
)
as
fh
:
        
for
f
in
sorted
(
            
itertools
.
chain
(
                
config
[
"
CONFIG_STATUS_DEPS
"
]
                
iter_modules_in_path
(
config
[
"
TOPOBJDIR
"
]
config
[
"
TOPSRCDIR
"
]
)
            
)
        
)
:
            
fh
.
write
(
"
%
s
\
n
"
%
mozpath
.
normpath
(
f
)
)
    
os
.
chmod
(
"
config
.
status
"
0o755
)
    
if
execute
:
        
from
mozbuild
.
config_status
import
config_status
        
return
config_status
(
args
=
[
]
*
*
sanitized_config
)
    
return
0
if
__name__
=
=
"
__main__
"
:
    
sys
.
exit
(
main
(
sys
.
argv
)
)
