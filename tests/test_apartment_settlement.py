from src.manager import Manager
from src.models import Parameters, ApartmentSettlement


def test_settlement_for_apartment_with_bills():
    manager = Manager(Parameters())
    settlement = manager.create_apartment_settlement('apart-polanka', 2025, 1)

    assert isinstance(settlement, ApartmentSettlement)
    assert settlement.apartment == 'apart-polanka'
    assert settlement.year == 2025
    assert settlement.month == 1
    assert settlement.total_rent_pln == 760.0
    assert settlement.total_bills_pln == 910.0
    assert settlement.total_due_pln == 910.0


def test_settlement_for_apartment_without_bills_in_month():
    manager = Manager(Parameters())
    settlement = manager.create_apartment_settlement('apart-polanka', 2025, 7)

    assert settlement.apartment == 'apart-polanka'
    assert settlement.year == 2025
    assert settlement.month == 7
    assert settlement.total_rent_pln == 0.0
    assert settlement.total_bills_pln == 0.0
    assert settlement.total_due_pln == 0.0


def test_settlement_for_nonexistent_apartment():
    manager = Manager(Parameters())
    assert manager.create_apartment_settlement('apart-nieistnieje', 2025, 1) is None
