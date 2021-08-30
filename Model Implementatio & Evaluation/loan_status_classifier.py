# -*- coding: utf-8 -*-
"""Loan Status Classifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18OlOFBXBvAzPJJD4MJAmQA6xPuCVVAzx

## **Import Dependencies**
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score, RandomizedSearchCV, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB

from sklearn import metrics
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score, f1_score, plot_roc_curve, roc_auc_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from imblearn.over_sampling import SMOTE

import warnings
warnings.filterwarnings("ignore")

"""## **Import & Getting Know About The Dataset**"""

df = pd.read_csv("/content/drive/MyDrive/Colab Materials/Loan Dataset/train.csv")
df.head()

# check the dataset shape( number of rows & columns)
df.shape

#checking data types
df.dtypes

# remove unwanted columns
df.drop(['Loan_ID'],axis=1,inplace=True)

"""## **Analyse & Visualize The Distribution of Target Variable**

## **Handle Missing Values**
"""

#checking for null values
df.isnull().sum()

df.hist(figsize=(15,15))
plt.show()

# fill missing values of numerical variable by using mean
df['LoanAmount'] = df['LoanAmount'].fillna(df['LoanAmount'].median())

# loan term shows discrete data but it higher number of categories. therefore in here we handle it as a continues varible
df['Loan_Amount_Term'] = df['Loan_Amount_Term'].fillna(df['Loan_Amount_Term'].mode()[0])

# fill missing values of categorical variables by using mode
df['Credit_History'] = df['Credit_History'].fillna(df['Credit_History'].mode()[0])
df['Gender'] = df['Gender'].fillna(df['Gender'].mode()[0])
df['Married'] = df['Married'].fillna(df['Married'].mode()[0])
df['Dependents'] = df['Dependents'].fillna(df['Dependents'].mode()[0])
df['Self_Employed'] = df['Self_Employed'].fillna(df['Self_Employed'].mode()[0])

df['Loan_Status'].value_counts()

#check null values after handled it 
df.isnull().sum()

# visualiza the distribution of dependent variable (Loan Status)
plt.figure(figsize=(12,7))

df['Loan_Status'].value_counts().plot.pie(autopct='%1.1f%%')
centre=plt.Circle((0,0),0.7,fc='white')

fig=plt.gcf()
fig.gca().add_artist(centre)

# display first 5 rows of balanced dataset
df.sample(5)

"""## **Numeric Variable Distribution**"""

df.hist(figsize=(15,15))
plt.show()

"""### *Credit history seems to like a categorical variable so we consider as categorical varible for further studies & analysis*

## **Identify outliers In More Accurate Way For Numeric Values**
"""

def outliers_check(column):

  title = str(column) + " Box Plot "
  plt.subplots(figsize=(5,5))
  sns.boxplot(data=df[str(i)]).set_title(title)
  plt.show()

for i in df[['ApplicantIncome',	'CoapplicantIncome',	'LoanAmount',	'Loan_Amount_Term']].columns:
  
    outliers_check(i)

df.describe().T

"""## **Categorical variable Analysis**"""

plt.figure(figsize=(10,8.5))
sns.countplot(df['Property_Area'])
plt.title("Property Area",size=15)
plt.show()

plt.figure(figsize=(10,8.5))
sns.countplot(df['Self_Employed'])
plt.title("Self Employ Status",size=15)
plt.show()

plt.figure(figsize=(10,8.5))
sns.countplot(df['Education'])
plt.title("Education",size=15)
plt.show()

plt.figure(figsize=(10,8.5))
sns.countplot(df['Married'])
plt.title("Matial Status",size=15)
plt.show()

plt.figure(figsize=(10,8.5))
sns.countplot(df['Gender'])
plt.title("Gender",size=15)
plt.show()

plt.figure(figsize=(10,8.5))
sns.countplot(df['Dependents'])
plt.title("Dependents",size=15)
plt.show()

plt.figure(figsize=(10,8.5))
sns.countplot(df['Credit_History'])
plt.title("Credit History",size=15)
plt.show()

