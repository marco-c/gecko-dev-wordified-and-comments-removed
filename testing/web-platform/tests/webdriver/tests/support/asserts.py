errors
=
{
    
"
element
click
intercepted
"
:
400
    
"
element
not
selectable
"
:
400
    
"
element
not
interactable
"
:
400
    
"
insecure
certificate
"
:
400
    
"
invalid
argument
"
:
400
    
"
invalid
cookie
domain
"
:
400
    
"
invalid
coordinates
"
:
400
    
"
invalid
element
state
"
:
400
    
"
invalid
selector
"
:
400
    
"
invalid
session
id
"
:
404
    
"
javascript
error
"
:
500
    
"
move
target
out
of
bounds
"
:
500
    
"
no
such
alert
"
:
400
    
"
no
such
cookie
"
:
404
    
"
no
such
element
"
:
404
    
"
no
such
frame
"
:
400
    
"
no
such
window
"
:
400
    
"
script
timeout
"
:
408
    
"
session
not
created
"
:
500
    
"
stale
element
reference
"
:
400
    
"
timeout
"
:
408
    
"
unable
to
set
cookie
"
:
500
    
"
unable
to
capture
screen
"
:
500
    
"
unexpected
alert
open
"
:
500
    
"
unknown
command
"
:
404
    
"
unknown
error
"
:
500
    
"
unknown
method
"
:
405
    
"
unsupported
operation
"
:
500
}
def
assert_error
(
response
error_code
)
:
    
"
"
"
Verify
that
the
provided
wdclient
.
Response
instance
described
a
valid
    
error
response
as
defined
by
dfn
-
send
-
an
-
error
and
the
provided
error
    
code
.
    
:
param
response
:
wdclient
.
Response
instance
    
:
param
error_code
:
string
value
of
the
expected
"
error
code
"
    
"
"
"
    
assert
response
.
status
=
=
errors
[
error_code
]
    
assert
"
value
"
in
response
.
body
    
assert
response
.
body
[
"
value
"
]
[
"
error
"
]
=
=
error_code
    
assert
isinstance
(
response
.
body
[
"
value
"
]
[
"
message
"
]
basestring
)
    
assert
isinstance
(
response
.
body
[
"
value
"
]
[
"
stacktrace
"
]
basestring
)
def
assert_success
(
response
value
)
:
    
"
"
"
Verify
that
the
provided
wdclient
.
Response
instance
described
a
valid
    
error
response
as
defined
by
dfn
-
send
-
an
-
error
and
the
provided
error
    
code
.
    
:
param
response
:
wdclient
.
Response
instance
    
:
param
value
:
expected
value
of
the
response
body
    
"
"
"
    
assert
response
.
status
=
=
200
    
assert
response
.
body
[
"
value
"
]
=
=
value
