#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 19:11:08 2024

@author: savannahellison
"""

# Clear all #

from IPython import get_ipython
get_ipython().magic('reset -sf')
from scipy.stats import ttest_ind
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np 
from scipy.optimize import minimize
import statsmodels.api as sm
# set working directory #

outputpath = r'/Users/savannahellison/Dropbox/phdee/hw2/output'

# import data #


df = pd.read_csv(r'/Users/savannahellison/Dropbox/phdee/hw2/kwh.csv')
print(df.head())

control_group = df[df['retrofit'] == 0]
treatment_group = df[df['retrofit'] == 1]

#### Balance Table ####
# Lists to store values
variables = []
control_values = []
treatment_values = []
p_values = []

# Loop through variables and calculate means, std devs, and p-values
for variable in ['sqft', 'temp', 'electricity']:  # Replace with your actual covariates
    control_mean = control_group[variable].mean()
    control_std = control_group[variable].std()
    
    treatment_mean = treatment_group[variable].mean()
    treatment_std = treatment_group[variable].std()
    
    # Perform t-test
    t_stat, p_value = ttest_ind(control_group[variable], treatment_group[variable])
    
    # Concatenate control mean and std dev into a single string
    control_summary = f'{control_mean:.2f} ± {control_std:.2f}'
    
    # Append values to lists
    variables.append(variable)
    control_values.append(control_summary)
    treatment_values.append(f'{treatment_mean:.2f} ± {treatment_std:.2f}')
    p_values.append(p_value)

# Create DataFrame from lists
balance_table = pd.DataFrame({
    'Variable': variables,
    'Control': control_values,
    'Treatment': treatment_values,
    'P-value': p_values
})
# Display the balance table
print(balance_table)

# Export the balance table to a LaTeX file in your Dropbox
output_file_path = os.path.join(outputpath, 'balance_table.tex')
balance_table.to_latex(output_file_path, index=False, escape=False)

## Plot keenal density ##

sns.kdeplot(treatment_group['electricity'], label='Retrofit', shade=True)
sns.kdeplot(control_group['electricity'], label='No Retrofit', shade=True)

# Label the plot
plt.title('Kernel Density Plots of Electricity Usage')
plt.xlabel('Electricity Usage in kwh')
plt.ylabel('Density')

# Show legend
plt.legend()

# Save plot
plt.savefig('kerneldensity.pdf',format='pdf') 
# Show the plot
plt.show()

# OLS by Hand
df = pd.read_csv(r'/Users/savannahellison/Dropbox/phdee/hw2/kwh.csv')
X_hand = df[['sqft', 'retrofit', 'temp']].values
Y_hand = df['electricity'].values.reshape(-1, 1)
X_hand = np.c_[np.ones(X_hand.shape[0]), X_hand]

try:
    beta_hat = np.linalg.inv(X_hand.T @ X_hand) @ X_hand.T @ Y_hand
    print("\nCoefficients (beta_hat) using OLS by Hand:")
    print(beta_hat)
except np.linalg.LinAlgError as e:
    print(f"\nError during calculation: {e}")

# Simulated Least Squares
X_simulated = df[['sqft', 'retrofit', 'temp']].values
Y_simulated = df['electricity'].values.reshape(-1, 1)
X_simulated = np.c_[np.ones(X_simulated.shape[0]), X_simulated]

# Define the sum of squares objective function
def sum_of_squares(beta, X, Y):
    residuals = Y - X @ beta.reshape(-1, 1)
    return np.sum(residuals**2)

initial_beta_simulated = np.zeros(X_simulated.shape[1])
result_simulated = minimize(sum_of_squares, initial_beta_simulated, args=(X_simulated, Y_simulated), method='Nelder-Mead')
optimal_beta_simulated = result_simulated.x.reshape(-1, 1)

print("\nOptimal Coefficients (beta) using Simulated Least Squares:")
print(optimal_beta_simulated)

# StatsModels OLS
X_statsmodels = sm.add_constant(df[['sqft', 'retrofit', 'temp']])
Y_statsmodels = df['electricity']

model_statsmodels = sm.OLS(Y_statsmodels, X_statsmodels).fit()
beta_hat_statsmodels = model_statsmodels.params.values.reshape(-1, 1)

# Extract scalar value for 'temp'
temp_statsmodels = beta_hat_statsmodels[3][0]

# Create a DataFrame with coefficients
coefficients_df = pd.DataFrame({
    'Method': ['OLS by Hand', 'Simulated Least Squares', 'StatsModels OLS'],
    'Intercept': [beta_hat[0][0], optimal_beta_simulated[0][0], beta_hat_statsmodels[0]],
    'sqft': [beta_hat[1][0], optimal_beta_simulated[1][0], beta_hat_statsmodels[1]],
    'retrofit': [beta_hat[2][0], optimal_beta_simulated[2][0], beta_hat_statsmodels[2]],
    'temp': [beta_hat[3][0], optimal_beta_simulated[3][0], temp_statsmodels]
})

# Display the coefficients DataFrame
print(coefficients_df)
# export table #
output_file_path = os.path.join(outputpath, 'coefficients_table.tex')
coefficients_df.to_latex(output_file_path, index=False, escape=False)

print("Coefficients table exported to:", output_file_path)