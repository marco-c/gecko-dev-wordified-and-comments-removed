"
"
"
Copied
from
raven
-
python
.
Used
for
DjangoIntegration
(
transaction_fron
=
"
raven_legacy
"
)
.
"
"
"
from
__future__
import
absolute_import
import
re
from
sentry_sdk
.
_types
import
MYPY
if
MYPY
:
    
from
django
.
urls
.
resolvers
import
URLResolver
    
from
typing
import
Dict
    
from
typing
import
List
    
from
typing
import
Optional
    
from
django
.
urls
.
resolvers
import
URLPattern
    
from
typing
import
Tuple
    
from
typing
import
Union
    
from
re
import
Pattern
try
:
    
from
django
.
urls
import
get_resolver
except
ImportError
:
    
from
django
.
core
.
urlresolvers
import
get_resolver
def
get_regex
(
resolver_or_pattern
)
:
    
"
"
"
Utility
method
for
django
'
s
deprecated
resolver
.
regex
"
"
"
    
try
:
        
regex
=
resolver_or_pattern
.
regex
    
except
AttributeError
:
        
regex
=
resolver_or_pattern
.
pattern
.
regex
    
return
regex
class
RavenResolver
(
object
)
:
    
_optional_group_matcher
=
re
.
compile
(
r
"
\
(
\
?
\
:
(
[
^
\
)
]
+
)
\
)
"
)
    
_named_group_matcher
=
re
.
compile
(
r
"
\
(
\
?
P
<
(
\
w
+
)
>
[
^
\
)
]
+
\
)
"
)
    
_non_named_group_matcher
=
re
.
compile
(
r
"
\
(
[
^
\
)
]
+
\
)
"
)
    
_either_option_matcher
=
re
.
compile
(
r
"
\
[
(
[
^
\
]
]
+
)
\
|
(
[
^
\
]
]
+
)
\
]
"
)
    
_camel_re
=
re
.
compile
(
r
"
(
[
A
-
Z
]
+
)
(
[
a
-
z
]
)
"
)
    
_cache
=
{
}
    
def
_simplify
(
self
pattern
)
:
        
r
"
"
"
        
Clean
up
urlpattern
regexes
into
something
readable
by
humans
:
        
From
:
        
>
"
^
(
?
P
<
sport_slug
>
\
w
+
)
/
athletes
/
(
?
P
<
athlete_slug
>
\
w
+
)
/
"
        
To
:
        
>
"
{
sport_slug
}
/
athletes
/
{
athlete_slug
}
/
"
        
"
"
"
        
result
=
self
.
_optional_group_matcher
.
sub
(
lambda
m
:
"
%
s
"
%
m
.
group
(
1
)
pattern
)
        
result
=
self
.
_named_group_matcher
.
sub
(
lambda
m
:
"
{
%
s
}
"
%
m
.
group
(
1
)
result
)
        
result
=
self
.
_non_named_group_matcher
.
sub
(
"
{
var
}
"
result
)
        
result
=
self
.
_either_option_matcher
.
sub
(
lambda
m
:
m
.
group
(
1
)
result
)
        
result
=
(
            
result
.
replace
(
"
^
"
"
"
)
            
.
replace
(
"
"
"
"
)
            
.
replace
(
"
?
"
"
"
)
            
.
replace
(
"
/
/
"
"
/
"
)
            
.
replace
(
"
\
\
"
"
"
)
        
)
        
return
result
    
def
_resolve
(
self
resolver
path
parents
=
None
)
:
        
match
=
get_regex
(
resolver
)
.
search
(
path
)
        
if
not
match
:
            
return
None
        
if
parents
is
None
:
            
parents
=
[
resolver
]
        
elif
resolver
not
in
parents
:
            
parents
=
parents
+
[
resolver
]
        
new_path
=
path
[
match
.
end
(
)
:
]
        
for
pattern
in
resolver
.
url_patterns
:
            
if
not
pattern
.
callback
:
                
match_
=
self
.
_resolve
(
pattern
new_path
parents
)
                
if
match_
:
                    
return
match_
                
continue
            
elif
not
get_regex
(
pattern
)
.
search
(
new_path
)
:
                
continue
            
try
:
                
return
self
.
_cache
[
pattern
]
            
except
KeyError
:
                
pass
            
prefix
=
"
"
.
join
(
self
.
_simplify
(
get_regex
(
p
)
.
pattern
)
for
p
in
parents
)
            
result
=
prefix
+
self
.
_simplify
(
get_regex
(
pattern
)
.
pattern
)
            
if
not
result
.
startswith
(
"
/
"
)
:
                
result
=
"
/
"
+
result
            
self
.
_cache
[
pattern
]
=
result
            
return
result
        
return
None
    
def
resolve
(
        
self
        
path
        
urlconf
=
None
    
)
:
        
resolver
=
get_resolver
(
urlconf
)
        
match
=
self
.
_resolve
(
resolver
path
)
        
return
match
or
path
LEGACY_RESOLVER
=
RavenResolver
(
)
