"
"
"
Provides
internationalization
for
arrow
in
over
60
languages
and
dialects
.
"
"
"
import
sys
from
math
import
trunc
from
typing
import
(
    
Any
    
ClassVar
    
Dict
    
List
    
Mapping
    
Optional
    
Sequence
    
Tuple
    
Type
    
Union
    
cast
)
if
sys
.
version_info
<
(
3
8
)
:
    
from
typing_extensions
import
Literal
else
:
    
from
typing
import
Literal
TimeFrameLiteral
=
Literal
[
    
"
now
"
    
"
second
"
    
"
seconds
"
    
"
minute
"
    
"
minutes
"
    
"
hour
"
    
"
hours
"
    
"
day
"
    
"
days
"
    
"
week
"
    
"
weeks
"
    
"
month
"
    
"
months
"
    
"
quarter
"
    
"
quarters
"
    
"
year
"
    
"
years
"
]
_TimeFrameElements
=
Union
[
    
str
Sequence
[
str
]
Mapping
[
str
str
]
Mapping
[
str
Sequence
[
str
]
]
]
_locale_map
:
Dict
[
str
Type
[
"
Locale
"
]
]
=
{
}
def
get_locale
(
name
:
str
)
-
>
"
Locale
"
:
    
"
"
"
Returns
an
appropriate
:
class
:
Locale
<
arrow
.
locales
.
Locale
>
    
corresponding
to
an
input
locale
name
.
    
:
param
name
:
the
name
of
the
locale
.
    
"
"
"
    
normalized_locale_name
=
name
.
lower
(
)
.
replace
(
"
_
"
"
-
"
)
    
locale_cls
=
_locale_map
.
get
(
normalized_locale_name
)
    
if
locale_cls
is
None
:
        
raise
ValueError
(
f
"
Unsupported
locale
{
normalized_locale_name
!
r
}
.
"
)
    
return
locale_cls
(
)
def
get_locale_by_class_name
(
name
:
str
)
-
>
"
Locale
"
:
    
"
"
"
Returns
an
appropriate
:
class
:
Locale
<
arrow
.
locales
.
Locale
>
    
corresponding
to
an
locale
class
name
.
    
:
param
name
:
the
name
of
the
locale
class
.
    
"
"
"
    
locale_cls
:
Optional
[
Type
[
Locale
]
]
=
globals
(
)
.
get
(
name
)
    
if
locale_cls
is
None
:
        
raise
ValueError
(
f
"
Unsupported
locale
{
name
!
r
}
.
"
)
    
return
locale_cls
(
)
class
Locale
:
    
"
"
"
Represents
locale
-
specific
data
and
functionality
.
"
"
"
    
names
:
ClassVar
[
List
[
str
]
]
=
[
]
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
_TimeFrameElements
]
]
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
"
"
        
"
minute
"
:
"
"
        
"
minutes
"
:
"
"
        
"
hour
"
:
"
"
        
"
hours
"
:
"
"
        
"
day
"
:
"
"
        
"
days
"
:
"
"
        
"
week
"
:
"
"
        
"
weeks
"
:
"
"
        
"
month
"
:
"
"
        
"
months
"
:
"
"
        
"
quarter
"
:
"
"
        
"
quarters
"
:
"
"
        
"
year
"
:
"
"
        
"
years
"
:
"
"
    
}
    
meridians
:
ClassVar
[
Dict
[
str
str
]
]
=
{
"
am
"
:
"
"
"
pm
"
:
"
"
"
AM
"
:
"
"
"
PM
"
:
"
"
}
    
past
:
ClassVar
[
str
]
    
future
:
ClassVar
[
str
]
    
and_word
:
ClassVar
[
Optional
[
str
]
]
=
None
    
month_names
:
ClassVar
[
List
[
str
]
]
=
[
]
    
month_abbreviations
:
ClassVar
[
List
[
str
]
]
=
[
]
    
day_names
:
ClassVar
[
List
[
str
]
]
=
[
]
    
day_abbreviations
:
ClassVar
[
List
[
str
]
]
=
[
]
    
ordinal_day_re
:
ClassVar
[
str
]
=
r
"
(
\
d
+
)
"
    
_month_name_to_ordinal
:
Optional
[
Dict
[
str
int
]
]
    
def
__init_subclass__
(
cls
*
*
kwargs
:
Any
)
-
>
None
:
        
for
locale_name
in
cls
.
names
:
            
if
locale_name
in
_locale_map
:
                
raise
LookupError
(
f
"
Duplicated
locale
name
:
{
locale_name
}
"
)
            
_locale_map
[
locale_name
.
lower
(
)
.
replace
(
"
_
"
"
-
"
)
]
=
cls
    
def
__init__
(
self
)
-
>
None
:
        
self
.
_month_name_to_ordinal
=
None
    
def
describe
(
        
self
        
timeframe
:
TimeFrameLiteral
        
delta
:
Union
[
float
int
]
=
0
        
only_distance
:
bool
=
False
    
)
-
>
str
:
        
"
"
"
Describes
a
delta
within
a
timeframe
in
plain
language
.
        
:
param
timeframe
:
a
string
representing
a
timeframe
.
        
:
param
delta
:
a
quantity
representing
a
delta
in
a
timeframe
.
        
:
param
only_distance
:
return
only
distance
eg
:
"
11
seconds
"
without
"
in
"
or
"
ago
"
keywords
        
"
"
"
        
humanized
=
self
.
_format_timeframe
(
timeframe
trunc
(
delta
)
)
        
if
not
only_distance
:
            
humanized
=
self
.
_format_relative
(
humanized
timeframe
delta
)
        
return
humanized
    
def
describe_multi
(
        
self
        
timeframes
:
Sequence
[
Tuple
[
TimeFrameLiteral
Union
[
int
float
]
]
]
        
only_distance
:
bool
=
False
    
)
-
>
str
:
        
"
"
"
Describes
a
delta
within
multiple
timeframes
in
plain
language
.
        
:
param
timeframes
:
a
list
of
string
quantity
pairs
each
representing
a
timeframe
and
delta
.
        
:
param
only_distance
:
return
only
distance
eg
:
"
2
hours
and
11
seconds
"
without
"
in
"
or
"
ago
"
keywords
        
"
"
"
        
parts
=
[
            
self
.
_format_timeframe
(
timeframe
trunc
(
delta
)
)
            
for
timeframe
delta
in
timeframes
        
]
        
if
self
.
and_word
:
            
parts
.
insert
(
-
1
self
.
and_word
)
        
humanized
=
"
"
.
join
(
parts
)
        
if
not
only_distance
:
            
timeframe_value
=
0
            
for
_
unit_value
in
timeframes
:
                
if
trunc
(
unit_value
)
!
=
0
:
                    
timeframe_value
=
trunc
(
unit_value
)
                    
break
            
humanized
=
self
.
_format_relative
(
humanized
"
seconds
"
timeframe_value
)
        
return
humanized
    
def
day_name
(
self
day
:
int
)
-
>
str
:
        
"
"
"
Returns
the
day
name
for
a
specified
day
of
the
week
.
        
:
param
day
:
the
int
day
of
the
week
(
1
-
7
)
.
        
"
"
"
        
return
self
.
day_names
[
day
]
    
def
day_abbreviation
(
self
day
:
int
)
-
>
str
:
        
"
"
"
Returns
the
day
abbreviation
for
a
specified
day
of
the
week
.
        
:
param
day
:
the
int
day
of
the
week
(
1
-
7
)
.
        
"
"
"
        
return
self
.
day_abbreviations
[
day
]
    
def
month_name
(
self
month
:
int
)
-
>
str
:
        
"
"
"
Returns
the
month
name
for
a
specified
month
of
the
year
.
        
:
param
month
:
the
int
month
of
the
year
(
1
-
12
)
.
        
"
"
"
        
return
self
.
month_names
[
month
]
    
def
month_abbreviation
(
self
month
:
int
)
-
>
str
:
        
"
"
"
Returns
the
month
abbreviation
for
a
specified
month
of
the
year
.
        
:
param
month
:
the
int
month
of
the
year
(
1
-
12
)
.
        
"
"
"
        
return
self
.
month_abbreviations
[
month
]
    
def
month_number
(
self
name
:
str
)
-
>
Optional
[
int
]
:
        
"
"
"
Returns
the
month
number
for
a
month
specified
by
name
or
abbreviation
.
        
:
param
name
:
the
month
name
or
abbreviation
.
        
"
"
"
        
if
self
.
_month_name_to_ordinal
is
None
:
            
self
.
_month_name_to_ordinal
=
self
.
_name_to_ordinal
(
self
.
month_names
)
            
self
.
_month_name_to_ordinal
.
update
(
                
self
.
_name_to_ordinal
(
self
.
month_abbreviations
)
            
)
        
return
self
.
_month_name_to_ordinal
.
get
(
name
)
    
def
year_full
(
self
year
:
int
)
-
>
str
:
        
"
"
"
Returns
the
year
for
specific
locale
if
available
        
:
param
year
:
the
int
year
(
4
-
digit
)
        
"
"
"
        
return
f
"
{
year
:
04d
}
"
    
def
year_abbreviation
(
self
year
:
int
)
-
>
str
:
        
"
"
"
Returns
the
year
for
specific
locale
if
available
        
:
param
year
:
the
int
year
(
4
-
digit
)
        
"
"
"
        
return
f
"
{
year
:
04d
}
"
[
2
:
]
    
def
meridian
(
self
hour
:
int
token
:
Any
)
-
>
Optional
[
str
]
:
        
"
"
"
Returns
the
meridian
indicator
for
a
specified
hour
and
format
token
.
        
:
param
hour
:
the
int
hour
of
the
day
.
        
:
param
token
:
the
format
token
.
        
"
"
"
        
if
token
=
=
"
a
"
:
            
return
self
.
meridians
[
"
am
"
]
if
hour
<
12
else
self
.
meridians
[
"
pm
"
]
        
if
token
=
=
"
A
"
:
            
return
self
.
meridians
[
"
AM
"
]
if
hour
<
12
else
self
.
meridians
[
"
PM
"
]
        
return
None
    
def
ordinal_number
(
self
n
:
int
)
-
>
str
:
        
"
"
"
Returns
the
ordinal
format
of
a
given
integer
        
:
param
n
:
an
integer
        
"
"
"
        
return
self
.
_ordinal_number
(
n
)
    
def
_ordinal_number
(
self
n
:
int
)
-
>
str
:
        
return
f
"
{
n
}
"
    
def
_name_to_ordinal
(
self
lst
:
Sequence
[
str
]
)
-
>
Dict
[
str
int
]
:
        
return
{
elem
.
lower
(
)
:
i
for
i
elem
in
enumerate
(
lst
[
1
:
]
1
)
}
    
def
_format_timeframe
(
self
timeframe
:
TimeFrameLiteral
delta
:
int
)
-
>
str
:
        
return
cast
(
str
self
.
timeframes
[
timeframe
]
)
.
format
(
trunc
(
abs
(
delta
)
)
)
    
def
_format_relative
(
        
self
        
humanized
:
str
        
timeframe
:
TimeFrameLiteral
        
delta
:
Union
[
float
int
]
    
)
-
>
str
:
        
if
timeframe
=
=
"
now
"
:
            
return
humanized
        
direction
=
self
.
past
if
delta
<
0
else
self
.
future
        
return
direction
.
format
(
humanized
)
class
EnglishLocale
(
Locale
)
:
    
names
=
[
        
"
en
"
        
"
en
-
us
"
        
"
en
-
gb
"
        
"
en
-
au
"
        
"
en
-
be
"
        
"
en
-
jp
"
        
"
en
-
za
"
        
"
en
-
ca
"
        
"
en
-
ph
"
    
]
    
past
=
"
{
0
}
ago
"
    
future
=
"
in
{
0
}
"
    
and_word
=
"
and
"
    
timeframes
=
{
        
"
now
"
:
"
just
now
"
        
"
second
"
:
"
a
second
"
        
"
seconds
"
:
"
{
0
}
seconds
"
        
"
minute
"
:
"
a
minute
"
        
"
minutes
"
:
"
{
0
}
minutes
"
        
"
hour
"
:
"
an
hour
"
        
"
hours
"
:
"
{
0
}
hours
"
        
"
day
"
:
"
a
day
"
        
"
days
"
:
"
{
0
}
days
"
        
"
week
"
:
"
a
week
"
        
"
weeks
"
:
"
{
0
}
weeks
"
        
"
month
"
:
"
a
month
"
        
"
months
"
:
"
{
0
}
months
"
        
"
quarter
"
:
"
a
quarter
"
        
"
quarters
"
:
"
{
0
}
quarters
"
        
"
year
"
:
"
a
year
"
        
"
years
"
:
"
{
0
}
years
"
    
}
    
meridians
=
{
"
am
"
:
"
am
"
"
pm
"
:
"
pm
"
"
AM
"
:
"
AM
"
"
PM
"
:
"
PM
"
}
    
month_names
=
[
        
"
"
        
"
January
"
        
"
February
"
        
"
March
"
        
"
April
"
        
"
May
"
        
"
June
"
        
"
July
"
        
"
August
"
        
"
September
"
        
"
October
"
        
"
November
"
        
"
December
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
Jan
"
        
"
Feb
"
        
"
Mar
"
        
"
Apr
"
        
"
May
"
        
"
Jun
"
        
"
Jul
"
        
"
Aug
"
        
"
Sep
"
        
"
Oct
"
        
"
Nov
"
        
"
Dec
"
    
]
    
day_names
=
[
        
"
"
        
"
Monday
"
        
"
Tuesday
"
        
"
Wednesday
"
        
"
Thursday
"
        
"
Friday
"
        
"
Saturday
"
        
"
Sunday
"
    
]
    
day_abbreviations
=
[
"
"
"
Mon
"
"
Tue
"
"
Wed
"
"
Thu
"
"
Fri
"
"
Sat
"
"
Sun
"
]
    
ordinal_day_re
=
r
"
(
(
?
P
<
value
>
[
2
-
3
]
?
1
(
?
=
st
)
|
[
2
-
3
]
?
2
(
?
=
nd
)
|
[
2
-
3
]
?
3
(
?
=
rd
)
|
[
1
-
3
]
?
[
04
-
9
]
(
?
=
th
)
|
1
[
1
-
3
]
(
?
=
th
)
)
(
st
|
nd
|
rd
|
th
)
)
"
    
def
_ordinal_number
(
self
n
:
int
)
-
>
str
:
        
if
n
%
100
not
in
(
11
12
13
)
:
            
remainder
=
abs
(
n
)
%
10
            
if
remainder
=
=
1
:
                
return
f
"
{
n
}
st
"
            
elif
remainder
=
=
2
:
                
return
f
"
{
n
}
nd
"
            
elif
remainder
=
=
3
:
                
return
f
"
{
n
}
rd
"
        
return
f
"
{
n
}
th
"
    
def
describe
(
        
self
        
timeframe
:
TimeFrameLiteral
        
delta
:
Union
[
int
float
]
=
0
        
only_distance
:
bool
=
False
    
)
-
>
str
:
        
"
"
"
Describes
a
delta
within
a
timeframe
in
plain
language
.
        
:
param
timeframe
:
a
string
representing
a
timeframe
.
        
:
param
delta
:
a
quantity
representing
a
delta
in
a
timeframe
.
        
:
param
only_distance
:
return
only
distance
eg
:
"
11
seconds
"
without
"
in
"
or
"
ago
"
keywords
        
"
"
"
        
humanized
=
super
(
)
.
describe
(
timeframe
delta
only_distance
)
        
if
only_distance
and
timeframe
=
=
"
now
"
:
            
humanized
=
"
instantly
"
        
return
humanized
class
ItalianLocale
(
Locale
)
:
    
names
=
[
"
it
"
"
it
-
it
"
]
    
past
=
"
{
0
}
fa
"
    
future
=
"
tra
{
0
}
"
    
and_word
=
"
e
"
    
timeframes
=
{
        
"
now
"
:
"
adesso
"
        
"
second
"
:
"
un
secondo
"
        
"
seconds
"
:
"
{
0
}
qualche
secondo
"
        
"
minute
"
:
"
un
minuto
"
        
"
minutes
"
:
"
{
0
}
minuti
"
        
"
hour
"
:
"
un
'
ora
"
        
"
hours
"
:
"
{
0
}
ore
"
        
"
day
"
:
"
un
giorno
"
        
"
days
"
:
"
{
0
}
giorni
"
        
"
week
"
:
"
una
settimana
"
        
"
weeks
"
:
"
{
0
}
settimane
"
        
"
month
"
:
"
un
mese
"
        
"
months
"
:
"
{
0
}
mesi
"
        
"
year
"
:
"
un
anno
"
        
"
years
"
:
"
{
0
}
anni
"
    
}
    
month_names
=
[
        
"
"
        
"
gennaio
"
        
"
febbraio
"
        
"
marzo
"
        
"
aprile
"
        
"
maggio
"
        
"
giugno
"
        
"
luglio
"
        
"
agosto
"
        
"
settembre
"
        
"
ottobre
"
        
"
novembre
"
        
"
dicembre
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
gen
"
        
"
feb
"
        
"
mar
"
        
"
apr
"
        
"
mag
"
        
"
giu
"
        
"
lug
"
        
"
ago
"
        
"
set
"
        
"
ott
"
        
"
nov
"
        
"
dic
"
    
]
    
day_names
=
[
        
"
"
        
"
luned
"
        
"
marted
"
        
"
mercoled
"
        
"
gioved
"
        
"
venerd
"
        
"
sabato
"
        
"
domenica
"
    
]
    
day_abbreviations
=
[
"
"
"
lun
"
"
mar
"
"
mer
"
"
gio
"
"
ven
"
"
sab
"
"
dom
"
]
    
ordinal_day_re
=
r
"
(
(
?
P
<
value
>
[
1
-
3
]
?
[
0
-
9
]
(
?
=
[
]
)
)
[
]
)
"
    
def
_ordinal_number
(
self
n
:
int
)
-
>
str
:
        
return
f
"
{
n
}
"
class
SpanishLocale
(
Locale
)
:
    
names
=
[
"
es
"
"
es
-
es
"
]
    
past
=
"
hace
{
0
}
"
    
future
=
"
en
{
0
}
"
    
and_word
=
"
y
"
    
timeframes
=
{
        
"
now
"
:
"
ahora
"
        
"
second
"
:
"
un
segundo
"
        
"
seconds
"
:
"
{
0
}
segundos
"
        
"
minute
"
:
"
un
minuto
"
        
"
minutes
"
:
"
{
0
}
minutos
"
        
"
hour
"
:
"
una
hora
"
        
"
hours
"
:
"
{
0
}
horas
"
        
"
day
"
:
"
un
d
a
"
        
"
days
"
:
"
{
0
}
d
as
"
        
"
week
"
:
"
una
semana
"
        
"
weeks
"
:
"
{
0
}
semanas
"
        
"
month
"
:
"
un
mes
"
        
"
months
"
:
"
{
0
}
meses
"
        
"
year
"
:
"
un
a
o
"
        
"
years
"
:
"
{
0
}
a
os
"
    
}
    
meridians
=
{
"
am
"
:
"
am
"
"
pm
"
:
"
pm
"
"
AM
"
:
"
AM
"
"
PM
"
:
"
PM
"
}
    
month_names
=
[
        
"
"
        
"
enero
"
        
"
febrero
"
        
"
marzo
"
        
"
abril
"
        
"
mayo
"
        
"
junio
"
        
"
julio
"
        
"
agosto
"
        
"
septiembre
"
        
"
octubre
"
        
"
noviembre
"
        
"
diciembre
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
ene
"
        
"
feb
"
        
"
mar
"
        
"
abr
"
        
"
may
"
        
"
jun
"
        
"
jul
"
        
"
ago
"
        
"
sep
"
        
"
oct
"
        
"
nov
"
        
"
dic
"
    
]
    
day_names
=
[
        
"
"
        
"
lunes
"
        
"
martes
"
        
"
mi
rcoles
"
        
"
jueves
"
        
"
viernes
"
        
"
s
bado
"
        
"
domingo
"
    
]
    
day_abbreviations
=
[
"
"
"
lun
"
"
mar
"
"
mie
"
"
jue
"
"
vie
"
"
sab
"
"
dom
"
]
    
ordinal_day_re
=
r
"
(
(
?
P
<
value
>
[
1
-
3
]
?
[
0
-
9
]
(
?
=
[
]
)
)
[
]
)
"
    
def
_ordinal_number
(
self
n
:
int
)
-
>
str
:
        
return
f
"
{
n
}
"
class
FrenchBaseLocale
(
Locale
)
:
    
past
=
"
il
y
a
{
0
}
"
    
future
=
"
dans
{
0
}
"
    
and_word
=
"
et
"
    
timeframes
=
{
        
"
now
"
:
"
maintenant
"
        
"
second
"
:
"
une
seconde
"
        
"
seconds
"
:
"
{
0
}
secondes
"
        
"
minute
"
:
"
une
minute
"
        
"
minutes
"
:
"
{
0
}
minutes
"
        
"
hour
"
:
"
une
heure
"
        
"
hours
"
:
"
{
0
}
heures
"
        
"
day
"
:
"
un
jour
"
        
"
days
"
:
"
{
0
}
jours
"
        
"
week
"
:
"
une
semaine
"
        
"
weeks
"
:
"
{
0
}
semaines
"
        
"
month
"
:
"
un
mois
"
        
"
months
"
:
"
{
0
}
mois
"
        
"
year
"
:
"
un
an
"
        
"
years
"
:
"
{
0
}
ans
"
    
}
    
