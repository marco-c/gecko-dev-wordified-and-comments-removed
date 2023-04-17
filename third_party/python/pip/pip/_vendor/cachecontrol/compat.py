try
:
    
from
urllib
.
parse
import
urljoin
except
ImportError
:
    
from
urlparse
import
urljoin
try
:
    
import
cPickle
as
pickle
except
ImportError
:
    
import
pickle
try
:
    
from
pip
.
_vendor
.
requests
.
packages
.
urllib3
.
response
import
HTTPResponse
except
ImportError
:
    
from
pip
.
_vendor
.
urllib3
.
response
import
HTTPResponse
try
:
    
from
pip
.
_vendor
.
requests
.
packages
.
urllib3
.
util
import
is_fp_closed
except
ImportError
:
    
from
pip
.
_vendor
.
urllib3
.
util
import
is_fp_closed
try
:
    
text_type
=
unicode
except
NameError
:
    
text_type
=
str
