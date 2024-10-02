import typing
import pandas as pd
import numpy as np

def sample_profiles(profiles: pd.DataFrame, size: int) -> pd.DataFrame:
    return profiles.sample(n=size, replace=True).reset_index(drop=True)