month_names
=
[
        
"
"
        
"
janvier
"
        
"
f
vrier
"
        
"
mars
"
        
"
avril
"
        
"
mai
"
        
"
juin
"
        
"
juillet
"
        
"
ao
t
"
        
"
septembre
"
        
"
octobre
"
        
"
novembre
"
        
"
d
cembre
"
    
]
    
day_names
=
[
        
"
"
        
"
lundi
"
        
"
mardi
"
        
"
mercredi
"
        
"
jeudi
"
        
"
vendredi
"
        
"
samedi
"
        
"
dimanche
"
    
]
    
day_abbreviations
=
[
"
"
"
lun
"
"
mar
"
"
mer
"
"
jeu
"
"
ven
"
"
sam
"
"
dim
"
]
    
ordinal_day_re
=
(
        
r
"
(
(
?
P
<
value
>
\
b1
(
?
=
er
\
b
)
|
[
1
-
3
]
?
[
02
-
9
]
(
?
=
e
\
b
)
|
[
1
-
3
]
1
(
?
=
e
\
b
)
)
(
er
|
e
)
\
b
)
"
    
)
    
def
_ordinal_number
(
self
n
:
int
)
-
>
str
:
        
if
abs
(
n
)
=
=
1
:
            
return
f
"
{
n
}
er
"
        
return
f
"
{
n
}
e
"
class
FrenchLocale
(
FrenchBaseLocale
Locale
)
:
    
names
=
[
"
fr
"
"
fr
-
fr
"
]
    
month_abbreviations
=
[
        
"
"
        
"
janv
"
        
"
f
vr
"
        
"
mars
"
        
"
avr
"
        
"
mai
"
        
"
juin
"
        
"
juil
"
        
"
ao
t
"
        
"
sept
"
        
"
oct
"
        
"
nov
"
        
"
d
c
"
    
]
class
FrenchCanadianLocale
(
FrenchBaseLocale
Locale
)
:
    
names
=
[
"
fr
-
ca
"
]
    
month_abbreviations
=
[
        
"
"
        
"
janv
"
        
"
f
vr
"
        
"
mars
"
        
"
avr
"
        
"
mai
"
        
"
juin
"
        
"
juill
"
        
"
ao
t
"
        
"
sept
"
        
"
oct
"
        
"
nov
"
        
"
d
c
"
    
]
class
GreekLocale
(
Locale
)
:
    
names
=
[
"
el
"
"
el
-
gr
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
and_word
=
"
"
    
timeframes
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
"
        
"
days
"
:
"
{
0
}
"
        
"
week
"
:
"
"
        
"
weeks
"
:
"
{
0
}
"
        
"
month
"
:
"
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
"
        
"
years
"
:
"
{
0
}
"
    
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
class
JapaneseLocale
(
Locale
)
:
    
names
=
[
"
ja
"
"
ja
-
jp
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
and_word
=
"
"
    
timeframes
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
1
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
1
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
1
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
1
"
        
"
days
"
:
"
{
0
}
"
        
"
week
"
:
"
1
"
        
"
weeks
"
:
"
{
0
}
"
        
"
month
"
:
"
1
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
1
"
        
"
years
"
:
"
{
0
}
"
    
}
    
month_names
=
[
        
"
"
        
"
1
"
        
"
2
"
        
"
3
"
        
"
4
"
        
"
5
"
        
"
6
"
        
"
7
"
        
"
8
"
        
"
9
"
        
"
10
"
        
"
11
"
        
"
12
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
1
"
        
"
2
"
        
"
3
"
        
"
4
"
        
"
5
"
        
"
6
"
        
"
7
"
        
"
8
"
        
"
9
"
        
"
10
"
        
"
11
"
        
"
12
"
    
]
    
day_names
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
    
day_abbreviations
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
class
SwedishLocale
(
Locale
)
:
    
names
=
[
"
sv
"
"
sv
-
se
"
]
    
past
=
"
f
r
{
0
}
sen
"
    
future
=
"
om
{
0
}
"
    
and_word
=
"
och
"
    
timeframes
=
{
        
"
now
"
:
"
just
nu
"
        
"
second
"
:
"
en
sekund
"
        
"
seconds
"
:
"
{
0
}
sekunder
"
        
"
minute
"
:
"
en
minut
"
        
"
minutes
"
:
"
{
0
}
minuter
"
        
"
hour
"
:
"
en
timme
"
        
"
hours
"
:
"
{
0
}
timmar
"
        
"
day
"
:
"
en
dag
"
        
"
days
"
:
"
{
0
}
dagar
"
        
"
week
"
:
"
en
vecka
"
        
"
weeks
"
:
"
{
0
}
veckor
"
        
"
month
"
:
"
en
m
nad
"
        
"
months
"
:
"
{
0
}
m
nader
"
        
"
year
"
:
"
ett
r
"
        
"
years
"
:
"
{
0
}
r
"
    
}
    
month_names
=
[
        
"
"
        
"
januari
"
        
"
februari
"
        
"
mars
"
        
"
april
"
        
"
maj
"
        
"
juni
"
        
"
juli
"
        
"
augusti
"
        
"
september
"
        
"
oktober
"
        
"
november
"
        
"
december
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
jan
"
        
"
feb
"
        
"
mar
"
        
"
apr
"
        
"
maj
"
        
"
jun
"
        
"
jul
"
        
"
aug
"
        
"
sep
"
        
"
okt
"
        
"
nov
"
        
"
dec
"
    
]
    
day_names
=
[
        
"
"
        
"
m
ndag
"
        
"
tisdag
"
        
"
onsdag
"
        
"
torsdag
"
        
"
fredag
"
        
"
l
rdag
"
        
"
s
ndag
"
    
]
    
day_abbreviations
=
[
"
"
"
m
n
"
"
tis
"
"
ons
"
"
tor
"
"
fre
"
"
l
r
"
"
s
n
"
]
class
FinnishLocale
(
Locale
)
:
    
names
=
[
"
fi
"
"
fi
-
fi
"
]
    
past
=
"
{
0
}
sitten
"
    
future
=
"
{
0
}
kuluttua
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
juuri
nyt
"
        
"
second
"
:
{
"
past
"
:
"
sekunti
"
"
future
"
:
"
sekunnin
"
}
        
"
seconds
"
:
{
"
past
"
:
"
{
0
}
sekuntia
"
"
future
"
:
"
{
0
}
sekunnin
"
}
        
"
minute
"
:
{
"
past
"
:
"
minuutti
"
"
future
"
:
"
minuutin
"
}
        
"
minutes
"
:
{
"
past
"
:
"
{
0
}
minuuttia
"
"
future
"
:
"
{
0
}
minuutin
"
}
        
"
hour
"
:
{
"
past
"
:
"
tunti
"
"
future
"
:
"
tunnin
"
}
        
"
hours
"
:
{
"
past
"
:
"
{
0
}
tuntia
"
"
future
"
:
"
{
0
}
tunnin
"
}
        
"
day
"
:
{
"
past
"
:
"
p
iv
"
"
future
"
:
"
p
iv
n
"
}
        
"
days
"
:
{
"
past
"
:
"
{
0
}
p
iv
"
"
future
"
:
"
{
0
}
p
iv
n
"
}
        
"
week
"
:
{
"
past
"
:
"
viikko
"
"
future
"
:
"
viikon
"
}
        
"
weeks
"
:
{
"
past
"
:
"
{
0
}
viikkoa
"
"
future
"
:
"
{
0
}
viikon
"
}
        
"
month
"
:
{
"
past
"
:
"
kuukausi
"
"
future
"
:
"
kuukauden
"
}
        
"
months
"
:
{
"
past
"
:
"
{
0
}
kuukautta
"
"
future
"
:
"
{
0
}
kuukauden
"
}
        
"
year
"
:
{
"
past
"
:
"
vuosi
"
"
future
"
:
"
vuoden
"
}
        
"
years
"
:
{
"
past
"
:
"
{
0
}
vuotta
"
"
future
"
:
"
{
0
}
vuoden
"
}
    
}
    
month_names
=
[
        
"
"
        
"
tammikuu
"
        
"
helmikuu
"
        
"
maaliskuu
"
        
"
huhtikuu
"
        
"
toukokuu
"
        
"
kes
kuu
"
        
"
hein
kuu
"
        
"
elokuu
"
        
"
syyskuu
"
        
"
lokakuu
"
        
"
marraskuu
"
        
"
joulukuu
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
tammi
"
        
"
helmi
"
        
"
maalis
"
        
"
huhti
"
        
"
touko
"
        
"
kes
"
        
"
hein
"
        
"
elo
"
        
"
syys
"
        
"
loka
"
        
"
marras
"
        
"
joulu
"
    
]
    
day_names
=
[
        
"
"
        
"
maanantai
"
        
"
tiistai
"
        
"
keskiviikko
"
        
"
torstai
"
        
"
perjantai
"
        
"
lauantai
"
        
"
sunnuntai
"
    
]
    
day_abbreviations
=
[
"
"
"
ma
"
"
ti
"
"
ke
"
"
to
"
"
pe
"
"
la
"
"
su
"
]
    
def
_format_timeframe
(
self
timeframe
:
TimeFrameLiteral
delta
:
int
)
-
>
str
:
        
form
=
self
.
timeframes
[
timeframe
]
        
if
isinstance
(
form
Mapping
)
:
            
if
delta
<
0
:
                
form
=
form
[
"
past
"
]
            
else
:
                
form
=
form
[
"
future
"
]
        
return
form
.
format
(
abs
(
delta
)
)
    
def
_ordinal_number
(
self
n
:
int
)
-
>
str
:
        
return
f
"
{
n
}
.
"
class
ChineseCNLocale
(
Locale
)
:
    
names
=
[
"
zh
"
"
zh
-
cn
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
1
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
1
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
1
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
1
"
        
"
days
"
:
"
{
0
}
"
        
"
week
"
:
"
1
"
        
"
weeks
"
:
"
{
0
}
"
        
"
month
"
:
"
1
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
1
"
        
"
years
"
:
"
{
0
}
"
    
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
1
"
        
"
2
"
        
"
3
"
        
"
4
"
        
"
5
"
        
"
6
"
        
"
7
"
        
"
8
"
        
"
9
"
        
"
10
"
        
"
11
"
        
"
12
"
    
]
    
day_names
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
    
day_abbreviations
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
class
ChineseTWLocale
(
Locale
)
:
    
names
=
[
"
zh
-
tw
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
and_word
=
"
"
    
timeframes
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
1
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
1
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
1
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
1
"
        
"
days
"
:
"
{
0
}
"
        
"
week
"
:
"
1
"
        
"
weeks
"
:
"
{
0
}
"
        
"
month
"
:
"
1
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
1
"
        
"
years
"
:
"
{
0
}
"
    
}
    
month_names
=
[
        
"
"
        
"
1
"
        
"
2
"
        
"
3
"
        
"
4
"
        
"
5
"
        
"
6
"
        
"
7
"
        
"
8
"
        
"
9
"
        
"
10
"
        
"
11
"
        
"
12
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
1
"
        
"
2
"
        
"
3
"
        
"
4
"
        
"
5
"
        
"
6
"
        
"
7
"
        
"
8
"
        
"
9
"
        
"
10
"
        
"
11
"
        
"
12
"
    
]
    
day_names
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
    
day_abbreviations
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
class
HongKongLocale
(
Locale
)
:
    
names
=
[
"
zh
-
hk
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
1
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
1
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
1
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
1
"
        
"
days
"
:
"
{
0
}
"
        
"
week
"
:
"
1
"
        
"
weeks
"
:
"
{
0
}
"
        
"
month
"
:
"
1
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
1
"
        
"
years
"
:
"
{
0
}
"
    
}
    
month_names
=
[
        
"
"
        
"
1
"
        
"
2
"
        
"
3
"
        
"
4
"
        
"
5
"
        
"
6
"
        
"
7
"
        
"
8
"
        
"
9
"
        
"
10
"
        
"
11
"
        
"
12
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
1
"
        
"
2
"
        
"
3
"
        
"
4
"
        
"
5
"
        
"
6
"
        
"
7
"
        
"
8
"
        
"
9
"
        
"
10
"
        
"
11
"
        
"
12
"
    
]
    
day_names
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
    
day_abbreviations
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
class
KoreanLocale
(
Locale
)
:
    
names
=
[
"
ko
"
"
ko
-
kr
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
1
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
1
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
"
        
"
days
"
:
"
{
0
}
"
        
"
week
"
:
"
1
"
        
"
weeks
"
:
"
{
0
}
"
        
"
month
"
:
"
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
1
"
        
"
years
"
:
"
{
0
}
"
    
}
    
special_dayframes
=
{
        
-
3
:
"
"
        
-
2
:
"
"
        
-
1
:
"
"
        
1
:
"
"
        
2
:
"
"
        
3
:
"
"
        
4
:
"
"
    
}
    
special_yearframes
=
{
-
2
:
"
"
-
1
:
"
"
1
:
"
"
2
:
"
"
}
    
month_names
=
[
        
"
"
        
"
1
"
        
"
2
"
        
"
3
"
        
"
4
"
        
"
5
"
        
"
6
"
        
"
7
"
        
"
8
"
        
"
9
"
        
"
10
"
        
"
11
"
        
"
12
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
1
"
        
"
2
"
        
"
3
"
        
"
4
"
        
"
5
"
        
"
6
"
        
"
7
"
        
"
8
"
        
"
9
"
        
"
10
"
        
"
11
"
        
"
12
"
    
]
    
day_names
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
    
day_abbreviations
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
    
def
_ordinal_number
(
self
n
:
int
)
-
>
str
:
        
ordinals
=
[
"
0
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
        
if
n
<
len
(
ordinals
)
:
            
return
f
"
{
ordinals
[
n
]
}
"
        
return
f
"
{
n
}
"
    
def
_format_relative
(
        
self
        
humanized
:
str
        
timeframe
:
TimeFrameLiteral
        
delta
:
Union
[
float
int
]
    
)
-
>
str
:
        
if
timeframe
in
(
"
day
"
"
days
"
)
:
            
special
=
self
.
special_dayframes
.
get
(
int
(
delta
)
)
            
if
special
:
                
return
special
        
elif
timeframe
in
(
"
year
"
"
years
"
)
:
            
special
=
self
.
special_yearframes
.
get
(
int
(
delta
)
)
            
if
special
:
                
return
special
        
return
super
(
)
.
_format_relative
(
humanized
timeframe
delta
)
class
DutchLocale
(
Locale
)
:
    
names
=
[
"
nl
"
"
nl
-
nl
"
]
    
past
=
"
{
0
}
geleden
"
    
future
=
"
over
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
nu
"
        
"
second
"
:
"
een
seconde
"
        
"
seconds
"
:
"
{
0
}
seconden
"
        
"
minute
"
:
"
een
minuut
"
        
"
minutes
"
:
"
{
0
}
minuten
"
        
"
hour
"
:
"
een
uur
"
        
"
hours
"
:
"
{
0
}
uur
"
        
"
day
"
:
"
een
dag
"
        
"
days
"
:
"
{
0
}
dagen
"
        
"
week
"
:
"
een
week
"
        
"
weeks
"
:
"
{
0
}
weken
"
        
"
month
"
:
"
een
maand
"
        
"
months
"
:
"
{
0
}
maanden
"
        
"
year
"
:
"
een
jaar
"
        
"
years
"
:
"
{
0
}
jaar
"
    
}
    
month_names
=
[
        
"
"
        
"
januari
"
        
"
februari
"
        
"
maart
"
        
"
april
"
        
"
mei
"
        
"
juni
"
        
"
juli
"
        
"
augustus
"
        
"
september
"
        
"
oktober
"
        
"
november
"
        
"
december
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
jan
"
        
"
feb
"
        
"
mrt
"
        
"
apr
"
        
"
mei
"
        
"
jun
"
        
"
jul
"
        
"
aug
"
        
"
sep
"
        
"
okt
"
        
"
nov
"
        
"
dec
"
    
]
    
day_names
=
[
        
"
"
        
"
maandag
"
        
"
dinsdag
"
        
"
woensdag
"
        
"
donderdag
"
        
"
vrijdag
"
        
"
zaterdag
"
        
"
zondag
"
    
]
    
day_abbreviations
=
[
"
"
"
ma
"
"
di
"
"
wo
"
"
do
"
"
vr
"
"
za
"
"
zo
"
]
class
SlavicBaseLocale
(
Locale
)
:
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
    
def
_format_timeframe
(
self
timeframe
:
TimeFrameLiteral
delta
:
int
)
-
>
str
:
        
form
=
self
.
timeframes
[
timeframe
]
        
delta
=
abs
(
delta
)
        
if
isinstance
(
form
Mapping
)
:
            
if
delta
%
10
=
=
1
and
delta
%
100
!
=
11
:
                
form
=
form
[
"
singular
"
]
            
elif
2
<
=
delta
%
10
<
=
4
and
(
delta
%
100
<
10
or
delta
%
100
>
=
20
)
:
                
form
=
form
[
"
dual
"
]
            
else
:
                
form
=
form
[
"
plural
"
]
        
return
form
.
format
(
delta
)
class
BelarusianLocale
(
SlavicBaseLocale
)
:
    
names
=
[
"
be
"
"
be
-
by
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
"
        
"
minutes
"
:
{
            
"
singular
"
:
"
{
0
}
"
            
"
dual
"
:
"
{
0
}
"
            
"
plural
"
:
"
{
0
}
"
        
}
        
"
hour
"
:
"
"
        
"
hours
"
:
{
            
"
singular
"
:
"
{
0
}
"
            
"
dual
"
:
"
{
0
}
"
            
"
plural
"
:
"
{
0
}
"
        
}
        
"
day
"
:
"
"
        
"
days
"
:
{
"
singular
"
:
"
{
0
}
"
"
dual
"
:
"
{
0
}
"
"
plural
"
:
"
{
0
}
"
}
        
"
month
"
:
"
"
        
"
months
"
:
{
            
"
singular
"
:
"
{
0
}
"
            
"
dual
"
:
"
{
0
}
"
            
"
plural
"
:
"
{
0
}
"
        
}
        
"
year
"
:
"
"
        
"
years
"
:
{
"
singular
"
:
"
{
0
}
"
"
dual
"
:
"
{
0
}
"
"
plural
"
:
"
{
0
}
"
}
    
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
class
PolishLocale
(
SlavicBaseLocale
)
:
    
names
=
[
"
pl
"
"
pl
-
pl
"
]
    
past
=
"
{
0
}
temu
"
    
future
=
"
za
{
0
}
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
teraz
"
        
"
second
"
:
"
sekund
"
        
"
seconds
"
:
{
            
"
singular
"
:
"
{
0
}
sekund
"
            
"
dual
"
:
"
{
0
}
sekundy
"
            
"
plural
"
:
"
{
0
}
sekund
"
        
}
        
"
minute
"
:
"
minut
"
        
"
minutes
"
:
{
            
"
singular
"
:
"
{
0
}
minut
"
            
"
dual
"
:
"
{
0
}
minuty
"
            
"
plural
"
:
"
{
0
}
minut
"
        
}
        
"
hour
"
:
"
godzin
"
        
"
hours
"
:
{
            
"
singular
"
:
"
{
0
}
godzin
"
            
"
dual
"
:
"
{
0
}
godziny
"
            
"
plural
"
:
"
{
0
}
godzin
"
        
}
        
"
day
"
:
"
dzie
"
        
"
days
"
:
"
{
0
}
dni
"
        
"
week
"
:
"
tydzie
"
        
"
weeks
"
:
{
            
"
singular
"
:
"
{
0
}
tygodni
"
            
"
dual
"
:
"
{
0
}
tygodnie
"
            
"
plural
"
:
"
{
0
}
tygodni
"
        
}
        
"
month
"
:
"
miesi
c
"
        
"
months
"
:
{
            
"
singular
"
:
"
{
0
}
miesi
cy
"
            
"
dual
"
:
"
{
0
}
miesi
ce
"
            
"
plural
"
:
"
{
0
}
miesi
cy
"
        
}
        
"
year
"
:
"
rok
"
        
"
years
"
:
{
"
singular
"
:
"
{
0
}
lat
"
"
dual
"
:
"
{
0
}
lata
"
"
plural
"
:
"
{
0
}
lat
"
}
    
}
    
month_names
=
[
        
"
"
        
"
stycze
"
        
"
luty
"
        
"
marzec
"
        
"
kwiecie
"
        
"
maj
"
        
"
czerwiec
"
        
"
lipiec
"
        
"
sierpie
"
        
"
wrzesie
"
        
"
pa
dziernik
"
        
"
listopad
"
        
"
grudzie
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
sty
"
        
"
lut
"
        
"
mar
"
        
"
kwi
"
        
"
maj
"
        
"
cze
"
        
"
lip
"
        
"
sie
"
        
"
wrz
"
        
"
pa
"
        
"
lis
"
        
"
gru
"
    
]
    
day_names
=
[
        
"
"
        
"
poniedzia
ek
"
        
"
wtorek
"
        
"
roda
"
        
"
czwartek
"
        
"
pi
tek
"
        
"
sobota
"
        
"
niedziela
"
    
]
    
day_abbreviations
=
[
"
"
"
Pn
"
"
Wt
"
"
r
"
"
Czw
"
"
Pt
"
"
So
"
"
Nd
"
]
class
RussianLocale
(
SlavicBaseLocale
)
:
    