df['Credit_History'].value_counts()

"""## **Exploratory Data Analysis**

---
"""

df.head()

"""> ## Loan staus vs **Gender**"""

plt.figure(figsize=(10,8.5))
sns.countplot(x='Loan_Status',hue='Gender',data=df)
plt.show()

"""> ## Loan staus vs **Matial Status**"""

plt.figure(figsize=(10,8.5))
sns.countplot(x='Loan_Status',hue='Married',data=df)
plt.show()

"""> ## Loan staus vs **Dependents**"""

plt.figure(figsize=(10,8.5))
sns.countplot(x='Loan_Status',hue='Dependents',data=df)
plt.show()

"""> ## Loan staus vs **Employed Status**"""

plt.figure(figsize=(10,8.5))
sns.countplot(x='Loan_Status',hue='Self_Employed',data=df)
plt.show()

"""> ## Loan staus vs **Property Status**"""

plt.figure(figsize=(10,8.5))
sns.countplot(x='Loan_Status',hue='Property_Area',data=df)
plt.show()

"""> ## Loan Status vs **Education Status**"""

plt.figure(figsize=(10,8.5))
sns.countplot(x='Loan_Status',hue='Education',data=df)
plt.show()

"""> ## Loan staus vs **Credit History**"""

plt.figure(figsize=(10,8.5))
sns.countplot(x='Loan_Status',hue='Credit_History',data=df)
plt.show()

"""> ## Loan staus vs **Applicant Income**"""

pl=sns.relplot(x='ApplicantIncome',y='ApplicantIncome',data=df,hue='Loan_Status',style='Loan_Status')
pl.fig.set_size_inches(10,7)
plt.show()

"""> ## Loan staus vs **Co-Applicant Income**"""

pl=sns.relplot(x='CoapplicantIncome',y='CoapplicantIncome',data=df,hue='Loan_Status',style='Loan_Status')
pl.fig.set_size_inches(10,7)
plt.show()

"""> ## Loan staus vs **Loan Amount**"""

pl=sns.relplot(x='LoanAmount',y='LoanAmount',data=df,hue='Loan_Status',style='Loan_Status')
pl.fig.set_size_inches(10,7)
plt.show()

"""> ## Loan staus vs **Loan Amount Term**"""

pl=sns.relplot(x='Loan_Amount_Term',y='Loan_Amount_Term',data=df,hue='Loan_Status',style='Loan_Status')
pl.fig.set_size_inches(10,7)
plt.show()

sns.pairplot(df[['Loan_Amount_Term','LoanAmount', 'CoapplicantIncome','ApplicantIncome']])

# label encode for categorical variables
label = LabelEncoder()

df['Credit_History'] = label.fit_transform(df['Credit_History'])
df['Education'] = label.fit_transform(df['Education'])
df['Property_Area'] = label.fit_transform(df['Property_Area'])
df['Self_Employed'] = label.fit_transform(df['Self_Employed'])
df['Dependents'] = label.fit_transform(df['Dependents'])
df['Married'] = label.fit_transform(df['Married'])
df['Gender'] = label.fit_transform(df['Gender'])
df['Loan_Status'] = label.fit_transform(df['Loan_Status'])

# check result after label encode
df.head(5)

features=['Gender', 'Dependents',	'Married',	'Education',	'Self_Employed', 'Credit_History', 'Property_Area']

plt.figure(figsize=(23,10))
for i in enumerate(features):
  plt.subplot(2,7,i[0]+1)
  sns.countplot(df[i[1]])

"""### **Releationship Between Each Numerical Variable**"""

plt.subplots(figsize = (14,10))
sns.heatmap(df[['ApplicantIncome','CoapplicantIncome','LoanAmount','Loan_Amount_Term','Loan_Status']].corr(),
            annot=True,fmt='.3g', vmin=-1, vmax=1, center= 0).set_title("Corelation Between Attributes")
plt.show()

