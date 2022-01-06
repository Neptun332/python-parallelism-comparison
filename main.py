import concurrent
import threading

import requests

from AsyncioProcessingUnit import AsyncioProcessingUnit


def invoke_endpoint(url):
    response = requests.get(url=url)
    print(response)


def run_program2():
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(invoke_endpoint, ["http://127.0.0.1:5000//api/v1/do_something"])
        executor.shutdown(wait=True)


def run_program3():
    tread = threading.Thread(target=invoke_endpoint, args=("http://127.0.0.1:5000//api/v1/do_something",))
    tread.start()
    tread.join()


# async def fetch(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             print('#', response.status)
#
#
# async def run_program():
#     task1 = asyncio.create_task(fetch(r"http://127.0.0.1:5000//api/v1/do_something"))
#     print("aa")
#     await task1
#
#
# if __name__ == '__main__':
#     asyncio.run(run_program())


if __name__ == '__main__':
    asyncio_processing_unit = AsyncioProcessingUnit(duration=1000,
                                                    sending_schedule=[100, 20, 50, 30, 120, 50, 10, 80, 90, 10, 5, 30,
                                                                      40, 10, 100])
    asyncio_processing_unit.start()
