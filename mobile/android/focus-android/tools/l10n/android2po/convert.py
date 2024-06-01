"
"
"
This
module
does
the
hard
work
of
converting
.
It
uses
a
simply
dict
-
based
memory
representation
of
Android
XML
string
resource
files
via
the
ResourceTree
class
.
The
.
po
files
are
represented
in
memory
via
Babel
'
s
Catalog
class
.
The
process
thus
is
:
    
read_xml
(
)
-
>
ResourceTree
-
>
xml2po
(
)
-
>
Catalog
-
>
po2xml
    
-
>
ResourceTree
-
>
write_xml
(
)
"
"
"
from
__future__
import
unicode_literals
from
itertools
import
chain
from
collections
import
namedtuple
from
lxml
import
etree
from
babel
.
messages
import
Catalog
from
babel
.
plural
import
_plural_tags
as
PLURAL_TAGS
try
:
    
from
collections
import
OrderedDict
except
ImportError
:
    
from
ordereddict
import
OrderedDict
__all__
=
(
'
xml2po
'
'
po2xml
'
'
read_xml
'
'
write_xml
'
           
'
set_catalog_plural_forms
'
'
InvalidResourceError
'
)
class
InvalidResourceError
(
Exception
)
:
    
pass
class
UnsupportedResourceError
(
Exception
)
:
    
"
"
"
A
resource
in
a
XML
file
can
'
t
be
processed
.
    
"
"
"
    
def
__init__
(
self
reason
)
:
        
self
.
reason
=
reason
WHITESPACE
=
'
\
n
\
t
'
EOF
=
None
KNOWN_NAMESPACES
=
{
    
'
urn
:
oasis
:
names
:
tc
:
xliff
:
document
:
1
.
2
'
:
'
xliff
'
}
def
dummy_warn
(
message
severity
=
None
)
:
    
return
None
class
ResourceTree
(
OrderedDict
)
:
    
language
=
None
    
def
__init__
(
self
language
=
None
)
:
        
OrderedDict
.
__init__
(
self
)
        
self
.
language
=
language
class
StringArray
(
list
)
:
    
pass
class
Plurals
(
dict
)
:
    
pass
Translation
=
namedtuple
(
'
Translation
'
[
'
text
'
'
comments
'
'
formatted
'
]
)
def
get_element_text
(
tag
name
warnfunc
=
dummy_warn
)
:
    
"
"
"
Return
a
tuple
of
the
contents
of
the
lxml
element
with
the
    
Android
specific
stuff
decoded
and
whether
the
text
includes
    
formatting
codes
.
    
"
Contents
"
isn
'
t
just
the
text
;
it
handles
nested
HTML
tags
as
well
.
    
"
"
"
    
def
convert_text
(
text
)
:
        
"
"
"
This
is
called
for
every
distinct
block
of
text
as
they
        
are
separated
by
tags
.
        
It
handles
most
of
the
Android
syntax
rules
:
quoting
escaping
        
collapsing
duplicate
whitespace
etc
.
        
"
"
"
        
text
=
text
.
replace
(
'
<
'
'
&
lt
;
'
)
        
text
=
text
.
replace
(
'
>
'
"
&
gt
;
"
)
        
space_count
=
0
        
active_quote
=
False
        
active_percent
=
False
        
active_escape
=
False
        
formatted
=
False
        
i
=
0
        
text
=
list
(
text
)
+
[
EOF
]
        
while
i
<
len
(
text
)
:
            
c
=
text
[
i
]
            
if
c
is
not
EOF
and
c
in
WHITESPACE
:
                
space_count
+
=
1
            
elif
space_count
>
1
:
                
if
not
active_quote
or
c
is
EOF
:
                    
text
[
i
-
space_count
:
i
]
=
'
'
                    
i
-
=
space_count
-
1
                
space_count
=
0
            
elif
space_count
=
=
1
:
                
text
[
i
-
1
]
=
'
'
                
space_count
=
0
            
else
:
                
space_count
=
0
            
if
c
=
=
'
"
'
and
not
active_escape
:
                
active_quote
=
not
active_quote
                
del
text
[
i
]
                
i
-
=
1
            
if
c
=
=
'
%
'
and
not
active_escape
:
                
active_percent
=
not
active_percent
            
