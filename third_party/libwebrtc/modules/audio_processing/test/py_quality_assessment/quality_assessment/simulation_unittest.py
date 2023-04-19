"
"
"
Unit
tests
for
the
simulation
module
.
"
"
"
import
logging
import
os
import
shutil
import
tempfile
import
unittest
import
mock
import
pydub
from
.
import
audioproc_wrapper
from
.
import
eval_scores_factory
from
.
import
evaluation
from
.
import
external_vad
from
.
import
signal_processing
from
.
import
simulation
from
.
import
test_data_generation_factory
class
TestApmModuleSimulator
(
unittest
.
TestCase
)
:
    
"
"
"
Unit
tests
for
the
ApmModuleSimulator
class
.
  
"
"
"
    
def
setUp
(
self
)
:
        
"
"
"
Create
temporary
folders
and
fake
audio
track
.
"
"
"
        
self
.
_output_path
=
tempfile
.
mkdtemp
(
)
        
self
.
_tmp_path
=
tempfile
.
mkdtemp
(
)
        
silence
=
pydub
.
AudioSegment
.
silent
(
duration
=
1000
frame_rate
=
48000
)
        
fake_signal
=
signal_processing
.
SignalProcessingUtils
.
GenerateWhiteNoise
(
            
silence
)
        
self
.
_fake_audio_track_path
=
os
.
path
.
join
(
self
.
_output_path
                                                   
'
fake
.
wav
'
)
        
signal_processing
.
SignalProcessingUtils
.
SaveWav
(
            
self
.
_fake_audio_track_path
fake_signal
)
    
def
tearDown
(
self
)
:
        
"
"
"
Recursively
delete
temporary
folders
.
"
"
"
        
shutil
.
rmtree
(
self
.
_output_path
)
        
shutil
.
rmtree
(
self
.
_tmp_path
)
    
def
testSimulation
(
self
)
:
        
ap_wrapper
=
audioproc_wrapper
.
AudioProcWrapper
(
            
audioproc_wrapper
.
AudioProcWrapper
.
DEFAULT_APM_SIMULATOR_BIN_PATH
)
        
evaluator
=
evaluation
.
ApmModuleEvaluator
(
)
        
ap_wrapper
.
Run
=
mock
.
MagicMock
(
name
=
'
Run
'
)
        
evaluator
.
Run
=
mock
.
MagicMock
(
name
=
'
Run
'
)
        
test_data_generator_factory
=
(
            
test_data_generation_factory
.
TestDataGeneratorFactory
(
                
aechen_ir_database_path
=
'
'
                
noise_tracks_path
=
'
'
                
copy_with_identity
=
False
)
)
        
evaluation_score_factory
=
eval_scores_factory
.
EvaluationScoreWorkerFactory
(
            
polqa_tool_bin_path
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
dirname
(
__file__
)
                                             
'
fake_polqa
'
)
            
echo_metric_tool_bin_path
=
None
)
        
simulator
=
simulation
.
ApmModuleSimulator
(
            
test_data_generator_factory
=
test_data_generator_factory
            
evaluation_score_factory
=
evaluation_score_factory
            
ap_wrapper
=
ap_wrapper
            
evaluator
=
evaluator
            
external_vads
=
{
                
'
fake
'
:
                
external_vad
.
ExternalVad
(
                    
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
dirname
(
__file__
)
                                 
'
fake_external_vad
.
py
'
)
'
fake
'
)
            
}
)
        
config_files
=
[
'
apm_configs
/
default
.
json
'
]
        
input_files
=
[
self
.
_fake_audio_track_path
]
        
test_data_generators
=
[
'
identity
'
'
white_noise
'
]
        
eval_scores
=
[
'
audio_level_mean
'
'
polqa
'
]
        
simulator
.
Run
(
config_filepaths
=
config_files
                      
capture_input_filepaths
=
input_files
                      
test_data_generator_names
=
test_data_generators
                      
eval_score_names
=
eval_scores
                      
output_dir
=
self
.
_output_path
)
        
min_number_of_simulations
=
len
(
config_files
)
*
len
(
input_files
)
*
len
(
            
test_data_generators
)
        
self
.
assertGreaterEqual
(
len
(
ap_wrapper
.
Run
.
call_args_list
)
                                
min_number_of_simulations
)
        
