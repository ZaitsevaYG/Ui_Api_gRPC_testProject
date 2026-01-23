from dataclasses import dataclass, field
from typing import Optional, List

from config import Config


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
            self.url = f"{Config.UI_BASE_URL}product/{self.id}"
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
    id= "01KDG94CN5W4A9ZRNE8K3TPT1G"
)

MEASURINGTAPE = Product(
    name = 'Measuring Tape',
    price = 10.07,
    co2 = 'C',
    category = "Measures",
    brand = "ForgeFlex Tools",
    id = "01KDG94CPHM7DN0DEPE1BK869J"
)

WOODSAW = Product(
    name='Wood Saw',
    price=12.18,
    co2='B',
    category="Hand Saw",
    brand="ForgeFlex Tools",
    id="01KDG94CNH84PRRRYPVCT1CYRA"

)

LONGNOSEPILERS = Product(
    name='Long Nose Pliers',
    price=14.24,
    co2='D',
    category="Pliers",
    brand="MightyCraft Hardware",
    id="01KDG94CMMFR85Q8A0S4Z6PT2A"
)



@dataclass
class User:
    email: str
    password: str
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postcode: Optional[str] = None
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


TESTUSER1 = User(
    email='customer@practicesoftwaretesting.com',
    password='welcome01',
    street='Happy Street, 24',
    city='Amarillo',
    state='Texas',
    country='USA',
    postcode='64154',
    full_name='Jane Doe'
)


WRONGUSER = User(
    email='unexisting@email.com',
    password='qwerty'
)


GUESTUSER = User(
    email='quest_user@mail.com',
    password='',
    first_name='Barbara',
    last_name='Streisand',
    street='Big Street,14',
    city='New York',
    state='New York',
    country='USA',
    postcode='87564'
)