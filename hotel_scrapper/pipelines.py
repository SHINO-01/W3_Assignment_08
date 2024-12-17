import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String, nullable=False)
    title = Column(String, nullable=False)
    rating = Column(String, nullable=True)
    location = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    room_type = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    images = Column(String, nullable=True)
    url = Column(String, nullable=False)

class HotelScrapperPipeline:
    def __init__(self):
        DATABASE_URL = "postgresql://scrapy_user:scrapy_pass@postgres:5432/scrapyDB"
        self.engine = sqlalchemy.create_engine(DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def process_item(self, item, spider):
        session = self.Session()
        try:
            hotel = Hotel(**item)
            session.add(hotel)
            session.commit()
            spider.log(f"Successfully added to database: {item}")
        except Exception as e:
            spider.log(f"Error adding to database: {e}")
            session.rollback()
        finally:
            session.close()
        return item
