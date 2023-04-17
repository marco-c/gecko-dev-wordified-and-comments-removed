from
.
base
import
NullBrowser
from
.
edge
import
(
EdgeBrowser
                   
EdgeDriverWdspecExecutor
                   
check_args
                   
browser_kwargs
                   
executor_kwargs
                   
env_extras
                   
env_options
                   
run_info_extras
                   
get_timeout_multiplier
)
from
.
.
executors
.
executorwebdriver
import
(
WebDriverTestharnessExecutor
                                           
WebDriverRefTestExecutor
)
__wptrunner__
=
{
"
product
"
:
"
edge_webdriver
"
                 
"
check_args
"
:
"
check_args
"
                 
"
browser
"
:
{
None
:
"
EdgeBrowser
"
                             
"
wdspec
"
:
"
NullBrowser
"
}
                 
"
executor
"
:
{
"
testharness
"
:
"
WebDriverTestharnessExecutor
"
                              
"
reftest
"
:
"
WebDriverRefTestExecutor
"
                              
"
wdspec
"
:
"
EdgeDriverWdspecExecutor
"
}
                 
"
browser_kwargs
"
:
"
browser_kwargs
"
                 
"
executor_kwargs
"
:
"
executor_kwargs
"
                 
"
env_extras
"
:
"
env_extras
"
                 
"
env_options
"
:
"
env_options
"
                 
"
run_info_extras
"
:
"
run_info_extras
"
                 
"
timeout_multiplier
"
:
"
get_timeout_multiplier
"
}
