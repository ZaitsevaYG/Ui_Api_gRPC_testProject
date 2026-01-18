from dataclasses import dataclass, field
from typing import Optional

main_link = "http://localhost:4200/"

@dataclass
class Product:
    name: Optional[str] = None
    price: Optional[float] = None
    co2: Optional[chr] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    id: Optional[str] = None
    url: Optional[str] = field(init=False)


    def __post_init__(self):
        if self.id:
            self.url = f"{main_link}product/{self.id}"
        else:
            self.url = None


SCREWS = Product(
    name = "Screws",
    price = None,
    co2 = '',
    category = "",
    brand = "",
    id = "",

)

THORHUMMER = Product(
    name = 'Thor Hammer',
    price = 11.14,
    co2 = 'D',
    category = "Hammer",
    brand = "ForgeFlex Tools",
    id="01KDG94CN5W4A9ZRNE8K3TPT1G"
)


@dataclass
class User:
    email: str
    password: str


TESTUSER1 = User(
    email='customer@practicesoftwaretesting.com',
    password='welcome01')