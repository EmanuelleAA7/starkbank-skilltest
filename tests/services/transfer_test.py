import pytest
from unittest.mock import MagicMock, patch
from app.services.transfer import handle_invoice_payment


def test_handle_invoice_payment_success():
    mock_log = MagicMock()
    mock_log.invoice.id = "INV123"
    mock_log.invoice.amount = 10000
    mock_log.fee = 500

    with patch('starkbank.transfer.create') as mock_create:
        mock_create.return_value = [MagicMock(id="TRANS456")]

        handle_invoice_payment(mock_log)

        assert mock_create.call_count == 1

        lista_de_transfers = mock_create.call_args.args[0]
        objeto_transfer = lista_de_transfers[0]

        assert objeto_transfer.amount == 9500
        assert objeto_transfer.tax_id == "20.018.183/0001-80"


def test_handle_invoice_payment_insufficient_funds():
    mock_log = MagicMock()
    mock_log.invoice.amount = 500
    mock_log.fee = 500

    with patch('starkbank.transfer.create') as mock_create:
        handle_invoice_payment(mock_log)
        mock_create.assert_not_called()


def test_handle_invoice_payment_sdk_error():
    mock_log = MagicMock()
    mock_log.invoice.amount = 1000
    mock_log.fee = 10

    with patch('starkbank.transfer.create') as mock_create:
        mock_create.side_effect = Exception("API Error")

        with pytest.raises(Exception):
            handle_invoice_payment(mock_log)
            