from config.config import MODEL_PATH, PREPROCESSOR_PATH
import joblib
import pandas as pd
import numpy as np


class PredictPipeline:
    def __init__(self):
        self.preprocessor = joblib.load(PREPROCESSOR_PATH)
        self.model = joblib.load(MODEL_PATH)

    def predict(self):
        sample_df = pd.DataFrame([self.data_input()])
        processed_df = self.preprocessor.transform(sample_df)
        predition_log = self.model.predict(processed_df)

        return np.expm1(predition_log[0])

    def data_input(self):
        City = (input("Hyderabad/Mumbai/Pune/Nagpur/Bangalore :"))
        Locality_Tier = input("Premium/Mid/Budget :")
        BHK = int(input("Enter BHK :"))
        Bathrooms = int(input("Enter number of bath rooms :"))
        Super_Area_sqft = float(input("Enter super area squre feet :"))
        Property_Age_years = int(input("Enter age of the property :"))
        Parking = int(input("Enter 1 if avaliable else 0 :"))
        Furnishing = (input("Semi-Furnished/Unfurnished/Fully-Furnished :"))
        Distance_to_CityCenter_km = float(input("Enter distance from city center :"))

        sample_data = {
            "City" : City,
            "Locality_Tier" : Locality_Tier,
            "BHK" : BHK,
            "Bathrooms" : Bathrooms,
            "Super_Area_sqft" : Super_Area_sqft,
            "Property_Age_years" : Property_Age_years,
            "Parking" : Parking,
            "Furnishing" : Furnishing,
            "Distance_to_CityCenter_km" : Distance_to_CityCenter_km
        }

        return sample_data

predict = PredictPipeline()
print("Price :",predict.predict())