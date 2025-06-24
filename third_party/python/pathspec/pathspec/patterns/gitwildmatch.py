"
"
"
This
module
implements
Git
'
s
wildmatch
pattern
matching
which
itself
is
derived
from
Rsync
'
s
wildmatch
.
Git
uses
wildmatch
for
its
"
.
gitignore
"
files
.
"
"
"
import
re
import
warnings
from
typing
import
(
	
AnyStr
	
Optional
	
Tuple
)
from
.
.
import
util
from
.
.
pattern
import
RegexPattern
_BYTES_ENCODING
=
'
latin1
'
"
"
"
The
encoding
to
use
when
parsing
a
byte
string
pattern
.
"
"
"
_DIR_MARK
=
'
ps_d
'
"
"
"
The
regex
group
name
for
the
directory
marker
.
This
is
only
used
by
:
class
:
GitIgnoreSpec
.
"
"
"
class
GitWildMatchPatternError
(
ValueError
)
:
	
"
"
"
	
The
:
class
:
GitWildMatchPatternError
indicates
an
invalid
git
wild
match
	
pattern
.
	
"
"
"
	
pass
class
GitWildMatchPattern
(
RegexPattern
)
:
	
"
"
"
	
The
:
class
:
GitWildMatchPattern
class
represents
a
compiled
Git
wildmatch
	
pattern
.
	
"
"
"
	
__slots__
=
(
)
	
classmethod
	
def
pattern_to_regex
(
		
cls
		
pattern
:
AnyStr
	
)
-
>
Tuple
[
Optional
[
AnyStr
]
Optional
[
bool
]
]
:
		
"
"
"
		
Convert
the
pattern
into
a
regular
expression
.
		
*
pattern
*
(
:
class
:
str
or
:
class
:
bytes
)
is
the
pattern
to
convert
into
a
		
regular
expression
.
		
Returns
the
uncompiled
regular
expression
(
:
class
:
str
:
class
:
bytes
or
		
:
data
:
None
)
;
and
whether
matched
files
should
be
included
(
:
data
:
True
)
		
excluded
(
:
data
:
False
)
or
if
it
is
a
null
-
operation
(
:
data
:
None
)
.
		
"
"
"
		
if
isinstance
(
pattern
str
)
:
			
return_type
=
str
		
elif
isinstance
(
pattern
bytes
)
:
			
return_type
=
bytes
			
pattern
=
pattern
.
decode
(
_BYTES_ENCODING
)
		
else
:
			
raise
TypeError
(
f
"
pattern
:
{
pattern
!
r
}
is
not
a
unicode
or
byte
string
.
"
)
		
original_pattern
=
pattern
		
if
pattern
.
endswith
(
'
\
\
'
)
:
			
pattern
=
pattern
.
lstrip
(
)
		
else
:
			
pattern
=
pattern
.
strip
(
)
		
if
pattern
.
startswith
(
'
#
'
)
:
			
regex
=
None
			
include
=
None
		
elif
pattern
=
=
'
/
'
:
			
regex
=
None
			
include
=
None
		
elif
pattern
:
			
if
pattern
.
startswith
(
'
!
'
)
:
				
include
=
False
				
pattern
=
pattern
[
1
:
]
			
else
:
				
include
=
True
			
override_regex
=
None
			
pattern_segs
=
pattern
.
split
(
'
/
'
)
			
is_dir_pattern
=
not
pattern_segs
[
-
1
]
			
for
i
in
range
(
len
(
pattern_segs
)
-
1
0
-
1
)
:
				
prev
=
pattern_segs
[
i
-
1
]
				
seg
=
pattern_segs
[
i
]
				
if
prev
=
=
'
*
*
'
and
seg
=
=
'
*
*
'
:
					
del
pattern_segs
[
i
]
			
if
len
(
pattern_segs
)
=
=
2
and
pattern_segs
[
0
]
=
=
'
*
*
'
and
not
pattern_segs
[
1
]
:
				
override_regex
=
f
'
^
.
+
(
?
P
<
{
_DIR_MARK
}
>
/
)
.
*
'
			
if
not
pattern_segs
[
0
]
:
				
del
pattern_segs
[
0
]
			
