from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error, root_mean_squared_error
import joblib
from SRC.preprocessing import Datasplit, DataPreprocessor
from SRC.load_data import LoadData
from config.config import PROCESSED_PATH
from SRC.model_trainer import ModelTrainer



loader = LoadData()
splitter = Datasplit()
preprocess = DataPreprocessor()
trainer = ModelTrainer()


df  = loader.load(PROCESSED_PATH)
X = df.drop(columns=["Market_Price_INR_Log"])
y = df["Market_Price_INR_Log"]
x_train, x_test, y_train, y_test = splitter.split(X, y)


numerical_columns = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_columns = X.select_dtypes(include=['object']).columns.tolist()

x_train_preprocessed, x_test_preprocessed = preprocess.preprocessing(x_train, x_test, numerical_columns, categorical_columns)

models = {
    "LinearRegression" : LinearRegression(),
    "RandomForestRegression" : RandomForestRegressor(),
    "GradientBoostingRegression" : GradientBoostingRegressor()
}

def helper(model):
    best_r2 = -1
    best_model = None
    best_name = None
    for model_name, model in models.items():
        trained_model = trainer.train(model, x_train_preprocessed, y_train)
        metrics, r2 = trainer.evalute(trained_model,  x_test_preprocessed, y_test, x_train_preprocessed, y_train)
        final_metrics = {model_name : metrics}
        joblib.dump(metrics, "models/metrics.json")
        if r2 > best_r2:
            best_r2 = r2
            best_model = model
            best_name = model_name

    joblib.dump(best_model, "models/model.pkl")


helper(models)