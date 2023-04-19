import
network_tester_config_pb2
def
AddConfig
(
all_configs
packet_send_interval_ms
packet_size
              
execution_time_ms
)
:
    
config
=
all_configs
.
configs
.
add
(
)
    
config
.
packet_send_interval_ms
=
packet_send_interval_ms
    
config
.
packet_size
=
packet_size
    
config
.
execution_time_ms
=
execution_time_ms
def
main
(
)
:
    
all_configs
=
network_tester_config_pb2
.
NetworkTesterAllConfigs
(
)
    
AddConfig
(
all_configs
10
50
200
)
    
AddConfig
(
all_configs
10
100
200
)
    
with
open
(
"
network_tester_config
.
dat
"
'
wb
'
)
as
f
:
        
f
.
write
(
all_configs
.
SerializeToString
(
)
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
