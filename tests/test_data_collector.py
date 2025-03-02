import pytest

from hansard_data_collector import PageCollector

@pytest.mark.asyncio
async def test_parse_page():
    with open('tests/fixtures/2020-01-09-CommonsChamber.html', 'r', encoding='utf-8') as file:
        mock_html = file.read()

    page_collector = PageCollector()
    parsed_data = await page_collector.parse_page(mock_html, "2022-01-01")

    assert parsed_data['date'] == "2022-01-01"
    assert 'theme' in parsed_data
    assert 'debates' in parsed_data