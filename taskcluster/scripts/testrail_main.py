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
lib
.
testrail_utils
import
(
    
build_milestone_description
    
build_milestone_name
    
get_release_type
    
get_release_version
    
load_testrail_credentials
)
from
slack_notifier
import
(
    
get_product_icon
    
get_taskcluster_options
    
send_error_notification
    
send_success_notification
)
SUCCESS_CHANNEL_ID
=
"
C07HUFVU2UD
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
get_release_version
(
)
    
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
        
milestone
=
testrail
.
create_milestone
(
            
testrail_project_id
milestone_name
milestone_description
        
)
        
for
device
in
devices
:
            
test_run
=
testrail
.
create_test_run
(
                
testrail_project_id
milestone
[
"
id
"
]
device
testrail_test_suite_id
            
)
            
testrail
.
update_test_run_tests
(
test_run
[
"
id
"
]
1
)
        
product_icon
=
get_product_icon
(
shipping_product
)
        
success_values
=
{
            
"
RELEASE_TYPE
"
:
release_type
            
"
RELEASE_VERSION
"
:
release_version
            
"
SHIPPING_PRODUCT
"
:
shipping_product
            
"
TESTRAIL_PROJECT_ID
"
:
testrail_project_id
            
"
TESTRAIL_PRODUCT_TYPE
"
:
testrail_product_type
            
"
PRODUCT_ICON
"
:
product_icon
        
}
        
send_success_notification
(
success_values
SUCCESS_CHANNEL_ID
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
