#Converting the values into Periodontitis or Healthy
#Periodontitis
maskp = data_com['Patient Diagnosis'].str.contains('periodontitis', na=False)
data_com.loc[maskp, 'Patient Diagnosis'] = 'Periodontitis'
maskP = data_com['Patient Diagnosis'].str.contains('Periodontitis', na=False)
data_com.loc[maskP, 'Patient Diagnosis'] = 'Periodontitis'
maskPG = data_com['Patient Diagnosis'].str.contains('Generalised', na=False)
data_com.loc[maskPG, 'Patient Diagnosis'] = 'Periodontitis'
maskPL = data_com['Patient Diagnosis'].str.contains('Localised', na=False)
data_com.loc[maskPL, 'Patient Diagnosis'] = 'Periodontitis'
#Healthy
maskh = data_com['Patient Diagnosis'].str.contains('gingivitis', na=False)
data_com.loc[maskh, 'Patient Diagnosis'] = 'Healthy'
maskhg = data_com['Patient Diagnosis'].str.contains('Gingivitis', na=False)
data_com.loc[maskhg, 'Patient Diagnosis'] = 'Healthy'
maskH = data_com['Patient Diagnosis'].str.contains('Healthy', na=False)
data_com.loc[maskH, 'Patient Diagnosis'] = 'Healthy'
print(data_com)

data_com.to_csv('data_com.csv', index=False)

# 
data_com['Patient Diagnosis'].value_counts()
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
featrs = data_com.drop('Patient Diagnosis',axis=1)
target = data_com['Patient Diagnosis']
sc = MinMaxScaler()
featrs = sc.fit_transform(featrs)
enc = LabelEncoder()
target = enc.fit_transform(target)
print(featrs)
print(target)

# SMOTE analysis for oversampling 
from imblearn.over_sampling import SMOTE
sm = SMOTE(random_state=42, k_neighbors=5)
featrs_sm, target_sm = sm.fit_resample(featrs, target)
np.unique(target_sm,return_counts=True)
from collections import Counter
# Count class distribution after SMOTE
class_counts = Counter(target_sm)
# Print class distribution
for class_label, count in class_counts.items():
    print(f"Class {class_label}: {count} samples")
