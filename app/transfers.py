import starkbank
import logging

logger = logging.getLogger(__name__)

# Conta destino fixa — dados fornecidos no desafio
DESTINATION_ACCOUNT = {
    "bank_code": "20018183",
    "branch_code": "0001",
    "account_number": "6341320293482496",
    "name": "Stark Bank S.A.",
    "tax_id": "20.018.183/0001-80",
    "account_type": "payment",
}

def send_transfer(amount: int) -> starkbank.Transfer:
    """
    Envia uma transferência para a conta destino.

    Args:
        amount: valor em centavos a transferir

    Returns:
        O objeto Transfer criado
    """
    if amount <= 0:
        raise ValueError(f"Valor inválido para transferência: {amount}")

    transfer = starkbank.transfer.create([
        starkbank.Transfer(
            amount=amount,
            bank_code=DESTINATION_ACCOUNT["bank_code"],
            branch_code=DESTINATION_ACCOUNT["branch_code"],
            account_number=DESTINATION_ACCOUNT["account_number"],
            account_type=DESTINATION_ACCOUNT["account_type"],
            name=DESTINATION_ACCOUNT["name"],
            tax_id=DESTINATION_ACCOUNT["tax_id"],
        )
    ])

    logger.info(f"Transferência criada: R${amount/100:.2f} → {DESTINATION_ACCOUNT['name']}")
    return transfer[0]