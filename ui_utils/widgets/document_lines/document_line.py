"""Document line data structure for :class:`DocumentLinesWidget`."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4


class LineType(str, Enum):
    """Supported document line categories."""

    PRODUCT = "product"
    TEXT = "text"
    SERVICE = "service"
    SEPARATOR = "separator"


@dataclass
class DocumentLine:
    """Generic, extensible representation of one editable document line.

    Numeric totals are maintained by the widget's calculation layer. Callers
    may store ERP-specific data in ``metadata`` without changing the core
    structure.
    """

    line_type: LineType = LineType.PRODUCT
    line_id: str = field(default_factory=lambda: str(uuid4()))

    # Product / service identifiers
    article_id: int | None = None
    reference: str = ""
    designation: str = ""
    description: str = ""

    # Quantities & pricing
    quantity: float = 1.0
    unit: str = "Unit"
    unit_id: int | None = None
    price_ht: float = 0.0
    discount_percent: float = 0.0
    vat_percent: float = 0.0
    vat_id: int | None = None

    # Computed amounts (updated by the widget)
    amount_ht: float = 0.0
    discount_amount: float = 0.0
    total_ht: float = 0.0
    tax_amount: float = 0.0
    total_ttc: float = 0.0

    # Extensibility
    metadata: dict[str, Any] = field(default_factory=dict)

    def clone(self) -> DocumentLine:
        """Return a deep copy with a fresh ``line_id``."""
        copy = deepcopy(self)
        copy.line_id = str(uuid4())
        return copy

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dictionary suitable for persistence."""
        return {
            "line_id": self.line_id,
            "line_type": self.line_type.value,
            "article_id": self.article_id,
            "reference": self.reference,
            "designation": self.designation,
            "description": self.description,
            "quantity": self.quantity,
            "unit": self.unit,
            "unit_id": self.unit_id,
            "price_ht": self.price_ht,
            "discount_percent": self.discount_percent,
            "vat_percent": self.vat_percent,
            "vat_id": self.vat_id,
            "amount_ht": self.amount_ht,
            "discount_amount": self.discount_amount,
            "total_ht": self.total_ht,
            "tax_amount": self.tax_amount,
            "total_ttc": self.total_ttc,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DocumentLine:
        """Build a line from a dictionary (e.g. database row or API payload)."""
        raw_type = data.get("line_type", data.get("type_ligne", LineType.PRODUCT.value))
        if isinstance(raw_type, LineType):
            line_type = raw_type
        elif isinstance(raw_type, int):
            line_type = {
                1: LineType.TEXT,
                2: LineType.SERVICE,
                3: LineType.SEPARATOR,
            }.get(raw_type, LineType.PRODUCT)
        else:
            line_type = LineType(str(raw_type))

        metadata = data.get("metadata")
        if metadata is None:
            metadata = {
                k: v
                for k, v in data.items()
                if k
                not in {
                    "line_id",
                    "line_type",
                    "article_id",
                    "reference",
                    "designation",
                    "description",
                    "quantity",
                    "unit",
                    "unit_id",
                    "price_ht",
                    "discount_percent",
                    "vat_percent",
                    "vat_id",
                    "amount_ht",
                    "discount_amount",
                    "total_ht",
                    "tax_amount",
                    "total_ttc",
                    "metadata",
                }
            }

        return cls(
            line_type=line_type,
            line_id=str(data.get("line_id") or data.get("id") or uuid4()),
            article_id=data.get("article_id"),
            reference=str(data.get("reference") or data.get("reference_article") or ""),
            designation=str(data.get("designation") or ""),
            description=str(data.get("description") or data.get("notes") or ""),
            quantity=float(data.get("quantity") or data.get("quantite") or 0),
            unit=str(data.get("unit") or data.get("nom_unite") or "Unit"),
            unit_id=data.get("unit_id"),
            price_ht=float(data.get("price_ht") or data.get("prix_unitaire_ht") or 0),
            discount_percent=float(data.get("discount_percent") or data.get("remise_percentage") or 0),
            vat_percent=float(data.get("vat_percent") or data.get("tva_percentage") or 0),
            vat_id=data.get("vat_id"),
            amount_ht=float(data.get("amount_ht") or data.get("montant_ht") or 0),
            discount_amount=float(data.get("discount_amount") or data.get("montant_remise") or 0),
            total_ht=float(data.get("total_ht") or data.get("montant_net_ht") or 0),
            tax_amount=float(data.get("tax_amount") or data.get("montant_tva") or 0),
            total_ttc=float(data.get("total_ttc") or data.get("montant_ttc") or 0),
            metadata=dict(metadata) if isinstance(metadata, dict) else {},
        )

    @classmethod
    def product(
        cls,
        *,
        reference: str = "",
        designation: str = "",
        description: str = "",
        quantity: float = 1.0,
        unit: str = "Unit",
        price_ht: float = 0.0,
        discount_percent: float = 0.0,
        vat_percent: float = 0.0,
        article_id: int | None = None,
        **extra: Any,
    ) -> DocumentLine:
        """Factory for a standard product line."""
        metadata = extra.pop("metadata", {})
        line = cls(
            line_type=LineType.PRODUCT,
            reference=reference,
            designation=designation,
            description=description,
            quantity=quantity,
            unit=unit,
            price_ht=price_ht,
            discount_percent=discount_percent,
            vat_percent=vat_percent,
            article_id=article_id,
            metadata=metadata,
        )
        for key, value in extra.items():
            if hasattr(line, key):
                setattr(line, key, value)
            else:
                line.metadata[key] = value
        return line

    @classmethod
    def text(cls, text: str = "") -> DocumentLine:
        """Factory for a free-text / comment line."""
        return cls(
            line_type=LineType.TEXT,
            description=text,
            quantity=0.0,
            price_ht=0.0,
        )