names
=
[
"
ru
"
"
ru
-
ru
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
{
            
"
singular
"
:
"
{
0
}
"
            
"
dual
"
:
"
{
0
}
"
            
"
plural
"
:
"
{
0
}
"
        
}
        
"
minute
"
:
"
"
        
"
minutes
"
:
{
            
"
singular
"
:
"
{
0
}
"
            
"
dual
"
:
"
{
0
}
"
            
"
plural
"
:
"
{
0
}
"
        
}
        
"
hour
"
:
"
"
        
"
hours
"
:
{
"
singular
"
:
"
{
0
}
"
"
dual
"
:
"
{
0
}
"
"
plural
"
:
"
{
0
}
"
}
        
"
day
"
:
"
"
        
"
days
"
:
{
"
singular
"
:
"
{
0
}
"
"
dual
"
:
"
{
0
}
"
"
plural
"
:
"
{
0
}
"
}
        
"
week
"
:
"
"
        
"
weeks
"
:
{
            
"
singular
"
:
"
{
0
}
"
            
"
dual
"
:
"
{
0
}
"
            
"
plural
"
:
"
{
0
}
"
        
}
        
"
month
"
:
"
"
        
"
months
"
:
{
            
"
singular
"
:
"
{
0
}
"
            
"
dual
"
:
"
{
0
}
"
            
"
plural
"
:
"
{
0
}
"
        
}
        
"
quarter
"
:
"
"
        
"
quarters
"
:
{
            
"
singular
"
:
"
{
0
}
"
            
"
dual
"
:
"
{
0
}
"
            
"
plural
"
:
"
{
0
}
"
        
}
        
"
year
"
:
"
"
        
"
years
"
:
{
"
singular
"
:
"
{
0
}
"
"
dual
"
:
"
{
0
}
"
"
plural
"
:
"
{
0
}
"
}
    
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
class
AfrikaansLocale
(
Locale
)
:
    
names
=
[
"
af
"
"
af
-
nl
"
]
    
past
=
"
{
0
}
gelede
"
    
future
=
"
in
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
nou
"
        
"
second
"
:
"
n
sekonde
"
        
"
seconds
"
:
"
{
0
}
sekondes
"
        
"
minute
"
:
"
minuut
"
        
"
minutes
"
:
"
{
0
}
minute
"
        
"
hour
"
:
"
uur
"
        
"
hours
"
:
"
{
0
}
ure
"
        
"
day
"
:
"
een
dag
"
        
"
days
"
:
"
{
0
}
dae
"
        
"
month
"
:
"
een
maand
"
        
"
months
"
:
"
{
0
}
maande
"
        
"
year
"
:
"
een
jaar
"
        
"
years
"
:
"
{
0
}
jaar
"
    
}
    
month_names
=
[
        
"
"
        
"
Januarie
"
        
"
Februarie
"
        
"
Maart
"
        
"
April
"
        
"
Mei
"
        
"
Junie
"
        
"
Julie
"
        
"
Augustus
"
        
"
September
"
        
"
Oktober
"
        
"
November
"
        
"
Desember
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
Jan
"
        
"
Feb
"
        
"
Mrt
"
        
"
Apr
"
        
"
Mei
"
        
"
Jun
"
        
"
Jul
"
        
"
Aug
"
        
"
Sep
"
        
"
Okt
"
        
"
Nov
"
        
"
Des
"
    
]
    
day_names
=
[
        
"
"
        
"
Maandag
"
        
"
Dinsdag
"
        
"
Woensdag
"
        
"
Donderdag
"
        
"
Vrydag
"
        
"
Saterdag
"
        
"
Sondag
"
    
]
    
day_abbreviations
=
[
"
"
"
Ma
"
"
Di
"
"
Wo
"
"
Do
"
"
Vr
"
"
Za
"
"
So
"
]
class
BulgarianLocale
(
SlavicBaseLocale
)
:
    
