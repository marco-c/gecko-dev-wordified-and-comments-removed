from
collections
import
defaultdict
from
.
platforms
import
PLATFORMS
SUPPORTED_ATTRIBUTES
=
(
    
"
domain
"
    
"
repo
"
    
"
owner
"
    
"
path_raw
"
    
"
groups_path
"
    
"
_user
"
    
"
port
"
    
"
url
"
    
"
platform
"
    
"
protocol
"
)
def
parse
(
url
check_domain
=
True
)
:
    
parsed_info
=
defaultdict
(
lambda
:
None
)
    
parsed_info
[
"
port
"
]
=
"
"
    
parsed_info
[
"
path_raw
"
]
=
"
"
    
parsed_info
[
"
groups_path
"
]
=
"
"
    
map
(
parsed_info
.
setdefault
SUPPORTED_ATTRIBUTES
)
    
for
name
platform
in
PLATFORMS
:
        
for
protocol
regex
in
platform
.
COMPILED_PATTERNS
.
items
(
)
:
            
match
=
regex
.
match
(
url
)
            
if
not
match
:
                
continue
            
domain
=
match
.
group
(
"
domain
"
)
            
if
check_domain
:
                
if
platform
.
DOMAINS
and
not
(
domain
in
platform
.
DOMAINS
)
:
                    
continue
                
if
platform
.
SKIP_DOMAINS
and
domain
in
platform
.
SKIP_DOMAINS
:
                    
continue
            
parsed_info
.
update
(
platform
.
DEFAULTS
)
            
matches
=
platform
.
clean_data
(
match
.
groupdict
(
default
=
"
"
)
)
            
parsed_info
.
update
(
matches
)
            
parsed_info
.
update
(
                
{
                    
"
url
"
:
url
                    
"
platform
"
:
name
                    
"
protocol
"
:
protocol
                
}
            
)
            
return
parsed_info
    
return
parsed_info
