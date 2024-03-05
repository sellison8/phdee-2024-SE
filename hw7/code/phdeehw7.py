#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 16:45:18 2024

@author: savannahellison
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import linregress
import statsmodels.api as sm

#set output path
outputpath = r'/Users/savannahellison/Dropbox/phdee/hw7/output'

# import data
df = pd.read_csv(r'/Users/savannahellison/Dropbox/phdee/hw5/instrumentalvehicles.csv')

# Set cutoff length
cutoff_length = 225

# Create a new column for 'length - cutoff'
df['length_minus_cutoff'] = df['length'] - cutoff_length

# Scatterplot with different colors on either side of the cutoff
plt.scatter(
    df[df['length_minus_cutoff'] < 0]['length_minus_cutoff'],
    df[df['length_minus_cutoff'] < 0]['mpg'],
    label='Below Cutoff',
    color='blue'
)

plt.scatter(
    df[df['length_minus_cutoff'] >= 0]['length_minus_cutoff'],
    df[df['length_minus_cutoff'] >= 0]['mpg'],
    label='Above Cutoff',
    color='orange'
)

# Line at the cutoff
plt.axvline(x=0, color='red', linestyle='--', label='Cutoff')

# Set labels and title
plt.xlabel('Length - Cutoff (inches)')
plt.ylabel('MPG')
plt.title('Scatterplot of MPG vs. Length - Cutoff')
plt.legend()

# Save the plot 
plt.savefig('scatterplot_colored.pdf')

#####################################

# Point 3: Fit a first-order polynomial to both sides of the cutoff
plt.figure(figsize=(12, 6))

# Scatter plot for points below the cutoff
plt.scatter(
    df[df['length_minus_cutoff'] < 0]['length_minus_cutoff'],
    df[df['length_minus_cutoff'] < 0]['mpg'],
    label='Below Cutoff',
    color='blue'
)

# Scatter plot for points above the cutoff
plt.scatter(
    df[df['length_minus_cutoff'] >= 0]['length_minus_cutoff'],
    df[df['length_minus_cutoff'] >= 0]['mpg'],
    label='Above Cutoff',
    color='orange'
)

# Fit first-order polynomial on either side of the cutoff
below_cutoff = df[df['length_minus_cutoff'] < 0]
above_cutoff = df[df['length_minus_cutoff'] >= 0]

# Fit polynomial for points below the cutoff
coeff_below = np.polyfit(below_cutoff['length_minus_cutoff'], below_cutoff['mpg'], 1)

# Fit polynomial for points above the cutoff
coeff_above = np.polyfit(above_cutoff['length_minus_cutoff'], above_cutoff['mpg'], 1)

# Plot the fitted polynomials with colored lines
x_below = np.linspace(min(below_cutoff['length_minus_cutoff']), 0, 100)
y_below = np.polyval(coeff_below, x_below)

x_above = np.linspace(0, max(above_cutoff['length_minus_cutoff']), 100)
y_above = np.polyval(coeff_above, x_above)

plt.plot(x_below, y_below, color='black', linestyle='--', label='Fit Below Cutoff')
plt.plot(x_above, y_above, color='black', linestyle='--', label='Fit Above Cutoff')

# Line at the cutoff
plt.axvline(x=0, color='red', linestyle='--', label='Cutoff')

# Set labels and title
plt.xlabel('Length - Cutoff (inches)')
plt.ylabel('MPG')
plt.title('Regression Discontinuity Design with Fitted Polynomials')
plt.legend()

# Save the plot to a .tex file
plt.savefig('regression_discontinuity_colored_lines.pdf')

# Estimate the impact of the policy on fuel efficiency at the cutoff
slope_below, intercept_below, _, _, _ = linregress(below_cutoff['length_minus_cutoff'], below_cutoff['mpg'])
slope_above, intercept_above, _, _, _ = linregress(above_cutoff['length_minus_cutoff'], above_cutoff['mpg'])

impact_estimate = slope_above - slope_below

# Report the first stage treatment effect estimate
print(f"First Stage Treatment Effect Estimate: {impact_estimate}")

##############################################
# Fit second-order polynomial to both sides of the cutoff
plt.figure(figsize=(12, 6))

# Scatter plot for points below the cutoff
plt.scatter(
    df[df['length_minus_cutoff'] < 0]['length_minus_cutoff'],
    df[df['length_minus_cutoff'] < 0]['mpg'],
    label='Below Cutoff',
    color='black'
)

# Scatter plot for points above the cutoff
plt.scatter(
    df[df['length_minus_cutoff'] >= 0]['length_minus_cutoff'],
    df[df['length_minus_cutoff'] >= 0]['mpg'],
    label='Above Cutoff',
    color='black'
)

# Fit second-order polynomial for points below the cutoff
coeff_below_2nd = np.polyfit(below_cutoff['length_minus_cutoff'], below_cutoff['mpg'], 2)
x_below_2nd = np.linspace(min(below_cutoff['length_minus_cutoff']), 0, 100)
y_below_2nd = np.polyval(coeff_below_2nd, x_below_2nd)

