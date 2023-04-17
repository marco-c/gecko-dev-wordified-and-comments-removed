import
os
import
string
import
urllib
.
parse
import
urllib
.
request
from
typing
import
Optional
from
.
compat
import
WINDOWS
def
get_url_scheme
(
url
)
:
    
if
"
:
"
not
in
url
:
        
return
None
    
return
url
.
split
(
"
:
"
1
)
[
0
]
.
lower
(
)
def
path_to_url
(
path
)
:
    
"
"
"
    
Convert
a
path
to
a
file
:
URL
.
The
path
will
be
made
absolute
and
have
    
quoted
path
parts
.
    
"
"
"
    
path
=
os
.
path
.
normpath
(
os
.
path
.
abspath
(
path
)
)
    
url
=
urllib
.
parse
.
urljoin
(
"
file
:
"
urllib
.
request
.
pathname2url
(
path
)
)
    
return
url
def
url_to_path
(
url
)
:
    
"
"
"
    
Convert
a
file
:
URL
to
a
path
.
    
"
"
"
    
assert
url
.
startswith
(
        
"
file
:
"
    
)
f
"
You
can
only
turn
file
:
urls
into
filenames
(
not
{
url
!
r
}
)
"
    
_
netloc
path
_
_
=
urllib
.
parse
.
urlsplit
(
url
)
    
if
not
netloc
or
netloc
=
=
"
localhost
"
:
        
netloc
=
"
"
    
elif
WINDOWS
:
        
netloc
=
"
\
\
\
\
"
+
netloc
    
else
:
        
raise
ValueError
(
            
f
"
non
-
local
file
URIs
are
not
supported
on
this
platform
:
{
url
!
r
}
"
        
)
    
path
=
urllib
.
request
.
url2pathname
(
netloc
+
path
)
    
if
(
        
WINDOWS
        
and
not
netloc
        
and
len
(
path
)
>
=
3
        
and
path
[
0
]
=
=
"
/
"
        
and
path
[
1
]
in
string
.
ascii_letters
        
and
path
[
2
:
4
]
in
(
"
:
"
"
:
/
"
)
    
)
:
        
path
=
path
[
1
:
]
    
return
path
