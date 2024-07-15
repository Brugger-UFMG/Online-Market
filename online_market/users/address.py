from __future__ import annotations


class Address:
    def __init__(
        self,
        street: str,
        city: str,
        state: str,
        zip_code: str,
        house_number: int,
        complement: str,
    ):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.house_number = house_number
        self.complement = complement

    @staticmethod
    def from_dict(data: dict) -> Address:
        return Address(**data)

    def to_dict(self) -> dict:
        """
        Transforma o objeto em um dicionário.

        Returns
        -------
        dict
            Dicionário
        """
        return {
            "street": self.street,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "house_number": self.house_number,
            "complement": self.complement,
        }

    def __repr__(self) -> str:
        return f"Address(street={self.street}, city={self.city}, state={self.state}, zip_code={self.zip_code}, house_number={self.house_number}, complement={self.complement})"
