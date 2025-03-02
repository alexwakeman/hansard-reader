from datetime import datetime, timedelta

import asyncio

from hansard_data_collector import PageCollector

BASE_URL = "https://hansard.parliament.uk/html/commons"
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2022, 1, 5)

def chunk_list(lst, size=100):
    return [lst[i:i + size] for i in range(0, len(lst), size)]

async def main():
    current_date = START_DATE
    page_collector = PageCollector()
    page_queries = []
    while current_date <= END_DATE:
        date_str = current_date.strftime('%Y-%m-%d')
        url = f"{BASE_URL}/{date_str}/CommonsChamber"
        page_queries.append(dict(url=url, date_str=date_str))
        current_date += timedelta(days=1)
    chunked_queries = chunk_list(page_queries)
    for chunk in chunked_queries:
        results = await page_collector.download_pages(chunk)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    tasks = [
        loop.create_task(main()),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()