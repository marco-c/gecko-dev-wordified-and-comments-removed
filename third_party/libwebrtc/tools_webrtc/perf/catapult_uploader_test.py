import
os
import
sys
import
unittest
from
unittest
.
mock
import
MagicMock
def
_ConfigurePythonPath
(
)
:
  
script_dir
=
os
.
path
.
dirname
(
os
.
path
.
realpath
(
__file__
)
)
  
checkout_root
=
os
.
path
.
abspath
(
os
.
path
.
join
(
script_dir
os
.
pardir
                                               
os
.
pardir
)
)
  
sys
.
path
.
insert
(
      
0
os
.
path
.
join
(
checkout_root
'
third_party
'
'
catapult
'
'
tracing
'
)
)
  
sys
.
path
.
insert
(
      
0
os
.
path
.
join
(
checkout_root
'
third_party
'
'
protobuf
'
'
python
'
)
)
  
histogram_proto_path
=
os
.
path
.
join
(
os
.
path
.
join
(
'
.
.
/
.
.
/
out
/
Default
'
)
                                      
'
pyproto
'
'
tracing
'
'
tracing
'
'
proto
'
)
  
sys
.
path
.
insert
(
0
histogram_proto_path
)
  
from
tracing
.
proto
import
histogram_proto
  
if
not
histogram_proto
.
HAS_PROTO
:
    
raise
ImportError
(
'
Could
not
find
histogram_pb2
.
You
need
to
build
the
'
                      
'
webrtc_dashboard_upload
target
before
invoking
this
'
                      
'
script
.
Expected
to
find
'
                      
'
histogram_pb2
.
py
in
%
s
.
'
%
histogram_proto_path
)
def
_CreateHistogram
(
name
=
'
hist
'
                     
master
=
None
                     
bot
=
None
                     
benchmark
=
None
                     
benchmark_description
=
None
                     
commit_position
=
None
                     
samples
=
None
)
:
  
hists
=
[
catapult_uploader
.
histogram
.
Histogram
(
name
'
count
'
)
]
  
if
samples
:
    
for
s
in
samples
:
      
hists
[
0
]
.
AddSample
(
s
)
  
histograms
=
catapult_uploader
.
histogram_set
.
HistogramSet
(
hists
)
  
if
master
:
    
histograms
.
AddSharedDiagnosticToAllHistograms
(
        
catapult_uploader
.
reserved_infos
.
MASTERS
.
name
        
catapult_uploader
.
generic_set
.
GenericSet
(
[
master
]
)
)
  
if
bot
:
    
histograms
.
AddSharedDiagnosticToAllHistograms
(
        
catapult_uploader
.
reserved_infos
.
BOTS
.
name
        
catapult_uploader
.
generic_set
.
GenericSet
(
[
bot
]
)
)
  
if
commit_position
:
    
histograms
.
AddSharedDiagnosticToAllHistograms
(
        
catapult_uploader
.
reserved_infos
.
CHROMIUM_COMMIT_POSITIONS
.
name
        
catapult_uploader
.
generic_set
.
GenericSet
(
[
commit_position
]
)
)
  
if
benchmark
:
    
histograms
.
AddSharedDiagnosticToAllHistograms
(
        
catapult_uploader
.
reserved_infos
.
BENCHMARKS
.
name
        
catapult_uploader
.
generic_set
.
GenericSet
(
[
benchmark
]
)
)
  
if
benchmark_description
:
    
histograms
.
AddSharedDiagnosticToAllHistograms
(
        
catapult_uploader
.
reserved_infos
.
BENCHMARK_DESCRIPTIONS
.
name
        
catapult_uploader
.
generic_set
.
GenericSet
(
[
benchmark_description
]
)
)
  
return
histograms
class
CatapultUploaderTest
(
unittest
.
TestCase
)
:
  
def
setUp
(
self
)
:
    
mock
=
MagicMock
(
return_value
=
[
200
None
]
)
    
catapult_uploader
.
httplib2
.
Http
.
request
=
mock
    
self
.
histogram
=
_CreateHistogram
(
        
master
=
'
master
'
        
bot
=
'
bot
'
        
benchmark
=
'
benchmark
'
        
commit_position
=
123
        
benchmark_description
=
'
Benchmark
description
.
'
        
samples
=
[
1
2
3
]
)
  
def
testSendHistogramsSet
(
self
)
:
    
url
=
'
http
:
/
/
notlocalhost
'
    
response
content
=
catapult_uploader
.
_SendHistogramSet
(
url
self
.
histogram
)
    
self
.
assertEqual
(
response
200
)
    
self
.
assertEqual
(
content
None
)
  
def
testSendHistogramsSetLocalhost
(
self
)
:
    
url
=
'
http
:
/
/
localhost
'
    
response
content
=
catapult_uploader
.
_SendHistogramSet
(
url
self
.
histogram
)
    
self
.
assertEqual
(
response
200
)
    
self
.
assertEqual
(
content
None
)
if
(
__name__
)
=
=
'
__main__
'
:
  
_ConfigurePythonPath
(
)
  
import
catapult_uploader
  
unittest
.
main
(
)
