import pytest

from src.manager import Manager
from src.models import Parameters, TenantSettlement


def test_settlements_for_three_tenants():
    manager = Manager(Parameters())
    settlements = manager.create_tenant_settlements('apart-polanka', 2025, 1)

    assert len(settlements) == 3
    for settlement in settlements:
        assert isinstance(settlement, TenantSettlement)
        assert settlement.apartment_settlement == 'apart-polanka'
        assert settlement.year == 2025
        assert settlement.month == 1
        assert settlement.bills_pln == pytest.approx(910.0 / 3)
        assert settlement.rent_pln == pytest.approx(760.0 / 3)
        assert settlement.total_due_pln == pytest.approx(910.0 / 3)
    assert sum(s.bills_pln for s in settlements) == pytest.approx(910.0)


def test_settlements_for_two_tenants():
    manager = Manager(Parameters())
    del manager.tenants['tenant-3']
    settlements = manager.create_tenant_settlements('apart-polanka', 2025, 1)

    assert len(settlements) == 2
    assert settlements[0].bills_pln == 455.0
    assert settlements[1].bills_pln == 455.0
    assert settlements[0].tenant != settlements[1].tenant


def test_settlement_for_one_tenant():
    manager = Manager(Parameters())
    del manager.tenants['tenant-2']
    del manager.tenants['tenant-3']
    settlements = manager.create_tenant_settlements('apart-polanka', 2025, 1)

    assert len(settlements) == 1
    assert settlements[0].tenant == 'tenant-1'
    assert settlements[0].bills_pln == 910.0
    assert settlements[0].rent_pln == 760.0
    assert settlements[0].total_due_pln == 910.0


def test_no_settlements_when_no_tenants():
    manager = Manager(Parameters())
    manager.tenants.clear()
    settlements = manager.create_tenant_settlements('apart-polanka', 2025, 1)

    assert settlements == []


def test_tenants_settlement_when_no_bills_in_month():
    manager = Manager(Parameters())
    settlements = manager.create_tenant_settlements('apart-polanka', 2025, 7)

    assert len(settlements) == 3
    assert settlements[0].bills_pln == 0.0
    assert settlements[0].total_due_pln == 0.0


def test_no_settlements_for_nonexistent_apartment():
    manager = Manager(Parameters())
    assert manager.create_tenant_settlements('apart-nieistnieje', 2025, 1) == []
