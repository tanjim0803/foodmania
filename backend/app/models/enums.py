import enum


class Roles(str, enum.Enum):
    CUSTOMER = "customer"
    RIDER = "rider"
    SELLER = "seller"
    ADMIN = "admin"
