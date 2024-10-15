from
.
big5prober
import
Big5Prober
from
.
charsetgroupprober
import
CharSetGroupProber
from
.
cp949prober
import
CP949Prober
from
.
enums
import
LanguageFilter
from
.
eucjpprober
import
EUCJPProber
from
.
euckrprober
import
EUCKRProber
from
.
euctwprober
import
EUCTWProber
from
.
gb2312prober
import
GB2312Prober
from
.
johabprober
import
JOHABProber
from
.
sjisprober
import
SJISProber
from
.
utf8prober
import
UTF8Prober
class
MBCSGroupProber
(
CharSetGroupProber
)
:
    
def
__init__
(
self
lang_filter
:
LanguageFilter
=
LanguageFilter
.
NONE
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
lang_filter
=
lang_filter
)
        
self
.
probers
=
[
            
UTF8Prober
(
)
            
SJISProber
(
)
            
EUCJPProber
(
)
            
GB2312Prober
(
)
            
EUCKRProber
(
)
            
CP949Prober
(
)
            
Big5Prober
(
)
            
EUCTWProber
(
)
            
JOHABProber
(
)
        
]
        
self
.
reset
(
)