# Fit second-order polynomial for points above the cutoff
coeff_above_2nd = np.polyfit(above_cutoff['length_minus_cutoff'], above_cutoff['mpg'], 2)
x_above_2nd = np.linspace(0, max(above_cutoff['length_minus_cutoff']), 100)
y_above_2nd = np.polyval(coeff_above_2nd, x_above_2nd)

plt.plot(x_below_2nd, y_below_2nd, color='blue', linestyle='--', label='Fit Below Cutoff (2nd Order)')
plt.plot(x_above_2nd, y_above_2nd, color='orange', linestyle='--', label='Fit Above Cutoff (2nd Order)')

# Line at the cutoff
plt.axvline(x=0, color='red', linestyle='--', label='Cutoff')

# Set labels and title
plt.xlabel('Length - Cutoff (inches)')
plt.ylabel('MPG')
plt.title('Regression Discontinuity Design with 2nd Order Polynomial')
plt.legend()

# Save the plot to a .tex file
plt.savefig('regression_discontinuity_2nd_order.pdf')


# Estimate the impact of the policy on fuel efficiency at the cutoff (2nd Order)
slope_below_2nd, intercept_below_2nd, _, _, _ = linregress(x_below_2nd, y_below_2nd)
slope_above_2nd, intercept_above_2nd, _, _, _ = linregress(x_above_2nd, y_above_2nd)

impact_estimate_2nd = slope_above_2nd - slope_below_2nd

# Report the first stage treatment effect estimate (2nd Order)
print(f"First Stage Treatment Effect Estimate (2nd Order): {impact_estimate_2nd}")

###################################################
# Fit fifth-order polynomial to both sides of the cutoff
plt.figure(figsize=(12, 6))

# Scatter plot for points below the cutoff
plt.scatter(
    df[df['length_minus_cutoff'] < 0]['length_minus_cutoff'],
    df[df['length_minus_cutoff'] < 0]['mpg'],
    label='Below Cutoff',
    color='black'
)

# Scatter plot for points above the cutoff
plt.scatter(
    df[df['length_minus_cutoff'] >= 0]['length_minus_cutoff'],
    df[df['length_minus_cutoff'] >= 0]['mpg'],
    label='Above Cutoff',
    color='black'
)

# Fit fifth-order polynomial for points below the cutoff
coeff_below_5th = np.polyfit(below_cutoff['length_minus_cutoff'], below_cutoff['mpg'], 5)
x_below_5th = np.linspace(min(below_cutoff['length_minus_cutoff']), 0, 100)
y_below_5th = np.polyval(coeff_below_5th, x_below_5th)

# Fit fifth-order polynomial for points above the cutoff
coeff_above_5th = np.polyfit(above_cutoff['length_minus_cutoff'], above_cutoff['mpg'], 5)
x_above_5th = np.linspace(0, max(above_cutoff['length_minus_cutoff']), 100)
y_above_5th = np.polyval(coeff_above_5th, x_above_5th)

plt.plot(x_below_5th, y_below_5th, color='blue', linestyle='--', label='Fit Below Cutoff (5th Order)')
plt.plot(x_above_5th, y_above_5th, color='orange', linestyle='--', label='Fit Above Cutoff (5th Order)')

# Line at the cutoff
plt.axvline(x=0, color='red', linestyle='--', label='Cutoff')

# Set labels and title
plt.xlabel('Length - Cutoff (inches)')
plt.ylabel('MPG')
plt.title('Regression Discontinuity Design with 5th Order Polynomial')
plt.legend()

# Save the plot to a .tex file
plt.savefig('regression_discontinuity_5th_order.pdf')

# Estimate the impact of the policy on fuel efficiency at the cutoff (5th Order)
slope_below_5th, intercept_below_5th, _, _, _ = linregress(x_below_5th, y_below_5th)
slope_above_5th, intercept_above_5th, _, _, _ = linregress(x_above_5th, y_above_5th)

impact_estimate_5th = slope_above_5th - slope_below_5th

# Report the first stage treatment effect estimate (5th Order)
print(f"First Stage Treatment Effect Estimate (5th Order): {impact_estimate_5th}")

######################################################
# Step 1: First Stage
# Choose a polynomial degree for the first stage
degree_first_stage = 2  # Adjust as needed

# Fit a polynomial for the first stage
coeff_first_stage = np.polyfit(df['length_minus_cutoff'], df['mpg'], degree_first_stage)
df['predicted_mpg'] = np.polyval(coeff_first_stage, df['length_minus_cutoff'])

# Step 2: Predicted Values from First Stage

# Step 3: Second Stage 
X_second_stage = df[['predicted_mpg', 'car']]
X_second_stage = sm.add_constant(X_second_stage)  # Add a constant term

# Dependent variable
y_second_stage = df['price']

# Fit the second stage model
model_second_stage = sm.OLS(y_second_stage, X_second_stage).fit()

# Display the regression results
print(model_second_stage.summary())

# Extract the coefficient for predicted_mpg as the estimated impact
estimated_impact_mpg = model_second_stage.params['predicted_mpg']

# Report the Average Treatment Effect (ATE)
print(f"Average Treatment Effect (ATE) of mpg on Sale Price: {estimated_impact_mpg}")