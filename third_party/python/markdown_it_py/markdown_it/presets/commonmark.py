"
"
"
Commonmark
default
options
.
This
differs
to
presets
.
default
primarily
in
that
it
allows
HTML
and
does
not
enable
components
:
-
block
:
table
-
inline
:
strikethrough
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
True
            
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
True
            
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
blockquote
"
                    
"
code
"
                    
"
fence
"
                    
"
heading
"
                    
"
hr
"
                    
"
html_block
"
                    
"
lheading
"
                    
"
list
"
                    
"
reference
"
                    
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
autolink
"
                    
"
backticks
"
                    
"
emphasis
"
                    
"
entity
"
                    
"
escape
"
                    
"
html_inline
"
                    
"
image
"
                    
"
link
"
                    
"
newline
"
                    
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
emphasis
"
"
fragments_join
"
]
            
}
        
}
    
}
