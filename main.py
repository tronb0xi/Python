from models import Antibiotic, Medicine, Vaccine, Vitamin

def print_medicines_info(medicines: list[Medicine]) -> None:
    for medicine in medicines:
        print(medicine.info())

if __name__ == "__main__":
    inventory: list[Medicine] = [
        Antibiotic(name="Амоксицилін", quantity=5, price=120.0),
        Vitamin(name="Вітамін C 1000мг", quantity=10, price=85.5),
        Vaccine(name="Вакцина проти грипу", quantity=2, price=450.0),
        Antibiotic(name="Азитроміцин", quantity=3, price=210.0),
    ]

    print("--- ЗВІТ ПО НАЯВНИХ МЕДИКАМЕНТАХ ---")
    print_medicines_info(inventory)