from minio import Minio
from minio.error import S3Error
from fastapi import Depends
from typing import Annotated
from app.configs import Config

config = Config()

# Initialize MinIO client
minio_client = Minio(
    endpoint=config.MINIO_ENDPOINT,
    access_key=config.MINIO_ROOT_USER,
    secret_key=config.MINIO_ROOT_PASSWORD,
    secure=config.MINIO_SECURE,
)


def init_storage():
    """
    Initialize storage by ensuring the bucket exists.
    This is already handled by docker-compose s3-setup service,
    but we check here for robustness.
    """
    try:
        bucket_name = config.MINIO_BUCKET_NAME
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            print(f"✅ Bucket '{bucket_name}' created successfully")
        else:
            print(f"✅ Bucket '{bucket_name}' already exists")
    except S3Error as e:
        print(f"❌ Error initializing storage: {e}")
        raise


def get_minio_client() -> Minio:
    """
    Dependency injection for MinIO client.
    Use this in FastAPI route dependencies.
    """
    return minio_client


# Type annotation for dependency injection (similar to SessionDep)
MinioDep = Annotated[Minio, Depends(get_minio_client)]

# Initialize storage on module import
init_storage()
