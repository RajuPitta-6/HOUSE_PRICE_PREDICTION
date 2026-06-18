from SRC.load_data import LoadData
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import joblib

class Datasplit:
    def split(self, X, y):
        return train_test_split( X, y, test_size=0.2, random_state=42)


class DataPreprocessor:
    def preprocessing(self,x_train, x_test, num, cat):

        num_pipeline = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')),('scaler', StandardScaler())])
        cat_pipeline = Pipeline(steps=[('imputer', SimpleImputer(strategy='most_frequent')),('encoding', OneHotEncoder(handle_unknown='ignore'))])

        preprocessor = ColumnTransformer(transformers=[('nums', num_pipeline, num),('cat', cat_pipeline, cat)])

        x_train_preprocessed = preprocessor.fit_transform(x_train)
        x_test_preprocessed = preprocessor.transform(x_test)

        joblib.dump(preprocessor, "models/preprocessor.pkl")

        return x_train_preprocessed, x_test_preprocessed
