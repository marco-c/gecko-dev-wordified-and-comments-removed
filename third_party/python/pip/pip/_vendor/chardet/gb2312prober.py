from
.
chardistribution
import
GB2312DistributionAnalysis
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
GB2312_SM_MODEL
class
GB2312Prober
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
GB2312_SM_MODEL
)
        
self
.
distribution_analyzer
=
GB2312DistributionAnalysis
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
GB2312
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
Chinese
"
