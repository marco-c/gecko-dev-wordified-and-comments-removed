"
"
"
Contains
helper
class
for
processing
javac
output
.
"
"
"
import
os
import
pathlib
import
re
import
sys
from
util
import
build_utils
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
build_utils
.
DIR_SOURCE_ROOT
'
third_party
'
'
colorama
'
'
src
'
)
)
import
colorama
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
build_utils
.
DIR_SOURCE_ROOT
'
tools
'
'
android
'
                 
'
modularization
'
'
convenience
'
)
)
import
lookup_dep
class
JavacOutputProcessor
:
  
def
__init__
(
self
target_name
)
:
    
self
.
_target_name
=
self
.
_RemoveSuffixesIfPresent
(
        
[
"
__compile_java
"
"
__errorprone
"
"
__header
"
]
target_name
)
    
self
.
_suggested_deps
=
set
(
)
    
fileline_prefix
=
(
        
r
'
(
?
P
<
fileline
>
(
?
P
<
file
>
[
-
.
\
w
/
\
\
]
+
.
java
)
:
(
?
P
<
line
>
[
0
-
9
]
+
)
:
)
'
)
    
self
.
_warning_re
=
re
.
compile
(
        
fileline_prefix
+
r
'
(
?
P
<
full_message
>
warning
:
(
?
P
<
message
>
.
*
)
)
'
)
    
self
.
_error_re
=
re
.
compile
(
fileline_prefix
+
                                
r
'
(
?
P
<
full_message
>
(
?
P
<
message
>
.
*
)
)
'
)
    
self
.
_marker_re
=
re
.
compile
(
r
'
\
s
*
(
?
P
<
marker
>
\
^
)
\
s
*
'
)
    
self
.
_please_add_dep_re
=
re
.
compile
(
r
'
(
?
P
<
full_message
>
Hint
:
.
*
)
'
)
    
self
.
_symbol_not_found_re_list
=
[
        
(
True
         
re
.
compile
(
fileline_prefix
+
                    
r
'
(
error
:
package
[
\
w
.
]
+
does
not
exist
)
'
)
)
        
(
False
re
.
compile
(
fileline_prefix
+
r
'
(
error
:
cannot
find
symbol
)
'
)
)
        
(
True
         
re
.
compile
(
fileline_prefix
+
r
'
(
error
:
symbol
not
found
[
\
w
.
]
+
)
'
)
)
    
]
    
self
.
_import_re
=
re
.
compile
(
r
'
\
s
*
import
(
?
P
<
imported_class
>
[
\
w
\
.
]
+
)
;
'
)
    
self
.
_warning_color
=
[
        
'
full_message
'
colorama
.
Fore
.
YELLOW
+
colorama
.
Style
.
DIM
    
]
    
self
.
_error_color
=
[
        
'
full_message
'
colorama
.
Fore
.
MAGENTA
+
colorama
.
Style
.
BRIGHT
    
]
    
self
.
_marker_color
=
[
'
marker
'
colorama
.
Fore
.
BLUE
+
colorama
.
Style
.
BRIGHT
]
    
self
.
_class_lookup_index
=
None
    
colorama
.
init
(
)
  
def
Process
(
self
lines
)
:
    
"
"
"
Processes
javac
output
.
      
-
Applies
colors
to
output
.
      
-
Suggests
GN
dep
to
add
for
'
unresolved
symbol
in
Java
import
'
errors
.
      
"
"
"
    
lines
=
self
.
_ElaborateLinesForUnknownSymbol
(
iter
(
lines
)
)
    
for
line
in
lines
:
      
yield
self
.
_ApplyColors
(
line
)
    
if
self
.
_suggested_deps
:
      
yield
"
Full
list
of
deps
to
add
to
{
}
:
"
.
format
(
self
.
_target_name
)
      
for
dep
in
sorted
(
self
.
_suggested_deps
)
:
        
yield
'
"
{
}
"
'
.
format
(
dep
)
  
def
_ElaborateLinesForUnknownSymbol
(
self
lines
)
:
    
"
"
"
Elaborates
passed
-
in
javac
output
for
unresolved
symbols
.
    
Looks
for
unresolved
symbols
in
imports
.
    
Adds
:
    
-
Line
with
GN
target
which
cannot
compile
.
    
-
Mention
of
unresolved
class
if
not
present
in
error
message
.
    
-
Line
with
suggestion
of
GN
dep
to
add
.
    
Args
:
      
lines
:
Generator
with
javac
input
.
    
Returns
:
      
Generator
with
processed
output
.
    
