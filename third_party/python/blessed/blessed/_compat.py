"
"
"
Provides
compatibility
between
different
Python
versions
.
"
"
"
import
sys
__all__
=
'
PY2
'
'
unicode_chr
'
'
StringIO
'
'
TextType
'
'
StringType
'
if
sys
.
version_info
[
0
]
>
=
3
:
    
PY2
=
False
    
unicode_chr
=
chr
    
from
io
import
StringIO
    
TextType
=
str
    
StringType
=
str
else
:
    
PY2
=
True
    
unicode_chr
=
unichr
    
from
StringIO
import
StringIO
    
TextType
=
unicode
    
StringType
=
basestring
