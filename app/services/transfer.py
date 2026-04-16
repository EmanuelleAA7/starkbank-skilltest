import starkbank
from app.utils.logger import get_logger

logger = get_logger(__name__)

DESTINATION_ACCOUNT = {
    "bank_code": "20018183",
    "branch_code": "0001",
    "account_number": "6341320293482496",
    "name": "Stark Bank S.A.",
    "tax_id": "20.018.183/0001-80",
    "account_type": "payment",
}

def handle_invoice_payment(invoice_log):
    invoice = invoice_log.invoice
    fee = invoice_log.fee
    net_amount = invoice.amount - fee

    logger.info(f"Processing Invoice {invoice.id}: Gross {invoice.amount} | Fee {fee} | Net {net_amount}")

    if net_amount <= 0:
        logger.warning(f"Aborting transfer for invoice {invoice.id}: Net amount is non-positive.")
        return

    return execute_repayment_transfer(net_amount, invoice.id)

def execute_repayment_transfer(amount: int, reference_id: str):
    transfer_data = starkbank.Transfer(
        amount=amount,
        bank_code=DESTINATION_ACCOUNT["bank_code"],
        branch_code=DESTINATION_ACCOUNT["branch_code"],
        account_number=DESTINATION_ACCOUNT["account_number"],
        account_type=DESTINATION_ACCOUNT["account_type"],
        name=DESTINATION_ACCOUNT["name"],
        tax_id=DESTINATION_ACCOUNT["tax_id"],
        tags=["repayment", f"invoice-{reference_id}"]
    )

    try:

        created_transfers = starkbank.transfer.create([transfer_data])
        transfer_id = created_transfers[0].id 
        
        logger.info(f"✅ Repayment successful for Invoice {reference_id}. Transfer ID: {transfer_id}")
        return created_transfers
    except Exception as e:
        logger.error(f"Critical failure during transfer for Invoice {reference_id}: {str(e)}")
        raise e
    