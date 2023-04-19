#
coding
=
utf8
from
__future__
import
absolute_import
import
fluent
.
syntax
.
ast
as
FTL
from
fluent
.
migrate
.
helpers
import
TERM_REFERENCE
transforms_from
VARIABLE_REFERENCE
from
fluent
.
migrate
.
transforms
import
(
    
COPY
    
LegacySource
    
REPLACE
    
REPLACE_IN_TEXT
    
Transform
)
import
re
class
MATCH
(
LegacySource
)
:
    
"
"
"
Custom
transform
for
extracting
parts
of
a
netError
.
dtd
message
.
    
start
and
end
are
not
included
in
the
result
which
is
always
trimmed
.
    
index
allows
for
targeting
matches
beyond
the
first
(
=
0
)
in
the
source
.
    
replacements
are
optional
;
if
set
they
work
as
in
REPLACE
(
)
    
"
"
"
    
def
__init__
(
        
self
path
key
start
:
str
end
:
str
index
=
0
replacements
=
None
*
*
kwargs
    
)
:
        
super
(
MATCH
self
)
.
__init__
(
path
key
*
*
kwargs
)
        
self
.
start
=
start
        
self
.
end
=
end
        
self
.
index
=
index
        
self
.
replacements
=
replacements
    
def
__call__
(
self
ctx
)
:
        
element
:
FTL
.
TextElement
=
super
(
MATCH
self
)
.
__call__
(
ctx
)
        
text
:
str
=
element
.
value
        
starts
=
list
(
re
.
finditer
(
re
.
escape
(
self
.
start
)
text
)
)
        
if
self
.
index
>
len
(
starts
)
-
1
:
            
print
(
                
f
"
WARNING
:
index
{
self
.
index
}
out
of
range
for
{
self
.
start
}
in
{
self
.
key
}
"
            
)
            
return
Transform
.
pattern_of
(
element
)
        
start
=
starts
[
self
.
index
]
.
end
(
)
        
end
=
text
.
find
(
self
.
end
start
)
        
text
=
self
.
trim_text
(
text
[
start
:
end
]
)
        
element
.
value
=
re
.
sub
(
"
[
\
n
\
r
]
+
"
"
"
text
)
        
if
self
.
replacements
is
None
:
            
return
Transform
.
pattern_of
(
element
)
        
else
:
            
return
REPLACE_IN_TEXT
(
element
self
.
replacements
)
(
ctx
)
def
BOLD_VARIABLE_REFERENCE
(
name
)
:
    
return
FTL
.
Pattern
(
        
[
            
FTL
.
TextElement
(
"
<
b
>
"
)
            
FTL
.
Placeable
(
VARIABLE_REFERENCE
(
name
)
)
            
FTL
.
TextElement
(
"
<
/
b
>
"
)
        
]
    
)
def
migrate
(
ctx
)
:
    
"
"
"
Bug
1734217
-
Migrate
aboutNetError
.
xhtml
from
DTD
to
Fluent
part
{
index
}
"
"
"
    
source
=
"
browser
/
chrome
/
overrides
/
netError
.
dtd
"
    
target
=
"
browser
/
browser
/
netError
.
ftl
"
    
