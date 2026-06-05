class TaskQueueConsumerInterface:
    def __init__(self, url: str, queue_name: str) -> None:
        self.url = url
        self.queue_name = queue_name

    def run(self):
        pass
