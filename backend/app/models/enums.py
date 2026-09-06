import enum


class RoleScope(str, enum.Enum):
    SELLER = "seller"
    RIDER = "rider"
    CUSTOMER = "customer"