self
.
assertGreaterEqual
(
len
(
evaluator
.
Run
.
call_args_list
)
                                
min_number_of_simulations
)
    
def
testInputSignalCreation
(
self
)
:
        
simulator
=
simulation
.
ApmModuleSimulator
(
            
test_data_generator_factory
=
(
                
test_data_generation_factory
.
TestDataGeneratorFactory
(
                    
aechen_ir_database_path
=
'
'
                    
noise_tracks_path
=
'
'
                    
copy_with_identity
=
False
)
)
            
evaluation_score_factory
=
(
                
eval_scores_factory
.
EvaluationScoreWorkerFactory
(
                    
polqa_tool_bin_path
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
dirname
(
__file__
)
                                                     
'
fake_polqa
'
)
                    
echo_metric_tool_bin_path
=
None
)
)
            
ap_wrapper
=
audioproc_wrapper
.
AudioProcWrapper
(
                
audioproc_wrapper
.
AudioProcWrapper
.
                
DEFAULT_APM_SIMULATOR_BIN_PATH
)
            
evaluator
=
evaluation
.
ApmModuleEvaluator
(
)
)
        
input_files
=
[
            
os
.
path
.
join
(
self
.
_tmp_path
'
pure_tone
-
440_1000
.
wav
'
)
            
os
.
path
.
join
(
self
.
_tmp_path
'
pure_tone
-
1000_500
.
wav
'
)
        
]
        
self
.
assertFalse
(
            
any
(
[
os
.
path
.
exists
(
input_file
)
for
input_file
in
(
input_files
)
]
)
)
        
simulator
.
Run
(
config_filepaths
=
[
'
apm_configs
/
default
.
json
'
]
                      
capture_input_filepaths
=
input_files
                      
test_data_generator_names
=
[
'
identity
'
]
                      
eval_score_names
=
[
'
audio_level_peak
'
]
                      
output_dir
=
self
.
_output_path
)
        
self
.
assertTrue
(
            
all
(
[
os
.
path
.
exists
(
input_file
)
for
input_file
in
(
input_files
)
]
)
)
    
def
testPureToneGenerationWithTotalHarmonicDistorsion
(
self
)
:
        
logging
.
warning
=
mock
.
MagicMock
(
name
=
'
warning
'
)
        
simulator
=
simulation
.
ApmModuleSimulator
(
            
test_data_generator_factory
=
(
                
test_data_generation_factory
.
TestDataGeneratorFactory
(
                    
aechen_ir_database_path
=
'
'
                    
noise_tracks_path
=
'
'
                    
copy_with_identity
=
False
)
)
            
evaluation_score_factory
=
(
                
eval_scores_factory
.
EvaluationScoreWorkerFactory
(
                    
polqa_tool_bin_path
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
dirname
(
__file__
)
                                                     
'
fake_polqa
'
)
                    
echo_metric_tool_bin_path
=
None
)
)
            
ap_wrapper
=
audioproc_wrapper
.
AudioProcWrapper
(
                
audioproc_wrapper
.
AudioProcWrapper
.
                
DEFAULT_APM_SIMULATOR_BIN_PATH
)
            
evaluator
=
evaluation
.
ApmModuleEvaluator
(
)
)
        
config_files
=
[
'
apm_configs
/
default
.
json
'
]
        
input_files
=
[
os
.
path
.
join
(
self
.
_tmp_path
'
pure_tone
-
440_1000
.
wav
'
)
]
        
eval_scores
=
[
'
thd
'
]
        
simulator
.
Run
(
config_filepaths
=
config_files
                      
capture_input_filepaths
=
input_files
                      
test_data_generator_names
=
[
'
identity
'
]
                      
eval_score_names
=
eval_scores
                      
output_dir
=
self
.
_output_path
)
        
self
.
assertFalse
(
logging
.
warning
.
called
)
        
simulator
.
Run
(
            
config_filepaths
=
config_files
            
capture_input_filepaths
=
input_files
            
test_data_generator_names
=
[
'
white_noise
'
]
            
eval_score_names
=
eval_scores
            
output_dir
=
self
.
_output_path
)
        
logging
.
warning
.
assert_called_with
(
'
the
evaluation
failed
:
%
s
'
(
            
'
The
THD
score
cannot
be
used
with
any
test
data
generator
other
than
'
            
'
"
identity
"
'
)
)
