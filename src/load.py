import os
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.dialects.postgresql import insert
from logger import logger

load_dotenv()


def load(df):

    logger.info(f"Loading {len(df)} records into PostgreSQL")

    try:
        # Database connection
        db_url = (
            f"postgresql://{os.getenv('DB_USER')}:"
            f"{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:"
            f"{os.getenv('DB_PORT')}/"
            f"{os.getenv('DB_NAME')}"
        )

        engine = create_engine(db_url)

        # Convert NaN to None
        df = df.astype(object).where(pd.notna(df), None)

        records = df.to_dict(orient="records")

        if not records:
            logger.info("No records to load")
            return {
                "records_inserted": 0,
                "records_skipped": 0,
                "records_failed": 0
            }

        # Get PostgreSQL table
        metadata = MetaData()

        aircraft_positions = Table(
            "aircraft_positions",
            metadata,
            autoload_with=engine
        )

        # Incremental insert
        stmt = insert(aircraft_positions).values(records)

        stmt = stmt.on_conflict_do_nothing(
            constraint="unique_aircraft_last_contact"
        )

        # Execute
        with engine.begin() as connection:
            result = connection.execute(stmt)

        inserted = result.rowcount or 0
        skipped = len(records) - inserted

        logger.info(f"Records received: {len(records)}")
        logger.info(f"Records inserted: {inserted}")
        logger.info(f"Duplicate records skipped: {skipped}")
        logger.info("Loading completed")

        return {
            "records_inserted": inserted,
            "records_skipped": skipped,
            "records_failed": 0
        }

    except Exception:
        logger.exception("Loading failed")
        raise

    finally:
        if "engine" in locals():
            engine.dispose()