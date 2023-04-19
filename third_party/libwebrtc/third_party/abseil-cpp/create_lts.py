"
"
"
A
script
to
do
source
transformations
to
create
a
new
LTS
release
.
   
Usage
:
.
/
create_lts
.
py
YYYYMMDD
"
"
"
import
sys
def
ReplaceStringsInFile
(
filename
replacement_dict
)
:
  
"
"
"
Performs
textual
replacements
in
a
file
.
  
Rewrites
filename
with
the
keys
in
replacement_dict
replaced
with
  
their
values
.
This
function
assumes
the
file
can
fit
in
memory
.
  
Args
:
    
filename
:
the
filename
to
perform
the
replacement
on
    
replacement_dict
:
a
dictionary
of
key
strings
to
be
replaced
with
their
      
values
  
Raises
:
    
Exception
:
A
failure
occured
  
"
"
"
  
f
=
open
(
filename
'
r
'
)
  
content
=
f
.
read
(
)
  
f
.
close
(
)
  
for
key
value
in
replacement_dict
.
items
(
)
:
    
original
=
content
    
content
=
content
.
replace
(
key
value
)
    
if
content
=
=
original
:
      
raise
Exception
(
'
Failed
to
find
{
}
in
{
}
'
.
format
(
key
filename
)
)
  
f
=
open
(
filename
'
w
'
)
  
f
.
write
(
content
)
  
f
.
close
(
)
def
StripContentBetweenTags
(
filename
strip_begin_tag
strip_end_tag
)
:
  
"
"
"
Strip
contents
from
a
file
.
  
Rewrites
filename
with
by
removing
all
content
between
  
strip_begin_tag
and
strip_end_tag
including
the
tags
themselves
.
  
Args
:
    
filename
:
the
filename
to
perform
the
replacement
on
    
strip_begin_tag
:
the
start
of
the
content
to
be
removed
    
strip_end_tag
:
the
end
of
the
content
to
be
removed
  
Raises
:
    
Exception
:
A
failure
occured
  
"
"
"
  
f
=
open
(
filename
'
r
'
)
  
content
=
f
.
read
(
)
  
f
.
close
(
)
  
while
True
:
    
begin
=
content
.
find
(
strip_begin_tag
)
    
if
begin
=
=
-
1
:
      
break
    
end
=
content
.
find
(
strip_end_tag
begin
+
len
(
strip_begin_tag
)
)
    
if
end
=
=
-
1
:
      
raise
Exception
(
'
{
}
:
imbalanced
strip
begin
(
{
}
)
and
'
                      
'
end
(
{
}
)
tags
'
.
format
(
filename
strip_begin_tag
                                             
strip_end_tag
)
)
    
content
=
content
.
replace
(
content
[
begin
:
end
+
len
(
strip_end_tag
)
]
'
'
)
  
f
=
open
(
filename
'
w
'
)
  
f
.
write
(
content
)
  
f
.
close
(
)
def
main
(
argv
)
:
  
if
len
(
argv
)
!
=
2
:
    
print
(
'
Usage
:
{
}
YYYYMMDD
'
.
format
(
sys
.
argv
[
0
]
file
=
sys
.
stderr
)
)
    
sys
.
exit
(
1
)
  
datestamp
=
sys
.
argv
[
1
]
  
if
len
(
datestamp
)
!
=
8
or
not
datestamp
.
isdigit
(
)
:
    
raise
Exception
(
        
'
datestamp
=
{
}
is
not
in
the
YYYYMMDD
format
'
.
format
(
datestamp
)
)
  
ReplaceStringsInFile
(
      
'
absl
/
base
/
options
.
h
'
{
          
'
#
define
ABSL_OPTION_USE_INLINE_NAMESPACE
0
'
:
              
'
#
define
ABSL_OPTION_USE_INLINE_NAMESPACE
1
'
          
'
#
define
ABSL_OPTION_INLINE_NAMESPACE_NAME
head
'
:
              
'
#
define
ABSL_OPTION_INLINE_NAMESPACE_NAME
lts_
{
}
'
.
format
(
                  
datestamp
)
      
}
)
  
ReplaceStringsInFile
(
      
'
CMakeLists
.
txt
'
{
          
'
project
(
absl
LANGUAGES
CXX
)
'
:
              
'
project
(
absl
LANGUAGES
CXX
VERSION
{
}
)
'
.
format
(
datestamp
)
      
}
)
  
ReplaceStringsInFile
(
      
'
CMake
/
AbseilHelpers
.
cmake
'
      
{
'
SOVERSION
0
'
:
'
SOVERSION
"
{
}
.
0
.
0
"
'
.
format
(
datestamp
[
2
:
6
]
)
}
)
  
StripContentBetweenTags
(
'
CMakeLists
.
txt
'
'
#
absl
:
lts
-
remove
-
begin
'
                          
'
#
absl
:
lts
-
remove
-
end
'
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
)
