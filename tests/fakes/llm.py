from src.interface_adapters.gateways.llm_gateway import LlmGatewayInterface


class FakeLlmGateway(LlmGatewayInterface):
    def __init__(
        self, response: dict | None = None, error: Exception | None = None
    ) -> None:
        self.response = response or {"content": "ok"}
        self.error = error
        self.calls: list[str] = []

    async def send(self, prompt: str) -> dict:
        self.calls.append(prompt)
        if self.error is not None:
            raise self.error
        return self.response
