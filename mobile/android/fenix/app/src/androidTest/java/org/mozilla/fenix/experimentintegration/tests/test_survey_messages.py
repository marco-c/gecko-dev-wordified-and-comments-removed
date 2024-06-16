import
pytest
pytest
.
mark
.
messaging_survey
def
test_survey_navigates_correctly
(
setup_experiment
gradlewbuild
)
:
    
setup_experiment
(
)
    
gradlewbuild
.
test
(
"
SurveyExperimentIntegrationTest
#
checkSurveyNavigatesCorrectly
"
)
pytest
.
mark
.
messaging_survey
def
test_survey_no_thanks_navigates_correctly
(
setup_experiment
gradlewbuild
)
:
    
setup_experiment
(
)
    
gradlewbuild
.
test
(
        
"
SurveyExperimentIntegrationTest
#
checkSurveyNoThanksNavigatesCorrectly
"
    
)
pytest
.
mark
.
messaging_homescreen
def
test_homescreen_survey_dismisses_correctly
(
setup_experiment
gradlewbuild
)
:
    
setup_experiment
(
)
    
gradlewbuild
.
test
(
        
"
SurveyExperimentIntegrationTest
#
checkHomescreenSurveyDismissesCorrectly
"
    
)
pytest
.
mark
.
messaging_survey
def
test_survey_landscape_looks_correct
(
setup_experiment
gradlewbuild
)
:
    
setup_experiment
(
)
    
gradlewbuild
.
test
(
        
"
SurveyExperimentIntegrationTest
#
checkSurveyLandscapeLooksCorrect
"
    
)
