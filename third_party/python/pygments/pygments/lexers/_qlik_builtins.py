"
"
"
    
pygments
.
lexers
.
_qlik_builtins
    
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
    
Qlik
builtins
.
    
:
copyright
:
Copyright
2006
-
2025
by
the
Pygments
team
see
AUTHORS
.
    
:
license
:
BSD
see
LICENSE
for
details
.
"
"
"
OPERATORS_LIST
=
{
    
"
words
"
:
[
        
"
bitnot
"
        
"
bitand
"
        
"
bitor
"
        
"
bitxor
"
        
"
and
"
        
"
or
"
        
"
not
"
        
"
xor
"
        
"
precedes
"
        
"
follows
"
        
"
like
"
    
]
    
"
symbols
"
:
[
        
"
>
>
"
        
"
<
<
"
        
"
+
"
        
"
-
"
        
"
/
"
        
"
*
"
        
"
<
"
        
"
<
=
"
        
"
>
"
        
"
>
=
"
        
"
=
"
        
"
<
>
"
        
"
&
"
    
]
}
STATEMENT_LIST
=
[
    
"
for
"
    
"
each
"
    
"
in
"
    
"
next
"
    
"
do
"
    
"
while
"
    
"
until
"
    
"
unless
"
    
"
loop
"
    
"
return
"
    
"
switch
"
    
"
case
"
    
"
default
"
    
"
if
"
    
"
else
"
    
"
endif
"
    
"
then
"
    
"
end
"
    
"
exit
"
    
"
script
"
    
"
switch
"
    
"
Add
"
    
"
Buffer
"
    
"
Concatenate
"
    
"
Crosstable
"
    
"
First
"
    
"
Generic
"
    
"
Hierarchy
"
    
"
HierarchyBelongsTo
"
    
"
Inner
"
    
"
IntervalMatch
"
    
"
Join
"
    
"
Keep
"
    
"
Left
"
    
"
Mapping
"
    
"
Merge
"
    
"
NoConcatenate
"
    
"
Outer
"
    
"
Partial
reload
"
    
"
Replace
"
    
"
Right
"
    
"
Sample
"
    
"
Semantic
"
    
"
Unless
"
    
"
When
"
    
"
Alias
"
    
"
as
"
    
"
AutoNumber
"
    
"
Binary
"
    
"
Comment
field
"
    
"
Comment
fields
"
    
"
using
"
    
"
with
"
    
"
Comment
table
"
    
"
Comment
tables
"
    
"
Connect
"
    
"
ODBC
"
    
"
OLEBD
"
    
"
CUSTOM
"
    
"
LIB
"
    
"
Declare
"
    
"
Derive
"
    
"
From
"
    
"
explicit
"
    
"
implicit
"
    
"
Direct
Query
"
    
"
dimension
"
    
"
measure
"
    
"
Directory
"
    
"
Disconnect
"
    
"
Drop
field
"
    
"
Drop
fields
"
    
"
Drop
table
"
    
"
Drop
tables
"
    
"
Execute
"
    
"
FlushLog
"
    
"
Force
"
    
"
capitalization
"
    
"
case
upper
"
    
"
case
lower
"
    
"
case
mixed
"
    
"
Load
"
    
"
distinct
"
    
"
from
"
    
"
inline
"
    
"
resident
"
    
"
from_field
"
    
"
autogenerate
"
    
"
extension
"
    
"
where
"
    
"
group
by
"
    
"
order
by
"
    
"
asc
"
    
"
desc
"
    
"
Let
"
    
"
Loosen
Table
"
    
"
Map
"
    
"
NullAsNull
"
    
"
NullAsValue
"
    
"
Qualify
"
    
"
Rem
"
    
"
Rename
field
"
    
"
Rename
fields
"
    
"
Rename
table
"
    
"
Rename
tables
"
    
"
Search
"
    
"
include
"
    
"
exclude
"
    
"
Section
"
    
"
access
"
    
"
application
"
    
"
Select
"
    
"
Set
"
    
"
Sleep
"
    
"
SQL
"
    
"
SQLColumns
"
    
"
SQLTables
"
    
"
SQLTypes
"
    
"
Star
"
    
"
Store
"
    
"
Tag
"
    
"
Trace
"
    
"
Unmap
"
    
"
Unqualify
"
    
"
Untag
"
    
"
total
"
]
SCRIPT_FUNCTIONS
=
[
    
"
FirstSortedValue
"
    
"
Max
"
    
"
Min
"
    
"
Mode
"
    
"
Only
"
    
"
Sum
"
    
"
Count
"
    
"
MissingCount
"
    
"
NullCount
"
    
"
NumericCount
"
    
"
TextCount
"
    
"
IRR
"
    
"
XIRR
"
    
"
NPV
"
    
"
XNPV
"
    
"
Avg
"
    
"
Correl
"
    
"
Fractile
"
    
"
FractileExc
"
    
"
Kurtosis
"
    
"
LINEST_B
"
"
LINEST_df
"
    
"
LINEST_f
"
    
"
LINEST_m
"
    
"
LINEST_r2
"
    
"
LINEST_seb
"
    
"
LINEST_sem
"
    
"
LINEST_sey
"
    
"
LINEST_ssreg
"
    
"
Linest_ssresid
"
    
"
Median
"
    
"
Skew
"
    
"
Stdev
"
    
"
Sterr
"
    
"
STEYX
"
    
"
Chi2Test_chi2
"
    
"
Chi2Test_df
"
    
"
Chi2Test_p
"
    
"
ttest_conf
"
    
"
ttest_df
"
    
"
ttest_dif
"
    
"
ttest_lower
"
    
"
ttest_sig
"
    
"
ttest_sterr
"
    
"
ttest_t
"
    
"
ttest_upper
"
    
"
ttestw_conf
"
    
"
ttestw_df
"
    
"
ttestw_dif
"
    
"
ttestw_lower
"
    
"
ttestw_sig
"
    
"
ttestw_sterr
"
    
"
ttestw_t
"
    
"
ttestw_upper
"
    
"
ttest1_conf
"
    
"
ttest1_df
"
    
"
ttest1_dif
"
    
"
ttest1_lower
"
    
"
ttest1_sig
"
    
"
ttest1_sterr
"
    
"
ttest1_t
"
    
"
ttest1_upper
"
    
"
ttest1w_conf
"
    
"
ttest1w_df
"
    
"
ttest1w_dif
"
    
"
ttest1w_lower
"
    
"
ttest1w_sig
"
    
"
ttest1w_sterr
"
    
"
ttest1w_t
"
    
"
ttest1w_upper
"
    
"
ztest_conf
"
    
"
ztest_dif
"
    
"
ztest_sig
"
    
"
ztest_sterr
"
    
"
ztest_z
"
    
"
ztest_lower
"
    
"
ztest_upper
"
    
"
ztestw_conf
"
    
"
ztestw_dif
"
    
"
ztestw_lower
"
    
"
ztestw_sig
"
    
"
ztestw_sterr
"
    
"
ztestw_upper
"
    
"
ztestw_z
"
    
"
Concat
"
    
"
FirstValue
"
    
"
LastValue
"
    
"
MaxString
"
    
"
MinString
"
    
"
ValueList
"
    
"
ValueLoop
"
    
"
ARGB
"
    
"
HSL
"
    
"
RGB
"
    
"
Color
"
    
"
Colormix1
"
    
"
Colormix2
"
    
"
SysColor
"
    
"
ColorMapHue
"
    
"
ColorMapJet
"
    
"
black
"
    
"
blue
"
    
"
brown
"
    
"
cyan
"
    
"
darkgray
"
    
"
green
"
    
"
lightblue
"
    
"
lightcyan
"
    
"
lightgray
"
    
"
lightgreen
"
    
"
lightmagenta
"
    
"
lightred
"
    
"
magenta
"
    
"
red
"
    
"
white
"
    
"
yellow
"
    
"
alt
"
    
"
class
"
    
"
coalesce
"
    
"
if
"
    
"
match
"
    
"
mixmatch
"
    
"
pick
"
    
"
wildmatch
"
    
"
autonumber
"
    
"
autonumberhash128
"
    
"
autonumberhash256
"
    
"
IterNo
"
    
"
RecNo
"
    
"
RowNo
"
    
"
second
"
    
"
minute
"
    
"
hour
"
    
"
day
"
    
"
week
"
    
"
month
"
    
"
year
"
    
"
weekyear
"
    
"
weekday
"
    
"
now
"
    
"
today
"
    
"
LocalTime
"
    
"
makedate
"
    
"
makeweekdate
"
    
"
maketime
"
    
"
AddMonths
"
    
"
AddYears
"
    
"
yeartodate
"
    
"
timezone
"
    
"
GMT
"
    
"
UTC
"
    
"
daylightsaving
"
    
"
converttolocaltime
"
    
"
setdateyear
"
    
"
setdateyearmonth
"
    
"
inyear
"
    
"
inyeartodate
"
    
"
inquarter
"
    
"
inquartertodate
"
    
"
inmonth
"
    
"
inmonthtodate
"
    
"
inmonths
"
    
"
inmonthstodate
"
    
"
inweek
"
    
"
inweektodate
"
    
"
inlunarweek
"
    
"
inlunarweektodate
"
    
"
inday
"
    
"
indaytotime
"
    
"
yearstart
"
    
"
yearend
"
    
"
yearname
"
    
"
quarterstart
"
    
"
quarterend
"
    
"
quartername
"
    
"
monthstart
"
    
"
monthend
"
    
"
monthname
"
    
"
monthsstart
"
    
"
monthsend
"
    
"
monthsname
"
    
"
weekstart
"
    
"
weekend
"
    
"
weekname
"
    
"
lunarweekstart
"
    
"
lunarweekend
"
    
"
lunarweekname
"
    
"
daystart
"
    
"
dayend
"
    
"
dayname
"
    
"
age
"
    
"
networkdays
"
    
"
firstworkdate
"
    
"
lastworkdate
"
    
"
daynumberofyear
"
    
"
daynumberofquarter
"
    
"
exp
"
    
"
log
"
    
"
log10
"
    
"
pow
"
    
"
sqr
"
    
"
sqrt
"
    
"
GetAlternativeCount
"
    
"
GetExcludedCount
"
    
"
GetNotSelectedCount
"
    
"
GetPossibleCount
"
    
"
GetSelectedCount
"
    
"
GetCurrentSelections
"
    
"
GetFieldSelections
"
    
"
GetObjectDimension
"
    
"
GetObjectField
"
    
"
GetObjectMeasure
"
    
"
Attribute
"
    
"
ConnectString
"
    
"
FileBaseName
"
    
"
FileDir
"
    
"
FileExtension
"
    
"
FileName
"
    
"
FilePath
"
    
"
FileSize
"
    
"
FileTime
"
    
"
GetFolderPath
"
    
"
QvdCreateTime
"
    
"
QvdFieldName
"
    
"
QvdNoOfFields
"
    
"
QvdNoOfRecords
"
    
"
QvdTableName
"
    
"
FV
"
    
"
nPer
"
    
"
Pmt
"
    
"
PV
"
    
"
Rate
"
    
"
ApplyCodepage
"
    
"
Date
"
    
"
Dual
"
    
"
Interval
"
    
"
Money
"
    
"
Num
"
    
"
Time
"
    
"
Timestamp
"
    
"
bitcount
"
    
"
div
"
    
"
fabs
"
    
"
fact
"
    
"
frac
"
    
"
sign
"
    
"
combin
"
    
"
permut
"
    
"
fmod
"
    
"
mod
"
    
"
even
"
    
"
odd
"
    
"
ceil
"
    
"
floor
"
    
"
round
"
    
"
GeoAggrGeometry
"
    
"
GeoBoundingBox
"
    
"
GeoCountVertex
"
    
"
GeoInvProjectGeometry
"
    
"
GeoProjectGeometry
"
    
"
GeoReduceGeometry
"
    
"
GeoGetBoundingBox
"
    
"
GeoGetPolygonCenter
"
    
"
GeoMakePoint
"
    
"
GeoProject
"
    
"
Date
#
"
    
"
Interval
#
"
    
"
Money
#
"
    
"
Num
#
"
    
"
Text
"
    
"
Time
#
"
    
"
Timestamp
#
"
    
"
FieldIndex
"
    
"
FieldValue
"
    
"
FieldValueCount
"
    
"
Exists
"
    
"
LookUp
"
    
"
Peek
"
    
"
Previous
"
    
"
IsNum
"
    
"
IsText
"
    
"
ApplyMap
"
    
"
MapSubstring
"
    
"
e
"
    
"
false
"
    
"
pi
"
    
"
rand
"
    
"
true
"
    
"
EmptyIsNull
"
    
"
IsNull
"
    
"
Null
"
    
"
RangeMax
"
    
"
RangeMaxString
"
    
"
RangeMin
"
    
"
RangeMinString
"
    
"
RangeMode
"
    
"
RangeOnly
"
    
"
RangeSum
"
    
"
RangeCount
"
    
"
RangeMissingCount
"
    
"
RangeNullCount
"
    
"
RangeNumericCount
"
    
"
RangeTextCount
"
    
"
RangeAvg
"
    
"
RangeCorrel
"
    
"
RangeFractile
"
    
"
RangeKurtosis
"
    
"
RangeSkew
"
    
"
RangeStdev
"
    
"
RangeIRR
"
    
"
RangeNPV
"
    
"
RangeXIRR
"
    
"
RangeXNPV
"
    
"
CHIDIST
"
    
"
CHIINV
"
    
"
NORMDIST
"
    
"
NORMINV
"
    
"
TDIST
"
    
"
TINV
"
    
"
FDIST
"
    
"
FINV
"
    
"
Capitalize
"
    
"
Chr
"
    
"
Evaluate
"
    
"
FindOneOf
"
    
"
Hash128
"
    
"
Hash160
"
    
"
Hash256
"
    
"
Index
"
    
"
KeepChar
"
    
"
Left
"
    
"
Len
"
    
"
LevenshteinDist
"
    
"
Lower
"
    
"
LTrim
"
    
"
Mid
"
    
"
Ord
"
    
"
PurgeChar
"
    
"
Repeat
"
    
"
Replace
"
    
"
Right
"
    
"
RTrim
"
    
"
SubField
"
    
"
SubStringCount
"
    
"
TextBetween
"
    
"
Trim
"
    
"
Upper
"
    
"
Author
"
    
"
ClientPlatform
"
    
"
ComputerName
"
    
"
DocumentName
"
    
"
DocumentPath
"
    
"
DocumentTitle
"
    
"
EngineVersion
"
    
"
GetCollationLocale
"
    
"
GetObjectField
"
    
"
GetRegistryString
"
    
"
IsPartialReload
"
    
"
OSUser
"
    
"
ProductVersion
"
    
"
ReloadTime
"
    
"
StateName
"
    
"
FieldName
"
    
"
FieldNumber
"
    
"
NoOfFields
"
    
"
NoOfRows
"
    
"
NoOfTables
"
    
"
TableName
"
    
"
TableNumber
"
]
CONSTANT_LIST
=
[
    
"
floppy
"
    
"
cd
"
    
"
include
"
    
"
must_include
"
    
"
hideprefix
"
    
"
hidesuffix
"
    
"
qvpath
"
    
"
qvroot
"
    
"
QvWorkPath
"
    
"
QvWorkRoot
"
    
"
StripComments
"
    
"
Verbatim
"
    
"
OpenUrlTimeout
"
    
"
WinPath
"
    
"
WinRoot
"
    
"
CollationLocale
"
    
"
CreateSearchIndexOnReload
"
    
"
NullDisplay
"
    
"
NullInterpret
"
    
"
NullValue
"
    
"
OtherSymbol
"
    
"
MoneyDecimalSep
"
    
"
MoneyFormat
"
    
"
MoneyThousandSep
"
    
"
DecimalSep
"
    
"
ThousandSep
"
    
"
NumericalAbbreviation
"
    
"
DateFormat
"
    
"
TimeFormat
"
    
"
TimestampFormat
"
    
"
MonthNames
"
    
"
LongMonthNames
"
    
"
DayNames
"
    
"
LongDayNames
"
    
"
FirstWeekDay
"
    
"
BrokenWeeks
"
    
"
ReferenceDay
"
    
"
FirstMonthOfYear
"
    
"
errormode
"
    
"
scripterror
"
    
"
scripterrorcount
"
    
"
scripterrorlist
"
    
"
null
"
]