ctx
.
add_transforms
(
        
target
        
target
        
transforms_from
(
            
"
"
"
neterror
-
page
-
title
=
{
COPY
(
source
"
loadError
.
label
"
)
}
certerror
-
page
-
title
=
{
COPY
(
source
"
certerror
.
pagetitle2
"
)
}
certerror
-
sts
-
page
-
title
=
{
COPY
(
source
"
certerror
.
sts
.
pagetitle
"
)
}
neterror
-
blocked
-
by
-
policy
-
page
-
title
=
{
COPY
(
source
"
blockedByPolicy
.
title
"
)
}
neterror
-
captive
-
portal
-
page
-
title
=
{
COPY
(
source
"
captivePortal
.
title
"
)
}
neterror
-
malformed
-
uri
-
page
-
title
=
{
COPY
(
source
"
malformedURI
.
pageTitle
"
)
}
neterror
-
advanced
-
button
=
{
COPY
(
source
"
advanced2
.
label
"
)
}
neterror
-
copy
-
to
-
clipboard
-
button
=
{
COPY
(
source
"
certerror
.
copyToClipboard
.
label
"
)
}
neterror
-
learn
-
more
-
link
=
{
COPY
(
source
"
errorReporting
.
learnMore
"
)
}
neterror
-
open
-
portal
-
login
-
page
-
button
=
{
COPY
(
source
"
openPortalLoginPage
.
label2
"
)
}
neterror
-
override
-
exception
-
button
=
{
COPY
(
source
"
securityOverride
.
exceptionButton1Label
"
)
}
neterror
-
pref
-
reset
-
button
=
{
COPY
(
source
"
prefReset
.
label
"
)
}
neterror
-
return
-
to
-
previous
-
page
-
button
=
{
COPY
(
source
"
returnToPreviousPage
.
label
"
)
}
neterror
-
return
-
to
-
previous
-
page
-
recommended
-
button
=
{
COPY
(
source
"
returnToPreviousPage1
.
label
"
)
}
neterror
-
try
-
again
-
button
=
{
COPY
(
source
"
retry
.
label
"
)
}
neterror
-
view
-
certificate
-
link
=
{
COPY
(
source
"
viewCertificate
.
label
"
)
}
neterror
-
pref
-
reset
=
{
COPY
(
source
"
prefReset
.
longDesc
"
)
}
"
"
"
            
source
=
source
        
)
        
+
[
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
error
-
reporting
-
automatic
"
)
                
value
=
REPLACE
(
                    
source
                    
"
errorReporting
.
automatic2
"
                    
replacements
=
{
                        
"
Mozilla
"
:
TERM_REFERENCE
(
"
vendor
-
short
-
name
"
)
                    
}
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
generic
-
error
"
)
                
value
=
MATCH
(
                    
source
                    
"
generic
.
longDesc
"
                    
start
=
"
<
p
>
"
                    
end
=
"
<
/
p
>
"
                    
replacements
=
{
                        
"
&
brandShortName
;
"
:
TERM_REFERENCE
(
"
brand
-
short
-
name
"
)
                    
}
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
load
-
error
-
try
-
again
"
)
                
value
=
MATCH
(
                    
source
                    
"
sharedLongDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
0
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
load
-
error
-
connection
"
)
                
value
=
MATCH
(
                    
source
                    
"
sharedLongDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
1
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
load
-
error
-
firewall
"
)
                
value
=
MATCH
(
                    
source
                    
"
sharedLongDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
2
                    
replacements
=
{
                        
"
&
brandShortName
;
"
:
TERM_REFERENCE
(
"
brand
-
short
-
name
"
)
                    
}
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
captive
-
portal
"
)
                
value
=
MATCH
(
                    
source
                    
"
captivePortal
.
longDesc2
"
                    
start
=
"
<
p
>
"
                    
end
=
"
<
/
p
>
"
                
)
            
)
        
]
        
+
transforms_from
(
            
"
"
"
neterror
-
dns
-
not
-
found
-
title
=
{
COPY_PATTERN
(
prev
"
dns
-
not
-
found
-
title
"
)
}
neterror
-
dns
-
not
-
found
-
with
-
suggestion
=
{
COPY_PATTERN
(
prev
"
dns
-
not
-
found
-
with
-
suggestion
"
)
}
neterror
-
dns
-
not
-
found
-
hint
-
header
=
{
COPY_PATTERN
(
prev
"
dns
-
not
-
found
-
hint
-
header
"
)
}
neterror
-
dns
-
not
-
found
-
hint
-
try
-
again
=
{
COPY_PATTERN
(
prev
"
dns
-
not
-
found
-
hint
-
try
-
again
"
)
}
neterror
-
dns
-
not
-
found
-
hint
-
check
-
network
=
{
COPY_PATTERN
(
prev
"
dns
-
not
-
found
-
hint
-
check
-
network
"
)
}
neterror
-
dns
-
not
-
found
-
hint
-
firewall
=
{
COPY_PATTERN
(
prev
"
dns
-
not
-
found
-
hint
-
firewall
"
)
}
"
"
"
            
prev
=
target
        
)
        
