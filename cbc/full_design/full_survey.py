import typing
import pandas as pd
import numpy as np

from cbc.utils import ( add_metadata,
                        get_duplicated_observations,
                        get_duplicated_response,
                        add_no_choice
                        )

from cbc.full_design.utils import (sample_random_sets,
                                   repeat_sets)

def full_survey(
        profiles: pd.DataFrame,
        N: int,
        n_alternatives: int,
        n_questions: int,
        no_choice: bool
) -> pd.DataFrame:
    
    survey = sample_random_sets(profiles, n_alternatives, n_questions)
    survey = repeat_sets(survey, N)
    survey = add_metadata(survey, N, n_alternatives, n_questions)
    duplicated_observation_rows = get_duplicated_observations(survey, n_alternatives)
    duplicated_response_rows = get_duplicated_response(survey, N)
    
    while len(duplicated_observation_rows) > 0 or len(duplicated_response_rows) > 0:
        survey = sample_random_sets(profiles, n_alternatives, n_questions)
        survey = repeat_sets(survey, N)
        survey = add_metadata(survey, N, n_alternatives, n_questions)
        duplicated_observation_rows = get_duplicated_observations(survey, n_alternatives)
        duplicated_response_rows = get_duplicated_response(survey, N)
    
    if no_choice:
        survey = add_no_choice(survey, n_alternatives)
    
    return survey