elif
len
(
pattern_segs
)
=
=
1
or
(
len
(
pattern_segs
)
=
=
2
and
not
pattern_segs
[
1
]
)
:
				
if
pattern_segs
[
0
]
!
=
'
*
*
'
:
					
pattern_segs
.
insert
(
0
'
*
*
'
)
			
else
:
				
pass
			
if
not
pattern_segs
:
				
raise
GitWildMatchPatternError
(
f
"
Invalid
git
pattern
:
{
original_pattern
!
r
}
"
)
			
if
not
pattern_segs
[
-
1
]
and
len
(
pattern_segs
)
>
1
:
				
pattern_segs
[
-
1
]
=
'
*
*
'
			
if
override_regex
is
None
:
				
output
=
[
'
^
'
]
				
need_slash
=
False
				
end
=
len
(
pattern_segs
)
-
1
				
for
i
seg
in
enumerate
(
pattern_segs
)
:
					
if
seg
=
=
'
*
*
'
:
						
if
i
=
=
0
and
i
=
=
end
:
							
output
.
append
(
f
'
[
^
/
]
+
(
?
:
/
.
*
)
?
'
)
						
elif
i
=
=
0
:
							
output
.
append
(
'
(
?
:
.
+
/
)
?
'
)
							
need_slash
=
False
						
elif
i
=
=
end
:
							
if
is_dir_pattern
:
								
output
.
append
(
f
'
(
?
P
<
{
_DIR_MARK
}
>
/
)
.
*
'
)
							
else
:
								
output
.
append
(
f
'
/
.
*
'
)
						
else
:
							
output
.
append
(
'
(
?
:
/
.
+
)
?
'
)
							
need_slash
=
True
					
elif
seg
=
=
'
*
'
:
						
if
need_slash
:
							
output
.
append
(
'
/
'
)
						
output
.
append
(
'
[
^
/
]
+
'
)
						
if
i
=
=
end
:
							
output
.
append
(
f
'
(
?
:
(
?
P
<
{
_DIR_MARK
}
>
/
)
.
*
)
?
'
)
						
need_slash
=
True
					
else
:
						
if
need_slash
:
							
output
.
append
(
'
/
'
)
						
try
:
							
output
.
append
(
cls
.
_translate_segment_glob
(
seg
)
)
						
except
ValueError
as
e
:
							
raise
GitWildMatchPatternError
(
f
"
Invalid
git
pattern
:
{
original_pattern
!
r
}
"
)
from
e
						
if
i
=
=
end
:
							
output
.
append
(
f
'
(
?
:
(
?
P
<
{
_DIR_MARK
}
>
/
)
.
*
)
?
'
)
						
need_slash
=
True
				
output
.
append
(
'
'
)
				
regex
=
'
'
.
join
(
output
)
			
else
:
				
regex
=
override_regex
		
else
:
			
regex
=
None
			
include
=
None
		
if
regex
is
not
None
and
return_type
is
bytes
:
			
regex
=
regex
.
encode
(
_BYTES_ENCODING
)
		
return
regex
include
	
staticmethod
	
def
_translate_segment_glob
(
pattern
:
str
)
-
>
str
:
		
"
"
"
		
Translates
the
glob
pattern
to
a
regular
expression
.
This
is
used
in
the
		
constructor
to
translate
a
path
segment
glob
pattern
to
its
corresponding
		
regular
expression
.
		
*
pattern
*
(
:
class
:
str
)
is
the
glob
pattern
.
		
Returns
the
regular
expression
(
:
class
:
str
)
.
		
"
"
"
		
escape
=
False
		
regex
=
'
'
		
i
end
=
0
len
(
pattern
)
		
while
i
<
end
:
			
char
=
pattern
[
i
]
			
i
+
=
1
			
if
escape
:
				
escape
=
False
				
regex
+
=
re
.
escape
(
char
)
			
elif
char
=
=
'
\
\
'
:
				
escape
=
True
			
elif
char
=
=
'
*
'
:
				
regex
+
=
'
[
^
/
]
*
'
			
elif
char
=
=
'
?
'
:
				
regex
+
=
'
[
^
/
]
'
			