names
=
[
"
bg
"
"
bg
-
bg
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
"
        
"
minutes
"
:
{
            
"
singular
"
:
"
{
0
}
"
            
"
dual
"
:
"
{
0
}
"
            
"
plural
"
:
"
{
0
}
"
        
}
        
"
hour
"
:
"
"
        
"
hours
"
:
{
"
singular
"
:
"
{
0
}
"
"
dual
"
:
"
{
0
}
"
"
plural
"
:
"
{
0
}
"
}
        
"
day
"
:
"
"
        
"
days
"
:
{
"
singular
"
:
"
{
0
}
"
"
dual
"
:
"
{
0
}
"
"
plural
"
:
"
{
0
}
"
}
        
"
month
"
:
"
"
        
"
months
"
:
{
            
"
singular
"
:
"
{
0
}
"
            
"
dual
"
:
"
{
0
}
"
            
"
plural
"
:
"
{
0
}
"
        
}
        
"
year
"
:
"
"
        
"
years
"
:
{
            
"
singular
"
:
"
{
0
}
"
            
"
dual
"
:
"
{
0
}
"
            
"
plural
"
:
"
{
0
}
"
        
}
    
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
class
UkrainianLocale
(
SlavicBaseLocale
)
:
    
names
=
[
"
ua
"
"
uk
"
"
uk
-
ua
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
"
        
"
minutes
"
:
{
            
"
singular
"
:
"
{
0
}
"
            
"
dual
"
:
"
{
0
}
"
            
"
plural
"
:
"
{
0
}
"
        
}
        
"
hour
"
:
"
"
        
"
hours
"
:
{
            
"
singular
"
:
"
{
0
}
"
            
"
dual
"
:
"
{
0
}
"
            
"
plural
"
:
"
{
0
}
"
        
}
        
"
day
"
:
"
"
        
"
days
"
:
{
"
singular
"
:
"
{
0
}
"
"
dual
"
:
"
{
0
}
"
"
plural
"
:
"
{
0
}
"
}
        
"
month
"
:
"
"
        
"
months
"
:
{
            
"
singular
"
:
"
{
0
}
"
            
"
dual
"
:
"
{
0
}
"
            
"
plural
"
:
"
{
0
}
"
        
}
        
"
year
"
:
"
"
        
"
years
"
:
{
"
singular
"
:
"
{
0
}
"
"
dual
"
:
"
{
0
}
"
"
plural
"
:
"
{
0
}
"
}
    
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
class
MacedonianLocale
(
SlavicBaseLocale
)
:
    
names
=
[
"
mk
"
"
mk
-
mk
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
{
            
"
singular
"
:
"
{
0
}
"
            
"
dual
"
:
"
{
0
}
"
            
"
plural
"
:
"
{
0
}
"
        
}
        
"
minute
"
:
"
"
        
"
minutes
"
:
{
            
"
singular
"
:
"
{
0
}
"
            
"
dual
"
:
"
{
0
}
"
            
"
plural
"
:
"
{
0
}
"
        
}
        
"
hour
"
:
"
"
        
"
hours
"
:
{
"
singular
"
:
"
{
0
}
"
"
dual
"
:
"
{
0
}
"
"
plural
"
:
"
{
0
}
"
}
        
"
day
"
:
"
"
        
"
days
"
:
{
"
singular
"
:
"
{
0
}
"
"
dual
"
:
"
{
0
}
"
"
plural
"
:
"
{
0
}
"
}
        
"
week
"
:
"
"
        
"
weeks
"
:
{
            
"
singular
"
:
"
{
0
}
"
            
"
dual
"
:
"
{
0
}
"
            
"
plural
"
:
"
{
0
}
"
        
}
        
"
month
"
:
"
"
        
"
months
"
:
{
            
"
singular
"
:
"
{
0
}
"
            
"
dual
"
:
"
{
0
}
"
            
"
plural
"
:
"
{
0
}
"
        
}
        
"
year
"
:
"
"
        
"
years
"
:
{
            
"
singular
"
:
"
{
0
}
"
            
"
dual
"
:
"
{
0
}
"
            
"
plural
"
:
"
{
0
}
"
        
}
    
}
    
meridians
=
{
"
am
"
:
"
"
"
pm
"
:
"
"
"
AM
"
:
"
"
"
PM
"
:
"
"
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
class
GermanBaseLocale
(
Locale
)
:
    
past
=
"
vor
{
0
}
"
    
future
=
"
in
{
0
}
"
    
and_word
=
"
und
"
    
timeframes
:
ClassVar
[
Dict
[
TimeFrameLiteral
str
]
]
=
{
        
"
now
"
:
"
gerade
eben
"
        
"
second
"
:
"
einer
Sekunde
"
        
"
seconds
"
:
"
{
0
}
Sekunden
"
        
"
minute
"
:
"
einer
Minute
"
        
"
minutes
"
:
"
{
0
}
Minuten
"
        
"
hour
"
:
"
einer
Stunde
"
        
"
hours
"
:
"
{
0
}
Stunden
"
        
"
day
"
:
"
einem
Tag
"
        
"
days
"
:
"
{
0
}
Tagen
"
        
"
week
"
:
"
einer
Woche
"
        
"
weeks
"
:
"
{
0
}
Wochen
"
        
"
month
"
:
"
einem
Monat
"
        
"
months
"
:
"
{
0
}
Monaten
"
        
"
year
"
:
"
einem
Jahr
"
        
"
years
"
:
"
{
0
}
Jahren
"
    
}
    
timeframes_only_distance
=
timeframes
.
copy
(
)
    
timeframes_only_distance
[
"
second
"
]
=
"
eine
Sekunde
"
    
timeframes_only_distance
[
"
minute
"
]
=
"
eine
Minute
"
    
timeframes_only_distance
[
"
hour
"
]
=
"
eine
Stunde
"
    
timeframes_only_distance
[
"
day
"
]
=
"
ein
Tag
"
    
timeframes_only_distance
[
"
days
"
]
=
"
{
0
}
Tage
"
    
timeframes_only_distance
[
"
week
"
]
=
"
eine
Woche
"
    
timeframes_only_distance
[
"
month
"
]
=
"
ein
Monat
"
    
timeframes_only_distance
[
"
months
"
]
=
"
{
0
}
Monate
"
    
timeframes_only_distance
[
"
year
"
]
=
"
ein
Jahr
"
    
timeframes_only_distance
[
"
years
"
]
=
"
{
0
}
Jahre
"
    
month_names
=
[
        
"
"
        
"
Januar
"
        
"
Februar
"
        
"
M
rz
"
        
"
April
"
        
"
Mai
"
        
"
Juni
"
        
"
Juli
"
        
"
August
"
        
"
September
"
        
"
Oktober
"
        
"
November
"
        
"
Dezember
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
Jan
"
        
"
Feb
"
        
"
M
r
"
        
"
Apr
"
        
"
Mai
"
        
"
Jun
"
        
"
Jul
"
        
"
Aug
"
        
"
Sep
"
        
"
Okt
"
        
"
Nov
"
        
"
Dez
"
    
]
    
day_names
=
[
        
"
"
        
"
Montag
"
        
"
Dienstag
"
        
"
Mittwoch
"
        
"
Donnerstag
"
        
"
Freitag
"
        
"
Samstag
"
        
"
Sonntag
"
    
]
    
day_abbreviations
=
[
"
"
"
Mo
"
"
Di
"
"
Mi
"
"
Do
"
"
Fr
"
"
Sa
"
"
So
"
]
    
def
_ordinal_number
(
self
n
:
int
)
-
>
str
:
        
return
f
"
{
n
}
.
"
    
def
describe
(
        
self
        
timeframe
:
TimeFrameLiteral
        
delta
:
Union
[
int
float
]
=
0
        
only_distance
:
bool
=
False
    
)
-
>
str
:
        
"
"
"
Describes
a
delta
within
a
timeframe
in
plain
language
.
        
:
param
timeframe
:
a
string
representing
a
timeframe
.
        
:
param
delta
:
a
quantity
representing
a
delta
in
a
timeframe
.
        
:
param
only_distance
:
return
only
distance
eg
:
"
11
seconds
"
without
"
in
"
or
"
ago
"
keywords
        
"
"
"
        
if
not
only_distance
:
            
return
super
(
)
.
describe
(
timeframe
delta
only_distance
)
        
humanized
:
str
=
self
.
timeframes_only_distance
[
timeframe
]
.
format
(
            
trunc
(
abs
(
delta
)
)
        
)
        
return
humanized
class
GermanLocale
(
GermanBaseLocale
Locale
)
:
    
names
=
[
"
de
"
"
de
-
de
"
]
class
SwissLocale
(
GermanBaseLocale
Locale
)
:
    
names
=
[
"
de
-
ch
"
]
class
AustrianLocale
(
GermanBaseLocale
Locale
)
:
    
names
=
[
"
de
-
at
"
]
    
month_names
=
[
        
"
"
        
"
J
nner
"
        
"
Februar
"
        
"
M
rz
"
        
"
April
"
        
"
Mai
"
        
"
Juni
"
        
"
Juli
"
        
"
August
"
        
"
September
"
        
"
Oktober
"
        
"
November
"
        
"
Dezember
"
    
]
class
NorwegianLocale
(
Locale
)
:
    
names
=
[
"
nb
"
"
nb
-
no
"
]
    
past
=
"
for
{
0
}
siden
"
    
future
=
"
om
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
n
nettopp
"
        
"
second
"
:
"
ett
sekund
"
        
"
seconds
"
:
"
{
0
}
sekunder
"
        
"
minute
"
:
"
ett
minutt
"
        
"
minutes
"
:
"
{
0
}
minutter
"
        
"
hour
"
:
"
en
time
"
        
"
hours
"
:
"
{
0
}
timer
"
        
"
day
"
:
"
en
dag
"
        
"
days
"
:
"
{
0
}
dager
"
        
"
week
"
:
"
en
uke
"
        
"
weeks
"
:
"
{
0
}
uker
"
        
"
month
"
:
"
en
m
ned
"
        
"
months
"
:
"
{
0
}
m
neder
"
        
"
year
"
:
"
ett
r
"
        
"
years
"
:
"
{
0
}
r
"
    
}
    
month_names
=
[
        
"
"
        
"
januar
"
        
"
februar
"
        
"
mars
"
        
"
april
"
        
"
mai
"
        
"
juni
"
        
"
juli
"
        
"
august
"
        
"
september
"
        
"
oktober
"
        
"
november
"
        
"
desember
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
jan
"
        
"
feb
"
        
"
mar
"
        
"
apr
"
        
"
mai
"
        
"
jun
"
        
"
jul
"
        
"
aug
"
        
"
sep
"
        
"
okt
"
        
"
nov
"
        
"
des
"
    
]
    
day_names
=
[
        
"
"
        
"
mandag
"
        
"
tirsdag
"
        
"
onsdag
"
        
"
torsdag
"
        
"
fredag
"
        
"
l
rdag
"
        
"
s
ndag
"
    
]
    
day_abbreviations
=
[
"
"
"
ma
"
"
ti
"
"
on
"
"
to
"
"
fr
"
"
l
"
"
s
"
]
    
def
_ordinal_number
(
self
n
:
int
)
-
>
str
:
        
return
f
"
{
n
}
.
"
class
NewNorwegianLocale
(
Locale
)
:
    
names
=
[
"
nn
"
"
nn
-
no
"
]
    
past
=
"
for
{
0
}
sidan
"
    
future
=
"
om
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
no
nettopp
"
        
"
second
"
:
"
eitt
sekund
"
        
"
seconds
"
:
"
{
0
}
sekund
"
        
"
minute
"
:
"
eitt
minutt
"
        
"
minutes
"
:
"
{
0
}
minutt
"
        
"
hour
"
:
"
ein
time
"
        
"
hours
"
:
"
{
0
}
timar
"
        
"
day
"
:
"
ein
dag
"
        
"
days
"
:
"
{
0
}
dagar
"
        
"
week
"
:
"
ei
veke
"
        
"
weeks
"
:
"
{
0
}
veker
"
        
"
month
"
:
"
ein
m
nad
"
        
"
months
"
:
"
{
0
}
m
nader
"
        
"
year
"
:
"
eitt
r
"
        
"
years
"
:
"
{
0
}
r
"
    
}
    
month_names
=
[
        
"
"
        
"
januar
"
        
"
februar
"
        
"
mars
"
        
"
april
"
        
"
mai
"
        
"
juni
"
        
"
juli
"
        
"
august
"
        
"
september
"
        
"
oktober
"
        
"
november
"
        
"
desember
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
jan
"
        
"
feb
"
        
"
mar
"
        
"
apr
"
        
"
mai
"
        
"
jun
"
        
"
jul
"
        
"
aug
"
        
"
sep
"
        
"
okt
"
        
"
nov
"
        
"
des
"
    
]
    
day_names
=
[
        
"
"
        
"
m
ndag
"
        
"
tysdag
"
        
"
onsdag
"
        
"
torsdag
"
        
"
fredag
"
        
"
laurdag
"
        
"
sundag
"
    
]
    
day_abbreviations
=
[
"
"
"
m
"
"
ty
"
"
on
"
"
to
"
"
fr
"
"
la
"
"
su
"
]
    
def
_ordinal_number
(
self
n
:
int
)
-
>
str
:
        
return
f
"
{
n
}
.
"
class
PortugueseLocale
(
Locale
)
:
    
names
=
[
"
pt
"
"
pt
-
pt
"
]
    
past
=
"
h
{
0
}
"
    
future
=
"
em
{
0
}
"
    
and_word
=
"
e
"
    
timeframes
=
{
        
"
now
"
:
"
agora
"
        
"
second
"
:
"
um
segundo
"
        
"
seconds
"
:
"
{
0
}
segundos
"
        
"
minute
"
:
"
um
minuto
"
        
"
minutes
"
:
"
{
0
}
minutos
"
        
"
hour
"
:
"
uma
hora
"
        
"
hours
"
:
"
{
0
}
horas
"
        
"
day
"
:
"
um
dia
"
        
"
days
"
:
"
{
0
}
dias
"
        
"
week
"
:
"
uma
semana
"
        
"
weeks
"
:
"
{
0
}
semanas
"
        
"
month
"
:
"
um
m
s
"
        
"
months
"
:
"
{
0
}
meses
"
        
"
year
"
:
"
um
ano
"
        
"
years
"
:
"
{
0
}
anos
"
    
}
    
month_names
=
[
        
"
"
        
"
Janeiro
"
        
"
Fevereiro
"
        
"
Mar
o
"
        
"
Abril
"
        
"
Maio
"
        
"
Junho
"
        
"
Julho
"
        
"
Agosto
"
        
"
Setembro
"
        
"
Outubro
"
        
"
Novembro
"
        
"
Dezembro
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
Jan
"
        
"
Fev
"
        
"
Mar
"
        
"
Abr
"
        
"
Mai
"
        
"
Jun
"
        
"
Jul
"
        
"
Ago
"
        
"
Set
"
        
"
Out
"
        
"
Nov
"
        
"
Dez
"
    
]
    
day_names
=
[
        
"
"
        
"
Segunda
-
feira
"
        
"
Ter
a
-
feira
"
        
"
Quarta
-
feira
"
        
"
Quinta
-
feira
"
        
"
Sexta
-
feira
"
        
"
S
bado
"
        
"
Domingo
"
    
]
    
day_abbreviations
=
[
"
"
"
Seg
"
"
Ter
"
"
Qua
"
"
Qui
"
"
Sex
"
"
Sab
"
"
Dom
"
]
class
BrazilianPortugueseLocale
(
PortugueseLocale
)
:
    
names
=
[
"
pt
-
br
"
]
    
past
=
"
faz
{
0
}
"
class
TagalogLocale
(
Locale
)
:
    
names
=
[
"
tl
"
"
tl
-
ph
"
]
    
past
=
"
nakaraang
{
0
}
"
    
future
=
"
{
0
}
mula
ngayon
"
    
timeframes
=
{
        
"
now
"
:
"
ngayon
lang
"
        
"
second
"
:
"
isang
segundo
"
        
"
seconds
"
:
"
{
0
}
segundo
"
        
"
minute
"
:
"
isang
minuto
"
        
"
minutes
"
:
"
{
0
}
minuto
"
        
"
hour
"
:
"
isang
oras
"
        
"
hours
"
:
"
{
0
}
oras
"
        
"
day
"
:
"
isang
araw
"
        
"
days
"
:
"
{
0
}
araw
"
        
"
week
"
:
"
isang
linggo
"
        
"
weeks
"
:
"
{
0
}
linggo
"
        
"
month
"
:
"
isang
buwan
"
        
"
months
"
:
"
{
0
}
buwan
"
        
"
year
"
:
"
isang
taon
"
        
"
years
"
:
"
{
0
}
taon
"
    
}
    
month_names
=
[
        
"
"
        
"
Enero
"
        
"
Pebrero
"
        
"
Marso
"
        
"
Abril
"
        
"
Mayo
"
        
"
Hunyo
"
        
"
Hulyo
"
        
"
Agosto
"
        
"
Setyembre
"
        
"
Oktubre
"
        
"
Nobyembre
"
        
"
Disyembre
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
Ene
"
        
"
Peb
"
        
"
Mar
"
        
"
Abr
"
        
"
May
"
        
"
Hun
"
        
"
Hul
"
        
"
Ago
"
        
"
Set
"
        
"
Okt
"
        
"
Nob
"
        
"
Dis
"
    
]
    
day_names
=
[
        
"
"
        
"
Lunes
"
        
"
Martes
"
        
"
Miyerkules
"
        
"
Huwebes
"
        
"
Biyernes
"
        
"
Sabado
"
        
"
Linggo
"
    
]
    
day_abbreviations
=
[
"
"
"
Lun
"
"
Mar
"
"
Miy
"
"
Huw
"
"
Biy
"
"
Sab
"
"
Lin
"
]
    
meridians
=
{
"
am
"
:
"
nu
"
"
pm
"
:
"
nh
"
"
AM
"
:
"
ng
umaga
"
"
PM
"
:
"
ng
hapon
"
}
    
def
_ordinal_number
(
self
n
:
int
)
-
>
str
:
        
return
f
"
ika
-
{
n
}
"
class
VietnameseLocale
(
Locale
)
:
    
names
=
[
"
vi
"
"
vi
-
vn
"
]
    
past
=
"
{
0
}
tr
c
"
    
future
=
"
{
0
}
n
a
"
    
timeframes
=
{
        
"
now
"
:
"
hi
n
t
i
"
        
"
second
"
:
"
m
t
gi
y
"
        
"
seconds
"
:
"
{
0
}
gi
y
"
        
"
minute
"
:
"
m
t
ph
t
"
        
"
minutes
"
:
"
{
0
}
ph
t
"
        
"
hour
"
:
"
m
t
gi
"
        
"
hours
"
:
"
{
0
}
gi
"
        
"
day
"
:
"
m
t
ng
y
"
        
"
days
"
:
"
{
0
}
ng
y
"
        
"
week
"
:
"
m
t
tu
n
"
        
"
weeks
"
:
"
{
0
}
tu
n
"
        
"
month
"
:
"
m
t
th
ng
"
        
"
months
"
:
"
{
0
}
th
ng
"
        
"
year
"
:
"
m
t
n
m
"
        
"
years
"
:
"
{
0
}
n
m
"
    
}
    
month_names
=
[
        
"
"
        
"
Th
ng
M
t
"
        
"
Th
ng
Hai
"
        
"
Th
ng
Ba
"
        
"
Th
ng
T
"
        
"
Th
ng
N
m
"
        
"
Th
ng
S
u
"
        
"
Th
ng
B
y
"
        
"
Th
ng
T
m
"
        
"
Th
ng
Ch
n
"
        
"
Th
ng
M
i
"
        
"
Th
ng
M
i
M
t
"
        
"
Th
ng
M
i
Hai
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
Th
ng
1
"
        
"
Th
ng
2
"
        
"
Th
ng
3
"
        
"
Th
ng
4
"
        
"
Th
ng
5
"
        
"
Th
ng
6
"
        
"
Th
ng
7
"
        
"
Th
ng
8
"
        
"
Th
ng
9
"
        
"
Th
ng
10
"
        
"
Th
ng
11
"
        
"
Th
ng
12
"
    
]
    
day_names
=
[
        
"
"
        
"
Th
Hai
"
        
"
Th
Ba
"
        
"
Th
T
"
        
"
Th
N
m
"
        
"
Th
S
u
"
        
"
Th
B
y
"
        
"
Ch
Nh
t
"
    
]
    
day_abbreviations
=
[
"
"
"
Th
2
"
"
Th
3
"
"
Th
4
"
"
Th
5
"
"
Th
6
"
"
Th
7
"
"
CN
"
]
class
TurkishLocale
(
Locale
)
:
    
names
=
[
"
tr
"
"
tr
-
tr
"
]
    
past
=
"
{
0
}
nce
"
    
future
=
"
{
0
}
sonra
"
    
and_word
=
"
ve
"
    
timeframes
=
{
        
"
now
"
:
"
imdi
"
        
"
second
"
:
"
bir
saniye
"
        
"
seconds
"
:
"
{
0
}
saniye
"
        
"
minute
"
:
"
bir
dakika
"
        
"
minutes
"
:
"
{
0
}
dakika
"
        
"
hour
"
:
"
bir
saat
"
        
"
hours
"
:
"
{
0
}
saat
"
        
"
day
"
:
"
bir
g
n
"
        
"
days
"
:
"
{
0
}
g
n
"
        
"
week
"
:
"
bir
hafta
"
        
"
weeks
"
:
"
{
0
}
hafta
"
        
"
month
"
:
"
bir
ay
"
        
"
months
"
:
"
{
0
}
ay
"
        
"
year
"
:
"
bir
y
l
"
        
"
years
"
:
"
{
0
}
y
l
"
    
}
    
meridians
=
{
"
am
"
:
"
"
"
pm
"
:
"
s
"
"
AM
"
:
"
"
"
PM
"
:
"
S
"
}
    
month_names
=
[
        
"
"
        
"
Ocak
"
        
"
ubat
"
        
"
Mart
"
        
"
Nisan
"
        
"
May
s
"
        
"
Haziran
"
        
"
Temmuz
"
        
"
A
ustos
"
        
"
Eyl
l
"
        
"
Ekim
"
        
"
Kas
m
"
        
"
Aral
k
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
Oca
"
        
"
ub
"
        
"
Mar
"
        
"
Nis
"
        
"
May
"
        
"
Haz
"
        
"
Tem
"
        
"
A
u
"
        
"
Eyl
"
        
"
Eki
"
        
"
Kas
"
        
"
Ara
"
    
]
    
day_names
=
[
        
"
"
        
"
Pazartesi
"
        
"
Sal
"
        
"
ar
amba
"
        
"
Per
embe
"
        
"
Cuma
"
        
"
Cumartesi
"
        
"
Pazar
"
    
]
    
day_abbreviations
=
[
"
"
"
Pzt
"
"
Sal
"
"
ar
"
"
Per
"
"
Cum
"
"
Cmt
"
"
Paz
"
]
class
AzerbaijaniLocale
(
Locale
)
:
    
names
=
[
"
az
"
"
az
-
az
"
]
    
past
=
"
{
0
}
vv
l
"
    
future
=
"
{
0
}
sonra
"
    
timeframes
=
{
        
"
now
"
:
"
indi
"
        
"
second
"
:
"
bir
saniy
"
        
"
seconds
"
:
"
{
0
}
saniy
"
        
"
minute
"
:
"
bir
d
qiq
"
        
"
minutes
"
:
"
{
0
}
d
qiq
"
        
"
hour
"
:
"
bir
saat
"
        
"
hours
"
:
"
{
0
}
saat
"
        
"
day
"
:
"
bir
g
n
"
        
"
days
"
:
"
{
0
}
g
n
"
        
"
week
"
:
"
bir
h
ft
"
        
"
weeks
"
:
"
{
0
}
h
ft
"
        
"
month
"
:
"
bir
ay
"
        
"
months
"
:
"
{
0
}
ay
"
        
"
year
"
:
"
bir
il
"
        
"
years
"
:
"
{
0
}
il
"
    
}
    
month_names
=
[
        
"
"
        
"
Yanvar
"
        
"
Fevral
"
        
"
Mart
"
        
"
Aprel
"
        
"
May
"
        
"
yun
"
        
"
yul
"
        
"
Avqust
"
        
"
Sentyabr
"
        
"
Oktyabr
"
        
"
Noyabr
"
        
"
Dekabr
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
Yan
"
        
"
Fev
"
        
"
Mar
"
        
"
Apr
"
        
"
May
"
        
"
yn
"
        
"
yl
"
        
"
Avq
"
        
"
Sen
"
        
"
Okt
"
        
"
Noy
"
        
"
Dek
"
    
]
    
day_names
=
[
        
"
"
        
"
Bazar
ert
si
"
        
"
r
nb
ax
am
"
        
"
r
nb
"
        
"
C
m
ax
am
"
        
"
C
m
"
        
"
nb
"
        
"
Bazar
"
    
]
    
day_abbreviations
=
[
"
"
"
Ber
"
"
ax
"
"
r
"
"
Cax
"
"
C
m
"
"
nb
"
"
Bzr
"
]
class
ArabicLocale
(
Locale
)
:
    
names
=
[
        
"
ar
"
        
"
ar
-
ae
"
        
"
ar
-
bh
"
        
"
ar
-
dj
"
        
"
ar
-
eg
"
        
"
ar
-
eh
"
        
"
ar
-
er
"
        
"
ar
-
km
"
        
"
ar
-
kw
"
        
"
ar
-
ly
"
        
"
ar
-
om
"
        
"
ar
-
qa
"
        
"
ar
-
sa
"
        
"
ar
-
sd
"
        
"
ar
-
so
"
        
"
ar
-
ss
"
        
"
ar
-
td
"
        
"
ar
-
ye
"
    
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
{
"
2
"
:
"
"
"
ten
"
:
"
{
0
}
"
"
higher
"
:
"
{
0
}
"
}
        
"
minute
"
:
"
"
        
"
minutes
"
:
{
"
2
"
:
"
"
"
ten
"
:
"
{
0
}
"
"
higher
"
:
"
{
0
}
"
}
        
"
hour
"
:
"
"
        
"
hours
"
:
{
"
2
"
:
"
"
"
ten
"
:
"
{
0
}
"
"
higher
"
:
"
{
0
}
"
}
        
"
day
"
:
"
"
        
"
days
"
:
{
"
2
"
:
"
"
"
ten
"
:
"
{
0
}
"
"
higher
"
:
"
{
0
}
"
}
        
"
week
"
:
"
"
        
"
weeks
"
:
{
"
2
"
:
"
"
"
ten
"
:
"
{
0
}
"
"
higher
"
:
"
{
0
}
"
}
        
"
month
"
:
"
"
        
"
months
"
:
{
"
2
"
:
"
"
"
ten
"
:
"
{
0
}
"
"
higher
"
:
"
{
0
}
"
}
        
"
year
"
:
"
"
        
"
years
"
:
{
"
2
"
:
"
"
"
ten
"
:
"
{
0
}
"
"
higher
"
:
"
{
0
}
"
}
    
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
    
def
_format_timeframe
(
self
timeframe
:
TimeFrameLiteral
delta
:
int
)
-
>
str
:
        
form
=
self
.
timeframes
[
timeframe
]
        
delta
=
abs
(
delta
)
        
if
isinstance
(
form
Mapping
)
:
            
if
delta
=
=
2
:
                
form
=
form
[
"
2
"
]
            
elif
2
<
delta
<
=
10
:
                
form
=
form
[
"
ten
"
]
            
else
:
                
form
=
form
[
"
higher
"
]
        
return
form
.
format
(
delta
)
class
LevantArabicLocale
(
ArabicLocale
)
:
    
names
=
[
"
ar
-
iq
"
"
ar
-
jo
"
"
ar
-
lb
"
"
ar
-
ps
"
"
ar
-
sy
"
]
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
class
AlgeriaTunisiaArabicLocale
(
ArabicLocale
)
:
    
names
=
[
"
ar
-
tn
"
"
ar
-
dz
"
]
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
class
MauritaniaArabicLocale
(
ArabicLocale
)
:
    
names
=
[
"
ar
-
mr
"
]
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
class
MoroccoArabicLocale
(
ArabicLocale
)
:
    
names
=
[
"
ar
-
ma
"
]
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
class
IcelandicLocale
(
Locale
)
:
    
def
_format_timeframe
(
self
timeframe
:
TimeFrameLiteral
delta
:
int
)
-
>
str
:
        
form
=
self
.
timeframes
[
timeframe
]
        
if
isinstance
(
form
Mapping
)
:
            
if
delta
<
0
:
                
form
=
form
[
"
past
"
]
            
elif
delta
>
0
:
                
form
=
form
[
"
future
"
]
            
else
:
                
raise
ValueError
(
                    
"
Icelandic
Locale
does
not
support
units
with
a
delta
of
zero
.
"
                    
"
Please
consider
making
a
contribution
to
fix
this
issue
.
"
                
)
        
return
form
.
format
(
abs
(
delta
)
)
    
names
=
[
"
is
"
"
is
-
is
"
]
    
past
=
"
fyrir
{
0
}
s
an
"
    
future
=
"
eftir
{
0
}
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
r
tt
essu
"
        
"
second
"
:
{
"
past
"
:
"
sek
ndu
"
"
future
"
:
"
sek
ndu
"
}
        
"
seconds
"
:
{
"
past
"
:
"
{
0
}
nokkrum
sek
ndum
"
"
future
"
:
"
nokkrar
sek
ndur
"
}
        
"
minute
"
:
{
"
past
"
:
"
einni
m
n
tu
"
"
future
"
:
"
eina
m
n
tu
"
}
        
"
minutes
"
:
{
"
past
"
:
"
{
0
}
m
n
tum
"
"
future
"
:
"
{
0
}
m
n
tur
"
}
        
"
hour
"
:
{
"
past
"
:
"
einum
t
ma
"
"
future
"
:
"
einn
t
ma
"
}
        
"
hours
"
:
{
"
past
"
:
"
{
0
}
t
mum
"
"
future
"
:
"
{
0
}
t
ma
"
}
        
"
day
"
:
{
"
past
"
:
"
einum
degi
"
"
future
"
:
"
einn
dag
"
}
        
"
days
"
:
{
"
past
"
:
"
{
0
}
d
gum
"
"
future
"
:
"
{
0
}
daga
"
}
        
"
month
"
:
{
"
past
"
:
"
einum
m
nu
i
"
"
future
"
:
"
einn
m
nu
"
}
        
"
months
"
:
{
"
past
"
:
"
{
0
}
m
nu
um
"
"
future
"
:
"
{
0
}
m
nu
i
"
}
        
"
year
"
:
{
"
past
"
:
"
einu
ri
"
"
future
"
:
"
eitt
r
"
}
        
"
years
"
:
{
"
past
"
:
"
{
0
}
rum
"
"
future
"
:
"
{
0
}
r
"
}
    
}
    
meridians
=
{
"
am
"
:
"
f
.
h
.
"
"
pm
"
:
"
e
.
h
.
"
"
AM
"
:
"
f
.
h
.
"
"
PM
"
:
"
e
.
h
.
"
}
    
month_names
=
[
        
"
"
        
"
jan
ar
"
        
"
febr
ar
"
        
"
mars
"
        
"
apr
l
"
        
"
ma
"
        
"
j
n
"
        
"
j
l
"
        
"
g
st
"
        
"
september
"
        
"
okt
ber
"
        
"
n
vember
"
        
"
desember
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
jan
"
        
"
feb
"
        
"
mar
"
        
"
apr
"
        
"
ma
"
        
"
j
n
"
        
"
j
l
"
        
"
g
"
        
"
sep
"
        
"
okt
"
        
"
n
v
"
        
"
des
"
    
]
    
day_names
=
[
        
"
"
        
"
m
nudagur
"
        
"
ri
judagur
"
        
"
mi
vikudagur
"
        
"
fimmtudagur
"
        
"
f
studagur
"
        
"
laugardagur
"
        
"
sunnudagur
"
    
]
    
day_abbreviations
=
[
"
"
"
m
n
"
"
ri
"
"
mi
"
"
fim
"
"
f
s
"
"
lau
"
"
sun
"
]
class
DanishLocale
(
Locale
)
:
    
names
=
[
"
da
"
"
da
-
dk
"
]
    
past
=
"
for
{
0
}
siden
"
    
future
=
"
om
{
0
}
"
    
and_word
=
"
og
"
    
timeframes
=
{
        
"
now
"
:
"
lige
nu
"
        
"
second
"
:
"
et
sekund
"
        
"
seconds
"
:
"
{
0
}
sekunder
"
        
"
minute
"
:
"
et
minut
"
        
"
minutes
"
:
"
{
0
}
minutter
"
        
"
hour
"
:
"
en
time
"
        
"
hours
"
:
"
{
0
}
timer
"
        
"
day
"
:
"
en
dag
"
        
"
days
"
:
"
{
0
}
dage
"
        
"
week
"
:
"
en
uge
"
        
"
weeks
"
:
"
{
0
}
uger
"
        
"
month
"
:
"
en
m
ned
"
        
"
months
"
:
"
{
0
}
m
neder
"
        
"
year
"
:
"
et
r
"
        
"
years
"
:
"
{
0
}
r
"
    
}
    
month_names
=
[
        
"
"
        
"
januar
"
        
"
februar
"
        
"
marts
"
        
"
april
"
        
"
maj
"
        
"
juni
"
        
"
juli
"
        
"
august
"
        
"
september
"
        
"
oktober
"
        
"
november
"
        
"
december
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
jan
"
        
"
feb
"
        
"
mar
"
        
"
apr
"
        
"
maj
"
        
"
jun
"
        
"
jul
"
        
"
aug
"
        
"
sep
"
        
"
okt
"
        
"
nov
"
        
"
dec
"
    
]
    
day_names
=
[
        
"
"
        
"
mandag
"
        
"
tirsdag
"
        
"
onsdag
"
        
"
torsdag
"
        
"
fredag
"
        
"
l
rdag
"
        
"
s
ndag
"
    
]
    
day_abbreviations
=
[
"
"
"
man
"
"
tir
"
"
ons
"
"
tor
"
"
fre
"
"
l
r
"
"
s
n
"
]
    
def
_ordinal_number
(
self
n
:
int
)
-
>
str
:
        
return
f
"
{
n
}
.
"
class
MalayalamLocale
(
Locale
)
:
    
names
=
[
"
ml
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
"
        
"
days
"
:
"
{
0
}
"
        
"
month
"
:
"
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
"
        
"
years
"
:
"
{
0
}
"
    
}
    
meridians
=
{
        
"
am
"
:
"
"
        
"
pm
"
:
"
"
        
"
AM
"
:
"
"
        
"
PM
"
:
"
"
    
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
    
day_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
class
HindiLocale
(
Locale
)
:
    
names
=
[
"
hi
"
"
hi
-
in
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
"
        
"
days
"
:
"
{
0
}
"
        
"
month
"
:
"
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
"
        
"
years
"
:
"
{
0
}
"
    
}
    
meridians
=
{
"
am
"
:
"
"
"
pm
"
:
"
"
"
AM
"
:
"
"
"
PM
"
:
"
"
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
class
CzechLocale
(
Locale
)
:
    
names
=
[
"
cs
"
"
cs
-
cz
"
]
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
Te
"
        
"
second
"
:
{
"
past
"
:
"
vte
ina
"
"
future
"
:
"
vte
ina
"
}
        
"
seconds
"
:
{
            
"
zero
"
:
"
vte
ina
"
            
"
past
"
:
"
{
0
}
sekundami
"
            
"
future
-
singular
"
:
"
{
0
}
sekundy
"
            
"
future
-
paucal
"
:
"
{
0
}
sekund
"
        
}
        
"
minute
"
:
{
"
past
"
:
"
minutou
"
"
future
"
:
"
minutu
"
}
        
"
minutes
"
:
{
            
"
zero
"
:
"
{
0
}
minut
"
            
"
past
"
:
"
{
0
}
minutami
"
            
"
future
-
singular
"
:
"
{
0
}
minuty
"
            
"
future
-
paucal
"
:
"
{
0
}
minut
"
        
}
        
"
hour
"
:
{
"
past
"
:
"
hodinou
"
"
future
"
:
"
hodinu
"
}
        
"
hours
"
:
{
            
"
zero
"
:
"
{
0
}
hodin
"
            
"
past
"
:
"
{
0
}
hodinami
"
            
"
future
-
singular
"
:
"
{
0
}
hodiny
"
            
"
future
-
paucal
"
:
"
{
0
}
hodin
"
        
}
        
"
day
"
:
{
"
past
"
:
"
dnem
"
"
future
"
:
"
den
"
}
        
"
days
"
:
{
            
"
zero
"
:
"
{
0
}
dn
"
            
"
past
"
:
"
{
0
}
dny
"
            
"
future
-
singular
"
:
"
{
0
}
dny
"
            
"
future
-
paucal
"
:
"
{
0
}
dn
"
        
}
        
"
week
"
:
{
"
past
"
:
"
t
dnem
"
"
future
"
:
"
t
den
"
}
        
"
weeks
"
:
{
            
"
zero
"
:
"
{
0
}
t
dn
"
            
"
past
"
:
"
{
0
}
t
dny
"
            
"
future
-
singular
"
:
"
{
0
}
t
dny
"
            
"
future
-
paucal
"
:
"
{
0
}
t
dn
"
        
}
        
"
month
"
:
{
"
past
"
:
"
m
s
cem
"
"
future
"
:
"
m
s
c
"
}
        
"
months
"
:
{
            
"
zero
"
:
"
{
0
}
m
s
c
"
            
"
past
"
:
"
{
0
}
m
s
ci
"
            
"
future
-
singular
"
:
"
{
0
}
m
s
ce
"
            
"
future
-
paucal
"
:
"
{
0
}
m
s
c
"
        
}
        
"
year
"
:
{
"
past
"
:
"
rokem
"
"
future
"
:
"
rok
"
}
        
"
years
"
:
{
            
"
zero
"
:
"
{
0
}
let
"
            
"
past
"
:
"
{
0
}
lety
"
            
"
future
-
singular
"
:
"
{
0
}
roky
"
            
"
future
-
paucal
"
:
"
{
0
}
let
"
        
}
    
}
    
past
=
"
P
ed
{
0
}
"
    
future
=
"
Za
{
0
}
"
    
month_names
=
[
        
"
"
        
"
leden
"
        
"
nor
"
        
"
b
ezen
"
        
"
duben
"
        
"
kv
ten
"
        
"
erven
"
        
"
ervenec
"
        
"
srpen
"
        
"
z
"
        
"
jen
"
        
"
listopad
"
        
"
prosinec
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
led
"
        
"
no
"
        
"
b
e
"
        
"
dub
"
        
"
kv
"
        
"
vn
"
        
"
vc
"
        
"
srp
"
        
"
z
"
        
"
j
"
        
"
lis
"
        
"
pro
"
    
]
    
day_names
=
[
        
"
"
        
"
pond
l
"
        
"
ter
"
        
"
st
eda
"
        
"
tvrtek
"
        
"
p
tek
"
        
"
sobota
"
        
"
ned
le
"
    
]
    
day_abbreviations
=
[
"
"
"
po
"
"
t
"
"
st
"
"
t
"
"
p
"
"
so
"
"
ne
"
]
    
def
_format_timeframe
(
self
timeframe
:
TimeFrameLiteral
delta
:
int
)
-
>
str
:
        
"
"
"
Czech
aware
time
frame
format
function
takes
into
account
        
the
differences
between
past
and
future
forms
.
"
"
"
        
abs_delta
=
abs
(
delta
)
        
form
=
self
.
timeframes
[
timeframe
]
        
if
isinstance
(
form
str
)
:
            
return
form
.
format
(
abs_delta
)
        
if
delta
=
=
0
:
            
key
=
"
zero
"
        
elif
delta
<
0
:
            
key
=
"
past
"
        
else
:
            
if
"
future
-
singular
"
not
in
form
:
                
key
=
"
future
"
            
elif
2
<
=
abs_delta
%
10
<
=
4
and
(
                
abs_delta
%
100
<
10
or
abs_delta
%
100
>
=
20
            
)
:
                
key
=
"
future
-
singular
"
            
else
:
                
key
=
"
future
-
paucal
"
        
form
:
str
=
form
[
key
]
        
return
form
.
format
(
abs_delta
)
class
SlovakLocale
(
Locale
)
:
    
names
=
[
"
sk
"
"
sk
-
sk
"
]
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
Teraz
"
        
"
second
"
:
{
"
past
"
:
"
sekundou
"
"
future
"
:
"
sekundu
"
}
        
"
seconds
"
:
{
            
"
zero
"
:
"
{
0
}
sek
nd
"
            
"
past
"
:
"
{
0
}
sekundami
"
            
"
future
-
singular
"
:
"
{
0
}
sekundy
"
            
"
future
-
paucal
"
:
"
{
0
}
sek
nd
"
        
}
        
"
minute
"
:
{
"
past
"
:
"
min
tou
"
"
future
"
:
"
min
tu
"
}
        
"
minutes
"
:
{
            
"
zero
"
:
"
{
0
}
min
t
"
            
"
past
"
:
"
{
0
}
min
tami
"
            
"
future
-
singular
"
:
"
{
0
}
min
ty
"
            
"
future
-
paucal
"
:
"
{
0
}
min
t
"
        
}
        
"
hour
"
:
{
"
past
"
:
"
hodinou
"
"
future
"
:
"
hodinu
"
}
        
"
hours
"
:
{
            
"
zero
"
:
"
{
0
}
hod
n
"
            
"
past
"
:
"
{
0
}
hodinami
"
            
"
future
-
singular
"
:
"
{
0
}
hodiny
"
            
"
future
-
paucal
"
:
"
{
0
}
hod
n
"
        
}
        
"
day
"
:
{
"
past
"
:
"
d
om
"
"
future
"
:
"
de
"
}
        
"
days
"
:
{
            
"
zero
"
:
"
{
0
}
dn
"
            
"
past
"
:
"
{
0
}
d
ami
"
            
"
future
-
singular
"
:
"
{
0
}
dni
"
            
"
future
-
paucal
"
:
"
{
0
}
dn
"
        
}
        
"
week
"
:
{
"
past
"
:
"
t
d
om
"
"
future
"
:
"
t
de
"
}
        
"
weeks
"
:
{
            
"
zero
"
:
"
{
0
}
t
d
ov
"
            
"
past
"
:
"
{
0
}
t
d
ami
"
            
"
future
-
singular
"
:
"
{
0
}
t
dne
"
            
"
future
-
paucal
"
:
"
{
0
}
t
d
ov
"
        
}
        
"
month
"
:
{
"
past
"
:
"
mesiacom
"
"
future
"
:
"
mesiac
"
}
        
"
months
"
:
{
            
"
zero
"
:
"
{
0
}
mesiacov
"
            
"
past
"
:
"
{
0
}
mesiacmi
"
            
"
future
-
singular
"
:
"
{
0
}
mesiace
"
            
"
future
-
paucal
"
:
"
{
0
}
mesiacov
"
        
}
        
"
year
"
:
{
"
past
"
:
"
rokom
"
"
future
"
:
"
rok
"
}
        
"
years
"
:
{
            
"
zero
"
:
"
{
0
}
rokov
"
            
"
past
"
:
"
{
0
}
rokmi
"
            
"
future
-
singular
"
:
"
{
0
}
roky
"
            
"
future
-
paucal
"
:
"
{
0
}
rokov
"
        
}
    
}
    
past
=
"
Pred
{
0
}
"
    
future
=
"
O
{
0
}
"
    
and_word
=
"
a
"
    
month_names
=
[
        
"
"
        
"
janu
r
"
        
"
febru
r
"
        
"
marec
"
        
"
apr
l
"
        
"
m
j
"
        
"
j
n
"
        
"
j
l
"
        
"
august
"
        
"
september
"
        
"
okt
ber
"
        
"
november
"
        
"
december
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
jan
"
        
"
feb
"
        
"
mar
"
        
"
apr
"
        
"
m
j
"
        
"
j
n
"
        
"
j
l
"
        
"
aug
"
        
"
sep
"
        
"
okt
"
        
"
nov
"
        
"
dec
"
    
]
    
day_names
=
[
        
"
"
        
"
pondelok
"
        
"
utorok
"
        
"
streda
"
        
"
tvrtok
"
        
"
piatok
"
        
"
sobota
"
        
"
nede
a
"
    
]
    
day_abbreviations
=
[
"
"
"
po
"
"
ut
"
"
st
"
"
t
"
"
pi
"
"
so
"
"
ne
"
]
    
def
_format_timeframe
(
self
timeframe
:
TimeFrameLiteral
delta
:
int
)
-
>
str
:
        
"
"
"
Slovak
aware
time
frame
format
function
takes
into
account
        
the
differences
between
past
and
future
forms
.
"
"
"
        
abs_delta
=
abs
(
delta
)
        
form
=
self
.
timeframes
[
timeframe
]
        
if
isinstance
(
form
str
)
:
            
return
form
.
format
(
abs_delta
)
        
if
delta
=
=
0
:
            
key
=
"
zero
"
        
elif
delta
<
0
:
            
key
=
"
past
"
        
else
:
            
if
"
future
-
singular
"
not
in
form
:
                
key
=
"
future
"
            
elif
2
<
=
abs_delta
%
10
<
=
4
and
(
                
abs_delta
%
100
<
10
or
abs_delta
%
100
>
=
20
            
)
:
                
key
=
"
future
-
singular
"
            
else
:
                
key
=
"
future
-
paucal
"
        
form
:
str
=
form
[
key
]
        
return
form
.
format
(
abs_delta
)
class
FarsiLocale
(
Locale
)
:
    
names
=
[
"
fa
"
"
fa
-
ir
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
"
        
"
days
"
:
"
{
0
}
"
        
"
month
"
:
"
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
"
        
"
years
"
:
"
{
0
}
"
    
}
    
meridians
=
{
        
"
am
"
:
"
"
        
"
pm
"
:
"
"
        
"
AM
"
:
"
"
        
"
PM
"
:
"
"
    
}
    
month_names
=
[
        
"
"
        
"
January
"
        
"
February
"
        
"
March
"
        
"
April
"
        
"
May
"
        
"
June
"
        
"
July
"
        
"
August
"
        
"
September
"
        
"
October
"
        
"
November
"
        
"
December
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
Jan
"
        
"
Feb
"
        
"
Mar
"
        
"
Apr
"
        
"
May
"
        
"
Jun
"
        
"
Jul
"
        
"
Aug
"
        
"
Sep
"
        
"
Oct
"
        
"
Nov
"
        
"
Dec
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
"
"
"
Mon
"
"
Tue
"
"
Wed
"
"
Thu
"
"
Fri
"
"
Sat
"
"
Sun
"
]
class
HebrewLocale
(
Locale
)
:
    
names
=
[
"
he
"
"
he
-
il
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
and_word
=
"
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
"
        
"
hours
"
:
{
"
2
"
:
"
"
"
ten
"
:
"
{
0
}
"
"
higher
"
:
"
{
0
}
"
}
        
"
day
"
:
"
"
        
"
days
"
:
{
"
2
"
:
"
"
"
ten
"
:
"
{
0
}
"
"
higher
"
:
"
{
0
}
"
}
        
"
week
"
:
"
"
        
"
weeks
"
:
{
"
2
"
:
"
"
"
ten
"
:
"
{
0
}
"
"
higher
"
:
"
{
0
}
"
}
        
"
month
"
:
"
"
        
"
months
"
:
{
"
2
"
:
"
"
"
ten
"
:
"
{
0
}
"
"
higher
"
:
"
{
0
}
"
}
        
"
year
"
:
"
"
        
"
years
"
:
{
"
2
"
:
"
"
"
ten
"
:
"
{
0
}
"
"
higher
"
:
"
{
0
}
"
}
    
}
    
meridians
=
{
        
"
am
"
:
'
"
'
        
"
pm
"
:
'
"
'
        
"
AM
"
:
"
"
        
"
PM
"
:
"
"
    
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
    
day_abbreviations
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
    
def
_format_timeframe
(
self
timeframe
:
TimeFrameLiteral
delta
:
int
)
-
>
str
:
        
form
=
self
.
timeframes
[
timeframe
]
        
delta
=
abs
(
delta
)
        
if
isinstance
(
form
Mapping
)
:
            
if
delta
=
=
2
:
                
form
=
form
[
"
2
"
]
            
elif
delta
=
=
0
or
2
<
delta
<
=
10
:
                
form
=
form
[
"
ten
"
]
            
else
:
                
form
=
form
[
"
higher
"
]
        
return
form
.
format
(
delta
)
    
def
describe_multi
(
        
self
        
timeframes
:
Sequence
[
Tuple
[
TimeFrameLiteral
Union
[
int
float
]
]
]
        
only_distance
:
bool
=
False
    
)
-
>
str
:
        
"
"
"
Describes
a
delta
within
multiple
timeframes
in
plain
language
.
        
In
Hebrew
the
and
word
behaves
a
bit
differently
.
        
:
param
timeframes
:
a
list
of
string
quantity
pairs
each
representing
a
timeframe
and
delta
.
        
:
param
only_distance
:
return
only
distance
eg
:
"
2
hours
and
11
seconds
"
without
"
in
"
or
"
ago
"
keywords
        
"
"
"
        
humanized
=
"
"
        
for
index
(
timeframe
delta
)
in
enumerate
(
timeframes
)
:
            
last_humanized
=
self
.
_format_timeframe
(
timeframe
trunc
(
delta
)
)
            
if
index
=
=
0
:
                
humanized
=
last_humanized
            
elif
index
=
=
len
(
timeframes
)
-
1
:
                
humanized
+
=
"
"
+
self
.
and_word
                
if
last_humanized
[
0
]
.
isdecimal
(
)
:
                    
humanized
+
=
"
"
                
humanized
+
=
last_humanized
            
else
:
                
humanized
+
=
"
"
+
last_humanized
        
if
not
only_distance
:
            
humanized
=
self
.
_format_relative
(
humanized
timeframe
trunc
(
delta
)
)
        
return
humanized
class
MarathiLocale
(
Locale
)
:
    
names
=
[
"
mr
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
"
        
"
days
"
:
"
{
0
}
"
        
"
month
"
:
"
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
"
        
"
years
"
:
"
{
0
}
"
    
}
    
meridians
=
{
"
am
"
:
"
"
"
pm
"
:
"
"
"
AM
"
:
"
"
"
PM
"
:
"
"
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
class
CatalanLocale
(
Locale
)
:
    
names
=
[
"
ca
"
"
ca
-
es
"
"
ca
-
ad
"
"
ca
-
fr
"
"
ca
-
it
"
]
    
past
=
"
Fa
{
0
}
"
    
future
=
"
En
{
0
}
"
    
and_word
=
"
i
"
    
timeframes
=
{
        
"
now
"
:
"
Ara
mateix
"
        
"
second
"
:
"
un
segon
"
        
"
seconds
"
:
"
{
0
}
segons
"
        
"
minute
"
:
"
un
minut
"
        
"
minutes
"
:
"
{
0
}
minuts
"
        
"
hour
"
:
"
una
hora
"
        
"
hours
"
:
"
{
0
}
hores
"
        
"
day
"
:
"
un
dia
"
        
"
days
"
:
"
{
0
}
dies
"
        
"
month
"
:
"
un
mes
"
        
"
months
"
:
"
{
0
}
mesos
"
        
"
year
"
:
"
un
any
"
        
"
years
"
:
"
{
0
}
anys
"
    
}
    
month_names
=
[
        
"
"
        
"
gener
"
        
"
febrer
"
        
"
mar
"
        
"
abril
"
        
"
maig
"
        
"
juny
"
        
"
juliol
"
        
"
agost
"
        
"
setembre
"
        
"
octubre
"
        
"
novembre
"
        
"
desembre
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
gen
.
"
        
"
febr
.
"
        
"
mar
"
        
"
abr
.
"
        
"
maig
"
        
"
juny
"
        
"
jul
.
"
        
"
ag
.
"
        
"
set
.
"
        
"
oct
.
"
        
"
nov
.
"
        
"
des
.
"
    
]
    
day_names
=
[
        
"
"
        
"
dilluns
"
        
"
dimarts
"
        
"
dimecres
"
        
"
dijous
"
        
"
divendres
"
        
"
dissabte
"
        
"
diumenge
"
    
]
    
day_abbreviations
=
[
        
"
"
        
"
dl
.
"
        
"
dt
.
"
        
"
dc
.
"
        
"
dj
.
"
        
"
dv
.
"
        
"
ds
.
"
        
"
dg
.
"
    
]
class
BasqueLocale
(
Locale
)
:
    
names
=
[
"
eu
"
"
eu
-
eu
"
]
    
past
=
"
duela
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
Orain
"
        
"
second
"
:
"
segundo
bat
"
        
"
seconds
"
:
"
{
0
}
segundu
"
        
"
minute
"
:
"
minutu
bat
"
        
"
minutes
"
:
"
{
0
}
minutu
"
        
"
hour
"
:
"
ordu
bat
"
        
"
hours
"
:
"
{
0
}
ordu
"
        
"
day
"
:
"
egun
bat
"
        
"
days
"
:
"
{
0
}
egun
"
        
"
month
"
:
"
hilabete
bat
"
        
"
months
"
:
"
{
0
}
hilabet
"
        
"
year
"
:
"
urte
bat
"
        
"
years
"
:
"
{
0
}
urte
"
    
}
    
month_names
=
[
        
"
"
        
"
urtarrilak
"
        
"
otsailak
"
        
"
martxoak
"
        
"
apirilak
"
        
"
maiatzak
"
        
"
ekainak
"
        
"
uztailak
"
        
"
abuztuak
"
        
"
irailak
"
        
"
urriak
"
        
"
azaroak
"
        
"
abenduak
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
urt
"
        
"
ots
"
        
"
mar
"
        
"
api
"
        
"
mai
"
        
"
eka
"
        
"
uzt
"
        
"
abu
"
        
"
ira
"
        
"
urr
"
        
"
aza
"
        
"
abe
"
    
]
    
day_names
=
[
        
"
"
        
"
astelehena
"
        
"
asteartea
"
        
"
asteazkena
"
        
"
osteguna
"
        
"
ostirala
"
        
"
larunbata
"
        
"
igandea
"
    
]
    
day_abbreviations
=
[
"
"
"
al
"
"
ar
"
"
az
"
"
og
"
"
ol
"
"
lr
"
"
ig
"
]
class
HungarianLocale
(
Locale
)
:
    
names
=
[
"
hu
"
"
hu
-
hu
"
]
    
past
=
"
{
0
}
ezel
tt
"
    
future
=
"
{
0
}
m
lva
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
ppen
most
"
        
"
second
"
:
{
"
past
"
:
"
egy
m
sodik
"
"
future
"
:
"
egy
m
sodik
"
}
        
"
seconds
"
:
{
"
past
"
:
"
{
0
}
m
sodpercekkel
"
"
future
"
:
"
{
0
}
p
r
m
sodperc
"
}
        
"
minute
"
:
{
"
past
"
:
"
egy
perccel
"
"
future
"
:
"
egy
perc
"
}
        
"
minutes
"
:
{
"
past
"
:
"
{
0
}
perccel
"
"
future
"
:
"
{
0
}
perc
"
}
        
"
hour
"
:
{
"
past
"
:
"
egy
r
val
"
"
future
"
:
"
egy
ra
"
}
        
"
hours
"
:
{
"
past
"
:
"
{
0
}
r
val
"
"
future
"
:
"
{
0
}
ra
"
}
        
"
day
"
:
{
"
past
"
:
"
egy
nappal
"
"
future
"
:
"
egy
nap
"
}
        
"
days
"
:
{
"
past
"
:
"
{
0
}
nappal
"
"
future
"
:
"
{
0
}
nap
"
}
        
"
week
"
:
{
"
past
"
:
"
egy
h
ttel
"
"
future
"
:
"
egy
h
t
"
}
        
"
weeks
"
:
{
"
past
"
:
"
{
0
}
h
ttel
"
"
future
"
:
"
{
0
}
h
t
"
}
        
"
month
"
:
{
"
past
"
:
"
egy
h
nappal
"
"
future
"
:
"
egy
h
nap
"
}
        
"
months
"
:
{
"
past
"
:
"
{
0
}
h
nappal
"
"
future
"
:
"
{
0
}
h
nap
"
}
        
"
year
"
:
{
"
past
"
:
"
egy
vvel
"
"
future
"
:
"
egy
v
"
}
        
"
years
"
:
{
"
past
"
:
"
{
0
}
vvel
"
"
future
"
:
"
{
0
}
v
"
}
    
}
    
month_names
=
[
        
"
"
        
"
janu
r
"
        
"
febru
r
"
        
"
m
rcius
"
        
"
prilis
"
        
"
m
jus
"
        
"
j
nius
"
        
"
j
lius
"
        
"
augusztus
"
        
"
szeptember
"
        
"
okt
ber
"
        
"
november
"
        
"
december
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
jan
"
        
"
febr
"
        
"
m
rc
"
        
"
pr
"
        
"
m
j
"
        
"
j
n
"
        
"
j
l
"
        
"
aug
"
        
"
szept
"
        
"
okt
"
        
"
nov
"
        
"
dec
"
    
]
    
day_names
=
[
        
"
"
        
"
h
tf
"
        
"
kedd
"
        
"
szerda
"
        
"
cs
t
rt
k
"
        
"
p
ntek
"
        
"
szombat
"
        
"
vas
rnap
"
    
]
    
day_abbreviations
=
[
"
"
"
h
t
"
"
kedd
"
"
szer
"
"
cs
t
"
"
p
nt
"
"
szom
"
"
vas
"
]
    
meridians
=
{
"
am
"
:
"
de
"
"
pm
"
:
"
du
"
"
AM
"
:
"
DE
"
"
PM
"
:
"
DU
"
}
    
def
_format_timeframe
(
self
timeframe
:
TimeFrameLiteral
delta
:
int
)
-
>
str
:
        
form
=
self
.
timeframes
[
timeframe
]
        
if
isinstance
(
form
Mapping
)
:
            
if
delta
>
0
:
                
form
=
form
[
"
future
"
]
            
else
:
                
form
=
form
[
"
past
"
]
        
return
form
.
format
(
abs
(
delta
)
)
class
EsperantoLocale
(
Locale
)
:
    
names
=
[
"
eo
"
"
eo
-
xx
"
]
    
past
=
"
anta
{
0
}
"
    
future
=
"
post
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
nun
"
        
"
second
"
:
"
sekundo
"
        
"
seconds
"
:
"
{
0
}
kelkaj
sekundoj
"
        
"
minute
"
:
"
unu
minuto
"
        
"
minutes
"
:
"
{
0
}
minutoj
"
        
"
hour
"
:
"
un
horo
"
        
"
hours
"
:
"
{
0
}
horoj
"
        
"
day
"
:
"
unu
tago
"
        
"
days
"
:
"
{
0
}
tagoj
"
        
"
month
"
:
"
unu
monato
"
        
"
months
"
:
"
{
0
}
monatoj
"
        
"
year
"
:
"
unu
jaro
"
        
"
years
"
:
"
{
0
}
jaroj
"
    
}
    