"""### **Model Implementation**"""

# pre-processing
y = df['Loan_Status']
x = df.drop(['Loan_Status'],axis=1)

# define object for over sampling
from imblearn.over_sampling import SMOTE
over=SMOTE()

# balance the dataset using over sampling method
x,y=over.fit_resample(x,y)

plt.figure(figsize=(7,7.5))
sns.countplot(y)
plt.title("Distribution of Loan Status After Over Sampling",size=15)
plt.show()

# scale the independent variable 
sc = StandardScaler()
x = sc.fit_transform(x)

# divide into training set & test sets
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.25, random_state=42)

#define functions for fit, & predict with each models
def models(mod,x_t,y_t,x_tes,y_tes,x_source,y_source):
    
    #Fit model
    mod.fit(x_t,y_t)
    
    #Predict Model
    pred = mod.predict(x_tes)
    
    #Accuracy Score
    accuracy = accuracy_score(y_tes,pred)

    #AUC_ROC Score
    AUC_ROC_Score = roc_auc_score(y_tes,pred)
    
    #Cross Validation Score
    cross_validation = cross_val_score(mod,x_source,y_source,cv=5)

    print("Accuracy Is : ",round(accuracy*100,4),"%")
    
    print("-------------------------------------------")   
    
    print('Cross validations mean score ',round(np.mean(cross_validation)*100,4),'%')
    
    print("-------------------------------------------")

    print('AUC_ROC Score ',round(np.mean(AUC_ROC_Score)*100,4),'%')

    print("-------------------------------------------")
    
    #Confusion Metrix
    print(confusion_matrix(y_tes, pred))
    
    print("-------------------------------------------")    
    
    #Recall Score , Percision Score, F1 Score
    print("Recall Score :",recall_score(y_tes, pred, average='weighted'))
    print("Percision Score :",precision_score(y_tes, pred, average='weighted'))
    print("F1 Score :",f1_score(y_tes, pred, average='weighted'))

"""### **LogisticRegression**"""

model = LogisticRegression()

models(model,x_train,y_train,x_test,y_test,x,y )

"""### **Decision Tree Classifier**"""

model_1 = DecisionTreeClassifier(random_state=42)
models(model_1,x_train,y_train,x_test,y_test,x,y )

"""### **RandomForestClassifier**"""

model_2 = RandomForestClassifier(n_estimators=150,random_state=42)
models(model_2,x_train,y_train,x_test,y_test,x,y )

"""### **Extra Trees Classifier**"""

model_3 = ExtraTreesClassifier(random_state=42)
models(model_3,x_train,y_train,x_test,y_test,x,y )

"""### **Support Vector Machine**"""

model_4 = svm.SVC()
models(model_4,x_train,y_train,x_test,y_test,x,y )

"""### *Random Forest Classifier model gives higher score accuracy more than other models. Therefore Random Forest Classifier model consider as the model for further implementations & evaluations*

### **Hyper Parameter Tuning with Random Forest Classifer Model**
"""

# define parameters & fit the model
parameters = {'n_estimators':[100, 200, 300, 400, 500],
            'criterion':['gini','entropty'],
            'max_depth':[None,1,2,3,4,5,6,7,8,9,10],
           'max_features':['int','float','auto','log2'],'random_state':[42]}

best_model = RandomForestClassifier()

clf = GridSearchCV(best_model, parameters, cv=5)
clf.fit(x_train, y_train)

# add model values to dataframe
df_grid = pd.DataFrame(clf.cv_results_)

# rank the datapoint by ranking
df_grid.sort_values(by=['rank_test_score']).head(3)

# best parameters
clf.best_params_

# highest score 
clf.best_score_

# model estimater/parameters
clf.best_estimator_

"""### **Test Model With Tuned Values** : *Decision Tree Classifier*"""

