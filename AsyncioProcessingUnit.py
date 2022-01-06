import asyncio
import time
from typing import List

import aiohttp

Tick = int


class AsyncioProcessingUnit:

    def __init__(self, duration: Tick, sending_schedule: List[int], inner_processing_time: float = 0.2,
                 url: str = "http://127.0.0.1:5000//api/v1/do_something"):
        self._validate(duration, sending_schedule)
        self.duration = duration
        self.iter_sending_schedule = iter(sending_schedule)
        self.current_schedule_value = next(self.iter_sending_schedule)
        self.sending_schedule = sending_schedule
        self.inner_processing_time = inner_processing_time
        self.url = url
        self.iter = 0
        self.tasks_control = []

    def start(self):
        asyncio.run(self.processing_loop())

    async def processing_loop(self):
        for i in range(self.duration):
            await self.repetitive_task()
            if self.should_send_event():
                self.run_sender()
            self.iter += 1

    async def repetitive_task(self):
        await asyncio.sleep(self.inner_processing_time)

    def should_send_event(self):
        if self.current_schedule_value and self.iter % self.current_schedule_value == 0:
            self.current_schedule_value = next(self.iter_sending_schedule, None)
            return True
        return False

    def run_sender(self):
        print("Created task to send data")
        task = asyncio.create_task(self.invoke_endpoint(self.url))
        task.add_done_callback(self.print_result)
        self.tasks_control.append(task)

    async def invoke_endpoint(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return response

    @staticmethod
    def print_result(response):
        print('#', response._result.status)

    @staticmethod
    def _validate(duration, sending_schedule):
        if type(duration) != int:
            raise TypeError("duration should be int value")
        if type(sending_schedule) != list:
            raise TypeError("duration should be List value")
        if sum(sending_schedule) > duration:
            raise ValueError("sum of sending_schedule cant be bigger than duration")
