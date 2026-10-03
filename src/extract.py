import requests
import json
from datetime import datetime
from logger import logger


def extract():

    logger.info("API extraction started")

    try:
        url="https://opensky-network.org/api/states/all"

        # API request
        response=requests.get(url, timeout=30)

        response.raise_for_status()

        data=response.json()

        record_count = len(data['states'])

        logger.info(f"API returned {record_count} aircraft records")

        # create filename
        filename=(
            f"data/flights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        # save raw data
        with open(filename,"w") as file:
            json.dump(data,file)

        logger.info(f"Raw data saved: {filename}")

        # return file location to Next step. 
        return filename

    except requests.RequestException as e:
        logger.error(f"API request failed: {e}")

        raise

    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise