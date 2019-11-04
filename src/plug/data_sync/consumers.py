import asyncio
import json
import os
import time
import uuid
from random import randrange

from django.core.cache import caches
from channels.consumer import AsyncConsumer
from django.conf import settings


class WsConsumer(AsyncConsumer):

    def __init__(self, *args, **kwargs):
        super(WsConsumer, self).__init__(*args, **kwargs)
        self.room = None
        self.socket_id = None
        self.sync_timestamp = None
        self.cache_ids = []

    async def websocket_connect(self, event):
        cycle_amount = self.scope["url_route"]["kwargs"]["cycles"]
        interval = self.scope["url_route"]["kwargs"]["interval"]
        self.socket_id = self.scope["url_route"]["kwargs"]["socket_id"]
        self.room = self.get_room(self.socket_id)
        self.sync_timestamp = caches["default"].get(self.socket_id)

        await self.channel_layer.group_add(
            self.room,
            self.channel_name
        )

        await self.send({
            "type": "websocket.accept"
        })

        for _ in (range(cycle_amount)):
            await asyncio.sleep(interval / 1000)

            await self.send({
                "type": "websocket.send",
                "text": self.generate_timestamp_data()
            })

        await self.channel_layer.group_send(
            self.room,
            {
                "type": "disconnect"
            }
        )

    async def disconnect(self, event):
        await self.send({
            "type": "websocket.close"
        })

    async def websocket_disconnect(self, event):
        await self.send({
            "type": "websocket.close"
        })

    @staticmethod
    def get_room(socket_id: int) -> str:
        return str(socket_id)

    def generate_timestamp_data(self) -> str:
        timestamp_since_sync = time.time() - self.sync_timestamp
        timestamp_data = f"{timestamp_since_sync} | {self.generate_random_number(1000000, 1000000000)}"
        file_identifier = uuid.uuid4()

        generated_data = {
            "file_identifier": str(file_identifier),
            "timestamp_data": timestamp_data
        }

        self.save_timestamp_data_to_file(generated_data)
        self.cache_ids.append(file_identifier)

        return json.dumps(generated_data)

    @staticmethod
    def generate_random_number(start_range: int, end_range: int) -> int:
        return randrange(start_range, end_range)

    @staticmethod
    def save_timestamp_data_to_file(data: dict) -> None:
        working_directory = settings.TIMESTAMPS_DIR
        file_identifier = data.get("file_identifier")
        timestamp_data = data.get("timestamp_data")

        with open(os.path.join(working_directory, f"{file_identifier}.txt"), "w+") as file:
            file.write(f"{timestamp_data}")
