import pandas as pd
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("choice_results.csv")

X = df.drop(columns=['profile_id', 'respondent_id', 'question_id', 'alternative_id', 'observation_id', 'choice', ])
X = sm.add_constant(X)
y = df['choice']

model = sm.Logit(y, X)
result = model.fit()
print(result.summary())

coefficients = result.params
price_coefficient = -coefficients['price']

wtp = {}
for attribute in coefficients.index:
    if attribute != 'price' and attribute != 'const':
        wtp[attribute] = coefficients[attribute] / price_coefficient

for attribute, value in wtp.items():
    print(f"Willingness to Pay for {attribute}: {value:.2f}")