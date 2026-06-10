import pandas as pd
from pathlib import Path
from config.config import RAW_DATA_PATH

class LoadData:
    def load(self,path:Path):
        try:
            if path.suffix.lower() != ".csv":
                raise ValueError ("only csv files allowed !")
            if not path.exists():
                raise FileNotFoundError(f"{path} doesnot exist !")
            df = pd.read_csv(path)
            
            if df.empty:
                raise ValueError("File doesn't contains data")

            return df
        except Exception as e:
            raise ValueError (f"Error : {e}")
        