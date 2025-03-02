from asyncio import sleep
from typing import List

import asyncio

import aiohttp
from bs4 import BeautifulSoup


class PageCollector:
    results = []

    async def download_pages(self, page_queries: List[dict]):
        """
        :param page_queries:
        :return:
        """
        async with aiohttp.ClientSession() as session:
            tasks = []
            for query in page_queries:
                tasks.append(self.fetch_redirected_page(query, session))
            await asyncio.gather(*tasks, return_exceptions=False, )
            return self.results

    async def fetch_redirected_page(self, page_query, session: aiohttp.ClientSession):
        """Follow the redirect and return the final page's HTML."""
        await sleep(0.1)
        async with session.get(page_query.get('url'), ssl=False, allow_redirects=True) as response:
            if response.status != 200:
                return
            text_content = await response.text()
            parsed_content = await self.parse_page(text_content, page_query.get('date_str'))
            self.results.append(parsed_content)

    async def parse_page(self, html, date_str):
        """Extract relevant information from the page."""
        soup = BeautifulSoup(html, 'html.parser')
        # Extract debates
        debates = []
        overarching_theme = soup.select_one('.primary-content .child-debate-list .child-debate .child-debate-list .child-debate h2').text
        for i, child_debate in enumerate(soup.select('.primary-content .child-debate-list .child-debate .child-debate-list .child-debate .child-debate-list .child-debate')):
            theme_text = child_debate.select_one('h2').text
            debates.append({
                'overarching_theme': overarching_theme,
                'theme': theme_text,
                'date': date_str,
                'debate_items': []
            })
            child_html = BeautifulSoup(str(child_debate), 'html.parser')
            for item in child_html.select('.contribution'):
                name = item.select_one('.contribution .header .primary-text')
                name_detail = item.select_one('.attributed-to-details .secondary-text')
                speech_content = item.select('.debate-item .content p')
                if hasattr(item, 'attrs'):
                    contribution_id = item.attrs.get('id', 'unknown')
                else:
                    contribution_id = None

                debates[i]['debate_items'].append({
                    'name': name.get_text(strip=True) if name else "Unknown",
                    'name_detail': name_detail.get_text(strip=True) if name_detail else "Unknown",
                    'contribution_id': contribution_id,
                    'speech': '\n'.join(p.get_text(strip=True) for p in speech_content)
                })

        return debates
