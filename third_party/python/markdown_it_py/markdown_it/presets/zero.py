"
"
"
"
Zero
"
preset
with
nothing
enabled
.
Useful
for
manual
configuring
of
simple
modes
.
For
example
to
parse
bold
/
italic
only
.
"
"
"
from
.
.
utils
import
PresetType
def
make
(
)
-
>
PresetType
:
    
return
{
        
"
options
"
:
{
            
"
maxNesting
"
:
20
            
"
html
"
:
False
            
"
linkify
"
:
False
            
"
typographer
"
:
False
            
"
quotes
"
:
"
\
u201c
\
u201d
\
u2018
\
u2019
"
            
"
xhtmlOut
"
:
False
            
"
breaks
"
:
False
            
"
langPrefix
"
:
"
language
-
"
            
"
highlight
"
:
None
        
}
        
"
components
"
:
{
            
"
core
"
:
{
"
rules
"
:
[
"
normalize
"
"
block
"
"
inline
"
"
text_join
"
]
}
            
"
block
"
:
{
"
rules
"
:
[
"
paragraph
"
]
}
            
"
inline
"
:
{
                
"
rules
"
:
[
"
text
"
]
                
"
rules2
"
:
[
"
balance_pairs
"
"
fragments_join
"
]
            
}
        
}
    
}
