"
"
"
Exceptions
relating
to
specific
conditions
that
occur
when
factoring
a
model
.
"
"
"
from
.
.
.
exception
import
CycloneDxException
__all__
=
[
'
FactoryException
'
'
LicenseChoiceFactoryException
'
'
InvalidSpdxLicenseException
'
           
'
LicenseFactoryException
'
'
InvalidLicenseExpressionException
'
]
class
FactoryException
(
CycloneDxException
)
:
    
"
"
"
    
Base
exception
that
covers
all
exceptions
that
may
be
thrown
during
model
factoring
.
    
"
"
"
    
pass
class
LicenseChoiceFactoryException
(
FactoryException
)
:
    
"
"
"
    
Base
exception
that
covers
all
LicenseChoiceFactory
exceptions
.
    
"
"
"
    
pass
class
InvalidSpdxLicenseException
(
LicenseChoiceFactoryException
)
:
    
"
"
"
    
Thrown
when
an
invalid
SPDX
License
is
provided
.
    
"
"
"
    
pass
class
LicenseFactoryException
(
FactoryException
)
:
    
"
"
"
    
Base
exception
that
covers
all
LicenseFactory
exceptions
.
    
"
"
"
    
pass
class
InvalidLicenseExpressionException
(
LicenseFactoryException
)
:
    
"
"
"
    
Thrown
when
an
invalid
License
expression
is
provided
.
    
"
"
"
    
pass
