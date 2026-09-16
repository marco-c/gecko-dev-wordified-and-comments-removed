"
"
"
distutils
.
command
.
build_scripts
Implements
the
Distutils
'
build_scripts
'
command
.
"
"
"
import
os
import
re
import
tokenize
from
distutils
import
sysconfig
from
distutils
.
_log
import
log
from
stat
import
ST_MODE
from
.
.
_modified
import
newer
from
.
.
core
import
Command
from
.
.
util
import
convert_path
shebang_pattern
=
re
.
compile
(
'
^
#
!
.
*
python
[
0
-
9
.
]
*
(
[
\
t
]
.
*
)
?
'
)
"
"
"
Pattern
matching
a
Python
interpreter
indicated
in
first
line
of
a
script
.
"
"
"
first_line_re
=
shebang_pattern
class
build_scripts
(
Command
)
:
    
description
=
"
\
"
build
\
"
scripts
(
copy
and
fixup
#
!
line
)
"
    
user_options
=
[
        
(
'
build
-
dir
=
'
'
d
'
"
directory
to
\
"
build
\
"
(
copy
)
to
"
)
        
(
'
force
'
'
f
'
"
forcibly
build
everything
(
ignore
file
timestamps
"
)
        
(
'
executable
=
'
'
e
'
"
specify
final
destination
interpreter
path
"
)
    
]
    
boolean_options
=
[
'
force
'
]
    
def
initialize_options
(
self
)
:
        
self
.
build_dir
=
None
        
self
.
scripts
=
None
        
self
.
force
=
None
        
self
.
executable
=
None
    
def
finalize_options
(
self
)
:
        
self
.
set_undefined_options
(
            
'
build
'
            
(
'
build_scripts
'
'
build_dir
'
)
            
(
'
force
'
'
force
'
)
            
(
'
executable
'
'
executable
'
)
        
)
        
self
.
scripts
=
self
.
distribution
.
scripts
    
def
get_source_files
(
self
)
:
        
return
self
.
scripts
    
def
run
(
self
)
:
        
if
not
self
.
scripts
:
            
return
        
self
.
copy_scripts
(
)
    
def
copy_scripts
(
self
)
:
        
"
"
"
        
Copy
each
script
listed
in
self
.
scripts
.
        
If
a
script
is
marked
as
a
Python
script
(
first
line
matches
        
'
shebang_pattern
'
i
.
e
.
starts
with
#
!
and
contains
        
"
python
"
)
then
adjust
in
the
copy
the
first
line
to
refer
to
        
the
current
Python
interpreter
.
        
"
"
"
        
self
.
mkpath
(
self
.
build_dir
)
        
outfiles
=
[
]
        
updated_files
=
[
]
        
for
script
in
self
.
scripts
:
            
self
.
_copy_script
(
script
outfiles
updated_files
)
        
self
.
_change_modes
(
outfiles
)
        
return
outfiles
updated_files
    
def
_copy_script
(
self
script
outfiles
updated_files
)
:
        
shebang_match
=
None
        
script
=
convert_path
(
script
)
        
outfile
=
os
.
path
.
join
(
self
.
build_dir
os
.
path
.
basename
(
script
)
)
        
outfiles
.
append
(
outfile
)
        
if
not
self
.
force
and
not
newer
(
script
outfile
)
:
            
log
.
debug
(
"
not
copying
%
s
(
up
-
to
-
date
)
"
script
)
            
return
        
try
:
            
f
=
tokenize
.
open
(
script
)
        
except
OSError
:
            
if
not
self
.
dry_run
:
                
raise
            
f
=
None
        
else
:
            
first_line
=
f
.
readline
(
)
            
if
not
first_line
:
                
self
.
warn
(
f
"
{
script
}
is
an
empty
file
(
skipping
)
"
)
                
return
            
shebang_match
=
shebang_pattern
.
match
(
first_line
)
        
updated_files
.
append
(
outfile
)
        
if
shebang_match
:
            
log
.
info
(
"
copying
and
adjusting
%
s
-
>
%
s
"
script
self
.
build_dir
)
            
if
not
self
.
dry_run
:
                
if
not
sysconfig
.
python_build
:
                    
executable
=
self
.
executable
                
else
:
                    
executable
=
os
.
path
.
join
(
                        
sysconfig
.
get_config_var
(
"
BINDIR
"
)
                        
"
python
{
}
{
}
"
.
format
(
                            
sysconfig
.
get_config_var
(
"
VERSION
"
)
                            
sysconfig
.
get_config_var
(
"
EXE
"
)
                        
)
                    
)
                
post_interp
=
shebang_match
.
group
(
1
)
or
'
'
                
shebang
=
"
#
!
"
+
executable
+
post_interp
+
"
\
n
"
                
self
.
_validate_shebang
(
shebang
f
.
encoding
)
                
with
open
(
outfile
"
w
"
encoding
=
f
.
encoding
)
as
outf
:
                    
outf
.
write
(
shebang
)
                    
outf
.
writelines
(
f
.
readlines
(
)
)
            
if
f
:
                
f
.
close
(
)
        
else
:
            
if
f
:
                
f
.
close
(
)
            
self
.
copy_file
(
script
outfile
)
    
def
_change_modes
(
self
outfiles
)
:
        
if
os
.
name
!
=
'
posix
'
:
            
return
        
for
file
in
outfiles
:
            
self
.
_change_mode
(
file
)
    
def
_change_mode
(
self
file
)
:
        
if
self
.
dry_run
:
            
log
.
info
(
"
changing
mode
of
%
s
"
file
)
            
return
        
oldmode
=
os
.
stat
(
file
)
[
ST_MODE
]
&
0o7777
        
newmode
=
(
oldmode
|
0o555
)
&
0o7777
        
if
newmode
!
=
oldmode
:
            
log
.
info
(
"
changing
mode
of
%
s
from
%
o
to
%
o
"
file
oldmode
newmode
)
            
os
.
chmod
(
file
newmode
)
    
staticmethod
    
def
_validate_shebang
(
shebang
encoding
)
:
        
try
:
            
shebang
.
encode
(
'
utf
-
8
'
)
        
except
UnicodeEncodeError
:
            
raise
ValueError
(
f
"
The
shebang
(
{
shebang
!
r
}
)
is
not
encodable
to
utf
-
8
"
)
        
try
:
            
shebang
.
encode
(
encoding
)
        
except
UnicodeEncodeError
:
            
raise
ValueError
(
                
f
"
The
shebang
(
{
shebang
!
r
}
)
is
not
encodable
"
                
f
"
to
the
script
encoding
(
{
encoding
}
)
"
            
)
