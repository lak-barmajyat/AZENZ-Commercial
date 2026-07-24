from datetime import datetime
from PyQt5.QtCore import QSettings
from datetime import datetime
from sqlalchemy import select, update
from services.sql.db_connection import with_cursor
import string

@with_cursor()
def generate_document_number(id_type: str, cursor=None) -> str:
    query = f"""
        SELECT dernier_numero
        FROM p_numerotation_documents
        WHERE type_document_id = {id_type}
    """
    cursor.execute(query)
    result = cursor.fetchone()
    result = result[0].reverse()

    new_number = ""

    for c in result:
        if c.isdigit():
            new_number.append(c)
            result.remove(c)
        else:
            break
    new_number.reverse()
    new_number = int("".join(new_number)) + 1
    
    return f"{''.join(result)}{new_number:04d}"

ALLOWED_FIELDS = {"prefix", "YYYY", "YY", "MM", "DD", "number"}


def validate_code_pattern(pattern: str) -> tuple[bool, str]:
    if not pattern or not pattern.strip():
        return False, "Pattern is empty"

    formatter = string.Formatter()

    try:
        fields = []
        for literal_text, field_name, format_spec, conversion in formatter.parse(pattern):
            if field_name is None:
                continue

            fields.append(field_name)

            if field_name not in ALLOWED_FIELDS:
                return False, f"Unknown field: {field_name}"

            if conversion is not None:
                return False, "Conversions are not allowed"

            if field_name == "number":
                if format_spec and not format_spec.isdigit():
                    return False, "Number format must be like {number:03}"

            elif format_spec:
                return False, f"{field_name} cannot have format"

        if "prefix" not in fields:
            return False, "Pattern must contain {prefix}"

        if "number" not in fields:
            return False, "Pattern must contain {number}"

        return True, "Pattern is valid"

    except ValueError as e:
        return False, str(e)


def get_next_document_code(document_type_id, cursor) -> str:
    settings = QSettings("YourCompany", "YourApp")

    pattern = settings.value(
        "documents/code_pattern",
        "{prefix}{number:03}"  # default: FA001
    )

    cursor.execute(
        """
        SELECT prefixe, dernier_numero
        FROM P_numerotation_documents
        WHERE type_document_id = %s
        FOR UPDATE
        """,
        (document_type_id,)
    )

    row = cursor.fetchone()

    if not row:
        raise ValueError(f"No numerotation found for document_type_id={document_type_id}")

    prefixe = row["prefixe"] if isinstance(row, dict) else row[0]
    dernier_numero = row["dernier_numero"] if isinstance(row, dict) else row[1]

    next_number = dernier_numero + 1

    cursor.execute(
        """
        UPDATE P_numerotation_documents
        SET dernier_numero = %s
        WHERE type_document_id = %s
        """,
        (next_number, document_type_id)
    )

    today = datetime.now()

    return pattern.format(
        prefix=prefixe,
        number=next_number,
        YYYY=today.strftime("%Y"),
        YY=today.strftime("%y"),
        MM=today.strftime("%m"),
        DD=today.strftime("%d"),
    )
