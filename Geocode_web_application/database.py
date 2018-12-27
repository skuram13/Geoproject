from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db_string = 'postgres://tazoxgldowebdu:d1676ea6a1add2937b87f7024a7a1adbd8634f18c618b7e964a3f6f9154b67ad@ec2-54-235-178-189.compute-1.amazonaws.com:5432/d1fv92bu0oqtcr?sslmode=require'

# 'postgresql://postgres:postgres@localhost/geocode_db'

db = create_engine(db_string)
base = declarative_base()

class geocode_cls(base):
    __tablename__= 'geocoder_tbl'

    ID = Column(String, primary_key=True)
    Address = Column(String)
    Name = Column(String)
    Employees = Column(String)
    # coordinates = Column(String)
    Latitude = Column(String)
    Longitude = Column(String)

Session = sessionmaker(db)
session = Session()
base.metadata.create_all(db)



