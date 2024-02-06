import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.utils import resample
import patsy

# Import data
df = pd.read_csv('/Users/savannahellison/Dropbox/phdee/hw3/kwh.csv')

# Apply logarithmic transformation to relevant columns
df['log_electricity'] = np.log(df['electricity'])
df['log_sqft'] = np.log(df['sqft'])
df['log_temp'] = np.log(df['temp'])

# Define the model formula
model_formula = 'log_electricity ~ retrofit + log_sqft + log_temp'

# Create the OLS model using patsy
y, X = patsy.dmatrices(model_formula, data=df, return_type='dataframe')

# Fit the model
ols_results = sm.OLS(y, X).fit()

# Function to calculate average marginal effects manually for OLS
def calculate_marginal_effects_ols(model, data):
    derivatives = model.params.drop('Intercept')  # Drop the intercept term

    # Initialize marginal effects with zeros
    marginal_effects = pd.DataFrame(0, index=data.index, columns=derivatives.index)

    for variable in derivatives.index:
        if ':' in variable:
            # Interaction term
            variable_name, interaction_name = variable.split(':')
            marginal_effects[variable_name] += data[interaction_name] * derivatives[variable]

        else:
            # Non-interaction term
            marginal_effects[variable] = data[variable] * derivatives[variable]

    return marginal_effects.sum(axis=1)

# Function to perform bootstrap replication
def bootstrap_replication(data):
    bootstrap_sample = resample(data, replace=True, random_state=42)
    bootstrap_sample.reset_index(drop=True, inplace=True)
    bootstrap_model = sm.OLS(y.loc[bootstrap_sample.index], X.loc[bootstrap_sample.index])
    bootstrap_model_results = bootstrap_model.fit()
    bootstrap_marginal_effects = calculate_marginal_effects_ols(bootstrap_model_results, X.loc[bootstrap_sample.index])
    return np.asarray(bootstrap_model_results.params).reshape(-1, 1), np.asarray(bootstrap_marginal_effects).reshape(-1, 1)

# Number of bootstrap replications
num_replications = 1000

# Lists to store coefficient and marginal effect estimates
coefficients = []
marginal_effects = []

# Perform bootstrap replications
for _ in range(num_replications):
    bootstrap_coefficients, bootstrap_marginal_effects = bootstrap_replication(df)
    coefficients.append(bootstrap_coefficients)
    marginal_effects.append(bootstrap_marginal_effects)

# Convert lists to DataFrames
coefficients_df = pd.DataFrame(np.vstack(coefficients), columns=X.design_info.column_names)
marginal_effects_df = pd.DataFrame(np.vstack(marginal_effects), columns=X.design_info.column_names)

# Calculate confidence intervals
coefficients_ci = coefficients_df.apply(lambda col: col.quantile([0.025, 0.975]))
marginal_effects_ci = marginal_effects_df.apply(lambda col: col.quantile([0.025, 0.975]))

# Display the results
result_table = pd.DataFrame({
    'Variable': coefficients_df.columns,
    'Coefficient Estimate': ols_results.params,
    'CI Lower (Coefficients)': coefficients_ci.loc[0.025],
    'CI Upper (Coefficients)': coefficients_ci.loc[0.975],
    'Marginal Effect Estimate': marginal_effects_df.mean(),
    'CI Lower (Marginal Effects)': marginal_effects_ci.loc[0.025],
    'CI Upper (Marginal Effects)': marginal_effects_ci.loc[0.975],
})

print(result_table)
