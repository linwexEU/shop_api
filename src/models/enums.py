from enum import Enum


class CategoriesEnum(Enum):
    Computers = "Computers"
    Phones = "Phones"
    Monitors = "Monitors"
    Legos = "Legos"
    Books = "Books"
    Keyboards = "Keyboards"
    Mouses = "Mouses"
    Electronics = "Electronics"


class UsersRoleEnum(Enum):
    Admin = "Admin"
    Customer = "Customer"
    Owner = "Owner"


class OrdersStateEnum(Enum):
    Preparing = "Preparing"
    Delivering = "Delivering"
    Done = "Done"
    Canceled = "Canceled"


class OrdersStateChangerEnum(Enum):
    Delivering = "Delivering"
    Done = "Done"
    Canceled = "Canceled"


class ActEnum(Enum):
    Like = "Like"
    Dislike = "Dislike"


class NotificationsStateEnum(Enum):
    Read = "Read"
    New = "New"


class NotificationsTypeEnum(Enum):
    OrderComplete = "Your order is completed!"
    NewOrder = "New order!"
