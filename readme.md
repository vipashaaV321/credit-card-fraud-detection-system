# Credit-Card-Fraud-Detection

<img src="https://i.pinimg.com/474x/11/73/5f/11735f221b016526a0426064352035d5.jpg" height="400" width="500"/> 

## This Project simulates How can we train a Machine Learning Model to detect credit card frauds in online transactions and how can we implement Machine Learning Model in realtime e-commerce website.

<hr/>

# Technology : 
<ul>
  <li>
    Python (All-over environment)
  </li>
  <li>
    numpy,pandas,matplotlib (for EDA)
  </li>
  <li>
    Scikit-learn (to implement SVM algorithm)
  </li>
  <li>
  Flask (website) 
  </li>
  <li>
  Pickle (Model Deployment)
  </li>
  </ul>
  
# About Machine Learning Model
 
## Data Source: https://www.kaggle.com/mlg-ulb/creditcardfraud

<hr/>

This dataset contains only numerical input variables which are the result of a PCA transformation. Unfortunately, due to confidentiality issues original features are not provided and more background information about the data is also not present. Features V1, V2, ... V28 are the principal components obtained with PCA, the only features which have not been transformed with PCA are 'Time' and 'Amount'. Feature 'Time' contains the seconds elapsed between each transaction and the first transaction in the dataset. The feature 'Amount' is the transaction Amount, this feature can be used for example-dependant cost-senstive learning. Feature 'Class' is the response variable and it takes value 1 in case of fraud and 0 otherwise.

we have done Exploratory Data Analysis on dataset to clean and pre-process our data and then we have reshaped our dataset with label encoding and over sampling. 

Here we have used Support vector Machine for Classify Fraudulent and Non-Fraudulent Transactions, The supervised detection algorithm is a method based on supervised machine learning algorithms that are trained on some labelled data to build predictive models, which will allow us to predict the output of new unseen data; it is named supervised in view of the fact that the learning process is performed under the supervision of an output variable. 
 
 ## Steps Involved
1. Importing the required packages into our python environment.
2. Importing the data
3. Processing the data to our needs and Exploratory Data Analysis
4. Feature Selection and Data Split
5. Building SVM classification models
6. Evaluating the created classification model

<hr/>

# Model Deployment

we can deploy our machine learning model with pickle, It converts ml model into byte-streams. After deploying our model we can use this into any application framework like flask or django. 

<hr/>

# How to run the Project

In order to run the project we have to run command "Python Main.py"..