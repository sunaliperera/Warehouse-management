from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Warehouse(Base):
    __tablename__ = "warehouses"

    WarehouseID = Column(Integer, primary_key=True, index=True)
    location = Column(String(255), index=True)
    capacity = Column(Integer)

class Package(Base):
    __tablename__ = "package"

    PackageID = Column(Integer, primary_key=True, index=True)
    ClientID = Column(Integer, index=True)
    WarehouseID = Column(Integer, index=True)
    status = Column(String(127), index=True)

    
