import
sys
try
:
    
if
sys
.
version_info
<
(
3
5
)
:
        
raise
ImportError
(
"
Fallback
to
vendored
code
"
)
    
from
ssl
import
CertificateError
match_hostname
except
ImportError
:
    
try
:
        
from
backports
.
ssl_match_hostname
import
CertificateError
match_hostname
    
except
ImportError
:
        
from
.
_implementation
import
CertificateError
match_hostname
__all__
=
(
'
CertificateError
'
'
match_hostname
'
)
