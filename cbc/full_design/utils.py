import typing
import pandas as pd
import numpy as np
from itertools import permutations

def sample_random_sets(
        profiles: pd.DataFrame,
        n_alternatives: int,
        n_questions: int
):
    sets = [profiles.sample(n=n_questions, random_state=x).reset_index(drop=True) for x in range(n_alternatives)]
    for i, s in enumerate(sets):
        s["order"] = range(n_questions)
    sets = pd.concat(sets, ignore_index=True)
    sets = sets.sort_values(by='order').reset_index(drop=True)
    sets = sets.drop(columns=['order'])
    return sets
    
def repeat_sets(choice_sets,  N: int):
    repeated_sets = []
    for resp in range(1, N + 1):
        block_sets = choice_sets.copy()
        block_sets['respondent_id'] = resp
        repeated_sets.append(block_sets)
    return pd.concat(repeated_sets, ignore_index=True)