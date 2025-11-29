# ---------- PRODUCT SCHEMAS ----------

class ProductBase(BaseModel):
    title: str
    description: str | None = None
    price: float


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


# ---------- CART SCHEMAS ----------

class CartItemBase(BaseModel):
    product_id: int
    quantity: int


class CartItem(CartItemBase):
    id: int

    class Config:
        orm_mode = True


class Cart(BaseModel):
    id: int
    items: list[CartItem] = []

    class Config:
        orm_mode = True


# ---------- USER SCHEMAS ----------

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    # we ignore password in DB, email is enough
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


# ---------- ORDER SCHEMAS ----------

class Order(BaseModel):
    id: int
    total: float

    class Config:
        orm_mode = True
