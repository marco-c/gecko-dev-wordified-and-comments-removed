from
.
chardistribution
import
JOHABDistributionAnalysis
from
.
codingstatemachine
import
CodingStateMachine
from
.
mbcharsetprober
import
MultiByteCharSetProber
from
.
mbcssm
import
JOHAB_SM_MODEL
class
JOHABProber
(
MultiByteCharSetProber
)
:
    
def
__init__
(
self
)
-
>
None
:
        
super
(
)
.
__init__
(
)
        
self
.
coding_sm
=
CodingStateMachine
(
JOHAB_SM_MODEL
)
        
self
.
distribution_analyzer
=
JOHABDistributionAnalysis
(
)
        
self
.
reset
(
)
    
property
    
def
charset_name
(
self
)
-
>
str
:
        
return
"
Johab
"
    
property
    
def
language
(
self
)
-
>
str
:
        
return
"
Korean
"