elif
not
active_escape
and
active_percent
:
                
formatted
=
True
                
active_percent
=
False
            
if
c
=
=
'
\
\
'
:
                
if
not
active_escape
:
                    
active_escape
=
True
                
else
:
                    
del
text
[
i
]
                    
i
-
=
1
                    
active_escape
=
False
            
else
:
                
if
active_escape
:
                    
if
c
is
EOF
:
                        
pass
                    
elif
c
=
=
'
n
'
:
                        
text
[
i
-
1
:
i
+
1
]
=
'
\
n
'
                        
i
-
=
1
                    
elif
c
=
=
'
t
'
:
                        
text
[
i
-
1
:
i
+
1
]
=
'
\
t
'
                        
i
-
=
1
                    
elif
c
in
'
"
\
'
'
:
                        
text
[
i
-
1
:
i
]
=
'
'
                        
i
-
=
1
                    
elif
c
=
=
'
u
'
:
                        
max_slice
=
min
(
i
+
5
len
(
text
)
-
1
)
                        
codepoint_str
=
"
"
.
join
(
text
[
i
+
1
:
max_slice
]
)
                        
if
len
(
codepoint_str
)
<
4
:
                            
codepoint_str
=
"
0
"
*
(
4
-
len
(
codepoint_str
)
)
+
codepoint_str
                        
print
(
repr
(
codepoint_str
)
)
                        
try
:
                            
if
not
codepoint_str
.
isalnum
(
)
:
                                
raise
ValueError
(
codepoint_str
)
                            
codepoint
=
chr
(
int
(
codepoint_str
16
)
)
                        
except
ValueError
:
                            
raise
UnsupportedResourceError
(
'
bad
unicode
escape
sequence
'
)
                        
text
[
i
-
1
:
max_slice
]
=
codepoint
                        
i
-
=
1
                    
else
:
                        
warnfunc
(
(
'
Resource
"
%
s
"
:
removing
unsupported
'
                                  
'
escape
sequence
"
%
s
"
'
)
%
(
                                    
name
"
"
.
join
(
text
[
i
-
1
:
i
+
1
]
)
)
'
warning
'
)
                        
text
[
i
-
1
:
i
+
1
]
=
'
'
                        
i
-
=
1
                    
active_escape
=
False
            
i
+
=
1
        
return
"
"
.
join
(
text
[
:
-
1
]
)
formatted
    
def
get_tag_name
(
elem
)
:
        
"
"
"
For
tags
without
a
namespace
returns
(
"
tag
"
None
)
.
        
For
tags
with
a
known
-
namespace
returns
(
"
prefix
:
tag
"
None
)
.
        
For
tags
with
an
unknown
-
namespace
returns
(
"
tag
"
(
"
prefix
"
"
ns
"
)
)
        
"
"
"
        
if
elem
.
prefix
:
            
namespace
=
elem
.
nsmap
[
elem
.
prefix
]
            
raw_name
=
elem
.
tag
[
elem
.
tag
.
index
(
'
}
'
)
+
1
:
]
            
if
namespace
in
KNOWN_NAMESPACES
:
                
return
"
%
s
:
%
s
"
%
(
KNOWN_NAMESPACES
[
namespace
]
raw_name
)
None
            
return
"
%
s
:
%
s
"
%
(
elem
.
prefix
raw_name
)
(
elem
.
prefix
namespace
)
        
return
elem
.
tag
None
    
value
=
"
"
    
formatted
=
False
    
for
ev
elem
in
etree
.
iterwalk
(
tag
events
=
(
'
start
'
'
end
'
)
)
:
        
is_root
=
elem
=
=
tag
        
has_children
=
len
(
tag
)
>
0
        
if
ev
=
=
'
start
'
:
            
if
not
is_root
:
                
tag_name
to_declare
=
get_tag_name
(
elem
)
                
params
=
[
"
%
s
=
\
"
%
s
\
"
"
%
(
k
v
)
for
k
v
in
list
(
elem
.
attrib
.
items
(
)
)
]
                
if
to_declare
:
                    
name
url
=
to_declare
                    
params
.
append
(
'
xmlns
:
%
s
=
"
%
s
"
'
%
(
name
url
)
)
                
