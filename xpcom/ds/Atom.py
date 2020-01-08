class
Atom
(
)
:
    
def
__init__
(
self
ident
string
ty
=
"
nsStaticAtom
"
)
:
        
self
.
ident
=
ident
        
self
.
string
=
string
        
self
.
ty
=
ty
class
PseudoElementAtom
(
Atom
)
:
    
def
__init__
(
self
ident
string
)
:
        
Atom
.
__init__
(
self
ident
string
ty
=
"
nsICSSPseudoElement
"
)
