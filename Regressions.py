import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from linearmodels import PanelOLS
from linearmodels import RandomEffects
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan

#from linearmodels.datasets import jobtraining
#data = jobtraining.load()
#year = pd.Categorical(data.year)
#data = data.set_index(['fcode', 'year'])
#data['year'] = year
#print(data.head(5))

#exog_vars = ['grant', 'employ']
#exog = sm.add_constant(data[exog_vars])
#od = RandomEffects(data.clscrap, exog)
#re_res = mod.fit()
#print(re_res)

#READING IN ALOTTMENTS DATA AND CLEANING
Allotments = pd.read_csv('Allotment.csv')
Allotments = Allotments.melt(id_vars = ['Year', 'Variable'], var_name = 'Agency', value_name = 'Value').sort_values('Year')
Allotments = Allotments.pivot(index=['Year', 'Agency'],
                              columns='Variable',
                              values='Value').reset_index()
Allotments['Agency'] = Allotments['Agency'].astype("string")
Allotments['Agency'] = Allotments['Agency'].str.strip()
#print(len(Alottments))

#READING IN ALOTTMENTS2 DATA AND CLEANING
Allotments2 = pd.read_csv('allotment2.csv')
Allotments2 = Allotments2.melt(id_vars = ['Year', 'Variable'], var_name = 'Agency', value_name = 'Value').sort_values('Year')
Allotments2 = Allotments2.pivot(index=['Year', 'Agency'],
                              columns='Variable',
                              values='Value').reset_index()
Allotments2['Agency'] = Allotments['Agency'].astype("string")
Allotments2['Agency'] = Allotments['Agency'].str.strip()

#READING IN SCHOOL DATA AND CLEANING
School = pd.read_csv('school.csv')
School['Variable'] = School['Variable'].str.strip()
School = School.melt(id_vars = ['Year', 'Variable'], var_name = 'Agency', value_name = 'Value').sort_values('Year')
School = School.pivot(index=['Year', 'Agency'],
                              columns='Variable',
                              values='Value').reset_index()

School['Agency'] = School['Agency'].astype("string")
School['Agency'] = School['Agency'].str.strip()
School = School.drop(School[School['Agency'] == 'OR_scattered'].index)
School = School.drop(School[School['Agency'] == 'WA_scattered'].index)
#print(School.info())

#READING IN TIMBER DATA AND CLEANING
Timber = pd.read_csv('Timber.csv')
Timber = Timber.melt(id_vars = ['Year', 'Variable'], var_name = 'Agency', value_name = 'Value').sort_values('Year')
Timber = Timber.pivot(index=['Year', 'Agency'],
                              columns='Variable',
                              values='Value').reset_index()
Timber['Agency'] = Timber['Agency'].astype("string")
Timber['Agency'] = Timber['Agency'].str.strip()
#print(len(Timber))

#READING IN LEASING DATA AND CLEANING
Leasing = pd.read_csv('Leasing2.csv')
Leasing = Leasing.melt(id_vars = ['Year', 'Variable'], var_name = 'Agency', value_name = 'Value').sort_values('Year')
Leasing = Leasing.pivot(index=['Year', 'Agency'],
                              columns='Variable',
                              values='Value').reset_index()
Leasing['Agency'] = Leasing['Agency'].astype("string")
Leasing['Agency'] = Leasing['Agency'].str.strip()
#print(Leasing.info())

#MERGING DATASETS
merged_df = pd.merge(Allotments, Timber, on=['Year', 'Agency'], how='outer')
merged_df = pd.merge(merged_df, Allotments2, on=['Year', 'Agency'], how='outer')
merged_df = pd.merge(merged_df, School, on=['Year', 'Agency'], how='outer')
merged_df = pd.merge(merged_df, Leasing, on=['Year', 'Agency'], how='outer')
merged_df['Year'] = pd.to_datetime(merged_df['Year'], format='%Y')
merged_df['Agency'] = merged_df['Agency'].astype('category')
#print(merged_df.info())

#CLEANING MERGED DATASET
#resetting index
merged_df.set_index(['Agency', 'Year'], inplace=True)

#removing extra spaces from NAs
for col in merged_df.columns[0:30]: #NEED TO CHANGE ITERATIONS HERE
    merged_df[col] = merged_df[col].apply(lambda x: x.strip() if isinstance(x, str) and x.strip() == "NA" else x)

#changing datatype of columns to numeric
for col in merged_df.columns[0:30]:
    merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')

for col in merged_df.columns[64:92]:
    merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')

#changing NAs to NaN
merged_df.replace('NA', pd.NA, inplace=True)
#print(merged_df.info())

#CREATING AGGREGATE STATISTICS FOR TIMBER ANALYSIS 
merged_df['total_boarded'] = merged_df['indian_children_in_govt-school|nonreservation_boarding'].fillna(0) + merged_df['indian_children_in_govt-school|reservation_boarding'].fillna(0) + merged_df['indian_children_in_mission/private|boarding'].fillna(0)
merged_df['total_boarded-1'] = merged_df['total_boarded'].shift(1)

