import datetime
from datetime import date

from bs4 import BeautifulSoup

# TODO:
# если повятся другие типы отчетов
# заменить извелечение на regex
REPORT_DATE_PREFIX = "oil_xls_"
# TODO:
# если повятся другие фильтры
# сделать tuple фильтров и вынести в объявление функции
REPORT_PATH = "/upload/reports/oil_xls/oil_xls_"
LINK_CLASS_CSS = "accordeon-inner__item-title link xls"


# TODO:
# разбить на функции по каждой ответственности
def parse_page_links(
    html: str,
    start_date: date,
    end_date: date,
    base_url: str = "https://spimex.com",
    file_extension: str = "xls",
):
    """
    Парсит ссылки на бюллетени с одной страницы:
    ```html
    <a class="accordeon-inner__item-title link xls" href="/upload/reports/oil_xls/oil_xls_20240101_test.xls">link1</a>
    ```
    """
    results = []
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all(
        "a",
        class_=LINK_CLASS_CSS,
    )

    for link in links:
        href = link.get("href")
        if not href:
            continue

        href = href.split("?")[0]
        has_valid_path = REPORT_PATH in href
        has_valid_extension = href.endswith(f".{file_extension}")
        if not has_valid_path or not has_valid_extension:
            continue

        try:
            date_str = href.split(REPORT_DATE_PREFIX)[1][:8]
            report_date = datetime.datetime.strptime(date_str, "%Y%m%d").date()
            if start_date <= report_date <= end_date:
                url = href if href.startswith("http") else f"{base_url}{href}"
                results.append((url, report_date))
            else:
                # TODO: перейти с print на logger
                print(f"Ссылка {href} вне диапазона дат")
        except ValueError as e:
            # TODO: перейти с print на logger
            print(f"Не удалось извлечь дату из ссылки {href}: {e}")

    return results
