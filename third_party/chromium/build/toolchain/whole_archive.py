import
re
def
wrap_with_whole_archive
(
command
is_apple
=
False
)
:
  
"
"
"
Modify
and
return
command
such
that
-
LinkWrapper
add
-
whole
-
archive
=
X
  
becomes
a
linking
inclusion
X
(
-
lX
)
but
wrapped
in
whole
-
archive
  
modifiers
.
"
"
"
  
def
extract_libname
(
s
)
:
    
m
=
re
.
match
(
r
'
-
LinkWrapper
add
-
whole
-
archive
=
(
.
+
)
'
s
)
    
return
m
.
group
(
1
)
  
whole_archive_libs
=
[
      
extract_libname
(
x
)
for
x
in
command
      
if
x
.
startswith
(
"
-
LinkWrapper
add
-
whole
-
archive
=
"
)
  
]
  
command
=
[
x
for
x
in
command
if
not
x
.
startswith
(
"
-
LinkWrapper
"
)
]
  
def
has_any_suffix
(
string
suffixes
)
:
    
for
suffix
in
suffixes
:
      
if
string
.
endswith
(
suffix
)
:
        
return
True
    
return
False
  
def
wrap_libs_with
(
command
libnames
before
after
)
:
    
out
=
[
]
    
for
arg
in
command
:
      
if
has_any_suffix
(
arg
libnames
)
:
        
out
.
extend
(
[
before
arg
]
)
        
if
after
:
          
out
.
append
(
after
)
      
else
:
        
out
.
append
(
arg
)
    
return
out
  
if
is_apple
:
    
return
wrap_libs_with
(
command
whole_archive_libs
"
-
Wl
-
force_load
"
None
)
  
else
:
    
return
wrap_libs_with
(
command
whole_archive_libs
"
-
Wl
-
-
whole
-
archive
"
                          
"
-
Wl
-
-
no
-
whole
-
archive
"
)
