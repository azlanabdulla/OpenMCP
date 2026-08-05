import uuid

from sqlalchemy.orm import Session

from app.db.models.package import Version
from app.schemas.version import VersionCreate


def get_version_by_package_and_string(db: Session, package_id: uuid.UUID, version_string: str) -> Version | None:
    return db.query(Version).filter(
        Version.package_id == package_id,
        Version.version_string == version_string
    ).first()

def get_versions_by_package(db: Session, package_id: uuid.UUID) -> list[Version]:
    return db.query(Version).filter(Version.package_id == package_id).all()

def create_version(db: Session, package_id: uuid.UUID, version_in: VersionCreate) -> Version:
    db_obj = Version(
        package_id=package_id,
        version_string=version_in.version_string,
        manifest_data=version_in.manifest_data.model_dump(),
        tarball_url=version_in.tarball_url,
        checksum=version_in.checksum
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
