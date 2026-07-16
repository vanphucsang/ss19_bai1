from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from sqlalchemy.orm import Session
from datetime import datetime, timezone

import models
import schemas
import service
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Supply Chain Management API")


def build_response(status_code: int, data, message: str, path: str, error=None):
    return {
        "statusCode": status_code,
        "data": data,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "path": path,
        "error": error,
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=build_response(exc.status_code, None, exc.detail, str(request.url.path), exc.detail),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=build_response(422, None, "Validation error", str(request.url.path), exc.errors()),
    )


@app.post("/warehouses", status_code=201)
def create_warehouse(warehouse: schemas.WarehouseCreate, request: Request, db: Session = Depends(get_db)):
    new_warehouse = service.create_warehouse(db, warehouse)
    data = schemas.WarehouseDetailResponse.model_validate(new_warehouse).model_dump()
    return build_response(201, data, "Warehouse created successfully", str(request.url.path))


@app.get("/warehouses/{warehouse_id}", status_code=200)
def get_warehouse(warehouse_id: int, request: Request, db: Session = Depends(get_db)):
    warehouse = service.get_warehouse_detail(db, warehouse_id)
    data = schemas.WarehouseDetailResponse.model_validate(warehouse).model_dump()
    return build_response(200, data, "Warehouse retrieved successfully", str(request.url.path))


@app.patch("/packages/{package_id}", status_code=200)
def update_package(package_id: int, package_update: schemas.PackageUpdate, request: Request, db: Session = Depends(get_db)):
    package = service.update_package(db, package_id, package_update)
    data = schemas.PackageResponse.model_validate(package).model_dump()
    return build_response(200, data, "Package updated successfully", str(request.url.path))


@app.delete("/waybills/{waybill_id}", status_code=200)
def delete_waybill(waybill_id: int, request: Request, db: Session = Depends(get_db)):
    waybill = service.delete_waybill(db, waybill_id)
    data = schemas.WaybillResponse.model_validate(waybill).model_dump()
    return build_response(200, data, "Waybill deleted successfully", str(request.url.path))
