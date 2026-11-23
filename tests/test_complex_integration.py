import pytest

from src.manager import Manager
from src.models import Parameters


def test_apartment_does_not_exist():
    manager = Manager(Parameters())
    with pytest.raises(KeyError):
        manager.get_apartment_costs('apart-nieistnieje', 2025, 1)


def test_no_bills_in_month():
    manager = Manager(Parameters())
    assert manager.get_apartment_costs('apart-polanka', 2025, 7) == 0.0


def test_same_year_different_month():
    manager = Manager(Parameters())
    assert manager.get_apartment_costs('apart-polanka', 2025, 2) == 0.0


def test_bills_in_month():
    manager = Manager(Parameters())
    # rent 760.0 + electricity 150.0
    assert manager.get_apartment_costs('apart-polanka', 2025, 1) == 910.0
