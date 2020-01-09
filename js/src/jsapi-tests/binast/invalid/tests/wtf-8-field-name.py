def
filter_ast
(
ast
)
:
    
import
filter_utils
as
utils
    
expr_stmt
=
utils
.
wrap
(
ast
)
\
        
.
assert_interface
(
'
Script
'
)
\
        
.
field
(
'
statements
'
)
\
        
.
elem
(
0
)
\
        
.
assert_interface
(
'
ExpressionStatement
'
)
\
    
expr_stmt
.
append_field
(
u
'
\
uD83E_
\
uDD9D
'
                           
expr_stmt
.
remove_field
(
'
expression
'
)
)
    
return
ast
