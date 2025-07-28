"
"
"
Extracts
an
LLD
partition
from
an
ELF
file
.
"
"
"
import
argparse
import
hashlib
import
os
import
struct
import
subprocess
import
sys
import
tempfile
def
_ComputeNewBuildId
(
old_build_id
file_path
)
:
  
"
"
"
    
Computes
the
new
build
-
id
from
old
build
-
id
and
file_path
.
    
Args
:
      
old_build_id
:
Original
build
-
id
in
bytearray
.
      
file_path
:
Path
to
output
ELF
file
.
    
Returns
:
      
New
build
id
with
the
same
length
as
|
old_build_id
|
.
    
"
"
"
  
m
=
hashlib
.
sha256
(
)
  
m
.
update
(
old_build_id
)
  
m
.
update
(
os
.
path
.
basename
(
file_path
)
.
encode
(
'
utf
-
8
'
)
)
  
hash_bytes
=
m
.
digest
(
)
  
id_size
=
len
(
old_build_id
)
  
hash_size
=
len
(
hash_bytes
)
  
return
(
hash_bytes
*
(
id_size
/
/
hash_size
+
1
)
)
[
:
id_size
]
def
_ExtractPartition
(
objcopy
input_elf
output_elf
partition
)
:
  
"
"
"
  
Extracts
a
partition
from
an
ELF
file
.
  
For
partitions
other
than
main
partition
we
need
to
rewrite
  
the
.
note
.
gnu
.
build
-
id
section
so
that
the
build
-
id
remains
  
unique
.
  
Note
:
  
-
objcopy
does
not
modify
build
-
id
when
partitioning
the
    
combined
ELF
file
by
default
.
  
-
The
new
build
-
id
is
calculated
as
hash
of
original
build
-
id
    
and
partitioned
ELF
file
name
.
  
Args
:
    
objcopy
:
Path
to
objcopy
binary
.
    
input_elf
:
Path
to
input
ELF
file
.
    
output_elf
:
Path
to
output
ELF
file
.
    
partition
:
Partition
to
extract
from
combined
ELF
file
.
None
when
      
extracting
main
partition
.
  
"
"
"
  
if
not
partition
:
    
subprocess
.
check_call
(
        
[
objcopy
'
-
-
extract
-
main
-
partition
'
input_elf
output_elf
]
)
    
return
  
build_id_section
=
'
.
note
.
gnu
.
build
-
id
'
  
with
tempfile
.
TemporaryDirectory
(
)
as
tempdir
:
    
temp_elf
=
os
.
path
.
join
(
tempdir
'
obj_without_id
.
so
'
)
    
old_build_id_file
=
os
.
path
.
join
(
tempdir
'
old_build_id
'
)
    
new_build_id_file
=
os
.
path
.
join
(
tempdir
'
new_build_id
'
)
    
subprocess
.
check_call
(
[
        
objcopy
        
'
-
-
extract
-
partition
'
        
partition
        
'
-
-
dump
-
section
'
        
'
{
}
=
{
}
'
.
format
(
build_id_section
old_build_id_file
)
        
input_elf
        
temp_elf
    
]
)
    
with
open
(
old_build_id_file
'
rb
'
)
as
f
:
      
note_content
=
f
.
read
(
)
    
descsz
=
struct
.
Struct
(
'
<
4xL
'
)
.
unpack_from
(
note_content
)
    
prefix
=
note_content
[
:
-
descsz
]
    
build_id
=
note_content
[
-
descsz
:
]
    
with
open
(
new_build_id_file
'
wb
'
)
as
f
:
      
f
.
write
(
prefix
+
_ComputeNewBuildId
(
build_id
output_elf
)
)
    
subprocess
.
check_call
(
[
        
objcopy
        
'
-
-
update
-
section
'
        
'
{
}
=
{
}
'
.
format
(
build_id_section
new_build_id_file
)
        
temp_elf
        
output_elf
    
]
)
def
main
(
)
:
  
parser
=
argparse
.
ArgumentParser
(
description
=
__doc__
)
  
parser
.
add_argument
(
      
'
-
-
partition
'
      
help
=
'
Name
of
partition
if
not
the
main
partition
'
      
metavar
=
'
PART
'
)
  
parser
.
add_argument
(
      
'
-
-
objcopy
'
      
required
=
True
      
help
=
'
Path
to
llvm
-
objcopy
binary
'
      
metavar
=
'
FILE
'
)
  
parser
.
add_argument
(
      
'
-
-
unstripped
-
output
'
      
required
=
True
      
help
=
'
Unstripped
output
file
'
      
metavar
=
'
FILE
'
)
  
parser
.
add_argument
(
      
'
-
-
stripped
-
output
'
      
required
=
True
      
help
=
'
Stripped
output
file
'
      
metavar
=
'
FILE
'
)
  
parser
.
add_argument
(
'
-
-
split
-
dwarf
'
action
=
'
store_true
'
)
  
parser
.
add_argument
(
'
input
'
help
=
'
Input
file
'
)
  
args
=
parser
.
parse_args
(
)
  
_ExtractPartition
(
args
.
objcopy
args
.
input
args
.
unstripped_output
                    
args
.
partition
)
  
subprocess
.
check_call
(
[
      
args
.
objcopy
      
'
-
-
strip
-
all
'
      
args
.
unstripped_output
      
args
.
stripped_output
  
]
)
  
if
args
.
split_dwarf
:
    
dest
=
args
.
unstripped_output
+
'
.
dwp
'
    
try
:
      
os
.
unlink
(
dest
)
    
except
OSError
:
      
pass
    
relpath
=
os
.
path
.
relpath
(
args
.
input
+
'
.
dwp
'
os
.
path
.
dirname
(
dest
)
)
    
os
.
symlink
(
relpath
dest
)
if
__name__
=
=
'
__main__
'
:
  
sys
.
exit
(
main
(
)
)
