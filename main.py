from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated, Optional
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class WarehouseBase(BaseModel):
    warehouseID: int
    clientID: int
    location: str
    capacity: int

class packageBase(BaseModel):
    clientID: int
    warehouseID: int
    status: str
    orderID: Optional[int] = None
    driverID: Optional[int] = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/warehouses", status_code=status.HTTP_201_CREATED)
async def create_warehouse(warehouse: WarehouseBase, db: db_dependency):
    db_warehouse = models.Warehouse(
        WarehouseID=warehouse.warehouseID,
        ClientID=warehouse.clientID,
        location=warehouse.location,
        capacity=warehouse.capacity
    )
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse

@app.get("/warehouse", status_code=status.HTTP_200_OK)
async def read_all_warehouses(db: db_dependency):
    warehouses = db.query(models.Warehouse).all() 
    return warehouses

@app.get("/warehouse/{warehouse_id}", status_code=status.HTTP_200_OK)
async def read_warehouse(warehouse_id: int, db: db_dependency):
    warehouse = db.query(models.Warehouse).filter(models.Warehouse.WarehouseID == warehouse_id).first()
    if warehouse is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Warehouse not found')
    return warehouse

@app.post("/package", status_code=status.HTTP_201_CREATED)
async def create_package(package: packageBase, db: db_dependency):
    db_package = models.Package(
        ClientID=package.clientID,
        WarehouseID=package.warehouseID,
        status=package.status,
        OrderID=package.orderID,
        DriverID=package.driverID
    )
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    return db_package

@app.get("/package", status_code=status.HTTP_200_OK)
async def read_all_packages(db: db_dependency):
    packages = db.query(models.Package).all()
    return packages

@app.get("/package/{package_id}", status_code=status.HTTP_200_OK)
async def read_package(package_id: int, db: db_dependency):
    package = db.query(models.Package).filter(models.Package.PackageID == package_id).first()
    if package is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Package not found')
    return package

@app.get("/package/client/{client_id}", status_code=status.HTTP_200_OK)
async def read_packages_by_client(client_id: int, db: db_dependency):
    packages = db.query(models.Package).filter(models.Package.ClientID == client_id).all()
    return packages

@app.get("/package/warehouse/{warehouse_id}", status_code=status.HTTP_200_OK)
async def read_packages_by_warehouse(warehouse_id: int, db: db_dependency):
    packages = db.query(models.Package).filter(models.Package.WarehouseID == warehouse_id).all()
    return packages

@app.put("/package/{package_id}", status_code=status.HTTP_200_OK)
async def update_package_status(package_id: int, status: str, db: db_dependency):
    package = db.query(models.Package).filter(models.Package.PackageID == package_id).first()
    if package is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Package not found')
    package.status = status
    db.commit()
    db.refresh(package)
    return package

@app.delete("/package/{package_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_package(package_id: int, db: db_dependency):
    package = db.query(models.Package).filter(models.Package.PackageID == package_id).first()
    if package is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Package not found')
    db.delete(package)
    db.commit()
    return




