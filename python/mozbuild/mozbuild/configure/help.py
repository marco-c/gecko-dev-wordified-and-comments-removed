import
os
import
re
from
collections
import
defaultdict
from
mozbuild
.
configure
.
options
import
Option
class
HelpFormatter
(
object
)
:
    
def
__init__
(
self
argv0
)
:
        
self
.
intro
=
[
"
Usage
:
%
s
[
options
]
"
%
os
.
path
.
basename
(
argv0
)
]
        
self
.
options
=
[
]
    
def
add
(
self
option
)
:
        
assert
isinstance
(
option
Option
)
        
if
option
.
possible_origins
=
=
(
"
implied
"
)
:
            
return
        
if
(
            
option
.
default
            
and
len
(
option
.
default
)
=
=
0
            
and
option
.
choices
            
and
option
.
nargs
in
(
"
?
"
"
*
"
)
        
)
:
            
option_1
=
Option
(
                
option
.
option
                
default
=
False
                
choices
=
option
.
choices
                
help
=
option
.
help
                
define_depth
=
1
            
)
            
option_2
=
Option
(
                
option
.
option
default
=
True
help
=
option
.
help
define_depth
=
1
            
)
            
self
.
options
.
append
(
option_1
)
            
self
.
options
.
append
(
option_2
)
        
else
:
            
self
.
options
.
append
(
option
)
    
def
format_options_by_category
(
self
options_by_category
)
:
        
ret
=
[
]
        
for
category
options
in
options_by_category
.
items
(
)
:
            
ret
.
append
(
"
"
+
category
+
"
:
"
)
            
for
option
in
options
:
                
opt
=
option
.
option
                
if
option
.
metavar
:
                    
if
option
.
nargs
=
=
"
?
"
:
                        
opt
+
=
f
"
[
=
{
option
.
metavar
}
]
"
                    
elif
option
.
nargs
=
=
"
*
"
:
                        
opt
+
=
f
"
[
=
{
option
.
metavar
}
.
.
.
]
"
                    
elif
option
.
nargs
=
=
"
+
"
:
                        
opt
+
=
f
"
=
{
option
.
metavar
}
.
.
.
"
                    
else
:
                        
opt
+
=
"
=
"
+
"
"
.
join
(
[
f
"
{
option
.
metavar
}
"
]
*
option
.
nargs
)
                
if
option
.
choices
:
                    
if
option
.
nargs
=
=
"
?
"
:
                        
opt
+
=
"
[
=
{
%
s
}
]
"
%
"
"
.
join
(
option
.
choices
)
                    
elif
option
.
nargs
=
=
"
*
"
:
                        
opt
+
=
"
[
=
{
%
s
}
.
.
.
]
"
%
"
"
.
join
(
option
.
choices
)
                    
elif
option
.
nargs
=
=
"
+
"
:
                        
opt
+
=
"
=
{
%
s
}
.
.
.
"
%
"
"
.
join
(
option
.
choices
)
                    
else
:
                        
opt
+
=
"
=
{
%
s
}
"
%
"
"
.
join
(
option
.
choices
)
                
help
=
self
.
format_help
(
option
)
                
if
len
(
option
.
default
)
:
                    
if
help
:
                        
help
+
=
"
"
                    
help
+
=
"
[
%
s
]
"
%
"
"
.
join
(
option
.
default
)
                
if
len
(
opt
)
>
24
or
not
help
:
                    
ret
.
append
(
"
%
s
"
%
opt
)
                    
if
help
:
                        
ret
.
append
(
"
%
s
%
s
"
%
(
"
"
*
30
help
)
)
                
else
:
                    
ret
.
append
(
"
%
-
24s
%
s
"
%
(
opt
help
)
)
            
ret
.
append
(
"
"
)
        
return
ret
    
RE_FORMAT
=
re
.
compile
(
r
"
{
(
[
^
|
}
]
*
)
\
|
(
[
^
|
}
]
*
)
}
"
)
    
def
format_help
(
self
option
)
:
        
if
not
option
.
help
:
            
return
"
"
        
if
option
.
prefix
in
(
"
enable
"
"
with
"
)
:
            
replacement
=
r
"
\
1
"
        
elif
option
.
prefix
in
(
"
disable
"
"
without
"
)
:
            
replacement
=
r
"
\
2
"
        
else
:
            
return
option
.
help
        
return
self
.
RE_FORMAT
.
sub
(
replacement
option
.
help
)
    
def
usage
(
self
out
)
:
        
options_by_category
=
defaultdict
(
list
)
        
env_by_category
=
defaultdict
(
list
)
        
for
option
in
self
.
options
:
            
target
=
options_by_category
if
option
.
name
else
env_by_category
            
target
[
option
.
category
]
.
append
(
option
)
        
if
options_by_category
:
            
options_formatted
=
[
                
"
Options
:
[
defaults
in
brackets
after
descriptions
]
"
            
]
+
self
.
format_options_by_category
(
options_by_category
)
        
else
:
            
options_formatted
=
[
]
        
if
env_by_category
:
            
env_formatted
=
[
                
"
Environment
variables
:
"
            
]
+
self
.
format_options_by_category
(
env_by_category
)
        
else
:
            
env_formatted
=
[
]
        
print
(
            
"
\
n
\
n
"
.
join
(
                
"
\
n
"
.
join
(
t
)
                
for
t
in
(
self
.
intro
options_formatted
env_formatted
)
                
if
t
            
)
            
file
=
out
        
)
