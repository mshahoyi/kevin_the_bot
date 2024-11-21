class BaseBot:
    def __init__(self, config):
        self.config = config
        
    async def process_message(self, message):
        # Common message processing logic
        pass

    async def send_response(self, response, context):
        # To be implemented by specific bot classes
        raise NotImplementedError
        
    async def start(self):
        # To be implemented by specific bot classes
        raise NotImplementedError 