import slack_sdk
from slack_bolt import App as SlackApp
from slack_bolt.adapter.socket_mode import SocketModeHandler
from .base_bot import BaseBot
from responses import get_response_for_message

class SlackBot(BaseBot):
    def __init__(self, config):
        super().__init__(config)
        self.app = SlackApp(token=config.SLACK_BOT_TOKEN)
        self.client = slack_sdk.WebClient(token=config.SLACK_BOT_TOKEN)

    async def start(self):
        handler = SocketModeHandler(
            app=self.app,
            app_token=self.config.SLACK_APP_TOKEN
        )
        
        @self.app.event("message")
        async def handle_message(event, say):
            if event.get('subtype') is None:
                response = get_response_for_message(event['text'])
                await self.send_response(response, {'channel': event['channel']})

        handler.start()

    async def send_response(self, response, context):
        if isinstance(response, dict):
            text = response.get('text', '') or response.get('caption', '')
        else:
            text = response
        await self.client.chat_postMessage(
            channel=context['channel'],
            text=text
        ) 