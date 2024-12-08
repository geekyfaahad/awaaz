# import asyncio
# import platform
# import time
# import httpx
# import aiohttp
# import trio
# import asks
# import httptools
# from datetime import datetime

# # Try importing uvloop and set event loop policy if available
# try:
#     import uvloop
# except ImportError:
#     uvloop = None

# # If uvloop is available and the platform is not Windows, set the event loop policy
# if uvloop and platform.system() != "Windows":
#     asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# # URL to be requested
# url = "https://www.google.com/search?q=site:kashmirobserver.net+OR+site:thekashmiyat.co.uk+OR+site:kashmirnews.in+OR+site:kashmirdespatch.com+OR+site:kashmirlife.net+OR+site:risingkashmir.com+OR+site:greaterkashmir.com+OR+site:asiannewshub.com+OR+site:thekashmirmonitor.net+OR+site:kashmirreader.com+OR+site:kashmirtimes.com+OR+site:newsvibesofindia.com+OR+site:kashmirvision.in+News&sca_esv=75315e11642a04a4&tbs=qdr:h&tbm=nws"

# # Timing utility function to measure average and standard deviation
# async def measure_avg_and_std(func, *args, **kwargs):
#     times = []
#     for _ in range(5):  # Run the function 5 times for more reliable average and std
#         start_time = time.time()
#         if asyncio.iscoroutinefunction(func):  # Check if the function is async
#             result = await func(*args, **kwargs)  # Ensure we await async functions
#         else:
#             result = func(*args, **kwargs)  # Call sync function normally
#         end_time = time.time()
#         times.append((end_time - start_time) * 1000)  # Time in milliseconds
#     avg_time = sum(times) / len(times)
#     std_dev = (sum([(x - avg_time) ** 2 for x in times]) / len(times)) ** 0.5
#     return result, avg_time, std_dev

# # HTTPX + uvloop (synchronous)
# def fetch_httpx_uvloop_sync():
#     if uvloop:
#         asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())  # Ensure uvloop is set
#     with httpx.Client(http2=True, timeout=10.0) as client:
#         response = client.get(url)
#     return response

# # AIOHTTP + uvloop (asynchronous)
# async def fetch_aiohttp_uvloop():
#     if uvloop:
#         asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())  # Ensure uvloop is set
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return response

# # Trio + asks
# asks.init("trio")

# async def fetch_trio_asks():
#     response = await asks.get(url)
#     return response

# # Httptools (custom HTTP request handling) - synchronous
# def fetch_httptools():
#     parser = httptools.HttpRequestParser(None)
#     request = f"GET {url} HTTP/1.1\r\nHost: www.google.com\r\n\r\n"
#     parser.feed_data(request.encode())
#     return "Request sent using httptools"

# # Function to save results to XML-like format
# def save_results_to_xml(results, test_name):
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     xml_result = f"""
#     <{test_name}>
#         <timestamp>{timestamp}</timestamp>
#         <HTTPX_uvloop>
#             <status_code>{results['httpx']['status_code']}</status_code>
#             <avg_time>{results['httpx']['avg_time']}</avg_time>
#             <std_dev>{results['httpx']['std_dev']}</std_dev>
#         </HTTPX_uvloop>
#         <AIOHTTP_uvloop>
#             <status_code>{results['aiohttp']['status_code']}</status_code>
#             <avg_time>{results['aiohttp']['avg_time']}</avg_time>
#             <std_dev>{results['aiohttp']['std_dev']}</std_dev>
#         </AIOHTTP_uvloop>
#         <Trio_asks>
#             <status_code>{results['trio']['status_code']}</status_code>
#             <avg_time>{results['trio']['avg_time']}</avg_time>
#             <std_dev>{results['trio']['std_dev']}</std_dev>
#         </Trio_asks>
#         <Httptools>
#             <response>{results['httptools']['response']}</response>
#             <time_taken>{results['httptools']['time_taken']}</time_taken>
#         </Httptools>
#     </{test_name}>
#     """
#     with open("test_results.xml", "a") as f:
#         f.write(xml_result)

# # Main async function to run the tests and measure performance
# async def run_tests():
#     test_name = f"Test_{datetime.now().strftime('%Y%m%d%H%M%S')}"
#     print("Measuring performance of different HTTP libraries...\n")
    
#     # HTTPX + uvloop
#     response_httpx_uvloop, avg_time_httpx_uvloop, std_dev_httpx_uvloop = await measure_avg_and_std(fetch_httpx_uvloop_sync)
#     print(f"HTTPX + uvloop response status code: {response_httpx_uvloop.status_code}")
#     print(f"Time taken by HTTPX + uvloop: {avg_time_httpx_uvloop:.2f} ms (Std Dev: {std_dev_httpx_uvloop:.2f} ms)\n")
    
