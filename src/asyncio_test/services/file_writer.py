import csv
from datetime import date, datetime

from exceptions import InvalidRowError, TableFormatError


def write_csv(rows: list[list[str]], report_date: date, filename: str) -> None:
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        try:
            for row in rows:
                row_to_write = [
                    row[0],
                    row[1],
                    row[0][:4],
                    row[0][4:7],
                    row[2],
                    row[0][-1],
                    row[3],
                    row[4],
                    row[13],
                    report_date,
                    datetime.now(),
                    None,
                ]
                writer.writerow(row_to_write)
        except IndexError as e:
            raise TableFormatError("Формат таблицы неверный") from e
        except (TypeError, ValueError) as e:
            raise InvalidRowError(f"Неверное значение в строке: {row}") from e
