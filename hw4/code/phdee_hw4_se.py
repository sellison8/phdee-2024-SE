#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 15:51:26 2024

@author: savannahellison
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.iolib.summary2 import summary_col
from patsy import dmatrices

#set output path
outputpath = r'/Users/savannahellison/Dropbox/phdee/hw4/output'

# import data

df = pd.read_csv(r'/Users/savannahellison/Dropbox/phdee/hw4/fishbycatch.csv')

print(df)

# reshape df using wide to long
df_long = pd.wide_to_long(df, stubnames=['shrimp','salmon', 'bycatch'], i=['firm'], j='month', sep='', suffix='\d+')
print("\nDataFrame after wide_to_long:")
print(df_long)
#reset index
df_long_reset = df_long.reset_index()
# visually inspect trends
# Filter data for months in 2017 and 2018
df_filtered = df_long_reset[df_long_reset['month'].between(1, 24)]

# Group by 'term', 'treated', and calculate the mean bycatch for each group
grouped_data = df_filtered.groupby(['month', 'treated'])['bycatch'].mean().reset_index()

# Plot the data
plt.figure(figsize=(10, 6))

for treated_group, group_data in grouped_data.groupby('treated'):
    plt.plot(group_data['month'], group_data['bycatch'], label=f'Treated: {treated_group}')

plt.title('Bycatch by Month Before and After Treatment')
plt.xlabel('Month')
plt.ylabel('Mean Bycatch')
plt.legend()

plt.savefig('visualtrends.pdf',format='pdf') 

plt.show()

# Filter data for December 2017 and January 2018
df_dec2017 = df_long_reset[(df_long_reset['month'] == 12)]
df_jan2018 = df_long_reset[(df_long_reset['month'] == 13)]

# Calculate means for treated and control groups in each period
pre_treated_mean = df_dec2017[df_dec2017['treated'] == 1]['bycatch'].mean()
pre_control_mean = df_dec2017[df_dec2017['treated'] == 0]['bycatch'].mean()
post_treated_mean = df_jan2018[df_jan2018['treated'] == 1]['bycatch'].mean()
post_control_mean = df_jan2018[df_jan2018['treated'] == 0]['bycatch'].mean()

# Calculate difference-in-differences estimate
DiD_estimate = (post_treated_mean - pre_treated_mean) - (post_control_mean - pre_control_mean)

# Print the estimate
print("Difference-in-Differences Estimate:", DiD_estimate)

# Create a group indicator variable
df_long_reset['group_indicator'] = df_long_reset['treated']

# Convert 'month' to a numerical variable
df_long_reset['group_indicator'] = (df_long_reset['treated'] == 1) & (df_long_reset['month'] >= 13)
df_long_reset['group_indicator'] = df_long_reset['group_indicator'].astype(int)
results=[]
# Model 1: Basic DiD without additional controls
X1 = sm.add_constant(df_long_reset[['group_indicator']])
model1 = sm.OLS(df_long_reset['bycatch'], X1)
result1 = model1.fit(cov_type='cluster', cov_kwds={'groups': df_long_reset['firm']})
results.append(result1)

# Model 2: DiD with time fixed effects
y, X2 = dmatrices('bycatch ~ group_indicator + treated + C(month)', data=df_long_reset, return_type='dataframe')
model2 = sm.OLS(y, X2)
result2 = model2.fit(cov_type='cluster', cov_kwds={'groups': df_long_reset['firm']})
results.append(result2)

# Model 3: DiD with added controls for firm size, shrimp, and salmon
X3_columns = ['group_indicator', 'treated', 'firmsize', 'shrimp', 'salmon']
X3 = sm.add_constant(df_long_reset[X3_columns])
model3 = sm.OLS(df_long_reset['bycatch'], X3)
result3 = model3.fit(cov_type='cluster', cov_kwds={'groups': df_long_reset['firm']})
results.append(result3)

# Display the summary tables for each model and export to PDF
for i, result in enumerate(results, start=1):
    table = result.summary().tables[1]
    table_df = pd.DataFrame(table.data[1:], columns=table.data[0])
    table_df.to_latex(os.path.join(outputpath, f'model_{i}_summary.tex'), index=False)

# Compile the results into a summary table
table = sm.iolib.summary2.summary_col(results, 
                                      model_names=['Model 1', 'Model 2', 'Model 3'],
                                      stars=True, 
                                      float_format='%0.4f', 
                                      info_dict={'N': lambda x: "{0:d}".format(int(x.nobs))})

# Export the compiled summary table to PDF
table_df = pd.DataFrame(table.tables[0])
table_df.to_latex(os.path.join(outputpath, 'compiled_summary.tex'), index=False)


