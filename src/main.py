import asyncio
import os
from dotenv import load_dotenv
from bots import TelegramBot, SlackBot, WhatsAppBot

class Config:
    def __init__(self):
        load_dotenv()
        self.TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        self.SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
        self.SLACK_APP_TOKEN = os.getenv('SLACK_APP_TOKEN')
        self.WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')

        if not self.TELEGRAM_BOT_TOKEN:
            raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables")

def main():
    try:
        print("Creating config...")
        config = Config()
        print("Config created successfully")
        
        print("Initializing Telegram bot...")
        telegram_bot = TelegramBot(config)
        print("Telegram bot initialized")
        
        try:
            print("Starting bot...")
            telegram_bot.start()
        except KeyboardInterrupt:
            print("Shutting down bots...")
            telegram_bot.stop()
        except Exception as e:
            print(f"Error during bot operation: {str(e)}")
            raise
    except Exception as e:
        print(f"Startup error: {str(e)}")
        raise

if __name__ == '__main__':
    main()