month_names
=
[
        
"
"
        
"
januaro
"
        
"
februaro
"
        
"
marto
"
        
"
aprilo
"
        
"
majo
"
        
"
junio
"
        
"
julio
"
        
"
a
gusto
"
        
"
septembro
"
        
"
oktobro
"
        
"
novembro
"
        
"
decembro
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
jan
"
        
"
feb
"
        
"
mar
"
        
"
apr
"
        
"
maj
"
        
"
jun
"
        
"
jul
"
        
"
a
g
"
        
"
sep
"
        
"
okt
"
        
"
nov
"
        
"
dec
"
    
]
    
day_names
=
[
        
"
"
        
"
lundo
"
        
"
mardo
"
        
"
merkredo
"
        
"
a
do
"
        
"
vendredo
"
        
"
sabato
"
        
"
diman
o
"
    
]
    
day_abbreviations
=
[
"
"
"
lun
"
"
mar
"
"
mer
"
"
a
"
"
ven
"
"
sab
"
"
dim
"
]
    
meridians
=
{
"
am
"
:
"
atm
"
"
pm
"
:
"
ptm
"
"
AM
"
:
"
ATM
"
"
PM
"
:
"
PTM
"
}
    
ordinal_day_re
=
r
"
(
(
?
P
<
value
>
[
1
-
3
]
?
[
0
-
9
]
(
?
=
a
)
)
a
)
"
    
def
_ordinal_number
(
self
n
:
int
)
-
>
str
:
        
return
f
"
{
n
}
a
"
class
ThaiLocale
(
Locale
)
:
    
names
=
[
"
th
"
"
th
-
th
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
1
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
1
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
1
"
        
"
days
"
:
"
{
0
}
"
        
"
month
"
:
"
1
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
1
"
        
"
years
"
:
"
{
0
}
"
    
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
.
.
"
        
"
.
.
"
        
"
.
.
"
        
"
.
.
"
        
"
.
.
"
        
"
.
.
"
        
"
.
.
"
        
"
.
.
"
        
"
.
.
"
        
"
.
.
"
        
"
.
.
"
        
"
.
.
"
    
]
    
day_names
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
    
day_abbreviations
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
    
