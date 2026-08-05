from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.package import Package
from app.schemas.package import PackageCreate, PackageUpdate


def get_package_by_name(db: Session, name: str) -> Package | None:
    return db.query(Package).filter(Package.name == name).first()

def get_package_by_id(db: Session, id: UUID) -> Package | None:
    return db.query(Package).filter(Package.id == id).first()

def get_packages(db: Session, skip: int = 0, limit: int = 100) -> list[Package]:
    return db.query(Package).offset(skip).limit(limit).all()

def create_package(db: Session, package_in: PackageCreate) -> Package:
    db_obj = Package(
        name=package_in.name,
        description=package_in.description,
        organization_id=package_in.organization_id,
        is_verified=False
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_package(db: Session, db_obj: Package, package_in: PackageUpdate) -> Package:
    update_data = package_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