# test model with tuned values
Tuned_model = RandomForestClassifier(bootstrap=True, ccp_alpha=0.0, class_weight=None,
                       criterion='gini', max_depth=None, max_features='auto',
                       max_leaf_nodes=None, max_samples=None,
                       min_impurity_decrease=0.0, min_impurity_split=None,
                       min_samples_leaf=1, min_samples_split=2,
                       min_weight_fraction_leaf=0.0, n_estimators=400,
                       n_jobs=None, oob_score=False, random_state=42, verbose=0,
                       warm_start=False)


models(Tuned_model,x_train,y_train,x_test,y_test,x,y )

"""### *Only tuned with few values due to the lack of hardware performance. therefore after get tuned values test the accuracy with some "n_estimators"*

### **ROC-AOC Curve**
"""

# calculate false positive rate & true posituve rate
fpred=pd.Series(Tuned_model.predict_proba(x_test)[:,1])
fpr,tpr,threshold=metrics.roc_curve(y_test,fpred)

# visualize the ROC-AOC Curve
plt.figure(figsize=(7,7))
plt.plot(fpr,tpr,color='k',label='ROC')
plt.plot([0,1],[0,1],color='b',linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC-AUC curve')
plt.legend()

"""### *After parameters tuned Random Forest Classifier Model gives higher accuracy , cross validation & ROC value. therefore we can get this model with tuned paramter values as our final model*

### **Test Final Model With Input Values**
"""

df.head(3)

def classifer(input_data):

  input_array = np.asarray(input_data)
  arr_reshape = input_array.reshape(1,-1)

  scaled = sc.transform(arr_reshape)

  Loan_pred =  Tuned_model.predict(scaled)
  print(Loan_pred[0])


def main():

  Gender  = 'Male'                
  Martial_st = 'Unmarried'               
  Dependents = '0'            
  Education = 'Graduate'          
  Self_Employed = 'No'            
  Credit_History = 'Yes' 
  Property_Area = 'Semi Urban'

  ApplicantIncome = 5849        
  CoapplicantIncome =  0  
  LoanAmount = 146.412162         
  Loan_Amount_Term =  360


#change gender.........................................
  if Gender == 'Female':
      Gender = 0

  elif Gender == 'Male':
      Gender = 1

#change martial status..................................
  if Martial_st == 'Maried':
      Martial_st = 1

  elif Martial_st == 'Unmarried':
      Martial_st = 0

#change Dependents status..................................
  if Dependents == '0':
      Dependents = 0

  elif Dependents == '1':
      Dependents = 1

  elif Dependents == '2':
      Dependents = 2

  elif Dependents == '3+':
      Dependents = 3 

#change Education status..................................
  if Education == 'Graduate':
      Education = 0

  elif Education == 'Not Graduate':
      Education = 1

#change Self_Employed status..................................
  if Self_Employed == 'Yes':
      Self_Employed = 1

  elif Self_Employed == 'No':
      Self_Employed = 0

#change credit history status..................................
  if Credit_History == 'Yes':
      Credit_History = 1

  elif Credit_History == 'No':
      Credit_History = 0

#change Property Area status..................................
  if Property_Area == 'Urban':
      Property_Area = 0

  elif Property_Area == 'Rural':
      Property_Area = 1

  elif Property_Area == 'Semi Urban':
      Property_Area = 2

# add feature value to set          
  input_data = [Gender,	Martial_st, Dependents,	Education, Self_Employed, float(ApplicantIncome),	float(CoapplicantIncome), float(LoanAmount), float(Loan_Amount_Term), Credit_History, Property_Area]


# tranfer value to model function & pre proccessings
  classifer(input_data)



#main
main()

"""### **Save Scaler**"""

import pickle
scalerfile = 'scaler.save'
pickle.dump(sc, open(scalerfile, 'wb'))

"""### **Save Model**"""

with open('Loan_cls_model','wb') as f:
  pickle.dump(Tuned_model,f)

"""### **Save Notebook File as HTML**"""

# Commented out IPython magic to ensure Python compatibility.
# %%shell
# jupyter nbconvert --to html '/content/Loan_Status_Classifier.ipynb'

