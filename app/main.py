from fastapi import FastAPI, Request, HTTPException
import starkbank
from app.config import init_starkbank
from app.services.transfer import handle_invoice_payment
from app.utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI()

init_starkbank()

@app.get("/")
async def health_check():
    return {"status": "alive", "service": "stark-bank-integration"}

@app.post("/webhook")
async def webhook_handler(request: Request):
    body = await request.body()
    signature = request.headers.get("stark-signature")

    if not signature:
        logger.error("Missing stark-signature header")
        raise HTTPException(status_code=400, detail="Missing signature")

    try:
        event = starkbank.event.parse(
            content=body.decode("utf-8"),
            signature=signature
        )

        if event.subscription == "invoice" and event.log.type == "paid":
            invoice_log = event.log 
            handle_invoice_payment(invoice_log)

        return {"status": "success", "message": "Event processed"}

    except Exception as e:
        logger.error(f"Failed to process webhook event: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid event payload")
    