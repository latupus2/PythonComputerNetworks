from datetime import datetime
import contextlib

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql://askona_user:password@localhost/askona_parser"
Base = declarative_base()

class Product(Base):
    __tablename__ = 'parsed_products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String)
    price = Column(String)
    rating = Column(String)
    reviews = Column(String)
    link = Column(String, unique=True)
    parse_date = Column(DateTime, default=datetime.utcnow)

class Database:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    @contextlib.contextmanager
    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def save_products(self, products):
        with self.get_session() as session:
            for product in products:
                db_product = Product(
                    name=product['name'],
                    type=product['type'],
                    price=product['price'],
                    rating=product['rating'],
                    reviews=product['reviews'],
                    link=product['link']
                )
                session.merge(db_product)
            session.commit()
            print(f"Saved {len(products)} products to the database")

    def get_products(self, limit=10):
        with self.get_session() as session:
            products = session.query(Product).order_by(Product.parse_date.desc()).limit(limit).all()
            return [
                {
                    "name": p.name,
                    "type": p.type,
                    "price": p.price,
                    "rating": p.rating,
                    "reviews": p.reviews,
                    "link": p.link,
                    "parse_date": p.parse_date.isoformat()
                }
                for p in products
            ]