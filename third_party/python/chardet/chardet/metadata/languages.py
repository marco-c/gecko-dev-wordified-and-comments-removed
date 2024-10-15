"
"
"
Metadata
about
languages
used
by
our
model
training
code
for
our
SingleByteCharSetProbers
.
Could
be
used
for
other
things
in
the
future
.
This
code
is
based
on
the
language
metadata
from
the
uchardet
project
.
"
"
"
from
string
import
ascii_letters
from
typing
import
List
Optional
class
Language
:
    
"
"
"
Metadata
about
a
language
useful
for
training
models
    
:
ivar
name
:
The
human
name
for
the
language
in
English
.
    
:
type
name
:
str
    
:
ivar
iso_code
:
2
-
letter
ISO
639
-
1
if
possible
3
-
letter
ISO
code
otherwise
                    
or
use
another
catalog
as
a
last
resort
.
    
:
type
iso_code
:
str
    
:
ivar
use_ascii
:
Whether
or
not
ASCII
letters
should
be
included
in
trained
                     
models
.
    
:
type
use_ascii
:
bool
    
:
ivar
charsets
:
The
charsets
we
want
to
support
and
create
data
for
.
    
:
type
charsets
:
list
of
str
    
:
ivar
alphabet
:
The
characters
in
the
language
'
s
alphabet
.
If
use_ascii
is
                    
True
you
only
need
to
add
those
not
in
the
ASCII
set
.
    
:
type
alphabet
:
str
    
:
ivar
wiki_start_pages
:
The
Wikipedia
pages
to
start
from
if
we
'
re
crawling
                            
Wikipedia
for
training
data
.
    
:
type
wiki_start_pages
:
list
of
str
    
"
"
"
    