merged_df['total_value_timber_cut'] = merged_df['timber_cut|contractors_value'] + merged_df['timber_cut|indians_value'] + merged_df['timber_cut|govt_value']
merged_df['total_value_nonindian_timber_cut'] = merged_df['timber_cut|govt_value'] + merged_df['timber_cut|contractors_value']
merged_df['sawmills'] = merged_df['govt_sawmills|number'].fillna(0) + merged_df['private_sawmills|number'].fillna(0)
merged_df['sawmills_cost'] = merged_df['govt_sawmills|cost'].fillna(0) + merged_df['private_sawmills|cost'].fillna(0)

#merged_df['total_rez income'] = merged_df['Total Timber Cut'] + merged_df['Total Income']
#print(merged_df.groupby('Year')['Indian children in Mission/Private|Boarding'].sum())

#ADDING IN COLUMNS FOR PROPORTIONS OF STUDENTS AT BOARDING SCHOOLS TYPES
merged_df['perc_offrez'] = merged_df['indian_children_in_govt-school|nonreservation_boarding']/merged_df['indian_children_in_school|total'] 
merged_df['perc_onrez'] = merged_df['indian_children_in_govt-school|reservation_boarding']/merged_df['indian_children_in_school|total']
merged_df['perc_mission'] = merged_df['indian_children_in_mission/private|boarding']/merged_df['indian_children_in_school|total']
merged_df['perc_boarding'] = merged_df['total_boarded']/merged_df['indian_children_in_school|total']
merged_df['perc_boarding2'] = merged_df['total_boarded']/merged_df['number_eligible_for_attendance']
#print(merged_df['prop_offrez'])

#ADDING IN LAG EFFECT VARIABLES
merged_df['offrez-1'] = merged_df['indian_children_in_govt-school|nonreservation_boarding'].shift(1)
merged_df['onrez-1'] = merged_df['indian_children_in_govt-school|reservation_boarding'].shift(1)
merged_df['mission-1'] = merged_df['indian_children_in_mission/private|boarding'].shift(1)
merged_df['indian_children_in_school|total-1'] = merged_df['indian_children_in_school|total'].shift(1)
merged_df['perc_boarding-1'] = merged_df['perc_boarding'].shift(1)
merged_df['number_eligible_for_attendance-1'] = merged_df['number_eligible_for_attendance'].shift(1)
merged_df['perc_boarding2-1'] = merged_df['perc_boarding2'].shift(1)

#print(merged_df.info())

#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#    print(merged_df.)

#for index, column_name in enumerate(merged_df.columns):
#    print(f"Column index {index}: {column_name}")
#print(merged_df.iloc[:,99])

#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
#print(Coastal_df['Total nonIndian Timber Cut'])

#ADDING IN BINARY VARIABLES FOR SUBREGION
#print(merged_df.index)
#WA_list = ['Colville', 'Neah bay', 'Spokane', 'Tulalip', 'Yakima', 'Cushman-Taholah']
#OR_list = ['Klamath', 'Siletz', 'Umatilla', 'Warm Springs']

#merged_df['State'] = 0
#merged_df.loc[merged_df.index.get_level_values('Agency').isin(WA_list), 'State'] = 1
#print(merged_df['State'])

Coastal = ['Neah bay', 'Tulalip', 'Cushman-Taholah', 'Klamath', 'Siletz', 'Warm Springs']
Coastal_df = merged_df.loc[merged_df.index.get_level_values('Agency').isin(Coastal)]
#print(Coastal_df.index)

#PRINTING OUT TEST VALUES FOR SPECIFIED AGENCY
#rows = merged_df.loc[merged_df.index.get_level_values('Agency') == 'Tulalip']
#values = rows.iloc[:,[12,43,44, 64]]
#print(values)

#PRINTING OUT CORRELATION MATRIX FOR INDEPENDENT VARIABLES
selected_columns1 = ['indian_children_in_school|total',
                     'total_boarded',
                     'number_eligible_for_attendance',
                     'indian_children_in_govt-school|nonreservation_boarding',
                     'indian_children_in_govt-school|reservation_boarding',
                     'indian_children_in_mission/private|boarding',
                     'unallotted|total_acreage',
                     'allotted|total_acreage',
                     'total_reservation_acreage']
df1 = merged_df.loc[:, selected_columns1]

pd.set_option('display.max_columns', None)
print(df1.corr())
#print(merged_df.iloc[:,26:28])

#selected_columns2 = ['|Total number of school age children',
#             '|Eligible for Attendance',
#             '|Total number of school age children',
#             '|Indian Population']
#df2 = merged_df.loc[:, selected_columns2]

