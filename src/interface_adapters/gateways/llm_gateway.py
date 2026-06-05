class LlmGatewayInterface:
    def __init__(self, client):
        self.client = client

    async def send(self):
        pass
