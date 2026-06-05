from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitMQSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="environments/rabbitmq.env",
        extra="ignore",
    )

    url: str = Field(
        default="amqp://guest:guest@rabbitmq:5672/",
        validation_alias="RABBITMQ_URL",
    )
    queue_name: str = Field(default="tasks", validation_alias="RABBITMQ_QUEUE_NAME")


rabbitmq_settings = RabbitMQSettings()
