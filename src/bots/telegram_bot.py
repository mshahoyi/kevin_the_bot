from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from pathlib import Path
from .base_bot import BaseBot
from responses import get_response_for_message, get_response_for_photo


class TelegramBot(BaseBot):
    def __init__(self, config):
        super().__init__(config)
        self.token = config.TELEGRAM_BOT_TOKEN
        self.app = Application.builder().token(self.token).build()
        # self.app.updater.drop_pending_updates = True
        self._setup_handlers()

    def _setup_handlers(self):
        self.app.add_handler(CommandHandler('start', self._start_command))
        self.app.add_handler(CommandHandler('help', self._help_command))
        self.app.add_handler(MessageHandler(filters.TEXT, self._handle_message))
        self.app.add_handler(MessageHandler(filters.PHOTO, self._handle_photo))
        self.app.add_error_handler(self._error)

    def start(self):
        # self.app.initialize()
        # self.app.start()
        self.app.run_polling(poll_interval=1)

    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Hello! I am your bot. Nice to meet you!')

    async def _help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('I can help you! Use /start to start the bot.')

    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_type = update.message.chat.type
        text = update.message.text
        print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
        
        response = get_response_for_message(text)
        await self.send_response(response, update)

    async def _handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        response = get_response_for_photo()
        await self.send_response(response, update)

    async def _error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'Update {update} caused error {context.error}')

    async def send_response(self, response, update):
        if isinstance(response, dict):
            if response.get('type') == 'document':
                with open(Path(response['file_path']), "rb") as pdf_file:
                    await update.message.reply_document(
                        pdf_file,
                        filename=response['filename'],
                        caption=response.get('caption'),
                        parse_mode='HTML'
                    )
            else:
                await update.message.reply_text(response['text'], parse_mode='HTML')
        else:
            await update.message.reply_text(response, parse_mode='HTML')

    async def stop(self):
        """Gracefully stop the bot and cleanup resources"""
        try:
            await self.app.stop()
            await self.app.shutdown()
        except Exception as e:
            print(f"Error while stopping Telegram bot: {e}") 