meridians
=
{
"
am
"
:
"
am
"
"
pm
"
:
"
pm
"
"
AM
"
:
"
AM
"
"
PM
"
:
"
PM
"
}
    
BE_OFFSET
=
543
    
def
year_full
(
self
year
:
int
)
-
>
str
:
        
"
"
"
Thai
always
use
Buddhist
Era
(
BE
)
which
is
CE
+
543
"
"
"
        
year
+
=
self
.
BE_OFFSET
        
return
f
"
{
year
:
04d
}
"
    
def
year_abbreviation
(
self
year
:
int
)
-
>
str
:
        
"
"
"
Thai
always
use
Buddhist
Era
(
BE
)
which
is
CE
+
543
"
"
"
        
year
+
=
self
.
BE_OFFSET
        
return
f
"
{
year
:
04d
}
"
[
2
:
]
    
def
_format_relative
(
        
self
        
humanized
:
str
        
timeframe
:
TimeFrameLiteral
        
delta
:
Union
[
float
int
]
    
)
-
>
str
:
        
"
"
"
Thai
normally
doesn
'
t
have
any
space
between
words
"
"
"
        
if
timeframe
=
=
"
now
"
:
            
return
humanized
        
direction
=
self
.
past
if
delta
<
0
else
self
.
future
        
relative_string
=
direction
.
format
(
humanized
)
        
if
timeframe
=
=
"
seconds
"
:
            
relative_string
=
relative_string
.
replace
(
"
"
"
"
)
        
return
relative_string
class
LaotianLocale
(
Locale
)
:
    
names
=
[
"
lo
"
"
lo
-
la
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
"
        
"
days
"
:
"
{
0
}
"
        
"
week
"
:
"
"
        
"
weeks
"
:
"
{
0
}
"
        
"
month
"
:
"
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
"
        
"
years
"
:
"
{
0
}
"
    
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
BE_OFFSET
=
543
    
def
year_full
(
self
year
:
int
)
-
>
str
:
        
"
"
"
Lao
always
use
Buddhist
Era
(
BE
)
which
is
CE
+
543
"
"
"
        
year
+
=
self
.
BE_OFFSET
        
return
f
"
{
year
:
04d
}
"
    
def
year_abbreviation
(
self
year
:
int
)
-
>
str
:
        
"
"
"
Lao
always
use
Buddhist
Era
(
BE
)
which
is
CE
+
543
"
"
"
        
year
+
=
self
.
BE_OFFSET
        
return
f
"
{
year
:
04d
}
"
[
2
:
]
    
def
_format_relative
(
        
self
        
humanized
:
str
        
timeframe
:
TimeFrameLiteral
        
delta
:
Union
[
float
int
]
    
)
-
>
str
:
        
"
"
"
Lao
normally
doesn
'
t
have
any
space
between
words
"
"
"
        
if
timeframe
=
=
"
now
"
:
            
return
humanized
        
direction
=
self
.
past
if
delta
<
0
else
self
.
future
        
relative_string
=
direction
.
format
(
humanized
)
        
if
timeframe
=
=
"
seconds
"
:
            
relative_string
=
relative_string
.
replace
(
"
"
"
"
)
        
return
relative_string
class
BengaliLocale
(
Locale
)
:
    
names
=
[
"
bn
"
"
bn
-
bd
"
"
bn
-
in
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
"
        
"
days
"
:
"
{
0
}
"
        
"
month
"
:
"
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
"
        
"
years
"
:
"
{
0
}
"
    
}
    
meridians
=
{
"
am
"
:
"
"
"
pm
"
:
"
"
"
AM
"
:
"
"
"
PM
"
:
"
"
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
    
def
_ordinal_number
(
self
n
:
int
)
-
>
str
:
        
if
n
>
10
or
n
=
=
0
:
            
return
f
"
{
n
}
"
        
if
n
in
[
1
5
7
8
9
10
]
:
            
return
f
"
{
n
}
"
        
if
n
in
[
2
3
]
:
            
return
f
"
{
n
}
"
        
if
n
=
=
4
:
            
return
f
"
{
n
}
"
        
if
n
=
=
6
:
            
return
f
"
{
n
}
"
        
return
"
"
class
RomanshLocale
(
Locale
)
:
    
names
=
[
"
rm
"
"
rm
-
ch
"
]
    
past
=
"
avant
{
0
}
"
    
future
=
"
en
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
en
quest
mument
"
        
"
second
"
:
"
in
secunda
"
        
"
seconds
"
:
"
{
0
}
secundas
"
        
"
minute
"
:
"
ina
minuta
"
        
"
minutes
"
:
"
{
0
}
minutas
"
        
"
hour
"
:
"
in
'
ura
"
        
"
hours
"
:
"
{
0
}
ura
"
        
"
day
"
:
"
in
di
"
        
"
days
"
:
"
{
0
}
dis
"
        
"
week
"
:
"
in
'
emna
"
        
"
weeks
"
:
"
{
0
}
emnas
"
        
"
month
"
:
"
in
mais
"
        
"
months
"
:
"
{
0
}
mais
"
        
"
year
"
:
"
in
onn
"
        
"
years
"
:
"
{
0
}
onns
"
    
}
    
month_names
=
[
        
"
"
        
"
schaner
"
        
"
favrer
"
        
"
mars
"
        
"
avrigl
"
        
"
matg
"
        
"
zercladur
"
        
"
fanadur
"
        
"
avust
"
        
"
settember
"
        
"
october
"
        
"
november
"
        
"
december
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
schan
"
        
"
fav
"
        
"
mars
"
        
"
avr
"
        
"
matg
"
        
"
zer
"
        
"
fan
"
        
"
avu
"
        
"
set
"
        
"
oct
"
        
"
nov
"
        
"
dec
"
    
]
    
day_names
=
[
        
"
"
        
"
glindesdi
"
        
"
mardi
"
        
"
mesemna
"
        
"
gievgia
"
        
"
venderdi
"
        
"
sonda
"
        
"
dumengia
"
    
]
    
day_abbreviations
=
[
"
"
"
gli
"
"
ma
"
"
me
"
"
gie
"
"
ve
"
"
so
"
"
du
"
]
class
RomanianLocale
(
Locale
)
:
    
names
=
[
"
ro
"
"
ro
-
ro
"
]
    
past
=
"
{
0
}
n
urm
"
    
future
=
"
peste
{
0
}
"
    
and_word
=
"
i
"
    
timeframes
=
{
        
"
now
"
:
"
acum
"
        
"
second
"
:
"
o
secunda
"
        
"
seconds
"
:
"
{
0
}
c
teva
secunde
"
        
"
minute
"
:
"
un
minut
"
        
"
minutes
"
:
"
{
0
}
minute
"
        
"
hour
"
:
"
o
or
"
        
"
hours
"
:
"
{
0
}
ore
"
        
"
day
"
:
"
o
zi
"
        
"
days
"
:
"
{
0
}
zile
"
        
"
month
"
:
"
o
lun
"
        
"
months
"
:
"
{
0
}
luni
"
        
"
year
"
:
"
un
an
"
        
"
years
"
:
"
{
0
}
ani
"
    
}
    
month_names
=
[
        
"
"
        
"
ianuarie
"
        
"
februarie
"
        
"
martie
"
        
"
aprilie
"
        
"
mai
"
        
"
iunie
"
        
"
iulie
"
        
"
august
"
        
"
septembrie
"
        
"
octombrie
"
        
"
noiembrie
"
        
"
decembrie
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
ian
"
        
"
febr
"
        
"
mart
"
        
"
apr
"
        
"
mai
"
        
"
iun
"
        
"
iul
"
        
"
aug
"
        
"
sept
"
        
"
oct
"
        
"
nov
"
        
"
dec
"
    
]
    
day_names
=
[
        
"
"
        
"
luni
"
        
"
mar
i
"
        
"
miercuri
"
        
"
joi
"
        
"
vineri
"
        
"
s
mb
t
"
        
"
duminic
"
    
]
    
day_abbreviations
=
[
"
"
"
Lun
"
"
Mar
"
"
Mie
"
"
Joi
"
"
Vin
"
"
S
m
"
"
Dum
"
]
class
SlovenianLocale
(
Locale
)
:
    
names
=
[
"
sl
"
"
sl
-
si
"
]
    
past
=
"
pred
{
0
}
"
    
future
=
"
ez
{
0
}
"
    
and_word
=
"
in
"
    
timeframes
=
{
        
"
now
"
:
"
zdaj
"
        
"
second
"
:
"
sekundo
"
        
"
seconds
"
:
"
{
0
}
sekund
"
        
"
minute
"
:
"
minuta
"
        
"
minutes
"
:
"
{
0
}
minutami
"
        
"
hour
"
:
"
uro
"
        
"
hours
"
:
"
{
0
}
ur
"
        
"
day
"
:
"
dan
"
        
"
days
"
:
"
{
0
}
dni
"
        
"
month
"
:
"
mesec
"
        
"
months
"
:
"
{
0
}
mesecev
"
        
"
year
"
:
"
leto
"
        
"
years
"
:
"
{
0
}
let
"
    
}
    
meridians
=
{
"
am
"
:
"
"
"
pm
"
:
"
"
"
AM
"
:
"
"
"
PM
"
:
"
"
}
    
month_names
=
[
        
"
"
        
"
Januar
"
        
"
Februar
"
        
"
Marec
"
        
"
April
"
        
"
Maj
"
        
"
Junij
"
        
"
Julij
"
        
"
Avgust
"
        
"
September
"
        
"
Oktober
"
        
"
November
"
        
"
December
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
Jan
"
        
"
Feb
"
        
"
Mar
"
        
"
Apr
"
        
"
Maj
"
        
"
Jun
"
        
"
Jul
"
        
"
Avg
"
        
"
Sep
"
        
"
Okt
"
        
"
Nov
"
        
"
Dec
"
    
]
    
day_names
=
[
        
"
"
        
"
Ponedeljek
"
        
"
Torek
"
        
"
Sreda
"
        
"
etrtek
"
        
"
Petek
"
        
"
Sobota
"
        
"
Nedelja
"
    
]
    
day_abbreviations
=
[
"
"
"
Pon
"
"
Tor
"
"
Sre
"
"
et
"
"
Pet
"
"
Sob
"
"
Ned
"
]
class
IndonesianLocale
(
Locale
)
:
    
names
=
[
"
id
"
"
id
-
id
"
]
    
past
=
"
{
0
}
yang
lalu
"
    
future
=
"
dalam
{
0
}
"
    
and_word
=
"
dan
"
    
timeframes
=
{
        
"
now
"
:
"
baru
saja
"
        
"
second
"
:
"
1
sebentar
"
        
"
seconds
"
:
"
{
0
}
detik
"
        
"
minute
"
:
"
1
menit
"
        
"
minutes
"
:
"
{
0
}
menit
"
        
"
hour
"
:
"
1
jam
"
        
"
hours
"
:
"
{
0
}
jam
"
        
"
day
"
:
"
1
hari
"
        
"
days
"
:
"
{
0
}
hari
"
        
"
week
"
:
"
1
minggu
"
        
"
weeks
"
:
"
{
0
}
minggu
"
        
"
month
"
:
"
1
bulan
"
        
"
months
"
:
"
{
0
}
bulan
"
        
"
quarter
"
:
"
1
kuartal
"
        
"
quarters
"
:
"
{
0
}
kuartal
"
        
"
year
"
:
"
1
tahun
"
        
"
years
"
:
"
{
0
}
tahun
"
    
}
    
meridians
=
{
"
am
"
:
"
"
"
pm
"
:
"
"
"
AM
"
:
"
"
"
PM
"
:
"
"
}
    
month_names
=
[
        
"
"
        
"
Januari
"
        
"
Februari
"
        
"
Maret
"
        
"
April
"
        
"
Mei
"
        
"
Juni
"
        
"
Juli
"
        
"
Agustus
"
        
"
September
"
        
"
Oktober
"
        
"
November
"
        
"
Desember
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
Jan
"
        
"
Feb
"
        
"
Mar
"
        
"
Apr
"
        
"
Mei
"
        
"
Jun
"
        
"
Jul
"
        
"
Ags
"
        
"
Sept
"
        
"
Okt
"
        
"
Nov
"
        
"
Des
"
    
]
    
day_names
=
[
"
"
"
Senin
"
"
Selasa
"
"
Rabu
"
"
Kamis
"
"
Jumat
"
"
Sabtu
"
"
Minggu
"
]
    
day_abbreviations
=
[
        
"
"
        
"
Senin
"
        
"
Selasa
"
        
"
Rabu
"
        
"
Kamis
"
        
"
Jumat
"
        
"
Sabtu
"
        
"
Minggu
"
    
]
class
NepaliLocale
(
Locale
)
:
    
names
=
[
"
ne
"
"
ne
-
np
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
"
        
"
days
"
:
"
{
0
}
"
        
"
month
"
:
"
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
"
        
"
years
"
:
"
{
0
}
"
    
}
    
meridians
=
{
"
am
"
:
"
"
"
pm
"
:
"
"
"
AM
"
:
"
"
"
PM
"
:
"
"
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
class
EstonianLocale
(
Locale
)
:
    
names
=
[
"
ee
"
"
et
"
]
    
past
=
"
{
0
}
tagasi
"
    
future
=
"
{
0
}
p
rast
"
    
and_word
=
"
ja
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Mapping
[
str
str
]
]
]
=
{
        
"
now
"
:
{
"
past
"
:
"
just
n
d
"
"
future
"
:
"
just
n
d
"
}
        
"
second
"
:
{
"
past
"
:
"
ks
sekund
"
"
future
"
:
"
he
sekundi
"
}
        
"
seconds
"
:
{
"
past
"
:
"
{
0
}
sekundit
"
"
future
"
:
"
{
0
}
sekundi
"
}
        
"
minute
"
:
{
"
past
"
:
"
ks
minut
"
"
future
"
:
"
he
minuti
"
}
        
"
minutes
"
:
{
"
past
"
:
"
{
0
}
minutit
"
"
future
"
:
"
{
0
}
minuti
"
}
        
"
hour
"
:
{
"
past
"
:
"
tund
aega
"
"
future
"
:
"
tunni
aja
"
}
        
"
hours
"
:
{
"
past
"
:
"
{
0
}
tundi
"
"
future
"
:
"
{
0
}
tunni
"
}
        
"
day
"
:
{
"
past
"
:
"
ks
p
ev
"
"
future
"
:
"
he
p
eva
"
}
        
"
days
"
:
{
"
past
"
:
"
{
0
}
p
eva
"
"
future
"
:
"
{
0
}
p
eva
"
}
        
"
month
"
:
{
"
past
"
:
"
ks
kuu
"
"
future
"
:
"
he
kuu
"
}
        
"
months
"
:
{
"
past
"
:
"
{
0
}
kuud
"
"
future
"
:
"
{
0
}
kuu
"
}
        
"
year
"
:
{
"
past
"
:
"
ks
aasta
"
"
future
"
:
"
he
aasta
"
}
        
"
years
"
:
{
"
past
"
:
"
{
0
}
aastat
"
"
future
"
:
"
{
0
}
aasta
"
}
    
}
    
month_names
=
[
        
"
"
        
"
Jaanuar
"
        
"
Veebruar
"
        
"
M
rts
"
        
"
Aprill
"
        
"
Mai
"
        
"
Juuni
"
        
"
Juuli
"
        
"
August
"
        
"
September
"
        
"
Oktoober
"
        
"
November
"
        
"
Detsember
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
Jan
"
        
"
Veb
"
        
"
M
r
"
        
"
Apr
"
        
"
Mai
"
        
"
Jun
"
        
"
Jul
"
        
"
Aug
"
        
"
Sep
"
        
"
Okt
"
        
"
Nov
"
        
"
Dets
"
    
]
    
day_names
=
[
        
"
"
        
"
Esmasp
ev
"
        
"
Teisip
ev
"
        
"
Kolmap
ev
"
        
"
Neljap
ev
"
        
"
Reede
"
        
"
Laup
ev
"
        
"
P
hap
ev
"
    
]
    
day_abbreviations
=
[
"
"
"
Esm
"
"
Teis
"
"
Kolm
"
"
Nelj
"
"
Re
"
"
Lau
"
"
P
h
"
]
    
def
_format_timeframe
(
self
timeframe
:
TimeFrameLiteral
delta
:
int
)
-
>
str
:
        
form
=
self
.
timeframes
[
timeframe
]
        
if
delta
>
0
:
            
_form
=
form
[
"
future
"
]
        
else
:
            
_form
=
form
[
"
past
"
]
        
return
_form
.
format
(
abs
(
delta
)
)
class
LatvianLocale
(
Locale
)
:
    
names
=
[
"
lv
"
"
lv
-
lv
"
]
    
past
=
"
pirms
{
0
}
"
    
future
=
"
p
c
{
0
}
"
    
and_word
=
"
un
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
tagad
"
        
"
second
"
:
"
sekundes
"
        
"
seconds
"
:
"
{
0
}
sekund
m
"
        
"
minute
"
:
"
min
tes
"
        
"
minutes
"
:
"
{
0
}
min
t
m
"
        
"
hour
"
:
"
stundas
"
        
"
hours
"
:
"
{
0
}
stund
m
"
        
"
day
"
:
"
dienas
"
        
"
days
"
:
"
{
0
}
dien
m
"
        
"
week
"
:
"
ned
as
"
        
"
weeks
"
:
"
{
0
}
ned
m
"
        
"
month
"
:
"
m
ne
a
"
        
"
months
"
:
"
{
0
}
m
ne
iem
"
        
"
year
"
:
"
gada
"
        
"
years
"
:
"
{
0
}
gadiem
"
    
}
    
month_names
=
[
        
"
"
        
"
janv
ris
"
        
"
febru
ris
"
        
"
marts
"
        
"
apr
lis
"
        
"
maijs
"
        
"
j
nijs
"
        
"
j
lijs
"
        
"
augusts
"
        
"
septembris
"
        
"
oktobris
"
        
"
novembris
"
        
"
decembris
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
jan
"
        
"
feb
"
        
"
marts
"
        
"
apr
"
        
"
maijs
"
        
"
j
nijs
"
        
"
j
lijs
"
        
"
aug
"
        
"
sept
"
        
"
okt
"
        
"
nov
"
        
"
dec
"
    
]
    
day_names
=
[
        
"
"
        
"
pirmdiena
"
        
"
otrdiena
"
        
"
tre
diena
"
        
"
ceturtdiena
"
        
"
piektdiena
"
        
"
sestdiena
"
        
"
sv
tdiena
"
    
]
    
day_abbreviations
=
[
        
"
"
        
"
pi
"
        
"
ot
"
        
"
tr
"
        
"
ce
"
        
"
pi
"
        
"
se
"
        
"
sv
"
    
]
class
SwahiliLocale
(
Locale
)
:
    
names
=
[
        
"
sw
"
        
"
sw
-
ke
"
        
"
sw
-
tz
"
    
]
    
past
=
"
{
0
}
iliyopita
"
    
future
=
"
muda
wa
{
0
}
"
    
and_word
=
"
na
"
    
timeframes
=
{
        
"
now
"
:
"
sasa
hivi
"
        
"
second
"
:
"
sekunde
"
        
"
seconds
"
:
"
sekunde
{
0
}
"
        
"
minute
"
:
"
dakika
moja
"
        
"
minutes
"
:
"
dakika
{
0
}
"
        
"
hour
"
:
"
saa
moja
"
        
"
hours
"
:
"
saa
{
0
}
"
        
"
day
"
:
"
siku
moja
"
        
"
days
"
:
"
siku
{
0
}
"
        
"
week
"
:
"
wiki
moja
"
        
"
weeks
"
:
"
wiki
{
0
}
"
        
"
month
"
:
"
mwezi
moja
"
        
"
months
"
:
"
miezi
{
0
}
"
        
"
year
"
:
"
mwaka
moja
"
        
"
years
"
:
"
miaka
{
0
}
"
    
}
    
meridians
=
{
"
am
"
:
"
asu
"
"
pm
"
:
"
mch
"
"
AM
"
:
"
ASU
"
"
PM
"
:
"
MCH
"
}
    
month_names
=
[
        
"
"
        
"
Januari
"
        
"
Februari
"
        
"
Machi
"
        
"
Aprili
"
        
"
Mei
"
        
"
Juni
"
        
"
Julai
"
        
"
Agosti
"
        
"
Septemba
"
        
"
Oktoba
"
        
"
Novemba
"
        
"
Desemba
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
Jan
"
        
"
Feb
"
        
"
Mac
"
        
"
Apr
"
        
"
Mei
"
        
"
Jun
"
        
"
Jul
"
        
"
Ago
"
        
"
Sep
"
        
"
Okt
"
        
"
Nov
"
        
"
Des
"
    
]
    
day_names
=
[
        
"
"
        
"
Jumatatu
"
        
"
Jumanne
"
        
"
Jumatano
"
        
"
Alhamisi
"
        
"
Ijumaa
"
        
"
Jumamosi
"
        
"
Jumapili
"
    
]
    
day_abbreviations
=
[
        
"
"
        
"
Jumatatu
"
        
"
Jumanne
"
        
"
Jumatano
"
        
"
Alhamisi
"
        
"
Ijumaa
"
        
"
Jumamosi
"
        
"
Jumapili
"
    
]
class
CroatianLocale
(
Locale
)
:
    
names
=
[
"
hr
"
"
hr
-
hr
"
]
    
past
=
"
prije
{
0
}
"
    
future
=
"
za
{
0
}
"
    
and_word
=
"
i
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
upravo
sad
"
        
"
second
"
:
"
sekundu
"
        
"
seconds
"
:
{
"
double
"
:
"
{
0
}
sekunde
"
"
higher
"
:
"
{
0
}
sekundi
"
}
        
"
minute
"
:
"
minutu
"
        
