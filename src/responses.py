from pathlib import Path

LOG_RESPONSE = """<a href="https://qbo.intuit.com/app/creditcardexpense?&txnId=144">Expense</a> added to QuickBooks

Payee: WalMart
Payment account: Cash
Payment date: Today
Payment method: Cash

Item 1:
    Category: Meals and entertainment
    Description: Snacks
    Quantity: 1
    Amount: USD 84

Total: USD 84"""

INVOICE_RESPONSE = """Invoice details to ABC Company
Customer email: purchasing@abc.com
Invoice date: Today
Due date: in a month (12/20/2024)

Item 1: Large TV Sets
    Quantity: 100
    Amount: USD 60000

Item 2: Setup Fees
    Quantity: 1
    Amount: USD 1000
    Service date: Today (11/20/2024)

Total: USD 61000

Message on invoice: It is a pleasure doing business with you!

Type y to send, n to abort, others to modify"""

UPDATED_INVOICE_RESPONSE = """Updated invoice details to ABC Company
# ... (rest of the response)
"""

PNL_RESPONSE = """Income
$10,200.77
# ... (rest of the response)
"""

PHOTO_RESPONSE = """<a href="https://qbo.intuit.com/app/creditcardexpense?&txnId=144">Expense</a> details
# ... (rest of the response)
"""

def get_response_for_message(text):
    text = text.lower()
    
    if "pnl" in text:
        return {
            'type': 'document',
            'file_path': 'ProfitandLoss.pdf',
            'filename': "Profit and Loss.pdf",
            'caption': PNL_RESPONSE
        }
    
    if "landscaping" in text:
        return {
            'type': 'document',
            'file_path': 'Sales by Landscaping Summary.pdf',
            'filename': "Sales by Landscaping Summary.pdf"
        }
        
    if "log" in text:
        return {'type': 'text', 'text': LOG_RESPONSE}
    
    if "invoice" in text:
        return {'type': 'text', 'text': INVOICE_RESPONSE}
        
    if "1400" in text:
        return {'type': 'text', 'text': UPDATED_INVOICE_RESPONSE}
    
    return {'type': 'text', 'text': f'Echo: {text}'}

def get_response_for_photo():
    return {'type': 'text', 'text': PHOTO_RESPONSE} 