"
"
"
    
previous_line
=
next
(
lines
None
)
    
line
=
next
(
lines
None
)
    
while
previous_line
!
=
None
:
      
elaborated_lines
=
self
.
_ElaborateLineForUnknownSymbol
(
          
previous_line
line
)
      
for
elaborated_line
in
elaborated_lines
:
        
yield
elaborated_line
      
previous_line
=
line
      
line
=
next
(
lines
None
)
  
def
_ApplyColors
(
self
line
)
:
    
"
"
"
Adds
colors
to
passed
-
in
line
and
returns
processed
line
.
"
"
"
    
if
self
.
_warning_re
.
match
(
line
)
:
      
line
=
self
.
_Colorize
(
line
self
.
_warning_re
self
.
_warning_color
)
    
elif
self
.
_error_re
.
match
(
line
)
:
      
line
=
self
.
_Colorize
(
line
self
.
_error_re
self
.
_error_color
)
    
elif
self
.
_please_add_dep_re
.
match
(
line
)
:
      
line
=
self
.
_Colorize
(
line
self
.
_please_add_dep_re
self
.
_error_color
)
    
elif
self
.
_marker_re
.
match
(
line
)
:
      
line
=
self
.
_Colorize
(
line
self
.
_marker_re
self
.
_marker_color
)
    
return
line
  
def
_ElaborateLineForUnknownSymbol
(
self
line
next_line
)
:
    
if
not
next_line
:
      
return
[
line
]
    
import_re_match
=
self
.
_import_re
.
match
(
next_line
)
    
if
not
import_re_match
:
      
return
[
line
]
    
symbol_missing
=
False
    
has_missing_symbol_in_error_msg
=
False
    
for
symbol_in_error_msg
regex
in
self
.
_symbol_not_found_re_list
:
      
if
regex
.
match
(
line
)
:
        
symbol_missing
=
True
        
has_missing_symbol_in_error_msg
=
symbol_in_error_msg
        
break
    
if
not
symbol_missing
:
      
return
[
line
]
    
class_to_lookup
=
import_re_match
.
group
(
'
imported_class
'
)
    
if
self
.
_class_lookup_index
=
=
None
:
      
self
.
_class_lookup_index
=
lookup_dep
.
ClassLookupIndex
(
pathlib
.
Path
(
          
os
.
getcwd
(
)
)
                                                             
should_build
=
False
)
    
suggested_deps
=
self
.
_class_lookup_index
.
match
(
class_to_lookup
)
    
if
len
(
suggested_deps
)
!
=
1
:
      
suggested_deps
=
self
.
_FindFactoryDep
(
suggested_deps
)
      
if
len
(
suggested_deps
)
!
=
1
:
        
return
[
line
]
    
suggested_target
=
suggested_deps
[
0
]
.
target
    
if
not
has_missing_symbol_in_error_msg
:
      
line
=
"
{
}
{
}
"
.
format
(
line
class_to_lookup
)
    
self
.
_suggested_deps
.
add
(
suggested_target
)
    
return
[
        
line
        
'
Hint
:
Add
"
{
}
"
to
deps
of
{
}
'
.
format
(
suggested_target
                                              
self
.
_target_name
)
    
]
  
staticmethod
  
def
_FindFactoryDep
(
class_entries
)
:
    
"
"
"
Find
the
android_library_factory
(
)
GN
target
.
"
"
"
    
if
len
(
class_entries
)
!
=
2
:
      
return
[
]
    
if
class_entries
[
0
]
.
low_classpath_priority
=
=
class_entries
[
        
1
]
.
low_classpath_priority
:
      
return
[
]
    
if
class_entries
[
0
]
.
low_classpath_priority
:
      
return
[
class_entries
[
0
]
]
    
return
[
class_entries
[
1
]
]
  
staticmethod
  
def
_RemoveSuffixesIfPresent
(
suffixes
text
)
:
    
for
suffix
in
suffixes
:
      
if
text
.
endswith
(
suffix
)
:
        
return
text
[
:
-
len
(
suffix
)
]
    
return
text
  
staticmethod
  
def
_Colorize
(
line
regex
color
)
:
    
match
=
regex
.
match
(
line
)
    
start
=
match
.
start
(
color
[
0
]
)
    
end
=
match
.
end
(
color
[
0
]
)
    
return
(
line
[
:
start
]
+
color
[
1
]
+
line
[
start
:
end
]
+
colorama
.
Fore
.
RESET
+
            
colorama
.
Style
.
RESET_ALL
+
line
[
end
:
]
)