"
minutes
"
:
{
"
double
"
:
"
{
0
}
minute
"
"
higher
"
:
"
{
0
}
minuta
"
}
        
"
hour
"
:
"
sat
"
        
"
hours
"
:
{
"
double
"
:
"
{
0
}
sata
"
"
higher
"
:
"
{
0
}
sati
"
}
        
"
day
"
:
"
jedan
dan
"
        
"
days
"
:
{
"
double
"
:
"
{
0
}
dana
"
"
higher
"
:
"
{
0
}
dana
"
}
        
"
week
"
:
"
tjedan
"
        
"
weeks
"
:
{
"
double
"
:
"
{
0
}
tjedna
"
"
higher
"
:
"
{
0
}
tjedana
"
}
        
"
month
"
:
"
mjesec
"
        
"
months
"
:
{
"
double
"
:
"
{
0
}
mjeseca
"
"
higher
"
:
"
{
0
}
mjeseci
"
}
        
"
year
"
:
"
godinu
"
        
"
years
"
:
{
"
double
"
:
"
{
0
}
godine
"
"
higher
"
:
"
{
0
}
godina
"
}
    
}
    
month_names
=
[
        
"
"
        
"
sije
anj
"
        
"
velja
a
"
        
"
o
ujak
"
        
"
travanj
"
        
"
svibanj
"
        
"
lipanj
"
        
"
srpanj
"
        
"
kolovoz
"
        
"
rujan
"
        
"
listopad
"
        
"
studeni
"
        
"
prosinac
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
sije
"
        
"
velj
"
        
"
o
uj
"
        
"
trav
"
        
"
svib
"
        
"
lip
"
        
"
srp
"
        
"
kol
"
        
"
ruj
"
        
"
list
"
        
"
stud
"
        
"
pros
"
    
]
    
day_names
=
[
        
"
"
        
"
ponedjeljak
"
        
"
utorak
"
        
"
srijeda
"
        
"
etvrtak
"
        
"
petak
"
        
"
subota
"
        
"
nedjelja
"
    
]
    
day_abbreviations
=
[
        
"
"
        
"
po
"
        
"
ut
"
        
"
sr
"
        
"
e
"
        
"
pe
"
        
"
su
"
        
"
ne
"
    
]
    
def
_format_timeframe
(
self
timeframe
:
TimeFrameLiteral
delta
:
int
)
-
>
str
:
        
form
=
self
.
timeframes
[
timeframe
]
        
delta
=
abs
(
delta
)
        
if
isinstance
(
form
Mapping
)
:
            
if
1
<
delta
<
=
4
:
                
form
=
form
[
"
double
"
]
            
else
:
                
form
=
form
[
"
higher
"
]
        
return
form
.
format
(
delta
)
class
LatinLocale
(
Locale
)
:
    
names
=
[
"
la
"
"
la
-
va
"
]
    
past
=
"
ante
{
0
}
"
    
future
=
"
in
{
0
}
"
    
and_word
=
"
et
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
nunc
"
        
"
second
"
:
"
secundum
"
        
"
seconds
"
:
"
{
0
}
secundis
"
        
"
minute
"
:
"
minutam
"
        
"
minutes
"
:
"
{
0
}
minutis
"
        
"
hour
"
:
"
horam
"
        
"
hours
"
:
"
{
0
}
horas
"
        
"
day
"
:
"
diem
"
        
"
days
"
:
"
{
0
}
dies
"
        
"
week
"
:
"
hebdomadem
"
        
"
weeks
"
:
"
{
0
}
hebdomades
"
        
"
month
"
:
"
mensem
"
        
"
months
"
:
"
{
0
}
mensis
"
        
"
year
"
:
"
annum
"
        
"
years
"
:
"
{
0
}
annos
"
    
}
    
month_names
=
[
        
"
"
        
"
Ianuarius
"
        
"
Februarius
"
        
"
Martius
"
        
"
Aprilis
"
        
"
Maius
"
        
"
Iunius
"
        
"
Iulius
"
        
"
Augustus
"
        
"
September
"
        
"
October
"
        
"
November
"
        
"
December
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
Ian
"
        
"
Febr
"
        
"
Mart
"
        
"
Apr
"
        
"
Mai
"
        
"
Iun
"
        
"
Iul
"
        
"
Aug
"
        
"
Sept
"
        
"
Oct
"
        
"
Nov
"
        
"
Dec
"
    
]
    
day_names
=
[
        
"
"
        
"
dies
Lunae
"
        
"
dies
Martis
"
        
"
dies
Mercurii
"
        
"
dies
Iovis
"
        
"
dies
Veneris
"
        
"
dies
Saturni
"
        
"
dies
Solis
"
    
]
    
day_abbreviations
=
[
        
"
"
        
"
dies
Lunae
"
        
"
dies
Martis
"
        
"
dies
Mercurii
"
        
"
dies
Iovis
"
        
"
dies
Veneris
"
        
"
dies
Saturni
"
        
"
dies
Solis
"
    
]
class
LithuanianLocale
(
Locale
)
:
    
names
=
[
"
lt
"
"
lt
-
lt
"
]
    
past
=
"
prie
{
0
}
"
    
future
=
"
po
{
0
}
"
    
and_word
=
"
ir
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
dabar
"
        
"
second
"
:
"
sekund
s
"
        
"
seconds
"
:
"
{
0
}
sekund
i
"
        
"
minute
"
:
"
minut
s
"
        
"
minutes
"
:
"
{
0
}
minu
i
"
        
"
hour
"
:
"
valandos
"
        
"
hours
"
:
"
{
0
}
valand
"
        
"
day
"
:
"
dien
"
        
"
days
"
:
"
{
0
}
dien
"
        
"
week
"
:
"
savait
s
"
        
"
weeks
"
:
"
{
0
}
savai
i
"
        
"
month
"
:
"
m
nesio
"
        
"
months
"
:
"
{
0
}
m
nesi
"
        
"
year
"
:
"
met
"
        
"
years
"
:
"
{
0
}
met
"
    
}
    
month_names
=
[
        
"
"
        
"
sausis
"
        
"
vasaris
"
        
"
kovas
"
        
"
balandis
"
        
"
gegu
"
        
"
bir
elis
"
        
"
liepa
"
        
"
rugpj
tis
"
        
"
rugs
jis
"
        
"
spalis
"
        
"
lapkritis
"
        
"
gruodis
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
saus
"
        
"
vas
"
        
"
kovas
"
        
"
bal
"
        
"
geg
"
        
"
bir
"
        
"
liepa
"
        
"
rugp
"
        
"
rugs
"
        
"
spalis
"
        
"
lapkr
"
        
"
gr
"
    
]
    
day_names
=
[
        
"
"
        
"
pirmadienis
"
        
"
antradienis
"
        
"
tre
iadienis
"
        
"
ketvirtadienis
"
        
"
penktadienis
"
        
"
e
tadienis
"
        
"
sekmadienis
"
    
]
    
day_abbreviations
=
[
        
"
"
        
"
pi
"
        
"
an
"
        
"
tr
"
        
"
ke
"
        
"
pe
"
        
"
e
"
        
"
se
"
    
]
class
MalayLocale
(
Locale
)
:
    
names
=
[
"
ms
"
"
ms
-
my
"
"
ms
-
bn
"
]
    
past
=
"
{
0
}
yang
lalu
"
    
future
=
"
dalam
{
0
}
"
    
and_word
=
"
dan
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
sekarang
"
        
"
second
"
:
"
saat
"
        
"
seconds
"
:
"
{
0
}
saat
"
        
"
minute
"
:
"
minit
"
        
"
minutes
"
:
"
{
0
}
minit
"
        
"
hour
"
:
"
jam
"
        
"
hours
"
:
"
{
0
}
jam
"
        
"
day
"
:
"
hari
"
        
"
days
"
:
"
{
0
}
hari
"
        
"
week
"
:
"
minggu
"
        
"
weeks
"
:
"
{
0
}
minggu
"
        
"
month
"
:
"
bulan
"
        
"
months
"
:
"
{
0
}
bulan
"
        
"
year
"
:
"
tahun
"
        
"
years
"
:
"
{
0
}
tahun
"
    
}
    
month_names
=
[
        
"
"
        
"
Januari
"
        
"
Februari
"
        
"
Mac
"
        
"
April
"
        
"
Mei
"
        
"
Jun
"
        
"
Julai
"
        
"
Ogos
"
        
"
September
"
        
"
Oktober
"
        
"
November
"
        
"
Disember
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
Jan
.
"
        
"
Feb
.
"
        
"
Mac
"
        
"
Apr
.
"
        
"
Mei
"
        
"
Jun
"
        
"
Julai
"
        
"
Og
.
"
        
"
Sept
.
"
        
"
Okt
.
"
        
"
Nov
.
"
        
"
Dis
.
"
    
]
    
day_names
=
[
        
"
"
        
"
Isnin
"
        
"
Selasa
"
        
"
Rabu
"
        
"
Khamis
"
        
"
Jumaat
"
        
"
Sabtu
"
        
"
Ahad
"
    
]
    
day_abbreviations
=
[
        
"
"
        
"
Isnin
"
        
"
Selasa
"
        
"
Rabu
"
        
"
Khamis
"
        
"
Jumaat
"
        
"
Sabtu
"
        
"
Ahad
"
    
]
class
MalteseLocale
(
Locale
)
:
    
names
=
[
"
mt
"
"
mt
-
mt
"
]
    
past
=
"
{
0
}
ilu
"
    
future
=
"
fi
{
0
}
"
    
and_word
=
"
u
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
issa
"
        
"
second
"
:
"
sekonda
"
        
"
seconds
"
:
"
{
0
}
sekondi
"
        
"
minute
"
:
"
minuta
"
        
"
minutes
"
:
"
{
0
}
minuti
"
        
"
hour
"
:
"
sieg
a
"
        
"
hours
"
:
{
"
dual
"
:
"
{
0
}
sag
tejn
"
"
plural
"
:
"
{
0
}
sig
at
"
}
        
"
day
"
:
"
jum
"
        
"
days
"
:
{
"
dual
"
:
"
{
0
}
jumejn
"
"
plural
"
:
"
{
0
}
ijiem
"
}
        
"
week
"
:
"
img
a
"
        
"
weeks
"
:
{
"
dual
"
:
"
{
0
}
imag
tejn
"
"
plural
"
:
"
{
0
}
img
at
"
}
        
"
month
"
:
"
xahar
"
        
"
months
"
:
{
"
dual
"
:
"
{
0
}
xahrejn
"
"
plural
"
:
"
{
0
}
xhur
"
}
        
"
year
"
:
"
sena
"
        
"
years
"
:
{
"
dual
"
:
"
{
0
}
sentejn
"
"
plural
"
:
"
{
0
}
snin
"
}
    
}
    
month_names
=
[
        
"
"
        
"
Jannar
"
        
"
Frar
"
        
"
Marzu
"
        
"
April
"
        
"
Mejju
"
        
"
unju
"
        
"
Lulju
"
        
"
Awwissu
"
        
"
Settembru
"
        
"
Ottubru
"
        
"
Novembru
"
        
"
Di
embru
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
Jan
"
        
"
Fr
"
        
"
Mar
"
        
"
Apr
"
        
"
Mejju
"
        
"
un
"
        
"
Lul
"
        
"
Aw
"
        
"
Sett
"
        
"
Ott
"
        
"
Nov
"
        
"
Di
"
    
]
    
day_names
=
[
        
"
"
        
"
It
-
Tnejn
"
        
"
It
-
Tlieta
"
        
"
L
-
Erbg
a
"
        
"
Il
-
amis
"
        
"
Il
-
img
a
"
        
"
Is
-
Sibt
"
        
"
Il
-
add
"
    
]
    
day_abbreviations
=
[
        
"
"
        
"
T
"
        
"
TL
"
        
"
E
"
        
"
"
        
"
"
        
"
S
"
        
"
"
    
]
    
def
_format_timeframe
(
self
timeframe
:
TimeFrameLiteral
delta
:
int
)
-
>
str
:
        
form
=
self
.
timeframes
[
timeframe
]
        
delta
=
abs
(
delta
)
        
if
isinstance
(
form
Mapping
)
:
            
if
delta
=
=
2
:
                
form
=
form
[
"
dual
"
]
            
else
:
                
form
=
form
[
"
plural
"
]
        
return
form
.
format
(
delta
)
class
SamiLocale
(
Locale
)
:
    
names
=
[
"
se
"
"
se
-
fi
"
"
se
-
no
"
"
se
-
se
"
]
    
past
=
"
{
0
}
dass
i
"
    
future
=
"
{
0
}
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
d
l
"
        
"
second
"
:
"
sekunda
"
        
"
seconds
"
:
"
{
0
}
sekundda
"
        
"
minute
"
:
"
minuhta
"
        
"
minutes
"
:
"
{
0
}
minuhta
"
        
"
hour
"
:
"
diimmu
"
        
"
hours
"
:
"
{
0
}
diimmu
"
        
"
day
"
:
"
beaivvi
"
        
"
days
"
:
"
{
0
}
beaivvi
"
        
"
week
"
:
"
vahku
"
        
"
weeks
"
:
"
{
0
}
vahku
"
        
"
month
"
:
"
m
nu
"
        
"
months
"
:
"
{
0
}
m
nu
"
        
"
year
"
:
"
jagi
"
        
"
years
"
:
"
{
0
}
jagi
"
    
}
    
month_names
=
[
        
"
"
        
"
O
ajagim
nnu
"
        
"
Guovvam
nnu
"
        
"
Njuk
am
nnu
"
        
"
Cuo
om
nnu
"
        
"
Miessem
nnu
"
        
"
Geassem
nnu
"
        
"
Suoidnem
nnu
"
        
"
Borgem
nnu
"
        
"
ak
am
nnu
"
        
"
Golggotm
nnu
"
        
"
Sk
bmam
nnu
"
        
"
Juovlam
nnu
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
O
ajagim
nnu
"
        
"
Guovvam
nnu
"
        
"
Njuk
am
nnu
"
        
"
Cuo
om
nnu
"
        
"
Miessem
nnu
"
        
"
Geassem
nnu
"
        
"
Suoidnem
nnu
"
        
"
Borgem
nnu
"
        
"
ak
am
nnu
"
        
"
Golggotm
nnu
"
        
"
Sk
bmam
nnu
"
        
"
Juovlam
nnu
"
    
]
    
day_names
=
[
        
"
"
        
"
M
nnodat
"
        
"
Disdat
"
        
"
Gaskavahkku
"
        
"
Duorastat
"
        
"
Bearjadat
"
        
"
L
vvordat
"
        
"
Sotnabeaivi
"
    
]
    
day_abbreviations
=
[
        
"
"
        
"
M
nnodat
"
        
"
Disdat
"
        
"
Gaskavahkku
"
        
"
Duorastat
"
        
"
Bearjadat
"
        
"
L
vvordat
"
        
"
Sotnabeaivi
"
    
]
class
OdiaLocale
(
Locale
)
:
    
names
=
[
"
or
"
"
or
-
in
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
"
        
"
days
"
:
"
{
0
}
"
        
"
month
"
:
"
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
"
        
"
years
"
:
"
{
0
}
"
    
}
    
meridians
=
{
"
am
"
:
"
"
"
pm
"
:
"
"
"
AM
"
:
"
"
"
PM
"
:
"
"
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
def
_ordinal_number
(
self
n
:
int
)
-
>
str
:
        
if
n
>
10
or
n
=
=
0
:
            
return
f
"
{
n
}
"
        
if
n
in
[
1
5
7
8
9
10
]
:
            
return
f
"
{
n
}
"
        
if
n
in
[
2
3
]
:
            
return
f
"
{
n
}
"
        
if
n
=
=
4
:
            
return
f
"
{
n
}
"
        
if
n
=
=
6
:
            
return
f
"
{
n
}
"
        
return
"
"
class
SerbianLocale
(
Locale
)
:
    
names
=
[
"
sr
"
"
sr
-
rs
"
"
sr
-
sp
"
]
    
past
=
"
pre
{
0
}
"
    
future
=
"
za
{
0
}
"
    
and_word
=
"
i
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
str
Mapping
[
str
str
]
]
]
]
=
{
        
"
now
"
:
"
sada
"
        
"
second
"
:
"
sekundu
"
        
"
seconds
"
:
{
"
double
"
:
"
{
0
}
sekunde
"
"
higher
"
:
"
{
0
}
sekundi
"
}
        
"
minute
"
:
"
minutu
"
        
"
minutes
"
:
{
"
double
"
:
"
{
0
}
minute
"
"
higher
"
:
"
{
0
}
minuta
"
}
        
"
hour
"
:
"
sat
"
        
"
hours
"
:
{
"
double
"
:
"
{
0
}
sata
"
"
higher
"
:
"
{
0
}
sati
"
}
        
"
day
"
:
"
dan
"
        
"
days
"
:
{
"
double
"
:
"
{
0
}
dana
"
"
higher
"
:
"
{
0
}
dana
"
}
        
"
week
"
:
"
nedelju
"
        
"
weeks
"
:
{
"
double
"
:
"
{
0
}
nedelje
"
"
higher
"
:
"
{
0
}
nedelja
"
}
        
"
month
"
:
"
mesec
"
        
"
months
"
:
{
"
double
"
:
"
{
0
}
meseca
"
"
higher
"
:
"
{
0
}
meseci
"
}
        
"
year
"
:
"
godinu
"
        
"
years
"
:
{
"
double
"
:
"
{
0
}
godine
"
"
higher
"
:
"
{
0
}
godina
"
}
    
}
    
month_names
=
[
        
"
"
        
"
januar
"
        
"
februar
"
        
"
mart
"
        
"
april
"
        
"
maj
"
        
"
jun
"
        
"
jul
"
        
"
avgust
"
        
"
septembar
"
        
"
oktobar
"
        
"
novembar
"
        
"
decembar
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
jan
"
        
"
feb
"
        
"
mar
"
        
"
apr
"
        
"
maj
"
        
"
jun
"
        
"
jul
"
        
"
avg
"
        
"
sep
"
        
"
okt
"
        
"
nov
"
        
"
dec
"
    
]
    
day_names
=
[
        
"
"
        
"
ponedeljak
"
        
"
utorak
"
        
"
sreda
"
        
"
etvrtak
"
        
"
petak
"
        
"
subota
"
        
"
nedelja
"
    
]
    
day_abbreviations
=
[
        
"
"
        
"
po
"
        
"
ut
"
        
"
sr
"
        
"
e
"
        
"
pe
"
        
"
su
"
        
"
ne
"
    
]
    
def
_format_timeframe
(
self
timeframe
:
TimeFrameLiteral
delta
:
int
)
-
>
str
:
        
form
=
self
.
timeframes
[
timeframe
]
        
delta
=
abs
(
delta
)
        
if
isinstance
(
form
Mapping
)
:
            
if
1
<
delta
<
=
4
:
                
form
=
form
[
"
double
"
]
            
else
:
                
form
=
form
[
"
higher
"
]
        
return
form
.
format
(
delta
)
class
LuxembourgishLocale
(
Locale
)
:
    
names
=
[
"
lb
"
"
lb
-
lu
"
]
    
past
=
"
virun
{
0
}
"
    
future
=
"
an
{
0
}
"
    
and_word
=
"
an
"
    
timeframes
:
ClassVar
[
Dict
[
TimeFrameLiteral
str
]
]
=
{
        
"
now
"
:
"
just
elo
"
        
"
second
"
:
"
enger
Sekonn
"
        
"
seconds
"
:
"
{
0
}
Sekonnen
"
        
"
minute
"
:
"
enger
Minutt
"
        
"
minutes
"
:
"
{
0
}
Minutten
"
        
"
hour
"
:
"
enger
Stonn
"
        
"
hours
"
:
"
{
0
}
Stonnen
"
        
"
day
"
:
"
engem
Dag
"
        
"
days
"
:
"
{
0
}
Deeg
"
        
"
week
"
:
"
enger
Woch
"
        
"
weeks
"
:
"
{
0
}
Wochen
"
        
"
month
"
:
"
engem
Mount
"
        
"
months
"
:
"
{
0
}
M
int
"
        
"
year
"
:
"
engem
Joer
"
        
"
years
"
:
"
{
0
}
Jahren
"
    
}
    
timeframes_only_distance
=
timeframes
.
copy
(
)
    
timeframes_only_distance
[
"
second
"
]
=
"
eng
Sekonn
"
    
timeframes_only_distance
[
"
minute
"
]
=
"
eng
Minutt
"
    
timeframes_only_distance
[
"
hour
"
]
=
"
eng
Stonn
"
    
timeframes_only_distance
[
"
day
"
]
=
"
een
Dag
"
    
timeframes_only_distance
[
"
days
"
]
=
"
{
0
}
Deeg
"
    
timeframes_only_distance
[
"
week
"
]
=
"
eng
Woch
"
    
timeframes_only_distance
[
"
month
"
]
=
"
ee
Mount
"
    
timeframes_only_distance
[
"
months
"
]
=
"
{
0
}
M
int
"
    
timeframes_only_distance
[
"
year
"
]
=
"
ee
Joer
"
    
timeframes_only_distance
[
"
years
"
]
=
"
{
0
}
Joer
"
    
month_names
=
[
        
"
"
        
"
Januar
"
        
"
Februar
"
        
"
M
erz
"
        
"
Abr
ll
"
        
"
Mee
"
        
"
Juni
"
        
"
Juli
"
        
"
August
"
        
"
September
"
        
"
Oktouber
"
        
"
November
"
        
"
Dezember
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
Jan
"
        
"
Feb
"
        
"
M
e
"
        
"
Abr
"
        
"
Mee
"
        
"
Jun
"
        
"
Jul
"
        
"
Aug
"
        
"
Sep
"
        
"
Okt
"
        
"
Nov
"
        
"
Dez
"
    
]
    
