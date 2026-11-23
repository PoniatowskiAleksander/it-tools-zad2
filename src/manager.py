from src.models import Apartment, ApartmentSettlement, Bill, Parameters, Tenant, Transfer


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 
        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def get_apartment_costs(self, apartment_key: str, year: int | None = None, month: int | None = None) -> float | None:
        """Suma rachunków mieszkania. Bez miesiąca - cały rok, bez roku - cała historia.
        Zwraca None, gdy mieszkanie nie istnieje. Rzuca ValueError dla miesiąca spoza 1-12."""
        if month is not None and not 1 <= month <= 12:
            raise ValueError(f"Nieprawidłowy miesiąc: {month}")
        if apartment_key not in self.apartments:
            return None
        return sum(
            bill.amount_pln for bill in self.bills
            if bill.apartment == apartment_key
            and (year is None or bill.settlement_year == year)
            and (month is None or bill.settlement_month == month)
        )

    def create_apartment_settlement(self, apartment_key: str, year: int, month: int) -> ApartmentSettlement | None:
        """Rozliczenie mieszkania za dany miesiąc (na razie bez przelewów i najemców)."""
        if apartment_key not in self.apartments:
            return None
        bills = [
            bill for bill in self.bills
            if bill.apartment == apartment_key
            and bill.settlement_year == year
            and bill.settlement_month == month
        ]
        total_rent = sum(bill.amount_pln for bill in bills if bill.type == 'rent')
        total_bills = sum(bill.amount_pln for bill in bills)
        return ApartmentSettlement(
            apartment=apartment_key,
            month=month,
            year=year,
            total_rent_pln=total_rent,
            total_bills_pln=total_bills,
            total_due_pln=total_bills
        )

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True