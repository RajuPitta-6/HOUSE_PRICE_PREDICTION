from pydantic import BaseModel

class HouseModel(BaseModel):
    City : str
    Locality_Tier : str
    BHK : int
    Bathrooms: int
    Super_Area_sqft : float
    Property_Age_years : int
    Parking : int
    Furnishing : str
    Distance_to_CityCenter_km : float