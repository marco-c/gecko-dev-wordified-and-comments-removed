'
'
'
Stuff
to
prevent
conflicting
shortcuts
.
'
'
'
from
__future__
import
print_function
from
grit
import
lazy_re
class
ShortcutGroup
(
object
)
:
  
'
'
'
Manages
a
list
of
cliques
that
belong
together
in
a
single
shortcut
  
group
.
Knows
how
to
detect
conflicting
shortcut
keys
.
  
'
'
'
  
SHORTCUT_RE
=
lazy_re
.
compile
(
'
(
[
^
&
]
|
^
)
(
&
[
A
-
Za
-
z
]
)
'
)
  
def
__init__
(
self
name
)
:
    
self
.
name
=
name
    
self
.
keys_by_lang
=
{
}
    
self
.
cliques
=
[
]
  
def
AddClique
(
self
c
)
:
    
for
existing_clique
in
self
.
cliques
:
      
if
existing_clique
.
GetId
(
)
=
=
c
.
GetId
(
)
:
        
return
    
self
.
cliques
.
append
(
c
)
    
for
(
lang
msg
)
in
c
.
clique
.
items
(
)
:
      
if
lang
not
in
self
.
keys_by_lang
:
        
self
.
keys_by_lang
[
lang
]
=
{
}
      
keymap
=
self
.
keys_by_lang
[
lang
]
      
content
=
msg
.
GetRealContent
(
)
      
keys
=
[
groups
[
1
]
for
groups
in
self
.
SHORTCUT_RE
.
findall
(
content
)
]
      
for
key
in
keys
:
        
key
=
key
.
upper
(
)
        
if
key
in
keymap
:
          
keymap
[
key
]
+
=
1
        
else
:
          
keymap
[
key
]
=
1
  
def
GenerateWarnings
(
self
tc_project
)
:
    
problem_langs
=
{
}
    
for
(
lang
keys
)
in
self
.
keys_by_lang
.
items
(
)
:
      
for
(
key
count
)
in
keys
.
items
(
)
:
        
if
count
>
1
:
          
if
lang
not
in
problem_langs
:
            
problem_langs
[
lang
]
=
[
]
          
problem_langs
[
lang
]
.
append
(
key
)
    
warnings
=
[
]
    
if
len
(
problem_langs
)
:
      
warnings
.
append
(
"
WARNING
-
duplicate
keys
exist
in
shortcut
group
%
s
"
%
                      
self
.
name
)
      
for
(
lang
keys
)
in
problem_langs
.
items
(
)
:
        
warnings
.
append
(
"
%
6s
duplicates
:
%
s
"
%
(
lang
'
'
.
join
(
keys
)
)
)
    
return
warnings
def
GenerateDuplicateShortcutsWarnings
(
uberclique
tc_project
)
:
  
'
'
'
Given
an
UberClique
and
a
project
name
will
print
out
helpful
warnings
  
if
there
are
conflicting
shortcuts
within
shortcut
groups
in
the
provided
  
UberClique
.
  
Args
:
    
uberclique
:
clique
.
UberClique
(
)
    
tc_project
:
'
MyProjectNameInTheTranslationConsole
'
  
Returns
:
    
[
'
warning
line
1
'
'
warning
line
2
'
.
.
.
]
  
'
'
'
  
warnings
=
[
]
  
groups
=
{
}
  
for
c
in
uberclique
.
AllCliques
(
)
:
    
for
group
in
c
.
shortcut_groups
:
      
if
group
not
in
groups
:
        
groups
[
group
]
=
ShortcutGroup
(
group
)
      
groups
[
group
]
.
AddClique
(
c
)
  
for
group
in
groups
.
values
(
)
:
    
warnings
+
=
group
.
GenerateWarnings
(
tc_project
)
  
return
warnings
