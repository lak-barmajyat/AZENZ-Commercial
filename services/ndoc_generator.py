
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



def get_next_document_code(prefix: str, counter: int) -> str:
    settings = QSettings("YourCompany", "YourApp")

    pattern = settings.value(
        "documents/code_pattern",
        "{prefix}{number:03}"  # default: FA001
    )

    today = datetime.now()

    return pattern.format(
        prefix=prefix,
        number=counter,
        YYYY=today.strftime("%Y"),
        YY=today.strftime("%y"),
        MM=today.strftime("%m"),
        DD=today.strftime("%d"),
    )

@with_cursor
def reset_document_counter(code_type: str = None, year: int = None, cursor=None):
    """
    Reset counter for:
    - specific type (FA, DV...)
    - or all types if code_type=None
    - optional specific year (default: current year)
    """

    target_year = year or datetime.now().year

    if code_type:
        # جلب id_type_document
        type_obj = cursor.execute(
            select(RefTypeDocument).where(
                RefTypeDocument.code_type == code_type
            )
        ).scalar_one_or_none()

        if not type_obj:
            raise ValueError(f"Type document '{code_type}' not found")

        stmt = (
            update(Counter)
            .where(
                Counter.categorie == "DOCUMENT",
                Counter.code == code_type,
                Counter.annee == target_year,
            )
            .values(valeur_courante=0)
        )
    else:
        # Reset all types
        stmt = (
            update(Counter)
            .where(Counter.annee == target_year)
            .values(valeur_courante=0)
        )

    cursor.execute(stmt)
