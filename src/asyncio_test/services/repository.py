from datetime import date, datetime

from models.spimex_trading_results import SpimexTradingResults
from exceptions import InvalidRowError, TableFormatError
from models.database import Session


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


def copy_to_db(filename: str) -> None:
    with Session() as session:
        raw_conn = session.connection().connection
        try:
            with open(filename, "r") as f:
                raw_conn.cursor().copy_expert(
                    """
                        COPY spimex_trading_results (
                            exchange_product_id,
                            exchange_product_name,
                            oil_id,
                            delivery_basis_id,
                            delivery_basis_name,
                            delivery_type_id,
                            volume,
                            total,
                            count,
                            date,
                            created_on,
                            updated_on
                        ) FROM STDIN WITH CSV
                        """,
                    f,
                )
                session.commit()
        finally:
            raw_conn.close()