day_names
=
[
        
"
"
        
"
M
indeg
"
        
"
D
nschdeg
"
        
"
M
ttwoch
"
        
"
Donneschdeg
"
        
"
Freideg
"
        
"
Samschdeg
"
        
"
Sonndeg
"
    
]
    
day_abbreviations
=
[
"
"
"
M
i
"
"
D
n
"
"
M
t
"
"
Don
"
"
Fre
"
"
Sam
"
"
Son
"
]
    
def
_ordinal_number
(
self
n
:
int
)
-
>
str
:
        
return
f
"
{
n
}
.
"
    
def
describe
(
        
self
        
timeframe
:
TimeFrameLiteral
        
delta
:
Union
[
int
float
]
=
0
        
only_distance
:
bool
=
False
    
)
-
>
str
:
        
if
not
only_distance
:
            
return
super
(
)
.
describe
(
timeframe
delta
only_distance
)
        
humanized
:
str
=
self
.
timeframes_only_distance
[
timeframe
]
.
format
(
            
trunc
(
abs
(
delta
)
)
        
)
        
return
humanized
class
ZuluLocale
(
Locale
)
:
    
names
=
[
"
zu
"
"
zu
-
za
"
]
    
past
=
"
{
0
}
edlule
"
    
future
=
"
{
0
}
"
    
and_word
=
"
futhi
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
Mapping
[
str
str
]
str
]
]
]
=
{
        
"
now
"
:
"
manje
"
        
"
second
"
:
{
"
past
"
:
"
umzuzwana
"
"
future
"
:
"
ngomzuzwana
"
}
        
"
seconds
"
:
{
"
past
"
:
"
{
0
}
imizuzwana
"
"
future
"
:
"
{
0
}
ngemizuzwana
"
}
        
"
minute
"
:
{
"
past
"
:
"
umzuzu
"
"
future
"
:
"
ngomzuzu
"
}
        
"
minutes
"
:
{
"
past
"
:
"
{
0
}
imizuzu
"
"
future
"
:
"
{
0
}
ngemizuzu
"
}
        
"
hour
"
:
{
"
past
"
:
"
ihora
"
"
future
"
:
"
ngehora
"
}
        
"
hours
"
:
{
"
past
"
:
"
{
0
}
amahora
"
"
future
"
:
"
{
0
}
emahoreni
"
}
        
"
day
"
:
{
"
past
"
:
"
usuku
"
"
future
"
:
"
ngosuku
"
}
        
"
days
"
:
{
"
past
"
:
"
{
0
}
izinsuku
"
"
future
"
:
"
{
0
}
ezinsukwini
"
}
        
"
week
"
:
{
"
past
"
:
"
isonto
"
"
future
"
:
"
ngesonto
"
}
        
"
weeks
"
:
{
"
past
"
:
"
{
0
}
amasonto
"
"
future
"
:
"
{
0
}
emasontweni
"
}
        
"
month
"
:
{
"
past
"
:
"
inyanga
"
"
future
"
:
"
ngenyanga
"
}
        
"
months
"
:
{
"
past
"
:
"
{
0
}
izinyanga
"
"
future
"
:
"
{
0
}
ezinyangeni
"
}
        
"
year
"
:
{
"
past
"
:
"
unyaka
"
"
future
"
:
"
ngonyak
"
}
        
"
years
"
:
{
"
past
"
:
"
{
0
}
iminyaka
"
"
future
"
:
"
{
0
}
eminyakeni
"
}
    
}
    
def
_format_timeframe
(
self
timeframe
:
TimeFrameLiteral
delta
:
int
)
-
>
str
:
        
"
"
"
Zulu
aware
time
frame
format
function
takes
into
account
        
the
differences
between
past
and
future
forms
.
"
"
"
        
abs_delta
=
abs
(
delta
)
        
form
=
self
.
timeframes
[
timeframe
]
        
if
isinstance
(
form
str
)
:
            
return
form
.
format
(
abs_delta
)
        
if
delta
>
0
:
            
key
=
"
future
"
        
else
:
            
key
=
"
past
"
        
form
=
form
[
key
]
        
return
form
.
format
(
abs_delta
)
    
month_names
=
[
        
"
"
        
"
uMasingane
"
        
"
uNhlolanja
"
        
"
uNdasa
"
        
"
UMbasa
"
        
"
UNhlaba
"
        
"
UNhlangulana
"
        
"
uNtulikazi
"
        
"
UNcwaba
"
        
"
uMandulo
"
        
"
uMfumfu
"
        
"
uLwezi
"
        
"
uZibandlela
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
uMasingane
"
        
"
uNhlolanja
"
        
"
uNdasa
"
        
"
UMbasa
"
        
"
UNhlaba
"
        
"
UNhlangulana
"
        
"
uNtulikazi
"
        
"
UNcwaba
"
        
"
uMandulo
"
        
"
uMfumfu
"
        
"
uLwezi
"
        
"
uZibandlela
"
    
]
    
day_names
=
[
        
"
"
        
"
uMsombuluko
"
        
"
uLwesibili
"
        
"
uLwesithathu
"
        
"
uLwesine
"
        
"
uLwesihlanu
"
        
"
uMgqibelo
"
        
"
iSonto
"
    
]
    
day_abbreviations
=
[
        
"
"
        
"
uMsombuluko
"
        
"
uLwesibili
"
        
"
uLwesithathu
"
        
"
uLwesine
"
        
"
uLwesihlanu
"
        
"
uMgqibelo
"
        
"
iSonto
"
    
]
class
TamilLocale
(
Locale
)
:
    
names
=
[
"
ta
"
"
ta
-
in
"
"
ta
-
lk
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
"
        
"
days
"
:
"
{
0
}
"
        
"
week
"
:
"
"
        
"
weeks
"
:
"
{
0
}
"
        
"
month
"
:
"
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
"
        
"
years
"
:
"
{
0
}
"
    
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
def
_ordinal_number
(
self
n
:
int
)
-
>
str
:
        
if
n
=
=
1
:
            
return
f
"
{
n
}
"
        
elif
n
>
=
0
:
            
return
f
"
{
n
}
"
        
else
:
            
return
"
"
class
AlbanianLocale
(
Locale
)
:
    
names
=
[
"
sq
"
"
sq
-
al
"
]
    
past
=
"
{
0
}
m
par
"
    
future
=
"
n
{
0
}
"
    
and_word
=
"
dhe
"
    
timeframes
=
{
        
"
now
"
:
"
tani
"
        
"
second
"
:
"
sekond
"
        
"
seconds
"
:
"
{
0
}
sekonda
"
        
"
minute
"
:
"
minut
"
        
"
minutes
"
:
"
{
0
}
minuta
"
        
"
hour
"
:
"
or
"
        
"
hours
"
:
"
{
0
}
or
"
        
"
day
"
:
"
dit
"
        
"
days
"
:
"
{
0
}
dit
"
        
"
week
"
:
"
jav
"
        
"
weeks
"
:
"
{
0
}
jav
"
        
"
month
"
:
"
muaj
"
        
"
months
"
:
"
{
0
}
muaj
"
        
"
year
"
:
"
vit
"
        
"
years
"
:
"
{
0
}
vjet
"
    
}
    
month_names
=
[
        
"
"
        
"
janar
"
        
"
shkurt
"
        
"
mars
"
        
"
prill
"
        
"
maj
"
        
"
qershor
"
        
"
korrik
"
        
"
gusht
"
        
"
shtator
"
        
"
tetor
"
        
"
n
ntor
"
        
"
dhjetor
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
jan
"
        
"
shk
"
        
"
mar
"
        
"
pri
"
        
"
maj
"
        
"
qer
"
        
"
korr
"
        
"
gush
"
        
"
sht
"
        
"
tet
"
        
"
n
n
"
        
"
dhj
"
    
]
    
day_names
=
[
        
"
"
        
"
e
h
n
"
        
"
e
mart
"
        
"
e
m
rkur
"
        
"
e
enjte
"
        
"
e
premte
"
        
"
e
shtun
"
        
"
e
diel
"
    
]
    
day_abbreviations
=
[
        
"
"
        
"
h
n
"
        
"
mar
"
        
"
m
r
"
        
"
enj
"
        
"
pre
"
        
"
sht
"
        
"
die
"
    
]
class
GeorgianLocale
(
Locale
)
:
    
names
=
[
"
ka
"
"
ka
-
ge
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
and_word
=
"
"
    
timeframes
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
"
        
"
days
"
:
"
{
0
}
"
        
"
week
"
:
"
"
        
"
weeks
"
:
"
{
0
}
"
        
"
month
"
:
"
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
"
        
"
years
"
:
"
{
0
}
"
    
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
class
SinhalaLocale
(
Locale
)
:
    
names
=
[
"
si
"
"
si
-
lk
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
and_word
=
"
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
Mapping
[
str
str
]
str
]
]
]
=
{
        
"
now
"
:
"
"
        
"
second
"
:
{
            
"
past
"
:
"
"
            
"
future
"
:
"
"
        
}
        
"
seconds
"
:
{
            
"
past
"
:
"
{
0
}
"
            
"
future
"
:
"
{
0
}
"
        
}
        
"
minute
"
:
{
            
"
past
"
:
"
"
            
"
future
"
:
"
"
        
}
        
"
minutes
"
:
{
            
"
past
"
:
"
{
0
}
"
            
"
future
"
:
"
{
0
}
"
        
}
        
"
hour
"
:
{
"
past
"
:
"
"
"
future
"
:
"
"
}
        
"
hours
"
:
{
            
"
past
"
:
"
{
0
}
"
            
"
future
"
:
"
{
0
}
"
        
}
        
"
day
"
:
{
"
past
"
:
"
"
"
future
"
:
"
"
}
        
"
days
"
:
{
            
"
past
"
:
"
{
0
}
"
            
"
future
"
:
"
{
0
}
"
        
}
        
"
week
"
:
{
"
past
"
:
"
"
"
future
"
:
"
"
}
        
"
weeks
"
:
{
            
"
past
"
:
"
{
0
}
"
            
"
future
"
:
"
{
0
}
"
        
}
        
"
month
"
:
{
"
past
"
:
"
"
"
future
"
:
"
"
}
        
"
months
"
:
{
            
"
past
"
:
"
{
0
}
"
            
"
future
"
:
"
{
0
}
"
        
}
        
"
year
"
:
{
"
past
"
:
"
"
"
future
"
:
"
"
}
        
"
years
"
:
{
            
"
past
"
:
"
{
0
}
"
            
"
future
"
:
"
{
0
}
"
        
}
    
}
    
timeframes_only_distance
=
{
}
    
timeframes_only_distance
[
"
second
"
]
=
"
"
    
timeframes_only_distance
[
"
seconds
"
]
=
"
{
0
}
"
    
timeframes_only_distance
[
"
minute
"
]
=
"
"
    
timeframes_only_distance
[
"
minutes
"
]
=
"
{
0
}
"
    
timeframes_only_distance
[
"
hour
"
]
=
"
"
    
timeframes_only_distance
[
"
hours
"
]
=
"
{
0
}
"
    
timeframes_only_distance
[
"
day
"
]
=
"
"
    
timeframes_only_distance
[
"
days
"
]
=
"
{
0
}
"
    
timeframes_only_distance
[
"
week
"
]
=
"
"
    
timeframes_only_distance
[
"
weeks
"
]
=
"
{
0
}
"
    
timeframes_only_distance
[
"
month
"
]
=
"
"
    
timeframes_only_distance
[
"
months
"
]
=
"
{
0
}
"
    
timeframes_only_distance
[
"
year
"
]
=
"
"
    
timeframes_only_distance
[
"
years
"
]
=
"
{
0
}
"
    
def
_format_timeframe
(
self
timeframe
:
TimeFrameLiteral
delta
:
int
)
-
>
str
:
        
"
"
"
        
Sinhala
awares
time
frame
format
function
takes
into
account
        
the
differences
between
general
past
and
future
forms
(
three
different
suffixes
)
.
        
"
"
"
        
abs_delta
=
abs
(
delta
)
        
form
=
self
.
timeframes
[
timeframe
]
        
if
isinstance
(
form
str
)
:
            
return
form
.
format
(
abs_delta
)
        
if
delta
>
0
:
            
key
=
"
future
"
        
else
:
            
key
=
"
past
"
        
form
=
form
[
key
]
        
return
form
.
format
(
abs_delta
)
    
def
describe
(
        
self
        
timeframe
:
TimeFrameLiteral
        
delta
:
Union
[
float
int
]
=
1
        
only_distance
:
bool
=
False
    
)
-
>
str
:
        
"
"
"
Describes
a
delta
within
a
timeframe
in
plain
language
.
        
:
param
timeframe
:
a
string
representing
a
timeframe
.
        
:
param
delta
:
a
quantity
representing
a
delta
in
a
timeframe
.
        
:
param
only_distance
:
return
only
distance
eg
:
"
11
seconds
"
without
"
in
"
or
"
ago
"
keywords
        
"
"
"
        
if
not
only_distance
:
            
return
super
(
)
.
describe
(
timeframe
delta
only_distance
)
        
humanized
=
self
.
timeframes_only_distance
[
timeframe
]
.
format
(
trunc
(
abs
(
delta
)
)
)
        
return
humanized
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
class
UrduLocale
(
Locale
)
:
    
names
=
[
"
ur
"
"
ur
-
pk
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
and_word
=
"
"
    
timeframes
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
"
        
"
days
"
:
"
{
0
}
"
        
"
week
"
:
"
"
        
"
weeks
"
:
"
{
0
}
"
        
"
month
"
:
"
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
"
        
"
years
"
:
"
{
0
}
"
    
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
class
KazakhLocale
(
Locale
)
:
    
names
=
[
"
kk
"
"
kk
-
kz
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
timeframes
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
"
        
"
days
"
:
"
{
0
}
"
        
"
week
"
:
"
"
        
"
weeks
"
:
"
{
0
}
"
        
"
month
"
:
"
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
"
        
"
years
"
:
"
{
0
}
"
    
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
class
AmharicLocale
(
Locale
)
:
    
names
=
[
"
am
"
"
am
-
et
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
and_word
=
"
"
    
timeframes
:
ClassVar
[
Mapping
[
TimeFrameLiteral
Union
[
Mapping
[
str
str
]
str
]
]
]
=
{
        
"
now
"
:
"
"
        
"
second
"
:
{
            
"
past
"
:
"
"
            
"
future
"
:
"
"
        
}
        
"
seconds
"
:
{
            
"
past
"
:
"
{
0
}
"
            
"
future
"
:
"
{
0
}
"
        
}
        
"
minute
"
:
{
            
"
past
"
:
"
"
            
"
future
"
:
"
"
        
}
        
"
minutes
"
:
{
            
"
past
"
:
"
{
0
}
"
            
"
future
"
:
"
{
0
}
"
        
}
        
"
hour
"
:
{
            
"
past
"
:
"
"
            
"
future
"
:
"
"
        
}
        
"
hours
"
:
{
            
"
past
"
:
"
{
0
}
"
            
"
future
"
:
"
{
0
}
"
        
}
        
"
day
"
:
{
            
"
past
"
:
"
"
            
"
future
"
:
"
"
        
}
        
"
days
"
:
{
            
"
past
"
:
"
{
0
}
"
            
"
future
"
:
"
{
0
}
"
        
}
        
"
week
"
:
{
            
"
past
"
:
"
"
            
"
future
"
:
"
"
        
}
        
"
weeks
"
:
{
            
"
past
"
:
"
{
0
}
"
            
"
future
"
:
"
{
0
}
"
        
}
        
"
month
"
:
{
            
"
past
"
:
"
"
            
"
future
"
:
"
"
        
}
        
"
months
"
:
{
            
"
past
"
:
"
{
0
}
"
            
"
future
"
:
"
{
0
}
"
        
}
        
"
year
"
:
{
            
"
past
"
:
"
"
            
"
future
"
:
"
"
        
}
        
"
years
"
:
{
            
"
past
"
:
"
{
0
}
"
            
"
future
"
:
"
{
0
}
"
        
}
    
}
    
timeframes_only_distance
=
{
        
"
second
"
:
"
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
"
        
"
days
"
:
"
{
0
}
"
        
"
week
"
:
"
"
        
"
weeks
"
:
"
{
0
}
"
        
"
month
"
:
"
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
"
        
"
years
"
:
"
{
0
}
"
    
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
"
]
    
def
_ordinal_number
(
self
n
:
int
)
-
>
str
:
        
return
f
"
{
n
}
"
    
def
_format_timeframe
(
self
timeframe
:
TimeFrameLiteral
delta
:
int
)
-
>
str
:
        
"
"
"
        
Amharic
awares
time
frame
format
function
takes
into
account
        
the
differences
between
general
past
and
future
forms
(
three
different
suffixes
)
.
        
"
"
"
        
abs_delta
=
abs
(
delta
)
        
form
=
self
.
timeframes
[
timeframe
]
        
if
isinstance
(
form
str
)
:
            
return
form
.
format
(
abs_delta
)
        
if
delta
>
0
:
            
key
=
"
future
"
        
else
:
            
key
=
"
past
"
        
form
=
form
[
key
]
        
return
form
.
format
(
abs_delta
)
    
def
describe
(
        
self
        
timeframe
:
TimeFrameLiteral
        
delta
:
Union
[
float
int
]
=
1
        
only_distance
:
bool
=
False
    
)
-
>
str
:
        
"
"
"
Describes
a
delta
within
a
timeframe
in
plain
language
.
        
:
param
timeframe
:
a
string
representing
a
timeframe
.
        
:
param
delta
:
a
quantity
representing
a
delta
in
a
timeframe
.
        
:
param
only_distance
:
return
only
distance
eg
:
"
11
seconds
"
without
"
in
"
or
"
ago
"
keywords
        
"
"
"
        
if
not
only_distance
:
            
return
super
(
)
.
describe
(
timeframe
delta
only_distance
)
        
humanized
=
self
.
timeframes_only_distance
[
timeframe
]
.
format
(
trunc
(
abs
(
delta
)
)
)
        
return
humanized
class
ArmenianLocale
(
Locale
)
:
    
names
=
[
"
hy
"
"
hy
-
am
"
]
    
past
=
"
{
0
}
"
    
future
=
"
{
0
}
"
    
and_word
=
"
"
    
timeframes
=
{
        
"
now
"
:
"
"
        
"
second
"
:
"
"
        
"
seconds
"
:
"
{
0
}
"
        
"
minute
"
:
"
"
        
"
minutes
"
:
"
{
0
}
"
        
"
hour
"
:
"
"
        
"
hours
"
:
"
{
0
}
"
        
"
day
"
:
"
"
        
"
days
"
:
"
{
0
}
"
        
"
month
"
:
"
"
        
"
months
"
:
"
{
0
}
"
        
"
year
"
:
"
"
        
"
years
"
:
"
{
0
}
"
        
"
week
"
:
"
"
        
"
weeks
"
:
"
{
0
}
"
    
}
    
meridians
=
{
        
"
am
"
:
"
"
        
"
pm
"
:
"
.
.
"
        
"
AM
"
:
"
"
        
"
PM
"
:
"
.
.
"
    
}
    
month_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_names
=
[
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
        
"
"
    
]
    
day_abbreviations
=
[
        
"
"
        
"
.
"
        
"
.
"
        
"
.
"
        
"
.
"
        
"
.
"
        
"
.
"
        
"
.
"
    
]
class
UzbekLocale
(
Locale
)
:
    
names
=
[
"
uz
"
"
uz
-
uz
"
]
    
past
=
"
{
0
}
dan
avval
"
    
future
=
"
{
0
}
dan
keyin
"
    
timeframes
=
{
        
"
now
"
:
"
hozir
"
        
"
second
"
:
"
bir
soniya
"
        
"
seconds
"
:
"
{
0
}
soniya
"
        
"
minute
"
:
"
bir
daqiqa
"
        
"
minutes
"
:
"
{
0
}
daqiqa
"
        
"
hour
"
:
"
bir
soat
"
        
"
hours
"
:
"
{
0
}
soat
"
        
"
day
"
:
"
bir
kun
"
        
"
days
"
:
"
{
0
}
kun
"
        
"
week
"
:
"
bir
hafta
"
        
"
weeks
"
:
"
{
0
}
hafta
"
        
"
month
"
:
"
bir
oy
"
        
"
months
"
:
"
{
0
}
oy
"
        
"
year
"
:
"
bir
yil
"
        
"
years
"
:
"
{
0
}
yil
"
    
}
    
month_names
=
[
        
"
"
        
"
Yanvar
"
        
"
Fevral
"
        
"
Mart
"
        
"
Aprel
"
        
"
May
"
        
"
Iyun
"
        
"
Iyul
"
        
"
Avgust
"
        
"
Sentyabr
"
        
"
Oktyabr
"
        
"
Noyabr
"
        
"
Dekabr
"
    
]
    
month_abbreviations
=
[
        
"
"
        
"
Yan
"
        
"
Fev
"
        
"
Mar
"
        
"
Apr
"
        
"
May
"
        
"
Iyn
"
        
"
Iyl
"
        
"
Avg
"
        
"
Sen
"
        
"
Okt
"
        
"
Noy
"
        
"
Dek
"
    
]
    
day_names
=
[
        
"
"
        
"
Dushanba
"
        
"
Seshanba
"
        
"
Chorshanba
"
        
"
Payshanba
"
        
"
Juma
"
        
"
Shanba
"
        
"
Yakshanba
"
    
]
    
day_abbreviations
=
[
"
"
"
Dush
"
"
Sesh
"
"
Chor
"
"
Pay
"
"
Jum
"
"
Shan
"
"
Yak
"
]