+
[
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
file
-
not
-
found
-
filename
"
)
                
value
=
MATCH
(
                    
source
                    
"
fileNotFound
.
longDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
0
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
file
-
not
-
found
-
moved
"
)
                
value
=
MATCH
(
                    
source
                    
"
fileNotFound
.
longDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
1
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
access
-
denied
"
)
                
value
=
MATCH
(
                    
source
                    
"
fileAccessDenied
.
longDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
0
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
unknown
-
protocol
"
)
                
value
=
MATCH
(
                    
source
                    
"
unknownProtocolFound
.
longDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
0
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
redirect
-
loop
"
)
                
value
=
MATCH
(
                    
source
                    
"
redirectLoop
.
longDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
0
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
unknown
-
socket
-
type
-
psm
-
installed
"
)
                
value
=
MATCH
(
                    
source
                    
"
unknownSocketType
.
longDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
0
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
unknown
-
socket
-
type
-
server
-
config
"
)
                
value
=
MATCH
(
                    
source
                    
"
unknownSocketType
.
longDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
1
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
not
-
cached
-
intro
"
)
                
value
=
MATCH
(
                    
source
                    
"
notCached
.
longDesc
"
                    
start
=
"
<
p
>
"
                    
end
=
"
<
/
p
>
"
                    
index
=
0
                    
replacements
=
{
                        
"
&
brandShortName
;
"
:
TERM_REFERENCE
(
"
brand
-
short
-
name
"
)
                    
}
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
not
-
cached
-
sensitive
"
)
                
value
=
MATCH
(
                    
source
                    
"
notCached
.
longDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
0
                    
replacements
=
{
                        
"
&
brandShortName
;
"
:
TERM_REFERENCE
(
"
brand
-
short
-
name
"
)
                    
}
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
not
-
cached
-
try
-
again
"
)
                
value
=
MATCH
(
                    
source
                    
"
notCached
.
longDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
1
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
net
-
offline
"
)
                
value
=
MATCH
(
                    
source
                    
"
netOffline
.
longDesc2
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
0
                    
replacements
=
{
                        
'
"
'
:
FTL
.
TextElement
(
"
"
)
                        
'
"
'
:
FTL
.
TextElement
(
"
"
)
                    
}
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
proxy
-
resolve
-
failure
-
settings
"
)
                
value
=
MATCH
(
                    
source
                    
"
proxyResolveFailure
.
longDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
0
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
proxy
-
resolve
-
failure
-
connection
"
)
                
value
=
MATCH
(
                    
source
                    
"
proxyResolveFailure
.
longDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
1
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
proxy
-
resolve
-
failure
-
firewall
"
)
                
value
=
MATCH
(
                    
source
                    
"
proxyResolveFailure
.
longDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
2
                    
replacements
=
{
                        
"
&
brandShortName
;
"
:
TERM_REFERENCE
(
"
brand
-
short
-
name
"
)
                    
}
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
proxy
-
connect
-
failure
-
settings
"
)
                
value
=
MATCH
(
                    
source
                    
"
proxyConnectFailure
.
longDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
0
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
proxy
-
connect
-
failure
-
contact
-
admin
"
)
                
value
=
MATCH
(
                    
source
                    
"
proxyConnectFailure
.
longDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
1
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
content
-
encoding
-
error
"
)
                
