#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 17:29:30 2024

@author: savannahellison
"""
import pandas as pd
import statsmodels.api as sm
from linearmodels.iv import IVGMM
import os
#set output path
outputpath = r'/Users/savannahellison/Dropbox/phdee/hw5/output'

# import data

df = pd.read_csv(r'/Users/savannahellison/Dropbox/phdee/hw5/instrumentalvehicles.csv')

print(df)

# Run OLS price on mpg and car
# Add a constant term to the independent variables
df['const'] = 1

# Define the independent variables
X = df[['mpg', 'car', 'const']]

# Define the dependent variable
y = df['price']

# Fit the OLS regression model
model = sm.OLS(y, X).fit()

# Print the summary of the regression results
print(model.summary())

# Initialize an empty list to store the results
results_list = []

# Initialize an empty list to store the results
results_list = []

# 3a first stage
X_first_stage = df[['weight', 'car', 'const']]
y_first_stage = df['mpg']

# Fit the first stage OLS regression model
first_stage_model = sm.OLS(y_first_stage, X_first_stage).fit()

# Store the first stage F-statistic
first_stage_f_statistic = first_stage_model.fvalue

# Obtain fitted values from the first stage
df['mpg_hat'] = first_stage_model.fittedvalues

# 3a second stage
X_second_stage = df[['mpg_hat', 'car', 'const']]  # Use fitted values from the first stage
y_second_stage = df['price']

# Fit the second stage OLS regression model
second_stage_model = sm.OLS(y_second_stage, X_second_stage).fit()

# Store the results in a dictionary
results_dict = {
    'Model': '3a',
    'First_Stage_F_Statistic': first_stage_f_statistic,
    'Second_Stage_Coefficient_Intercept': second_stage_model.params['const'],
    'Second_Stage_Coefficient_car': second_stage_model.params['car'],
    'Second_Stage_Coefficient_mpg_hat': second_stage_model.params['mpg_hat'],
    'Second_Stage_Standard_Error_Intercept': second_stage_model.bse['const'],
    'Second_Stage_Standard_Error_car': second_stage_model.bse['car'],
    'Second_Stage_Standard_Error_mpg_hat': second_stage_model.bse['mpg_hat']
}

# Append the dictionary to the results list
results_list.append(results_dict)

# Print the summary of the second stage regression results
print(second_stage_model.summary())

# Save the latex summary to a file
output_file_path = os.path.join(outputpath, 'modelsummary1.tex')
with open(output_file_path, 'w') as f:
    f.write(second_stage_model.summary().as_latex())

# 3b first stage
df['weight_squared'] = df['weight']**2
X_first_stage_b = df[['weight_squared', 'car', 'const']]  # Add other exogenous variables if applicable
y_first_stage_b = df['mpg']

# Add a constant term to the independent variables
X_first_stage_b = sm.add_constant(X_first_stage_b)

# Fit the first stage OLS regression model
first_stage_model_b = sm.OLS(y_first_stage_b, X_first_stage_b).fit()

# Store the first stage F-statistic
first_stage_f_statistic_b = first_stage_model_b.fvalue

# Obtain fitted values from the first stage
df['mpg_hat'] = first_stage_model_b.fittedvalues

# 3b second stage
X_second_stage_b = df[['mpg_hat', 'car', 'const']]  # Use fitted values from the first stage
y_second_stage_b = df['price']

# Add a constant term to the independent variables
X_second_stage_b = sm.add_constant(X_second_stage_b)

# Fit the second stage OLS regression model
second_stage_model_b = sm.OLS(y_second_stage_b, X_second_stage_b).fit()

# Store the results in a dictionary
results_dict_b = {
    'Model': '3b',
    'First_Stage_F_Statistic': first_stage_f_statistic_b,
    'Second_Stage_Coefficient_Intercept': second_stage_model_b.params['const'],
    'Second_Stage_Coefficient_car': second_stage_model_b.params['car'],
    'Second_Stage_Coefficient_mpg_hat': second_stage_model_b.params['mpg_hat'],
    'Second_Stage_Standard_Error_Intercept': second_stage_model_b.bse['const'],
    'Second_Stage_Standard_Error_car': second_stage_model_b.bse['car'],
    'Second_Stage_Standard_Error_mpg_hat': second_stage_model_b.bse['mpg_hat']
}

# Append the dictionary to the results list
results_list.append(results_dict_b)

# Print the summary of the second stage regression results
print(second_stage_model_b.summary())

# Save the latex summary to a file
output_file_path = os.path.join(outputpath, 'modelsummary2.tex')
with open(output_file_path, 'w') as f:
    f.write(second_stage_model_b.summary().as_latex())

# 3c first stage
X_first_stage_c = df[['height', 'car', 'const']]  # Add other exogenous variables if applicable
y_first_stage_c = df['mpg']

# Fit the first stage OLS regression model
first_stage_model_c = sm.OLS(y_first_stage_c, X_first_stage_c).fit()

# Store the first stage F-statistic
first_stage_f_statistic_c = first_stage_model_c.fvalue

# Obtain fitted values from the first stage
df['mpg_hat'] = first_stage_model_c.fittedvalues

# 3c second stage
X_second_stage_c = df[['mpg_hat', 'car', 'const']]  # Use fitted values from the first stage
y_second_stage_c = df['price']

# Fit the second stage OLS regression model
second_stage_model_c = sm.OLS(y_second_stage_c, X_second_stage_c).fit()

# Store the results in a dictionary
results_dict_c = {
    'Model': '3c',
    'First_Stage_F_Statistic': first_stage_f_statistic_c,
    'Second_Stage_Coefficient_Intercept': second_stage_model_c.params['const'],
    'Second_Stage_Coefficient_car': second_stage_model_c.params['car'],
    'Second_Stage_Coefficient_mpg_hat': second_stage_model_c.params['mpg_hat'],
    'Second_Stage_Standard_Error_Intercept': second_stage_model_c.bse['const'],
    'Second_Stage_Standard_Error_car': second_stage_model_c.bse['car'],
    'Second_Stage_Standard_Error_mpg_hat': second_stage_model_c.bse['mpg_hat']
}

# Append the dictionary to the results list
results_list.append(results_dict_c)

# Print the summary of the second stage regression results
print(second_stage_model_c.summary())

# Save the latex summary to a file
output_file_path = os.path.join(outputpath, 'modelsummary3.tex')
with open(output_file_path, 'w') as f:
    f.write(second_stage_model_c.summary().as_latex())

# Create a DataFrame from the results list
results_df = pd.DataFrame(results_list)

# Transpose the DataFrame to have models as columns
results_df_transposed = results_df.set_index('Model').transpose()

# Print the transposed results table
print(results_df_transposed)

# Save the transposed results table to a .tex file
transposed_results_tex_path = os.path.join(outputpath, 'transposed_detailed_results.tex')
results_df_transposed.to_latex(transposed_results_tex_path, index=True)
## IVGMM
# Stage 1: Regress 'mpg' on 'weight' and other exogenous variables
X_first_stage_4 = df[['weight', 'car', 'const']]  
y_first_stage_4 = df['mpg']

# Add a constant term to the independent variables
X_first_stage_4 = sm.add_constant(X_first_stage_4)

# Fit the first stage OLS regression model
first_stage_model_4 = sm.OLS(y_first_stage_4, X_first_stage_4).fit()

# Obtain the fitted values from the first stage
df['mpg_hat'] = first_stage_model_4.fittedvalues

# Stage 2: Regress 'price' on the fitted values and other exogenous variables
X_second_stage_4 = df[['mpg_hat', 'car']]  # Use fitted values from the first stage
y_second_stage_4 = df['price']

# Add a constant term to the independent variables
X_second_stage_4 = sm.add_constant(X_second_stage_4)

# Fit the second stage OLS regression model
second_stage_model_4 = sm.OLS(y_second_stage_4, X_second_stage_4).fit()

# Calculate IV estimate using GMM
iv_model = IVGMM.from_formula('price ~ [mpg_hat + car]', df)
iv_result = iv_model.fit()

# Print the summary of the IV-GMM regression results
print(iv_result)
output_file_path = os.path.join(outputpath, 'modelsummary4.tex')
with open(output_file_path, 'w') as f:
    f.write(iv_result.summary.as_latex())