#pd.set_option('display.max_columns', None)
#print(df2.corr())
#print(merged_df.info())

#PRINT OUT CHARTS FOR THE TIMBER VARIABLES
sum_by_year = merged_df.groupby('Year')['total_value_nonindian_timber_cut'].sum()

# Plot the chart
plt.figure(figsize=(10, 6))
plt.plot(sum_by_year.index, sum_by_year, marker='o', linestyle='-')

# Adding labels and title
plt.xlabel('Year')
plt.ylabel('Total Value of non-Indian Timber Cut')
plt.title('Annual Value of non-Indian Timber Cut on Reservation, WA and OR')

# Display the plot
plt.grid(True)
#plt.show()

#PRINT OUT CHARTS BY AGENCY OF DEPENDENT VARIABLES OVER YEAR
grouped = merged_df.groupby(['Year', 'Agency'])['timber_cut|indians_value'].sum().unstack()

# Plotting
plt.figure(figsize=(10, 6))
for agency in grouped.columns:
    plt.plot(grouped.index, grouped[agency], label=agency)

plt.xlabel('Year')
plt.ylabel('Value of Native Timber Cut')
plt.title('Native Logging Revenues by Year and Agency')
plt.legend()
plt.grid(True)
plt.show()

#print(grouped.head(10))

#REGRESSIONS MODELS
exog_vars = [#'total_indians_under_federal_supervision',
             #'indian_children_in_school|total-1',
             #'number_eligible_for_attendance-1',
             #'offrez-1',
             #'onrez-1',
             #'mission-1',
             #'total_boarded-1',
             #'perc_boarding-1',
             'perc_boarding2-1',
             #'total_tribal_and_individual_property',
             #'total_indians_allotted',
             #'unallotted_indians']
             #'allotted_timber|total_stumpage_value',
             #'unallotted_timber|total_stumpage_value',
             'unallotted|total_acreage',
             'allotted|total_acreage']
             #'holding_fee_patents|total']
             #'allotted_timber|acreage',
             #'unallotted_timber|acreage',
             #'sawmills'
             #'sawmills_cost']
exog = sm.add_constant(Coastal_df[exog_vars])
mod = PanelOLS(Coastal_df['total_value_timber_cut'], exog, entity_effects=True, time_effects=True)
fe_res = mod.fit()
#print(fe_res)

#mod = RandomEffects(merged_df['Sale of Land|Total Proceeds'], exog)
#re_res = mod.fit()
#print(re_res)

#CHECKING RESIDUALS USING A PANEL PLOT OF RESIDUALS
#fe_residuals = fe_res.resids
#merged_df['residuals'] = fe_residuals

# Plotting panel plot of residuals over time
#fig, ax = plt.subplots(figsize=(10, 6))

# Loop through unique entities and plot residuals over time for each entity
#for agency, group_data in merged_df.groupby('Agency'):
#    ax.plot(group_data.index.get_level_values('Year'), group_data['residuals'], marker='o', label=f'Agency {agency}')

# Add labels and legend
#ax.set_xlabel('Time Period')
#ax.set_ylabel('Fixed Effect Residual')
#ax.set_title('Panel Plot of Fixed Effect Residuals Over Time')
#ax.legend()

# Show plot
#plt.grid(True)
#plt.show()

#CHECKING FOR HOMOSKEDASTICITY
# Step 4: Check for homoscedasticity using Breusch-Pagan test
#bp_test = het_breuschpagan(fe_residuals, merged_df[exog])
#print("Breusch-Pagan test statistic:", bp_test[0])
#print("Breusch-Pagan p-value:", bp_test[1])

#PLOT OF INDEPENDENT VARIABLES, CROSS SECTION

# Compute the ratios for each column
ratio_A = merged_df.groupby('Year')['indian_children_in_govt-school|nonreservation_boarding'].sum() / merged_df.groupby('Year')['number_eligible_for_attendance'].sum()
ratio_B = merged_df.groupby('Year')['indian_children_in_govt-school|reservation_boarding'].sum() / merged_df.groupby('Year')['number_eligible_for_attendance'].sum()
ratio_C = merged_df.groupby('Year')['indian_children_in_mission/private|boarding'].sum() / merged_df.groupby('Year')['number_eligible_for_attendance'].sum()

# Plotting the lines
plt.figure(figsize=(10, 6))
plt.plot(ratio_A.index, ratio_A, label='Percentage Off-Reservation Boarding')
plt.plot(ratio_B.index, ratio_B, label='Percentage On-Reservation Boarding')
plt.plot(ratio_C.index, ratio_C, label='Percentage Mission/Contract Boarding')

# Adding labels and title
plt.xlabel('Year')
plt.ylabel('Percentage')
plt.title('Percentage of eligible school-aged children in boarding school by school type, WA and OR')

# Adding legend
plt.legend()

# Display the plot
plt.grid(True)
#plt.show()