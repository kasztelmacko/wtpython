import pandas as pd
import numpy as np

def simulate_choices(survey: pd.DataFrame, obsID: str = "observation_id") -> pd.DataFrame:
    return simulate_choices_rand(survey, obsID)


def simulate_choices_rand(survey: pd.DataFrame, obsID: str) -> pd.DataFrame:
    nrows = survey[obsID].value_counts()
    choices = []
    for n in nrows:
        choice = np.zeros(n)
        choice[np.random.choice(n)] = 1
        choices.append(choice)
    survey['choice'] = np.concatenate(choices)
    return survey
