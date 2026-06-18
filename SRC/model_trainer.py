from sklearn.metrics import r2_score, mean_absolute_error, root_mean_squared_error

class ModelTrainer:
    def train(self, model, x_train_processed, y_train):
        model.fit(x_train_processed, y_train)
        return model
    
    def evalute(self, model, x_test, y_test, x_train_processed,  y_train):
        preds = model.predict(x_test)
        train_preds = model.predict(x_train_processed)

        metrics = {
            "R2": r2_score(y_test, preds),
            "MAE" : mean_absolute_error(y_test, preds),
            "RMSE" : root_mean_squared_error(y_test, preds),
            "Train_R2" : r2_score(y_train, train_preds)
        }
        return metrics, r2_score(y_test, preds)
