import starkbank
import random
from datetime import datetime

def create_random_invoices():
    """
    Gera entre 8 e 12 faturas (invoices) para pessoas aleatórias.
    """
    number_of_invoices = random.randint(8, 12)
    invoices = []

    for _ in range(number_of_invoices):
        # Gerando dados fictícios simples para o desafio
        # Em um cenário real, você usaria um gerador de CPF/Nomes
        invoices.append(starkbank.Invoice(
            amount=random.randint(1000, 100000), # Valor entre R$ 10,00 e R$ 1.000,00
            name=f"Customer {random.randint(1, 1000)}",
            tax_id="20.018.183/0001-80", # Usando o próprio CNPJ da Stark para simplificar
        ))

    created_invoices = starkbank.invoice.create(invoices)
    print(f"[{datetime.now()}] {len(created_invoices)} invoices criadas com sucesso.")
    return created_invoices