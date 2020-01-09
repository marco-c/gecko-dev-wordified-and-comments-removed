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
    
utils
.
assert_interface
(
ast
'
Script
'
)
    
global_stmts
=
utils
.
get_field
(
ast
'
statements
'
)
    
expr_stmt
=
utils
.
get_element
(
global_stmts
0
)
    
utils
.
assert_interface
(
expr_stmt
'
ExpressionStatement
'
)
    
field
=
utils
.
get_field
(
expr_stmt
'
expression
'
)
    
utils
.
append_field
(
expr_stmt
u
'
\
uD83E_
\
uDD9D
'
field
)
    
utils
.
remove_field
(
expr_stmt
'
expression
'
)
    
return
ast
