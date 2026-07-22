import pdfplumber

from datetime import date
from io import BytesIO
from collections import defaultdict

from logger import logging


logger = logging.getLogger(__name__)


def get_tables(pages: dict[date, bytes]) -> dict[date, list[list[str]]]:
    tables: defaultdict[date, list[list[str]]] = defaultdict(list)
    for report_date, page in pages.items():
        with pdfplumber.open(BytesIO(page)) as pdf:
            for page_pdf in pdf.pages:
                # «Единица измерения: Метрическая тонна» - нужная таблица, в отчетах она идет последней по порядку
                # отсекаем 2 строки с заголовками
                try:
                    table = page_pdf.extract_tables()[-1][2:]
                except IndexError as e:
                    logger.warning(
                        f"Не нашли таблицу на странице {page_pdf}. Ошибка: {e}"
                    )
                    continue
                if table:
                    for line in table:
                        try:
                            # отсекаем строки без сделок ("Количество договоров" != '-')
                            # 0 тоже пройдет, но на практике значение или '-' или число больше 0
                            if line[13] != "-":
                                cleaned = [item for item in line if item is not None]
                                tables[report_date].append(cleaned)
                        except IndexError as e:
                            logger.warning(
                                f"Формат таблицы неверный: {line}. Ошибка: {e}"
                            )
                            continue
    return tables
