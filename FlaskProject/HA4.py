from sqlalchemy import (
    create_engine,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Numeric,
    Boolean,
    Identity,
    func
)
from sqlalchemy.orm import sessionmaker, relationship, Mapped, mapped_column
from sqlalchemy.orm import declarative_base
from datetime import datetime


Base = declarative_base()
engine = create_engine('sqlite:///:memory:')


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255))

    products: Mapped[list['Product']] = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'), nullable=False)

    category: Mapped['Category'] = relationship("Category", back_populates="products")


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


categories = [
    Category(name="Электроника", description="Гаджеты и устройства."),
    Category(name="Книги", description="Печатные книги и электронные книги."),
    Category(name="Одежда", description="Одежда для мужчин и женщин.")
]
session.add_all(categories)
session.commit()


category_map = {category.name: category.id for category in session.query(Category).all()}


products = [
    Product(name="Смартфон", price=299.99, in_stock=True, category_id=category_map["Электроника"]),
    Product(name="Ноутбук", price=499.99, in_stock=True, category_id=category_map["Электроника"]),
    Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category_id=category_map["Книги"]),
    Product(name="Джинсы", price=40.50, in_stock=True, category_id=category_map["Одежда"]),
    Product(name="Футболка", price=20.00, in_stock=True, category_id=category_map["Одежда"])
]

session.add_all(products)
session.commit()



print("\nСписок категорий и их продуктов:")
categories_with_products = session.query(Category).all()

for category in categories_with_products:
    print(f"\nКатегория: {category.name} - {category.description}")
    for product in category.products:
        print(f"  - {product.name}, Цена: {product.price}")




smartphone = session.query(Product).filter_by(name="Смартфон").first()

if smartphone:
    print(f"\nОбновление цены для {smartphone.name}: {smartphone.price} → 349.99")
    smartphone.price = 349.99
    session.commit()
else:
    print("\nСмартфон не найден в базе данных.")


updated_smartphone = session.query(Product).filter_by(name="Смартфон").first()
print(f"\nНовая цена смартфона: {updated_smartphone.price}")


session.close()
