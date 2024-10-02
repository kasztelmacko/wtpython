from cbc.cbc_profiles import generate_profiles
from cbc.cbc_survey import cbc_survey

levels = {
    "price": [1,2,3,4],
    "type": ["Fuji", "Gala", "Honeycrisp"],
    "freshnes": ['Poor', 'Average', 'Excellent'],
}

restrictors = [["type", "Fuji", "price", "<=", 2]]

profiles = generate_profiles(levels, restrictors)
print(profiles)

random_survey = cbc_survey(profiles, N = 900, n_alternatives= 3, n_questions= 6, no_choice=True, method="random")
print(random_survey)