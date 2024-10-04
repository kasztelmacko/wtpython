from cbc.cbc_profiles import generate_profiles
from cbc.cbc_survey import cbc_survey
from cbc.survey_details import survey_details
from cbc.simulate_choices import simulate_choices

import statsmodels.api as sm
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

levels = {
    "company": ["Wendy’s", "Shake Shack", "Da Dun"],
    "type": ["burger_classic", "burger_bacon", "burger_premium", "bundle_classic", "bundle_premium"],
    "portion_size": [180, 200, 220, 220, 240, 260, 240, 260, 280, 350, 380],
    "calories": [400, 450, 500, 400, 450, 500, 650, 700, 750, 830, 880, 920, 880, 920, 950],
    "price": [20, 21.99, 22.99, 20, 21.99, 22.99, 27.70, 28.10, 29.10, 30.99, 31.50, 32.99, 38.99, 40, 40.20]
}

restrictors = [
    ["type", "burger_classic", "portion_size", "in", [180, 200, 220]],
    ["type", "burger_classic", "calories", "in", [400, 450, 500]],
    ["type", "burger_classic", "price", "in", [20, 21.99, 22.99]],

    ["type", "burger_bacon", "portion_size", "in", [220, 240, 260]],
    ["type", "burger_bacon", "calories", "in", [400, 450, 500]],
    ["type", "burger_bacon", "price", "in", [20, 21.99, 22.99]],

    ["type", "burger_premium", "portion_size", "in", [240, 260, 280]],
    ["type", "burger_premium", "calories", "in", [650, 700, 750]],
    ["type", "burger_premium", "price", "in", [27.70, 28.10, 29.10]],

    ["type", "bundle_classic", "portion_size", "=", 350],
    ["type", "bundle_classic", "calories", "in", [830, 880, 920]],
    ["type", "bundle_classic", "price", "in", [30.99, 31.50, 32.99]],

    ["type", "bundle_premium", "portion_size", "=", 380],
    ["type", "bundle_premium", "calories", "in", [880, 920, 950]],
    ["type", "bundle_premium", "price", "in", [38.99, 40, 40.20]]
]

profiles = generate_profiles(levels, restrictors=restrictors)
# print(profiles)

random_survey = cbc_survey(profiles, N = 900, n_alternatives= 3, n_questions= 6, no_choice=True, method="random")
print(random_survey)