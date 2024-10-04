import pandas as pd
from itertools import combinations

def survey_balance(survey):
    atts = [col for col in survey.columns if col not in ["respondent_id", "question_id", "alternative_id", "observation_id", "profile_id"]]
    counts = {att: survey[att].value_counts() for att in atts}
    pairs = list(combinations(atts, 2))
    counts_pair = {pair: pd.crosstab(survey[pair[0]], survey[pair[1]]) for pair in pairs}
    
    print("=====================================")
    print("Individual attribute level counts\n")
    for att, count in counts.items():
        print(f"{att} :\n{count}\n")
    
    print("=====================================")
    print("Pairwise attribute level counts\n")
    for pair in pairs:
        counts1 = counts[pair[0]]
        counts2 = counts[pair[1]]
        print(f"{pair[0]} x {pair[1]} :\n")
        combined = pd.concat([counts1, counts_pair[pair]], axis=1).fillna(0)
        print(combined)
        print("\n")

def survey_overlap(survey):
    atts = [col for col in survey.columns if col not in ["respondent_id", "question_id", "alternative_id", "observation_id", "profile_id"]]
    counts = [get_att_overlap_counts(att, survey) for att in atts]
    
    print("==============================")
    print("Counts of attribute overlap:")
    print("(# of questions with N unique levels)\n")
    
    for i in range(len(counts)):
        print(f"{atts[i]} :\n")
        print(counts[i])
        print("\n")

def get_att_overlap_counts(x, survey):
    counts = survey.groupby('observation_id')[x].nunique()
    counts = counts.value_counts().sort_index()
    counts.index = range(1, len(counts) + 1)  # Renaming index to start from 1
    return counts