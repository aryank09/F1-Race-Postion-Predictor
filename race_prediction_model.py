import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data(data):
    #Converts a dictionary to a pandas DataFrame and preprocesses it.

    df = pd.DataFrame(data).T  #Transpose to have drivers as rows
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Driver'}, inplace=True)
    return df

def handle_missing_values(df):
    #Fills missing values with column mean and drops rows with missing 'Qualifying' data.
    
    df.fillna(df.mean(numeric_only=True), inplace=True)
    df.dropna(subset=['Qualifying'], inplace=True)
    return df

def encode_categorical_data(df):
    #Encodes categorical data using one-hot encoding.

    df = pd.get_dummies(df, columns=['Constructor'], drop_first=True)
    return df

def add_target_column(df, top_n=5):
    #Adds a binary target column 'Top N', indicating if a driver is in the top N based on Driver Points.

    df[f'Top {top_n}'] = df['Driver Points'].rank(ascending=False).le(top_n).astype(int)
    return df

def split_features_target(df, target_column):
    #Splits the DataFrame into features (X) and target (y).

    X = df.drop(columns=['Driver', target_column])
    y = df[target_column]
    return X, y

# Model Training and Evaluation Functions

def train_logistic_regression(X_train, y_train):
    #Trains a logistic regression model.
    
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model

def train_random_forest(X_train, y_train):
    #Trains a random forest classifier.
    
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    #Evaluates the model and prints accuracy and classification report.
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
    print("Classification Report:\n", report)

def feature_importance(model, feature_names):
    #Displays feature importance for tree-based models.
    
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        sorted_importance = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)
        print("Feature Importance:")
        for feature, importance in sorted_importance:
            print(f"{feature}: {importance:.4f}")
    else:
        print("Feature importance is not available for this model.")

#Main Pipeline Function

def main(data):

    #Preprocessing
    df = load_data(data)
    df = handle_missing_values(df)
    df = encode_categorical_data(df)
    df = add_target_column(df, top_n=5)
    
    #Split features and target
    X, y = split_features_target(df, target_column='Top 5')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #Train models
    print("Training Logistic Regression...")
    lr_model = train_logistic_regression(X_train, y_train)
    print("Evaluating Logistic Regression...")
    evaluate_model(lr_model, X_test, y_test)

    print("\nTraining Random Forest...")
    rf_model = train_random_forest(X_train, y_train)
    print("Evaluating Random Forest...")
    evaluate_model(rf_model, X_test, y_test)

    #Feature importance for Random Forest
    print("\nRandom Forest Feature Importance:")
    feature_importance(rf_model, X.columns)
