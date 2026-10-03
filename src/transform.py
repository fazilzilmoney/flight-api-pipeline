import json
import pandas as pd
from logger import logger

file_path = "data/flights_20260923_140708.json"

def transform(file_path):

    logger.info("Transformation started")

    try:
        # Read JSON file
        with open(file_path, "r") as file:
            data = json.load(file)

        # Extract aircraft data
        states = data["states"]

        logger.info(f"Records recieved: {len(states)}")


        # Create dataframe

        columns = [
            "aircraft_id",
            "origin_country",
            "callsign",
            "time_position",
            "last_contact",
            "longitude",
            "latitude",
            "baro_altitude",
            "on_ground",
            "velocity",
            "true_track",
            "vertical_rate",
            "sensors",
            "geo_altitude",
            "squawk",
            "spi",
            "position_source"
        ]

        # create dataframe
        df = pd.DataFrame(
            states,
            columns=columns
        )

        # Remove rows without aircraft ID
        df = df.dropna(
            subset=["aircraft_id"]
        )

        # Remove duplicate aircraft records
        df = df.drop_duplicates(
            subset=["aircraft_id"]
        )

        # Fill missing numeric values

        numeric_columns = [
            "longitude",
            "latitude",
            "baro_altitude",
            "velocity"
        ]

        df[numeric_columns] = df[numeric_columns].fillna(0)

        logger.info(
            f"Records after cleaning: {len(df)}"
            )
        print(df.info())

        print(df.head())

        logger.info("Transformation completed")
    
        # Return dataframe to next step
        return df

    except Exception as e:
        logger.error(f"Transformation failed: {e}")

        raise