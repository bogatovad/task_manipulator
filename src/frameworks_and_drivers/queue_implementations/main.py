import asyncio

from src.frameworks_and_drivers.queue_implementations.consumer import run_consumer


def main() -> None:
    asyncio.run(run_consumer())


if __name__ == "__main__":
    main()
