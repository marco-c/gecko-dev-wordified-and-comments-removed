class
LintException
(
Exception
)
:
    
pass
class
LinterNotFound
(
LintException
)
:
    
def
__init__
(
self
path
)
:
        
LintException
.
__init__
(
self
f
"
Could
not
find
lint
file
'
{
path
}
'
"
)
class
NoValidLinter
(
LintException
)
:
    
def
__init__
(
self
)
:
        
LintException
.
__init__
(
            
self
            
"
Invalid
linters
given
run
again
using
valid
linters
or
no
linters
"
        
)
class
LinterParseError
(
LintException
)
:
    
def
__init__
(
self
path
message
)
:
        
LintException
.
__init__
(
self
f
"
{
path
}
:
{
message
}
"
)
class
LintersNotConfigured
(
LintException
)
:
    
def
__init__
(
self
)
:
        
LintException
.
__init__
(
            
self
            
"
No
linters
registered
!
Use
LintRoller
.
read
to
register
a
linter
.
"
        
)
