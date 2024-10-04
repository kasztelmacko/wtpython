import typing
import pandas as pd

from cbc.random_design.random_survey import random_survey
from cbc.full_design.full_survey import full_survey

def cbc_survey(
        profiles: pd.DataFrame,
        N: int,
        n_alternatives: int,
        n_questions: int,
        no_choice: bool,
        method: str,
):
    if method == "random":
        survey = random_survey(
            profiles, 
            N,
            n_alternatives,
            n_questions,
            no_choice
        )

    elif method == "full":
        survey = full_survey(
            profiles,
            N,
            n_alternatives,
            n_questions,
            no_choice
        )

    return survey