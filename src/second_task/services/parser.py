import pdfplumber

from datetime import date
from io import BytesIO
from collections import defaultdict

from exceptions import TableFormatError


def get_tables(pages: defaultdict[date, bytes]) -> dict[date, list[list[str]]]:
    tables: defaultdict[date, list[list[str]]] = defaultdict(list)
    for report_date, page in pages.items():
        with pdfplumber.open(BytesIO(page)) as pdf:
            for i, page in enumerate(pdf.pages):
                # «Единица измерения: Метрическая тонна» - нужная таблица, в отчетах она идет последней по порядку
                # отсекаем 2 строки с заголовками
                table = page.extract_tables()[-1][2:]
                if table:
                    for line in table:
                        try:
                            # отсекаем строки без сделок ("Количество договоров" != '-')
                            # 0 тоже пройдет, но на практике значение или '-' или число больше 0
                            if line[13] != "-":
                                cleaned = [item for item in line if item is not None]
                                tables[report_date].append(cleaned)
                        except IndexError as e:
                            raise TableFormatError(
                                f"Формат таблицы неверный: {line}"
                            ) from e
    return tables
