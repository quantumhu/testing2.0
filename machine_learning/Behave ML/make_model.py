import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier

def model_creator(drop_features):
    contents = pd.read_csv('/Users/claremcmullen/PycharmProjects/Behave ML/train-2.csv')
    contents['Survived'] = contents['Survived'].astype(bool)
    contents['Pclass'] = contents['Pclass'].astype(object)
    features = contents.drop(columns=drop_features)

    target = contents['Survived']
    cats = features.select_dtypes(include='object').columns
    numeric = features.select_dtypes(include='number').columns

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.20, random_state=0)

    numeric_features = numeric
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    categorical_features = cats
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])


    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])

    clas = Pipeline(steps=[('preprocessor', preprocessor),
                          ('classifier', RandomForestClassifier())])

    X_train = X_train[[*numeric_features, *categorical_features]]
    X_test = X_test[[*numeric_features, *categorical_features]]


    clas.fit(X_train, y_train)

    #print("Training accuracy: %0.4f" % clas.score(X_train, y_train))
    #print("Testing accuracy: %0.4f" % clas.score(X_test, y_test))
    #print(type(clas))
    return clas

#model_creator(['PassengerId', 'Name','Ticket','Cabin','Survived'])

def get_testing_set(drop_features):
    contents = pd.read_csv('/Users/claremcmullen/PycharmProjects/Behave ML/train-2.csv')
    contents['Survived'] = contents['Survived'].astype(bool)
    contents['Pclass'] = contents['Pclass'].astype(object)
    features = contents.drop(columns=drop_features)

    target = contents['Survived']
    cats = features.select_dtypes(include='object').columns
    numeric = features.select_dtypes(include='number').columns

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.20, random_state=0)

    return X_test, y_test

