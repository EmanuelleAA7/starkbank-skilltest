Stark Bank Challenge - Invoice Repayment SystemThis repository contains a Python-based automated system designed to manage Stark Bank Invoices and automate the repayment process.

🚀 OverviewThe system performs three main automated tasks:Invoice Generation: Every 3 hours, a random number of Invoices (between 8 and 12) are created for random persons.Webhook Integration: A FastAPI-based server listens for "Invoice Paid" events.Automated Repayment: Upon receiving a payment notification, the system automatically transfers the net amount (total minus fees) to the Stark Bank corporate account.🛠️ ArchitectureThe project follows a modular structure to ensure maintainability and testability:app/services/: Contains the business logic for creating invoices and handling transfers.app/webhooks/: FastAPI routes to handle incoming POST requests from Stark Bank.app/utils/: Shared utilities like logging and environment configuration.tests/: Unit tests using pytest and unittest.mock.

📦 Installation & Setup1. RequirementsPython 3.10+Stark Bank API Keys (ECDSA)2. Environment VariablesCreate a .env file in the root directory:Snippet de códigoPROJECT_ID="your-project-id"
PRIVATE_KEY="""-----BEGIN EC PRIVATE KEY-----
...
-----END EC PRIVATE KEY-----"""
ENVIRONMENT="sandbox"
3. Install DependenciesPowerShellpython -m pip install -r requirements.txt

🚦 How to RunRun the Application (Server & Scheduler)To start the webhook server and the background scheduler:PowerShellpython main.py
Run Unit TestsTo execute the test suite (including the transfer logic we validated):PowerShellpython -m pytest
🧪 Implementation DetailsThe Repayment LogicThe system is designed to be resilient. When an invoice is paid:It calculates:$$Net = Gross - Fee$$It checks if the amount is positive.It issues a starkbank.transfer.create call with the exact credentials provided in the challenge requirements.LoggingAll operations are logged with timestamps and status tags (INFO/ERROR) to allow easy monitoring of the automation flow.📝 Challenge Requirements Coverage[x] Create 8 to 12 Invoices every 3 hours.[x] Handle Webhook events for paid Invoices.[x] Transfer the received amount (after fees) to the provided account.[x] Use the Stark Bank SDK.[x] Modular and clean code structure.