##1.Import libraries

#Data Handling libraries
import pandas as pd
import numpy as np
import os

#visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns

#machine learning model libraries
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

#Logistic Regression is suitable for binary classification problems where the output has two classes (Approved / Rejected)
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

##2.Load dataset
df = pd.read_csv("loan_approval_dataset.csv")
# remove extra spaces from column names
df.columns = df.columns.str.strip()
print(df.columns)
df = df.drop("loan_id", axis=1)
print("\nFirst 5 rows:")
print(df.head())
print("\nDataset info:")
print(df.info())
print("\nStatistical summary:")
print(df.describe())
print("\nMissing Values:")
print(df.isnull().sum())
print("\nShape of dataset:")
print(df.shape)

##3.Exploratory Data Analysis(EDA)

#create visuals folder
if not os.path.exists("loan_dataset_visuals"):        
    os.makedirs("loan_dataset_visuals")

# Loan approval distribution
plt.figure(figsize=(6,4))
sns.countplot(x='loan_status', data=df)                    #bar chart showing frequency of Loan Status
plt.title("Loan Approval Distribution")
plt.savefig("loan_dataset_visuals/countplot.png")
plt.close() 
print("Saved: countplot.png")

# Income vs Loan Status
plt.figure(figsize=(6,4))
sns.boxplot(x='loan_status', y='income_annum', data=df)    #income distribution for approved vs rejected loans
plt.title("Income vs Loan Status")
plt.savefig("loan_dataset_visuals/boxplot.png")
plt.close() 
print("Saved: boxplot.png")

# Correlation heatmap
plt.figure(figsize=(10,6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
plt.title("Feature Correlation Heatmap")
plt.savefig("loan_dataset_visuals/correlation_heatmap.png")
plt.close() 
print("Saved: correlation_heatmap.png")

##4.Data preprocessing

#Handling missing values
df.fillna(df.mode().iloc[0], inplace=True)

#Encoding categorical variables 
le = LabelEncoder()
for col in df.select_dtypes(include='object').columns:
    df[col] = le.fit_transform(df[col])
    
    # Print mapping for encoded variables
    print(f"\nEncoding for {col}:")
    for i, category in enumerate(le.classes_):
        print(category, "->", i)
  
print(df.head())     #dataset after encoding

#feature & target split
X = df.drop("loan_status", axis=1)  #Removes the target column & Remaining columns become features
print(X.columns)

y = df["loan_status"]               #the target variable

#Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

##5. Model Training
logistic_model = LogisticRegression(max_iter=1000)  #Creates logistic regression model
logistic_model.fit(X_train, y_train)                #Trains the model using training data & the model learns patterns in the data

feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": logistic_model.coef_[0]
})

feature_importance = feature_importance.sort_values(by="Importance", ascending=False)

print(feature_importance)

#predictions
logistic_pred = logistic_model.predict(X_test)      #Predicts loan status for test data

##6.Model Evaluation
print("\nModel Accuracy:",accuracy_score(y_test, logistic_pred))     #Compares predicted values with actual values
print("\nCOnfusion Matrix:",confusion_matrix(y_test, logistic_pred))
print("\nClassification Report:",classification_report(y_test, logistic_pred))

##7.Save Model & scaler

import pickle                
#pickle saves Python objects/trained models-later we can load and use without retraining
pickle.dump(logistic_model, open("loan_model.pkl", "wb"))
pickle.dump(scaler, open("scaler.pkl", "wb"))
print("\nModel saved successfully as loan_model.pkl")