value
=
MATCH
(
                    
source
                    
"
contentEncodingError
.
longDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
0
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
unsafe
-
content
-
type
"
)
                
value
=
MATCH
(
                    
source
                    
"
unsafeContentType
.
longDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
0
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
nss
-
failure
-
not
-
verified
"
)
                
value
=
MATCH
(
                    
source
                    
"
nssFailure2
.
longDesc2
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
0
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
nss
-
failure
-
contact
-
website
"
)
                
value
=
MATCH
(
                    
source
                    
"
nssFailure2
.
longDesc2
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
1
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
certerror
-
intro
"
)
                
value
=
REPLACE
(
                    
source
                    
"
certerror
.
introPara2
"
                    
replacements
=
{
                        
"
&
brandShortName
;
"
:
TERM_REFERENCE
(
"
brand
-
short
-
name
"
)
                        
"
<
span
class
=
'
hostname
'
/
>
"
:
BOLD_VARIABLE_REFERENCE
(
"
hostname
"
)
                    
}
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
certerror
-
sts
-
intro
"
)
                
value
=
REPLACE
(
                    
source
                    
"
certerror
.
sts
.
introPara
"
                    
replacements
=
{
                        
"
&
brandShortName
;
"
:
TERM_REFERENCE
(
"
brand
-
short
-
name
"
)
                        
"
<
span
class
=
'
hostname
'
/
>
"
:
BOLD_VARIABLE_REFERENCE
(
"
hostname
"
)
                    
}
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
certerror
-
expired
-
cert
-
intro
"
)
                
value
=
REPLACE
(
                    
source
                    
"
certerror
.
expiredCert
.
introPara
"
                    
replacements
=
{
                        
"
&
brandShortName
;
"
:
TERM_REFERENCE
(
"
brand
-
short
-
name
"
)
                        
"
<
span
class
=
'
hostname
'
/
>
"
:
BOLD_VARIABLE_REFERENCE
(
"
hostname
"
)
                    
}
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
certerror
-
mitm
"
)
                
value
=
REPLACE
(
                    
source
                    
"
certerror
.
mitm
.
longDesc
"
                    
replacements
=
{
                        
"
<
span
class
=
'
hostname
'
>
<
/
span
>
"
:
BOLD_VARIABLE_REFERENCE
(
                            
"
hostname
"
                        
)
                        
"
<
span
class
=
'
mitm
-
name
'
/
>
"
:
BOLD_VARIABLE_REFERENCE
(
"
mitm
"
)
                    
}
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
corrupted
-
content
-
intro
"
)
                
value
=
MATCH
(
                    
source
                    
"
corruptedContentErrorv2
.
longDesc
"
                    
start
=
"
<
p
>
"
                    
end
=
"
<
/
p
>
"
                    
index
=
0
                    
replacements
=
{
                        
"
&
brandShortName
;
"
:
TERM_REFERENCE
(
"
brand
-
short
-
name
"
)
                    
}
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
corrupted
-
content
-
contact
-
website
"
)
                
value
=
MATCH
(
                    
source
                    
"
corruptedContentErrorv2
.
longDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
0
                    
replacements
=
{
                        
"
&
brandShortName
;
"
:
TERM_REFERENCE
(
"
brand
-
short
-
name
"
)
                    
}
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
sslv3
-
used
"
)
                
value
=
COPY
(
                    
source
                    
"
sslv3Used
.
longDesc2
"
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
inadequate
-
security
-
intro
"
)
                
value
=
MATCH
(
                    
source
                    
"
inadequateSecurityError
.
longDesc
"
                    
start
=
"
<
p
>
"
                    
end
=
"
<
/
p
>
"
                    
index
=
0
                    
replacements
=
{
                        
"
<
span
class
=
'
hostname
'
>
<
/
span
>
"
:
BOLD_VARIABLE_REFERENCE
(
                            
"
hostname
"
                        
)
                    
}
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
inadequate
-
security
-
code
"
)
                