elif
char
=
=
'
[
'
:
				
j
=
i
				
if
j
<
end
and
(
pattern
[
j
]
=
=
'
!
'
or
pattern
[
j
]
=
=
'
^
'
)
:
					
j
+
=
1
				
if
j
<
end
and
pattern
[
j
]
=
=
'
]
'
:
					
j
+
=
1
				
while
j
<
end
and
pattern
[
j
]
!
=
'
]
'
:
					
j
+
=
1
				
if
j
<
end
:
					
j
+
=
1
					
expr
=
'
[
'
					
if
pattern
[
i
]
=
=
'
!
'
:
						
expr
+
=
'
^
'
						
i
+
=
1
					
elif
pattern
[
i
]
=
=
'
^
'
:
						
expr
+
=
'
^
'
						
i
+
=
1
					
expr
+
=
pattern
[
i
:
j
]
.
replace
(
'
\
\
'
'
\
\
\
\
'
)
					
regex
+
=
expr
					
i
=
j
				
else
:
					
regex
+
=
'
\
\
[
'
			
else
:
				
regex
+
=
re
.
escape
(
char
)
		
if
escape
:
			
raise
ValueError
(
f
"
Escape
character
found
with
no
next
character
to
escape
:
{
pattern
!
r
}
"
)
		
return
regex
	
staticmethod
	
def
escape
(
s
:
AnyStr
)
-
>
AnyStr
:
		
"
"
"
		
Escape
special
characters
in
the
given
string
.
		
*
s
*
(
:
class
:
str
or
:
class
:
bytes
)
a
filename
or
a
string
that
you
want
to
		
escape
usually
before
adding
it
to
a
"
.
gitignore
"
.
		
Returns
the
escaped
string
(
:
class
:
str
or
:
class
:
bytes
)
.
		
"
"
"
		
if
isinstance
(
s
str
)
:
			
return_type
=
str
			
string
=
s
		
elif
isinstance
(
s
bytes
)
:
			
return_type
=
bytes
			
string
=
s
.
decode
(
_BYTES_ENCODING
)
		
else
:
			
raise
TypeError
(
f
"
s
:
{
s
!
r
}
is
not
a
unicode
or
byte
string
.
"
)
		
meta_characters
=
r
"
[
]
!
*
#
?
"
		
out_string
=
"
"
.
join
(
"
\
\
"
+
x
if
x
in
meta_characters
else
x
for
x
in
string
)
		
if
return_type
is
bytes
:
			
return
out_string
.
encode
(
_BYTES_ENCODING
)
		
else
:
			
return
out_string
util
.
register_pattern
(
'
gitwildmatch
'
GitWildMatchPattern
)
class
GitIgnorePattern
(
GitWildMatchPattern
)
:
	
"
"
"
	
The
:
class
:
GitIgnorePattern
class
is
deprecated
by
:
class
:
GitWildMatchPattern
.
	
This
class
only
exists
to
maintain
compatibility
with
v0
.
4
.
	
"
"
"
	
def
__init__
(
self
*
args
*
*
kw
)
-
>
None
:
		
"
"
"
		
Warn
about
deprecation
.
		
"
"
"
		
self
.
_deprecated
(
)
		
super
(
GitIgnorePattern
self
)
.
__init__
(
*
args
*
*
kw
)
	
staticmethod
	
def
_deprecated
(
)
-
>
None
:
		
"
"
"
		
Warn
about
deprecation
.
		
"
"
"
		
warnings
.
warn
(
(
			
"
GitIgnorePattern
(
'
gitignore
'
)
is
deprecated
.
Use
GitWildMatchPattern
"
			
"
(
'
gitwildmatch
'
)
instead
.
"
		
)
DeprecationWarning
stacklevel
=
3
)
	
classmethod
	
def
pattern_to_regex
(
cls
*
args
*
*
kw
)
:
		
"
"
"
		
Warn
about
deprecation
.
		
"
"
"
		
cls
.
_deprecated
(
)
		
return
super
(
GitIgnorePattern
cls
)
.
pattern_to_regex
(
*
args
*
*
kw
)
util
.
register_pattern
(
'
gitignore
'
GitIgnorePattern
)
