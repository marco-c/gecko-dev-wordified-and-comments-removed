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
__future__
import
absolute_import
print_function
from
string
import
ascii_letters
class
Language
(
object
)
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
=
None
iso_code
=
None
use_ascii
=
True
charsets
=
None
                 
alphabet
=
None
wiki_start_pages
=
None
)
:
        
super
(
Language
self
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
'
Must
supply
alphabet
if
use_ascii
is
False
'
)
        
self
.
alphabet
=
'
'
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
:
        
return
'
{
}
(
{
}
)
'
.
format
(
self
.
__class__
.
__name__
                               
'
'
.
join
(
'
{
}
=
{
!
r
}
'
.
format
(
k
v
)
                                         
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
'
_
'
)
)
)
LANGUAGES
=
{
'
Arabic
'
:
Language
(
name
=
'
Arabic
'
                                
iso_code
=
'
ar
'
                                
use_ascii
=
False
                                
charsets
=
[
'
ISO
-
8859
-
6
'
'
WINDOWS
-
1256
'
                                          
'
CP720
'
'
CP864
'
]
                                
alphabet
=
u
'
'
                                
wiki_start_pages
=
[
u
'
_
'
]
)
             
'
Belarusian
'
:
Language
(
name
=
'
Belarusian
'
                                    
iso_code
=
'
be
'
                                    
use_ascii
=
False
                                    
charsets
=
[
'
ISO
-
8859
-
5
'
'
WINDOWS
-
1251
'
                                              
'
IBM866
'
'
MacCyrillic
'
]
                                    
alphabet
=
(
u
'
'
                                              
u
'
'
)
                                    
wiki_start_pages
=
[
u
'
_
'
]
)
             
'
Bulgarian
'
:
Language
(
name
=
'
Bulgarian
'
                                   
iso_code
=
'
bg
'
                                   
use_ascii
=
False
                                   
charsets
=
[
'
ISO
-
8859
-
5
'
'
WINDOWS
-
1251
'
                                             
'
IBM855
'
]
                                   
alphabet
=
(
u
'
'
                                             
u
'
'
)
                                   
wiki_start_pages
=
[
u
'
_
'
]
)
             
'
Czech
'
:
Language
(
name
=
'
Czech
'
                               
iso_code
=
'
cz
'
                               
use_ascii
=
True
                               
charsets
=
[
'
ISO
-
8859
-
2
'
'
WINDOWS
-
1250
'
]
                               
alphabet
=
u
'
'
                               
wiki_start_pages
=
[
u
'
Hlavn
_strana
'
]
)
             
'
Danish
'
:
Language
(
name
=
'
Danish
'
                                
iso_code
=
'
da
'
                                
use_ascii
=
True
                                
charsets
=
[
'
ISO
-
8859
-
1
'
'
ISO
-
8859
-
15
'
                                          
'
WINDOWS
-
1252
'
]
                                
alphabet
=
u
'
'
                                
wiki_start_pages
=
[
u
'
Forside
'
]
)
             
'
German
'
:
Language
(
name
=
'
German
'
                                
iso_code
=
'
de
'
                                
use_ascii
=
True
                                
charsets
=
[
'
ISO
-
8859
-
1
'
'
WINDOWS
-
1252
'
]
                                
alphabet
=
u
'
'
                                
wiki_start_pages
=
[
u
'
Wikipedia
:
Hauptseite
'
]
)
             
'
Greek
'
:
Language
(
name
=
'
Greek
'
                               
iso_code
=
'
el
'
                               
use_ascii
=
False
                               
charsets
=
[
'
ISO
-
8859
-
7
'
'
WINDOWS
-
1253
'
]
                               
alphabet
=
(
u
'
'
                                         
u
'
'
)
                               
wiki_start_pages
=
[
u
'
:
'
]
)
             
'
English
'
:
Language
(
name
=
'
English
'
                                 
iso_code
=
'
en
'
                                 
use_ascii
=
True
                                 
charsets
=
[
'
ISO
-
8859
-
1
'
'
WINDOWS
-
1252
'
]
                                 
wiki_start_pages
=
[
u
'
Main_Page
'
]
)
             
'
Esperanto
'
:
Language
(
name
=
'
Esperanto
'
                                   
iso_code
=
'
eo
'
                                   
use_ascii
=
False
                                   
charsets
=
[
'
ISO
-
8859
-
3
'
]
                                   
alphabet
=
(
u
'
abc
defg
h
ij
klmnoprs
tu
vz
'
                                             
u
'
ABC
DEFG
H
IJ
KLMNOPRS
TU
VZ
'
)
                                   
wiki_start_pages
=
[
u
'
Vikipedio
:
efpa
o
'
]
)
             
'
Spanish
'
:
Language
(
name
=
'
Spanish
'
                                 
iso_code
=
'
es
'
                                 
use_ascii
=
True
                                 
charsets
=
[
'
ISO
-
8859
-
1
'
'
ISO
-
8859
-
15
'
                                           
'
WINDOWS
-
1252
'
]
                                 
alphabet
=
u
'
'
                                 
wiki_start_pages
=
[
u
'
Wikipedia
:
Portada
'
]
)
             
'
Estonian
'
:
Language
(
name
=
'
Estonian
'
                                  
iso_code
=
'
et
'
                                  
use_ascii
=
False
                                  
charsets
=
[
'
ISO
-
8859
-
4
'
'
ISO
-
8859
-
13
'
                                            
'
WINDOWS
-
1257
'
]
                                  
alphabet
=
(
u
'
ABDEGHIJKLMNOPRSTUV
'
                                            
u
'
abdeghijklmnoprstuv
'
)
                                  
wiki_start_pages
=
[
u
'
Esileht
'
]
)
             
'
Finnish
'
:
Language
(
name
=
'
Finnish
'
                                 
iso_code
=
'
fi
'
                                 
use_ascii
=
True
                                 
charsets
=
[
'
ISO
-
8859
-
1
'
'
ISO
-
8859
-
15
'
                                           
'
WINDOWS
-
1252
'
]
                                 
alphabet
=
u
'
'
                                 
wiki_start_pages
=
[
u
'
Wikipedia
:
Etusivu
'
]
)
             
'
French
'
:
Language
(
name
=
'
French
'
                                
iso_code
=
'
fr
'
                                
use_ascii
=
True
                                
charsets
=
[
'
ISO
-
8859
-
1
'
'
ISO
-
8859
-
15
'
                                          
'
WINDOWS
-
1252
'
]
                                
alphabet
=
u
'
'
                                
wiki_start_pages
=
[
u
'
Wikip
dia
:
Accueil_principal
'
                                                  
u
'
B
uf
(
animal
)
'
]
)
             
'
Hebrew
'
:
Language
(
name
=
'
Hebrew
'
                                
iso_code
=
'
he
'
                                
use_ascii
=
False
                                
charsets
=
[
'
ISO
-
8859
-
8
'
'
WINDOWS
-
1255
'
]
                                
alphabet
=
u
'
'
                                
wiki_start_pages
=
[
u
'
_
'
]
)
             
'
Croatian
'
:
Language
(
name
=
'
Croatian
'
                                  
iso_code
=
'
hr
'
                                  
use_ascii
=
False
                                  
charsets
=
[
'
ISO
-
8859
-
2
'
'
WINDOWS
-
1250
'
]
                                  
alphabet
=
(
u
'
abc
d
efghijklmnoprs
tuvz
'
                                            
u
'
ABC
D
EFGHIJKLMNOPRS
TUVZ
'
)
                                  
wiki_start_pages
=
[
u
'
Glavna_stranica
'
]
)
             
'
Hungarian
'
:
Language
(
name
=
'
Hungarian
'
                                   
iso_code
=
'
hu
'
                                   
use_ascii
=
False
                                   
charsets
=
[
'
ISO
-
8859
-
2
'
'
WINDOWS
-
1250
'
]
                                   
alphabet
=
(
u
'
abcdefghijklmnoprstuvz
'
                                             
u
'
ABCDEFGHIJKLMNOPRSTUVZ
'
)
                                   
wiki_start_pages
=
[
u
'
Kezd
lap
'
]
)
             
'
Italian
'
:
Language
(
name
=
'
Italian
'
                                 
iso_code
=
'
it
'
                                 
use_ascii
=
True
                                 
charsets
=
[
'
ISO
-
8859
-
1
'
'
ISO
-
8859
-
15
'
                                           
'
WINDOWS
-
1252
'
]
                                 
alphabet
=
u
'
'
                                 
wiki_start_pages
=
[
u
'
Pagina_principale
'
]
)
             
'
Lithuanian
'
:
Language
(
name
=
'
Lithuanian
'
                                    
iso_code
=
'
lt
'
                                    
use_ascii
=
False
                                    
charsets
=
[
'
ISO
-
8859
-
13
'
'
WINDOWS
-
1257
'
                                              
'
ISO
-
8859
-
4
'
]
                                    
alphabet
=
(
u
'
A
BC
DE
FGHI
YJKLMNOPRS
TU
VZ
'
                                              
u
'
a
bc
de
fghi
yjklmnoprs
tu
vz
'
)
                                    
wiki_start_pages
=
[
u
'
Pagrindinis_puslapis
'
]
)
             
'
Latvian
'
:
Language
(
name
=
'
Latvian
'
                                 
iso_code
=
'
lv
'
                                 
use_ascii
=
False
                                 
charsets
=
[
'
ISO
-
8859
-
13
'
'
WINDOWS
-
1257
'
                                           
'
ISO
-
8859
-
4
'
]
                                 
alphabet
=
(
u
'
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
'
                                           
u
'
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
'
)
                                 
wiki_start_pages
=
[
u
'
S
kumlapa
'
]
)
             
'
Macedonian
'
:
Language
(
name
=
'
Macedonian
'
                                    
iso_code
=
'
mk
'
                                    
use_ascii
=
False
                                    
charsets
=
[
'
ISO
-
8859
-
5
'
'
WINDOWS
-
1251
'
                                              
'
MacCyrillic
'
'
IBM855
'
]
                                    
alphabet
=
(
u
'
'
                                              
u
'
'
)
                                    
wiki_start_pages
=
[
u
'
_
'
]
)
             
'
Dutch
'
:
Language
(
name
=
'
Dutch
'
                               
iso_code
=
'
nl
'
                               
use_ascii
=
True
                               
charsets
=
[
'
ISO
-
8859
-
1
'
'
WINDOWS
-
1252
'
]
                               
wiki_start_pages
=
[
u
'
Hoofdpagina
'
]
)
             
'
Polish
'
:
Language
(
name
=
'
Polish
'
                                
iso_code
=
'
pl
'
                                
use_ascii
=
False
                                
charsets
=
[
'
ISO
-
8859
-
2
'
'
WINDOWS
-
1250
'
]
                                
alphabet
=
(
u
'
A
BC
DE
FGHIJKL
MN
O
PRS
TUWYZ
'
                                          
u
'
a
bc
de
fghijkl
mn
o
prs
tuwyz
'
)
                                
wiki_start_pages
=
[
u
'
Wikipedia
:
Strona_g
wna
'
]
)
             
'
Portuguese
'
:
Language
(
name
=
'
Portuguese
'
                                 
iso_code
=
'
pt
'
                                 
use_ascii
=
True
                                 
charsets
=
[
'
ISO
-
8859
-
1
'
'
ISO
-
8859
-
15
'
                                           
'
WINDOWS
-
1252
'
]
                                 
alphabet
=
u
'
'
                                 
wiki_start_pages
=
[
u
'
Wikip
dia
:
P
gina_principal
'
]
)
             
'
Romanian
'
:
Language
(
name
=
'
Romanian
'
                                  
iso_code
=
'
ro
'
                                  
use_ascii
=
True
                                  
charsets
=
[
'
ISO
-
8859
-
2
'
'
WINDOWS
-
1250
'
]
                                  
alphabet
=
u
'
'
                                  
wiki_start_pages
=
[
u
'
Pagina_principal
'
]
)
             
'
Russian
'
:
Language
(
name
=
'
Russian
'
                                 
iso_code
=
'
ru
'
                                 
use_ascii
=
False
                                 
charsets
=
[
'
ISO
-
8859
-
5
'
'
WINDOWS
-
1251
'
                                           
'
KOI8
-
R
'
'
MacCyrillic
'
'
IBM866
'
                                           
'
IBM855
'
]
                                 
alphabet
=
(
u
'
'
                                           
u
'
'
)
                                 
wiki_start_pages
=
[
u
'
_
'
]
)
             
'
Slovak
'
:
Language
(
name
=
'
Slovak
'
                                
iso_code
=
'
sk
'
                                
use_ascii
=
True
                                
charsets
=
[
'
ISO
-
8859
-
2
'
'
WINDOWS
-
1250
'
]
                                
alphabet
=
u
'
'
                                
wiki_start_pages
=
[
u
'
Hlavn
_str
nka
'
]
)
             
'
Slovene
'
:
Language
(
name
=
'
Slovene
'
                                 
iso_code
=
'
sl
'
                                 
use_ascii
=
False
                                 
charsets
=
[
'
ISO
-
8859
-
2
'
'
WINDOWS
-
1250
'
]
                                 
alphabet
=
(
u
'
abc
defghijklmnoprs
tuvz
'
                                           
u
'
ABC
DEFGHIJKLMNOPRS
TUVZ
'
)
                                 
wiki_start_pages
=
[
u
'
Glavna_stran
'
]
)
             
'
Serbian
'
:
Language
(
name
=
'
Serbian
'
                                 
iso_code
=
'
sr
'
                                 
alphabet
=
(
u
'
'
                                           
u
'
'
)
                                 
charsets
=
[
'
ISO
-
8859
-
5
'
'
WINDOWS
-
1251
'
                                           
'
MacCyrillic
'
'
IBM855
'
]
                                 
wiki_start_pages
=
[
u
'
_
'
]
)
             
'
Thai
'
:
Language
(
name
=
'
Thai
'
                              
iso_code
=
'
th
'
                              
use_ascii
=
False
                              
charsets
=
[
'
ISO
-
8859
-
11
'
'
TIS
-
620
'
'
CP874
'
]
                              
alphabet
=
u
'
'
                              
wiki_start_pages
=
[
u
'
'
]
)
             
'
Turkish
'
:
Language
(
name
=
'
Turkish
'
                                 
iso_code
=
'
tr
'
                                 
use_ascii
=
False
                                 
charsets
=
[
'
ISO
-
8859
-
3
'
'
ISO
-
8859
-
9
'
                                           
'
WINDOWS
-
1254
'
]
                                 
alphabet
=
(
u
'
abc
defg
h
ijklmno
prs
tu
vyz
'
                                           
u
'
ABC
DEFG
HI
JKLMNO
PRS
TU
VYZ
'
)
                                 
wiki_start_pages
=
[
u
'
Ana_Sayfa
'
]
)
             
'
Vietnamese
'
:
Language
(
name
=
'
Vietnamese
'
                                    
iso_code
=
'
vi
'
                                    
use_ascii
=
False
                                    
charsets
=
[
'
WINDOWS
-
1258
'
]
                                    
alphabet
=
(
u
'
a
bcd
e
ghiklmno
pqrstu
vxy
'
                                              
u
'
A
BCD
E
GHIKLMNO
PQRSTU
VXY
'
)
                                    
wiki_start_pages
=
[
u
'
Ch
_Qu
c_ng
'
]
)
            
}
