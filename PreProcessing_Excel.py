# pre-processing as the excel looks good 
df = pd.read_excel('pdts3.xlsx',index_col=[0])
#filling in empty spaces 
df = df.fillna(method='ffill',axis=0)
# dropping columns
df.drop('tooth #',axis=1,inplace=True)
# 
# Function to process each group
def balance_group(group):
   #Replace 'np', 'nv', 'NP', 'NV' with 0 in 'mesial length measurement' and 'distal length measurement'
    group['mesial length measurement'] = group['mesial length measurement'].replace(['np', 'nv', 'NP', 'NV'], 0)
    group['distal length measurement'] = group['distal length measurement'].replace(['np', 'nv', 'NP', 'NV','.NV'], 0)

    # Sort by 'mesial length measurement' and 'distal length measurement'
    group_sorted = group.sort_values(by=['mesial length measurement', 'distal length measurement'], ascending=False)

    # If there are more than 5 rows, keep the top 5 with greatest measurements
    if len(group_sorted) > 5:
        group_sorted = group_sorted.head(5)
    # If there are less than 5 rows, add additional rows with 0 values
    elif len(group_sorted) < 5:
        num_rows_to_add = 5 - len(group_sorted)
        for _ in range(num_rows_to_add):
            new_row = pd.DataFrame({'Number': group_sorted['Number'].iloc[0],
                                    'mesial length measurement': 0,
                                    'distal length measurement': 0,
                                    'Patient Diagnosis': group_sorted['Patient Diagnosis'].iloc[0]},
                                    index=[0])
            group_sorted = pd.concat([group_sorted, new_row], ignore_index=True)

    # Set 'Patient Diagnosis' to empty (or NaN) for all rows except the first one
    group_sorted['Patient Diagnosis'].iloc[1:] = None

    return group_sorted

# Group by 'Number' and apply the balance function to each group
df_balanced = df.groupby('Number').apply(balance_group).reset_index(drop=True)

# Save the cleaned and balanced dataframe
df_balanced.to_csv('balanced_dataset.csv', index=False)

# Output the balanced dataframe
df_balanced.head()

# Function to clean and process mesial and distal lengths
def clean_length(value):
    if isinstance(value, str):
        value = value.replace(',', '.')
        if not value.replace('.', '', 1).isdigit():
            value = '0'
    return value

# Function to concatenate mesial and distal lengths for each 'Number'
def flatten_group(group):
    mesial_list = group['mesial length measurement'].tolist()
    distal_list = group['distal length measurement'].tolist()

    # Clean mesial and distal lengths
    mesial_list = [clean_length(x) for x in mesial_list]
    distal_list = [clean_length(x) for x in distal_list]

    # Flatten into a dictionary format for easy conversion back to DataFrame
    flattened_data = {'Number': group['Number'].iloc[0]}

    for i in range(1, len(mesial_list) + 1):
        flattened_data[f'ml{i}'] = mesial_list[i-1]
        flattened_data[f'dl{i}'] = distal_list[i-1]

    # Only retain 'Patient Diagnosis' for the first row
    flattened_data['Patient Diagnosis'] = group['Patient Diagnosis'].iloc[0]

    return pd.DataFrame([flattened_data])

# Apply the flattening process group by group
df_flattened = df_balanced.groupby('Number').apply(flatten_group).reset_index(drop=True)

# Replace 'Number' column with sequential integers
df_flattened['Number'] = range(1, len(df_flattened) + 1)

# Save the cleaned and flattened dataset
df_flattened.to_csv('flattened_dataset.csv', index=False)


