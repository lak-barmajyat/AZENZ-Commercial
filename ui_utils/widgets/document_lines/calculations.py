"""Line and document total calculations for document lines."""

from __future__ import annotations

from dataclasses import dataclass

from .document_line import DocumentLine, LineType


@dataclass
class DocumentTotals:
    """Aggregated totals for all product/service lines in a document."""

    total_ht: float = 0.0
    total_discount: float = 0.0
    total_tva: float = 0.0
    total_ttc: float = 0.0
    line_count: int = 0
    product_line_count: int = 0
    total_quantity: float = 0.0

    def to_dict(self) -> dict[str, float | int]:
        return {
            "total_ht": self.total_ht,
            "total_discount": self.total_discount,
            "total_tva": self.total_tva,
            "total_ttc": self.total_ttc,
            "line_count": self.line_count,
            "product_line_count": self.product_line_count,
            "total_quantity": self.total_quantity,
        }


def is_calculable_line(line: DocumentLine) -> bool:
    return line.line_type in (LineType.PRODUCT, LineType.SERVICE)


def recalculate_line(line: DocumentLine) -> DocumentLine:
    """Recompute derived amounts on *line* (in place) and return it."""
    if not is_calculable_line(line):
        line.amount_ht = 0.0
        line.discount_amount = 0.0
        line.total_ht = 0.0
        line.tax_amount = 0.0
        line.total_ttc = 0.0
        return line

    qty = max(float(line.quantity or 0), 0.0)
    price = max(float(line.price_ht or 0), 0.0)
    disc = min(max(float(line.discount_percent or 0), 0.0), 100.0)
    vat = min(max(float(line.vat_percent or 0), 0.0), 100.0)

    amount_ht = qty * price
    discount_amount = amount_ht * disc / 100.0
    net_ht = amount_ht - discount_amount
    tax_amount = net_ht * vat / 100.0
    total_ttc = net_ht + tax_amount

    line.amount_ht = round(amount_ht, 6)
    line.discount_amount = round(discount_amount, 6)
    line.total_ht = round(net_ht, 6)
    line.tax_amount = round(tax_amount, 6)
    line.total_ttc = round(total_ttc, 6)
    return line


def recalculate_document_totals(lines: list[DocumentLine]) -> DocumentTotals:
    """Aggregate totals from a list of real (non-placeholder) lines."""
    totals = DocumentTotals(line_count=len(lines))

    for line in lines:
        if line.line_type in (LineType.PRODUCT, LineType.SERVICE):
            totals.product_line_count += 1
            totals.total_ht += line.total_ht
            totals.total_discount += line.discount_amount
            totals.total_tva += line.tax_amount
            totals.total_ttc += line.total_ttc
            totals.total_quantity += max(float(line.quantity or 0), 0.0)

    totals.total_ht = round(totals.total_ht, 2)
    totals.total_discount = round(totals.total_discount, 2)
    totals.total_tva = round(totals.total_tva, 2)
    totals.total_ttc = round(totals.total_ttc, 2)
    totals.total_quantity = round(totals.total_quantity, 4)
    return totals
