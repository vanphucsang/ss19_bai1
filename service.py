from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException
import models
import schemas


def create_warehouse(db: Session, warehouse: schemas.WarehouseCreate):
    try:
        new_warehouse = models.Warehouse(**warehouse.model_dump())
        db.add(new_warehouse)
        db.commit()
        db.refresh(new_warehouse)
        return new_warehouse
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Warehouse data violates a unique constraint")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while creating warehouse")


def get_warehouse_detail(db: Session, warehouse_id: int):
    warehouse = db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return warehouse


def update_package(db: Session, package_id: int, package_update: schemas.PackageUpdate):
    package = db.query(models.Package).filter(models.Package.id == package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    try:
        update_data = package_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(package, key, value)
        db.commit()
        db.refresh(package)
        return package
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Package data violates a unique constraint")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while updating package")


def delete_waybill(db: Session, waybill_id: int):
    waybill = db.query(models.Waybill).filter(models.Waybill.id == waybill_id).first()
    if not waybill:
        raise HTTPException(status_code=404, detail="Waybill not found")
    try:
        db.delete(waybill)
        db.commit()
        return waybill
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while deleting waybill")