value
=
MATCH
(
                    
source
                    
"
inadequateSecurityError
.
longDesc
"
                    
start
=
"
<
p
>
"
                    
end
=
"
<
/
p
>
"
                    
index
=
1
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
clock
-
skew
-
error
"
)
                
value
=
REPLACE
(
                    
source
                    
"
clockSkewError
.
longDesc
"
                    
replacements
=
{
                        
"
&
brandShortName
;
"
:
TERM_REFERENCE
(
"
brand
-
short
-
name
"
)
                        
"
<
span
class
=
'
hostname
'
>
<
/
span
>
"
:
BOLD_VARIABLE_REFERENCE
(
                            
"
hostname
"
                        
)
                        
"
<
span
id
=
'
wrongSystemTime_systemDate1
'
/
>
"
:
FTL
.
FunctionReference
(
                            
id
=
FTL
.
Identifier
(
"
DATETIME
"
)
                            
arguments
=
FTL
.
CallArguments
(
                                
positional
=
[
VARIABLE_REFERENCE
(
"
now
"
)
]
                                
named
=
[
                                    
FTL
.
NamedArgument
(
                                        
FTL
.
Identifier
(
"
dateStyle
"
)
                                        
FTL
.
StringLiteral
(
"
medium
"
)
                                    
)
                                
]
                            
)
                        
)
                    
}
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
network
-
protocol
-
error
-
intro
"
)
                
value
=
MATCH
(
                    
source
                    
"
networkProtocolError
.
longDesc
"
                    
start
=
"
<
p
>
"
                    
end
=
"
<
/
p
>
"
                    
index
=
0
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
neterror
-
network
-
protocol
-
error
-
contact
-
website
"
)
                
value
=
MATCH
(
                    
source
                    
"
networkProtocolError
.
longDesc
"
                    
start
=
"
<
li
>
"
                    
end
=
"
<
/
li
>
"
                    
index
=
0
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
certerror
-
expired
-
cert
-
second
-
para
"
)
                
value
=
REPLACE
(
                    
source
                    
"
certerror
.
expiredCert
.
secondPara2
"
                    
replacements
=
{
                        
"
&
brandShortName
;
"
:
TERM_REFERENCE
(
"
brand
-
short
-
name
"
)
                    
}
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
certerror
-
expired
-
cert
-
sts
-
second
-
para
"
)
                
value
=
REPLACE
(
                    
source
                    
"
certerror
.
expiredCert
.
sts
.
secondPara
"
                    
replacements
=
{
                        
"
&
brandShortName
;
"
:
TERM_REFERENCE
(
"
brand
-
short
-
name
"
)
                    
}
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
certerror
-
what
-
can
-
you
-
do
-
about
-
it
-
title
"
)
                
value
=
COPY
(
                    
source
                    
"
certerror
.
whatCanYouDoAboutItTitle
"
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
                    
"
certerror
-
unknown
-
issuer
-
what
-
can
-
you
-
do
-
about
-
it
-
website
"
                
)
                
value
=
MATCH
(
                    
source
                    
"
certerror
.
unknownIssuer
.
whatCanYouDoAboutIt
"
                    
start
=
"
<
p
>
"
                    
end
=
"
<
/
p
>
"
                    
index
=
0
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
                    
"
certerror
-
unknown
-
issuer
-
what
-
can
-
you
-
do
-
about
-
it
-
contact
-
admin
"
                
)
                
value
=
MATCH
(
                    
source
                    
"
certerror
.
unknownIssuer
.
whatCanYouDoAboutIt
"
                    
start
=
"
<
p
>
"
                    
end
=
"
<
/
p
>
"
                    
index
=
1
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
                    
"
certerror
-
expired
-
cert
-
what
-
can
-
you
-
do
-
about
-
it
-
clock
"
                
)
                
