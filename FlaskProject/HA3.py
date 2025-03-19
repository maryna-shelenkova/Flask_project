from sqlalchemy import create_engine, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship, sessionmaker

engine = create_engine("sqlite:///:memory:", echo=True, echo_pool=True)
Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))

    products: Mapped["Product"] = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    in_stock: Mapped[bool] = mapped_column(Boolean)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))

    category: Mapped["Category"] = relationship("Category", back_populates="products")


Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
session.close()


category = [Category(name="Toys", description="Toys"), Category(name="Toys1", description="Toys1"),Category(name="Toys2", description="Toys2")]
session.add_all(category)
session.commit()
#
records = session.query(Category).filter_by(id=2).all()
for record in records:
    print(record.name, record.description)






