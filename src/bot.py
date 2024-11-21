from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables")


log_response = """<a href="https://qbo.intuit.com/app/creditcardexpense?&txnId=144">Expense</a> added to QuickBooks

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

invoice_response = """Invoice details to ABC Company
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

updated_invoice_response = """Updated invoice details to ABC Company
Customer email: purchasing@abc.com
Invoice date: Today
Due date: in a month (12/20/2024)

Item 1: Large TV Sets
    Quantity: 100
    Amount: USD 60000

Item 2: Setup Fees
    Quantity: 1
    Amount: USD 1400
    Service date: Today (11/20/2024)

Total: USD 61400

Message on invoice: It is a pleasure doing business with you!

Type y to send, n to abort, others to modify"""

pnl_response = """Income
$10,200.77

COGS
$405.00

GROSS PROFIT
$9,795.77

Expenses
$5,237.31

NET OP. INCOME
$4,558.46

Other Expenses
$2,916.00

NET OTHER INCOME           
-2,916.00

NET INCOME
$1,642.46"""

photo_response = """<a href="https://qbo.intuit.com/app/creditcardexpense?&txnId=144">Expense</a> details

Payee: IKEA
Payment account: Cash
Payment date: Today
Payment method: Cash

Item 1:
    Category: Office supplies
    Description: Brown chair
    Quantity: 1
    Amount: USD 255

Item 2:
    Category: Office supplies
    Description: Computer Desktop Table
    Quantity: 1
    Amount: USD 265

Total: USD 520

Type y to save, n to abort, others to modify"""

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command"""
    await update.message.reply_text('Hello! I am your bot. Nice to meet you!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /help command"""
    await update.message.reply_text('I can help you! Use /start to start the bot.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for text messages"""
    message_type = update.message.chat.type
    text = update.message.text

    # Log message
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')


    if "pnl" in text.lower():
        with open(Path('ProfitandLoss.pdf'), "rb") as pdf_file:
            await update.message.reply_document(
                pdf_file, 
                filename="Profit and Loss.pdf",
                caption=pnl_response,
                parse_mode='HTML'
            )
        return
    
    if "landscaping" in text.lower():
        with open(Path('Sales by Landscaping Summary.pdf'), "rb") as pdf_file:
            await update.message.reply_document(pdf_file, filename="Sales by Landscaping Summary.pdf")
        return
        
    if "log" in text.lower(): 
        response = log_response
        await update.message.reply_text(response, parse_mode='HTML')
        return
    
    if "invoice" in text.lower(): response = invoice_response
    elif "1400" in text.lower(): response = updated_invoice_response
    else: response = f'Echo: {text}'
        
    await update.message.reply_text(response)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for photo messages"""
    await update.message.reply_text(photo_response, parse_mode='HTML')

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Error handler"""
    print(f'Update {update} caused error {context.error}')

def main():
    # Create application
    app = Application.builder().token(TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # Add message handlers
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Add error handler
    app.add_error_handler(error)

    # Start polling
    print('Starting bot...')
    app.run_polling(poll_interval=1)

if __name__ == '__main__':
    main() 
