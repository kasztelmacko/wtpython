import typing
from itertools import product
import pandas as pd

def generate_profiles(levels: dict, restrictors: list = None) -> pd.DataFrame:
    profiles = pd.DataFrame(list(product(*levels.values())), columns=levels.keys())
    profiles = restrict_profiles(profiles, restrictors)
    profiles = profiles.reset_index(drop=True)
    profiles["profile_id"] = profiles.index
    return profiles

def restrict_profiles(profiles: pd.DataFrame, restrictors: list) -> pd.DataFrame:
    if not restrictors:
        return profiles
    query_str = ""
    for restrictor in restrictors:
        if len(restrictor) == 2:
            column_to_check, value_to_check = restrictor
            restriction = f"~({column_to_check} == '{value_to_check}')"
        else:
            column_to_check, value_to_check, column_to_filter, operator, threshold = restrictor
            if operator == "in":
                threshold_str = "(" + ", ".join(map(str, threshold)) + ")"
                restriction = f"~(({column_to_check} == '{value_to_check}') & ({column_to_filter} {operator} {threshold_str}))"
            elif operator == "=":
                restriction = f"~(({column_to_check} == '{value_to_check}') & ({column_to_filter} == {threshold}))"
            else:
                restriction = f"~(({column_to_check} == '{value_to_check}') & ({column_to_filter} {operator} {threshold}))"

        if query_str:
            query_str += " & " + restriction
        else:
            query_str = restriction

    filtered_profiles = profiles.query(query_str)
    return filtered_profiles