value
=
MATCH
(
                    
source
                    
"
certerror
.
expiredCert
.
whatCanYouDoAboutIt2
"
                    
start
=
"
<
p
>
"
                    
end
=
"
<
/
p
>
"
                    
index
=
0
                    
replacements
=
{
                        
"
<
span
class
=
'
hostname
'
/
>
"
:
BOLD_VARIABLE_REFERENCE
(
"
hostname
"
)
                        
"
<
span
id
=
'
wrongSystemTime_systemDate2
'
/
>
"
:
FTL
.
FunctionReference
(
                            
id
=
FTL
.
Identifier
(
"
DATETIME
"
)
                            
arguments
=
FTL
.
CallArguments
(
                                
positional
=
[
VARIABLE_REFERENCE
(
"
now
"
)
]
                                
named
=
[
                                    
FTL
.
NamedArgument
(
                                        
FTL
.
Identifier
(
"
dateStyle
"
)
                                        
FTL
.
StringLiteral
(
"
medium
"
)
                                    
)
                                
]
                            
)
                        
)
                    
}
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
                    
"
certerror
-
expired
-
cert
-
what
-
can
-
you
-
do
-
about
-
it
-
contact
-
website
"
                
)
                
value
=
MATCH
(
                    
source
                    
"
certerror
.
expiredCert
.
whatCanYouDoAboutIt2
"
                    
start
=
"
<
p
>
"
                    
end
=
"
<
/
p
>
"
                    
index
=
1
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
certerror
-
bad
-
cert
-
domain
-
what
-
can
-
you
-
do
-
about
-
it
"
)
                
value
=
MATCH
(
                    
source
                    
"
certerror
.
badCertDomain
.
whatCanYouDoAboutIt
"
                    
start
=
"
<
p
>
"
                    
end
=
"
<
/
p
>
"
                    
index
=
0
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
certerror
-
mitm
-
what
-
can
-
you
-
do
-
about
-
it
-
antivirus
"
)
                
value
=
COPY
(
                    
source
                    
"
certerror
.
mitm
.
whatCanYouDoAboutIt1
"
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
certerror
-
mitm
-
what
-
can
-
you
-
do
-
about
-
it
-
corporate
"
)
                
value
=
COPY
(
                    
source
                    
"
certerror
.
mitm
.
whatCanYouDoAboutIt2
"
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
certerror
-
mitm
-
what
-
can
-
you
-
do
-
about
-
it
-
attack
"
)
                
value
=
REPLACE
(
                    
source
                    
"
certerror
.
mitm
.
whatCanYouDoAboutIt3
"
                    
replacements
=
{
                        
"
<
span
class
=
'
mitm
-
name
'
/
>
"
:
BOLD_VARIABLE_REFERENCE
(
"
mitm
"
)
                    
}
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
certerror
-
mitm
-
what
-
can
-
you
-
do
-
about
-
it
-
attack
-
sts
"
)
                
value
=
REPLACE
(
                    
source
                    
"
certerror
.
mitm
.
sts
.
whatCanYouDoAboutIt3
"
                    
replacements
=
{
                        
"
<
span
class
=
'
mitm
-
name
'
/
>
"
:
BOLD_VARIABLE_REFERENCE
(
"
mitm
"
)
                    
}
                
)
            
)
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
                    
"
certerror
-
what
-
should
-
i
-
do
-
bad
-
sts
-
cert
-
explanation
"
                
)
                
value
=
REPLACE
(
                    
source
                    
"
certerror
.
whatShouldIDo
.
badStsCertExplanation1
"
                    
replacements
=
{
                        
"
&
brandShortName
;
"
:
TERM_REFERENCE
(
"
brand
-
short
-
name
"
)
                        
"
<
span
class
=
'
hostname
'
>
<
/
span
>
"
:
BOLD_VARIABLE_REFERENCE
(
                            
"
hostname
"
                        
)
                    
}
                
)
            
)
        
]
    
)
