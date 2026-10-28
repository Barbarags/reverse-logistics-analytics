import pathlib, sys
from datetime import date
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "reference_implementation"))
from return_stage import Delivery, stage, needs_attention


def test_closed_when_received_and_credited():
    assert stage(Delivery("D1", "A", date(2026, 3, 1))) == "Closed - received and credited"

def test_credit_without_receipt_needs_attention():
    d = Delivery("D2", "A")
    assert stage(d) == "Credited - physical receipt unconfirmed" and needs_attention(d)

def test_received_without_credit_needs_attention():
    d = Delivery("D3", None, date(2026, 3, 1))
    assert stage(d) == "Received - credit pending" and needs_attention(d)

def test_virtual_credit_is_not_a_physical_return():
    assert stage(Delivery("D4", "B")) == "Virtual credit (no physical return expected)"

def test_in_transit():
    assert stage(Delivery("D5", "C")) == "Returning - in transit"

def test_open_carrier_claim_flags_attention_even_when_closed():
    assert needs_attention(Delivery("D6", "A", date(2026, 3, 1), carrier_claim_open=True))

def test_no_activity():
    assert stage(Delivery("D7")) == "No return activity" and not needs_attention(Delivery("D7"))
