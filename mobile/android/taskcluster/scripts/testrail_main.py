"
"
"
This
Python
script
automates
creating
milestones
and
test
runs
in
TestRail
and
updating
test
cases
based
on
the
results
of
automated
smoke
tests
for
different
product
releases
.
Functionality
includes
:
-
Reading
TestRail
credentials
and
environment
variables
.
-
Building
milestone
names
and
descriptions
.
-
Interacting
with
the
TestRail
API
to
create
milestones
test
runs
and
update
test
cases
.
-
Sending
notifications
to
a
specified
Slack
channel
.
"
"
"
import
os
import
sys
from
lib
.
testrail_api
import
TestRail
from
slack_notifier
import
(
    
get_taskcluster_options
    
send_error_notification
    
send_success_notification
)
from
lib
.
testrail_utils
import
(
    
build_milestone_name
    
build_milestone_description
    
get_release_version
    
get_release_type
    
load_testrail_credentials
)
SUCCESS_CHANNEL_ID
=
"
C02KDDS9QM9
"
ERROR_CHANNEL_ID
=
"
G016BC5FUHJ
"
def
main
(
)
:
    
credentials
=
load_testrail_credentials
(
"
.
testrail_credentials
.
json
"
)
    
testrail
=
TestRail
(
        
credentials
[
"
host
"
]
credentials
[
"
username
"
]
credentials
[
"
password
"
]
    
)
    
try
:
        
shipping_product
=
os
.
environ
[
"
SHIPPING_PRODUCT
"
]
        
testrail_product_type
=
os
.
environ
[
"
TESTRAIL_PRODUCT_TYPE
"
]
        
testrail_project_id
=
os
.
environ
[
"
TESTRAIL_PROJECT_ID
"
]
        
testrail_test_suite_id
=
os
.
environ
[
"
TESTRAIL_TEST_SUITE_ID
"
]
    
except
KeyError
as
e
:
        
raise
ValueError
(
f
"
ERROR
:
Missing
Environment
Variable
:
{
e
}
"
)
    
release_version
=
"
125
.
0b3
"
    
release_type
=
get_release_type
(
release_version
)
    
milestone_name
=
build_milestone_name
(
        
testrail_product_type
release_type
release_version
    
)
    
milestone_description
=
build_milestone_description
(
milestone_name
)
    
options
=
get_taskcluster_options
(
)
    
try
:
        
if
testrail
.
does_milestone_exist
(
testrail_project_id
milestone_name
)
:
            
print
(
f
"
Milestone
for
{
milestone_name
}
already
exists
.
Exiting
script
.
.
.
"
)
            
sys
.
exit
(
)
        
devices
=
[
"
Google
Pixel
3
(
Android11
)
"
"
Google
Pixel
2
(
Android11
)
"
]
        
testrail
.
create_milestone_and_test_runs
(
            
testrail_project_id
            
milestone_name
            
milestone_description
            
devices
            
testrail_test_suite_id
        
)
        
success_values
=
{
            
"
RELEASE_VERSION
"
:
release_version
            
"
RELEASE_TYPE
"
:
release_type
            
"
SHIPPING_PRODUCT
"
:
shipping_product
            
"
TESTRAIL_PRODUCT_TYPE
"
:
testrail_product_type
        
}
        
send_success_notification
(
success_values
ERROR_CHANNEL_ID
options
)
    
except
Exception
as
error_message
:
        
send_error_notification
(
str
(
error_message
)
ERROR_CHANNEL_ID
options
)
if
__name__
=
=
"
__main__
"
:
    
main
(
)
