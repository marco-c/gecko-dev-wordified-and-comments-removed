#
-
*
-
coding
:
utf
-
8
-
*
-
from
__future__
import
absolute_import
unicode_literals
import
sys
PY3
=
sys
.
version_info
>
=
(
3
0
)
if
PY3
:
    
basestring
=
str
    
long
=
int
    
xrange
=
range
    
unicode
=
str
    
uchr
=
chr
    
def
uord
(
ch
)
:
        
return
ord
(
ch
[
0
]
)
else
:
    
basestring
=
basestring
    
long
=
long
    
xrange
=
xrange
    
unicode
=
unicode
    
try
:
        
unichr
(
0x10000
)
        
uchr
=
unichr
        
def
uord
(
ch
)
:
            
return
ord
(
ch
[
0
]
)
    
except
ValueError
:
        
def
uchr
(
code
)
:
            
if
code
<
=
0xFFFF
:
                
return
unichr
(
code
)
            
cu1
=
(
(
code
-
0x10000
)
>
>
10
)
+
0xD800
            
cu2
=
(
(
code
-
0x10000
)
&
1023
)
+
0xDC00
            
return
unichr
(
cu1
)
+
unichr
(
cu2
)
        
def
uord
(
ch
)
:
            
cp
=
ord
(
ch
[
0
]
)
            
if
cp
>
=
0xD800
and
cp
<
=
0xDBFF
:
                
second
=
ord
(
ch
[
1
]
)
                
if
second
>
=
0xDC00
and
second
<
=
0xDFFF
:
                    
first
=
cp
                    
cp
=
(
first
-
0xD800
)
*
0x400
+
second
-
0xDC00
+
0x10000
            
return
cp
