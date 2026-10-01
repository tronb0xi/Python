from abc import ABC, abstractmethod

class Medicine(ABC):
    def __init__(self, name: str, quantity: int, price: float):
        if not isinstance(name, str):
            raise TypeError("Поле 'name' має бути строкою (str).")
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise TypeError("Поле 'quantity' має бути цілим числом (int).")
        if not isinstance(price, (int, float)) or isinstance(price, bool):
            raise TypeError("Поле 'price' має бути числом (float/int).")

        self.name = name
        self.quantity = quantity
        self.price = float(price)

    @abstractmethod
    def requires_prescription(self) -> bool:
        pass

    @abstractmethod
    def storage_requirements(self) -> str:
        pass

    def total_price(self) -> float:
        return self.quantity * self.price

    @abstractmethod
    def info(self) -> str:
        pass

class Antibiotic(Medicine):
    def requires_prescription(self) -> bool:
        return True

    def storage_requirements(self) -> str:
        return "8–15°C, темне місце"

    def info(self) -> str:
        prescription = "Так" if self.requires_prescription() else "Ні"
        return (
            f"[Антибіотик] {self.name} | Кількість: {self.quantity} шт. | "
            f"Ціна: {self.price} грн | Разом: {self.total_price():.2f} грн | "
            f"Рецепт: {prescription} | Умови: {self.storage_requirements()}"
        )

class Vitamin(Medicine):
    def requires_prescription(self) -> bool:
        return False

    def storage_requirements(self) -> str:
        return "15–25°C, сухо"

    def info(self) -> str:
        prescription = "Так" if self.requires_prescription() else "Ні"
        return (
            f"[Вітамін] {self.name} | Кількість: {self.quantity} шт. | "
            f"Ціна: {self.price} грн | Разом: {self.total_price():.2f} грн | "
            f"Рецепт: {prescription} | Умови: {self.storage_requirements()}"
        )

class Vaccine(Medicine):
    def requires_prescription(self) -> bool:
        return True

    def storage_requirements(self) -> str:
        return "2–8°C, холодильник"

    def total_price(self) -> float:
        base_total = super().total_price()
        return base_total * 1.10

    def info(self) -> str:
        prescription = "Так" if self.requires_prescription() else "Ні"
        return (
            f"[Вакцина] {self.name} | Кількість: {self.quantity} шт. | "
            f"Базова ціна: {self.price} грн | Разом (+10%): {self.total_price():.2f} грн | "
            f"Рецепт: {prescription} | Умови: {self.storage_requirements()}"
        )