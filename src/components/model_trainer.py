import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import(
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
from src.utils import evaluate_models



@dataclass
class ModeltrainerConfig:
    trained_model_file_path = os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModeltrainerConfig()

    def initiate_model_training(self,train_array,test_array):
        try:
            logging.info("Splitting training and test data")
            x_train,y_train,x_test,y_test= (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1],
            ) 

            models = {
                "Random Forrest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Neihgbors Classifier": KNeighborsRegressor(),
                "XGBClassifier": XGBRegressor(),
                "Cat Boosting Classifier": CatBoostRegressor(verbose= False),
                "AdaBoost Classfier": AdaBoostRegressor()
            }


            model_report:dict = evaluate_models(x_train= x_train, y_train=y_train,x_test= x_test,y_test=y_test,models=models)


            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            
            best_model = models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("No best model found")
            
            logging.info(f"Best found model on both training and testing dataset: {best_model_name}")


            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj= best_model
            ) 

            predicted = best_model.predict(x_test)
            return r2_score



        except Exception as e:
            raise CustomException(e,sys)
