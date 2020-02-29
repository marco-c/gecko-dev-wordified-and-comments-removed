"
"
"
parser
.
py
-
A
JavaScript
parser
currently
with
many
bugs
.
See
README
.
md
for
instructions
.
"
"
"
import
jsparagus
from
.
import
parser_tables
from
.
lexer
import
JSLexer
Script_entry_state
=
0
class
JSParser
(
jsparagus
.
runtime
.
Parser
)
:
    
def
__init__
(
self
)
:
        
jsparagus
.
runtime
.
Parser
.
__init__
(
            
self
            
parser_tables
.
actions
            
parser_tables
.
ctns
            
parser_tables
.
reductions
            
parser_tables
.
special_cases
            
parser_tables
.
error_codes
            
Script_entry_state
            
parser_tables
.
DefaultBuilder
(
)
        
)
    
def
on_recover
(
self
error_code
lexer
t
)
:
        
"
"
"
Check
that
ASI
error
recovery
is
really
acceptable
.
"
"
"
        
if
error_code
=
=
'
asi
'
:
            
if
not
self
.
closed
and
t
!
=
'
}
'
and
not
lexer
.
saw_line_terminator
(
)
:
                
lexer
.
throw
(
"
missing
semicolon
"
)
        
else
:
            
assert
error_code
=
=
'
do_while_asi
'
def
parse_Script
(
text
)
:
    
lexer
=
JSLexer
(
JSParser
(
)
)
    
lexer
.
write
(
text
)
    
return
lexer
.
close
(
)
