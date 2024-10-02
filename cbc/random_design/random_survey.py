import typing
import pandas as pd
import numpy as np

from cbc.utils import (add_metadata,
                        get_duplicated_observations,
                        get_duplicated_response,
                        add_no_choice
                        )

from cbc.random_design.utils import sample_profiles

def random_survey(
            profiles: pd.DataFrame, 
            N: int,
            n_alternatives: int,
            n_questions: int,
            no_choice: bool
) -> pd.DataFrame:
    
    survey = sample_profiles(profiles, size = N * n_alternatives * n_questions)
    survey = add_metadata(survey, N, n_alternatives, n_questions)

    duplicated_observation_rows = get_duplicated_observations(survey, n_alternatives)
    duplicated_response_rows = get_duplicated_response(survey, N)

    while len(duplicated_observation_rows) > 0 or len(duplicated_response_rows) > 0:
        dup_rows = np.unique(np.concatenate((duplicated_observation_rows, duplicated_response_rows)))
        new_rows = sample_profiles(profiles, size=len(dup_rows))
        survey.iloc[dup_rows, :new_rows.shape[1]] = new_rows.values

        duplicated_observation_rows = get_duplicated_observations(survey, n_alternatives)
        duplicated_response_rows = get_duplicated_response(survey, N)

    if no_choice:
        survey = add_no_choice(survey, n_alternatives)

    return survey