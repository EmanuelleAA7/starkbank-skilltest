import starkbank
import random
from datetime import datetime, timedelta
from app.utils.logger import get_logger

logger = get_logger(__name__)

def create_random_invoices():
    invoice_list = []
    batch_size = random.randint(8, 12)

    for i in range(batch_size):
        invoice_list.append(starkbank.Invoice(
            amount=random.randint(1000, 100000), 
            name=f"Test Customer {i + 1}",
            tax_id="20.018.183/0001-80", 
            due=(datetime.utcnow() + timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            tags=["batch-test"]
        ))

    try:
        created = starkbank.invoice.create(invoice_list)
        logger.info(f"Successfully issued {len(created)} invoices.")
        return created
    except Exception as e:
        logger.error(f"Error creating invoice batch: {str(e)}")
        return []
    