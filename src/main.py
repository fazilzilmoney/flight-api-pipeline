import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from extract import extract
from transform import transform
from load import load
from logger import logger


load_dotenv()


def save_pipeline_run(
    started_at,
    completed_at,
    records_extracted,
    records_inserted,
    records_skipped,
    records_failed,
    status,
    error_message=None
):

    db_url = (
        f"postgresql://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )

    engine = create_engine(db_url)

    duration = (
        completed_at - started_at
    ).total_seconds()

    query = text("""
        INSERT INTO pipeline_runs (
            started_at,
            completed_at,
            records_extracted,
            records_inserted,
            records_skipped,
            records_failed,
            status,
            error_message,
            duration_seconds
        )
        VALUES (
            :started_at,
            :completed_at,
            :records_extracted,
            :records_inserted,
            :records_skipped,
            :records_failed,
            :status,
            :error_message,
            :duration_seconds
        )
    """)

    with engine.begin() as connection:

        connection.execute(
            query,
            {
                "started_at": started_at,
                "completed_at": completed_at,
                "records_extracted": records_extracted,
                "records_inserted": records_inserted,
                "records_skipped": records_skipped,
                "records_failed": records_failed,
                "status": status,
                "error_message": error_message,
                "duration_seconds": duration
            }
        )

    engine.dispose()


start_time = datetime.now()

try:

    logger.info("Pipeline started")

    # Extract
    file_path = extract()

    # Transform
    df = transform(file_path)

    # Load
    stats = load(df)

    # Pipeline statistics
    records_extracted = len(df)
    records_inserted = stats["records_inserted"]
    records_skipped = stats["records_skipped"]
    records_failed = stats["records_failed"]

    completed_at = datetime.now()

    duration = (
        completed_at - start_time
    ).total_seconds()

    logger.info(
        f"Pipeline summary | "
        f"Extracted: {records_extracted} | "
        f"Inserted: {records_inserted} | "
        f"Skipped: {records_skipped} | "
        f"Failed: {records_failed}"
    )

    logger.info(
        f"Pipeline completed successfully "
        f"in {duration:.2f} seconds"
    )

    # Save pipeline metadata
    save_pipeline_run(
        started_at=start_time,
        completed_at=completed_at,
        records_extracted=records_extracted,
        records_inserted=records_inserted,
        records_skipped=records_skipped,
        records_failed=records_failed,
        status="SUCCESS"
    )


except Exception as e:

    completed_at = datetime.now()

    logger.exception("Pipeline failed")

    try:

        save_pipeline_run(
            started_at=start_time,
            completed_at=completed_at,
            records_extracted=0,
            records_inserted=0,
            records_skipped=0,
            records_failed=1,
            status="FAILED",
            error_message=str(e)
        )

    except Exception:

        logger.exception(
            "Could not save failed pipeline run"
        )

    print(
        "Pipeline failed. Check logs for details."
    )