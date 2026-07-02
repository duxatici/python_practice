import asyncio
import random
import aiohttp
import re

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import date
from itertools import count
from collections import defaultdict

from exceptions import DownloadReportError
from logger import logging

logger = logging.getLogger(__name__)


BASE_URL = "https://spimex.com"
REPORTS_ENDPOINT = "/markets/oil_products/trades/results?page=page-"
BXAJAXID = "&bxajaxid=d609bce6ada86eff0b6f7e49e6bae904"


async def get_pages(
    from_date: date, session: aiohttp.ClientSession
) -> defaultdict[date, bytes]:
    pdf_urls = await get_pdf_urls_by_date(from_date, session)

    semaphore = asyncio.Semaphore(2)

    async def fetch_pdf(url: str) -> tuple[date, bytes] | None:
        cur_date = get_date_from_url(url)
        if not cur_date:
            return None
        async with semaphore:
            response = await send_get_request(url, session)
            return cur_date, response

    tasks = [fetch_pdf(url) for url in pdf_urls]
    results = await asyncio.gather(*tasks)

    pages: defaultdict[date, bytes] = defaultdict(bytes)
    for result in results:
        if result:
            cur_date, content = result
            pages[cur_date] = content

    return pages


async def get_reports_by_page(
    page_number: int, session: aiohttp.ClientSession
) -> list[str]:
    url = f"{BASE_URL}{REPORTS_ENDPOINT + str(page_number)}{BXAJAXID}"
    response = await send_get_request(url, session)
    result = get_report_urls(response.decode("utf-8"))
    return result


async def send_get_request(url: str, session: aiohttp.ClientSession) -> bytes:
    attempt = 0
    while True:
        try:
            async with session.get(url, ssl=False) as response:
                response.raise_for_status()
                return await response.read()
        except (aiohttp.ClientResponseError, aiohttp.ClientError) as e:
            if attempt == 2:
                raise DownloadReportError(f"Не удалось скачать PDF: {e}") from e
            attempt += 1
            logger.warning(f"Делаем ретрай на {url}")
            await asyncio.sleep(random.randint(5, 10))


def get_report_urls(response: str) -> list[str]:
    soup = BeautifulSoup(response, "lxml")
    links = soup.select("a.pdf")

    urls = []
    for link in links:
        href = link.get("href")
        if isinstance(href, str):
            urls.append(urljoin(BASE_URL, href))

    return urls


async def get_pdf_urls_by_date(
    from_date: date, session: aiohttp.ClientSession
) -> list[str]:
    to_date = date.today()
    report_urls = []
    for page_number in count(1, 1):
        urls = await get_reports_by_page(page_number, session)
        if not urls:
            raise DownloadReportError(
                f"Получили пустую страницу без ссылок {page_number}"
            )
        for url in urls:
            cur_date = get_date_from_url(url)
            if not cur_date:
                continue
            if from_date <= cur_date <= to_date:
                report_urls.append(url)
            else:
                return report_urls
    return report_urls


def get_date_from_url(url: str) -> date | None:
    match: re.Match[str] | None = re.search(r"oil_(\d{8})", url)
    if match is not None:
        date_str = match.group(1)
        cur_date = date.strptime(date_str, "%Y%m%d")
        return cur_date
    else:
        logger.warning(f"Значение даты не было найдено в url отчета: {url}")
