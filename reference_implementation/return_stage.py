"""Return-lifecycle stage classifier (reference implementation, synthetic).

An order is followed through the post-sale chain using ONE key - the delivery
number - that exists in the ERP, in the RMA registry and in the customer-service
system. This module shows how the stage of a return is derived from the joined facts.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional

# credit-note types as they come from the ERP (A/B/C codes are normalized on load)
CREDIT_NOTE = {"A": "RETURN", "B": "VIRTUAL", "C": "IN_TRANSIT"}


@dataclass
class Delivery:
    delivery_id: str
    credit_note_code: Optional[str] = None   # A / B / C, None if no credit note exists
    rma_received_on: Optional[date] = None   # physical receipt registered by the warehouse
    cancelled_before_shipping: bool = False
    carrier_claim_open: bool = False


def stage(d: Delivery) -> str:
    cn = CREDIT_NOTE.get(d.credit_note_code or "", None)
    if d.cancelled_before_shipping:
        return "Cancelled before shipping"
    if cn == "VIRTUAL" and not d.rma_received_on:
        return "Virtual credit (no physical return expected)"
    if cn == "IN_TRANSIT":
        return "Returning - in transit"
    if d.rma_received_on and cn == "RETURN":
        return "Closed - received and credited"
    if d.rma_received_on and cn is None:
        return "Received - credit pending"
    if cn == "RETURN" and not d.rma_received_on:
        return "Credited - physical receipt unconfirmed"
    return "No return activity"


def needs_attention(d: Delivery) -> bool:
    """Stages where money or stock is exposed and a person should act."""
    return stage(d) in {"Received - credit pending", "Credited - physical receipt unconfirmed"} or d.carrier_claim_open