params_str
=
"
%
s
"
%
"
"
.
join
(
params
)
if
params
else
"
"
                
value
+
=
"
<
%
s
%
s
>
"
%
(
tag_name
params_str
)
            
if
elem
.
text
is
not
None
:
                
t
=
elem
.
text
                
raw
=
etree
.
tostring
(
elem
)
                
if
is_root
and
not
has_children
and
len
(
tag
)
=
=
0
:
                    
t
=
t
.
strip
(
WHITESPACE
)
                
if
is_root
and
not
has_children
and
t
and
t
[
0
]
=
=
'
'
:
                    
raise
UnsupportedResourceError
(
                        
'
resource
references
(
%
s
)
are
not
supported
'
%
t
)
                
if
"
<
!
[
CDATA
[
"
in
raw
:
                    
value
+
=
t
                
else
:
                    
converted_value
elem_formatted
=
convert_text
(
t
)
                    
if
elem_formatted
:
                        
formatted
=
True
                    
value
+
=
converted_value
        
elif
ev
=
=
'
end
'
:
            
if
not
is_root
:
                
tag_name
_
=
get_tag_name
(
elem
)
                
value
+
=
"
<
/
%
s
>
"
%
tag_name
                
if
elem
.
tail
is
not
None
:
                    
converted_value
elem_formatted
=
convert_text
(
elem
.
tail
)
                    
if
elem_formatted
:
                        
formatted
=
True
                    
value
+
=
converted_value
    
if
value
=
=
'
'
:
        
raise
UnsupportedResourceError
(
'
empty
resources
not
supported
'
)
    
return
value
formatted
def
read_xml
(
xml_file
language
=
None
warnfunc
=
dummy_warn
)
:
    
"
"
"
Load
all
resource
names
from
an
Android
strings
.
xml
resource
file
.
    
The
result
is
a
ResourceTree
instance
.
    
"
"
"
    
result
=
ResourceTree
(
language
)
    
comment
=
[
]
    
parser
=
etree
.
XMLParser
(
strip_cdata
=
False
)
    
try
:
        
doc
=
etree
.
parse
(
xml_file
parser
=
parser
)
    
except
etree
.
XMLSyntaxError
as
e
:
        
raise
InvalidResourceError
(
e
)
    
for
tag
in
doc
.
getroot
(
)
:
        
if
tag
.
tag
=
=
etree
.
Comment
:
            
comment
.
append
(
tag
.
text
)
            
continue
        
if
'
name
'
not
in
tag
.
attrib
:
            
comment
=
[
]
            
continue
        
if
tag
.
attrib
.
get
(
'
translatable
'
)
=
=
'
false
'
:
            
comment
=
[
]
            
continue
        
name
=
tag
.
attrib
[
'
name
'
]
        
if
name
in
result
:
            
warnfunc
(
'
Duplicate
resource
id
found
:
%
s
ignoring
.
'
%
name
                     
'
warning
'
)
            
comment
=
[
]
            
continue
        
if
tag
.
tag
=
=
'
string
'
:
            
try
:
                
text
formatted
=
get_element_text
(
tag
name
warnfunc
)
            
except
UnsupportedResourceError
as
e
:
                
warnfunc
(
'
"
%
s
"
has
been
skipped
reason
:
%
s
'
%
(
                    
name
e
.
reason
)
'
info
'
)
            
else
:
                
translation
=
Translation
(
text
comment
formatted
)
                
result
[
name
]
=
translation
        
elif
tag
.
tag
=
=
'
string
-
array
'
:
            
result
[
name
]
=
StringArray
(
)
            
for
child
in
tag
.
findall
(
'
item
'
)
:
                
try
:
                    
text
formatted
=
get_element_text
(
child
name
warnfunc
)
                
except
UnsupportedResourceError
as
e
:
                    
warnfunc
(
(
'
Warning
:
The
array
"
%
s
"
contains
items
'
+
                              
'
that
can
\
'
t
be
processed
(
reason
:
%
s
)
-
'
                              
'
the
array
will
be
incomplete
'
)
%
                             
(
name
e
.
reason
)
'
warning
'
)
                
else
:
                    
translation
=
Translation
(
text
comment
formatted
)
                    
result
[
name
]
.
append
(
translation
)
        
elif
tag
.
tag
=
=
'
plurals
'
:
            
result
[
name
]
=
Plurals
(
)
            
for
child
in
tag
.
findall
(
'
item
'
)
:
                
try
:
                    
quantity
=
child
.
attrib
[
'
quantity
'
]
                    
assert
quantity
in
PLURAL_TAGS
                
except
(
IndexError
AssertionError
)
:
                    
warnfunc
(
(
'
"
%
s
"
contains
a
plural
with
no
or
'
+
                              
'
an
invalid
quantity
'
)
%
name
'
warning
'
)
                
else
:
                    
try
:
                        
text
formatted
=
get_element_text
(
child
name
warnfunc
)
                    
except
UnsupportedResourceError
as
e
:
                        
warnfunc
(
(
'
Warning
:
The
plural
"
%
s
"
can
\
'
t
'
+
                                  
'
be
processed
(
reason
:
%
s
)
-
'
                                  
'
the
plural
will
be
incomplete
'
)
%
                                 
(
name
e
.
reason
)
'
warning
'
)
                    
else
:
                        
translation
=
Translation
(
text
comment
formatted
)
                        
result
[
name
]
[
quantity
]
=
translation
        
comment
=
[
]
    
return
result
def
plural_to_gettext
(
rule
)
:
    
"
"
"
This
is
a
copy
of
the
code
of
babel
.
plural
.
to_gettext
.
    
We
need
to
use
a
custom
version
because
the
original
only
returns
    
a
full
plural_forms
string
which
the
Babel
catalog
object
does
not
    
allow
us
to
assign
to
anything
.
Instead
we
need
the
expr
and
the
    
plural
count
separately
.
See
http
:
/
/
babel
.
edgewall
.
org
/
ticket
/
291
.
    
"
"
"
    
from
babel
.
plural
import
(
PluralRule
_fallback_tag
_plural_tags
                              
_GettextCompiler
)
    
rule
=
PluralRule
.
parse
(
rule
)
    
used_tags
=
rule
.
tags
|
set
(
[
_fallback_tag
]
)
    
_compile
=
_GettextCompiler
(
)
.
compile
    
_get_index
=
[
tag
for
tag
in
_plural_tags
if
tag
in
used_tags
]
.
index
    
expr
=
[
'
(
'
]
    
for
tag
ast
in
rule
.
abstract
:
        
expr
.
append
(
'
%
s
?
%
d
:
'
%
(
_compile
(
ast
)
_get_index
(
tag
)
)
)
    
expr
.
append
(
'
%
d
)
'
%
_get_index
(
_fallback_tag
)
)
    
return
len
(
used_tags
)
'
'
.
join
(
expr
)
def
set_catalog_plural_forms
(
catalog
language
)
:
    
"
"
"
Set
the
catalog
to
use
the
correct
plural
forms
for
the
    
language
.
    
"
"
"
    
try
:
        
catalog
.
_num_plurals
catalog
.
_plural_expr
=
plural_to_gettext
(
            
language
.
locale
.
plural_form
)
    
except
KeyError
:
        
pass
def
xml2po
(
resources
translations
=
None
resfilter
=
None
warnfunc
=
dummy_warn
)
:
    
"
"
"
Return
resources
as
a
Babel
.
po
Catalog
instance
.
    
If
given
translations
will
be
used
for
the
translated
values
.
    
In
this
case
the
returned
value
is
a
2
-
tuple
(
catalog
unmatched
)
    
with
the
latter
being
a
list
of
Android
string
resource
names
that
    
are
in
the
translated
file
but
not
in
the
original
.
    
Both
resources
and
translations
must
be
ResourceTree
    
objects
as
returned
by
read_xml
(
)
.
    
From
the
application
perspective
it
will
call
this
function
with
    
a
translations
object
when
initializing
a
new
.
po
file
based
on
    
an
existing
resource
file
(
the
'
init
'
command
)
.
For
'
export
'
this
    
function
is
called
without
translations
.
It
will
thus
generate
what
    
is
essentially
a
POT
file
(
an
empty
.
po
file
)
and
this
will
be
    
merged
into
the
existing
.
po
catalogs
as
per
how
gettext
usually
    
"
"
"
    
assert
not
translations
or
translations
.
language
    
catalog
=
Catalog
(
)
    
if
translations
is
not
None
:
        
catalog
.
locale
=
translations
.
language
.
locale
        
set_catalog_plural_forms
(
catalog
translations
.
language
)
    
for
name
org_value
in
resources
.
items
(
)
:
        
if
resfilter
and
resfilter
(
name
)
:
            
continue
        
trans_value
=
None
        
if
translations
:
            
trans_value
=
translations
.
pop
(
name
trans_value
)
        
if
isinstance
(
org_value
StringArray
)
:
            
if
len
(
org_value
)
=
=
0
:
                
warnfunc
(
"
Warning
:
string
-
array
'
%
s
'
is
empty
"
%
name
'
warning
'
)
                
continue
            
if
not
isinstance
(
trans_value
StringArray
)
:
                
if
trans_value
:
                    
warnfunc
(
(
'
"
"
%
s
"
is
a
string
-
array
in
the
reference
'
                              
'
file
but
not
in
the
translation
.
'
)
%
                             
name
'
warning
'
)
                
trans_value
=
StringArray
(
)
            
for
index
item
in
enumerate
(
org_value
)
:
                
item_trans
=
trans_value
[
index
]
.
text
if
index
<
len
(
trans_value
)
else
'
'
                
flags
=
[
]
                
if
item
.
formatted
:
                    
flags
.
append
(
'
c
-
format
'
)
                
ctx
=
"
%
s
:
%
d
"
%
(
name
index
)
                
catalog
.
add
(
item
.
text
item_trans
auto_comments
=
item
.
comments
                            
flags
=
flags
context
=
ctx
)
        
elif
isinstance
(
org_value
Plurals
)
:
            
if
len
(
org_value
)
=
=
0
:
                
warnfunc
(
"
Warning
:
plurals
'
%
s
'
is
empty
"
%
name
'
warning
'
)
                
continue
            
if
not
isinstance
(
trans_value
Plurals
)
:
                
if
trans_value
:
                    
warnfunc
(
(
'
"
"
%
s
"
is
a
plurals
in
the
reference
'
                              
'
file
but
not
in
the
translation
.
'
)
%
                             
name
'
warning
'
)
                
trans_value
=
Plurals
(
)
            
formatted
=
False
            
comments
=
[
]
            
for
_
translation
in
list
(
org_value
.
items
(
)
)
:
                
if
translation
.
formatted
:
                    
formatted
=
True
                
comments
.
extend
(
translation
.
comments
)
            
temp
=
org_value
.
copy
(
)
            
singular
=
\
                
temp
.
pop
(
'
one
'
)
if
'
one
'
in
temp
else
\
                
temp
.
pop
(
'
other
'
)
if
'
other
'
in
temp
else
\
                
temp
.
pop
(
list
(
temp
.
keys
(
)
)
[
0
]
)
            
plural
=
\
                
temp
.
pop
(
'
other
'
)
if
'
other
'
in
temp
else
\
                
temp
[
list
(
temp
.
keys
(
)
)
[
0
]
]
if
temp
else
\
                
singular
            
msgid
=
(
singular
.
text
plural
.
text
)
            
del
temp
singular
plural
            
msgstr
=
'
'
            
if
trans_value
:
                
allowed_keywords
=
translations
.
language
.
plural_keywords
                
msgstr
=
[
'
'
for
i
in
range
(
len
(
allowed_keywords
)
)
]
                
for
quantity
translation
in
list
(
trans_value
.
items
(
)
)
:
                    
try
:
                        
index
=
translations
.
language
.
plural_keywords
.
index
(
quantity
)
                    
except
ValueError
:
                        
warnfunc
(
                            
(
'
"
plurals
"
%
s
"
uses
quantity
"
%
s
"
which
'
                             
'
is
not
supported
for
this
language
.
See
'
                             
'
the
README
for
an
explanation
.
The
'
                             
'
quantity
has
been
ignored
'
)
%
                            
(
name
quantity
)
'
warning
'
)
                    
else
:
                        
msgstr
[
index
]
=
translation
.
text
            
flags
=
[
]
            
if
formatted
:
                
flags
.
append
(
'
c
-
format
'
)
            
catalog
.
add
(
msgid
tuple
(
msgstr
)
flags
=
flags
                        
auto_comments
=
comments
context
=
name
)
        
else
:
            
flags
=
[
]
            
if
org_value
.
formatted
:
                
flags
.
append
(
'
c
-
format
'
)
            
catalog
.
add
(
org_value
.
text
trans_value
.
text
if
trans_value
else
'
'
                        
flags
=
flags
auto_comments
=
org_value
.
comments
context
=
name
)
    
if
translations
is
not
None
:
        
return
catalog
list
(
translations
.
keys
(
)
)
    
else
:
        
return
catalog
def
write_to_dom
(
elem_name
value
ref
namespaces
=
None
warnfunc
=
dummy_warn
)
:
    
"
"
"
Create
a
DOM
object
with
the
tag
name
elem_name
containing
    
the
string
value
formatted
according
to
Android
XML
rules
.
    
The
result
might
be
a
<
string
>
-
tag
or
a
<
item
>
-
tag
as
found
as
    
children
of
<
string
-
array
>
for
example
.
    
It
might
feel
awkward
at
first
that
the
Android
-
XML
formatting
    
does
not
happen
in
a
separate
method
but
is
part
of
the
creation
    
of
a
tag
but
due
to
us
having
to
do
certain
formatting
based
on
    
child
DOM
elements
that
value
may
include
the
two
fit
    
naturally
together
(
see
the
POSTPROCESS
section
of
this
function
)
.
    
If
one
of
our
supported
namespace
prefixes
is
used
within
nested
tags
    
inside
value
the
appropriate
data
is
added
to
the
    
namespaces
dict
if
given
so
the
caller
may
generate
the
    
proper
declarations
.
    
"
"
"
    
loose_parser
=
etree
.
XMLParser
(
recover
=
True
)
    
if
value
is
None
:
        
value
=
'
'
    
value
=
value
.
replace
(
'
&
'
'
&
amp
;
'
)
    
value
=
value
.
replace
(
'
&
amp
;
lt
;
'
'
&
lt
;
'
)
    
value
=
value
.
replace
(
'
&
amp
;
gt
;
'
'
&
gt
;
'
)
    
namespace_text
=
"
"
.
join
(
[
'
xmlns
:
%
s
=
"
%
s
"
'
%
(
prefix
ns
)
for
ns
prefix
in
list
(
KNOWN_NAMESPACES
.
items
(
)
)
]
)
    
value_to_parse
=
"
<
root
%
s
>
<
%
s
>
%
s
<
/
%
s
>
<
/
root
>
"
%
(
namespace_text
elem_name
value
elem_name
)
    
try
:
        
elem
=
etree
.
fromstring
(
value_to_parse
)
    
except
etree
.
XMLSyntaxError
as
e
:
        
elem
=
etree
.
fromstring
(
value_to_parse
loose_parser
)
        
warnfunc
(
(
'
%
s
contains
invalid
XHTML
(
%
s
)
;
Falling
back
to
'
                  
'
loose
parser
.
'
)
%
(
ref
e
)
'
warning
'
)
    
if
namespaces
is
not
None
:
        
for
c
in
elem
.
iterdescendants
(
)
:
            
if
c
.
prefix
:
                
nsuri
=
c
.
nsmap
[
c
.
prefix
]
                
if
nsuri
in
KNOWN_NAMESPACES
:
                    
namespaces
[
KNOWN_NAMESPACES
[
nsuri
]
]
=
nsuri
    
elem
=
elem
[
0
]
    
def
quote
(
text
)
:
        
"
"
"
Return
text
surrounded
by
quotes
if
necessary
.
        
"
"
"
        
if
text
is
None
:
            
return
        
needs_quoting
=
text
.
strip
(
WHITESPACE
)
!
=
text
        
if
not
needs_quoting
:
            
space_count
=
0
            
for
c
in
chain
(
text
[
EOF
]
)
:
                
if
c
is
not
EOF
and
c
in
WHITESPACE
:
                    
space_count
+
=
1
                    
if
space_count
>
=
2
:
                        
needs_quoting
=
True
                        
break
                
else
:
                    
space_count
=
0
        
if
needs_quoting
:
            
return
'
"
%
s
"
'
%
text
        
return
text
    
def
escape
(
text
)
:
        
"
"
"
Escape
all
the
characters
we
know
need
to
be
escaped
        
in
an
Android
XML
file
.
"
"
"
        
if
text
is
None
:
            
return
        
text
=
text
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
        
text
=
text
.
replace
(
'
\
n
'
'
\
\
n
'
)
        
text
=
text
.
replace
(
'
\
t
'
'
\
\
t
'
)
        
text
=
text
.
replace
(
'
\
'
'
'
\
\
\
'
'
)
        
text
=
text
.
replace
(
'
"
'
'
\
\
"
'
)
        
text
=
text
.
replace
(
'
'
'
\
\
'
)
        
return
text
    
for
child_elem
in
elem
.
iter
(
)
:
        
child_elem
.
text
=
quote
(
escape
(
child_elem
.
text
)
)
        
child_elem
.
tail
=
quote
(
escape
(
child_elem
.
tail
)
)
    
return
elem
def
key_plural_keywords
(
x
)
:
    
"
"
"
Extracts
CLDR
plural
keywords
index
starting
with
'
zero
'
    
and
ending
with
'
other
'
.
"
"
"
    
return
PLURAL_TAGS
.
index
(
x
)
if
x
in
PLURAL_TAGS
else
-
1
def
po2xml
(
catalog
with_untranslated
=
False
resfilter
=
None
warnfunc
=
dummy_warn
)
:
    
"
"
"
Convert
the
gettext
catalog
in
catalog
to
a
ResourceTree
    
instance
(
our
in
-
memory
representation
of
an
Android
XML
resource
)
    
This
currently
relies
entirely
in
the
fact
that
we
can
use
the
context
    
of
each
message
to
specify
the
Android
resource
name
(
which
we
need
    
to
do
to
handle
duplicates
but
this
is
a
nice
by
-
product
)
.
However
    
that
also
means
we
cannot
handle
arbitrary
catalogs
.
    
The
latter
would
in
theory
be
possible
by
using
the
original
    
untranslated
XML
to
match
up
a
messages
id
to
a
resource
name
but
    
right
now
we
don
'
t
support
this
(
and
it
'
s
not
clear
it
would
be
    
necessary
even
)
.
    
If
with_untranslated
is
given
then
strings
in
the
catalog
    
that
have
no
translation
are
written
out
with
the
original
id
    
whenever
this
is
safely
possible
.
This
does
not
include
string
-
arrays
    
which
for
technical
reasons
always
must
include
all
elements
and
it
    
does
not
include
plurals
for
which
the
same
is
true
.
    
"
"
"
    
plural_validation
=
{
'
done
'
:
False
}
    
def
validate_plural_config
(
)
:
        
if
plural_validation
[
'
done
'
]
:
            
return
        
if
catalog
.
num_plurals
!
=
len
(
catalog
.
language
.
plural_keywords
)
:
            
warnfunc
(
(
'
Catalog
defines
%
d
plurals
we
expect
%
d
for
'
                      
'
this
language
.
See
the
README
for
an
'
                      
'
explanation
.
plurals
have
very
likely
been
'
                      
'
incorrectly
written
.
'
)
%
(
                
catalog
.
num_plurals
len
(
catalog
.
language
.
plural_keywords
)
)
'
error
'
)
            
pass
        
plural_validation
[
'
done
'
]
=
True
    
xml_tree
=
ResourceTree
(
getattr
(
catalog
'
language
'
None
)
)
    
for
message
in
catalog
:
        
if
not
message
.
id
:
            
continue
        
if
not
message
.
context
:
            
warnfunc
(
(
'
Ignoring
message
"
%
s
"
:
has
no
context
;
somebody
other
'
+
                      
'
than
android2po
seems
to
have
added
to
this
'
+
                      
'
catalog
.
'
)
%
message
.
id
'
error
'
)
            
continue
        
if
resfilter
and
resfilter
(
message
)
:
            
continue
        
value
=
message
.
string
or
message
.
id
        
if
'
:
'
in
message
.
context
:
            
name
index
=
message
.
context
.
split
(
'
:
'
2
)
            
index
=
int
(
index
)
            
xml_tree
.
setdefault
(
name
StringArray
(
)
)
            
while
index
>
=
len
(
xml_tree
[
name
]
)
:
                
xml_tree
[
name
]
.
append
(
None
)
            
if
xml_tree
[
name
]
[
index
]
is
not
None
:
                
warnfunc
(
(
'
Duplicate
index
%
s
in
array
"
%
s
"
;
ignoring
'
+
                          
'
the
message
.
The
catalog
has
possibly
been
'
+
                          
'
corrupted
.
'
)
%
(
index
name
)
'
error
'
)
            
xml_tree
[
name
]
[
index
]
=
value
        
elif
isinstance
(
message
.
string
tuple
)
:
            
validate_plural_config
(
)
            
if
not
any
(
message
.
string
)
:
                
continue
            
xml_tree
[
message
.
context
]
=
Plurals
(
[
                
(
k
None
)
for
k
in
catalog
.
language
.
plural_keywords
]
)
            
for
index
keyword
in
enumerate
(
catalog
.
language
.
plural_keywords
)
:
                
try
:
                    
xml_tree
[
message
.
context
]
[
keyword
]
=
message
.
string
[
index
]
                
except
IndexError
:
                    
break
        
else
:
            
if
not
message
.
string
and
not
with_untranslated
:
                
continue
            
xml_tree
[
message
.
context
]
=
value
    
return
xml_tree
def
stringify_children
(
node
)
:
    
from
lxml
.
etree
import
tostring
    
from
itertools
import
chain
    
parts
=
(
[
node
.
text
]
+
            
list
(
chain
(
*
(
[
tostring
(
c
with_tail
=
False
)
c
.
tail
]
for
c
in
node
.
getchildren
(
)
)
)
)
+
            
[
node
.
tail
]
)
    
return
'
'
.
join
(
filter
(
None
parts
)
)
def
write_xml
(
tree
warnfunc
=
dummy_warn
)
:
    
"
"
"
Takes
a
ResourceTree
(
our
in
-
memory
representation
of
an
Android
    
XML
resource
)
and
returns
a
XML
DOM
(
via
an
etree
.
Element
)
.
    
"
"
"
    
root_tags
=
[
]
    
namespaces_used
=
{
}
    
for
name
value
in
tree
.
items
(
)
:
        
if
isinstance
(
value
StringArray
)
:
            
array_el
=
etree
.
Element
(
'
string
-
array
'
)
            
array_el
.
attrib
[
'
name
'
]
=
name
            
for
i
v
in
enumerate
(
value
)
:
                
item_el
=
write_to_dom
(
                    
'
item
'
v
'
"
%
s
"
index
%
d
'
%
(
name
i
)
namespaces_used
                    
warnfunc
)
                
array_el
.
append
(
item_el
)
            
root_tags
.
append
(
array_el
)
        
elif
isinstance
(
value
Plurals
)
:
            
plural_el
=
etree
.
Element
(
'
plurals
'
)
            
plural_el
.
attrib
[
'
name
'
]
=
name
            
for
k
in
sorted
(
value
key
=
key_plural_keywords
)
:
                
item_el
=
write_to_dom
(
                    
'
item
'
value
[
k
]
'
"
%
s
"
quantity
%
s
'
%
(
name
k
)
                    
namespaces_used
warnfunc
)
                
item_el
.
attrib
[
"
quantity
"
]
=
k
                
plural_el
.
append
(
item_el
)
            
root_tags
.
append
(
plural_el
)
        
else
:
            
string_el
=
write_to_dom
(
                
'
string
'
value
'
"
%
s
"
'
%
name
namespaces_used
warnfunc
)
            
string_el
.
attrib
[
'
name
'
]
=
name
            
if
len
(
string_el
)
>
0
:
                
text
=
stringify_children
(
string_el
)
.
strip
(
)
                
if
(
tag
in
text
for
tag
in
[
'
<
ul
>
'
'
<
p
>
'
'
<
br
'
'
<
strong
>
'
'
<
li
>
'
'
<
b
>
'
]
)
:
                    
del
string_el
[
:
]
                    
string_el
.
text
=
etree
.
CDATA
(
text
)
            
root_tags
.
append
(
string_el
)
    
root_el
=
etree
.
Element
(
'
resources
'
nsmap
=
namespaces_used
)
    
for
e
in
root_tags
:
        
root_el
.
append
(
e
)
    
return
root_el
