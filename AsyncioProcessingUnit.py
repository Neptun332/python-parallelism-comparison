import asyncio
import time
from typing import List

import aiohttp


class AsyncioProcessingUnit:

    def __init__(self, duration: int, sending_schedule: List[int], inner_processing_time: float = 0.2,
                 url: str = "http://127.0.0.1:5000//api/v1/do_something"):
        self._validate(duration, sending_schedule)
        self.duration = duration
        self.iter_sending_schedule = iter(sending_schedule)
        self.current_schedule_value = next(self.iter_sending_schedule)
        self.sending_schedule = sending_schedule
        self.inner_processing_time = inner_processing_time
        self.url = url
        self.iter = 0
        self.last_task = None

    def start(self):
        for i in range(self.duration):
            self.repetitive_task()
            if self.should_send_event():
                print("a")
                asyncio.run(self.run_sender())
            self.iter += 1

    def repetitive_task(self):
        time.sleep(self.inner_processing_time)

    def should_send_event(self):
        if self.iter % self.current_schedule_value == 0:
            self.current_schedule_value = next(self.iter_sending_schedule, self.sending_schedule[-1])
            return True
        return False

    async def run_sender(self):
        try:
            if self.last_task:
                await self.last_task
            self.last_task = asyncio.create_task(self.invoke_endpoint(self.url))
        except Exception as e:
            print(e)

    async def invoke_endpoint(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                print('#', response.status)

    def _validate(self, duration, sending_schedule):
        if type(duration) != int:
            raise TypeError("duration should be int value")
        if type(sending_schedule) != list:
            raise TypeError("duration should be List value")
        if sum(sending_schedule) > duration:
            raise ValueError("sum of sending_schedule cant be bigger than duration")