#     # AIOHTTP + uvloop
#     response_aiohttp_uvloop, avg_time_aiohttp_uvloop, std_dev_aiohttp_uvloop = await measure_avg_and_std(fetch_aiohttp_uvloop)
#     print(f"AIOHTTP + uvloop response status code: {response_aiohttp_uvloop.status}")
#     print(f"Time taken by AIOHTTP + uvloop: {avg_time_aiohttp_uvloop:.2f} ms (Std Dev: {std_dev_aiohttp_uvloop:.2f} ms)\n")

#     # Trio + asks
#     response_trio_asks, avg_time_trio_asks, std_dev_trio_asks = await measure_avg_and_std(fetch_trio_asks)
#     print(f"Trio + asks response status code: {response_trio_asks.status_code}")
#     print(f"Time taken by Trio + asks: {avg_time_trio_asks:.2f} ms (Std Dev: {std_dev_trio_asks:.2f} ms)\n")
    
#     # Httptools (this is synchronous)
#     response_httptools = fetch_httptools()
#     print(f"Httptools response: {response_httptools}")
#     # Since Httptools is synchronous, we manually measure the time here
#     elapsed_time_httptools = 0  # No need to measure time for sync call (it's a small operation)
#     print(f"Time taken by Httptools: {elapsed_time_httptools:.2f} ms\n")
    
#     # Collect results into a dictionary for XML generation
#     results = {
#         "httpx": {
#             "status_code": response_httpx_uvloop.status_code,
#             "avg_time": avg_time_httpx_uvloop,
#             "std_dev": std_dev_httpx_uvloop
#         },
#         "aiohttp": {
#             "status_code": response_aiohttp_uvloop.status,
#             "avg_time": avg_time_aiohttp_uvloop,
#             "std_dev": std_dev_aiohttp_uvloop
#         },
#         "trio": {
#             "status_code": response_trio_asks.status_code,
#             "avg_time": avg_time_trio_asks,
#             "std_dev": std_dev_trio_asks
#         },
#         "httptools": {
#             "response": response_httptools,
#             "time_taken": elapsed_time_httptools
#         }
#     }
    
#     # Save results to an XML-like format
#     save_results_to_xml(results, test_name)

# # Function to continuously run the tests in a loop
# async def continuous_test_loop():
#     while True:
#         await run_tests()
#         print("\nTest completed. Waiting before next test...\n")
#         await asyncio.sleep(1)  # Wait 60 seconds before the next test

# if __name__ == "__main__":
#     # Run the continuous test loop
#     asyncio.run(continuous_test_loop())

import asyncio, aiohttp, concurrent.futures
from datetime import datetime
import uvloop


class UVloopTester():
    def __init__(self):
        self.timeout = 20
        self.threads = 500
        self.totalTime = 0
        self.totalRequests = 0

    @staticmethod
    def timestamp():
        return f'[{datetime.now().strftime("%H:%M:%S")}]'

    async def getCheck(self):
        async with aiohttp.ClientSession() as session:
            response = await session.get('https://www.google.com', timeout=self.timeout)
            response.close()
        await session.close()
        return True

    async def testRun(self, id):
        now = datetime.now()
        try:
            if await self.getCheck():
                elapsed = (datetime.now() - now).total_seconds()
                print(f'{self.timestamp()} Request {id} TTC: {elapsed}')
                self.totalTime += elapsed
                self.totalRequests += 1
        except concurrent.futures._base.TimeoutError: print(f'{self.timestamp()} Request {id} timed out')

    async def main(self):
        await asyncio.gather(*[asyncio.ensure_future(self.testRun(x)) for x in range(self.threads)])

    def start(self):
        # comment these lines to toggle
        uvloop.install()
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

        loop = asyncio.get_event_loop()
        now = datetime.now()
        loop.run_until_complete(self.main())
        elapsed = (datetime.now() - now).total_seconds()
        print(f'{self.timestamp()} Main TTC: {elapsed}')
        print()
        print(f'{self.timestamp()} Average TTC per Request: {self.totalTime / self.totalRequests}')
        if len(asyncio.Task.all_tasks()) > 0:
            for task in asyncio.Task.all_tasks(): task.cancel()
            try: loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks()))
            except asyncio.CancelledError: pass
        loop.close()


test = UVloopTester()
test.start()