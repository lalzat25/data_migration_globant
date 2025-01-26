import csv
import logging
from sqlalchemy.orm import Session
from io import StringIO

from datetime import datetime
import csv
from io import StringIO
from sqlalchemy.orm import Session

logging.basicConfig(
    filename="failed_transactions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def process_csv(file, model, session: Session, batch_size: int = 1000):
    content = await file.read()
    content = content.decode("utf-8")
    csv_data = StringIO(content)
    csv_reader = csv.reader(csv_data)

    records = []
    total_records = 0

    for index, row in enumerate(csv_reader):
        if len(row) != len(model.__table__.columns.keys()):
            logger.error(f"Row {index + 1} is invalid. Expected {len(model.__table__.columns)} columns, got {len(row)}")
            continue
        
        is_datetime, message = validate_row_types(row, model)
        if not is_datetime:
            logger.error(message)
            continue

        try:
            record = model(**{list(model.__table__.columns.keys())[i]: row[i] for i in range(len(model.__table__.columns))})
            records.append(record)

            if len(records) >= batch_size:
                session.add_all(records)
                session.commit()
                total_records += len(records)
                records = []  
        except Exception as e:
            logger.error(f"Error processing row {index + 1}: {str(e)}")

    if records:
        try:
            session.add_all(records)
            session.commit()
            total_records += len(records)
        except Exception as e:
            logger.error(f"Error during final commit: {str(e)}")

    return total_records

def validate_row_types(row, model):
    """
    Valida si los tipos de los valores en una fila coinciden con los tipos esperados en el modelo.

    :param row: Lista de valores de la fila a validar.
    :param model: Modelo SQLAlchemy con las definiciones de columnas.
    :return: True si todos los valores son válidos, False si algún valor no es del tipo esperado.
    """
    columns = model.__table__.columns  # Obtiene las columnas del modelo
    for i, (column_name, column) in enumerate(columns.items()):
        if str(column.type) == "DATETIME":
            try:
                datetime.strptime(row[i], "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                return False, f"The column '{column_name}' expects a {str(column.type)}, but the value '{row[i]}' is invalid. Row: {row}"
        elif str(column.type) == "INTEGER":
            try:
                int(row[i])
            except ValueError:
                return False, f"The column '{column_name}' expects a {str(column.type)}, but the value '{row[i]}' is invalid. Row: {row}"
    return True, "All row types are valid."
