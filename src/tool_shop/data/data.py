import dataclasses
from typing import Optional

main_link = "http://localhost:4200/"

@dataclasses.dataclass
class Product:
    name: Optional[str] = None
    price: Optional[float] = None
    co2: Optional[chr] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    id: Optional[str] = None


SCREWS = Product(
    name = "Screws",
    price = None,
    co2 = '',
    category = "",
    brand = "",
    id = ""
)