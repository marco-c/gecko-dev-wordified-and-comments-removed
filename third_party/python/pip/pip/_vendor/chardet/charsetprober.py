import
logging
import
re
from
typing
import
Optional
Union
from
.
enums
import
LanguageFilter
ProbingState
INTERNATIONAL_WORDS_PATTERN
=
re
.
compile
(
    
b
"
[
a
-
zA
-
Z
]
*
[
\
x80
-
\
xFF
]
+
[
a
-
zA
-
Z
]
*
[
^
a
-
zA
-
Z
\
x80
-
\
xFF
]
?
"
)
class
CharSetProber
:
    
SHORTCUT_THRESHOLD
=
0
.
95
    
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
        
self
.
_state
=
ProbingState
.
DETECTING
        
self
.
active
=
True
        
self
.
lang_filter
=
lang_filter
        
self
.
logger
=
logging
.
getLogger
(
__name__
)
    
def
reset
(
self
)
-
>
None
:
        
self
.
_state
=
ProbingState
.
DETECTING
    
property
    
def
charset_name
(
self
)
-
>
Optional
[
str
]
:
        
return
None
    
property
    
def
language
(
self
)
-
>
Optional
[
str
]
:
        
raise
NotImplementedError
    
def
feed
(
self
byte_str
:
Union
[
bytes
bytearray
]
)
-
>
ProbingState
:
        
raise
NotImplementedError
    
property
    
def
state
(
self
)
-
>
ProbingState
:
        
return
self
.
_state
    
def
get_confidence
(
self
)
-
>
float
:
        
return
0
.
0
    
staticmethod
    
def
filter_high_byte_only
(
buf
:
Union
[
bytes
bytearray
]
)
-
>
bytes
:
        
buf
=
re
.
sub
(
b
"
(
[
\
x00
-
\
x7F
]
)
+
"
b
"
"
buf
)
        
return
buf
    
staticmethod
    
def
filter_international_words
(
buf
:
Union
[
bytes
bytearray
]
)
-
>
bytearray
:
        
"
"
"
        
We
define
three
types
of
bytes
:
        
alphabet
:
english
alphabets
[
a
-
zA
-
Z
]
        
international
:
international
characters
[
\
x80
-
\
xFF
]
        
marker
:
everything
else
[
^
a
-
zA
-
Z
\
x80
-
\
xFF
]
        
The
input
buffer
can
be
thought
to
contain
a
series
of
words
delimited
        
by
markers
.
This
function
works
to
filter
all
words
that
contain
at
        
least
one
international
character
.
All
contiguous
sequences
of
markers
        
are
replaced
by
a
single
space
ascii
character
.
        
This
filter
applies
to
all
scripts
which
do
not
use
English
characters
.
        
"
"
"
        
filtered
=
bytearray
(
)
        
words
=
INTERNATIONAL_WORDS_PATTERN
.
findall
(
buf
)
        
for
word
in
words
:
            
filtered
.
extend
(
word
[
:
-
1
]
)
            
last_char
=
word
[
-
1
:
]
            
if
not
last_char
.
isalpha
(
)
and
last_char
<
b
"
\
x80
"
:
                
last_char
=
b
"
"
            
filtered
.
extend
(
last_char
)
        
return
filtered
    
staticmethod
    
def
remove_xml_tags
(
buf
:
Union
[
bytes
bytearray
]
)
-
>
bytes
:
        
"
"
"
        
Returns
a
copy
of
buf
that
retains
only
the
sequences
of
English
        
alphabet
and
high
byte
characters
that
are
not
between
<
>
characters
.
        
This
filter
can
be
applied
to
all
scripts
which
contain
both
English
        
characters
and
extended
ASCII
characters
but
is
currently
only
used
by
        
Latin1Prober
.
        
"
"
"
        
filtered
=
bytearray
(
)
        
in_tag
=
False
        
prev
=
0
        
buf
=
memoryview
(
buf
)
.
cast
(
"
c
"
)
        
for
curr
buf_char
in
enumerate
(
buf
)
:
            
if
buf_char
=
=
b
"
>
"
:
                
prev
=
curr
+
1
                
in_tag
=
False
            
elif
buf_char
=
=
b
"
<
"
:
                
if
curr
>
prev
and
not
in_tag
:
                    
filtered
.
extend
(
buf
[
prev
:
curr
]
)
                    
filtered
.
extend
(
b
"
"
)
                
in_tag
=
True
        
if
not
in_tag
:
            
filtered
.
extend
(
buf
[
prev
:
]
)
        
return
filtered
