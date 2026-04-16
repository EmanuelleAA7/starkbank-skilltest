import schedule
import time
from app.utils.logger import get_logger
from app.services.invoice import create_random_invoices
from app.config import init_starkbank


logger = get_logger("scheduler_service")

def job():
    logger.info("Executing scheduled job: Invoice Generation")
    try:
        create_random_invoices()
    except Exception as e:
        logger.error(f"Job execution failed: {str(e)}")

def start_automation():
    init_starkbank()
    
    logger.info("Scheduler started. Cycle: Every 3 hours.")

    schedule.every(3).hours.do(job)

    job()

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    start_automation()
