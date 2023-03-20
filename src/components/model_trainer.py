import os
import sys
from dataclasses import dataclass
from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object,evaluate_model

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_training(self,train_array,test_array):
        try:
            logging.info("Splitting training and testing input data")
            X_train,y_train,X_test,y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:, :-1],
                test_array[:, -1]
            )
            models = {
                "Random Forest":RandomForestRegressor(),
                "Decision Tree":DecisionTreeRegressor(),
                "Gradient Boosting":GradientBoostingRegressor(),
                "Linear Regression":LinearRegression(),
                "K_Neighbours Regression":KNeighborsRegressor(),
                "XGBRegressor":XGBRegressor(),
                "CatBoosting Regression":CatBoostRegressor(),
                "AdaBoost Regressor":AdaBoostRegressor()
            }
            model_report:dict = evaluate_model(X_train,y_train,X_test,y_test,models = models)
            logging.info(f"R2 Metrics Score for each model : {model_report}")

            #Get Best model score
            best_model_score = max(sorted(model_report.values()))

            #Get Best model name
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            # Get Best model object
            best_model_object = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found...",sys)

            logging.info("Best model found after training and predicting data")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model_object
            )
            logging.info("Saving Best model pkl file")
            y_pred = best_model_object.predict(X_test)
            r2_model_score = r2_score(y_test,y_pred)
            return r2_model_score
        except Exception as e:
            raise CustomException(e,sys)
