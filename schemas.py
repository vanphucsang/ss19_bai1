from pydantic import BaseModel
from typing import Optional, List


class WarehouseCreate(BaseModel):
    warehouse_name: str
    location: str


class PackageResponse(BaseModel):
    id: int
    package_code: str
    weight: float
    warehouse_id: int

    class Config:
        from_attributes = True


class WarehouseDetailResponse(BaseModel):
    id: int
    warehouse_name: str
    location: str
    packages: List[PackageResponse] = []

    class Config:
        from_attributes = True


class PackageUpdate(BaseModel):
    package_code: Optional[str] = None
    weight: Optional[float] = None


class WaybillResponse(BaseModel):
    id: int
    tracking_number: str
    shipping_status: str
    package_id: int

    class Config:
        from_attributes = True
