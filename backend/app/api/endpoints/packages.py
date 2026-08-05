import hashlib
import json
from typing import Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api import deps
from app.db.models.user import User
from app.schemas.package import PackageCreate, PackageRead
from app.schemas.version import ManifestData, VersionCreate, VersionRead
from app.services import package_service, version_service
from app.services.storage import storage

router = APIRouter()

@router.get("/", response_model=list[PackageRead])
def get_packages(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve a list of packages.
    """
    packages = package_service.get_packages(db, skip=skip, limit=limit)
    return packages

@router.get("/{name}", response_model=PackageRead)
def get_package_by_name(
    name: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get detailed information about a package.
    """
    package = package_service.get_package_by_name(db, name=name)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return package

@router.post("/", response_model=PackageRead)
def create_package(
    *,
    db: Session = Depends(deps.get_db),
    package_in: PackageCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Register a new package namespace.
    """
    package = package_service.get_package_by_name(db, name=package_in.name)
    if package:
        raise HTTPException(status_code=400, detail="Package with this name already exists")
    
    # In a full implementation, check if user is allowed to create in this namespace/organization
    package = package_service.create_package(db, package_in)
    return package

@router.post("/{name}/versions", response_model=VersionRead)
async def publish_package_version(
    name: str,
    manifest: str = Form(...),
    tarball: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Publish a new version of a package.
    Requires uploading the `manifest.json` string and the tarball file.
    """
    # 1. Verify package exists and user has permission
    package = package_service.get_package_by_name(db, name=name)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found. You must register the package namespace first.")
    
    # 2. Parse and validate manifest
    try:
        manifest_dict = json.loads(manifest)
        manifest_data = ManifestData(**manifest_dict)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid manifest data: {e!s}")
        
    if manifest_data.name != name:
         raise HTTPException(status_code=400, detail="Manifest name does not match package namespace.")

    # 3. Check version uniqueness
    existing_version = version_service.get_version_by_package_and_string(
        db, package_id=package.id, version_string=manifest_data.version
    )
    if existing_version:
        raise HTTPException(status_code=400, detail=f"Version {manifest_data.version} already exists for this package.")

    # 4. Process and upload tarball
    content = await tarball.read()
    checksum = hashlib.sha256(content).hexdigest()
    
    # Stub: Upload to S3
    tarball_url = storage.upload_file(content, filename=tarball.filename or f"{name}-{manifest_data.version}.tgz")
    
    # 5. Save version to database
    version_in = VersionCreate(
        version_string=manifest_data.version,
        manifest_data=manifest_data,
        tarball_url=tarball_url,
        checksum=checksum
    )
    
    new_version = version_service.create_version(db, package_id=package.id, version_in=version_in)
    
    return new_version
