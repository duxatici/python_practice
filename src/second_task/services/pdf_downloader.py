import requests
import re

from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from requests import Response
from urllib.parse import urljoin
from datetime import date
from itertools import count
from collections import defaultdict

from exceptions import DownloadReportError


BASE_URL = "https://spimex.com"
REPORTS_ENDPOINT = "/markets/oil_products/trades/results?page=page-"


def get_pages(from_date: date) -> defaultdict[date, bytes]:
    pdf_urls = get_pdf_urls_by_date(from_date)
    pages: defaultdict[date, bytes] = defaultdict(bytes)
    for url in pdf_urls:
        cur_date = get_date_from_url(url)
        response = send_get_request(url)
        pages[cur_date] = response.content

    return pages


def get_all_reports(page_number: int = 1) -> list[str]:
    url = f"{BASE_URL}{REPORTS_ENDPOINT + str(page_number)}"
    response = send_get_request(url)
    result = get_report_urls(response)
    return result


def send_get_request(url: str) -> Response:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except RequestException as e:
        raise DownloadReportError(f"Не удалось скачать PDF: {e}") from e


def get_report_urls(response: Response) -> list[str]:
    soup = BeautifulSoup(response.text, "lxml")
    links = soup.select("a.pdf")

    urls = []
    for link in links:
        href = link.get("href")
        if isinstance(href, str):
            urls.append(urljoin(BASE_URL, href))

    return urls


def get_pdf_urls_by_date(from_date: date) -> list[str]:
    to_date = date.today()
    report_urls = []
    for page_number in count(1, 1):
        urls = get_all_reports(page_number)
        for url in urls:
            cur_date = get_date_from_url(url)
            if from_date <= cur_date <= to_date:
                report_urls.append(url)
            else:
                return report_urls
    return report_urls


def get_date_from_url(url: str) -> date:
    match: re.Match[str] | None = re.search(r"oil_(\d{8})", url)
    if match is not None:
        date_str = match.group(1)
        cur_date = date.strptime(date_str, "%Y%m%d")
        return cur_date
    else:
        raise TypeError(f"Значение даты не было найдено в url отчета: {url}")
