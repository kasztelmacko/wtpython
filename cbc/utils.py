import typing
import pandas as pd
import numpy as np

def add_metadata(survey: pd.DataFrame, N: int, n_alternatives: int, n_questions: int) -> pd.DataFrame:
    total_rows = N * n_alternatives * n_questions
    if len(survey) != total_rows:
        raise ValueError(f"Survey length {len(survey)} does not match expected length {total_rows}.")
    
    survey["respondent_id"] = np.repeat(np.arange(1, N + 1), n_alternatives * n_questions)
    survey["question_id"] = np.tile(np.repeat(np.arange(1, n_questions + 1), n_alternatives), N)
    survey["alternative_id"] = np.tile(np.arange(1, n_alternatives + 1), N * n_questions)
    survey["observation_id"] = np.repeat(np.arange(1, N * n_questions + 1), n_alternatives)
    return survey

def get_duplicated_observations(survey: pd.DataFrame, n_alternatives: int) -> pd.Index:
    counts = survey.groupby("observation_id")["profile_id"].nunique()
    dup_ids = counts[counts != n_alternatives].index
    dup_rows = survey[survey["observation_id"].isin(dup_ids)].index
    return dup_rows

def get_duplicated_response(survey: pd.DataFrame, N: int) -> pd.Index:
    duplicated_ids = []
    for respondent_id in survey["respondent_id"].unique():
        respondent_data = survey[survey["respondent_id"] == respondent_id]
        duplicated_ids.extend(duplicated_observation_by_response(respondent_data))
    
    dup_rows = survey[survey["observation_id"].isin(duplicated_ids)].index
    return dup_rows

def duplicated_observation_by_response(df: pd.DataFrame) -> typing.List[int]:
    profiles_list = df.groupby("observation_id")["profile_id"].apply(sorted)
    dup_df = pd.DataFrame(profiles_list.tolist(), index=profiles_list.index)
    duplicated_ids = dup_df[dup_df.duplicated()].index
    if not duplicated_ids.empty:
        return list(duplicated_ids)
    return []

def add_no_choice(survey: pd.DataFrame, n_alternatives: int) -> pd.DataFrame:
    non_numeric = survey.select_dtypes(exclude=[np.number]).columns.tolist()

    if non_numeric:
        survey = pd.get_dummies(survey, columns=non_numeric, drop_first=True)

    survey_og = survey[survey["alternative_id"] == 1].copy()
    cols_to_zero = survey.columns.difference(["respondent_id", "question_id", "alternative_id", "observation_id"])
    survey_og[cols_to_zero] = 0
    survey_og["alternative_id"] = n_alternatives + 1
    survey_og["no_choice"] = 1

    survey["no_choice"] = 0
    survey = pd.concat([survey, survey_og], ignore_index=True)
    survey = survey.sort_values(by="observation_id").reset_index(drop=True)

    return survey