def
__init__
(
        
self
        
name
:
Optional
[
str
]
=
None
        
iso_code
:
Optional
[
str
]
=
None
        
use_ascii
:
bool
=
True
        
charsets
:
Optional
[
List
[
str
]
]
=
None
        
alphabet
:
Optional
[
str
]
=
None
        
wiki_start_pages
:
Optional
[
List
[
str
]
]
=
None
    
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
name
=
name
        
self
.
iso_code
=
iso_code
        
self
.
use_ascii
=
use_ascii
        
self
.
charsets
=
charsets
        
if
self
.
use_ascii
:
            
if
alphabet
:
                
alphabet
+
=
ascii_letters
            
else
:
                
alphabet
=
ascii_letters
        
elif
not
alphabet
:
            
raise
ValueError
(
"
Must
supply
alphabet
if
use_ascii
is
False
"
)
        
self
.
alphabet
=
"
"
.
join
(
sorted
(
set
(
alphabet
)
)
)
if
alphabet
else
None
        
self
.
wiki_start_pages
=
wiki_start_pages
    
def
__repr__
(
self
)
-
>
str
:
        
param_str
=
"
"
.
join
(
            
f
"
{
k
}
=
{
v
!
r
}
"
for
k
v
in
self
.
__dict__
.
items
(
)
if
not
k
.
startswith
(
"
_
"
)
        
)
        
return
f
"
{
self
.
__class__
.
__name__
}
(
{
param_str
}
)
"
LANGUAGES
=
{
    
"
Arabic
"
:
Language
(
        
name
=
"
Arabic
"
        
iso_code
=
"
ar
"
        
use_ascii
=
False
        
charsets
=
[
"
ISO
-
8859
-
6
"
"
WINDOWS
-
1256
"
"
CP720
"
"
CP864
"
]
        
alphabet
=
"
"
        
wiki_start_pages
=
[
"
_
"
]
    
)
    
"
Belarusian
"
:
Language
(
        
name
=
"
Belarusian
"
        
iso_code
=
"
be
"
        
use_ascii
=
False
        
charsets
=
[
"
ISO
-
8859
-
5
"
"
WINDOWS
-
1251
"
"
IBM866
"
"
MacCyrillic
"
]
        
alphabet
=
"
"
        
wiki_start_pages
=
[
"
_
"
]
    
)
    
"
Bulgarian
"
:
Language
(
        
name
=
"
Bulgarian
"
        
iso_code
=
"
bg
"
        
use_ascii
=
False
        
charsets
=
[
"
ISO
-
8859
-
5
"
"
WINDOWS
-
1251
"
"
IBM855
"
]
        
alphabet
=
"
"
        
wiki_start_pages
=
[
"
_
"
]
    
)
    
"
Czech
"
:
Language
(
        
name
=
"
Czech
"
        
iso_code
=
"
cz
"
        
use_ascii
=
True
        
charsets
=
[
"
ISO
-
8859
-
2
"
"
WINDOWS
-
1250
"
]
        
alphabet
=
"
"
        
wiki_start_pages
=
[
"
Hlavn
_strana
"
]
    
)
    
"
Danish
"
:
Language
(
        
name
=
"
Danish
"
        
iso_code
=
"
da
"
        
use_ascii
=
True
        
charsets
=
[
"
ISO
-
8859
-
1
"
"
ISO
-
8859
-
15
"
"
WINDOWS
-
1252
"
"
MacRoman
"
]
        
alphabet
=
"
"
        
wiki_start_pages
=
[
"
Forside
"
]
    
)
    
"
German
"
:
Language
(
        
name
=
"
German
"
        
iso_code
=
"
de
"
        
use_ascii
=
True
        
charsets
=
[
"
ISO
-
8859
-
1
"
"
ISO
-
8859
-
15
"
"
WINDOWS
-
1252
"
"
MacRoman
"
]
        
alphabet
=
"
"
        
wiki_start_pages
=
[
"
Wikipedia
:
Hauptseite
"
]
    
)
    
"
Greek
"
:
Language
(
        
name
=
"
Greek
"
        
iso_code
=
"
el
"
        
use_ascii
=
False
        
charsets
=
[
"
ISO
-
8859
-
7
"
"
WINDOWS
-
1253
"
]
        
alphabet
=
"
"
        
wiki_start_pages
=
[
"
:
"
]
    
)
    
"
English
"
:
Language
(
        
name
=
"
English
"
        
iso_code
=
"
en
"
        
use_ascii
=
True
        
charsets
=
[
"
ISO
-
8859
-
1
"
"
WINDOWS
-
1252
"
"
MacRoman
"
]
        
wiki_start_pages
=
[
"
Main_Page
"
]
    
)
    
"
Esperanto
"
:
Language
(
        
name
=
"
Esperanto
"
        
iso_code
=
"
eo
"
        
use_ascii
=
False
        
charsets
=
[
"
ISO
-
8859
-
3
"
]
        
alphabet
=
"
abc
defg
h
ij
klmnoprs
tu
vzABC
DEFG
H
IJ
KLMNOPRS
TU
VZ
"
        
wiki_start_pages
=
[
"
Vikipedio
:
efpa
o
"
]
    
)
    
"
Spanish
"
:
Language
(
        
name
=
"
Spanish
"
        
iso_code
=
"
es
"
        
use_ascii
=
True
        
charsets
=
[
"
ISO
-
8859
-
1
"
"
ISO
-
8859
-
15
"
"
WINDOWS
-
1252
"
"
MacRoman
"
]
        
alphabet
=
"
"
        
wiki_start_pages
=
[
"
Wikipedia
:
Portada
"
]
    
)
    
"
Estonian
"
:
Language
(
        
name
=
"
Estonian
"
        
iso_code
=
"
et
"
        
use_ascii
=
False
        
charsets
=
[
"
ISO
-
8859
-
4
"
"
ISO
-
8859
-
13
"
"
WINDOWS
-
1257
"
]
        
alphabet
=
"
ABDEGHIJKLMNOPRSTUV
abdeghijklmnoprstuv
"
        
wiki_start_pages
=
[
"
Esileht
"
]
    
)
    
"
Finnish
"
:
Language
(
        
name
=
"
Finnish
"
        
iso_code
=
"
fi
"
        
use_ascii
=
True
        
charsets
=
[
"
ISO
-
8859
-
1
"
"
ISO
-
8859
-
15
"
"
WINDOWS
-
1252
"
"
MacRoman
"
]
        
alphabet
=
"
"
        
wiki_start_pages
=
[
"
Wikipedia
:
Etusivu
"
]
    
)
    
"
French
"
:
Language
(
        
name
=
"
French
"
        
iso_code
=
"
fr
"
        
use_ascii
=
True
        
charsets
=
[
"
ISO
-
8859
-
1
"
"
ISO
-
8859
-
15
"
"
WINDOWS
-
1252
"
"
MacRoman
"
]
        
alphabet
=
"
"
        
wiki_start_pages
=
[
"
Wikip
dia
:
Accueil_principal
"
"
B
uf
(
animal
)
"
]
    
)
    
"
Hebrew
"
:
Language
(
        
name
=
"
Hebrew
"
        
iso_code
=
"
he
"
        
use_ascii
=
False
        
charsets
=
[
"
ISO
-
8859
-
8
"
"
WINDOWS
-
1255
"
]
        
alphabet
=
"
"
        
wiki_start_pages
=
[
"
_
"
]
    
)
    
"
Croatian
"
:
Language
(
        
name
=
"
Croatian
"
        
iso_code
=
"
hr
"
        
use_ascii
=
False
        
charsets
=
[
"
ISO
-
8859
-
2
"
"
WINDOWS
-
1250
"
]
        
alphabet
=
"
abc
d
efghijklmnoprs
tuvz
ABC
D
EFGHIJKLMNOPRS
TUVZ
"
        
wiki_start_pages
=
[
"
Glavna_stranica
"
]
    
)
    
"
Hungarian
"
:
Language
(
        
name
=
"
Hungarian
"
        
iso_code
=
"
hu
"
        
use_ascii
=
False
        
charsets
=
[
"
ISO
-
8859
-
2
"
"
WINDOWS
-
1250
"
]
        
alphabet
=
"
abcdefghijklmnoprstuvz
ABCDEFGHIJKLMNOPRSTUVZ
"
        
wiki_start_pages
=
[
"
Kezd
lap
"
]
    
)
    
"
Italian
"
:
Language
(
        
name
=
"
Italian
"
        
iso_code
=
"
it
"
        
use_ascii
=
True
        
charsets
=
[
"
ISO
-
8859
-
1
"
"
ISO
-
8859
-
15
"
"
WINDOWS
-
1252
"
"
MacRoman
"
]
        
alphabet
=
"
"
        
wiki_start_pages
=
[
"
Pagina_principale
"
]
    
)
    
"
Lithuanian
"
:
Language
(
        
name
=
"
Lithuanian
"
        
iso_code
=
"
lt
"
        
use_ascii
=
False
        
charsets
=
[
"
ISO
-
8859
-
13
"
"
WINDOWS
-
1257
"
"
ISO
-
8859
-
4
"
]
        
alphabet
=
"
A
BC
DE
FGHI
YJKLMNOPRS
TU
VZ
a
bc
de
fghi
yjklmnoprs
tu
vz
"
        
wiki_start_pages
=
[
"
Pagrindinis_puslapis
"
]
    
)
    
"
Latvian
"
:
Language
(
        
name
=
"
Latvian
"
        
iso_code
=
"
lv
"
        
use_ascii
=
False
        
charsets
=
[
"
ISO
-
8859
-
13
"
"
WINDOWS
-
1257
"
"
ISO
-
8859
-
4
"
]
        
alphabet
=
"
A
BC
DE
FG
HI
JK
L
MN
OPRS
TU
VZ
a
bc
de
fg
hi
jk
l
mn
oprs
tu
vz
"
        
wiki_start_pages
=
[
"
S
kumlapa
"
]
    
)
    
"
Macedonian
"
:
Language
(
        
name
=
"
Macedonian
"
        
iso_code
=
"
mk
"
        
use_ascii
=
False
        
charsets
=
[
"
ISO
-
8859
-
5
"
"
WINDOWS
-
1251
"
"
MacCyrillic
"
"
IBM855
"
]
        
alphabet
=
"
"
        
wiki_start_pages
=
[
"
_
"
]
    
)
    
"
Dutch
"
:
Language
(
        
name
=
"
Dutch
"
        
iso_code
=
"
nl
"
        
use_ascii
=
True
        
charsets
=
[
"
ISO
-
8859
-
1
"
"
WINDOWS
-
1252
"
"
MacRoman
"
]
        
wiki_start_pages
=
[
"
Hoofdpagina
"
]
    
)
    
"
Polish
"
:
Language
(
        
name
=
"
Polish
"
        
iso_code
=
"
pl
"
        
use_ascii
=
False
        
charsets
=
[
"
ISO
-
8859
-
2
"
"
WINDOWS
-
1250
"
]
        
alphabet
=
"
A
BC
DE
FGHIJKL
MN
O
PRS
TUWYZ
a
bc
de
fghijkl
mn
o
prs
tuwyz
"
        
wiki_start_pages
=
[
"
Wikipedia
:
Strona_g
wna
"
]
    
)
    
"
Portuguese
"
:
Language
(
        
name
=
"
Portuguese
"
        
iso_code
=
"
pt
"
        
use_ascii
=
True
        
charsets
=
[
"
ISO
-
8859
-
1
"
"
ISO
-
8859
-
15
"
"
WINDOWS
-
1252
"
"
MacRoman
"
]
        
alphabet
=
"
"
        
wiki_start_pages
=
[
"
Wikip
dia
:
P
gina_principal
"
]
    
)
    
"
Romanian
"
:
Language
(
        
name
=
"
Romanian
"
        
iso_code
=
"
ro
"
        
use_ascii
=
True
        
charsets
=
[
"
ISO
-
8859
-
2
"
"
WINDOWS
-
1250
"
]
        
alphabet
=
"
"
        
wiki_start_pages
=
[
"
Pagina_principal
"
]
    
)
    
"
Russian
"
:
Language
(
        
name
=
"
Russian
"
        
iso_code
=
"
ru
"
        
use_ascii
=
False
        
charsets
=
[
            
"
ISO
-
8859
-
5
"
            
"
WINDOWS
-
1251
"
            
"
KOI8
-
R
"
            
"
MacCyrillic
"
            
"
IBM866
"
            
"
IBM855
"
        
]
        
alphabet
=
"
"
        
wiki_start_pages
=
[
"
_
"
]
    
)
    
"
Slovak
"
:
Language
(
        
name
=
"
Slovak
"
        
iso_code
=
"
sk
"
        
use_ascii
=
True
        
charsets
=
[
"
ISO
-
8859
-
2
"
"
WINDOWS
-
1250
"
]
        
alphabet
=
"
"
        
wiki_start_pages
=
[
"
Hlavn
_str
nka
"
]
    
)
    
"
Slovene
"
:
Language
(
        
name
=
"
Slovene
"
        
iso_code
=
"
sl
"
        
use_ascii
=
False
        
charsets
=
[
"
ISO
-
8859
-
2
"
"
WINDOWS
-
1250
"
]
        
alphabet
=
"
abc
defghijklmnoprs
tuvz
ABC
DEFGHIJKLMNOPRS
TUVZ
"
        
wiki_start_pages
=
[
"
Glavna_stran
"
]
    
)
    
"
Serbian
"
:
Language
(
        
name
=
"
Serbian
"
        
iso_code
=
"
sr
"
        
alphabet
=
"
"
        
charsets
=
[
"
ISO
-
8859
-
5
"
"
WINDOWS
-
1251
"
"
MacCyrillic
"
"
IBM855
"
]
        
wiki_start_pages
=
[
"
_
"
]
    
)
    
"
Thai
"
:
Language
(
        
name
=
"
Thai
"
        
iso_code
=
"
th
"
        
use_ascii
=
False
        
charsets
=
[
"
ISO
-
8859
-
11
"
"
TIS
-
620
"
"
CP874
"
]
        
alphabet
=
"
"
        
wiki_start_pages
=
[
"
"
]
    
)
    
"
Turkish
"
:
Language
(
        
name
=
"
Turkish
"
        
iso_code
=
"
tr
"
        
use_ascii
=
False
        
charsets
=
[
"
ISO
-
8859
-
3
"
"
ISO
-
8859
-
9
"
"
WINDOWS
-
1254
"
]
        
alphabet
=
"
abc
defg
h
ijklmno
prs
tu
vyz
ABC
DEFG
HI
JKLMNO
PRS
TU
VYZ
"
        
wiki_start_pages
=
[
"
Ana_Sayfa
"
]
    
)
    
"
Vietnamese
"
:
Language
(
        
name
=
"
Vietnamese
"
        
iso_code
=
"
vi
"
        
use_ascii
=
False
        
charsets
=
[
"
WINDOWS
-
1258
"
]
        
alphabet
=
"
a
bcd
e
ghiklmno
pqrstu
vxyA
BCD
E
GHIKLMNO
PQRSTU
VXY
"
        
wiki_start_pages
=
[
"
Ch
_Qu
c_ng
"
]
    
)
}
