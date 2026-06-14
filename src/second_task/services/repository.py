from datetime import date, datetime

from models.spimex_trading_results import SpimexTradingResults
from exceptions import InvalidRowError, TableFormatError


def parse_metric_row(row: list[str], report_date: date) -> SpimexTradingResults:
    try:
        return SpimexTradingResults(
            exchange_product_id=row[0],
            exchange_product_name=row[1],
            oil_id=row[0][:4],
            delivery_basis_id=row[0][4:7],
            delivery_basis_name=row[2],
            delivery_type_id=row[0][-1],
            volume=row[3],
            total=row[4],
            count=row[13],
            date=report_date,
            created_on=datetime.now(),
            updated_on=None,
        )
    except IndexError as e:
        raise TableFormatError("Формат таблицы неверный") from e
    except ValueError as e:
        raise InvalidRowError(f"Неверное значение в строке: {row}") from e
