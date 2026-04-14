from fastapi import FastAPI, Request, Header, HTTPException
import starkbank
from .config import init_starkbank
from .transfers import send_transfer
import logging

# Configuração básica de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Inicializa o SDK
init_starkbank()

@app.get("/")
def read_root():
    return {"status": "Stark Bank Integration Online"}

@app.post("/webhook")
async def receive_webhook(request: Request, digital_signature: str = Header(None, alias="Digital-Signature")):
    """
    Recebe o callback da Stark Bank, valida a assinatura e
    realiza a transferência se o invoice foi creditado.
    """
    body = await request.body()
    payload = body.decode("utf-8")

    try:
        # Validação de segurança obrigatória
        event = starkbank.event.parse(
            content=payload,
            signature=digital_signature
        )

        if event.subscription == "invoice" and event.log.type == "credited":
            invoice = event.log.invoice
            amount = invoice.amount
            
            logger.info(f"Pagamento recebido: R${amount/100:.2f}. Iniciando transferência...")
            
            # Realiza a transferência do valor recebido
            send_transfer(amount=amount)
            
        return {"status": "success"}

    except Exception as e:
        logger.error(f"Erro no processamento do webhook: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid Webhook")