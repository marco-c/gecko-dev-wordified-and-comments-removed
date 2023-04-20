from
.
errorsummary
import
ErrorSummaryFormatter
from
.
grouping
import
GroupingFormatter
from
.
html
import
HTMLFormatter
from
.
machformatter
import
MachFormatter
from
.
tbplformatter
import
TbplFormatter
from
.
unittest
import
UnittestFormatter
from
.
xunit
import
XUnitFormatter
try
:
    
import
ujson
as
json
except
ImportError
:
    
import
json
def
JSONFormatter
(
)
:
    
return
lambda
x
:
json
.
dumps
(
x
)
+
"
\
n
"
__all__
=
[
    
"
UnittestFormatter
"
    
"
XUnitFormatter
"
    
"
HTMLFormatter
"
    
"
MachFormatter
"
    
"
TbplFormatter
"
    
"
ErrorSummaryFormatter
"
    
"
JSONFormatter
"
    
"
GroupingFormatter
"
]
